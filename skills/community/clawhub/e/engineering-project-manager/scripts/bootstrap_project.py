#!/usr/bin/env python3

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

WORKSPACE = Path.home() / ".openclaw" / "workspace"
PM = Path(__file__).resolve().parent.parent
TEMPLATES = PM / "templates"
STATE_ENGINE = PM / "scripts" / "project_state.py"

ARCHETYPES = {
    "desktop": ["SWE"],
    "mobile": ["SWE"],
    "website": ["SWE"],
    "saas": ["SWE", "CYBER"],
    "iot": ["SYS", "SWE", "HWE", "CYBER"],
    "home-automation": ["SYS", "SWE", "HWE", "CYBER"],
    "embedded": ["SYS", "SWE", "HWE"],
    "robot": ["SYS", "SWE", "HWE", "MECH"],
    "drone": ["SYS", "SWE", "HWE", "MECH", "CYBER"],
    "edge-ai": ["SYS", "SWE", "HWE", "MLE"],
    "ml": ["SWE", "MLE"],
    "custom": [],
}

DOMAIN_DIR = {
    "SYS": "system",
    "SWE": "software",
    "HWE": "hardware",
    "MLE": "machine-learning",
    "MECH": "mechanical",
    "CYBER": "cybersecurity",
}

REQ_PREFIX = {
    "SYS": "SYS",
    "SWE": "SWE",
    "HWE": "HWE",
    "MLE": "MLE",
    "MECH": "MEC",
    "CYBER": "CYB",
}

BASE_TEMPLATES = [
    "PROJECT.md",
    "PROCESS-SCOPE.md",
    "STANDARDS.md",
    "STATUS.md",
    "DECISIONS.md",
    "RISK-REGISTER.md",
    "QA-PLAN.md",
    "CONFIGURATION-PLAN.md",
    "TRACEABILITY.md",
    "REQUIREMENTS-SPECIFICATION.md",
    "ARCHITECTURE.md",
]

MLE_TEMPLATES = [
    "DATA-CARD.md",
    "MODEL-CARD.md",
]

STEPS = [
    "preflight",
    "structure",
    "task_engine",
    "git_init",
    "remote_create",
    "initial_push",
    "verification",
    "finalization",
]


class BootstrapError(RuntimeError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def command_exists(name):
    return shutil.which(name) is not None


def run(cmd, cwd=None, env=None, check=True, capture=False):
    cmd = [str(x) for x in cmd]

    if capture:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    else:
        print("+", " ".join(cmd))
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            text=True,
        )

    if check and result.returncode != 0:
        if capture:
            msg = (result.stderr or result.stdout or "").strip()
            raise BootstrapError(
                f"Command failed ({result.returncode}): "
                f"{' '.join(cmd)}\n{msg}"
            )

        raise BootstrapError(
            f"Command failed ({result.returncode}): "
            f"{' '.join(cmd)}"
        )

    return result


def git_config(key):
    result = run(
        ["git", "config", "--global", "--get", key],
        check=False,
        capture=True,
    )

    if result.returncode != 0:
        return ""

    return result.stdout.strip()


def normalize_host(value):
    value = value.strip()

    if "://" in value:
        parsed = urlparse(value)
        value = parsed.netloc

    return value.rstrip("/")


def host_and_port(host, scheme="https"):
    if host.startswith("[") and "]" in host:
        if "]:" in host:
            h, port = host.rsplit(":", 1)
            return h.strip("[]"), int(port)
        return host.strip("[]"), 443 if scheme == "https" else 80

    if ":" in host:
        h, port = host.rsplit(":", 1)

        if port.isdigit():
            return h, int(port)

    return host, 443 if scheme == "https" else 80


def network_check(host, scheme="https"):
    hostname, port = host_and_port(host, scheme)

    try:
        socket.getaddrinfo(hostname, port)
    except socket.gaierror as exc:
        raise BootstrapError(
            f"DNS resolution failed for {hostname}: {exc}"
        )

    try:
        with socket.create_connection(
            (hostname, port),
            timeout=5,
        ):
            pass
    except OSError as exc:
        raise BootstrapError(
            f"Unable to connect to {hostname}:{port}: {exc}"
        )


def required_templates(domains):
    required = list(BASE_TEMPLATES)

    if "MLE" in domains:
        required += MLE_TEMPLATES

    return required


def check_templates(domains):
    missing = []

    for name in required_templates(domains):
        if not (TEMPLATES / name).is_file():
            missing.append(name)

    if missing:
        raise BootstrapError(
            "Missing templates: " + ", ".join(missing)
        )


def check_state_engine():
    if not STATE_ENGINE.is_file():
        raise BootstrapError(
            f"State engine missing: {STATE_ENGINE}"
        )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "py_compile",
            str(STATE_ENGINE),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise BootstrapError(
            "Invalid project_state.py:\n"
            + result.stderr.strip()
        )


def check_git():
    if not command_exists("git"):
        raise BootstrapError("git is not installed.")

    name = git_config("user.name")
    email = git_config("user.email")

    if not name:
        raise BootstrapError(
            "Global git user.name not configured."
        )

    if not email:
        raise BootstrapError(
            "Global git user.email not configured."
        )

    return {
        "user_name": name,
        "user_email": email,
    }


def github_preflight():
    host = "github.com"

    if not command_exists("gh"):
        raise BootstrapError(
            "GitHub CLI 'gh' is not installed."
        )

    auth = run(
        ["gh", "auth", "status", "-h", host],
        check=False,
        capture=True,
    )

    auth_text = (
        (auth.stdout or "") + "\n" + (auth.stderr or "")
    )

    if auth.returncode != 0:
        raise BootstrapError(
            "GitHub CLI is not authenticated for github.com.\n"
            "Use: gh auth login -h github.com"
        )

    if "workflow" not in auth_text.lower():
        raise BootstrapError(
            "The GitHub token does not appear to have the "
            "scope 'workflow'.\n"
            "Use: gh auth refresh -h github.com -s workflow"
        )

    network_check(host, "https")

    return {
        "backend": "github",
        "profile": "GITHUB",
        "host": host,
        "scheme": "https",
    }


def github_setup_git():
    """Configure credentials only during the authorized provisioning phase."""
    setup = run(
        [
            "gh",
            "auth",
            "setup-git",
            "--hostname",
            "github.com",
        ],
        check=False,
        capture=True,
    )

    if setup.returncode != 0:
        msg = (
            setup.stderr
            or setup.stdout
            or "unknown error"
        ).strip()

        raise BootstrapError(
            "Unable to configure Git to use "
            f"GitHub CLI authentication:\n{msg}"
        )

def gitlab_preflight(host, scheme):
    host = normalize_host(host)

    if not command_exists("glab"):
        raise BootstrapError(
            "GitLab CLI 'glab' is not installed."
        )

    api = run(
        [
            "glab",
            "api",
            "user",
            "--hostname",
            host,
        ],
        check=False,
        capture=True,
    )

    if api.returncode != 0:
        msg = (
            api.stderr
            or api.stdout
            or "API GitLab inaccessible"
        ).strip()

        raise BootstrapError(
            f"Invalid GitLab API/authentication for {host}:\\n{msg}"
        )

    profile = (
        "GITLAB_SAAS"
        if host == "gitlab.com"
        else "GITLAB_SELF_MANAGED"
    )

    return {
        "backend": "gitlab",
        "profile": profile,
        "host": host,
        "scheme": scheme,
    }


def preflight(args, project, domains):
    print("=== BOOTSTRAP PREFLIGHT ===")

    check_templates(domains)
    print("PASS templates")

    check_state_engine()
    print("PASS project_state.py")

    git_info = check_git()
    print(
        "PASS git identity:",
        git_info["user_name"],
        f"<{git_info['user_email']}>",
    )

    if args.git_backend == "github":
        if args.git_host and normalize_host(args.git_host) != "github.com":
            raise BootstrapError(
                "This version handles GitHub via github.com. "
                "Use GitLab for self-managed GitLab "
                "instances."
            )

        backend = github_preflight()

    else:
        host = args.git_host or "gitlab.com"

        backend = gitlab_preflight(
            host,
            args.git_scheme,
        )

    print(
        "PASS backend:",
        backend["profile"],
        backend["host"],
    )

    if project.exists() and any(project.iterdir()):
        runtime = project / ".bootstrap-state.json"
        complete = project / "00-project/BOOTSTRAP-STATUS.json"

        if complete.exists():
            raise BootstrapError(
                "The project already exists and its bootstrap "
                "is declared COMPLETE."
            )

        if runtime.exists():
            print("PASS partial project detected: RESUME possible")
        else:
            raise BootstrapError(
                "The project folder exists and is not empty, "
                "but contains no V2 bootstrap state. "
                "Refusing to adopt it automatically."
            )
    else:
        print("PASS destination available")

    print("=== PREFLIGHT PASS ===")

    return backend

# ---------------------------------------------------------------------------
# CREATE / RESUME ENGINE
# ---------------------------------------------------------------------------

def copy_template_once(name, destination):
    src = TEMPLATES / name

    if not src.exists():
        raise BootstrapError(f"Missing template: {src}")

    destination.parent.mkdir(parents=True, exist_ok=True)

    if not destination.exists():
        shutil.copy2(src, destination)


def write_once(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text(content, encoding="utf-8")


def write_json_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")

    tmp.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    tmp.replace(path)


def write_json_once(path, data):
    """Resume a failed structure step without resetting existing registries."""
    if path.exists():
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise BootstrapError(f"Existing JSON is invalid: {path.name} ({type(exc).__name__})") from None
        return
    write_json_atomic(path, data)


def state_path(project):
    return project / ".bootstrap-state.json"


def new_state(summary, backend):
    return {
        "schema_version": 2,
        "state": "IN_PROGRESS",
        "created_at": now(),
        "updated_at": now(),
        "project": summary,
        "backend_profile": backend["profile"],
        "steps": {
            step: {
                "status": "PENDING",
                "updated_at": None,
                "error": None,
            }
            for step in STEPS
        },
        "last_error": None,
    }


def validate_resume(state, summary):
    old = state.get("project", {})

    keys = [
        "slug",
        "git_backend",
        "git_host",
        "repository",
    ]
    keys += [key for key in ("project", "archetype", "domains", "git_scheme", "git_protocol",
                            "default_branch", "visibility", "drive", "git_ssh_host", "git_ssh_port",
                            "setup_sha256") if key in old or key in summary]

    for key in keys:
        if old.get(key) != summary.get(key):
            raise BootstrapError(
                "Parameters incompatible with the existing bootstrap: "
                f"{key}: old={old.get(key)!r}, "
                f"new={summary.get(key)!r}"
            )


def load_or_create_state(project, summary, backend):
    path = state_path(project)

    if path.exists():
        with path.open(encoding="utf-8") as f:
            state = json.load(f)

        validate_resume(state, summary)

        if state.get("state") == "COMPLETE":
            raise BootstrapError(
                "The bootstrap is already COMPLETE."
            )

        print("RESUME existing bootstrap")
        return state

    state = new_state(summary, backend)
    write_json_atomic(path, state)
    return state


def save_state(project, state):
    state["updated_at"] = now()
    write_json_atomic(state_path(project), state)


def mark_step(project, state, step, status, error=None):
    state["steps"][step]["status"] = status
    state["steps"][step]["updated_at"] = now()
    state["steps"][step]["error"] = error

    if error:
        state["last_error"] = error

    save_state(project, state)


def execute_step(project, state, step, fn):
    current = state["steps"][step]["status"]

    if current == "PASS":
        print(f"SKIP {step}: already PASS")
        return

    print()
    print(f"=== {step.upper()} ===")

    mark_step(project, state, step, "RUNNING")

    try:
        fn()
    except Exception as exc:
        mark_step(
            project,
            state,
            step,
            "FAILED",
            str(exc),
        )
        raise

    mark_step(project, state, step, "PASS")
    print(f"PASS {step}")


def create_structure(project, domains):
    dirs = [
        "00-project/management",
        "01-requirements/stakeholder",
        "02-architecture",
        "03-development",
        "04-integration",
        "05-verification",
        "06-validation",
        "07-quality/REVIEWS",
        "08-configuration",
        "09-risks",
        "10-changes",
        "11-metrics",
        "12-releases",
        "13-deliverables",
        "99-archive",
    ]

    for domain in domains:
        d = DOMAIN_DIR[domain]

        dirs += [
            f"01-requirements/{d}",
            f"02-architecture/{d}",
            f"03-development/{d}",
            f"05-verification/{d}",
        ]

    for directory in dirs:
        (project / directory).mkdir(
            parents=True,
            exist_ok=True,
        )


def _create_git_files_base(project, backend):
    write_once(
        project / ".gitignore",
        """# Bootstrap runtime
.bootstrap-state.json

# Secrets
.env
.env.*
*.key
*.pem

# Python
__pycache__/
*.pyc
.venv/

# Builds
build/
dist/
out/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Temporary
*.tmp
*.bak
~*

# Project Manager runtime locks
08-configuration/.change-requests.lock
08-configuration/.baselines.lock
05-verification/.evidence.lock
00-project/management/.tasks.lock
00-project/management/.milestones.lock
09-risks/.risks.lock
07-quality/.problems.lock
01-requirements/intake/.sources.lock
01-requirements/intake/.compliance.lock
""",
    )

    write_once(
        project / "README.md",
        "# Project Repository\n\n"
        "Managed by OpenClaw Project Manager.\n\n"
        "See `00-project/PROJECT.md` and "
        "`00-project/PROCESS-SCOPE.md`.\n",
    )

    if backend["backend"] == "github":
        write_once(
            project / ".github/workflows/governance.yml",
            """name: Governance

on:
  push:
  pull_request:

jobs:
  project-governance:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Check mandatory project files
        run: |
          test -f 00-project/PROJECT.md
          test -f 00-project/PROCESS-SCOPE.md
          test -f 00-project/STANDARDS.md
          test -f 00-project/BOOTSTRAP.json
          test -f 00-project/management/TASKS.json
          test -f 01-requirements/TRACEABILITY.md
          test -f 08-configuration/CONFIGURATION-PLAN.md
""",
        )

    else:
        write_once(
            project / ".gitlab-ci.yml",
            """stages:
  - governance

project-governance:
  stage: governance
  tags:
    - project-manager
  script:
    - test -f 00-project/PROJECT.md
    - test -f 00-project/PROCESS-SCOPE.md
    - test -f 00-project/STANDARDS.md
    - test -f 00-project/BOOTSTRAP.json
    - test -f 00-project/management/TASKS.json
    - test -f 01-requirements/TRACEABILITY.md
    - test -f 08-configuration/CONFIGURATION-PLAN.md
""",
        )


def _install_project_audit_tooling_base(project, backend):
    from pathlib import Path
    import shutil

    project = Path(project)

    source_dir = Path(__file__).resolve().parent
    target_dir = project / "tools" / "project-audit"

    target_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    scripts = [
        "pm_common.py",
        "project_state.py",
        "project_report.py",
        "delegation_plan.py",
        "migration_assess.py",
        "project_audit.py",
        "requirements_lint.py",
        "traceability_check.py",
        "domain_audit.py",
        "change_manager.py",
        "baseline_manager.py",
        "configuration_audit.py",
        "verification_evidence.py",
        "verification_evidence_audit.py",
        "release_check.py",
        "management_common.py",
        "management_init.py",
        "management_audit.py",
        "risk_manager.py",
        "problem_manager.py",
        "milestone_manager.py",
        "intake_manager.py",
        "compliance_manager.py",
    ]

    for name in scripts:
        src = source_dir / name

        if not src.exists():
            raise BootstrapError(
                f"Missing Project Manager audit: {src}"
            )

        if not (target_dir / name).exists():
            shutil.copy2(src, target_dir / name)

    readme = """# Project Audit Tooling

These audit tools are generated and controlled by the
OpenClaw Project Manager bootstrap.

Normal CI quality checks:

- project_audit.py
- requirements_lint.py
- traceability_check.py
- configuration_audit.py
- management_audit.py

release_check.py is the strict release gate and is not
executed on every development commit.
"""

    write_once(target_dir / "README.md", readme)

    backend_name = (
        backend.get("backend")
        if isinstance(backend, dict)
        else str(backend)
    )

    if backend_name == "gitlab":
        gitlab_ci = """stages:
  - governance
  - quality
  - release

project-governance:
  stage: governance
  tags:
    - project-manager
  script:
    - test -f 00-project/PROJECT.md
    - test -f 00-project/PROCESS-SCOPE.md
    - test -f 00-project/STANDARDS.md
    - test -f 00-project/BOOTSTRAP.json
    - test -f 00-project/management/TASKS.json
    - test -f 01-requirements/TRACEABILITY.md
    - test -f 08-configuration/CONFIGURATION-PLAN.md

project-quality:
  stage: quality
  tags:
    - project-manager
  script:
    - python3 tools/project-audit/project_audit.py .
    - python3 tools/project-audit/requirements_lint.py .
    - python3 tools/project-audit/traceability_check.py .
    - python3 tools/project-audit/domain_audit.py .
    - python3 tools/project-audit/configuration_audit.py .
    - python3 tools/project-audit/management_audit.py .

release-gate:
  stage: release
  tags:
    - project-manager
  script:
    - python3 tools/project-audit/release_check.py .
  rules:
    - if: '$CI_COMMIT_TAG'
      when: on_success
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
      allow_failure: true
    - when: never
"""

        if "ci_runner_tags" in backend:
            tags = backend["ci_runner_tags"]
            tag_block = "  tags:\n" + "".join("    - " + json.dumps(tag) + "\n" for tag in tags) if tags else ""
            gitlab_ci = gitlab_ci.replace("  tags:\n    - project-manager\n", tag_block)
        write_once(project / ".gitlab-ci.yml", gitlab_ci)

    elif backend_name == "github":
        workflow_dir = (
            project
            / ".github"
            / "workflows"
        )

        workflow_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        github_ci = """name: Project Quality

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  project-quality:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Project structure audit
        run: python3 tools/project-audit/project_audit.py .

      - name: Requirements lint
        run: python3 tools/project-audit/requirements_lint.py .

      - name: Traceability check
        run: python3 tools/project-audit/traceability_check.py .

      - name: Engineering domain audit
        run: python3 tools/project-audit/domain_audit.py .

      - name: Configuration management audit
        run: python3 tools/project-audit/configuration_audit.py .

      - name: Project management audit
        run: python3 tools/project-audit/management_audit.py .
"""

        write_once(workflow_dir / "project-quality.yml", github_ci)

    else:
        raise BootstrapError(
            f"Unsupported CI backend: {backend_name}"
        )

    print(
        "PASS project audit tooling:",
        backend_name,
    )


def install_project_audit_tooling(project, backend):
    from pathlib import Path

    _install_project_audit_tooling_base(
        project,
        backend,
    )

    backend_name = (
        backend.get("backend")
        if isinstance(backend, dict)
        else str(backend)
    )

    if backend_name != "github":
        return

    project = Path(project)

    workflow_dir = (
        project
        / ".github"
        / "workflows"
    )

    workflow_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    release_workflow = """name: Project Release Gate

on:
  push:
    tags:
      - "*"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  release-gate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Strict release gate
        run: python3 tools/project-audit/release_check.py .
"""

    write_once(workflow_dir / "project-release.yml", release_workflow)

    print("PASS GitHub release workflow")



def create_git_files(project, backend):
    install_project_audit_tooling(project, backend)
    _create_git_files_base(project, backend)




def _instantiate_project_before_work_products(project, args, summary, backend, domains):
    copy_template_once(
        "PROJECT.md",
        project / "00-project/PROJECT.md",
    )

    copy_template_once(
        "PROCESS-SCOPE.md",
        project / "00-project/PROCESS-SCOPE.md",
    )

    copy_template_once(
        "STANDARDS.md",
        project / "00-project/STANDARDS.md",
    )

    copy_template_once(
        "STATUS.md",
        project / "00-project/STATUS.md",
    )

    copy_template_once(
        "DECISIONS.md",
        project / "00-project/DECISIONS.md",
    )

    copy_template_once(
        "QA-PLAN.md",
        project / "07-quality/QA-PLAN.md",
    )

    copy_template_once(
        "RISK-REGISTER.md",
        project / "09-risks/RISK-REGISTER.md",
    )

    copy_template_once(
        "CONFIGURATION-PLAN.md",
        project / "08-configuration/CONFIGURATION-PLAN.md",
    )

    copy_template_once(
        "TRACEABILITY.md",
        project / "01-requirements/TRACEABILITY.md",
    )

    for domain in domains:
        d = DOMAIN_DIR[domain]
        prefix = REQ_PREFIX[domain]

        copy_template_once(
            "REQUIREMENTS-SPECIFICATION.md",
            project
            / "01-requirements"
            / d
            / f"{prefix}-REQUIREMENTS.md",
        )

        if domain in {"SYS", "SWE", "HWE", "MLE"}:
            copy_template_once(
                "ARCHITECTURE.md",
                project
                / "02-architecture"
                / d
                / f"{prefix}-ARCHITECTURE.md",
            )

    if "MLE" in domains:
        copy_template_once(
            "DATA-CARD.md",
            project
            / "03-development/machine-learning/DATA-CARD.md",
        )

        copy_template_once(
            "MODEL-CARD.md",
            project
            / "03-development/machine-learning/MODEL-CARD.md",
        )

    metadata = {
        "schema_version": 2,
        "project_title": args.title,
        "project_slug": args.slug,
        "archetype": args.archetype,
        "domains": domains,
        "git_backend": args.git_backend,
        "git_profile": backend["profile"],
        "git_host": backend["host"],
        "repository": args.repo,
        "visibility": args.visibility,
        "drive": args.drive_url,
        "created_at": now(),
    }

    write_json_once(
        project / "00-project/BOOTSTRAP.json",
        metadata,
    )

    write_once(
        project / "00-project/STORAGE-MAP.md",
        f"""# Storage Map

- Project: {args.title}
- Project Slug: {args.slug}
- Git Backend: {args.git_backend.upper()}
- Git Profile: {backend["profile"]}
- Git Host: {backend["host"]}
- Primary Repository: {args.repo}
- Google Drive: {args.drive_url or "DISABLED"}

## Canonical Rules

Git is mandatory and canonical for source code, configuration,
requirements, architecture, tests, CI/CD and reproducible engineering data.

Google Drive is optional and complementary.

If GitHub and GitLab are both used, exactly one remote must be
declared canonical.
""",
    )

    write_once(
        project / "08-configuration/CONFIGURATION-ITEMS.md",
        f"""# Configuration Items

| CI ID | Item | Type | Canonical Location | Status |
|---|---|---|---|---|
| CI-001 | Project repository | Git | {args.repo} | CONTROLLED |
""",
    )

    write_once(
        project / "08-configuration/BASELINES.md",
        "# Baselines\n\nModel version: 1.1\n\n"
        "| Baseline ID | Status | Purpose | Git Commit | Integrity Hash |\n"
        "|---|---|---|---|---|\n"
        "| - | No baselines | - | - | - |\n",
    )

    write_once(
        project / "08-configuration/CHANGE-REQUESTS.md",
        "# Change Requests\n\nModel version: 1.1\n\n"
        "| Change ID | Title | Status | Analysis Result | Current Assignee | Current Role |\n"
        "|---|---|---|---|---|---|\n"
        "| - | No Change Requests | - | - | - | - |\n",
    )

    write_json_once(
        project / "08-configuration/CONFIGURATION-MANAGEMENT.json",
        {
            "enabled": True,
            "model": "PROJECT_MANAGER_CONFIGURATION_MANAGEMENT",
            "model_version": "1.1",
            "enabled_at": now(),
            "enabled_by": "bootstrap_project.py",
        },
    )

    write_json_once(
        project / "08-configuration/CHANGE-REQUESTS.json",
        {
            "model": "PROJECT_MANAGER_CHANGE_MANAGEMENT",
            "model_version": "1.1",
            "registry_revision": 0,
            "next_number": 1,
            "changes": [],
        },
    )

    write_json_once(
        project / "08-configuration/BASELINE-REGISTRY.json",
        {
            "model": "PROJECT_MANAGER_BASELINE_MANAGEMENT",
            "model_version": "1.1",
            "registry_revision": 0,
            "next_number": 1,
            "baselines": [],
        },
    )

    (project / "08-configuration/changes").mkdir(
        parents=True,
        exist_ok=True,
    )
    (project / "08-configuration/baselines").mkdir(
        parents=True,
        exist_ok=True,
    )

    write_json_once(
        project / "05-verification/EVIDENCE-MANAGEMENT.json",
        {
            "enabled": True,
            "model": "PROJECT_MANAGER_VERIFICATION_EVIDENCE_MANAGEMENT",
            "model_version": "1.0",
            "enabled_at": now(),
            "enabled_by": "bootstrap_project.py",
        },
    )

    write_json_once(
        project / "05-verification/EVIDENCE.json",
        {
            "model": "PROJECT_MANAGER_VERIFICATION_EVIDENCE",
            "model_version": "1.0",
            "registry_revision": 0,
            "next_number": 1,
            "evidence": [],
        },
    )

    write_once(
        project / "05-verification/EVIDENCE.md",
        "# Verification Evidence\n\nModel version: 1.0\n\n"
        "| Evidence ID | Requirement | Status | Method | Scope | Activity | Process |\n"
        "|---|---|---|---|---|---|---|\n"
        "| - | No evidence records | - | - | - | - | - |\n",
    )

    (project / "05-verification/evidence").mkdir(
        parents=True,
        exist_ok=True,
    )


def instantiate_project(project, args, summary, backend, domains):
    from management_audit import MARKER, MODELS
    enable_management = (not (project / "00-project/PROJECT.md").exists()
                         or (project / MARKER).exists()
                         or any((project / relative).exists() for _, relative, _, _ in MODELS))
    # Persist the new-project opt-in before copying templates. A later copy
    # failure must not make the next run mistake this project for a legacy one.
    from management_init import initialize
    if enable_management:
        initialize(project, "Project coordinator")

    _instantiate_project_before_work_products(
        project,
        args,
        summary,
        backend,
        domains,
    )

    # DOMAIN WORK PRODUCTS AUTO-GENERATION
    for domain in domains:
        d = DOMAIN_DIR.get(domain)
        prefix = domain if domain in {"SYS", "SWE", "HWE", "MLE"} else None

        if not d or not prefix:
            continue

        if domain == "SYS":
            copy_template_once(
                "INTERFACE-SPECIFICATION.md",
                project
                / "02-architecture"
                / d
                / f"{prefix}-INTERFACE-SPECIFICATION.md",
            )

        if domain in {"SWE", "HWE"}:
            copy_template_once(
                "DETAILED-DESIGN.md",
                project
                / "03-design"
                / d
                / f"{prefix}-DETAILED-DESIGN.md",
            )

        if domain in {"SYS", "SWE", "HWE", "MLE"}:
            copy_template_once(
                "TEST-SPECIFICATION.md",
                project
                / "05-verification"
                / d
                / f"{prefix}-TEST-SPECIFICATION.md",
            )

            copy_template_once(
                "VERIFICATION-REPORT.md",
                project
                / "05-verification"
                / d
                / f"{prefix}-VERIFICATION-REPORT.md",
            )

    # CYBER WORK PRODUCTS AUTO-GENERATION
    if "CYBER" in domains:
        cyber_template_root = (
            Path(__file__).resolve().parent.parent
            / "templates"
        )

        cyber_outputs = {
            "CYBER-ARCHITECTURE.md":
                "02-architecture/cybersecurity/"
                "CYBER-ARCHITECTURE.md",

            "CYBER-THREAT-MODEL.md":
                "02-architecture/cybersecurity/"
                "CYBER-THREAT-MODEL.md",

            "CYBER-SECURITY-PLAN.md":
                "03-design/cybersecurity/"
                "CYBER-SECURITY-PLAN.md",

            "CYBER-TEST-SPECIFICATION.md":
                "05-verification/cybersecurity/"
                "CYBER-TEST-SPECIFICATION.md",

            "CYBER-VERIFICATION-REPORT.md":
                "05-verification/cybersecurity/"
                "CYBER-VERIFICATION-REPORT.md",
        }

        for template_name, relative_path in cyber_outputs.items():
            template_path = (
                cyber_template_root / template_name
            )

            if not template_path.is_file():
                raise FileNotFoundError(
                    f"Missing CYBER template: "
                    f"{template_path}"
                )

            destination = (
                project / relative_path
            )

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            # Resume-safe: never overwrite an existing
            # engineering work product.
            if not destination.exists():
                destination.write_text(
                    template_path.read_text(
                        encoding="utf-8"
                    ),
                    encoding="utf-8",
                )

    # MECH WORK PRODUCTS AUTO-GENERATION
    if "MECH" in domains:
        mech_template_root = (
            Path(__file__).resolve().parent.parent
            / "templates"
        )

        mech_outputs = {
            "MECH-ARCHITECTURE.md":
                "02-architecture/mechanical/"
                "MECH-ARCHITECTURE.md",

            "MECH-INTERFACE-SPECIFICATION.md":
                "02-architecture/mechanical/"
                "MECH-INTERFACE-SPECIFICATION.md",

            "MECH-DETAILED-DESIGN.md":
                "03-design/mechanical/"
                "MECH-DETAILED-DESIGN.md",

            "MECH-ASSEMBLY-SPECIFICATION.md":
                "03-design/mechanical/"
                "MECH-ASSEMBLY-SPECIFICATION.md",

            "MECH-TEST-SPECIFICATION.md":
                "05-verification/mechanical/"
                "MECH-TEST-SPECIFICATION.md",

            "MECH-VERIFICATION-REPORT.md":
                "05-verification/mechanical/"
                "MECH-VERIFICATION-REPORT.md",
        }

        for template_name, relative_path in mech_outputs.items():
            template_path = (
                mech_template_root / template_name
            )

            if not template_path.is_file():
                raise FileNotFoundError(
                    f"Missing MECH template: "
                    f"{template_path}"
                )

            destination = (
                project / relative_path
            )

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            # Resume-safe: never overwrite an
            # existing engineering work product.
            if not destination.exists():
                destination.write_text(
                    template_path.read_text(
                        encoding="utf-8"
                    ),
                    encoding="utf-8",
                )




def initialize_structure(project, args, summary, backend, domains):
    create_structure(project, domains)

    instantiate_project(
        project,
        args,
        summary,
        backend,
        domains,
    )

    if getattr(args, "setup_config", None):
        from project_setup import persist_project_setup
        persist_project_setup(project, args.setup_config)

    create_git_files(project, backend)


def initialize_task_engine(project, args):
    tasks = project / "00-project/management/TASKS.json"

    if tasks.exists():
        try:
            with tasks.open(encoding="utf-8") as f:
                json.load(f)
        except Exception as exc:
            raise BootstrapError(
                f"Existing TASKS.json is invalid: {exc}"
            )

        print("TASKS.json already present")
        return

    run([
        sys.executable,
        str(STATE_ENGINE),
        "init",
        str(project),
        "--title",
        args.title,
        "--slug",
        args.slug,
    ])


def git_has_head(project):
    result = run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=project,
        check=False,
        capture=True,
    )

    return result.returncode == 0


def _stage_bootstrap_files_base(project):
    paths = [
        ".gitignore",
        "README.md",
        "00-project",
        "01-requirements",
        "02-architecture",
        "03-development",
        "04-integration",
        "05-verification",
        "06-validation",
        "07-quality",
        "08-configuration",
        "09-risks",
        "10-changes",
        "11-metrics",
        "12-releases",
        "13-deliverables",
        "99-archive",
    ]

    if (project / ".github").exists():
        paths.append(".github")

    if (project / ".gitlab-ci.yml").exists():
        paths.append(".gitlab-ci.yml")

    existing = [
        item
        for item in paths
        if (project / item).exists()
    ]

    run(
        ["git", "add", "--", *existing],
        cwd=project,
    )


def _stage_bootstrap_files_before_github_release(project):
    from pathlib import Path

    project = Path(project)

    _stage_bootstrap_files_base(project)

    audit_dir = (
        project
        / "tools"
        / "project-audit"
    )

    if audit_dir.exists():
        run(
            [
                "git",
                "add",
                "--",
                "tools/project-audit",
            ],
            cwd=project,
        )

    ci_files = [
        ".gitlab-ci.yml",
        ".github/workflows/project-quality.yml",
    ]

    for rel in ci_files:
        if (project / rel).exists():
            run(
                [
                    "git",
                    "add",
                    "--",
                    rel,
                ],
                cwd=project,
            )


def stage_bootstrap_files(project):
    from pathlib import Path

    project = Path(project)

    _stage_bootstrap_files_before_github_release(
        project
    )

    release_workflow = (
        project
        / ".github"
        / "workflows"
        / "project-release.yml"
    )

    if release_workflow.exists():
        run(
            [
                "git",
                "add",
                "--",
                ".github/workflows/project-release.yml",
            ],
            cwd=project,
        )


    # STAGE DOMAIN DESIGN WORK PRODUCTS
    design_dir = project / "03-design"

    if design_dir.exists():
        run(
            [
                "git",
                "add",
                "--",
                "03-design",
            ],
            cwd=project,
        )





def initialize_git(project, args):
    branch_name = args.default_branch

    if not (project / ".git").exists():
        run(
            ["git", "init", "-b", branch_name],
            cwd=project,
        )

    branch = run(
        ["git", "branch", "--show-current"],
        cwd=project,
        check=False,
        capture=True,
    ).stdout.strip()

    if branch and branch != branch_name:
        raise BootstrapError(
            f"Unexpected local branch: {branch}. "
            f"Expected branch: {branch_name}."
        )

    stage_bootstrap_files(project)

    staged = run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=project,
        check=False,
        capture=True,
    )

    if staged.returncode == 1:
        message = (
            "chore: initialize controlled project structure"
            if not git_has_head(project)
            else "chore: resume project bootstrap"
        )

        run(
            ["git", "commit", "-m", message],
            cwd=project,
        )

    if not git_has_head(project):
        raise BootstrapError(
            "No Git commit has been created."
        )



def expected_remote_url(args, backend):
    host = backend["host"]

    if args.git_backend == "github":
        return f"https://github.com/{args.repo}.git"

    if args.git_protocol == "ssh":
        ssh_host = args.git_ssh_host or host_and_port(
            host,
            args.git_scheme,
        )[0]

        if args.git_ssh_port:
            return (
                f"ssh://git@{ssh_host}:"
                f"{args.git_ssh_port}/{args.repo}.git"
            )

        return f"git@{ssh_host}:{args.repo}.git"

    return (
        f"{args.git_scheme}://"
        f"{host}/{args.repo}.git"
    )


def normalize_remote_url(url):
    return url.strip().rstrip("/").removesuffix(".git")


def remote_repository_exists(args, backend):
    if args.git_backend == "github":
        result = run(
            [
                "gh",
                "repo",
                "view",
                args.repo,
                "--json",
                "nameWithOwner",
            ],
            check=False,
            capture=True,
        )

        return result.returncode == 0

    from urllib.parse import quote

    project_id = quote(
        args.repo,
        safe="",
    )

    result = run(
        [
            "glab",
            "api",
            f"projects/{project_id}",
            "--hostname",
            backend["host"],
        ],
        check=False,
        capture=True,
    )

    if result.returncode == 0:
        return True

    text = (
        (result.stdout or "")
        + "\\n"
        + (result.stderr or "")
    )

    if (
        "404" in text
        or "Not Found" in text
        or "not found" in text
    ):
        return False

    raise BootstrapError(
        "Unable to determine whether the GitLab project exists:\\n"
        + text.strip()
    )



def create_remote_repository(args, backend):
    if remote_repository_exists(args, backend):
        print("Remote repository already exists")
        return

    if args.git_backend == "github":
        visibility_flag = (
            "--private"
            if args.visibility == "private"
            else "--public"
        )

        run([
            "gh",
            "repo",
            "create",
            args.repo,
            visibility_flag,
        ])
        return

    from urllib.parse import quote

    if "/" not in args.repo:
        raise BootstrapError(
            "Invalid GitLab repository. "
            "Expected format: namespace/project"
        )

    namespace_path, project_path = args.repo.rsplit("/", 1)

    user_result = run(
        [
            "glab",
            "api",
            "user",
            "--hostname",
            backend["host"],
        ],
        capture=True,
    )

    try:
        current_user = json.loads(user_result.stdout)
        current_username = current_user["username"]
    except Exception as exc:
        raise BootstrapError(
            f"Invalid GitLab user API response: {exc}"
        )

    cmd = [
        "glab",
        "api",
        "projects",
        "--hostname",
        backend["host"],
        "-X",
        "POST",
        "-F",
        f"name={args.title}",
        "-F",
        f"path={project_path}",
        "-F",
        f"visibility={args.visibility}",
    ]

    if namespace_path != current_username:
        namespace_id_path = quote(
            namespace_path,
            safe="",
        )

        ns_result = run(
            [
                "glab",
                "api",
                f"namespaces/{namespace_id_path}",
                "--hostname",
                backend["host"],
            ],
            capture=True,
        )

        try:
            namespace = json.loads(ns_result.stdout)
            namespace_id = namespace["id"]
        except Exception as exc:
            raise BootstrapError(
                f"Invalid GitLab namespace "
                f"{namespace_path}: {exc}"
            )

        cmd += [
            "-F",
            f"namespace_id={namespace_id}",
        ]

    run(cmd)

    if not remote_repository_exists(args, backend):
        raise BootstrapError(
            "The GitLab project is not visible after its creation."
        )

    print(
        "GitLab project created:",
        args.repo,
    )





def configure_origin(project, args, backend):
    expected = expected_remote_url(args, backend)

    current = run(
        ["git", "remote", "get-url", "origin"],
        cwd=project,
        check=False,
        capture=True,
    )

    if current.returncode == 0:
        actual = current.stdout.strip()

        if (
            normalize_remote_url(actual)
            != normalize_remote_url(expected)
        ):
            raise BootstrapError(
                "The origin remote exists but points elsewhere.\n"
                f"Expected: {expected}\n"
                f"Actual:   {actual}"
            )

        print("origin already correctly configured")
        return

    run(
        ["git", "remote", "add", "origin", expected],
        cwd=project,
    )


def remote_create_step(project, args, backend):
    if args.git_backend == "github":
        github_setup_git()
    create_remote_repository(args, backend)
    configure_origin(project, args, backend)


def initial_push(project, args, backend):
    branch_name = args.default_branch

    run(
        [
            "git",
            "push",
            "-u",
            "origin",
            branch_name,
        ],
        cwd=project,
    )

    if args.git_backend == "gitlab":
        from urllib.parse import quote

        project_id = quote(
            args.repo,
            safe="",
        )

        run(
            [
                "glab",
                "api",
                f"projects/{project_id}",
                "--hostname",
                backend["host"],
                "-X",
                "PUT",
                "-F",
                f"default_branch={branch_name}",
            ],
        )

        check = run(
            [
                "glab",
                "api",
                f"projects/{project_id}",
                "--hostname",
                backend["host"],
            ],
            capture=True,
        )

        try:
            project_info = json.loads(check.stdout)
            actual = project_info.get("default_branch")
        except Exception as exc:
            raise BootstrapError(
                f"Invalid GitLab response after push: {exc}"
            )

        if actual != branch_name:
            raise BootstrapError(
                "Incorrect GitLab default branch. "
                f"Expected={branch_name}, actual={actual}"
            )

        print(
            "GitLab default branch:",
            actual,
        )

    run(
        [
            "git",
            "remote",
            "set-head",
            "origin",
            "-a",
        ],
        cwd=project,
        check=False,
    )




def remote_branch_sha(project, branch_name):
    result = run(
        [
            "git",
            "ls-remote",
            "origin",
            f"refs/heads/{branch_name}",
        ],
        cwd=project,
        capture=True,
    )

    text = result.stdout.strip()

    if not text:
        raise BootstrapError(
            f"The remote branch {branch_name} is missing."
        )

    return text.split()[0]



def verify_repository(project, args):
    branch_name = args.default_branch

    dirty = run(
        ["git", "status", "--porcelain"],
        cwd=project,
        capture=True,
    ).stdout.strip()

    if dirty:
        raise BootstrapError(
            "Working tree not clean:\n" + dirty
        )

    local_sha = run(
        ["git", "rev-parse", "HEAD"],
        cwd=project,
        capture=True,
    ).stdout.strip()

    remote_sha = remote_branch_sha(
        project,
        branch_name,
    )

    if local_sha != remote_sha:
        raise BootstrapError(
            "The local and remote commits differ.\n"
            f"Branch: {branch_name}\n"
            f"local : {local_sha}\n"
            f"remote: {remote_sha}"
        )

    print("Branch:", branch_name)
    print("Local HEAD:", local_sha)
    print("Remote HEAD:", remote_sha)



def finalization_step(project, args, backend):
    status_file = project / "00-project/BOOTSTRAP-STATUS.json"

    status = {
        "schema_version": 2,
        "state": "COMPLETE",
        "complete": True,
        "completed_at": now(),
        "git_backend": args.git_backend,
        "git_profile": backend["profile"],
        "git_host": backend["host"],
        "repository": args.repo,
        "default_branch": args.default_branch,
        "drive": args.drive_url,
    }

    write_json_atomic(status_file, status)

    run(
        [
            "git",
            "add",
            "--",
            "00-project/BOOTSTRAP-STATUS.json",
        ],
        cwd=project,
    )

    staged = run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=project,
        check=False,
        capture=True,
    )

    if staged.returncode == 1:
        run(
            [
                "git",
                "commit",
                "-m",
                "chore: record successful bootstrap",
            ],
            cwd=project,
        )

    run(
        [
            "git",
            "push",
            "origin",
            args.default_branch,
        ],
        cwd=project,
    )

    verify_repository(project, args)



def gitlab_transport_preflight(args):
    if args.git_protocol != "ssh":
        return

    host = args.git_ssh_host or host_and_port(args.git_host or "gitlab.com", args.git_scheme)[0]

    if not host:
        raise BootstrapError(
            "Missing GitLab SSH hostname."
        )

    cmd = [
        "ssh",
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=5",
    ]

    if args.git_ssh_port:
        cmd += ["-p", str(args.git_ssh_port)]

    cmd += ["-T", "git@" + host]

    result = run(
        cmd,
        check=False,
        capture=True,
    )

    output = (
        (result.stdout or "")
        + "\\n"
        + (result.stderr or "")
    )

    if "Welcome to GitLab" not in output:
        raise BootstrapError(
            "GitLab SSH authentication not validated.\\n"
            + output.strip()
        )

    print("PASS GitLab SSH:", host)

def robust_preflight(args, project, domains):
    print("=== BOOTSTRAP PREFLIGHT ===")

    check_templates(domains)
    print("PASS templates")

    check_state_engine()
    print("PASS project_state.py")

    git_info = check_git()

    print(
        "PASS git identity:",
        git_info["user_name"],
        f"<{git_info['user_email']}>",
    )

    if args.git_backend == "github":
        backend = github_preflight()
    else:
        backend = gitlab_preflight(
            args.git_host or "gitlab.com",
            args.git_scheme,
        )

    print(
        "PASS backend:",
        backend["profile"],
        backend["host"],
    )

    if args.git_backend == "gitlab":
        gitlab_transport_preflight(args)

    runtime = state_path(project)

    if project.exists() and any(project.iterdir()):
        if not runtime.exists():
            raise BootstrapError(
                "The project folder exists and is not empty "
                "but does not contain .bootstrap-state.json.\\n"
                "Refusing to adopt it automatically."
            )

        with runtime.open(encoding="utf-8") as f:
            existing_state = json.load(f)

        if existing_state.get("state") == "COMPLETE":
            raise BootstrapError(
                "This project is already fully bootstrapped."
            )

        print("PASS partial project: RESUME")
        fresh = False

    else:
        print("PASS local destination available")
        fresh = True

    if fresh and remote_repository_exists(args, backend):
        raise BootstrapError(
            "The remote repository already exists while "
            "the local project is new.\\n"
            "Refusing to adopt it automatically."
        )

    print("=== PREFLIGHT PASS ===")

    return backend


def build_parser():
    p = argparse.ArgumentParser(
        description="OpenClaw Project Manager robust bootstrap V2"
    )

    p.add_argument("--title")
    p.add_argument("--slug")
    p.add_argument("--project-dir", help="Explicit project directory; defaults to the legacy OpenClaw workspace")
    p.add_argument("--config", help="Resolved project setup JSON from project_setup.py")
    p.add_argument("--approve-config", help="SHA-256 from the reviewed --config --dry-run plan; authorizes provisioning")

    p.add_argument(
        "--archetype",
        choices=ARCHETYPES.keys(),
    )

    p.add_argument(
        "--add-domain",
        action="append",
        choices=DOMAIN_DIR.keys(),
    )

    p.add_argument(
        "--git-backend",
        choices=["github", "gitlab"],
    )

    p.add_argument(
        "--repo",
        help="OWNER/REPO or GROUP/SUBGROUP/REPO",
    )

    p.add_argument(
        "--git-host",
        help="GitLab hostname. Defaults to gitlab.com.",
    )

    p.add_argument(
        "--git-scheme",
        choices=["https", "http"],
        default="https",
    )

    p.add_argument(
        "--git-protocol",
        choices=["https", "http", "ssh"],
        default="https",
    )

    p.add_argument("--git-ssh-host")
    p.add_argument("--git-ssh-port", type=int)

    p.add_argument(
        "--default-branch",
        default="main",
        help="Canonical Git branch. Defaults to main.",
    )

    p.add_argument(
        "--visibility",
        choices=["private", "public"],
        default="private",
    )

    p.add_argument("--drive-url")
    p.add_argument("--business", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--preflight-only", action="store_true")

    return p

def parse_args(argv=None):
    from project_setup import SetupError, _branch, _host, load_config, to_bootstrap_args
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    args = parser.parse_args(argv)
    args.setup_config = None
    try:
        if args.config:
            allowed = {"--config", "--approve-config", "--dry-run", "--preflight-only"}
            if any(arg.startswith("--") and arg.split("=", 1)[0] not in allowed for arg in argv):
                raise BootstrapError("--config cannot be combined with project flags; edit and review the configuration instead")
            args.setup_config = load_config(args.config)
            for key, value in to_bootstrap_args(args.setup_config).items():
                setattr(args, key, value)
        else:
            if args.approve_config:
                raise BootstrapError("--approve-config requires --config")
            for key in ("title", "slug", "archetype", "git_backend", "repo"):
                if not getattr(args, key):
                    parser.error("--" + key.replace("_", "-") + " is required without --config")
            _branch(args.default_branch)
            _host(normalize_host(args.git_host or args.git_backend + ".com"), "git host")
            if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*(?:/[A-Za-z0-9_][A-Za-z0-9_.-]*)+", args.repo):
                raise BootstrapError("Invalid repository: use OWNER/REPO or GROUP/SUBGROUP/REPO")
            if args.git_ssh_port is not None and not 1 <= args.git_ssh_port <= 65535:
                raise BootstrapError("SSH port must be from 1 to 65535")
    except SetupError as exc:
        raise BootstrapError(str(exc)) from None
    return args


def main(argv=None):
    args = parse_args(argv)

    if not re.fullmatch(
        r"[a-z0-9][a-z0-9-]*",
        args.slug,
    ):
        raise BootstrapError(
            "Invalid slug: lowercase letters, digits and hyphens only."
        )

    if args.git_backend == "github":
        if (
            args.git_host
            and normalize_host(args.git_host) != "github.com"
        ):
            raise BootstrapError(
                "The GitHub backend uses github.com."
            )

        if args.git_protocol != "https":
            raise BootstrapError(
                "This version uses HTTPS for GitHub."
            )

        git_host = "github.com"

    else:
        git_host = normalize_host(
            args.git_host or "gitlab.com"
        )

    domains = list(ARCHETYPES[args.archetype])

    for domain in args.add_domain or []:
        if domain not in domains:
            domains.append(domain)

    root = (
        WORKSPACE / "business-projects"
        if args.business
        else WORKSPACE / "projects"
    )

    project = Path(args.project_dir).expanduser().resolve() if args.project_dir else root / args.slug
    if project == Path(project.anchor):
        raise BootstrapError("Project directory must not be a filesystem root")

    summary = {
        "project": str(project),
        "title": args.title,
        "slug": args.slug,
        "archetype": args.archetype,
        "domains": domains,
        "git_backend": args.git_backend,
        "git_host": git_host,
        "git_scheme": args.git_scheme,
        "git_protocol": args.git_protocol,
        "git_ssh_host": args.git_ssh_host,
        "git_ssh_port": args.git_ssh_port,
        "default_branch": args.default_branch,
        "repository": args.repo,
        "visibility": args.visibility,
        "drive": args.drive_url,
    }

    if args.setup_config:
        from project_setup import fingerprint, review
        summary["setup_sha256"] = fingerprint(args.setup_config)

    if args.dry_run:
        print(
            json.dumps(
                review(args.setup_config) if args.setup_config else summary,
                indent=2,
                ensure_ascii=False,
            )
        )
        return

    if args.setup_config and not args.preflight_only and args.approve_config != summary["setup_sha256"]:
        raise BootstrapError(
            "Configuration has not been authorized. Review --config FILE --dry-run, then pass "
            "--approve-config with its approval_sha256 after user authorization. No project or remote was created."
        )

    backend = robust_preflight(
        args,
        project,
        domains,
    )
    if args.setup_config:
        backend["ci_runner_tags"] = args.setup_config["infrastructure"]["ci_runner_tags"]

    if args.preflight_only:
        print()
        print("No files created.")
        return

    project.mkdir(
        parents=True,
        exist_ok=True,
    )

    state = load_or_create_state(
        project,
        summary,
        backend,
    )

    mark_step(
        project,
        state,
        "preflight",
        "PASS",
    )

    execute_step(
        project,
        state,
        "structure",
        lambda: initialize_structure(
            project,
            args,
            summary,
            backend,
            domains,
        ),
    )

    execute_step(
        project,
        state,
        "task_engine",
        lambda: initialize_task_engine(
            project,
            args,
        ),
    )

    execute_step(
        project,
        state,
        "git_init",
        lambda: initialize_git(project, args),
    )

    execute_step(
        project,
        state,
        "remote_create",
        lambda: remote_create_step(
            project,
            args,
            backend,
        ),
    )

    execute_step(
        project,
        state,
        "initial_push",
        lambda: initial_push(project, args, backend),
    )

    execute_step(
        project,
        state,
        "verification",
        lambda: verify_repository(project, args),
    )

    execute_step(
        project,
        state,
        "finalization",
        lambda: finalization_step(
            project,
            args,
            backend,
        ),
    )

    state["state"] = "COMPLETE"
    state["last_error"] = None
    save_state(project, state)

    print()
    print("================================")
    print("BOOTSTRAP COMPLETE")
    print("================================")
    print("Project:", project)
    print("Domains:", ", ".join(domains))
    print("Git profile:", backend["profile"])
    print("Git host:", backend["host"])
    print("Repository:", args.repo)


if __name__ == "__main__":
    try:
        main()

    except BootstrapError as exc:
        print()
        print("BOOTSTRAP ERROR:")
        print(exc)
        sys.exit(1)

    except subprocess.CalledProcessError as exc:
        print()
        print("BOOTSTRAP COMMAND ERROR:")
        print(exc)
        sys.exit(1)

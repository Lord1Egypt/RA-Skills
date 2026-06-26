#!/usr/bin/env python3
"""
Render provisional project structures for high-rigor reports.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Iterable

TEMPLATES = {
    "api-service": """service/
  src/
    app.py
    routes/
    domain/
    integrations/
  tests/
  pyproject.toml
  README.md""",
    "web-app": """app/
  src/
    pages/
    components/
    features/
    lib/
  public/
  tests/
  package.json""",
    "cli-tool": """tool/
  src/
    cli.py
    commands/
    core/
  tests/
  pyproject.toml
  README.md""",
    "full-stack": """project/
  apps/
    web/
    api/
  packages/
    shared/
    config/
  tests/
  package.json""",
    "monorepo": """workspace/
  apps/
    web/
    api/
    worker/
  packages/
    ui/
    config/
    shared/
  tooling/
  package.json""",
    "github-actions-pipeline": """repo/
  .github/
    workflows/
      ci.yml
      deploy.yml
  scripts/
    build.sh
    rollback.sh
  docs/
    runbooks/
      release.md
  pyproject.toml""",
    "delivery-pipeline": """repo/
  ci/
    pipeline.yml
  scripts/
    build.sh
    deploy.sh
    rollback.sh
  docs/
    runbooks/
      release.md""",
}

TERM_SEPARATOR_PATTERN = r"[\s./_-]+"
BUILD_CONTEXT_TERMS = (
    "github actions",
    "ci/cd",
    "ci",
    "cd",
    "pipeline",
    "build pipeline",
    "build system",
    "build tooling",
    "build output",
    "build logs",
    "rollback",
)
BUILD_CREATION_PATTERN = re.compile(
    r"\bbuild(?:\s+(?:a|an|the|my|our|new|another))?\s+"
    r"(?:marketing\s+site|landing\s+page|website|site|app|dashboard|frontend|backend|"
    r"api|service|worker|cli(?:\s+tool)?|tool|library|package|sdk)\b"
)
BUILD_FAILURE_PATTERNS = (
    re.compile(r"\bfailing(?:\s+\w+){0,2}\s+builds?\b"),
    re.compile(r"\bfailed(?:\s+\w+){0,2}\s+builds?\b"),
    re.compile(r"\bbroken(?:\s+\w+){0,2}\s+builds?\b"),
    re.compile(r"\bbuild(?:\s+\w+){0,2}\s+failure(?:s)?\b"),
)

KNOWN_MANIFESTS = {
    "pyproject.toml": ("python", "poetry"),
    "poetry.lock": ("python", "poetry"),
    "uv.lock": ("python", "uv"),
    "requirements.txt": ("python", "pip"),
    "package.json": ("node", None),
    "package-lock.json": ("node", "npm"),
    "pnpm-lock.yaml": ("node", "pnpm"),
    "pnpm-workspace.yaml": ("node", "pnpm"),
    "yarn.lock": ("node", "yarn"),
    "Cargo.toml": ("rust", "cargo"),
    "go.mod": ("go", None),
    "Gemfile": ("ruby", "bundler"),
}
KNOWN_DEPLOY_FILES = {
    "fly.toml": "fly.io",
    "vercel.json": "vercel",
    "netlify.toml": "netlify",
    "docker-compose.yml": "docker",
    "docker-compose.yaml": "docker",
    "Dockerfile": "docker",
}
INTERESTING_DIRS = {
    ".github",
    "apps",
    "packages",
    "src",
    "app",
    "public",
    "tests",
    "tooling",
    "scripts",
    "docs",
    "ci",
    "services",
    "libs",
}
TOP_LEVEL_PRIORITY = {
    ".github": 0,
    "apps": 1,
    "packages": 2,
    "src": 3,
    "app": 4,
    "public": 5,
    "tests": 6,
    "ci": 7,
    "scripts": 8,
    "docs": 9,
    "tooling": 10,
    "package.json": 11,
    "pnpm-workspace.yaml": 12,
    "pyproject.toml": 13,
    "fly.toml": 14,
    "README.md": 15,
}


@dataclass(frozen=True)
class RepoObservations:
    root: Path | None
    has_repo: bool
    top_level_dirs: tuple[str, ...]
    top_level_files: tuple[str, ...]
    tree_paths: tuple[str, ...]
    manifests: tuple[str, ...]
    runtime_signals: tuple[str, ...]
    package_manager_signals: tuple[str, ...]
    ci_signals: tuple[str, ...]
    deploy_signals: tuple[str, ...]
    archetype_hint: str | None


def _matches_term(prompt: str, term: str) -> bool:
    parts = re.findall(r"[a-z0-9]+", term.lower())
    if not parts:
        return False
    pattern = r"\b" + TERM_SEPARATOR_PATTERN.join(re.escape(part) for part in parts) + r"\b"
    return re.search(pattern, prompt.lower()) is not None


def _looks_like_build_creation_prompt(prompt: str) -> bool:
    return BUILD_CREATION_PATTERN.search(prompt.lower()) is not None


def _matches_build_failure(prompt: str) -> bool:
    lowered = prompt.lower()
    return any(pattern.search(lowered) is not None for pattern in BUILD_FAILURE_PATTERNS)


def is_build_task_prompt(prompt: str) -> bool:
    lowered = prompt.lower()
    if _looks_like_build_creation_prompt(lowered):
        return False
    if _matches_build_failure(lowered):
        return True
    return any(_matches_term(lowered, term) for term in BUILD_CONTEXT_TERMS)


def _infer_build_template(prompt: str, repo: RepoObservations | None = None) -> str:
    if repo and "github-actions" in repo.ci_signals:
        return "github-actions-pipeline"
    if _matches_term(prompt, "github actions"):
        return "github-actions-pipeline"
    return "delivery-pipeline"


def infer_template(
    prompt: str,
    task_type: str | None = None,
    repo_observations: RepoObservations | None = None,
) -> str | None:
    if task_type == "build" or (task_type is None and is_build_task_prompt(prompt)):
        return _infer_build_template(prompt, repo_observations)

    if repo_observations and repo_observations.archetype_hint:
        hint = repo_observations.archetype_hint
        if hint in TEMPLATES:
            return hint

    lowered = prompt.lower()
    if "monorepo" in lowered:
        return "monorepo"
    if ("frontend" in lowered or "web" in lowered) and ("api" in lowered or "backend" in lowered):
        return "full-stack"
    if "worker" in lowered and ("web" in lowered or "api" in lowered):
        return "monorepo"
    if "cli" in lowered:
        return "cli-tool"
    if "api" in lowered or "backend" in lowered or "service" in lowered:
        return "api-service"
    if "full-stack" in lowered or "full stack" in lowered:
        return "full-stack"
    return "web-app"


def render_structure(template_name: str) -> str:
    return TEMPLATES.get(template_name, TEMPLATES["web-app"])


def _signal_to_archetype(
    top_level_dirs: tuple[str, ...],
    manifests: tuple[str, ...],
    runtime_signals: tuple[str, ...],
) -> str | None:
    dir_set = set(top_level_dirs)
    manifest_set = set(manifests)
    runtimes = set(runtime_signals)

    if {"apps", "packages"} <= dir_set:
        return "monorepo"
    if {"web", "api"} <= dir_set or {"frontend", "backend"} <= dir_set:
        return "full-stack"
    if "ci" in dir_set or ".github" in dir_set:
        return "delivery-pipeline"
    if "package.json" in manifest_set and {"src", "public"} & dir_set:
        return "web-app"
    if "pyproject.toml" in manifest_set and "src" in dir_set and "node" not in runtimes:
        return "api-service"
    return None


def _walk_repo_paths(root: Path, *, max_depth: int) -> tuple[str, ...]:
    collected: set[str] = set()
    if max_depth < 1:
        return ()

    for path in root.rglob("*"):
        if path.is_symlink():
            continue
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        parts = relative.parts
        if not parts or len(parts) > max_depth:
            continue
        if any(part == ".git" or part == "__pycache__" for part in parts):
            continue
        if len(parts) == 1 and parts[0] not in INTERESTING_DIRS and parts[0] not in KNOWN_MANIFESTS and parts[0] not in KNOWN_DEPLOY_FILES and parts[0] not in {"README.md"}:
            if path.is_dir():
                continue
        if path.is_file() or parts[0] in INTERESTING_DIRS:
            collected.add(relative.as_posix())
    return tuple(sorted(collected))


def inspect_repo(repo_root: Path | str | None, *, max_depth: int = 2) -> RepoObservations:
    if repo_root is None:
        return RepoObservations(None, False, (), (), (), (), (), (), (), (), None)

    root = Path(repo_root).resolve()
    if not root.exists() or not root.is_dir():
        return RepoObservations(root, False, (), (), (), (), (), (), (), (), None)

    top_level_dirs: list[str] = []
    top_level_files: list[str] = []
    manifests: set[str] = set()
    runtime_signals: set[str] = set()
    package_manager_signals: set[str] = set()
    ci_signals: set[str] = set()
    deploy_signals: set[str] = set()

    for child in sorted(root.iterdir(), key=lambda item: item.name.lower()):
        if child.name == ".git" or child.name == "__pycache__":
            continue
        if child.is_dir():
            top_level_dirs.append(child.name)
        elif child.is_file():
            top_level_files.append(child.name)

        if child.name in KNOWN_MANIFESTS:
            manifests.add(child.name)
            runtime, package_manager = KNOWN_MANIFESTS[child.name]
            runtime_signals.add(runtime)
            if package_manager:
                package_manager_signals.add(package_manager)
        if child.name in KNOWN_DEPLOY_FILES:
            deploy_signals.add(KNOWN_DEPLOY_FILES[child.name])

    github_workflows = root / ".github" / "workflows"
    if github_workflows.exists() and github_workflows.is_dir():
        ci_signals.add("github-actions")
    if (root / ".gitlab-ci.yml").exists():
        ci_signals.add("gitlab-ci")
    if (root / "Jenkinsfile").exists():
        ci_signals.add("jenkins")
    if (root / "ci").exists():
        ci_signals.add("generic-ci")

    if (root / "package.json").exists():
        package_manager_signals.add("npm")
        runtime_signals.add("node")
    if (root / "pnpm-lock.yaml").exists() or (root / "pnpm-workspace.yaml").exists():
        package_manager_signals.add("pnpm")
    if (root / "yarn.lock").exists():
        package_manager_signals.add("yarn")
    if (root / "uv.lock").exists():
        package_manager_signals.add("uv")
        runtime_signals.add("python")
    if (root / "poetry.lock").exists():
        package_manager_signals.add("poetry")
        runtime_signals.add("python")
    if (root / "Dockerfile").exists():
        deploy_signals.add("docker")

    tree_paths = _walk_repo_paths(root, max_depth=max_depth)
    archetype_hint = _signal_to_archetype(
        tuple(top_level_dirs),
        tuple(sorted(manifests)),
        tuple(sorted(runtime_signals)),
    )

    has_repo = bool(top_level_dirs or top_level_files)
    return RepoObservations(
        root=root,
        has_repo=has_repo,
        top_level_dirs=tuple(top_level_dirs),
        top_level_files=tuple(top_level_files),
        tree_paths=tree_paths,
        manifests=tuple(sorted(manifests)),
        runtime_signals=tuple(sorted(runtime_signals)),
        package_manager_signals=tuple(sorted(package_manager_signals)),
        ci_signals=tuple(sorted(ci_signals)),
        deploy_signals=tuple(sorted(deploy_signals)),
        archetype_hint=archetype_hint,
    )


def _root_label(template_name: str) -> str:
    if template_name == "monorepo":
        return "workspace/"
    if template_name == "web-app":
        return "app/"
    if template_name == "api-service":
        return "service/"
    if template_name == "cli-tool":
        return "tool/"
    if template_name == "full-stack":
        return "project/"
    return "repo/"


def _priority(path: str) -> tuple[int, str]:
    head = path.split("/", 1)[0]
    return (TOP_LEVEL_PRIORITY.get(head, 100), path)


def _iter_children(paths: Iterable[str], prefix: str) -> list[str]:
    children = {
        path[len(prefix):].split("/", 1)[0]
        for path in paths
        if path.startswith(prefix) and path != prefix.rstrip("/")
    }
    return sorted(children)


def _build_tree_lines(paths: tuple[str, ...], *, root_label: str) -> list[str]:
    lines = [root_label]
    sorted_paths = tuple(sorted(paths, key=_priority))

    def visit(prefix: str, depth: int) -> None:
        for child in _iter_children(sorted_paths, prefix):
            line = f"{'  ' * depth}{child}"
            child_prefix = f"{prefix}{child}"
            is_dir = any(path.startswith(f"{child_prefix}/") for path in sorted_paths)
            lines.append(f"{line}/" if is_dir else line)
            if is_dir:
                visit(f"{child_prefix}/", depth + 1)

    visit("", 1)
    return lines


def _prompt_extra_paths(
    prompt: str,
    *,
    template_name: str,
    existing_paths: tuple[str, ...],
) -> tuple[str, ...]:
    lowered = prompt.lower()
    extras: set[str] = set()
    existing = set(existing_paths)

    if template_name in {"monorepo", "full-stack"}:
        if "worker" in lowered and "apps/worker" not in existing:
            extras.add("apps/worker")
        if ("frontend" in lowered or "web" in lowered) and "apps/web" not in existing:
            extras.add("apps/web")
        if ("backend" in lowered or "api" in lowered) and "apps/api" not in existing:
            extras.add("apps/api")

    if template_name == "api-service":
        if "src/routes" not in existing and ("api" in lowered or "backend" in lowered):
            extras.add("src/routes")
        if "tests" not in existing:
            extras.add("tests")
        if "pyproject.toml" not in existing:
            extras.add("pyproject.toml")

    if template_name == "web-app":
        if "src/components" not in existing:
            extras.add("src/components")
        if "public" not in existing:
            extras.add("public")
        if "package.json" not in existing:
            extras.add("package.json")

    if template_name in {"delivery-pipeline", "github-actions-pipeline"}:
        if "scripts/build.sh" not in existing:
            extras.add("scripts/build.sh")
        if "scripts/rollback.sh" not in existing:
            extras.add("scripts/rollback.sh")

    return tuple(sorted(extras))


def _select_relevant_repo_paths(
    repo_observations: RepoObservations,
    *,
    template_name: str,
) -> tuple[str, ...]:
    if template_name in {"delivery-pipeline", "github-actions-pipeline"}:
        keep_prefixes = (".github", "ci", "scripts", "docs")
    elif template_name == "api-service":
        keep_prefixes = ("src", "tests", "docs", "scripts")
    elif template_name == "web-app":
        keep_prefixes = ("src", "public", "tests")
    elif template_name == "cli-tool":
        keep_prefixes = ("src", "tests", "docs")
    elif template_name in {"full-stack", "monorepo"}:
        keep_prefixes = ("apps", "packages", "tooling", "docs", "scripts")
    else:
        keep_prefixes = ("src", "tests")

    keep_files = set(KNOWN_MANIFESTS) | set(KNOWN_DEPLOY_FILES) | {"README.md"}
    selected = {
        path
        for path in repo_observations.tree_paths
        if path in keep_files or path.startswith(keep_prefixes)
    }
    return tuple(sorted(selected))


def _repo_prompt_overlap(prompt: str) -> bool:
    lowered = prompt.lower()
    return any(
        term in lowered
        for term in ("existing", "current", "this repo", "this repository", "in this repo", "already")
    )


def should_apply_repo_context(
    prompt: str,
    *,
    task_type: str | None,
    repo_observations: RepoObservations | None,
    repo_root_explicit: bool,
) -> bool:
    if repo_observations is None or not repo_observations.has_repo:
        return False

    if repo_root_explicit:
        return True

    if task_type in {"coding", "build", "architecture", "debugging", "discovery"}:
        return _repo_prompt_overlap(prompt)

    return False


def render_project_structure(
    prompt: str,
    *,
    task_type: str | None = None,
    report_basis: str = "repo_plus_prompt",
    repo_observations: RepoObservations | None = None,
    repo_root: Path | str | None = None,
    repo_scan_max_depth: int = 2,
    repo_root_explicit: bool = False,
    apply_repo_context: bool | None = None,
) -> str:
    observations = repo_observations
    if observations is None and report_basis == "repo_plus_prompt":
        observations = inspect_repo(repo_root, max_depth=repo_scan_max_depth)

    if report_basis == "prompt_only":
        template_name = infer_template(prompt, task_type=task_type)
        return render_structure(template_name or "web-app")

    if report_basis == "template_first":
        template_name = infer_template(prompt, task_type=task_type, repo_observations=observations)
        return render_structure(template_name or "web-app")

    use_repo_structure = (
        apply_repo_context
        if apply_repo_context is not None
        else should_apply_repo_context(
            prompt,
            task_type=task_type,
            repo_observations=observations,
            repo_root_explicit=repo_root_explicit,
        )
    )
    template_name = infer_template(
        prompt,
        task_type=task_type,
        repo_observations=observations if use_repo_structure else None,
    )
    if not observations or not use_repo_structure:
        return render_structure(template_name or "web-app")

    selected_paths = set(
        _select_relevant_repo_paths(observations, template_name=template_name or "web-app")
    )
    selected_paths.update(_prompt_extra_paths(prompt, template_name=template_name or "web-app", existing_paths=observations.tree_paths))
    if not selected_paths:
        return render_structure(template_name or "web-app")
    return "\n".join(
        _build_tree_lines(tuple(sorted(selected_paths)), root_label=_root_label(template_name or "web-app"))
    )


def main() -> int:
    if len(sys.argv) == 1:
        print(render_structure("web-app"))
        return 0

    args = sys.argv[1:]
    report_basis = "prompt_only"
    repo_root: Path | None = None
    prompt = args[0]

    if "--repo-root" in args:
        index = args.index("--repo-root")
        if index + 1 >= len(args):
            print("error: --repo-root requires a path", file=sys.stderr)
            return 2
        repo_root = Path(args[index + 1]).resolve()
        report_basis = "repo_plus_prompt"

    template_name = prompt if prompt in TEMPLATES else None
    if template_name is not None and repo_root is None:
        print(render_structure(template_name))
        return 0

    print(
        render_project_structure(
            prompt,
            report_basis=report_basis,
            repo_root=repo_root,
            repo_root_explicit=repo_root is not None,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Collect and validate a project setup plan without provisioning infrastructure."""

import argparse
import copy
import hashlib
import ipaddress
import json
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit


class SetupError(ValueError):
    pass


def _object(value, allowed, location, required=()):
    if not isinstance(value, dict):
        raise SetupError(f"{location} must be an object")
    if set(value) - set(allowed):
        raise SetupError(f"{location} contains unsupported fields; credentials must never be stored in setup files")
    missing = set(required) - set(value)
    if missing:
        raise SetupError(f"{location} is missing: {', '.join(sorted(missing))}")


def _text(value, location, optional=False):
    if not isinstance(value, str) or (not optional and not value.strip()):
        raise SetupError(f"{location} must be {'an optional' if optional else 'a nonempty'} string")
    if any(ord(c) < 32 for c in value):
        raise SetupError(f"{location} must be a single line without control characters")
    # These checks reject common accidental disclosures, not arbitrary secrets.
    if re.search(r"(?:gh[pousr]_|github_pat_|glpat-|sk-proj-)[A-Za-z0-9_-]{8,}|-----BEGIN .*PRIVATE KEY", value):
        raise SetupError(f"{location} appears to contain a credential; use an env: or keychain: reference")
    return value.strip()


def _strings(value, location, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise SetupError(f"{location} must be {'a nonempty' if nonempty else 'a'} list of strings")
    return [_text(item, location) for item in value]


def _choice(value, choices, location):
    if not isinstance(value, str) or value not in choices:
        raise SetupError(f"{location} must be one of: {', '.join(choices)}")
    return value


def _integer(value, location, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum:
        raise SetupError(f"{location} must be an integer from {minimum} to {maximum}")
    return value


def _host(value, location):
    value = _text(value, location)
    if not re.fullmatch(r"(?:[A-Za-z0-9][A-Za-z0-9.-]*|\[[0-9a-fA-F:]+\])(?::[0-9]+)?", value):
        raise SetupError(f"{location} must be a hostname with an optional port, without credentials or URL paths")
    try:
        parsed = urlsplit("//" + value)
        if value.startswith("["):
            ipaddress.IPv6Address(parsed.hostname)
        if parsed.port is not None:
            _integer(parsed.port, location + " port", 1, 65535)
    except ValueError:
        raise SetupError(f"{location} has an invalid address or port") from None
    return value


def _branch(value):
    value = _text(value, "infrastructure.default_branch")
    if (value.startswith(("-", "/", ".")) or value.endswith(("/", "."))
            or any(part.startswith(".") or part.endswith(".lock") for part in value.split("/"))
            or any(fragment in value for fragment in ("..", "@{", "//"))
            or any(c in value for c in " ~^:?*[\\") or value == "@"):
        raise SetupError("infrastructure.default_branch is not a valid Git branch name")
    return value


def validate_config(data, base_dir=None):
    """Return a fully resolved, deterministic copy; never access the network."""
    from bootstrap_project import ARCHETYPES, DOMAIN_DIR

    data = copy.deepcopy(data)
    _object(data, ("schema_version", "project", "infrastructure", "delegation"), "setup",
            ("schema_version", "project", "infrastructure", "delegation"))
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise SetupError("Unsupported setup schema_version; expected 1")
    project = data["project"]
    _object(project, ("title", "slug", "path", "archetype", "add_domains", "objective", "in_scope",
                      "out_of_scope", "owners", "constraints", "milestones"), "project",
            ("title", "slug", "path", "archetype", "objective", "in_scope", "owners"))
    for key in ("title", "slug", "path", "objective"):
        project[key] = _text(project[key], "project." + key)
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", project["slug"]):
        raise SetupError("project.slug must contain lowercase letters, digits and hyphens")
    path = Path(project["path"]).expanduser()
    if not path.is_absolute():
        path = Path(base_dir or Path.cwd()) / path
    project["path"] = str(path.resolve())
    if path.resolve() == Path(path.anchor):
        raise SetupError("project.path must not be a filesystem root")
    _choice(project["archetype"], ARCHETYPES, "project.archetype")
    project["add_domains"] = _strings(project.get("add_domains", []), "project.add_domains")
    for domain in project["add_domains"]:
        _choice(domain, DOMAIN_DIR, "project.add_domains")
    project["add_domains"] = list(dict.fromkeys(project["add_domains"]))
    if project["archetype"] == "custom" and not project["add_domains"]:
        raise SetupError("A custom project requires at least one engineering domain")
    for key in ("in_scope", "out_of_scope", "owners", "constraints", "milestones"):
        project[key] = _strings(project.get(key, []), "project." + key, key in ("in_scope", "owners"))

    infra = data["infrastructure"]
    _object(infra, ("git_backend", "repository", "host", "scheme", "protocol", "ssh_host", "ssh_port",
                    "visibility", "default_branch", "drive_url", "credential_refs", "ci_runner_tags",
                    "test_commands"), "infrastructure", ("git_backend", "repository"))
    _choice(infra["git_backend"], ("github", "gitlab"), "infrastructure.git_backend")
    infra["repository"] = _text(infra["repository"], "infrastructure.repository")
    parts = infra["repository"].split("/")
    if len(parts) < 2 or any(not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", p) or p in (".", "..") for p in parts):
        raise SetupError("infrastructure.repository must be OWNER/REPO or GROUP/SUBGROUP/REPO")
    if infra["git_backend"] == "github" and len(parts) != 2:
        raise SetupError("GitHub repository must be OWNER/REPO")
    infra["host"] = _host(infra.get("host", infra["git_backend"] + ".com"), "infrastructure.host")
    for key, default, choices in (
        ("scheme", "https", ("https", "http")),
        ("protocol", "https", ("https", "http", "ssh")),
        ("visibility", "private", ("private", "public")),
    ):
        infra[key] = _choice(infra.get(key, default), choices, "infrastructure." + key)
    if infra["git_backend"] == "github" and (infra["host"] != "github.com" or infra["protocol"] != "https" or infra["scheme"] != "https"):
        raise SetupError("The GitHub backend requires github.com over HTTPS")
    if infra["protocol"] != "ssh" and infra["protocol"] != infra["scheme"]:
        raise SetupError("HTTP(S) Git protocol and scheme must match")
    infra["default_branch"] = _branch(infra.get("default_branch", "main"))
    infra["ssh_host"] = infra.get("ssh_host")
    infra["ssh_port"] = infra.get("ssh_port")
    if infra["ssh_host"] is not None:
        infra["ssh_host"] = _text(infra["ssh_host"], "infrastructure.ssh_host")
        if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", infra["ssh_host"]):
            raise SetupError("ssh_host must be a host or SSH alias; use ssh_port separately")
    if infra["ssh_port"] is not None:
        _integer(infra["ssh_port"], "infrastructure.ssh_port", 1, 65535)
    if infra["protocol"] != "ssh" and (infra["ssh_host"] is not None or infra["ssh_port"] is not None):
        raise SetupError("SSH options require protocol ssh")
    infra["drive_url"] = infra.get("drive_url")
    if infra["drive_url"] is not None:
        value = _text(infra["drive_url"], "infrastructure.drive_url")
        try:
            url = urlsplit(value)
            valid = (url.scheme == "https" and url.hostname in ("drive.google.com", "docs.google.com")
                     and not any((url.username, url.password, url.query, url.fragment, url.port)))
        except ValueError:
            valid = False
        if not valid:
            raise SetupError("drive_url must be an HTTPS Google Drive/Docs link without credentials, query or fragment")
    for key in ("credential_refs", "ci_runner_tags", "test_commands"):
        infra[key] = _strings(infra.get(key, []), "infrastructure." + key)
    for ref in infra["credential_refs"]:
        if not re.fullmatch(r"env:[A-Za-z_][A-Za-z0-9_]*|keychain:[A-Za-z0-9_.\-/]+", ref):
            raise SetupError("credential_refs must contain only env:VARIABLE or keychain:item references, never values")

    delegation = data["delegation"]
    _object(delegation, ("enabled", "agents", "max_parallel", "max_attempts", "writable_paths", "approval_policy"), "delegation")
    delegation.setdefault("enabled", False)
    if type(delegation["enabled"]) is not bool:
        raise SetupError("delegation.enabled must be a boolean")
    agents = delegation.setdefault("agents", [])
    if not isinstance(agents, list):
        raise SetupError("delegation.agents must be a list")
    labels = set()
    for agent in agents:
        _object(agent, ("label", "role", "worker", "capabilities"), "delegation.agents entry", ("label", "role", "worker"))
        for key in ("label", "role", "worker"):
            agent[key] = _text(agent[key], "agent." + key)
        agent["capabilities"] = _strings(agent.get("capabilities", []), "agent.capabilities")
        if agent["label"] in labels:
            raise SetupError("Agent labels must be unique")
        labels.add(agent["label"])
    if delegation["enabled"] and not agents:
        raise SetupError("Enabled delegation requires at least one declared agent")
    for key, default, maximum in (("max_parallel", 1, 3), ("max_attempts", 2, 10)):
        delegation[key] = _integer(delegation.get(key, default), "delegation." + key, 1, maximum)
    delegation["writable_paths"] = _strings(delegation.get("writable_paths", []), "delegation.writable_paths")
    for value in delegation["writable_paths"]:
        path = PurePosixPath(value)
        if not path.parts or path.is_absolute() or ".." in path.parts or ":" in value or "\\" in value or value.startswith("~") or ".git" in path.parts:
            raise SetupError("Delegation writable paths must stay within the project and exclude .git")
    if delegation["enabled"] and not delegation["writable_paths"]:
        raise SetupError("Enabled delegation requires explicit writable_paths")
    delegation["approval_policy"] = _choice(delegation.get("approval_policy", "review-before-integration"),
                                            ("review-before-integration", "review-each-task"), "delegation.approval_policy")
    return data


def load_config(path):
    path = Path(path).resolve()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SetupError(f"Cannot read setup JSON: {type(exc).__name__}") from None
    return validate_config(data, path.parent)


def fingerprint(config):
    return hashlib.sha256(json.dumps(config, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def review(config):
    return {
        "configuration": config,
        "approval_sha256": fingerprint(config),
        "infrastructure_check": "NOT_RUN: validation does not establish authentication, reachability, runner or agent availability",
        "effects_after_approval": ["Create or resume local project", "Initialize and commit Git repository",
                                   "Create remote repository if absent", "Push project and set default branch"],
        "planning_only": ["Agent and worker labels", "Delegation policy", "Test commands", "Milestone labels"],
    }


def to_bootstrap_args(config):
    p, i = config["project"], config["infrastructure"]
    return dict(title=p["title"], slug=p["slug"], archetype=p["archetype"], add_domain=p["add_domains"],
                project_dir=p["path"], git_backend=i["git_backend"], repo=i["repository"], git_host=i["host"],
                git_scheme=i["scheme"], git_protocol=i["protocol"], git_ssh_host=i["ssh_host"], git_ssh_port=i["ssh_port"],
                visibility=i["visibility"], default_branch=i["default_branch"], drive_url=i["drive_url"], business=False)


def questionnaire(seed=None, ask=input):
    """Ask only missing values. A seed is user-provided context, never discovered secrets."""
    data = copy.deepcopy({} if seed is None else seed)
    _object(data, ("schema_version", "project", "infrastructure", "delegation"), "seed")
    data.setdefault("schema_version", 1)
    p = data.setdefault("project", {})
    i = data.setdefault("infrastructure", {})
    d = data.setdefault("delegation", {})
    if any(not isinstance(section, dict) for section in (p, i, d)):
        raise SetupError("Seed project, infrastructure and delegation must be objects")

    def prompt(section, key, question, default=None, convert=str):
        if key not in section:
            suffix = f" [{default}]" if default is not None else ""
            answer = ask(question + suffix + ": ").strip()
            section[key] = convert(answer if answer else (str(default) if default is not None else ""))

    csv = lambda answer: [item.strip() for item in answer.split(";") if item.strip()]
    nullable = lambda answer: answer or None
    def number(answer):
        try:
            return int(answer)
        except ValueError:
            raise SetupError("A numeric answer was expected") from None
    prompt(p, "title", "Project title")
    prompt(p, "slug", "Project slug (lowercase, digits, hyphens)")
    prompt(p, "objective", "Objective and intended outcome")
    prompt(p, "in_scope", "In-scope deliverables (separate with ;)", convert=csv)
    prompt(p, "out_of_scope", "Out of scope (separate with ;)", "", csv)
    prompt(p, "archetype", "Archetype: desktop/mobile/website/saas/iot/home-automation/embedded/robot/drone/edge-ai/ml/custom")
    prompt(p, "add_domains", "Additional domains: SYS/SWE/HWE/MLE/CYBER/MECH (separate with ;)", "", csv)
    prompt(p, "path", "Project directory", "./projects/" + p["slug"])
    prompt(p, "owners", "Responsible owner/role labels, not personal contact data (separate with ;)", convert=csv)
    prompt(p, "constraints", "Technical, cost, schedule, safety/security and regulatory constraints (separate with ;)", "", csv)
    prompt(p, "milestones", "Milestone planning labels and acceptance targets (separate with ;)", "", csv)
    prompt(i, "git_backend", "Canonical Git provider: github/gitlab", "gitlab")
    prompt(i, "host", "Git API hostname (optional :port)", i["git_backend"] + ".com")
    prompt(i, "repository", "Repository namespace/project")
    prompt(i, "visibility", "Repository visibility: private/public", "private")
    prompt(i, "default_branch", "Default branch", "main")
    prompt(i, "scheme", "Git API scheme: https/http", "https")
    prompt(i, "protocol", "Git transport: https/http/ssh", i["scheme"])
    if i["protocol"] == "ssh":
        prompt(i, "ssh_host", "SSH host or configured SSH alias (blank uses API host)", "", nullable)
        prompt(i, "ssh_port", "SSH port (blank uses SSH configuration)", "", lambda answer: number(answer) if answer else None)
    prompt(i, "drive_url", "Optional complementary Google Drive URL (blank disables)", "", nullable)
    prompt(i, "credential_refs", "Credential references only, env:VARIABLE or keychain:item (separate with ;)", "", csv)
    prompt(i, "ci_runner_tags", "Existing GitLab runner tags (separate with ;, blank for untagged jobs)", "", csv)
    prompt(i, "test_commands", "Planned test commands, recorded but never executed here (separate with ;)", "", csv)

    def boolean(answer):
        if answer.lower() not in ("yes", "no"):
            raise SetupError("Delegation choice must be yes or no")
        return answer.lower() == "yes"

    prompt(d, "enabled", "Allow bounded agent delegation? yes/no", "no", boolean)
    if d["enabled"]:
        if "agents" not in d:
            labels = csv(ask("Available agent labels (separate with ;): "))
            d["agents"] = [{"label": label, "role": ask(f"Role for {label}: ").strip(),
                            "worker": ask(f"Worker/host label for {label} (no credentials): ").strip(),
                            "capabilities": csv(ask(f"Capabilities for {label} (separate with ;): "))} for label in labels]
        prompt(d, "max_parallel", "Maximum simultaneous delegated tasks", 1, number)
        prompt(d, "max_attempts", "Maximum attempts before escalation", 2, number)
        prompt(d, "writable_paths", "Allowed relative project paths (separate with ;)", convert=csv)
        prompt(d, "approval_policy", "Review policy: review-before-integration/review-each-task", "review-before-integration")
    return data


def persist_project_setup(project, config):
    """Store resolved intent in the project; exclude the machine-specific local path."""
    from bootstrap_project import write_once
    stored = copy.deepcopy(config)
    stored["project"].pop("path")
    write_once(project / "00-project/PROJECT-SETUP.json", json.dumps(stored, indent=2, ensure_ascii=False) + "\n")
    p = config["project"]
    lines = ["# Project Setup", "", "## Objective", "", p["objective"], ""]
    for title, values in (("In scope", p["in_scope"]), ("Out of scope", p["out_of_scope"]),
                          ("Owners (role labels)", p["owners"]), ("Constraints", p["constraints"]),
                          ("Milestones (planning labels only)", p["milestones"]),
                          ("Planned test commands (not executed)", config["infrastructure"]["test_commands"])):
        lines += ["## " + title, ""] + (["- " + item for item in values] or ["None declared."]) + [""]
    lines += ["## Infrastructure and delegation", "", "See PROJECT-SETUP.json. Agent and worker labels are declarations,",
              "not evidence of availability. Test commands are planning inputs; review before execution.",
              "Git is canonical. Optional Drive is complementary. No new milestone or lifecycle registry is created.", ""]
    write_once(project / "00-project/PROJECT-SETUP.md", "\n".join(lines))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="Validate and review an existing setup JSON; no questionnaire")
    parser.add_argument("--seed", help="Partial JSON with already-known answers; ask only missing fields")
    parser.add_argument("--output", help="New JSON path for questionnaire answers; refuses overwrite")
    args = parser.parse_args(argv)
    if args.config:
        if args.seed or args.output:
            parser.error("--config cannot be combined with --seed or --output")
        config = load_config(args.config)
    else:
        if not args.output:
            parser.error("Questionnaire requires --output; use --config to review")
        target = Path(args.output).resolve()
        if target.exists():
            raise SetupError("Output already exists; review it with --config or choose a new output")
        seed = json.loads(Path(args.seed).read_text(encoding="utf-8")) if args.seed else None
        print("Enter role labels and credential references only. No secrets. This step creates no project or remote.")
        config = validate_config(questionnaire(seed), target.parent)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(config, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(review(config), indent=2, ensure_ascii=False))
    print("Review the resolved plan before authorizing bootstrap. No infrastructure has been created or checked.")


if __name__ == "__main__":
    try:
        main()
    except (SetupError, OSError, ValueError, EOFError, KeyboardInterrupt) as exc:
        print(f"SETUP ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

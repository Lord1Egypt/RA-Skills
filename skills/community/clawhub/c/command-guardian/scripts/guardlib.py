import os
import re
import shlex
import subprocess


RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}
CHAIN_OPERATORS = {"&&", "||", ";", "|"}
SHELL_WRAPPERS = {"bash", "sh", "zsh", "pwsh", "powershell", "cmd"}
FILE_WRITE_COMMANDS = {"rm", "del", "erase", "mv", "move-item", "cp", "copy-item", "rmdir", "remove-item", "chmod", "chown", "rsync"}
POWERSHELL_DESTRUCTIVE_COMMANDS = {"remove-item", "move-item"}
POWERSHELL_WRITE_COMMANDS = {"copy-item", "set-content", "out-file", "clear-content"}
POWERSHELL_FILE_COMMANDS = POWERSHELL_DESTRUCTIVE_COMMANDS | POWERSHELL_WRITE_COMMANDS
READ_ONLY_COMMANDS = {"cat", "type", "ls", "dir", "rg", "git", "docker", "kubectl", "terraform"}
PACKAGE_MANAGERS = {"npm", "pnpm", "yarn", "pip", "cargo"}
POWERSHELL_PATH_FLAGS = {"-path", "-literalpath", "-destination", "-filter", "-include", "-exclude"}
POWERSHELL_SOURCE_FLAGS = {"-path", "-literalpath"}
POWERSHELL_DEST_FLAGS = {"-destination"}


def split_command(command):
    text = (command or "").strip()
    if not text:
        return []
    for posix in (False, True):
        try:
            return shlex.split(text, posix=posix)
        except ValueError:
            continue
    return text.split()


def split_compound_command(command):
    text = (command or "").strip()
    if not text:
        return []

    segments = []
    current = []
    quote = ""
    escape = False
    i = 0
    while i < len(text):
        ch = text[i]
        if escape:
            current.append(ch)
            escape = False
            i += 1
            continue
        if ch == "\\":
            current.append(ch)
            escape = True
            i += 1
            continue
        if quote:
            current.append(ch)
            if ch == quote:
                quote = ""
            i += 1
            continue
        if ch in ('"', "'"):
            quote = ch
            current.append(ch)
            i += 1
            continue

        two = text[i:i + 2]
        if two in {"&&", "||"}:
            segment = "".join(current).strip()
            if segment:
                segments.append(segment)
            segments.append(two)
            current = []
            i += 2
            continue

        if ch in {';', '|'}:
            segment = "".join(current).strip()
            if segment:
                segments.append(segment)
            segments.append(ch)
            current = []
            i += 1
            continue

        current.append(ch)
        i += 1

    segment = "".join(current).strip()
    if segment:
        segments.append(segment)
    return segments


def normalize_token(token):
    value = (token or "").strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def executable_name(token):
    value = normalize_token(token)
    value = os.path.basename(value).lower()
    for suffix in (".exe", ".cmd", ".bat", ".ps1"):
        if value.endswith(suffix):
            return value[: -len(suffix)]
    return value


def get_subcommand(tokens):
    for token in tokens[1:]:
        value = normalize_token(token)
        if value and not value.startswith("-") and value not in {"|", "&&", "||", ";"}:
            return value.lower()
    return ""


def is_windows_drive_path(value):
    return bool(re.match(r"^[a-zA-Z]:([\\/]|$)", value or ""))


def is_remote_path(value):
    value = normalize_token(value).lower()
    return value.startswith(("http://", "https://", "ssh://", "git@", "s3://"))


def is_probable_path(value):
    value = normalize_token(value)
    if not value or is_remote_path(value):
        return False
    if value in {".", "..", "/", "\\", "*", ".\\*", "./*", "*.*"}:
        return True
    if is_windows_drive_path(value):
        return True
    if any(sep in value for sep in ("/", "\\")):
        return True
    if value.startswith(("~", ".")):
        return True
    if "*" in value or "?" in value:
        return True
    if re.search(r"\.(json|ya?ml|tf|txt|env|ini|toml|cfg|conf|lock|ps1|sh|bat|cmd|py)$", value, re.I):
        return True
    return False


def resolve_path(raw_value, cwd):
    value = normalize_token(raw_value)
    if not value or is_remote_path(value):
        return ""
    expanded = os.path.expandvars(os.path.expanduser(value))
    if os.path.isabs(expanded) or is_windows_drive_path(expanded):
        return os.path.abspath(expanded)
    return os.path.abspath(os.path.join(cwd, expanded))


def path_within_roots(path, allowed_roots):
    if not path:
        return True
    target = os.path.abspath(path)
    for root in allowed_roots:
        base = os.path.abspath(root)
        try:
            if os.path.commonpath([target, base]) == base:
                return True
        except ValueError:
            continue
    return False


def mask_secret(value):
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}...{value[-4:]}"


def max_risk(*levels):
    best = "low"
    for level in levels:
        if RISK_ORDER.get(level, -1) > RISK_ORDER[best]:
            best = level
    return best


def detect_nested_command(tokens):
    if not tokens:
        return ""
    primary = executable_name(tokens[0])
    if primary in SHELL_WRAPPERS:
        for index, token in enumerate(tokens[1:], start=1):
            value = normalize_token(token).lower()
            if value in {"-c", "-command", "/c"} and index + 1 < len(tokens):
                return normalize_token(tokens[index + 1])
    return ""


def powershell_option_values(tokens, option_names):
    values = []
    normalized_options = {name.lower() for name in option_names}
    for index, token in enumerate(tokens[:-1]):
        option = normalize_token(token).lower()
        if option in normalized_options:
            candidate = normalize_token(tokens[index + 1])
            if candidate and not candidate.startswith("-"):
                values.append(candidate)
    return values


def powershell_file_details(tokens):
    if not tokens:
        return {}

    primary = executable_name(tokens[0])
    if primary not in POWERSHELL_FILE_COMMANDS | POWERSHELL_DESTRUCTIVE_COMMANDS:
        return {}

    details = {
        "uses_recurse": any(normalize_token(token).lower() == "-recurse" for token in tokens[1:]),
        "uses_force": any(normalize_token(token).lower() == "-force" for token in tokens[1:]),
        "uses_literal_path": any(normalize_token(token).lower() == "-literalpath" for token in tokens[1:]),
        "uses_path": any(normalize_token(token).lower() == "-path" for token in tokens[1:]),
        "path_values": powershell_option_values(tokens, POWERSHELL_SOURCE_FLAGS),
        "destination_values": powershell_option_values(tokens, POWERSHELL_DEST_FLAGS),
    }

    positional = []
    skip_next = False
    for index, token in enumerate(tokens[1:], start=1):
        if skip_next:
            skip_next = False
            continue
        value = normalize_token(token)
        lowered = value.lower()
        if lowered in POWERSHELL_PATH_FLAGS:
            if index + 1 < len(tokens):
                skip_next = True
            continue
        if value.startswith("-") or value in CHAIN_OPERATORS:
            continue
        positional.append(value)

    if not details["path_values"]:
        if primary in {"remove-item", "set-content", "out-file", "clear-content"} and positional:
            details["path_values"] = [positional[0]]
        elif primary in {"copy-item", "move-item"} and positional:
            details["path_values"] = [positional[0]]
            if len(positional) > 1 and not details["destination_values"]:
                details["destination_values"] = [positional[1]]

    return details


def classify_command(command, _nested=False):
    tokens = split_command(command)
    primary = executable_name(tokens[0]) if tokens else ""
    subcommand = get_subcommand(tokens)
    categories = set()
    reasons = []
    risk = "low"

    if primary in READ_ONLY_COMMANDS:
        categories.add("read-capable")
    if primary in FILE_WRITE_COMMANDS and primary not in POWERSHELL_FILE_COMMANDS:
        categories.update({"write", "destructive"})
        risk = "high"
        reasons.append(f"{primary} can modify or remove local files")

    ps_details = powershell_file_details(tokens)
    if primary in POWERSHELL_DESTRUCTIVE_COMMANDS:
        categories.update({"write", "destructive"})
        risk = max_risk(risk, "high")
        reasons.append(f"{primary} can modify or remove local files")
    elif primary in POWERSHELL_WRITE_COMMANDS:
        categories.add("write")
        risk = max_risk(risk, "medium")
        reasons.append(f"{primary} can overwrite local file content")

    if primary in POWERSHELL_FILE_COMMANDS | POWERSHELL_DESTRUCTIVE_COMMANDS:
        if ps_details.get("uses_recurse"):
            risk = max_risk(risk, "critical" if primary == "remove-item" else "high")
            reasons.append(f"{primary} -Recurse expands the scope beyond a single item")
        if ps_details.get("uses_force"):
            risk = max_risk(risk, "high")
            reasons.append(f"{primary} -Force bypasses normal PowerShell safety checks")
        if ps_details.get("uses_path") and not ps_details.get("uses_literal_path"):
            reasons.append(f"{primary} -Path may expand wildcards in PowerShell")
        if ps_details.get("uses_literal_path"):
            reasons.append(f"{primary} -LiteralPath narrows matching by disabling wildcard expansion")
        if primary in {"copy-item", "move-item"} and not ps_details.get("destination_values"):
            risk = max_risk(risk, "high")
            reasons.append(f"{primary} destination could not be resolved from the command")

    if primary in PACKAGE_MANAGERS and subcommand in {"install", "add", "remove", "uninstall", "update"}:
        categories.add("write")
        risk = max_risk(risk, "medium")
        reasons.append(f"{primary} {subcommand} changes project dependencies")

    if primary == "git":
        if subcommand == "push" and "--force" in command and "--force-with-lease" not in command:
            categories.update({"write", "destructive"})
            risk = max_risk(risk, "high")
            reasons.append("force-push rewrites remote branch history")
        if subcommand == "reset" and "--hard" in command:
            categories.update({"write", "destructive"})
            risk = max_risk(risk, "critical")
            reasons.append("git reset --hard discards local changes")
        if subcommand == "clean" and re.search(r"(^|\s)-f", command):
            categories.update({"write", "destructive"})
            risk = max_risk(risk, "high")
            reasons.append("git clean permanently removes untracked files")
        if subcommand in {"push", "reset", "clean", "rebase", "checkout", "restore"}:
            categories.add("write")

    if primary == "docker" and "prune" in tokens:
        categories.update({"write", "destructive"})
        risk = max_risk(risk, "high")
        reasons.append("docker prune deletes resources across the local Docker host")
        if "-a" in tokens or "--all" in tokens or "--volumes" in tokens:
            risk = max_risk(risk, "critical")
            reasons.append("global prune with all images or volumes is hard to reverse")

    if primary == "kubectl" and subcommand in {"apply", "replace", "delete", "patch", "scale"}:
        categories.update({"write", "production-impacting"})
        risk = max_risk(risk, "high")
        reasons.append(f"kubectl {subcommand} changes cluster state")

    if primary == "terraform" and subcommand in {"apply", "destroy"}:
        categories.update({"write", "production-impacting"})
        risk = max_risk(risk, "high")
        reasons.append(f"terraform {subcommand} changes managed infrastructure")
        if subcommand == "destroy":
            risk = max_risk(risk, "critical")

    lowered = command.lower()
    if any(word in lowered for word in (" sudo ", " runas ", " -verb runas")) or lowered.startswith("sudo "):
        categories.add("privileged")
        risk = max_risk(risk, "high")
        reasons.append("command appears to require elevated privileges")

    if re.search(r"\b(prod|production)\b", lowered):
        categories.add("production-impacting")
        risk = max_risk(risk, "high")
        reasons.append("command explicitly references production")

    remote_exec = re.search(r"(?i)\b(curl|wget|invoke-webrequest|iwr)\b.*\|\s*(sh|bash|pwsh|powershell|cmd)\b", command)
    if remote_exec:
        categories.update({"write", "destructive", "remote-exec"})
        risk = max_risk(risk, "critical")
        reasons.append("download-and-execute pattern can run unreviewed remote code")

    if ">" in command or ">>" in command:
        categories.add("write")
        risk = max_risk(risk, "medium")
        reasons.append("shell redirection can overwrite or append files")

    nested_command = detect_nested_command(tokens)
    if nested_command and not _nested:
        nested = classify_compound_command(nested_command, nested=True)
        if nested["parts"]:
            risk = max_risk(risk, nested["risk"])
            categories.update(nested["categories"])
            for item in nested["reasons"]:
                if item not in reasons:
                    reasons.append(f"nested command: {item}")

    if not tokens:
        reasons.append("empty command")

    return {
        "risk": risk,
        "primary_command": primary,
        "subcommand": subcommand,
        "categories": sorted(categories),
        "reasons": reasons,
        "tokens": tokens,
        "nested_command": nested_command,
    }


def classify_compound_command(command, nested=False):
    segments = split_compound_command(command)
    parts = []
    combined_categories = set()
    reasons = []
    risk = "low"

    for segment in segments:
        if segment in CHAIN_OPERATORS:
            continue
        part = classify_command(segment, _nested=nested)
        parts.append({
            "command": segment,
            "risk": part["risk"],
            "primary_command": part["primary_command"],
            "subcommand": part["subcommand"],
            "categories": part["categories"],
            "reasons": part["reasons"],
        })
        risk = max_risk(risk, part["risk"])
        combined_categories.update(part["categories"])
        for item in part["reasons"]:
            if item not in reasons:
                reasons.append(item)

    if len(parts) > 1:
        reasons.append(f"compound command contains {len(parts)} executable segments")

    return {
        "risk": risk,
        "categories": sorted(combined_categories),
        "reasons": reasons,
        "parts": parts,
        "segments": segments,
    }


def find_secret_findings(command):
    patterns = [
        ("bearer", r"(?i)\bBearer\s+([A-Za-z0-9._\-+/=]{10,})", "critical"),
        ("jwt", r"\b(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)\b", "critical"),
        ("aws_access_key", r"\b(AKIA[0-9A-Z]{16})\b", "critical"),
        ("github_pat", r"\b(gh[pousr]_[A-Za-z0-9]{20,})\b", "critical"),
        ("openai_key", r"\b(sk-[A-Za-z0-9]{20,})\b", "critical"),
        ("generic_secret", r"(?i)\b(api[_-]?key|token|password|passwd|secret)\s*[:=]\s*([^\s'\"`]+)", "high"),
        ("cookie", r"(?i)\bcookie\s*[:=]\s*([^\s]+)", "high"),
    ]

    findings = []
    risk = "low"
    reasons = []

    for name, pattern, level in patterns:
        for match in re.finditer(pattern, command):
            value = match.group(match.lastindex or 0)
            masked = mask_secret(value)
            findings.append({"type": name, "match": masked, "risk": level})
            risk = max_risk(risk, level)
            if level == "critical":
                reasons.append(f"inline {name} looks like an active credential")
            else:
                reasons.append(f"inline {name} may leak sensitive data")

    return {"risk": risk, "findings": findings, "reasons": reasons}


def extract_path_candidates(command, tokens, classification):
    primary = classification["primary_command"]
    option_names = {
        "-f",
        "--file",
        "--filename",
        "-path",
        "-literalpath",
        "-destination",
        "-dest",
        "-target",
        "-source",
        "-src",
        "-out",
        "-output",
    }
    candidates = []
    ps_details = powershell_file_details(tokens)

    if primary in POWERSHELL_FILE_COMMANDS | POWERSHELL_DESTRUCTIVE_COMMANDS:
        candidates.extend(ps_details.get("path_values", []))
        candidates.extend(ps_details.get("destination_values", []))

    for index, token in enumerate(tokens):
        value = normalize_token(token)
        if not value or value in CHAIN_OPERATORS or value in {">", ">>"}:
            continue
        previous = normalize_token(tokens[index - 1]) if index > 0 else ""
        if previous.lower() in option_names and not value.startswith("-"):
            candidates.append(value)
            continue
        if primary in FILE_WRITE_COMMANDS and index > 0 and not value.startswith("-"):
            candidates.append(value)
            continue
        if primary in {"kubectl", "terraform"} and is_probable_path(value):
            candidates.append(value)
            continue
        if is_probable_path(value) and previous in {">", ">>"}:
            candidates.append(value)

    unique = []
    seen = set()
    for item in candidates:
        key = item.lower()
        if key not in seen:
            unique.append(item)
            seen.add(key)
    return unique


def path_findings(command, cwd, allowed_roots):
    classification = classify_command(command)
    tokens = classification["tokens"]
    roots = [os.path.abspath(root) for root in (allowed_roots or [cwd])]
    destructive = "destructive" in classification["categories"]
    ps_details = powershell_file_details(tokens)
    literal_mode = bool(ps_details.get("uses_literal_path"))
    findings = []
    risk = "low"
    resolved_candidates = []

    for raw in extract_path_candidates(command, tokens, classification):
        if is_remote_path(raw):
            continue
        resolved = resolve_path(raw, cwd)
        resolved_candidates.append({"raw": raw, "resolved": resolved})
        normalized = normalize_token(raw)
        broad = normalized in {".", "..", "/", "\\", "*", ".\\*", "./*", "*.*"}
        broad = broad or re.match(r"^[a-zA-Z]:\\?$", normalized or "") is not None

        if broad and destructive:
            findings.append({
                "type": "broad-target",
                "raw": raw,
                "resolved": resolved,
                "reason": "destructive command targets a broad path",
            })
            risk = max_risk(risk, "critical")

        if resolved and not path_within_roots(resolved, roots):
            findings.append({
                "type": "path-escape",
                "raw": raw,
                "resolved": resolved,
                "reason": "target resolves outside the allowed roots",
            })
            risk = max_risk(risk, "critical" if destructive else "high")
            continue

        if destructive and resolved and any(os.path.abspath(resolved) == root for root in roots):
            findings.append({
                "type": "root-target",
                "raw": raw,
                "resolved": resolved,
                "reason": "destructive command points at the workspace root",
            })
            risk = max_risk(risk, "critical")

        if destructive and ("*" in normalized or "?" in normalized) and not literal_mode:
            findings.append({
                "type": "wildcard-target",
                "raw": raw,
                "resolved": resolved,
                "reason": "destructive wildcard may match more files than intended",
            })
            risk = max_risk(risk, "high")

    reasons = [item["reason"] for item in findings]
    return {"risk": risk, "candidates": resolved_candidates, "findings": findings, "reasons": reasons}


def git_context(cwd):
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=cwd, stderr=subprocess.DEVNULL, text=True).strip()
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd, stderr=subprocess.DEVNULL, text=True).strip()
        status = subprocess.check_output(["git", "status", "--porcelain"], cwd=cwd, stderr=subprocess.DEVNULL, text=True)
        return {
            "in_repo": True,
            "repo_root": root,
            "branch": branch,
            "is_default_branch": branch in {"main", "master"},
            "dirty": bool(status.strip()),
        }
    except Exception:
        return {
            "in_repo": False,
            "repo_root": "",
            "branch": "",
            "is_default_branch": False,
            "dirty": False,
        }


def context_findings(command, cwd):
    classification = classify_command(command)
    primary = classification["primary_command"]
    subcommand = classification["subcommand"]
    reasons = []
    risk = "low"
    details = {}

    if primary == "git":
        git_info = git_context(cwd)
        details["git"] = git_info
        if git_info["in_repo"]:
            if git_info["is_default_branch"] and subcommand in {"push", "reset", "clean", "rebase", "checkout", "restore"}:
                risk = max_risk(risk, "high")
                reasons.append(f"git operation is running on default branch {git_info['branch']}")
            if git_info["dirty"] and subcommand in {"reset", "clean", "checkout", "restore", "rebase"}:
                risk = max_risk(risk, "high")
                reasons.append("git working tree has uncommitted changes")
    return {"risk": risk, "reasons": reasons, "details": details}


def rollback_hints(command, cwd=None):
    classification = classify_command(command)
    primary = classification["primary_command"]
    subcommand = classification["subcommand"]
    hints = []

    if primary == "git":
        branch = ""
        if cwd:
            branch = git_context(cwd).get("branch", "")
        suffix = f"-{branch}" if branch and branch not in {"HEAD", ""} else ""
        if subcommand == "push" and "--force" in command:
            hints.extend([
                f"Create a backup branch before rewriting remote history: git branch backup/pre-force-push{suffix} HEAD",
                "Use git reflog locally if you need to restore the previous tip",
            ])
        elif subcommand == "reset" and "--hard" in command:
            hints.extend([
                f"Create a backup ref before reset: git branch backup/pre-reset{suffix} HEAD",
                "Recover with git reflog and git reset --hard <previous-sha> if needed",
            ])
        elif subcommand == "clean":
            hints.extend([
                "Preview deletions with git clean -ndx before running the destructive variant",
                "Recover only from backups or regeneration after git clean removes ignored files",
            ])

    if primary == "kubectl":
        hints.extend([
            "Export current resources before changes: kubectl get -o yaml > backup.yaml",
            "Use kubectl rollout undo for deployment regressions where supported",
        ])

    if primary == "terraform":
        hints.extend([
            "Save a reviewed plan first: terraform plan -out=tfplan",
            "Back up the current state before apply or destroy",
        ])

    if primary == "docker" and "prune" in classification["tokens"]:
        hints.extend([
            "List affected resources before pruning and keep image or volume names handy",
            "Back up named volumes before global prune if data matters",
        ])

    if primary in PACKAGE_MANAGERS:
        hints.extend([
            "Commit or snapshot manifest and lockfile changes before dependency updates",
            "Use version control to revert package changes if the install breaks the build",
        ])

    if primary in {"rm", "del", "erase", "rmdir", "remove-item", "mv", "move-item"}:
        hints.extend([
            "Prefer moving files to a quarantine directory before permanent deletion",
            "Capture a directory listing or archive first if the data is not reproducible",
        ])

    if primary in {"copy-item", "set-content", "out-file", "clear-content"}:
        hints.extend([
            "Create a backup copy or commit before overwriting file content",
            "Capture the previous file contents if the change is not trivially reproducible",
        ])

    seen = []
    for hint in hints:
        if hint not in seen:
            seen.append(hint)
    return seen


def safer_actions(command, cwd=None):
    classification = classify_command(command)
    primary = classification["primary_command"]
    subcommand = classification["subcommand"]
    actions = []
    safer_commands = []

    git_info = git_context(cwd) if cwd and primary == "git" else {"branch": "", "is_default_branch": False}
    branch_suffix = f"-{git_info['branch']}" if git_info.get("branch") not in {"", "HEAD"} else ""

    if primary == "git" and subcommand == "push" and "--force" in command and "--force-with-lease" not in command:
        actions.extend([
            "Create a backup branch first",
            "Use git push --force-with-lease instead of plain --force",
        ])
        safer_commands.extend([
            f"git branch backup/pre-force-push{branch_suffix} HEAD",
            command.replace("--force", "--force-with-lease", 1),
        ])

    if primary == "git" and subcommand == "reset" and "--hard" in command:
        actions.extend([
            "Create a safety branch before reset",
            "Prefer git restore or git stash if the goal is not full discard",
        ])
        safer_commands.append(f"git branch backup/pre-reset{branch_suffix} HEAD")

    if primary == "git" and subcommand == "clean":
        actions.extend([
            "Preview the clean operation before deleting untracked files",
            "Create a backup or archive if ignored files matter",
        ])
        safer_commands.append("git clean -ndx")

    if re.search(r"(?i)\b(curl|wget|invoke-webrequest|iwr)\b.*\|\s*(sh|bash|pwsh|powershell|cmd)\b", command):
        actions.extend([
            "Download the script to a file, inspect it, and verify checksum or signature before execution",
            "Run the local reviewed script instead of piping remote output directly into a shell",
        ])

    if primary == "kubectl" and subcommand in {"apply", "delete", "replace"}:
        actions.extend([
            "Run kubectl diff or a server-side dry run before the live change",
            "Export the current resource YAML before applying or deleting",
        ])

    if primary == "terraform" and subcommand in {"apply", "destroy"}:
        actions.extend([
            "Run terraform plan -out=tfplan and review the saved plan before execution",
            "Back up state and prefer narrower targets when possible",
        ])

    if primary == "docker" and "prune" in classification["tokens"]:
        actions.extend([
            "Inspect docker image ls, docker container ls -a, and docker volume ls before pruning",
            "Use targeted docker image rm or docker volume rm if only a subset should be removed",
        ])

    if primary in {"rm", "del", "erase", "rmdir", "remove-item", "mv", "move-item"}:
        actions.extend([
            "Resolve the exact target path first and prefer a literal path over a wildcard",
            "List the target contents before deletion or move if scope is not obvious",
        ])

    if primary in {"copy-item", "set-content", "out-file", "clear-content"}:
        actions.extend([
            "Resolve the exact destination path first and prefer -LiteralPath when wildcards are unintended",
            "Create a backup or dry-run equivalent before overwriting content",
        ])

    if not actions and classification["risk"] in {"medium", "high", "critical"}:
        actions.append("Narrow the target, remove inline secrets, and create a rollback checkpoint before running the command")

    dedup_actions = []
    for action in actions:
        if action not in dedup_actions:
            dedup_actions.append(action)

    dedup_commands = []
    for item in safer_commands:
        if item and item not in dedup_commands:
            dedup_commands.append(item)

    return {"actions": dedup_actions, "commands": dedup_commands}


def preflight_report(command, cwd, allowed_roots):
    compound = classify_compound_command(command)
    classification = classify_command(command)
    secrets = find_secret_findings(command)
    paths = path_findings(command, cwd, allowed_roots)
    context = context_findings(command, cwd)

    display_parts = list(compound["parts"])
    nested_command = classification.get("nested_command", "")
    nested_compound = classify_compound_command(nested_command, nested=True) if nested_command else {"parts": [], "risk": "low", "categories": [], "reasons": []}
    if nested_compound["parts"]:
        display_parts = nested_compound["parts"]

    rollback = rollback_hints(command, cwd=cwd)
    safer = safer_actions(command, cwd=cwd)

    part_sources = display_parts if display_parts else compound["parts"]
    if len(part_sources) > 0:
        for part in part_sources:
            for item in rollback_hints(part["command"], cwd=cwd):
                if item not in rollback:
                    rollback.append(item)
            part_safer = safer_actions(part["command"], cwd=cwd)
            for item in part_safer["actions"]:
                if item not in safer["actions"]:
                    safer["actions"].append(item)
            for item in part_safer["commands"]:
                if item not in safer["commands"]:
                    safer["commands"].append(item)

    risk = max_risk(classification["risk"], compound["risk"], nested_compound["risk"], secrets["risk"], paths["risk"], context["risk"])

    categories = sorted(set(classification["categories"]) | set(compound["categories"]) | set(nested_compound.get("categories", [])))

    reason_groups = [classification["reasons"], compound["reasons"], secrets["reasons"], paths["reasons"], context["reasons"]]
    if nested_compound.get("parts") and display_parts == nested_compound["parts"]:
        reason_groups.insert(2, nested_compound.get("reasons", []))

    reasons = []
    seen_reason_suffixes = set()
    for group in reason_groups:
        for item in group:
            suffix = item.replace("nested command: ", "")
            if suffix in seen_reason_suffixes:
                continue
            if item not in reasons:
                reasons.append(item)
                seen_reason_suffixes.add(suffix)

    need_approval = risk in {"high", "critical"}

    return {
        "command": command,
        "cwd": os.path.abspath(cwd),
        "allowed_roots": [os.path.abspath(root) for root in (allowed_roots or [cwd])],
        "risk": risk,
        "need_approval": need_approval,
        "primary_command": classification["primary_command"],
        "subcommand": classification["subcommand"],
        "categories": categories,
        "reasons": reasons,
        "compound_parts": display_parts,
        "path_findings": paths["findings"],
        "secret_findings": secrets["findings"],
        "context_findings": context["details"],
        "rollback": rollback,
        "safer_actions": safer["actions"],
        "safer_commands": safer["commands"],
    }

import os
import platform
import re
import subprocess
import tempfile
import hashlib
from typing import Dict, List

def get_secure_workspace(base_dir=None):
    """
    Creates a secure directory for storing sensitive logs and traces.
    Restricts access to the current user only.
    """
    if base_dir is None:
        # Default to a .secure_workspace folder inside the skill directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    secure_dir = os.path.join(base_dir, ".secure_workspace")
    
    if not os.path.exists(secure_dir):
        os.makedirs(secure_dir)
        _secure_directory(secure_dir)
    else:
        _secure_directory(secure_dir)
        
    return secure_dir

def _secure_directory(path):
    """
    Restricts directory permissions to the current user only.
    """
    system = platform.system()
    
    try:
        if system == "Windows":
            # Windows: Use icacls to remove inheritance and grant full control to current user only
            # /inheritance:r - Remove all inherited ACEs
            # /grant:r "%USERNAME%":(OI)(CI)F - Grant Full access to current user, verify inheritance
            username = os.environ.get("USERNAME")
            if username:
                # 1. Break inheritance and remove existing permissions
                subprocess.run(['icacls', path, '/inheritance:r'], check=True, capture_output=True)
                # 2. Grant full control to current user
                subprocess.run(['icacls', path, '/grant:r', f'{username}:(OI)(CI)F'], check=True, capture_output=True)
                
        else:
            # Linux/Mac: chmod 700 (rwx------)
            os.chmod(path, 0o700)
            
    except Exception as e:
        print(f"Warning: Failed to set secure permissions on {path}: {e}")

def clean_secure_workspace(path):
    """
    Securely removes files in the workspace.
    """
    if os.path.exists(path):
        for f in os.listdir(path):
            file_path = os.path.join(path, f)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error cleaning up {file_path}: {e}")


def assert_safe_file_target(path, must_exist=True, require_write=False):
    """
    Validates file path safety and basic permission requirements.
    - Rejects symlinks.
    - Ensures path points to a regular file.
    - Validates read/write permissions when required.
    - On POSIX, rejects world/group writable files and directories.
    """
    abs_path = os.path.abspath(path)
    parent_dir = os.path.dirname(abs_path) or "."

    if os.path.islink(abs_path):
        raise PermissionError(f"Unsafe path (symlink not allowed): {abs_path}")

    if must_exist:
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"File not found: {abs_path}")
        if not os.path.isfile(abs_path):
            raise PermissionError(f"Path is not a regular file: {abs_path}")
        if not os.access(abs_path, os.R_OK):
            raise PermissionError(f"No read permission: {abs_path}")
        if require_write and not os.access(abs_path, os.W_OK):
            raise PermissionError(f"No write permission: {abs_path}")

    if not os.path.exists(parent_dir):
        raise FileNotFoundError(f"Parent directory not found: {parent_dir}")
    if require_write and not os.access(parent_dir, os.W_OK):
        raise PermissionError(f"No write permission on parent directory: {parent_dir}")

    if platform.system() != "Windows":
        try:
            parent_mode = os.stat(parent_dir).st_mode & 0o777
            if parent_mode & 0o022:
                raise PermissionError(f"Insecure directory permissions: {parent_dir} ({oct(parent_mode)})")
            if os.path.exists(abs_path):
                file_mode = os.stat(abs_path).st_mode & 0o777
                if file_mode & 0o022:
                    raise PermissionError(f"Insecure file permissions: {abs_path} ({oct(file_mode)})")
        except OSError as e:
            raise PermissionError(f"Failed to verify permissions for {abs_path}: {e}") from e

    return abs_path


def _secure_file(path):
    """
    Restricts file permissions to the current user when possible.
    """
    try:
        if platform.system() == "Windows":
            username = os.environ.get("USERNAME")
            if username and os.path.exists(path):
                subprocess.run(["icacls", path, "/inheritance:r"], check=True, capture_output=True)
                subprocess.run(["icacls", path, "/grant:r", f"{username}:F"], check=True, capture_output=True)
        else:
            if os.path.exists(path):
                os.chmod(path, 0o600)
    except Exception as e:
        print(f"Warning: Failed to set secure permissions on file {path}: {e}")


def atomic_write_text(file_path, content, encoding="utf-8"):
    """
    Writes content atomically via temporary file + replace.
    """
    abs_path = os.path.abspath(file_path)
    parent_dir = os.path.dirname(abs_path) or "."
    os.makedirs(parent_dir, exist_ok=True)
    assert_safe_file_target(abs_path, must_exist=False, require_write=True)

    fd, temp_path = tempfile.mkstemp(prefix=".tmp_", dir=parent_dir, text=True)
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, abs_path)
        _secure_file(abs_path)
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass


def atomic_append_text(file_path, content, encoding="utf-8"):
    """
    Appends text atomically by read-modify-replace.
    """
    abs_path = os.path.abspath(file_path)
    existing = ""
    if os.path.exists(abs_path):
        assert_safe_file_target(abs_path, must_exist=True, require_write=True)
        with open(abs_path, "r", encoding=encoding) as f:
            existing = f.read()
    atomic_write_text(abs_path, existing + content, encoding=encoding)


HIGH_RISK_COMMAND_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\bmkfs(\.\w+)?\b",
    r"\bdd\s+if=",
    r">\s*/dev/sd[a-z]",
    r"\bchmod\s+777\b",
    r"\bchown\b",
    r"\bpkill\b",
    r"\bkillall\b",
    r"\bcurl\b",
    r"\bwget\b",
    r"\b(cat|type)\s+(/etc/passwd|/etc/shadow)\b",
]

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"disregard\s+all\s+prior\s+constraints",
    r"system\s+prompt",
    r"developer\s+message",
    r"you\s+are\s+now\s+in\s+developer\s+mode",
]


def _scan_patterns(text: str, patterns: List[str], scanner_name: str, severity: str) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            issues.append({
                "scanner": scanner_name,
                "severity": severity,
                "pattern": pattern,
                "message": f"Matched pattern: {pattern}"
            })
    return issues


def run_multi_security_scans(original_content: str, new_content: str, context_text: str = "") -> Dict[str, object]:
    """
    Runs layered security checks:
    1) Diff-aware high-risk command detection (new-only suspicious additions)
    2) Absolute blocklist scan on generated content
    3) Prompt-injection marker scan on generated content and context
    """
    issues: List[Dict[str, str]] = []
    original_lower = original_content.lower()
    new_lower = new_content.lower()

    for pattern in HIGH_RISK_COMMAND_PATTERNS:
        new_match = re.search(pattern, new_lower, re.IGNORECASE)
        old_match = re.search(pattern, original_lower, re.IGNORECASE)
        if new_match and not old_match:
            issues.append({
                "scanner": "diff_high_risk",
                "severity": "critical",
                "pattern": pattern,
                "message": f"New high-risk behavior introduced: {pattern}"
            })

    issues.extend(_scan_patterns(new_content, HIGH_RISK_COMMAND_PATTERNS, "blocklist_generated", "high"))
    issues.extend(_scan_patterns(new_content, PROMPT_INJECTION_PATTERNS, "prompt_injection_generated", "high"))

    if context_text:
        issues.extend(_scan_patterns(context_text, PROMPT_INJECTION_PATTERNS, "prompt_injection_context", "medium"))

    blocking_levels = {"critical", "high"}
    passed = not any(issue["severity"] in blocking_levels for issue in issues)
    return {"passed": passed, "issues": issues}


def sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _split_frontmatter(markdown: str):
    if not markdown.startswith("---\n"):
        return "", markdown
    end = markdown.find("\n---\n", 4)
    if end == -1:
        return "", markdown
    frontmatter = markdown[: end + 5]
    body = markdown[end + 5 :]
    return frontmatter, body


def assert_frontmatter_unchanged(original_markdown: str, candidate_markdown: str):
    original_frontmatter, _ = _split_frontmatter(original_markdown)
    candidate_frontmatter, _ = _split_frontmatter(candidate_markdown)
    if original_frontmatter != candidate_frontmatter:
        raise PermissionError("Frontmatter change detected and blocked by policy.")


def _parse_h2_sections(body: str):
    pattern = re.compile(r"(?m)^##\s+(.+?)\s*$")
    matches = list(pattern.finditer(body))
    if not matches:
        return body, [], {}

    preamble = body[: matches[0].start()]
    ordered_titles = []
    sections = {}
    for idx, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        ordered_titles.append(title)
        sections[title] = body[start:end].rstrip() + "\n"
    return preamble, ordered_titles, sections


def enforce_section_whitelist(original_markdown: str, candidate_markdown: str, allowed_sections: List[str]) -> str:
    original_frontmatter, original_body = _split_frontmatter(original_markdown)
    _, candidate_body = _split_frontmatter(candidate_markdown)

    original_preamble, original_titles, original_sections = _parse_h2_sections(original_body)
    _, _, candidate_sections = _parse_h2_sections(candidate_body)

    allowed_set = {s.strip() for s in allowed_sections if s.strip()}
    if not allowed_set:
        return original_markdown

    merged_sections = dict(original_sections)
    for title in allowed_set:
        if title in candidate_sections:
            merged_sections[title] = candidate_sections[title]

    merged_body_parts = [original_preamble.rstrip() + "\n\n" if original_preamble.strip() else ""]
    for title in original_titles:
        section_text = merged_sections.get(title, original_sections.get(title, ""))
        if section_text:
            merged_body_parts.append(section_text.rstrip() + "\n\n")

    for title in allowed_set:
        if title in candidate_sections and title not in original_sections:
            merged_body_parts.append(candidate_sections[title].rstrip() + "\n\n")

    merged_body = "".join(merged_body_parts).rstrip() + "\n"
    return (original_frontmatter + merged_body) if original_frontmatter else merged_body

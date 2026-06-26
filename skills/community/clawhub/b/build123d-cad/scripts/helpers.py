"""Shared helpers for build123d CAD scripts.

Security: user-supplied scripts NEVER execute in the parent process.
All execution happens in a sandboxed subprocess with:
  - Static validation blocks dangerous imports, builtins, and patterns
  - Clean environment (no API keys, tokens, secrets)
  - Isolated tmpdir as cwd
  - Timeout (default 120s for complex geometry)
  - Result communicated via a JSON file, not stdout parsing

The parent constructs a full Python script (user code + operation), writes it
to a temp file, runs it in a subprocess, reads the result JSON file.
No geometry objects cross the process boundary.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


WORKSPACE = Path(os.environ.get("CAD_WORKSPACE", os.path.expanduser("~/.openclaw/workspace/cad-output")))
WORKSPACE.mkdir(parents=True, exist_ok=True)

# Modules the user script is allowed to import. Anything else is blocked.
ALLOWED_IMPORTS = {
    "build123d", "math", "typing", "dataclasses", "enum", "functools",
    "itertools", "collections", "copy", "json",
}

# Patterns that must never appear in user scripts.
BLOCKED_PATTERNS = [
    r"\bsubprocess\b",
    r"\bos\.system\b",
    r"\bos\.popen\b",
    r"\bos\.exec\b",
    r"\bos\.spawn\b",
    r"\bos\.remove\b",
    r"\bos\.unlink\b",
    r"\bos\.rmdir\b",
    r"\bshutil\.rmtree\b",
    r"\bshutil\.move\b",
    r"\b__import__\b",
    r"\bimportlib\b",
    r"\beval\s*\(",
    r"\bexec\s*\(",
    r"\bcompile\s*\(",
    r"\bopen\s*\(",
    r"\bsocket\b",
    r"\burllib\b",
    r"\brequests\b",
    r"\bhttpx\b",
    r"\bhttp\.\b",
    r"\bctypes\b",
    r"\bsignal\b",
    r"\bpickle\b",
    r"\bshelve\b",
    r"\bglobals\s*\(",
    r"\blocals\s*\(",
    r"\bbreakpoint\s*\(",
]


def validate_script(script: str) -> str | None:
    """Check script for disallowed patterns. Returns error message or None if clean."""
    for pattern in BLOCKED_PATTERNS:
        match = re.search(pattern, script)
        if match:
            return f"Blocked: script contains disallowed pattern '{match.group()}'"

    # Check imports — only allow whitelisted modules
    for match in re.finditer(r"(?:from|import)\s+([\w.]+)", script):
        module = match.group(1).split(".")[0]
        if module not in ALLOWED_IMPORTS:
            return f"Blocked: import of '{module}' is not allowed. Allowed: {', '.join(sorted(ALLOWED_IMPORTS))}"

    return None


def _extract_user_script(full_script: str) -> str | None:
    """Extract user code between marker comments, or return None if no markers."""
    m = re.search(
        r"# --- user script ---\n(.*?)# --- end user script ---",
        full_script, re.DOTALL,
    )
    return m.group(1) if m else None


def run_sandboxed(full_script: str, timeout: int = 120) -> dict:
    """Run a complete Python script in a sandboxed subprocess.

    The script must write JSON to the path in env var _RESULT_PATH.
    User code (between marker comments) is validated before execution.
    """
    user_code = _extract_user_script(full_script)
    if user_code is not None:
        violation = validate_script(user_code)
        if violation:
            return {"success": False, "error": violation}
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = Path(tmpdir) / "run.py"
        result_path = Path(tmpdir) / "result.json"
        script_path.write_text(full_script)

        clean_env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": tmpdir,
            "TMPDIR": tmpdir,
            "PYTHONDONTWRITEBYTECODE": "1",
            "_RESULT_PATH": str(result_path),
            "_WORKSPACE": str(WORKSPACE),
        }
        venv = os.environ.get("VIRTUAL_ENV")
        if venv:
            clean_env["VIRTUAL_ENV"] = venv
            clean_env["PATH"] = f"{venv}/bin:{clean_env['PATH']}"

        try:
            proc = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True, text=True,
                timeout=timeout, cwd=tmpdir, env=clean_env,
            )
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Script timed out after {timeout}s."}

        if result_path.exists():
            try:
                return json.loads(result_path.read_text())
            except (json.JSONDecodeError, OSError) as e:
                return {"success": False, "error": f"Bad result file: {e}", "stderr": proc.stderr[-2000:]}

        return {
            "success": False,
            "error": proc.stderr[-2000:] if proc.stderr else "No result produced.",
            "stdout": proc.stdout[-2000:],
        }


def output_json(data: dict):
    print(json.dumps(data))
    sys.exit(0 if data.get("success", False) else 1)

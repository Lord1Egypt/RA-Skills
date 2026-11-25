#!/usr/bin/env python3
"""Guarded privileged execution with approval, policy checks, and audit logging.

How a command is approved
- Approval is asked for and answered on the controlling terminal (/dev/tty), never
  on stdin. A caller that pipes "y" into this script cannot approve its own command,
  and with no terminal attached the command is refused.
- With --use-sudo, the command runs as "sudo -k -- command": sudo ignores any cached
  credentials for that run, so it asks for the user's password every time. That
  prompt is enforced by the operating system and is the control that holds even
  against a process running as the same user. It cannot be switched off by a flag
  or an environment variable.
- The sudo binary is one of a fixed list of system paths, never taken from the
  environment, and the command that runs is the fully resolved path that was
  validated and shown for approval.
- An optional approval token (OPENCLAW_APPROVAL_TOKEN) is typed without echo.

Settings are read from ~/.openclaw/env and the process environment (see
security_config.py). Review before enabling. No network calls are made.

Exit codes
   0  command ran (its own exit code is returned when non-zero)
   1  approval denied
   2  no command supplied
   3  blocked by command policy
   4  approval token incorrect
   5  untrusted source not confirmed
   6  task session id required but missing
   7  required policy files missing
   8  command failed validation
   9  sudo binary failed validation
  10  audit log could not be written
  11  no terminal available to ask for approval
"""
import argparse
import hmac
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Allow importing sibling modules when executed from arbitrary cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import security_config  # noqa: E402
from audit_logger import append_audit  # noqa: E402
from command_policy import evaluate_command  # noqa: E402
from prompt_policy import load_policy  # noqa: E402

# Bare command names ("ls") are resolved here only: system directories that are root-owned.
SAFE_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"
SAFE_ENV_VARS = {
    "PATH": SAFE_PATH,
    "LANG": os.environ.get("LANG", "C.UTF-8"),
    "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
    "HOME": os.environ.get("HOME", "/root"),
    "TERM": os.environ.get("TERM", "dumb"),
}
# Explicit allowlist: only the vars above are passed to subprocesses.
# LD_PRELOAD, LD_LIBRARY_PATH, PYTHONPATH, IFS, CDPATH, etc. are excluded.

EXIT_AUDIT_FAILED = 10
EXIT_NO_TERMINAL = 11

# The only places sudo is looked for. Not configurable: a caller-supplied path could
# name a program that skips authentication.
SUDO_CANDIDATES = ("/usr/bin/sudo", "/bin/sudo", "/usr/local/bin/sudo")
MAX_TIMEOUT_MINUTES = 30


class TerminalPrompter:
    """Talks to the person at the controlling terminal, bypassing stdin and stdout."""

    def _paths(self) -> Tuple[str, str]:
        return ("CONIN$", "CONOUT$") if os.name == "nt" else ("/dev/tty", "/dev/tty")

    def available(self) -> bool:
        try:
            with open(self._paths()[0], "r"):
                return True
        except OSError:
            return False

    def show(self, text: str) -> None:
        with open(self._paths()[1], "w") as out:
            out.write(text + "\n")

    def ask(self, prompt: str) -> str:
        reader, writer = self._paths()
        with open(writer, "w") as out:
            out.write(prompt)
            out.flush()
        with open(reader, "r") as tty:
            return tty.readline().strip()

    def secret(self, prompt: str) -> str:
        """Like ask(), without echoing what is typed (where the terminal allows it)."""
        if os.name == "nt":
            return self.ask(prompt)
        import termios

        with open("/dev/tty", "r+") as tty:
            tty.write(prompt)
            tty.flush()
            fd = tty.fileno()
            old = termios.tcgetattr(fd)
            new = termios.tcgetattr(fd)
            new[3] &= ~termios.ECHO
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, new)
                value = tty.readline().strip()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
                tty.write("\n")
            return value


def run_guard(args, *guard_args):
    # A caller may shorten the idle timeout but never lengthen it.
    timeout = min(max(1, args.timeout_minutes), MAX_TIMEOUT_MINUTES)
    cmd = [
        sys.executable,
        str(Path(__file__).with_name("root_session_guard.py")),
        "--state-file",
        args.state_file,
        "--timeout-minutes",
        str(timeout),
        *guard_args,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def obtain_approval(
    prompter,
    reason: str,
    command_argv: List[str],
    token_required: Optional[str] = None,
    audit: bool = True,
) -> Tuple[bool, str]:
    """Ask the person at the terminal to approve ``command_argv``.

    Returns (approved, outcome) where outcome is one of "approved", "no_terminal",
    "denied" or "token_failed".
    """

    def record(event):
        if audit:
            append_audit(event)

    record({"action": "approval_requested", "reason": reason, "argv": command_argv})
    if not prompter.available():
        record({"action": "approval_unavailable", "reason": "no terminal", "argv": command_argv})
        return False, "no_terminal"

    prompter.show("Approval required for elevated execution.")
    prompter.show(f"Reason: {reason}")
    prompter.show("Command argv:")
    prompter.show(json.dumps(command_argv, indent=2))
    answer = prompter.ask("Approve elevated access for this command? [y/N]: ").strip().lower()
    approved = answer in {"y", "yes"}
    record({"action": "approval_decision", "reason": reason, "argv": command_argv, "approved": approved})
    if not approved:
        return False, "denied"

    if token_required:
        token = prompter.secret("Enter approval token: ")
        if not hmac.compare_digest(token.encode("utf-8"), token_required.encode("utf-8")):
            record({"action": "approval_token_failed", "argv": command_argv})
            return False, "token_failed"
        record({"action": "approval_token_ok", "argv": command_argv})
    return True, "approved"


def _validate_binary(path: str, allow_setuid: bool = False) -> Optional[str]:
    """Validate a binary path. Returns error string if invalid, else None."""
    if not path:
        return "missing binary"
    if not os.path.isabs(path):
        return "binary path must be absolute"
    real = os.path.realpath(path)
    if not os.path.exists(real):
        return "binary path does not exist"
    try:
        st = os.stat(real)
    except Exception:
        return "cannot stat binary"
    # must be root owned and not group/other writable
    if st.st_uid != 0:
        return "binary is not root-owned"
    if (st.st_mode & 0o022) != 0:
        return "binary is group/other writable"
    if not allow_setuid and (st.st_mode & 0o6000):
        return "binary has setuid/setgid bit set"
    return None


def resolve_command(argv: List[str], search_path: str = SAFE_PATH) -> Tuple[List[str], Optional[str]]:
    """Turn a bare command name into its absolute path in the system directories.

    Returns (argv, error). A name is looked up in ``search_path`` only, never the
    caller's PATH, so a binary planted earlier on PATH cannot be picked up.
    """
    if not argv:
        return argv, "empty argv"
    head = argv[0]
    if head.startswith("-"):
        return argv, (
            "command must not start with an option; sudo options such as -u or -E are not "
            "supported through the guard"
        )
    if os.sep in head or (os.altsep and os.altsep in head):
        return argv, None
    found = shutil.which(head, path=search_path)
    if not found:
        return argv, f"'{head}' was not found in the system directories ({search_path}); give its absolute path"
    return [found] + argv[1:], None


def _validate_command_argv(argv: List[str]) -> Optional[str]:
    if not argv:
        return "empty argv"
    if argv[0].startswith("-"):
        return "command must not start with an option"
    if not os.path.isabs(argv[0]):
        return "command path must be absolute"
    real = os.path.realpath(argv[0])
    if not os.path.exists(real):
        return "command path does not exist"
    try:
        st = os.stat(real)
    except Exception:
        return "cannot stat command"
    if st.st_uid != 0:
        return (
            "command binary is not root-owned (a binary the user can overwrite could be "
            "swapped before it runs as root)"
        )
    if (st.st_mode & 0o022) != 0:
        return "command binary is group/other writable"
    if st.st_mode & 0o6000:
        return "command binary has setuid/setgid bit set"
    return None


def find_sudo() -> Optional[str]:
    """The system's sudo: root-owned, not writable by others, from a fixed list of paths."""
    for candidate in SUDO_CANDIDATES:
        if _validate_binary(candidate, allow_setuid=True) is None:
            return candidate
    return None


def run_command(argv: List[str], use_sudo: bool) -> int:
    exec_argv = argv
    if use_sudo:
        sudo_bin = find_sudo()
        if sudo_bin is None:
            append_audit({"action": "sudo_binary_invalid", "candidates": list(SUDO_CANDIDATES)})
            print("No valid sudo binary found in the system directories.", file=sys.stderr)
            return 9
        # "-k" with a command makes sudo ignore cached credentials for this run and not
        # refresh them, so the password prompt cannot be skipped.
        exec_argv = [sudo_bin, "-k", "--"] + argv
    print("Executing argv:")
    print(json.dumps(exec_argv, indent=2))
    append_audit({"action": "exec_start", "argv": argv, "use_sudo": use_sudo})
    result = subprocess.run(exec_argv, env=SAFE_ENV_VARS)
    append_audit({"action": "exec_finish", "argv": argv, "use_sudo": use_sudo, "returncode": result.returncode})
    return result.returncode


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute privileged commands with approval + idle-timeout guard",
    )
    parser.add_argument(
        "--state-file",
        default=str(Path.home() / ".openclaw" / "security" / "root-session-state.json"),
        help="Path to root session state file",
    )
    parser.add_argument(
        "--timeout-minutes",
        type=int,
        default=30,
        help="Idle timeout for elevated mode / approval session",
    )
    parser.add_argument(
        "--reason",
        required=True,
        help="Business/security reason for privileged command",
    )
    parser.add_argument(
        "--use-sudo",
        action="store_true",
        help="Prefix command with sudo",
    )
    # Accepted for compatibility with older callers. Cached sudo credentials are always
    # ignored now, so the flag changes nothing.
    parser.add_argument("--sudo-kill-cache", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument(
        "--keep-session",
        action="store_true",
        default=False,
        help="Keep elevated session after command (still restricted to allowlisted argv; expires on idle timeout)",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help='Command to run, e.g. -- /usr/bin/systemctl restart nginx',
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None, prompter=None) -> int:
    args = parse_args(argv)
    prompter = TerminalPrompter() if prompter is None else prompter
    if not args.command:
        print("No command supplied.", file=sys.stderr)
        return 2

    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        print("No command supplied after -- delimiter.", file=sys.stderr)
        return 2

    settings = security_config.load_env_file()

    # A privileged action that cannot be recorded does not run (unless explicitly made optional).
    if not append_audit({"action": "guard_invoked", "reason": args.reason, "argv": command}):
        if not security_config.flag("OPENCLAW_AUDIT_OPTIONAL", settings):
            print(
                "Audit log could not be written. Refusing privileged execution "
                "(set OPENCLAW_AUDIT_OPTIONAL=1 to allow it).",
                file=sys.stderr,
            )
            return EXIT_AUDIT_FAILED

    if security_config.flag("OPENCLAW_REQUIRE_POLICY_FILES", settings):
        required = [
            Path.home() / ".openclaw" / "security" / "command-policy.json",
            Path.home() / ".openclaw" / "security" / "approved_ports.json",
            Path.home() / ".openclaw" / "security" / "egress_allowlist.json",
        ]
        missing = [str(p) for p in required if not p.exists()]
        if missing:
            append_audit({"action": "policy_files_missing", "missing": missing})
            print("Missing required policy files. Refusing privileged execution.", file=sys.stderr)
            return 7

    # Resolve bare names in the system directories, then validate path + ownership.
    command, err = resolve_command(command)
    err = err or _validate_command_argv(command)
    if err:
        append_audit({"action": "command_invalid", "argv": command, "error": err})
        print(f"Invalid command: {err}", file=sys.stderr)
        return 8

    # From here on the command is the fully resolved file that was just validated. A
    # symbolic link cannot be repointed between the check, the approval and the run.
    # Policy is applied to both spellings so a rule written against either one holds.
    requested = command
    command = [os.path.realpath(command[0])] + command[1:]
    policy_result = evaluate_command(requested)
    if policy_result.get("allowed", False) and command != requested:
        policy_result = evaluate_command(command)
    if not policy_result.get("allowed", False):
        append_audit(
            {
                "action": "policy_block",
                "argv": command,
                "reason": policy_result.get("reason"),
                "pattern": policy_result.get("pattern"),
            }
        )
        print("Command blocked by policy.", file=sys.stderr)
        return 3

    session_id = os.environ.get("OPENCLAW_TASK_SESSION_ID") or None
    if security_config.flag("OPENCLAW_REQUIRE_SESSION_ID", settings) and not session_id:
        append_audit({"action": "session_id_missing", "argv": command})
        print("Task session id is required but not provided.", file=sys.stderr)
        return 6

    argv_json = json.dumps(command)
    authorize_args = ["authorize", "--argv-json", argv_json]
    if session_id:
        authorize_args += ["--session-id", session_id]
    authz = run_guard(args, *authorize_args)
    if authz.returncode not in (0, 2):
        sys.stderr.write(authz.stderr or authz.stdout)
        return authz.returncode
    if "integrity" in (authz.stderr or "") or '"state_integrity": "reset"' in (authz.stdout or ""):
        append_audit({"action": "state_integrity_failed", "argv": command})
        sys.stderr.write(authz.stderr or "")

    needs_approval = authz.returncode == 2
    prompt_policy = load_policy()
    if prompt_policy.get("require_confirmation_for_untrusted") and os.environ.get("OPENCLAW_UNTRUSTED_SOURCE") == "1":
        confirmed = prompter.available() and prompter.ask(
            "Untrusted content source detected. Proceed? [y/N]: "
        ).strip().lower() in {"y", "yes"}
        if not confirmed:
            append_audit({"action": "untrusted_source_block", "argv": command})
            print("Untrusted content source was not confirmed at a terminal.", file=sys.stderr)
            return 5
        append_audit({"action": "untrusted_source_confirmed", "argv": command})

    if needs_approval:
        token_required = security_config.setting("OPENCLAW_APPROVAL_TOKEN", settings)
        approved, outcome = obtain_approval(prompter, args.reason, command, token_required)
        if outcome == "no_terminal":
            print(
                "Approval must be given at a terminal, and none is attached. Refusing privileged execution.",
                file=sys.stderr,
            )
            return EXIT_NO_TERMINAL
        if outcome == "token_failed":
            print("Invalid approval token.", file=sys.stderr)
            return 4
        if not approved:
            print("User denied elevated access. Running in normal mode is required.")
            run_guard(args, "normal-used")
            append_audit({"action": "approval_denied", "reason": args.reason, "argv": command})
            return 1

        approve_args = ["approve", "--reason", args.reason, "--argv-json", argv_json]
        if session_id:
            approve_args += ["--session-id", session_id]
        approve = run_guard(args, *approve_args)
        if approve.returncode != 0:
            sys.stderr.write(approve.stderr or approve.stdout)
            return approve.returncode
        append_audit({"action": "approval_granted", "reason": args.reason, "argv": command, "session_id": session_id})

    try:
        if args.use_sudo:
            run_guard(args, "elevated-used")
        return run_command(command, args.use_sudo)
    finally:
        if not args.keep_session:
            run_guard(args, "drop")
            append_audit({"action": "drop_elevation", "argv": command, "reason": "post-command"})


if __name__ == "__main__":
    raise SystemExit(main())

"""Run tests and benchmarks with explicit failures, checked evidence, and owned-artifact cleanup."""

from __future__ import annotations

import argparse
import codecs
from collections import defaultdict
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET

from detect_lang import (
    add_project_arguments,
    positive_int,
    print_report,
    require_python,
    scan_files,
    select_language,
)

# Run the version guard before loading platform-specific execution helpers.
require_python()
from process_control import spawn_process  # noqa: E402

OUTPUT_TAIL_BYTES = 262144
PARSE_LIMIT_BYTES = 32 * 1024 * 1024
SNAPSHOT_LIMIT = 20000
CHANGE_LIST_LIMIT = 50
FAILURE_STATES = {"failed", "error", "timed_out"}
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
RUST_SUMMARY = re.compile(
    r"^test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored;", re.M
)
RUST_TARGET = re.compile(
    r"^\s*(?:Running \S+(?: \S+)? \((?:.*[/\\])?([A-Za-z0-9_]+)-[0-9a-f]{16}(?:\.exe)?\)"
    r"|Doc-tests ([A-Za-z0-9_]+))\s*$",
    re.M,
)
UNITTEST_RAN = re.compile(r"^Ran (\d+) tests? in [\d.]+s", re.M)
UNITTEST_STATUS = re.compile(r"^(?:OK|FAILED)(?: \(([^)]*)\))?\s*$", re.M)
PYTEST_SUMMARY = re.compile(r"^(?:=+ )?(.+?) in [\d.]+s\b", re.M)
PYTEST_ITEM = re.compile(r"\d+ [a-z][a-z ]*")
PYTEST_WORDS = {
    "passed": "passed",
    "xfailed": "passed",
    "xpassed": "passed",
    "failed": "failed",
    "error": "failed",
    "errors": "failed",
    "skipped": "skipped",
}
TAP_SUMMARY = re.compile(
    r"^(?:#|ℹ)\s+(tests|pass|fail|cancelled|skipped|todo)\s+(\d+)\s*$", re.M
)
JEST_LINE = re.compile(r"^\s*Tests:?\s+(.*)$", re.M)
MOCHA_SUMMARY = re.compile(r"^\s*(\d+) (passing|failing|pending)\b", re.M)
GO_TEXT = re.compile(r"^\s*--- (PASS|FAIL|SKIP): ", re.M)
ENVIRONMENT_SIGNS = re.compile(
    r"ModuleNotFoundError|ImportError|No module named|cannot import name|"
    r"Cannot find module|ERR_MODULE_NOT_FOUND|command not found|"
    r"error\[E0463\]|can't find crate|no matching package named|"
    r"failed to (?:download|load source for)|module lookup disabled by GOPROXY=off|"
    r"cannot find package|missing go\.sum entry|"
    r"Could not resolve host|EADDRINUSE|ECONNREFUSED"
)
BUILD_SIGNS = re.compile(
    r"error\[E\d{4}\]|could not compile|error: linking with|undefined reference to|"
    r"ld: (?:library|symbol\(s\)) not found|\[build failed\]|\[setup failed\]|"
    r"SyntaxError|IndentationError|error TS\d{4}|CMake Error"
)
ASSERTION_SIGNS = re.compile(
    r"AssertionError|assert(?:ion)? failed|panicked at|--- FAIL|✕|^not ok \d|"
    r"Expected|expect\("
)


def command_argv(
    command: str, trusted_shell: bool = False, shell: str | None = None
) -> list[str]:
    """Keep legacy POSIX tokens distinct from explicitly authorized shell programs."""
    if trusted_shell:
        selected = shell or ("powershell" if os.name == "nt" else "bash")
        names = ("pwsh.exe", "powershell.exe") if os.name == "nt" else ("pwsh", "powershell")
        if selected == "powershell":
            executable = next((path for name in names if (path := shutil.which(name))), None)
            if executable is None:
                raise FileNotFoundError("PowerShell is unavailable; install it or use direct argv")
            args = [executable, "-NoProfile", "-NonInteractive", "-Command", command]
        else:
            executable = shutil.which("bash")
            if executable is None:
                raise FileNotFoundError("Bash is unavailable; use direct argv or PowerShell")
            args = [executable, "--noprofile", "--norc", "-o", "pipefail", "-c", command]
        if not command.strip():
            raise ValueError("command must not be empty")
    else:
        args = shlex.split(command)
    if not args or not args[0]:
        raise ValueError("command must not be empty")
    return args


def supplied_command(args: argparse.Namespace, prefix: str = "command") -> bool:
    """Distinguish omitted commands from empty, explicitly invalid command inputs."""
    text_name = "command" if prefix == "command" else f"{prefix}_cmd"
    argv_name = "command_argv" if prefix == "command" else f"{prefix}_argv"
    return any(getattr(args, name, None) is not None for name in (text_name, argv_name, f"{argv_name}_file"))


def input_command(args: argparse.Namespace, root: Path, prefix: str = "command") -> list[str]:
    """Load a command's string or lossless JSON argv without passing JSON through a shell."""
    text_name = "command" if prefix == "command" else f"{prefix}_cmd"
    argv_name = "command_argv" if prefix == "command" else f"{prefix}_argv"
    encoded = getattr(args, argv_name, None)
    filename = getattr(args, f"{argv_name}_file", None)
    trust_name = "trust_command" if prefix == "command" else f"trust_{prefix}_cmd"
    trusted = getattr(args, trust_name, False)
    if encoded is None and filename is None:
        return command_argv(getattr(args, text_name), trusted, getattr(args, "shell", None))
    if trusted:
        raise ValueError("trusted shell flags require a command string, not JSON argv")
    if filename is not None:
        path = Path(filename).expanduser()
        if not path.is_absolute():
            path = root / path
        encoded = path.read_text(encoding="utf-8-sig")
    values = json.loads(encoded)
    if not isinstance(values, list) or not values or not all(isinstance(value, str) for value in values):
        raise ValueError("command argv must be a nonempty JSON array of strings")
    if not values[0] or any("\0" in value for value in values):
        raise ValueError("command executable must not be empty and arguments must not contain NUL")
    return values


def executable_argv(argv: list[str], root: Path, env: dict) -> list[str]:
    """Resolve Windows executables and confine implicit batch execution to the npm adapter."""
    if os.name != "nt":
        return argv
    program = argv[0]
    candidate = Path(program)
    if not candidate.is_absolute():
        local = root / candidate
        found = shutil.which(str(local)) or shutil.which(program, path=env.get("PATH"))
    else:
        found = shutil.which(program)
    if found is None:
        raise FileNotFoundError(f"executable not found: {program}")
    if Path(found).suffix.lower() not in {".cmd", ".bat"}:
        return [found, *argv[1:]]
    if Path(found).name.lower() != "npm.cmd" or argv[1:] != ["test"]:
        raise ValueError("batch files need an explicit trusted PowerShell command; direct argv supports native programs")
    if any(character in found for character in '%!\r\n"'):
        raise ValueError("npm.cmd path cannot contain batch expansion characters; use an explicit shell command")
    system_root = env.get("SYSTEMROOT") or env.get("SystemRoot")
    command_processor = str(Path(system_root) / "System32" / "cmd.exe") if system_root else shutil.which("cmd.exe")
    if command_processor is None or not Path(command_processor).is_file():
        raise FileNotFoundError("npm.cmd requires the Windows command processor")
    return [command_processor, "/d", "/v:off", "/s", "/c", f'""{found}" test"']


def output_encoding(value: str) -> str:
    """Reject unknown log codecs before any project command can run."""
    try:
        codec = codecs.lookup(value)
        b"".decode(codec.name)
    except (LookupError, TypeError) as error:
        raise argparse.ArgumentTypeError(f"invalid text encoding: {value}") from error
    return codec.name


def decoded_output(data: bytes, encoding: str) -> tuple[str, bool]:
    """Keep decoding damage visible while retaining raw-byte hashes and comparisons."""
    try:
        return data.decode(encoding), False
    except UnicodeError:
        return data.decode(encoding, errors="backslashreplace"), True


def run_command(
    argv: list[str], root: Path, env: dict, timeout: int, summarize: bool = False,
    encoding: str = "utf-8",
) -> dict:
    """Run a command with a timeout, terminate its process group, and clean temporary output.

    The report keeps the last 256 KiB of combined output plus a digest of all of it. With
    summarize, test summaries are parsed from the complete output (up to 32 MiB), so early
    summary blocks are not lost to tail truncation.
    """
    started = time.perf_counter()
    result = {
        "command": argv,
        "exit_code": None,
        "timed_out": False,
        "timeout_seconds": timeout,
        "error": None,
        "output_encoding": encoding,
        "output_decode_error": False,
        "cleanup_error": None,
        "process_management": "windows-job" if os.name == "nt" else "posix-process-group",
    }
    with tempfile.TemporaryFile() as output:
        process = None
        try:
            argv = executable_argv(argv, root, env)
            result["command"] = argv
            # cmd.exe consumes /c as shell text, not as an MSVCRT-quoted argv
            # argument. Only executable_argv's fixed npm adapter reaches here.
            raw_command = None
            if (
                os.name == "nt" and len(argv) == 6
                and Path(argv[0]).name.lower() == "cmd.exe"
                and argv[1:5] == ["/d", "/v:off", "/s", "/c"]
            ):
                raw_command = subprocess.list2cmdline(argv[:-1]) + " " + argv[-1]
            process = spawn_process(argv, root, env, output, windows_command_line=raw_command)
            try:
                process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                result["timed_out"] = True
                process.stop(grace=0 if os.name == "nt" else 2)
            except KeyboardInterrupt:
                # Windows console children normally receive the same Ctrl+C;
                # give their own cleanup a bounded opportunity to finish.
                process.stop(grace=2 if os.name == "nt" else 0)
                raise
            except BaseException:
                process.stop(grace=0)
                raise
            result["exit_code"] = process.returncode
        except OSError as error:
            result["error"] = f"{type(error).__name__}: {error}"
        finally:
            if process is not None:
                try:
                    process.close()
                except OSError as error:
                    result["cleanup_error"] = f"{type(error).__name__}: {error}"
                    result["error"] = result["error"] or f"process cleanup failed: {error}"
        result["duration_seconds"] = time.perf_counter() - started
        size = output.tell()
        output.seek(0)
        digest = hashlib.sha256()
        for chunk in iter(lambda: output.read(1 << 20), b""):
            digest.update(chunk)
        result["output_sha256"] = digest.hexdigest()
        if summarize:
            result["output_parsed"] = size <= PARSE_LIMIT_BYTES
            output.seek(0)
            if result["output_parsed"]:
                text, damaged = decoded_output(output.read(), encoding)
                result["output_decode_error"] = damaged
                result["output_summary"] = None if damaged else summary_counts(text)
            else:
                result["output_summary"] = None
        output.seek(max(0, size - OUTPUT_TAIL_BYTES))
        result["output"], tail_damaged = decoded_output(output.read(), encoding)
        # A truncated multibyte sequence at the tail boundary is not evidence of
        # damage in the complete output already parsed above.
        if not summarize or not result.get("output_parsed"):
            result["output_decode_error"] = tail_damaged
        result["output_truncated"] = size > OUTPUT_TAIL_BYTES
    return result


def junit_counts(path: Path) -> dict:
    """Count JUnit testcase evidence and reject malformed or inconsistent summaries."""
    root = ET.parse(path).getroot()
    if root.tag.rsplit("}", 1)[-1] not in {"testsuite", "testsuites"}:
        raise ValueError("not a JUnit report")
    cases = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "testcase"]
    counts = {"total": len(cases), "executed": 0, "failed": 0, "skipped": 0}
    for case in cases:
        tags = {child.tag.rsplit("}", 1)[-1] for child in case}
        skipped = "skipped" in tags or case.attrib.get("status") in {
            "notrun",
            "disabled",
        }
        counts["skipped"] += int(skipped)
        counts["executed"] += int(not skipped)
        counts["failed"] += int(bool(tags & {"failure", "error"}))
    for suite in root.iter():
        if suite.tag.rsplit("}", 1)[-1] not in {"testsuite", "testsuites"}:
            continue
        local = [
            case for case in suite.iter() if case.tag.rsplit("}", 1)[-1] == "testcase"
        ]
        if "tests" in suite.attrib and int(suite.attrib["tests"]) != len(local):
            raise ValueError("JUnit suite count disagrees with testcase nodes")
        if counts["failed"] == 0 and any(
            int(suite.attrib.get(key, "0")) > 0 for key in ("failures", "errors")
        ):
            raise ValueError("JUnit declares failures without failure/error nodes")
    counts["formats"] = ["junit"]
    return counts


def rust_summary(output: str) -> tuple[int, int, int, int] | None:
    """Sum libtest result lines from every test binary, including doc-tests."""
    rows = RUST_SUMMARY.findall(output)
    if not rows:
        return None
    passed, failed, skipped = (sum(int(row[i]) for row in rows) for i in range(3))
    return passed, failed, skipped, len(rows)


def unittest_summary(output: str) -> tuple[int, int, int, int] | None:
    """Sum unittest runs, reading failures and skips only from their final status lines."""
    totals = [int(value) for value in UNITTEST_RAN.findall(output)]
    if not totals:
        return None
    counts: dict[str, int] = defaultdict(int)
    for detail in UNITTEST_STATUS.findall(output):
        for key, value in re.findall(r"([a-z ]+)=(\d+)", detail):
            counts[key.strip()] += int(value)
    failed = counts["failures"] + counts["errors"] + counts["unexpected successes"]
    skipped = counts["skipped"]
    return max(0, sum(totals) - failed - skipped), failed, skipped, len(totals)


def pytest_summary(output: str) -> tuple[int, int, int, int] | None:
    """Sum pytest terminal summaries such as '1 failed, 2 passed in 0.10s'."""
    counts: dict[str, int] = defaultdict(int)
    blocks = 0
    for part in PYTEST_SUMMARY.findall(output):
        items = [item.split(" ", 1) for item in part.split(", ")]
        if not all(PYTEST_ITEM.fullmatch(" ".join(item)) for item in items):
            continue
        if not any(word in PYTEST_WORDS for _, word in items):
            continue
        blocks += 1
        for number, word in items:
            if word in PYTEST_WORDS:
                counts[PYTEST_WORDS[word]] += int(number)
    if not blocks:
        return None
    return counts["passed"], counts["failed"], counts["skipped"], blocks


def tap_summary(output: str) -> tuple[int, int, int, int] | None:
    """Sum TAP and Node test-runner totals across every reported block."""
    counts: dict[str, int] = defaultdict(int)
    blocks = 0
    for key, value in TAP_SUMMARY.findall(output):
        counts[key] += int(value)
        blocks += key == "tests"
    if not blocks:
        return None
    failed = counts["fail"] + counts["cancelled"]
    skipped = counts["skipped"] + counts["todo"]
    return max(0, counts["tests"] - failed - skipped), failed, skipped, blocks


def jest_summary(output: str) -> tuple[int, int, int, int] | None:
    """Sum Jest and Vitest 'Tests' lines, so a failed run between passing runs stays visible."""
    totals = [0, 0, 0]
    blocks = 0
    patterns = (r"(\d+) passed", r"(\d+) failed", r"(\d+) (?:skipped|todo|pending)")
    for line in JEST_LINE.findall(output):
        values = [sum(map(int, re.findall(pattern, line))) for pattern in patterns]
        if any(values):
            totals = [old + new for old, new in zip(totals, values)]
            blocks += 1
    return (*totals, blocks) if blocks else None


def mocha_summary(output: str) -> tuple[int, int, int, int] | None:
    """Sum Mocha passing, failing and pending lines."""
    counts: dict[str, int] = defaultdict(int)
    blocks = 0
    for value, word in MOCHA_SUMMARY.findall(output):
        counts[word] += int(value)
        blocks += word == "passing"
    if not blocks:
        return None
    return counts["passing"], counts["failing"], counts["pending"], blocks


def go_summary(output: str) -> tuple[int, int, int, int] | None:
    """Count go test -json test events, falling back to verbose '--- PASS' lines."""
    counts: dict[str, int] = defaultdict(int)
    found = False
    for line in output.splitlines():
        if not (line.startswith("{") and '"Test"' in line):
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get("Test"):
            action = event.get("Action")
            if action in {"pass", "fail", "skip"}:
                counts[action] += 1
                found = True
    if not found:
        for verdict in GO_TEXT.findall(output):
            counts[verdict.lower()] += 1
            found = True
    return (counts["pass"], counts["fail"], counts["skip"], 1) if found else None


SUMMARY_PARSERS = (
    ("rust", rust_summary),
    ("unittest", unittest_summary),
    ("pytest", pytest_summary),
    ("tap", tap_summary),
    ("jest", jest_summary),
    ("mocha", mocha_summary),
    ("go", go_summary),
)


def summary_counts(output: str) -> dict | None:
    """Sum every recognized test summary so one failing block cannot hide behind passing ones.

    Exit zero or generic success text is insufficient evidence; unrecognized output returns None.
    """
    output = ANSI.sub("", output)
    passed = failed = skipped = blocks = 0
    formats = []
    for name, parser in SUMMARY_PARSERS:
        found = parser(output)
        if found is None:
            continue
        passed, failed, skipped, blocks = (
            total + value for total, value in zip((passed, failed, skipped, blocks), found)
        )
        formats.append(name)
    if not formats:
        return None
    counts = {
        "total": passed + failed + skipped,
        "executed": passed + failed,
        "failed": failed,
        "skipped": skipped,
        "formats": formats,
        "summary_blocks": blocks,
    }
    if "rust" in formats:
        counts["rust_targets"] = sorted(
            {name for pair in RUST_TARGET.findall(output) for name in pair if name}
        )
    return counts


def cargo_workspace_flags(root: Path) -> list[str]:
    """Test every workspace member; a root package alone would hide failing members."""
    import tomllib  # Deferred so the interpreter version check runs first.

    try:
        with (root / "Cargo.toml").open("rb") as handle:
            data = tomllib.load(handle)
    except FileNotFoundError:
        return []
    return ["--workspace"] if isinstance(data.get("workspace"), dict) else []


def automatic_test_command(
    root: Path, lang: str, report: Path, temp: Path
) -> tuple[list[str], dict[str, str]] | None:
    """Select an existing runner without installing tools, configuring builds, or guessing scripts.

    Returns the argv and any environment overrides the adapter needs, or None.
    """
    if lang == "python" and importlib.util.find_spec("pytest"):
        return [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--junitxml",
            str(report),
            "--basetemp",
            str(temp / "pytest"),
            "-o",
            f"cache_dir={temp / 'pytest-cache'}",
        ], {}
    if lang == "rust" and (root / "Cargo.toml").is_file():
        return [
            "cargo",
            "test",
            "--locked",
            "--offline",
            "--no-fail-fast",
            *cargo_workspace_flags(root),
            "--target-dir",
            str(temp / "cargo-target"),
        ], {}
    if lang == "javascript" and (root / "package.json").is_file():
        scripts = json.loads((root / "package.json").read_bytes()).get("scripts", {})
        if scripts.get("test"):
            # Modern which() can also discover npm's extensionless Unix shim;
            # the Windows adapter deliberately selects the installed batch shim.
            return ["npm.cmd" if os.name == "nt" else "npm", "test"], {}
    if lang == "go" and (root / "go.mod").is_file():
        # Never download modules during a review run; a missing cache is reported instead.
        # -count=1 bypasses the test cache so the counts come from a fresh execution.
        return ["go", "test", "-count=1", "-json", "./..."], {"GOPROXY": "off"}
    if lang in {"c", "cpp"}:
        for name in ("build", "cmake-build-debug", "cmake-build-release", "out"):
            if (root / name / "CTestTestfile.cmake").is_file():
                return [
                    "ctest",
                    "--test-dir",
                    str(root / name),
                    "--output-on-failure",
                    "--no-tests=error",
                    "--output-junit",
                    str(report),
                ], {}
    return None


def assess_test_execution(
    execution: dict, report_path: Path, argv: list[str]
) -> tuple[dict, int]:
    """Assess execution and fresh reports so empty evidence or broken wrappers cannot pass."""
    result = {"status": "incomplete", "complete": False, "tests": None}
    if execution["error"] or execution["timed_out"]:
        result["status"] = "error" if execution["error"] else "timed_out"
        if execution["timed_out"]:
            result["reason"] = (
                f"command exceeded --timeout {execution['timeout_seconds']}s and its "
                + ("process cleanup failed; inspect execution.cleanup_error" if execution.get("cleanup_error")
                   else "owned processes were stopped; raise --timeout if the suite needs longer")
            )
        elif execution["error"]:
            result["reason"] = execution["error"]
        return result, 2
    has_junit = report_path.is_file()
    if not has_junit and execution.get("output_decode_error"):
        result["reason"] = (
            f"output could not be decoded as {execution['output_encoding']}; "
            "set --output-encoding or provide fresh JUnit via {report}"
        )
        return result, 2
    if not has_junit and not execution.get("output_parsed", False):
        result["reason"] = (
            f"output exceeded {PARSE_LIMIT_BYTES // (1024 * 1024)} MiB; "
            "complete test totals require fresh JUnit evidence via {report}"
        )
        return result, 2
    try:
        counts = (
            junit_counts(report_path)
            if has_junit
            else execution.get("output_summary")
        )
    except (ValueError, OSError, ET.ParseError) as error:
        result["reason"] = f"invalid test evidence: {error}"
        return result, 2
    result["tests"] = counts
    if counts is not None and counts["failed"] > 0:
        result.update(status="failed", complete=True)
        return result, 1
    no_tests = counts is not None and counts["executed"] == 0
    no_tests = no_tests or (
        not counts
        and bool(
            re.search(
                r"No tests were found|no tests ran|collected 0 items",
                execution["output"],
                re.I,
            )
        )
    )
    if no_tests:
        known_empty_exit = (
            execution["exit_code"] == 0
            or (execution["exit_code"] == 5 and "pytest" in argv)
            or (
                Path(argv[0]).name == "ctest"
                and execution["exit_code"] == 8
                and "No tests were found" in execution["output"]
            )
        )
        if not known_empty_exit:
            result.update(
                status="failed",
                reason="empty evidence does not waive this command failure",
            )
            return result, 1
        result.update(
            status="no_tests",
            reason="zero tests executed (all skipped also counts as zero)",
        )
        return result, 2
    if execution["exit_code"] != 0:
        result.update(status="failed", reason="test command failed; inspect output")
        return result, 1
    if counts is None:
        result["reason"] = (
            "exit 0 without recognized test count; provide fresh JUnit via {report}"
        )
        return result, 2
    result.update(status="passed", complete=True)
    return result, 0


def matching_lines(output: str, pattern: re.Pattern, limit: int = 3) -> list[str]:
    """Quote the first few output lines that match a signature as classification evidence."""
    found = []
    for line in output.splitlines():
        if pattern.search(line):
            found.append(line.strip()[:200])
            if len(found) == limit:
                break
    return found


def classify_failure(execution: dict, counts: dict | None) -> dict:
    """Separate environment and build failures from assertion failures by output signatures.

    The result is a triage hint with quoted evidence lines, not a root-cause verdict.
    """
    if execution.get("cleanup_error"):
        return {"failure_kind": "cleanup"}
    if execution["timed_out"]:
        return {"failure_kind": "timeout"}
    if execution["error"]:
        missing = execution["error"].startswith(("FileNotFoundError", "PermissionError"))
        return {"failure_kind": "tool_missing" if missing else "spawn_error"}
    output = ANSI.sub("", execution["output"])
    for kind, pattern in (("environment", ENVIRONMENT_SIGNS), ("build", BUILD_SIGNS)):
        evidence = matching_lines(output, pattern)
        if evidence:
            return {"failure_kind": kind, "failure_evidence": evidence}
    if counts and counts["failed"]:
        return {
            "failure_kind": "assertion",
            "failure_evidence": matching_lines(output, ASSERTION_SIGNS),
        }
    return {"failure_kind": "unknown"}


def environment_hint(root: Path, explicit_command: bool) -> str:
    """Suggest rerunning in the project's own environment when tools or modules are missing."""
    if not explicit_command:
        for name in (".venv", "venv"):
            relative = Path(name) / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            if (root / relative).is_file():
                command = json.dumps([str(relative), "-m", "pytest", "--junitxml", "{report}"])
                return (
                    "the adapter used the helper's interpreter; rerun with "
                    f"--command-argv {command} (or --command-argv-file) to use the project virtualenv"
                )
    return (
        "missing modules or tools usually mean the run used a different interpreter or "
        "toolchain than the project; rerun with --command in the project's environment"
    )


def workspace_snapshot(root: Path, exclude: Path | None = None) -> dict | None:
    """Record size and mtime of scanned project files, or None when the tree is too large."""
    files, warnings = scan_files(root, SNAPSHOT_LIMIT)
    if any(warning.startswith("file limit") for warning in warnings):
        return None
    # Resolve so a symlinked temp location (macOS /var -> /private/var) is still excluded.
    exclude = exclude.resolve() if exclude is not None else None
    snapshot = {}
    for path in files:
        if exclude is not None and path.is_relative_to(exclude):
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        snapshot[path.relative_to(root).as_posix()] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def record_workspace_changes(
    result: dict, root: Path, before: dict | None, exclude: Path | None = None
) -> None:
    """Attach project-tree changes made by executed commands so side effects stay visible.

    Directories excluded from scans by default (build/, target/, node_modules/ and others)
    are not tracked.
    """
    after = workspace_snapshot(root, exclude) if before is not None else None
    if before is None or after is None:
        result["warnings"].append(
            f"workspace mutation check skipped: more than {SNAPSHOT_LIMIT} files"
        )
        return
    created = sorted(after.keys() - before.keys())
    deleted = sorted(before.keys() - after.keys())
    modified = sorted(p for p in before.keys() & after.keys() if before[p] != after[p])
    total = len(created) + len(deleted) + len(modified)
    result["workspace_mutations"] = {
        "created": created[:CHANGE_LIST_LIMIT],
        "modified": modified[:CHANGE_LIST_LIMIT],
        "deleted": deleted[:CHANGE_LIST_LIMIT],
        "total": total,
    }
    if total:
        result["warnings"].append(
            f"commands changed {total} file(s) in the reviewed tree; see workspace_mutations"
        )


def correctness(args: argparse.Namespace, root: Path) -> tuple[dict, int]:
    """Coordinate test adapters, temporary artifacts, and scale observations with separate verdict logic."""
    lang = select_language(root, args.lang)
    result = {
        "kind": "correctness",
        "language": lang,
        "status": "incomplete",
        "complete": False,
        "tests": None,
        "scale_requested": args.scale,
        "scale_verified": False,
        "warnings": [],
    }
    with tempfile.TemporaryDirectory(prefix="codesift-test-") as directory:
        temp = Path(directory)
        report_path, metrics = temp / "junit.xml", temp / "metrics.json"
        env = dict(
            os.environ,
            PYTHONDONTWRITEBYTECODE="1",
            CI="true",
            CODESIFT_REPORT_PATH=str(report_path),
            CODESIFT_METRICS_PATH=str(metrics),
            PCR_METRICS_PATH=str(metrics),
            npm_config_cache=str(temp / "npm-cache"),
            npm_config_update_notifier="false",
        )
        if args.scale is not None:
            env["TEST_SCALE"] = str(args.scale)
        explicit = supplied_command(args)
        if explicit:
            argv = input_command(args, root)
            if getattr(args, "trust_command", False):
                if "{report}" in args.command or "{metrics}" in args.command:
                    raise ValueError(
                        "trusted shell commands use CODESIFT_REPORT_PATH and "
                        "CODESIFT_METRICS_PATH environment variables; brace placeholders are for direct argv"
                    )
            else:
                # Substitute after splitting so paths containing spaces stay one argument.
                argv = [
                    value.replace("{report}", str(report_path)).replace(
                        "{metrics}", str(metrics)
                    )
                    for value in argv
                ]
        else:
            adapter = automatic_test_command(root, lang, report_path, temp)
            if adapter is None:
                result["reason"] = (
                    "no supported existing runner; provide --command with fresh JUnit {report}"
                )
                return result, 2
            argv, overrides = adapter
            env.update(overrides)
            if overrides:
                result["adapter_env"] = overrides
        before = workspace_snapshot(root, temp)
        execution = run_command(
            argv, root, env, args.timeout, summarize=True,
            encoding=getattr(args, "output_encoding", "utf-8"),
        )
        result["execution"] = execution
        if execution["output_decode_error"]:
            result["warnings"].append("command output contains undecodable bytes; inspect --output-encoding")
        record_workspace_changes(result, root, before, temp)
        verdict, exit_code = assess_test_execution(execution, report_path, argv)
        result.update(verdict)
        if result["status"] in FAILURE_STATES:
            result.update(classify_failure(execution, result["tests"]))
            if result["failure_kind"] in {"environment", "tool_missing"}:
                result["hint"] = environment_hint(root, explicit)
        if result["status"] == "no_tests" and args.allow_no_tests:
            return result, 0
        if result["status"] == "passed" and args.scale is not None:
            try:
                data = json.loads(metrics.read_bytes())
                result["scale_verified"] = (
                    type(data.get("observed_scale")) is int
                    and data["observed_scale"] == args.scale
                )
            except (OSError, ValueError, AttributeError):
                result["scale_verified"] = False
            if not result["scale_verified"]:
                result.update(
                    status="incomplete",
                    complete=False,
                    reason="tests passed but harness did not report matching observed_scale via CODESIFT_METRICS_PATH",
                )
                return result, 2
        return result, exit_code


def run_samples(
    result: dict, commands: dict, root: Path, env: dict, args: argparse.Namespace
) -> int | None:
    """Alternate project and baseline runs; return an exit code at the first unsuccessful run."""
    for index in range(args.warmup + args.runs):
        order = ("project", "baseline") if index % 2 == 0 else ("baseline", "project")
        destination = (
            result["warmup_results"] if index < args.warmup else result["samples"]
        )
        for name in order:
            execution = run_command(
                commands[name], root, env, args.timeout,
                encoding=getattr(args, "output_encoding", "utf-8"),
            )
            execution["side"] = name
            destination.append(execution)
            if execution["output_decode_error"] and not result["warnings"]:
                result["warnings"].append("command output contains undecodable bytes; byte comparisons remain unchanged")
            if execution["error"] or execution["timed_out"] or execution["exit_code"] != 0:
                result["status"] = (
                    "error" if execution["error"] else ("timed_out" if execution["timed_out"] else "failed")
                )
                result["reason"] = (
                    f"{name} command exceeded --timeout {args.timeout}s"
                    if execution["timed_out"]
                    else f"{name} command did not complete successfully"
                )
                return 1 if result["status"] == "failed" else 2
    return None


def compare_outputs(result: dict) -> bool:
    """Require every project and baseline run to print byte-identical combined output."""
    runs = result["warmup_results"] + result["samples"]
    digests = {
        side: sorted({run["output_sha256"] for run in runs if run["side"] == side})
        for side in ("project", "baseline")
    }
    equal = len(digests["project"]) == 1 and digests["project"] == digests["baseline"]
    result["output_comparison"] = {
        "equal": equal,
        "project_sha256": digests["project"],
        "baseline_sha256": digests["baseline"],
        "scope": "combined stdout/stderr bytes of every run",
    }
    return equal


def summarize_samples(result: dict) -> None:
    """Report medians, MAD, ranges and whether the two sides' sample ranges overlap."""
    result["summary"] = {}
    for name in ("project", "baseline"):
        values = [
            sample["duration_seconds"]
            for sample in result["samples"]
            if sample["side"] == name
        ]
        median = statistics.median(values)
        result["summary"][name] = {
            "median_seconds": median,
            "mad_seconds": statistics.median(abs(value - median) for value in values),
            "min_seconds": min(values),
            "max_seconds": max(values),
            "samples_seconds": values,
        }
    project, baseline = result["summary"]["project"], result["summary"]["baseline"]
    result["ratio_project_over_baseline"] = (
        project["median_seconds"] / baseline["median_seconds"]
        if baseline["median_seconds"] > 0
        else None
    )
    overlap = (
        project["min_seconds"] <= baseline["max_seconds"]
        and baseline["min_seconds"] <= project["max_seconds"]
    )
    result["spread"] = {
        "ranges_overlap": overlap,
        "verdict": "inconclusive" if overlap else "separated",
        "interpretation": (
            "sample ranges overlap; the difference may be run-to-run noise"
            if overlap
            else "sample ranges do not overlap in these runs; workload, output and "
            "environment comparability still need review"
        ),
    }


def benchmark(args: argparse.Namespace, root: Path) -> tuple[dict, int]:
    """Alternate two explicit commands and stop on any failed warmup or measured run."""
    result = {
        "kind": "benchmark",
        "status": "incomplete",
        "complete": False,
        "language": select_language(root, args.lang),
        "measurement": "whole-command wall time",
        "workload": args.workload,
        "comparability": "must be checked against workload, output and environment by reviewer",
        "runs": args.runs,
        "warmup": args.warmup,
        "samples": [],
        "warmup_results": [],
        "warnings": [],
    }
    if not supplied_command(args, "project") or not supplied_command(args, "baseline"):
        result["reason"] = "both project and baseline commands are required (--project-cmd/--baseline-cmd or JSON argv)"
        return result, 2
    commands = {
        "project": input_command(args, root, "project"),
        "baseline": input_command(args, root, "baseline"),
    }
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", CI="true")
    before = workspace_snapshot(root)
    failure = run_samples(result, commands, root, env, args)
    record_workspace_changes(result, root, before)
    if failure is not None:
        return result, failure
    if args.compare_output and not compare_outputs(result):
        result.update(
            status="output_mismatch",
            reason="outputs differ between sides or runs; timings do not compare the same work",
        )
        return result, 1
    summarize_samples(result)
    result.update(status="measured", complete=True)
    return result, 0


def nonnegative_int(value: str) -> int:
    """Allow zero warmups while rejecting negative counts that would skip execution."""
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be non-negative")
    return number


def stop_on_signal(signum: int, frame: object) -> None:
    """Turn termination signals into SystemExit so child groups and temporary files are cleaned."""
    raise SystemExit(128 + signum)


def main() -> int:
    """Provide a consistent CLI and emit one report with explicit completion and failure states."""
    require_python()
    for name in ("SIGTERM", "SIGHUP", "SIGBREAK"):
        number = getattr(signal, name, None)
        if number is not None:
            signal.signal(number, stop_on_signal)
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)
    test = subparsers.add_parser("correctness")
    bench = subparsers.add_parser("benchmark")
    for command, timeout in ((test, 300), (bench, 120)):
        add_project_arguments(command)
        command.add_argument("--json", action="store_true")
        command.add_argument("--shell", choices=("bash", "powershell"), help="shell for explicitly trusted command strings")
        command.add_argument("--output-encoding", type=output_encoding, default="utf-8", help="child log encoding (default utf-8); raw hashes and comparisons stay byte-based")
        command.add_argument(
            "--timeout",
            type=positive_int,
            default=timeout,
            help=f"seconds per command run (default {timeout})",
        )
    test_input = test.add_mutually_exclusive_group()
    test_input.add_argument(
        "--command",
        help="POSIX-token argv string on every platform; {report}/{metrics} expand after splitting",
    )
    test_input.add_argument("--command-argv", help="nonempty JSON array of program and string arguments")
    test_input.add_argument("--command-argv-file", type=Path, help="UTF-8/BOM JSON argv file; relative to --root")
    test.add_argument("--trust-command", action="store_true", help="explicitly authorize shell syntax in --command")
    test.add_argument("--scale", type=positive_int)
    test.add_argument("--allow-no-tests", action="store_true")
    for side in ("project", "baseline"):
        arguments = bench.add_mutually_exclusive_group()
        arguments.add_argument(f"--{side}-cmd", help="POSIX-token argv string on every platform")
        arguments.add_argument(f"--{side}-argv", help="nonempty JSON array of program and string arguments")
        arguments.add_argument(f"--{side}-argv-file", type=Path, help="UTF-8/BOM JSON argv file; relative to --root")
    bench.add_argument("--trust-project-cmd", action="store_true")
    bench.add_argument("--trust-baseline-cmd", action="store_true")
    bench.add_argument("--runs", type=positive_int, default=5)
    bench.add_argument("--warmup", type=nonnegative_int, default=1)
    bench.add_argument(
        "--compare-output",
        action="store_true",
        help="require byte-identical output from every project and baseline run",
    )
    bench.add_argument(
        "--workload", default="unspecified; comparability not established"
    )
    args = parser.parse_args()
    trusted = args.trust_command if args.mode == "correctness" else (args.trust_project_cmd or args.trust_baseline_cmd)
    if args.shell and not trusted:
        parser.error("--shell requires an explicit --trust-command or benchmark trust flag")
    if args.mode == "correctness" and args.trust_command and args.command is None:
        parser.error("--trust-command requires --command")
    if args.mode == "benchmark":
        for side in ("project", "baseline"):
            if getattr(args, f"trust_{side}_cmd") and getattr(args, f"{side}_cmd") is None:
                parser.error(f"--trust-{side}-cmd requires --{side}-cmd")
    root = args.root.resolve()
    if not root.is_dir():
        parser.error("--root must be an existing directory")
    try:
        report, exit_code = (
            correctness(args, root)
            if args.mode == "correctness"
            else benchmark(args, root)
        )
    except (ValueError, OSError) as error:
        report, exit_code = (
            {"status": "error", "complete": False, "reason": str(error)},
            2,
        )
    except KeyboardInterrupt:
        report, exit_code = {"status": "cancelled", "complete": False, "reason": "interrupted by Ctrl+C; owned process cleanup was requested"}, 130
    print_report(report, args.json)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

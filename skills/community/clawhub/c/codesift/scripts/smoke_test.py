#!/usr/bin/env python3
"""Run offline semantic regressions with automatically cleaned temporary fixtures."""

import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import urllib.error

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from detect_lang import python_version_error, require_python  # noqa: E402

# Check the interpreter before importing modules that need Python 3.11+ (tomllib).
require_python()

import check_runner  # noqa: E402
from dependencies import load_manifest, read_dependencies  # noqa: E402
import detect_lang as language_tools  # noqa: E402
from detect_lang import detect_lang  # noqa: E402
import verify_packages  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
WINDOWS = os.name == "nt"
ENTRY_POINTS = {
    "collect_facts.sh": ("lib/source_checks.py", "facts"),
    "detect_duplicates.sh": ("lib/source_checks.py", "duplicates"),
    "run_correctness_test.sh": ("lib/check_runner.py", "correctness"),
    "run_benchmark_comparison.sh": ("lib/check_runner.py", "benchmark"),
}

HARNESS = '''"""Produce controlled test reports without accessing the network."""
import json
import os
from pathlib import Path
import sys

mode = sys.argv[1]
if mode == "exit":
    sys.exit(int(sys.argv[2]))
if mode == "output":
    sys.stdout.write(sys.argv[2])
    sys.exit(0)
if mode == "argv":
    print(json.dumps(sys.argv[2:], ensure_ascii=True))
    sys.exit(0)
report = Path(sys.argv[2])
cases = {
    "pass": '<testsuite tests="1"><testcase name="one"/></testsuite>',
    "failure": '<testsuite tests="1"><testcase name="one"><failure message="wrong"/></testcase></testsuite>',
    "false_success": '<testsuite tests="1"><testcase name="one"><failure/></testcase></testsuite>',
    "empty": '<testsuite tests="0"/>',
    "skip": '<testsuite tests="1"><testcase name="one"><skipped/></testcase></testsuite>',
    "mismatch": '<testsuite tests="2"><testcase name="one"/></testsuite>',
    "invalid": '<broken',
    "empty_error": '<testsuite tests="0"/>',
    "hidden_error": '<testsuite tests="1" errors="1"><testcase name="one"/></testsuite>',
}
report.write_text(cases.get(mode, cases["pass"]), encoding="utf-8")
if mode in {"scale", "wrong_scale", "boolean_scale", "legacy_scale"}:
    scale = int(os.environ["TEST_SCALE"])
    exact = mode in {"scale", "legacy_scale"}
    observed = scale if exact else (True if mode == "boolean_scale" else scale + 1)
    variable = "PCR_METRICS_PATH" if mode == "legacy_scale" else "CODESIFT_METRICS_PATH"
    Path(os.environ[variable]).write_text(json.dumps({"observed_scale": observed}), encoding="utf-8")
if mode == "side_effect":
    Path("side_effect.txt").write_text("changed", encoding="utf-8")
sys.exit(3 if mode == "empty_error" else (1 if mode == "failure" else 0))
'''

PROCESS_TREE = '''"""Record a live three-generation process tree for ownership regressions."""
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

role, directory, behavior = sys.argv[1:4]
directory = Path(directory)
directory.mkdir(parents=True, exist_ok=True)
if behavior == "ignore-console" and os.name == "nt":
    signal.signal(signal.SIGINT, signal.SIG_IGN)
handshake = directory / (role + ".tmp")
handshake.write_text(str(os.getpid()), encoding="ascii")
handshake.replace(directory / role)
if role != "grandchild":
    next_role = "child" if role == "root" else "grandchild"
    subprocess.Popen([sys.executable, __file__, next_role, str(directory), behavior])
if role == "root" and behavior == "root-exit":
    deadline = time.monotonic() + 10
    while not (directory / "grandchild").is_file():
        if time.monotonic() > deadline:
            raise RuntimeError("grandchild did not start")
        time.sleep(0.02)
    print("Tests: 1 passed, 1 total", flush=True)
    sys.exit(0)
time.sleep(60)
'''


def process_is_running(pid):
    """Check liveness without sending Windows console events or counting POSIX zombies."""
    if WINDOWS:
        import ctypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.OpenProcess.argtypes = (ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong)
        kernel32.OpenProcess.restype = ctypes.c_void_p
        kernel32.WaitForSingleObject.argtypes = (ctypes.c_void_p, ctypes.c_ulong)
        kernel32.WaitForSingleObject.restype = ctypes.c_ulong
        kernel32.CloseHandle.argtypes = (ctypes.c_void_p,)
        kernel32.CloseHandle.restype = ctypes.c_int
        handle = kernel32.OpenProcess(0x00100000, False, pid)
        if not handle:
            error = ctypes.get_last_error()
            if error == 87:
                return False
            raise OSError(error, f"OpenProcess failed for test-owned PID {pid}")
        try:
            result = kernel32.WaitForSingleObject(handle, 0)
            if result not in (0, 258):
                raise OSError(ctypes.get_last_error(), "WaitForSingleObject failed")
            return result == 258
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    status = subprocess.run(
        ["ps", "-p", str(pid), "-o", "stat="],
        capture_output=True, text=True, encoding="ascii", check=False,
    )
    return bool(status.stdout.strip()) and not status.stdout.lstrip().startswith("Z")


def terminate_test_process(pid):
    """Unconditionally clean a recorded test-owned process after a failed assertion."""
    if not process_is_running(pid):
        return
    if WINDOWS:
        import ctypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.OpenProcess.argtypes = (ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong)
        kernel32.OpenProcess.restype = ctypes.c_void_p
        kernel32.TerminateProcess.argtypes = (ctypes.c_void_p, ctypes.c_uint)
        kernel32.WaitForSingleObject.argtypes = (ctypes.c_void_p, ctypes.c_ulong)
        kernel32.CloseHandle.argtypes = (ctypes.c_void_p,)
        handle = kernel32.OpenProcess(0x00100001, False, pid)
        if not handle:
            if ctypes.get_last_error() == 87:
                return
            raise OSError(ctypes.get_last_error(), "Could not clean a test-owned process")
        try:
            kernel32.TerminateProcess(handle, 1)
            kernel32.WaitForSingleObject(handle, 5000)
        finally:
            kernel32.CloseHandle(handle)
    else:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


class FakeResponse:
    """Stand in for an HTTP response context manager in offline registry tests."""

    def __init__(self, status):
        """Remember the HTTP status the fake registry returns."""
        self.status = status

    def __enter__(self):
        """Return the response itself, like urllib's context manager."""
        return self

    def __exit__(self, *exc):
        """Propagate exceptions raised inside the with-block."""
        return False


class HelperRegressionTests(unittest.TestCase):
    """Check observable outcomes and failure causes rather than accepting arbitrary nonzero exits."""

    def setUp(self):
        """Create an isolated directory for each test and register unconditional cleanup."""
        self.temporary = tempfile.TemporaryDirectory(prefix="codesift regression ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "tmp").mkdir()
        self.env = dict(
            os.environ,
            PYTHONDONTWRITEBYTECODE="1",
            PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
            TMPDIR=str(self.root / "tmp"),
            TEMP=str(self.root / "tmp"),
            TMP=str(self.root / "tmp"),
            CARGO_NET_OFFLINE="true",
            CARGO_HOME=str(self.root / "cargo-home"),
            npm_config_cache=str(self.root / "npm-cache"),
        )
        self.harness = self.write("case.py", HARNESS)

    def write(self, relative, text):
        """Create required fixtures only inside the directory owned by this test."""
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def helper_argv(self, script, *arguments):
        """Select the portable Python entry point independently of optional shell wrappers."""
        path, *mode = ENTRY_POINTS.get(script, (script,))
        return [
            sys.executable,
            str(SCRIPTS / path),
            *mode,
            "--root",
            str(self.root),
            *arguments,
        ]

    def invoke(self, script, *arguments):
        """Run a public helper from the fixture project and parse its JSON report."""
        process = self.run_plain(script, *arguments)
        try:
            report = json.loads(process.stdout)
        except ValueError:
            self.fail(
                f"expected JSON, got rc={process.returncode}: {process.stdout}\n{process.stderr}"
            )
        return process.returncode, report

    def verify(self, inventory, **options):
        """Verify registry names with isolated user configuration and no system pip files."""
        options.setdefault("environ", {})
        options.setdefault("home", self.root / "home")
        with patch.object(verify_packages, "SYSTEM_PIP_CONFIGS", ()), patch.object(
            verify_packages, "pip_site_prefix", return_value=self.root / "prefix"
        ):
            return verify_packages.verify_inventory(inventory, self.root, **options)

    def run_plain(self, script, *arguments, env=None):
        """Run a public helper and return the raw process result for non-JSON checks."""
        command = self.helper_argv(script, *arguments)
        with subprocess.Popen(
            command, env=env or self.env, cwd=self.root,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8",
        ) as process:
            try:
                stdout, stderr = process.communicate(timeout=360)
            except BaseException:
                if process.poll() is None:
                    # POSIX helpers handle SIGTERM; a Windows owner kill closes its Job handle.
                    process.kill() if WINDOWS else process.terminate()
                try:
                    process.communicate(timeout=15)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.communicate(timeout=10)
                raise
            return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)

    def command_for_case(self, mode):
        """Build a direct command while preserving spaces in fixture paths."""
        return [sys.executable, str(self.harness), mode, "{report}"]

    def harness_command(self, mode, *arguments):
        """Construct controlled child argv without requiring POSIX command-line parsing."""
        return [sys.executable, str(self.harness), mode, *arguments]

    def python_command(self, source):
        """Run inline fixture Python through the exact interpreter running this suite."""
        return [sys.executable, "-c", source]

    def tree_command(self, behavior="wait", name="pids"):
        """Prepare a process tree and register its fallback cleanup before it is started."""
        script = self.write("process_tree.py", PROCESS_TREE)
        directory = self.root / name
        self.addCleanup(self.cleanup_tree, directory)
        return [sys.executable, str(script), "root", str(directory), behavior], directory

    def recorded_pids(self, directory):
        """Read each process's independent handshake file without racing shared JSON writes."""
        return {
            role: int((directory / role).read_text(encoding="ascii"))
            for role in ("root", "child", "grandchild")
            if (directory / role).is_file()
        }

    def cleanup_tree(self, directory):
        """Remove any surviving fixture process even when the behavior under test fails."""
        deadline = time.monotonic() + 1
        while True:
            pids = self.recorded_pids(directory)
            for pid in pids.values():
                terminate_test_process(pid)
            if len(pids) == 3 or time.monotonic() >= deadline:
                return
            time.sleep(0.05)

    def wait_for_tree(self, directory, timeout=15):
        """Wait for all three generations to be alive before testing cancellation."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            pids = self.recorded_pids(directory)
            if len(pids) == 3 and all(process_is_running(pid) for pid in pids.values()):
                return pids
            time.sleep(0.05)
        self.fail(f"process tree did not become ready: {self.recorded_pids(directory)}")

    def assert_tree_stopped(self, directory, timeout=10):
        """Confirm that root, child and grandchild all stopped instead of checking only the root."""
        pids = self.recorded_pids(directory)
        self.assertEqual(set(pids), {"root", "child", "grandchild"})
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            live = {role: pid for role, pid in pids.items() if process_is_running(pid)}
            if not live:
                return
            time.sleep(0.05)
        self.fail(f"test-owned descendants survived cleanup: {live}")

    def cleanup_helper(self, process):
        """Stop a still-running helper before unconditional fixture-directory cleanup."""
        if process.poll() is None:
            process.kill()
        process.wait(timeout=10)

    def correctness(self, mode, *extra):
        """Run a fixture that produces a fresh JUnit report."""
        return self.invoke(
            "run_correctness_test.sh",
            "--command-argv",
            json.dumps(self.command_for_case(mode)),
            "--json",
            *extra,
        )

    def bench(self, project=None, baseline=None, *extra):
        """Exercise both benchmark commands and their failure states using real processes."""
        return self.invoke(
            "run_benchmark_comparison.sh",
            "--project-argv",
            json.dumps(project if project is not None else self.harness_command("exit", "0")),
            "--baseline-argv",
            json.dumps(baseline if baseline is not None else self.harness_command("exit", "0")),
            "--runs",
            "2",
            "--warmup",
            "0",
            "--json",
            *extra,
        )

    def test_benchmark_failed_baseline_is_failure(self):
        """A failed baseline must remain a failure regardless of successful project samples."""
        code, report = self.bench(None, self.harness_command("exit", "1"))
        self.assertEqual(
            (code, report["status"], report["complete"]), (1, "failed", False)
        )
        self.assertEqual(report["samples"][-1]["exit_code"], 1)

    def test_benchmark_requires_both_sides(self):
        """A baseline alone cannot produce a completed comparison."""
        code, report = self.invoke(
            "run_benchmark_comparison.sh", "--baseline-argv",
            json.dumps(self.harness_command("exit", "0")), "--json"
        )
        self.assertEqual((code, report["status"]), (2, "incomplete"))

    def test_benchmark_failed_project_is_failure(self):
        """A failed project command must stop the comparison."""
        code, report = self.bench(self.harness_command("exit", "1"))
        self.assertEqual((code, report["status"]), (1, "failed"))

    def test_plain_command_is_valid(self):
        """An ordinary portable command must run repeatedly and produce completed samples."""
        command = self.harness_command("output", "normal")
        code, report = self.bench(command, command)
        self.assertEqual(
            (code, report["status"], report["complete"]), (0, "measured", True)
        )
        self.assertEqual(len(report["summary"]["project"]["samples_seconds"]), 2)

    def test_metacharacters_are_literal_without_shell(self):
        """Direct argv execution must not interpret command separators inside arguments."""
        code, report = self.bench(self.harness_command("output", "; touch injected"))
        self.assertEqual(code, 0)
        self.assertFalse((self.root / "injected").exists())
        self.assertEqual(report["samples"][0]["output"], "; touch injected")

    @unittest.skipIf(WINDOWS, "Bash pipefail is a POSIX shell contract")
    def test_trusted_shell_propagates_pipeline_failure(self):
        """Trusted shell execution must preserve failures within a pipeline."""
        code, report = self.invoke(
            "run_benchmark_comparison.sh", "--project-cmd", "false | cat",
            "--trust-project-cmd", "--shell", "bash", "--baseline-argv",
            json.dumps(self.harness_command("exit", "0")), "--runs", "1", "--json",
        )
        self.assertEqual((code, report["status"]), (1, "failed"))

    def test_benchmark_warmup_failure_is_not_ignored(self):
        """A failed warmup must prevent measurement from starting."""
        code, report = self.bench(self.harness_command("exit", "1"), None, "--warmup", "1")
        self.assertEqual((code, report["status"]), (1, "failed"))
        self.assertEqual(report["samples"], [])

    def test_benchmark_timeout_stops_children(self):
        """A benchmark timeout must terminate every recorded generation of its command."""
        command, directory = self.tree_command()
        code, report = self.bench(command, None, "--timeout", "3")
        self.assertEqual((code, report["status"]), (2, "timed_out"))
        self.assert_tree_stopped(directory)

    def test_parent_exit_still_cleans_descendants(self):
        """A successful parent exit must not let its sleeping descendants escape ownership."""
        command, directory = self.tree_command("root-exit")
        code, report = self.invoke(
            "run_correctness_test.sh", "--command-argv", json.dumps(command), "--json"
        )
        self.assertEqual((code, report["status"]), (0, "passed"))
        self.assert_tree_stopped(directory)

    def test_real_junit_pass_and_cleanup(self):
        """An executed passing case must pass and leave no temporary report behind."""
        code, report = self.correctness("pass")
        self.assertEqual(
            (code, report["status"], report["tests"]["executed"]), (0, "passed", 1)
        )
        self.assertFalse(Path(report["execution"]["command"][-1]).exists())
        self.assertEqual(list((self.root / "tmp").iterdir()), [])
        self.assertEqual(report["workspace_mutations"]["total"], 0)

    def test_junit_failure_and_cleanup(self):
        """A failed test must remain failed while its temporary artifacts are cleaned."""
        code, report = self.correctness("failure")
        self.assertEqual(
            (code, report["status"], report["tests"]["failed"]), (1, "failed", 1)
        )
        self.assertEqual(list((self.root / "tmp").iterdir()), [])

    def test_junit_failure_overrides_exit_zero(self):
        """A failing JUnit report must override a misleading zero exit code."""
        code, report = self.correctness("false_success")
        self.assertEqual((code, report["status"]), (1, "failed"))

    def test_empty_junit_is_no_tests(self):
        """An empty test report must not count as executed test evidence."""
        code, report = self.correctness("empty")
        self.assertEqual(
            (code, report["status"], report["complete"]), (2, "no_tests", False)
        )

    def test_all_skipped_is_no_tests(self):
        """An entirely skipped suite must not count as executed tests."""
        code, report = self.correctness("skip")
        self.assertEqual(
            (code, report["status"], report["tests"]["executed"]), (2, "no_tests", 0)
        )

    def test_allow_no_tests_does_not_claim_pass(self):
        """Allowing no tests may change the exit code but not the evidence state."""
        code, report = self.correctness("empty", "--allow-no-tests")
        self.assertEqual(
            (code, report["status"], report["complete"]), (0, "no_tests", False)
        )

    def test_allow_no_tests_does_not_hide_missing_tool(self):
        """Allowing no tests must not suppress a missing-tool error."""
        code, report = self.invoke(
            "run_correctness_test.sh",
            "--command-argv",
            json.dumps([str(self.root / "missing-tool")]),
            "--allow-no-tests",
            "--json",
        )
        self.assertEqual((code, report["status"]), (2, "error"))

    def test_missing_adapter_is_not_an_allowed_empty_suite(self):
        """A missing adapter remains incomplete rather than an approved empty suite."""
        code, report = self.invoke(
            "run_correctness_test.sh", "--lang", "c", "--allow-no-tests", "--json"
        )
        self.assertEqual(
            (code, report["status"], report["complete"]), (2, "incomplete", False)
        )

    def test_empty_report_does_not_waive_other_errors(self):
        """An empty report must not let allow-no-tests suppress unrelated command failures."""
        code, report = self.correctness("empty_error", "--allow-no-tests")
        self.assertEqual((code, report["status"]), (1, "failed"))

    def test_summary_error_cannot_hide_behind_passing_cases(self):
        """Inconsistent error summaries and testcase evidence must not pass."""
        code, report = self.correctness("hidden_error")
        self.assertEqual((code, report["status"]), (2, "incomplete"))

    def test_truncated_tail_still_counts_full_output(self):
        """Summaries are parsed from the full output even when the report keeps only its tail."""
        code_text = "print('Tests: 1 passed, 1 total'); print('x'*300000)"
        command = self.python_command(code_text)
        code, report = self.invoke(
            "run_correctness_test.sh", "--command-argv", json.dumps(command), "--json"
        )
        self.assertEqual((code, report["status"]), (0, "passed"))
        self.assertTrue(report["execution"]["output_truncated"])
        self.assertTrue(report["execution"]["output_parsed"])

    def test_oversized_text_requires_complete_report(self):
        """Output beyond the parse limit must not establish complete test totals."""
        code_text = "import sys; sys.stdout.write('x'*(33*1024*1024)); print('Tests: 1 passed, 1 total')"
        command = self.python_command(code_text)
        code, report = self.invoke(
            "run_correctness_test.sh", "--command-argv", json.dumps(command), "--json"
        )
        self.assertEqual((code, report["status"]), (2, "incomplete"))
        self.assertIn("MiB", report["reason"])

    def test_exit_zero_without_test_evidence_is_incomplete(self):
        """A successful no-op command must not count as test evidence."""
        code, report = self.invoke(
            "run_correctness_test.sh", "--command-argv",
            json.dumps(self.harness_command("exit", "0")), "--json"
        )
        self.assertEqual((code, report["status"]), (2, "incomplete"))

    def test_invalid_junit_is_incomplete(self):
        """Malformed XML must not be interpreted as zero failures."""
        code, report = self.correctness("invalid")
        self.assertEqual((code, report["status"]), (2, "incomplete"))

    def test_inconsistent_junit_is_incomplete(self):
        """Reject reports whose declared totals disagree with testcase evidence."""
        code, report = self.correctness("mismatch")
        self.assertEqual((code, report["status"]), (2, "incomplete"))

    def test_scale_requires_observation(self):
        """Exporting a scale variable must not establish that the requested workload ran."""
        code, report = self.correctness("pass", "--scale", "17")
        self.assertEqual(
            (code, report["status"], report["scale_verified"]), (2, "incomplete", False)
        )

    def test_matching_scale_observation_passes(self):
        """A matching scale observation must complete the requested scale check."""
        code, report = self.correctness("scale", "--scale", "17")
        self.assertEqual(
            (code, report["status"], report["scale_verified"]), (0, "passed", True)
        )

    def test_wrong_or_boolean_scale_is_rejected(self):
        """Reject incorrect scales and booleans that compare equal to integer values."""
        for mode in ("wrong_scale", "boolean_scale"):
            with self.subTest(mode=mode):
                code, report = self.correctness(mode, "--scale", "1")
                self.assertEqual((code, report["status"]), (2, "incomplete"))

    @unittest.skipUnless(importlib.util.find_spec("pytest"), "pytest unavailable")
    def test_real_pytest_empty_suite(self):
        """Distinguish an empty real pytest suite from an ordinary test failure."""
        code, report = self.invoke(
            "run_correctness_test.sh", "--lang", "python", "--json"
        )
        self.assertEqual((code, report["status"]), (2, "no_tests"))

    @unittest.skipUnless(importlib.util.find_spec("pytest"), "pytest unavailable")
    def test_real_pytest_passes_one_case(self):
        """Verify report handling and executed-case counts with real pytest."""
        self.write(
            "test_example.py",
            'def test_sum():\n    """Verify a simple observable behavior."""\n    assert sum([1, 2]) == 3\n',
        )
        code, report = self.invoke(
            "run_correctness_test.sh", "--lang", "python", "--json"
        )
        self.assertEqual(
            (code, report["status"], report["tests"]["executed"]), (0, "passed", 1)
        )

    @unittest.skipUnless(shutil.which("ctest"), "ctest unavailable")
    def test_real_ctest_empty_suite(self):
        """An existing CTest configuration with no cases must not pass."""
        self.write("build/CTestTestfile.cmake", "# No tests intentionally.\n")
        code, report = self.invoke("run_correctness_test.sh", "--lang", "c", "--json")
        self.assertEqual((code, report["status"]), (2, "no_tests"))

    @unittest.skipUnless(shutil.which("ctest"), "ctest unavailable")
    def test_real_ctest_passes_one_case(self):
        """One real CTest case must produce usable JUnit evidence."""
        self.write(
            "build/CTestTestfile.cmake",
            f'add_test(one "{Path(sys.executable).as_posix()}" "-c" "assert sum([1,2]) == 3")\n',
        )
        code, report = self.invoke("run_correctness_test.sh", "--lang", "c", "--json")
        self.assertEqual(
            (code, report["status"], report["tests"]["executed"]), (0, "passed", 1)
        )

    @unittest.skipUnless(
        shutil.which("cargo") and shutil.which("rustc"), "Rust toolchain unavailable"
    )
    def test_real_rust_counts_zero_and_one(self):
        """Real Rust suites with zero and one test must produce different verdicts."""
        self.write(
            "Cargo.toml",
            '[package]\nname="pcr_fixture"\nversion="0.1.0"\nedition="2021"\n',
        )
        self.write(
            "src/lib.rs", "/// A fixture with no tests.\npub fn value() -> u32 { 1 }\n"
        )
        setup = subprocess.run(
            ["cargo", "generate-lockfile", "--offline"],
            cwd=self.root,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(setup.returncode, 0, setup.stderr)
        code, report = self.invoke(
            "run_correctness_test.sh", "--lang", "rust", "--json"
        )
        self.assertEqual(
            (code, report["status"], report["tests"]["executed"]), (2, "no_tests", 0)
        )
        self.write(
            "src/lib.rs",
            "/// A real fixture test.\n#[test]\nfn sum_is_correct() { assert_eq!(1 + 2, 3); }\n",
        )
        code, report = self.invoke(
            "run_correctness_test.sh", "--lang", "rust", "--json"
        )
        self.assertEqual(
            (code, report["status"], report["tests"]["executed"]), (0, "passed", 1)
        )

    @unittest.skipUnless(
        shutil.which("npm") and shutil.which("node"), "Node/npm unavailable"
    )
    def test_real_node_counts_zero_and_one(self):
        """Check empty and nonempty real Node suites through the npm entry point."""
        self.write("package.json", '{"scripts":{"test":"node --test"}}')
        code, report = self.invoke(
            "run_correctness_test.sh", "--lang", "javascript", "--json"
        )
        self.assertEqual(
            (code, report["status"], report["tests"]["executed"]), (2, "no_tests", 0)
        )
        self.write(
            "one.test.cjs",
            "const test = require('node:test');\nconst assert = require('node:assert/strict');\n// Verify one real assertion.\ntest('sum', () => { assert.equal(1 + 2, 3); });\n",
        )
        code, report = self.invoke(
            "run_correctness_test.sh", "--lang", "javascript", "--json"
        )
        self.assertEqual(
            (code, report["status"], report["tests"]["executed"]), (0, "passed", 1)
        )

    def test_dependency_cap_enforced(self):
        """Exceeding an explicit cap must fail; meeting the cap must complete."""
        self.write("requirements.txt", "requests\nflask\n")
        for cap, expected in (("1", 1), ("2", 0)):
            with self.subTest(cap=cap):
                code, report = self.invoke(
                    "dependency_audit.py",
                    "--lang",
                    "python",
                    "--max-deps",
                    cap,
                    "--json",
                )
                self.assertEqual(code, expected)
                self.assertEqual(report["policy"]["exceeded"], expected == 1)

    def test_malformed_manifest_not_zero_success(self):
        """An unreadable manifest must expose a parsing error."""
        self.write("package.json", "{broken")
        code, report = self.invoke(
            "dependency_audit.py", "--lang", "javascript", "--json"
        )
        self.assertEqual((code, report["status"]), (2, "incomplete"))
        self.assertTrue(report["errors"])

    def test_invalid_dependency_shape_is_not_character_list(self):
        """A malformed string dependency list must not become individual package characters."""
        self.write("pyproject.toml", '[project]\ndependencies="requests"\n')
        code, report = self.invoke("dependency_audit.py", "--lang", "python", "--json")
        self.assertEqual((code, report["status"]), (2, "incomplete"))
        self.assertTrue(report["errors"])

    def test_missing_workspace_member_is_visible(self):
        """An unmatched workspace member must expose a coverage gap."""
        self.write("Cargo.toml", '[workspace]\nmembers=["missing/*"]\n')
        code, report = self.invoke("dependency_audit.py", "--lang", "rust", "--json")
        self.assertEqual((code, report["status"]), (2, "incomplete"))
        self.assertTrue(report["warnings"])

    def test_python_names_are_canonicalized_for_counts(self):
        """Equivalent package-name separators must not cause a false cap violation."""
        self.write("requirements.txt", "my_pkg\nmy-pkg\n")
        code, report = self.invoke(
            "dependency_audit.py", "--lang", "python", "--max-deps", "1", "--json"
        )
        self.assertEqual((code, report["count"]), (0, 1))

    def test_rust_alias_and_path_sources(self):
        """Resolve Cargo aliases and avoid public registry queries for path dependencies."""
        self.write(
            "Cargo.toml",
            '[dependencies]\nalias={package="serde",version="1"}\nlocal={path="../local"}\n',
        )
        inventory = read_dependencies(self.root, "rust")
        self.assertEqual(
            [(d["name"], d["source"]) for d in inventory["direct"]],
            [("serde", "registry"), ("local", "path")],
        )
        with patch.object(
            verify_packages, "check_registry", return_value=("registry_match", "exists")
        ) as checker:
            report = self.verify(inventory, public_registry=True)
        checker.assert_called_once_with("serde", "rust", 10, "https://index.crates.io")
        self.assertEqual(report["results"][1]["status"], "not_applicable")

    def test_workspace_inheritance_and_targets(self):
        """Include workspace inheritance and target-specific declarations in the inventory."""
        self.write(
            "Cargo.toml",
            '[workspace]\nmembers=["member"]\n[workspace.dependencies]\nalias={package="serde",version="1"}\n',
        )
        self.write(
            "member/Cargo.toml",
            '[dependencies]\nalias={workspace=true}\n[target."cfg(unix)".build-dependencies]\ncc="1"\n',
        )
        inventory = read_dependencies(self.root, "rust")
        self.assertEqual({d["name"] for d in inventory["direct"]}, {"serde", "cc"})
        self.assertFalse(inventory["errors"])

    def test_setup_py_is_not_executed(self):
        """Extract literal requirements without executing setup.py side effects."""
        self.write(
            "setup.py",
            "from pathlib import Path\nPath('executed').write_text('bad')\nsetup(install_requires=['requests>=2'])\n",
        )
        inventory = read_dependencies(self.root, "python")
        self.assertEqual(inventory["direct"][0]["name"], "requests")
        self.assertFalse((self.root / "executed").exists())

    def test_explicit_empty_setup_dependencies_are_valid(self):
        """Distinguish explicitly empty dependencies from unresolved declarations."""
        self.write("setup.py", "setup(install_requires=[])\n")
        code, report = self.invoke("dependency_audit.py", "--lang", "python", "--json")
        self.assertEqual((code, report["count"], report["complete"]), (0, 0, True))

    def test_poetry_configured_source_is_not_assumed_public(self):
        """Configured Poetry sources must not be replaced with assumed public PyPI queries."""
        self.write(
            "pyproject.toml",
            '[tool.poetry.dependencies]\ninternal="1"\n[[tool.poetry.source]]\nname="internal"\nurl="https://registry.invalid"\n',
        )
        inventory = read_dependencies(self.root, "python")
        with patch.object(
            verify_packages,
            "check_registry",
            side_effect=AssertionError("network called"),
        ):
            report = self.verify(inventory, public_registry=True)
        self.assertEqual(report["results"][0]["status"], "unresolved")

    def test_native_manifest_names_do_not_prove_installation(self):
        """Native declaration counts must not imply registry matches or installed libraries."""
        self.write("vcpkg.json", '{"dependencies":["zlib",{"name":"fmt"}]}')
        self.write(
            "conanfile.txt", "[requires]\nopenssl/3.0\n[generators]\nCMakeDeps\n"
        )
        inventory = read_dependencies(self.root, "cpp")
        self.assertEqual(inventory["count"], 3)
        with patch.object(
            verify_packages,
            "check_registry",
            side_effect=AssertionError("network called"),
        ):
            report = self.verify(inventory, public_registry=True)
        self.assertEqual(report["status"], "incomplete")
        self.assertTrue(
            all(item["status"] == "unresolved" for item in report["results"])
        )

    def test_npm_alias_and_workspace(self):
        """Resolve npm aliases and avoid public registry queries for workspace dependencies."""
        self.write(
            "package.json",
            json.dumps(
                {
                    "dependencies": {
                        "alias": "npm:@scope/real@^2",
                        "internal": "workspace:*",
                    }
                }
            ),
        )
        inventory = read_dependencies(self.root, "javascript")
        self.assertEqual(
            [(d["name"], d["source"]) for d in inventory["direct"]],
            [("@scope/real", "registry"), ("internal", "workspace")],
        )

    def test_private_registry_is_unresolved(self):
        """Private registry declarations must remain unresolved rather than publicly disproven."""
        self.write("package.json", '{"dependencies":{"@org/private":"1"}}')
        self.write(".npmrc", "@org:registry=https://registry.invalid/\n")
        inventory = read_dependencies(self.root, "javascript")
        with patch.object(
            verify_packages,
            "check_registry",
            side_effect=AssertionError("network called"),
        ):
            report = self.verify(inventory, public_registry=True)
        self.assertEqual(report["status"], "incomplete")
        self.assertEqual(report["results"][0]["status"], "unresolved")

    def test_offline_mode_does_not_query(self):
        """Offline checks must remain unverified and make no network calls."""
        self.write("requirements.txt", "requests\n")
        inventory = read_dependencies(self.root, "python")
        with patch.object(
            verify_packages,
            "check_registry",
            side_effect=AssertionError("network called"),
        ):
            report = self.verify(inventory, offline=True, public_registry=True)
        self.assertEqual(
            (report["status"], report["checks_performed"]), ("incomplete", 0)
        )

    def test_network_error_is_not_missing_package(self):
        """Network or server failures must not become missing-package findings."""
        self.write("requirements.txt", "requests\n")
        inventory = read_dependencies(self.root, "python")
        with patch.object(
            verify_packages, "check_registry", return_value=("error", "HTTP 503")
        ):
            report = self.verify(inventory, public_registry=True)
        self.assertEqual(report["results"][0]["status"], "error")
        self.assertEqual(report["status"], "incomplete")

    def test_registry_404_is_only_registry_absence(self):
        """A public HTTP 404 must retain its registry-specific interpretation."""
        import urllib.error

        error = urllib.error.HTTPError(
            "https://example.invalid", 404, "missing", {}, None
        )
        with patch("urllib.request.urlopen", side_effect=error):
            status, reason = verify_packages.check_registry("missing", "python")
        self.assertEqual(status, "not_found")
        self.assertIn("not proof", reason)

    def test_registry_budget_is_visible(self):
        """Exhausting the request budget must leave remaining declarations visible."""
        self.write("requirements.txt", "requests\nflask\n")
        inventory = read_dependencies(self.root, "python")
        with patch.object(
            verify_packages, "check_registry", return_value=("registry_match", "exists")
        ):
            report = self.verify(inventory, max_checks=1, public_registry=True)
        self.assertEqual(
            (report["status"], report["checks_performed"]), ("incomplete", 1)
        )
        self.assertEqual(len(report["results"]), 2)

    def test_mixed_manifest_not_arbitrarily_selected(self):
        """Mixed root manifests must require an explicit package or language selection."""
        self.write("Cargo.toml", "[package]\nname='x'\n")
        self.write("package.json", "{}")
        self.assertEqual(detect_lang(self.root), "mixed")
        code, report = self.invoke("dependency_audit.py", "--json")
        self.assertEqual((code, report["status"]), (2, "incomplete"))

    def test_cmake_default_languages(self):
        """Distinguish default CMake languages from an explicit C-only project."""
        self.harness.unlink()
        self.write("CMakeLists.txt", "project(example)\n")
        self.assertEqual(detect_lang(self.root), "cpp")
        self.write("CMakeLists.txt", "project(example LANGUAGES C)\n")
        self.assertEqual(detect_lang(self.root), "c")

    def test_facts_paths_with_spaces_and_same_line_deps(self):
        """Handle paths with spaces and same-line dependency arrays correctly."""
        self.write(
            "pyproject.toml",
            '[project]\nname="demo"\ndependencies=["requests","flask"]\n',
        )
        self.write("directory with spaces/app.py", "x = 1\ny = 2\n")
        code, report = self.invoke("collect_facts.sh", "--output", "json")
        self.assertEqual(code, 0)
        self.assertEqual(
            [(i["unit"], i["count"]) for i in report["dependency_inventories"]],
            [(".", 2)],
        )
        self.assertEqual(report["codebase"]["source_files"], 2)

    def test_file_limit_is_incomplete(self):
        """A scan limit must not imply complete project coverage."""
        # Add a second file to make the limit genuinely truncate.
        self.write("another.py", "x = 1\n")
        code, report = self.invoke(
            "collect_facts.sh", "--max-files", "1", "--output", "json"
        )
        self.assertEqual(
            (code, report["status"], report["complete"]), (2, "incomplete", False)
        )

    def test_ordered_duplicate_blocks(self):
        """Match ordered blocks rather than unordered collections of shared lines."""
        self.harness.unlink()
        self.write("a.py", "alpha=1\nbeta=2\ngamma=3\n")
        self.write("b.py", "alpha=1\nbeta=2\ngamma=3\n")
        self.write("c.py", "gamma=3\nbeta=2\nalpha=1\n")
        code, report = self.invoke(
            "detect_duplicates.sh", "--lang", "python", "--threshold", "3", "--json"
        )
        self.assertEqual(code, 0)
        self.assertEqual(len(report["candidates"]), 1)
        self.assertEqual(
            {loc["file"] for loc in report["candidates"][0]["locations"]},
            {"a.py", "b.py"},
        )

    def test_braces_are_not_duplicate_evidence(self):
        """Punctuation-only lines must not create duplicate-implementation candidates."""
        self.write("a.c", "{\n}\n{\n}\n")
        self.write("b.c", "{\n}\n{\n}\n")
        code, report = self.invoke(
            "detect_duplicates.sh", "--lang", "c", "--threshold", "2", "--json"
        )
        self.assertEqual((code, report["candidates"]), (0, []))

    def test_duplicate_result_limit_is_visible(self):
        """Truncated duplicate results must not claim complete coverage."""
        for name in ("a", "b"):
            self.write(
                f"{name}.py",
                f"alpha=1\nbeta=2\ngamma=3\nonly_{name}=0\nomega=9\npsi=8\nchi=7\n",
            )
        code, report = self.invoke(
            "detect_duplicates.sh",
            "--lang",
            "python",
            "--threshold",
            "3",
            "--max-results",
            "1",
            "--json",
        )
        self.assertEqual((code, report["status"]), (2, "incomplete"))
        self.assertEqual(len(report["candidates"]), 1)

    def test_invalid_limits_are_rejected_before_execution(self):
        """Reject invalid limits before they can skip checks or remove execution bounds."""
        for flag, value in (("--runs", "0"), ("--warmup", "-1"), ("--timeout", "0")):
            with self.subTest(flag=flag):
                result = subprocess.run(
                    self.helper_argv("run_benchmark_comparison.sh", flag, value),
                    cwd=self.root,
                    env=self.env,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("must be", result.stderr)

    def test_jest_and_node_counts(self):
        """Known summaries must distinguish executed cases from entirely skipped suites."""
        for output, executed in (
            ("Tests: 2 passed, 1 skipped, 3 total", 2),
            ("# tests 3\n# pass 2\n# fail 0\n# skipped 1\n", 2),
            ("Tests  3 skipped (3)", 0),
        ):
            with self.subTest(output=output):
                self.assertEqual(
                    check_runner.summary_counts(output)["executed"], executed
                )


    # Test evidence: summaries, adapters, failure kinds, side effects and limits.

    def test_every_summary_block_is_counted(self):
        """A failing summary between passing ones must fail even when the command exits zero."""
        script = self.write(
            "summaries.py",
            "print('Tests: 1 passed, 1 total')\nprint('Tests: 2 failed, 2 total')\n"
            "print('Tests: 1 passed, 1 total')\n",
        )
        command = [sys.executable, str(script)]
        code, report = self.invoke("run_correctness_test.sh", "--command-argv", json.dumps(command), "--json")
        self.assertEqual((code, report["status"]), (1, "failed"))
        self.assertEqual(
            (report["tests"]["executed"], report["tests"]["failed"], report["tests"]["summary_blocks"]),
            (4, 2, 3),
        )
        counts = check_runner.summary_counts(
            "# tests 2\n# pass 2\n# fail 0\n# tests 3\n# pass 2\n# fail 1\n"
        )
        self.assertEqual((counts["executed"], counts["failed"], counts["summary_blocks"]), (5, 1, 2))

    def test_other_runner_summaries_are_counted(self):
        """Mocha, pytest, repeated unittest and go test summaries must produce counts."""
        events = (
            {"Action": "run", "Test": "TestA"},
            {"Action": "pass", "Test": "TestA"},
            {"Action": "fail", "Test": "TestB"},
            {"Action": "skip", "Test": "TestC"},
            {"Action": "fail", "Package": "example.com/x"},
        )
        cases = {
            "  2 passing (5ms)\n  1 pending\n  1 failing\n": (3, 1, 1),
            "===== 1 failed, 2 passed, 1 skipped, 3 warnings in 0.12s =====\n": (3, 1, 1),
            "Ran 2 tests in 0.001s\n\nOK\nRan 3 tests in 0.002s\n\nFAILED (failures=1, skipped=1)\n": (4, 1, 1),
            "\n".join(json.dumps(event) for event in events): (2, 1, 1),
            "--- PASS: TestA (0.00s)\n    --- FAIL: TestA/sub (0.00s)\n": (2, 1, 0),
        }
        for output, expected in cases.items():
            with self.subTest(output=output[:40]):
                counts = check_runner.summary_counts(output)
                self.assertEqual((counts["executed"], counts["failed"], counts["skipped"]), expected)
        self.assertIsNone(check_runner.summary_counts("2 retries in 3.5s\nall good\n"))

    def test_environment_failures_are_not_assertions(self):
        """Missing modules must be classified apart from failing assertions."""
        script = self.write(
            "broken.py",
            "print(\"ModuleNotFoundError: No module named 'absent_dependency'\")\nraise SystemExit(1)\n",
        )
        command = [sys.executable, str(script)]
        code, report = self.invoke("run_correctness_test.sh", "--command-argv", json.dumps(command), "--json")
        self.assertEqual((code, report["status"], report["failure_kind"]), (1, "failed", "environment"))
        self.assertIn("absent_dependency", report["failure_evidence"][0])
        self.assertIn("--command", report["hint"])
        code, report = self.correctness("failure")
        self.assertEqual((code, report["failure_kind"]), (1, "assertion"))

    @unittest.skipUnless(importlib.util.find_spec("pytest"), "pytest unavailable")
    def test_real_pytest_import_error_is_environment(self):
        """A collection ImportError in real pytest must be reported as an environment failure."""
        self.write(
            "test_imports.py",
            "import absent_dependency_for_codesift\n\n\ndef test_never_runs():\n"
            "    \"\"\"Never reached because collection fails.\"\"\"\n    assert True\n",
        )
        code, report = self.invoke("run_correctness_test.sh", "--lang", "python", "--json")
        self.assertEqual((code, report["status"], report["failure_kind"]), (1, "failed", "environment"))

    def test_workspace_mutation_is_reported(self):
        """A test command that writes into the reviewed tree must be reported, not hidden."""
        code, report = self.correctness("side_effect")
        self.assertEqual((code, report["status"]), (0, "passed"))
        self.assertEqual(report["workspace_mutations"]["created"], ["side_effect.txt"])
        self.assertTrue(any("changed 1 file" in warning for warning in report["warnings"]))

    def test_timeout_reason_names_the_limit(self):
        """A timed-out suite must say which limit stopped it; the default suits real suites."""
        command = self.python_command("import time; time.sleep(5)")
        code, report = self.invoke(
            "run_correctness_test.sh", "--command-argv", json.dumps(command), "--timeout", "1", "--json"
        )
        self.assertEqual((code, report["status"], report["failure_kind"]), (2, "timed_out", "timeout"))
        self.assertIn("--timeout 1s", report["reason"])
        help_text = self.run_plain("run_correctness_test.sh", "--help").stdout
        self.assertIn("default 300", help_text)

    def test_legacy_metrics_variable_still_works(self):
        """Harnesses written for PCR_METRICS_PATH must keep working."""
        code, report = self.correctness("legacy_scale", "--scale", "5")
        self.assertEqual((code, report["status"], report["scale_verified"]), (0, "passed", True))

    @unittest.skipIf(WINDOWS, "POSIX SIGTERM differs from Windows console cancellation")
    def test_sigterm_stops_children_and_cleans_temp(self):
        """SIGTERM and SIGHUP must clean all generations and the helper's temporary reports."""
        for number in (signal.SIGTERM, signal.SIGHUP):
            with self.subTest(signal=number):
                command, directory = self.tree_command(name=f"pids-{number}")
                process = subprocess.Popen(
                    self.helper_argv(
                        "run_correctness_test.sh", "--command-argv", json.dumps(command), "--json"
                    ),
                    env=self.env, cwd=self.root,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                self.addCleanup(self.cleanup_helper, process)
                self.wait_for_tree(directory)
                process.send_signal(number)
                self.assertEqual(process.wait(timeout=10), 128 + number)
                self.assert_tree_stopped(directory)
                self.assertEqual(list((self.root / "tmp").iterdir()), [])

    def test_cargo_workspace_flag_only_for_workspaces(self):
        """Only Cargo workspaces need --workspace to include member packages."""
        self.write("Cargo.toml", '[package]\nname="solo"\nversion="0.1.0"\n')
        self.assertEqual(check_runner.cargo_workspace_flags(self.root), [])
        self.write("Cargo.toml", '[package]\nname="solo"\nversion="0.1.0"\n[workspace]\nmembers=["m"]\n')
        self.assertEqual(check_runner.cargo_workspace_flags(self.root), ["--workspace"])

    @unittest.skipUnless(
        shutil.which("cargo") and shutil.which("rustc"), "Rust toolchain unavailable"
    )
    def test_real_rust_workspace_member_failure_is_seen(self):
        """A failing workspace member must not hide behind a passing root package."""
        self.write(
            "Cargo.toml",
            '[package]\nname="root_pkg"\nversion="0.1.0"\nedition="2021"\n'
            '[workspace]\nmembers=["member"]\n',
        )
        self.write("src/lib.rs", "/// Root fixture test.\n#[test]\nfn root_ok() { assert_eq!(1, 1); }\n")
        self.write("member/Cargo.toml", '[package]\nname="member_pkg"\nversion="0.1.0"\nedition="2021"\n')
        self.write(
            "member/src/lib.rs",
            "/// A member test that fails.\n#[test]\nfn member_broken() { assert_eq!(1, 2); }\n",
        )
        setup = subprocess.run(
            ["cargo", "generate-lockfile", "--offline"],
            cwd=self.root,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(setup.returncode, 0, setup.stderr)
        code, report = self.invoke("run_correctness_test.sh", "--lang", "rust", "--json")
        self.assertEqual((code, report["status"], report["tests"]["failed"]), (1, "failed", 1))
        self.assertIn("--workspace", report["execution"]["command"])
        self.assertEqual(report["failure_kind"], "assertion")
        self.assertEqual(report["tests"]["rust_targets"], ["member_pkg", "root_pkg"])

    @unittest.skipUnless(shutil.which("go"), "Go toolchain unavailable")
    def test_real_go_adapter_counts_tests(self):
        """The Go adapter must run offline and count executed tests from -json events."""
        self.write("go.mod", "module example.com/fixture\n\ngo 1.21\n")
        self.write(
            "fixture_test.go",
            "package fixture\n\nimport \"testing\"\n\n// TestSum verifies one observable behavior.\n"
            "func TestSum(t *testing.T) {\n\tif 1+2 != 3 {\n\t\tt.Fatal(\"wrong sum\")\n\t}\n}\n",
        )
        self.env.update(
            GOCACHE=str(self.root / "tmp" / "go-cache"),
            GOPATH=str(self.root / "tmp" / "gopath"),
            GOTOOLCHAIN="local",
            GOFLAGS="",
            GOWORK="off",
        )
        code, report = self.invoke("run_correctness_test.sh", "--lang", "go", "--json")
        self.assertEqual((code, report["status"], report["tests"]["executed"]), (0, "passed", 1))
        self.assertEqual(report["adapter_env"], {"GOPROXY": "off"})
        self.assertIn("-count=1", report["execution"]["command"])
        for path in (self.root / "tmp").rglob("*"):
            path.chmod(path.stat().st_mode | stat.S_IWUSR)
        shutil.rmtree(self.root / "tmp" / "go-cache", ignore_errors=True)
        shutil.rmtree(self.root / "tmp" / "gopath", ignore_errors=True)

    def test_benchmark_output_comparison_and_spread(self):
        """Different outputs must not be timed as the same work; equal outputs report spread."""
        code, report = self.bench(
            self.harness_command("output", "a"), self.harness_command("output", "b"), "--compare-output"
        )
        self.assertEqual((code, report["status"], report["output_comparison"]["equal"]), (1, "output_mismatch", False))
        command = self.harness_command("output", "same")
        code, report = self.bench(command, command, "--compare-output")
        self.assertEqual((code, report["status"], report["output_comparison"]["equal"]), (0, "measured", True))
        self.assertIn(report["spread"]["verdict"], {"inconclusive", "separated"})
        self.assertGreaterEqual(report["summary"]["project"]["mad_seconds"], 0)

    # Python interpreter guard.

    def test_python_version_guard_explains_old_interpreters(self):
        """Old interpreters must get an actionable message and exit 2 instead of a traceback."""
        message = python_version_error((3, 9, 6), "/usr/bin/python3")
        self.assertIn("3.9.6", message)
        self.assertIn("CODESIFT_PYTHON", message)
        self.assertIsNone(python_version_error((3, 11, 0)))
        old = Path("/usr/bin/python3")
        if not old.is_file():
            return
        probe = subprocess.run(
            [str(old), "-c", "import sys; print(sys.version_info >= (3, 11))"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if probe.stdout.strip() != "False":
            return
        result = subprocess.run(
            [str(old), str(SCRIPTS / "dependency_audit.py"), "--root", str(self.root)],
            env=self.env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("require Python 3.11+", result.stderr)

    @unittest.skipIf(WINDOWS, "Bash wrappers are an optional POSIX compatibility entry point")
    @unittest.skipUnless(shutil.which("bash"), "Bash unavailable for wrapper integration")
    def test_posix_wrappers_match_python_entry_points(self):
        """Keep the four Bash wrappers covered while the core suite uses native Python."""
        success = json.dumps(self.harness_command("exit", "0"))
        arguments = {
            "collect_facts.sh": ("--output", "json"),
            "detect_duplicates.sh": ("--json",),
            "run_correctness_test.sh": (
                "--command-argv", json.dumps(self.command_for_case("pass")), "--json"
            ),
            "run_benchmark_comparison.sh": (
                "--project-argv", success, "--baseline-argv", success,
                "--runs", "1", "--warmup", "0", "--json"
            ),
        }
        for script, extra in arguments.items():
            with self.subTest(script=script):
                expected_code, expected = self.invoke(script, *extra)
                process = subprocess.run(
                    ["bash", str(SCRIPTS / script), "--root", str(self.root), *extra],
                    env=dict(self.env, CODESIFT_PYTHON=sys.executable), cwd=self.root,
                    capture_output=True, text=True, encoding="utf-8", timeout=50,
                )
                self.assertEqual(process.returncode, expected_code, process.stderr)
                actual = json.loads(process.stdout)
                self.assertEqual(
                    (actual["status"], actual["complete"]),
                    (expected["status"], expected["complete"]),
                )
        self.assertEqual(check_runner.command_argv("printf normal"), ["printf", "normal"])
        old = Path("/usr/bin/python3")
        if old.is_file():
            probe = subprocess.run(
                [str(old), "-c", "import sys; print(sys.version_info >= (3, 11))"],
                capture_output=True, text=True, encoding="utf-8", timeout=30,
            )
            if probe.returncode == 0 and probe.stdout.strip() == "False":
                wrapped = subprocess.run(
                    ["bash", str(SCRIPTS / "collect_facts.sh"), "--root", str(self.root)],
                    env=dict(self.env, CODESIFT_PYTHON=str(old)), cwd=self.root,
                    capture_output=True, text=True, encoding="utf-8", timeout=30,
                )
                self.assertEqual(wrapped.returncode, 2)
                self.assertIn("CODESIFT_PYTHON", wrapped.stderr)

    def test_setup_and_requirements_declared_encodings(self):
        """Honor Python encoding cookies and UTF-8 BOMs without executing setup.py."""
        for encoding, label in (("latin-1", "café"), ("gbk", "中文"), ("utf-8-sig", "中文")):
            with self.subTest(encoding=encoding):
                header = "" if encoding == "utf-8-sig" else f"# coding: {encoding}\n"
                (self.root / "setup.py").write_bytes(
                    (header + f"# {label}\nsetup(install_requires=['requests>=2'])\n").encode(encoding)
                )
                (self.root / "requirements.txt").write_bytes(
                    (header + f"# {label}\nflask>=3\n").encode(encoding)
                )
                inventory = read_dependencies(self.root, "python")
                self.assertEqual({item["name"] for item in inventory["direct"]}, {"requests", "flask"})
                self.assertFalse(inventory["errors"], inventory["errors"])
                self.assertFalse((self.root / "executed").exists())

    def test_manifest_decoding_ignores_host_locale(self):
        """UTF-8 JSON and TOML must preserve Unicode on an otherwise CP1252 host."""
        original_open = io.open

        def legacy_open(file, mode="r", *arguments, **options):
            """Simulate a legacy text default while retaining binary file semantics."""
            if "b" not in mode and options.get("encoding") in (None, "locale"):
                options["encoding"] = "cp1252"
            return original_open(file, mode, *arguments, **options)

        expected = {"name": "中文 café"}
        for filename, text in (
            ("package.json", json.dumps(expected, ensure_ascii=False)),
            ("pyproject.toml", 'name = "中文 café"\n'),
        ):
            with self.subTest(filename=filename):
                path = self.write(filename, text)
                with patch("pathlib.io.open", side_effect=legacy_open):
                    self.assertEqual(load_manifest(path), expected)

    def test_reports_survive_restricted_stdout(self):
        """JSON retains Unicode values and text output stays writable on legacy code pages."""
        report = {"path": "目录/café/😀", "status": "completed"}
        for encoding in ("cp1252", "gbk"):
            with self.subTest(encoding=encoding), io.BytesIO() as buffer:
                with io.TextIOWrapper(buffer, encoding=encoding, errors="strict") as stream:
                    with patch("sys.stdout", stream):
                        language_tools.print_report(report, True)
                        stream.flush()
                        self.assertEqual(json.loads(buffer.getvalue().decode(encoding)), report)
                        language_tools.print_text("目录/café/😀")
                        stream.flush()
                    self.assertIn(b"completed", buffer.getvalue())

    def test_json_argv_preserves_unicode_and_literal_arguments(self):
        """A structured argv preserves quotes, empty strings and metacharacters on every OS."""
        script = self.write("中文 path/argument echo.py", HARNESS)
        values = ["", "two words", "中文", 'a"b', "a'b", "C:\\trailing\\", "; touch injected", "$(touch injected)", "& echo injected > injected", "%CODESIFT_NOT_EXPANDED%"]
        command = [sys.executable, str(script), "argv", *values]
        code, report = self.bench(command)
        self.assertEqual((code, report["status"]), (0, "measured"))
        self.assertEqual(json.loads(report["samples"][0]["output"]), values)
        self.assertFalse((self.root / "injected").exists())

    def test_argv_files_are_relative_to_root_and_accept_utf8_bom(self):
        """Argument files resolve from the reviewed root and preserve their Unicode payload."""
        correct = self.write("命令/correct.json", json.dumps(self.command_for_case("pass"), ensure_ascii=False))
        correct.write_bytes(b"\xef\xbb\xbf" + correct.read_bytes())
        code, report = self.invoke(
            "run_correctness_test.sh", "--command-argv-file", "命令/correct.json", "--json"
        )
        self.assertEqual((code, report["status"]), (0, "passed"))
        for side in ("project", "baseline"):
            self.write(f"命令/{side}.json", json.dumps(self.harness_command("output", "same")))
        code, report = self.invoke(
            "run_benchmark_comparison.sh", "--project-argv-file", "命令/project.json",
            "--baseline-argv-file", "命令/baseline.json", "--runs", "1", "--warmup", "0",
            "--compare-output", "--json",
        )
        self.assertEqual((code, report["status"], report["output_comparison"]["equal"]), (0, "measured", True))

    def test_invalid_argv_is_rejected_before_execution(self):
        """Malformed structured commands must fail before a child can write a marker."""
        marker = self.python_command("from pathlib import Path; Path('injected').write_text('bad')")
        for value in ("[]", "{}", '"command"', '["", "argument"]', '["python", 1]', '["python", null]', '["python", "bad\\u0000arg"]', "[broken", json.dumps([*marker, None])):
            with self.subTest(value=value):
                result = self.run_plain("run_correctness_test.sh", "--command-argv", value, "--json")
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        result = self.run_plain(
            "run_correctness_test.sh", "--command", "unused", "--command-argv", '["unused"]'
        )
        self.assertEqual(result.returncode, 2)
        result = self.run_plain(
            "run_correctness_test.sh", "--command-argv", json.dumps(marker),
            "--output-encoding", "not-a-real-codec", "--json",
        )
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "injected").exists())

    def test_child_log_encoding_is_explicit_and_damage_is_visible(self):
        """An explicit codec restores valid evidence while an incorrect codec remains incomplete."""
        for encoding, label in (("cp1252", "café"), ("gbk", "中文"), ("utf-8-sig", "中文")):
            with self.subTest(encoding=encoding):
                raw = (label + "\nTests: 1 passed, 1 total\n").encode(encoding)
                command = self.python_command(f"import sys; sys.stdout.buffer.write({raw!r})")
                code, report = self.invoke(
                    "run_correctness_test.sh", "--command-argv", json.dumps(command),
                    "--output-encoding", encoding, "--json",
                )
                self.assertEqual((code, report["status"]), (0, "passed"))
                self.assertFalse(report["execution"]["output_decode_error"])
                self.assertIn(label, report["execution"]["output"])
                if encoding != "utf-8-sig":
                    code, damaged = self.invoke(
                        "run_correctness_test.sh", "--command-argv", json.dumps(command), "--json"
                    )
                    self.assertEqual((code, damaged["status"]), (2, "incomplete"))
                    self.assertTrue(damaged["execution"]["output_decode_error"])
                    self.assertEqual(damaged["execution"]["output_sha256"], report["execution"]["output_sha256"])

    @unittest.skipUnless(WINDOWS, "PowerShell native entry-point integration runs on Windows")
    def test_powershell_entry_preserves_unicode_and_argv_file(self):
        """Windows PowerShell 5.1 and available pwsh must pass Unicode paths into Python intact."""
        shells = list(dict.fromkeys(path for name in ("powershell.exe", "pwsh.exe") if (path := shutil.which(name))))
        self.assertTrue(shutil.which("powershell.exe"), "Windows PowerShell 5.1 is required for this integration")
        target = self.write("项目 名/案例.py", HARNESS)
        argument_file = self.write("命令/参数.json", json.dumps([sys.executable, str(target), "pass", "{report}"]))
        environment = dict(
            self.env,
            CODESIFT_TEST_PYTHON=sys.executable,
            CODESIFT_TEST_RUNNER=str(SCRIPTS / "lib/check_runner.py"),
            CODESIFT_TEST_ROOT=str(self.root),
            CODESIFT_TEST_ARGV=str(argument_file),
        )
        command = (
            '& $env:CODESIFT_TEST_PYTHON $env:CODESIFT_TEST_RUNNER correctness '
            '--root $env:CODESIFT_TEST_ROOT --command-argv-file $env:CODESIFT_TEST_ARGV --json; '
            'exit $LASTEXITCODE'
        )
        for shell in shells:
            with self.subTest(shell=shell):
                result = subprocess.run(
                    [shell, "-NoProfile", "-NonInteractive", "-Command", command],
                    cwd=self.root, env=environment, capture_output=True, text=True, encoding="utf-8", timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
                report = json.loads(result.stdout)
                self.assertEqual((report["status"], report["tests"]["executed"]), ("passed", 1))
                self.assertIn(str(target), report["execution"]["command"])

    @unittest.skipUnless(WINDOWS, "Trusted PowerShell execution is a Windows native contract")
    def test_powershell_trusted_exit_code_is_propagated(self):
        """Both Windows shells must retain a failing native exit status through the trusted path."""
        shells = list(dict.fromkeys(path for name in ("powershell.exe", "pwsh.exe") if (path := shutil.which(name))))
        self.assertTrue(shutil.which("powershell.exe"), "Windows PowerShell 5.1 is required for this integration")
        original_path = self.env.get("PATH", "")
        self.env["CODESIFT_TEST_PYTHON"] = sys.executable
        try:
            for shell in shells:
                with self.subTest(shell=shell):
                    self.env["PATH"] = os.pathsep.join((str(Path(shell).parent), str(Path(sys.executable).parent)))
                    code, report = self.invoke(
                        "run_correctness_test.sh", "--command",
                        "Write-Output 'Tests: 1 passed, 1 total'; & $env:CODESIFT_TEST_PYTHON -c 'import sys; sys.exit(7)'; exit $LASTEXITCODE",
                        "--trust-command", "--shell", "powershell", "--json",
                    )
                    self.assertEqual((code, report["status"], report["execution"]["exit_code"]), (1, "failed", 7))
                    self.assertEqual(Path(report["execution"]["command"][0]).resolve(), Path(shell).resolve())
        finally:
            self.env["PATH"] = original_path

    @unittest.skipUnless(WINDOWS, "Case-insensitive native environment lookup requires Windows")
    def test_windows_native_environment_overrides_are_unique(self):
        """Win32 must read the temporary npm settings instead of inherited uppercase duplicates."""
        outside = self.root / "outside-cache"
        for key in tuple(self.env):
            if key.upper() in {"NPM_CONFIG_CACHE", "NPM_CONFIG_UPDATE_NOTIFIER"}:
                del self.env[key]
        self.env.update(
            NPM_CONFIG_CACHE=str(outside),
            NPM_CONFIG_UPDATE_NOTIFIER="true",
            CODESIFT_OUTSIDE_CACHE=str(outside),
        )
        script = self.write(
            "native_environment.py",
            '"""Use Win32 lookups to verify the exact environment delivered to a real child."""\n'
            "import ctypes\nfrom pathlib import Path\n"
            "kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)\n"
            "kernel32.GetEnvironmentVariableW.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_ulong)\n"
            "kernel32.GetEnvironmentVariableW.restype = ctypes.c_ulong\n"
            "def native_value(name):\n"
            '    """Read a variable using Windows lookup semantics rather than Python enumeration."""\n'
            "    size = kernel32.GetEnvironmentVariableW(name, None, 0)\n"
            "    if not size:\n        raise ctypes.WinError(ctypes.get_last_error())\n"
            "    buffer = ctypes.create_unicode_buffer(size)\n"
            "    copied = kernel32.GetEnvironmentVariableW(name, buffer, size)\n"
            "    if not copied or copied >= size:\n        raise RuntimeError('environment value changed')\n"
            "    return buffer.value\n"
            "report = Path(native_value('CODESIFT_REPORT_PATH'))\n"
            "cache = Path(native_value('NPM_CONFIG_CACHE'))\n"
            "outside = Path(native_value('CODESIFT_OUTSIDE_CACHE'))\n"
            "if cache.resolve() == outside.resolve() or native_value('NPM_CONFIG_UPDATE_NOTIFIER') != 'false':\n"
            "    outside.mkdir(parents=True, exist_ok=True)\n"
            "    (outside / 'leaked').write_text('wrong environment', encoding='ascii')\n"
            "    raise AssertionError('native lookup saw inherited npm settings')\n"
            "assert cache.resolve() == (report.parent / 'npm-cache').resolve()\n"
            "report.write_text('<testsuite tests=\"1\"><testcase name=\"native_environment\"/></testsuite>', encoding='utf-8')\n",
        )
        code, report = self.invoke(
            "run_correctness_test.sh", "--command-argv", json.dumps([sys.executable, str(script)]), "--json"
        )
        self.assertEqual((code, report["status"], report["tests"]["executed"]), (0, "passed", 1))
        self.assertFalse((outside / "leaked").exists())
        self.assertFalse(outside.exists())
        self.assertEqual(list((self.root / "tmp").iterdir()), [])

    @unittest.skipUnless(WINDOWS, "Job Object handle closure requires a Windows kernel")
    def test_windows_hard_killed_owner_reaps_job_descendants(self):
        """Killing the Job owner must close its non-inherited handle and terminate all descendants."""
        command, directory = self.tree_command()
        owner = self.write(
            "job_owner.py",
            '"""Keep one owned process tree alive until the outer test hard-kills this owner."""\n'
            "import os\nfrom pathlib import Path\nimport sys\n"
            f"sys.path.insert(0, {str(SCRIPTS / 'lib')!r})\n"
            "from process_control import spawn_process\n"
            f"with open(os.devnull, 'wb') as output:\n"
            f"    process = spawn_process({command!r}, Path.cwd(), dict(os.environ), output)\n"
            "    try:\n        process.wait(timeout=60)\n    finally:\n        process.close()\n",
        )
        process = subprocess.Popen(
            [sys.executable, str(owner)], cwd=self.root, env=self.env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        self.addCleanup(self.cleanup_helper, process)
        self.wait_for_tree(directory)
        process.kill()
        process.wait(timeout=10)
        self.assert_tree_stopped(directory)

    @unittest.skipUnless(WINDOWS, "CTRL_C_EVENT integration requires an isolated Windows console")
    def test_windows_console_cancel_reaps_ignoring_descendants(self):
        """A private console Ctrl+C cancels the helper and reaps children that ignore Ctrl+C."""
        command, directory = self.tree_command("ignore-console")
        arguments = self.helper_argv("run_correctness_test.sh", "--command-argv", json.dumps(command), "--json")
        result_file = self.root / "console-result.json"
        monitor = self.write(
            "console_monitor.py",
            '"""Generate Ctrl+C only in this process\'s separately created console."""\n'
            "import ctypes\nimport json\nfrom pathlib import Path\nimport subprocess\nimport time\n"
            "kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)\n"
            "handler_type = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong)\n"
            "kernel32.SetConsoleCtrlHandler.argtypes = (handler_type, ctypes.c_int)\n"
            "kernel32.GenerateConsoleCtrlEvent.argtypes = (ctypes.c_ulong, ctypes.c_ulong)\n"
            "@handler_type\n"
            "def ignore_monitor_event(number):\n"
            '    """Let the monitor survive its own console broadcast without changing child handlers."""\n'
            "    return number == 0\n"
            "if not kernel32.SetConsoleCtrlHandler(ignore_monitor_event, True):\n"
            "    raise ctypes.WinError(ctypes.get_last_error())\n"
            f"directory = Path({str(directory)!r})\n"
            f"process = subprocess.Popen({arguments!r}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n"
            "try:\n"
            "    deadline = time.monotonic() + 15\n"
            "    while not all((directory / role).is_file() for role in ('root', 'child', 'grandchild')):\n"
            "        if process.poll() is not None or time.monotonic() > deadline:\n"
            "            raise RuntimeError('command tree did not become ready')\n"
            "        time.sleep(0.05)\n"
            "    if not kernel32.GenerateConsoleCtrlEvent(0, 0):\n"
            "        raise ctypes.WinError(ctypes.get_last_error())\n"
            "    code = process.wait(timeout=15)\n"
            f"    Path({str(result_file)!r}).write_text(json.dumps({{'exit_code': code}}), encoding='ascii')\n"
            "finally:\n"
            "    if process.poll() is None:\n        process.kill()\n"
            "    process.wait(timeout=10)\n",
        )
        startup = subprocess.STARTUPINFO(
            dwFlags=subprocess.STARTF_USESHOWWINDOW, wShowWindow=subprocess.SW_HIDE
        )
        process = subprocess.Popen(
            [sys.executable, str(monitor)], cwd=self.root, env=self.env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            startupinfo=startup,
        )
        self.addCleanup(self.cleanup_helper, process)
        self.assertEqual(process.wait(timeout=35), 0, "isolated console monitor failed")
        self.assertEqual(json.loads(result_file.read_bytes())["exit_code"], 130)
        self.assert_tree_stopped(directory)
        self.assertEqual(list((self.root / "tmp").iterdir()), [])

    # Repository facts: units, exclusions, encodings and output format.

    def test_monorepo_units_and_languages(self):
        """Nested packages in other languages must become review units with counted sources."""
        self.write(
            "package.json",
            json.dumps({"private": True, "workspaces": ["packages/*"], "scripts": {"build": "tsc"}}),
        )
        self.write("packages/web/package.json", json.dumps({"name": "web", "main": "index.js"}))
        self.write("packages/web/index.js", "module.exports = 1;\n")
        self.write(
            "services/api/pyproject.toml",
            '[project]\nname="api"\ndependencies=["fastapi"]\n[project.scripts]\napi="api.main:run"\n',
        )
        self.write(
            "services/api/api/main.py",
            "def run():\n    return 1\n\nif __name__ == '__main__':\n    run()\n",
        )
        self.write("crates/tool/Cargo.toml", '[package]\nname="tool"\nversion="0.1.0"\n')
        self.write("crates/tool/src/main.rs", "fn main() {}\n")
        self.write("services/worker/go.mod", "module example.com/worker\n\ngo 1.21\n")
        self.write("services/worker/main.go", "package main\n\nfunc main() {}\n")
        code, report = self.invoke("collect_facts.sh", "--output", "json")
        self.assertEqual(code, 0, report["warnings"] + report["errors"])
        self.assertEqual(
            [unit["path"] for unit in report["units"]],
            [".", "crates/tool", "packages/web", "services/api", "services/worker"],
        )
        self.assertEqual(report["project"]["repository_languages"], ["go", "javascript", "python", "rust"])
        self.assertEqual(report["project"]["language"], "mixed")
        self.assertEqual(report["codebase"]["source_files"], 5)
        entries = {
            (entry["file"], entry.get("line"), entry.get("field"))
            for entry in report["entry_point_candidates"]
        }
        expected = {
            ("crates/tool/src/main.rs", 1, None),
            ("services/worker/main.go", 3, None),
            ("services/api/api/main.py", 4, None),
            ("services/api/pyproject.toml", None, "project.scripts"),
            ("packages/web/package.json", None, "main"),
        }
        self.assertTrue(expected <= entries, entries)
        self.assertEqual(report["coverage"]["dependency_languages_without_reader"], ["go"])
        self.assertEqual(
            {(item["unit"], item["language"]) for item in report["dependency_inventories"]},
            {(".", "javascript"), ("crates/tool", "rust"), ("packages/web", "javascript"), ("services/api", "python")},
        )
        code, report = self.invoke("collect_facts.sh", "--lang", "python", "--output", "json")
        self.assertEqual(code, 0, report["warnings"] + report["errors"])
        self.assertEqual(
            (report["project"]["language"], report["codebase"]["source_files"]), ("python", 2)
        )
        self.assertEqual(report["project"]["repository_languages"], ["go", "javascript", "python", "rust"])

    def test_facts_reports_dependency_errors_and_mixed_roots(self):
        """Facts must inventory mixed roots per language and never hide a failed manifest."""
        self.write("Cargo.toml", "[package]\nname='x'\n")
        self.write("package.json", "{}")
        code, report = self.invoke("collect_facts.sh", "--output", "json")
        self.assertEqual(code, 0, report["warnings"] + report["errors"])
        self.assertEqual(
            {(item["unit"], item["language"]) for item in report["dependency_inventories"]},
            {(".", "javascript"), (".", "rust")},
        )
        self.write("package.json", "{broken")
        code, report = self.invoke("collect_facts.sh", "--output", "json")
        self.assertEqual((code, report["status"]), (2, "incomplete"))
        self.assertTrue(any(error.startswith(". (javascript)") for error in report["errors"]))

    def test_pruned_directories_are_listed_and_includable(self):
        """Default exclusions must be visible, and an explicit include must scan them."""
        self.write("build/deploy.py", "print('deploy')\n")
        code, report = self.invoke("collect_facts.sh", "--output", "json")
        self.assertIn({"path": "build", "reason": "default_exclude"}, report["coverage"]["pruned_directories"])
        self.assertEqual((code, report["codebase"]["source_files"]), (0, 1))
        code, report = self.invoke("collect_facts.sh", "--output", "json", "--include-dir", "build")
        self.assertEqual((code, report["codebase"]["source_files"]), (0, 2))
        self.assertNotIn("build", report["coverage"]["excluded_directories"])

    def test_gbk_source_is_decoded_not_skipped(self):
        """Legacy GBK sources must be scanned and reported as decoded with a fallback."""
        text = "# \u4e2d\u6587\nvalue = '\u4f60\u597d'\n"
        (self.root / "legacy.py").write_bytes(text.encode("gbk"))
        code, report = self.invoke("collect_facts.sh", "--output", "json")
        self.assertEqual((code, report["codebase"]["source_files"]), (0, 2))
        self.assertEqual(
            report["coverage"]["decoded_with_fallback"],
            [{"file": "legacy.py", "encoding": "gb18030"}],
        )

    def test_markdown_output_is_markdown(self):
        """--output md must render a Markdown document, not key/value lines."""
        result = self.run_plain("collect_facts.sh", "--output", "md")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("# CodeSift facts\n"))
        self.assertIn("| status | completed |", result.stdout)
        self.assertIn("## coverage", result.stdout)

    # Duplicate candidates.

    def test_duplicates_within_one_file_and_merged_windows(self):
        """A long copy must be one candidate, and copies inside one file must be found."""
        self.harness.unlink()
        block = "".join(f"value_{i} = {i}\n" for i in range(20))
        self.write("a.py", block)
        self.write("b.py", block)
        self.write(
            "c.py",
            "first = 1\nsecond = 2\nthird = 3\nunrelated = 0\nfirst = 1\nsecond = 2\nthird = 3\n",
        )
        code, report = self.invoke(
            "detect_duplicates.sh", "--lang", "python", "--threshold", "3", "--json"
        )
        self.assertEqual(code, 0)
        by_files = {
            tuple(location["file"] for location in candidate["locations"]): candidate
            for candidate in report["candidates"]
        }
        self.assertEqual(set(by_files), {("a.py", "b.py"), ("c.py", "c.py")})
        self.assertEqual(by_files[("a.py", "b.py")]["matched_nontrivial_lines"], 20)
        self.assertEqual(
            [(item["start"], item["end"]) for item in by_files[("c.py", "c.py")]["locations"]],
            [(1, 3), (5, 7)],
        )

    def test_c_pointer_and_decrement_lines_are_code(self):
        """Lines such as '*p = 1;' and '--count;' are code, not comments."""
        body = "*p = 1;\n--count;\n*q = 2;\n"
        self.write("a.c", body)
        self.write("b.c", body)
        code, report = self.invoke(
            "detect_duplicates.sh", "--lang", "c", "--threshold", "3", "--json"
        )
        self.assertEqual((code, len(report["candidates"])), (0, 1))

    # Dependency inventory.

    def test_setup_py_is_read_next_to_requirements(self):
        """setup.py declarations must not be skipped when requirements.txt also exists."""
        self.write("requirements.txt", "flask\n")
        self.write(
            "setup.py",
            "from setuptools import setup\nsetup(install_requires=['requests'], extras_require={'dev': ['pytest']})\n",
        )
        inventory = read_dependencies(self.root, "python")
        self.assertEqual(
            {(d["name"], d["group"]) for d in inventory["direct"]},
            {("flask", "requirements"), ("requests", "runtime"), ("pytest", "optional:dev")},
        )
        self.assertEqual(inventory["manifests"], ["requirements.txt", "setup.py"])
        self.assertFalse(inventory["warnings"] or inventory["errors"])

    def test_setup_shim_without_arguments_is_complete(self):
        """A bare setup() shim declares nothing and must not be reported as unresolved."""
        self.write("pyproject.toml", '[project]\nname="demo"\ndependencies=["requests"]\n')
        self.write("setup.py", "from setuptools import setup\nsetup()\n")
        code, report = self.invoke("dependency_audit.py", "--lang", "python", "--json")
        self.assertEqual((code, report["count"], report["complete"]), (0, 1, True))

    def test_setup_cfg_poetry_legacy_and_pipfile(self):
        """setup.cfg, legacy Poetry dev groups and Pipfile packages must be inventoried."""
        self.write(
            "setup.cfg",
            '[options]\ninstall_requires =\n    requests\n    importlib-metadata; python_version<"3.8"\n'
            "[options.extras_require]\ndev = pytest\n",
        )
        self.write(
            "pyproject.toml",
            '[tool.poetry.dependencies]\npython="^3.11"\nhttpx="0.27"\n[tool.poetry.dev-dependencies]\nblack="24"\n',
        )
        self.write(
            "Pipfile",
            '[[source]]\nname="pypi"\nurl="https://pypi.org/simple"\n[packages]\nrich="*"\n'
            'local={path="./local"}\n[dev-packages]\nmypy="*"\n',
        )
        inventory = read_dependencies(self.root, "python")
        self.assertEqual(
            {(d["name"], d["group"], d["source"]) for d in inventory["direct"]},
            {
                ("httpx", "runtime", "registry"),
                ("black", "development:legacy", "registry"),
                ("requests", "runtime", "registry"),
                ("importlib-metadata", "runtime", "registry"),
                ("pytest", "optional:dev", "registry"),
                ("rich", "runtime", "registry"),
                ("local", "runtime", "path"),
                ("mypy", "development", "registry"),
            },
        )
        self.assertFalse(inventory["errors"])

    def test_uv_workspace_sources_are_not_public_names(self):
        """uv workspace and path sources must not be checked as public PyPI names."""
        self.write(
            "pyproject.toml",
            '[project]\nname="app"\ndependencies=["core","requests"]\n[tool.uv.sources]\n'
            'core={workspace=true}\n[tool.uv.workspace]\nmembers=["packages/*"]\n',
        )
        inventory = read_dependencies(self.root, "python")
        self.assertEqual(
            {d["name"]: d["source"] for d in inventory["direct"]},
            {"core": "workspace", "requests": "registry"},
        )
        self.assertIn("uv workspace", " ".join(inventory["warnings"]))

    def test_pnpm_workspace_is_visible(self):
        """A pnpm workspace root must not report its member packages as covered."""
        self.write("package.json", '{"dependencies":{"left-pad":"1"}}')
        self.write("pnpm-workspace.yaml", "packages:\n  - 'packages/*'\n")
        code, report = self.invoke("dependency_audit.py", "--lang", "javascript", "--json")
        self.assertEqual((code, report["status"]), (2, "incomplete"))
        self.assertIn("pnpm-workspace.yaml", report["manifests"])

    def test_requirement_url_lines_keep_inventory_and_redact_tokens(self):
        """URL, VCS and path lines are classified; one invalid line must not erase the inventory."""
        self.write(
            "requirements.txt",
            "requests>=2\ngit+https://user:token@github.com/org/tool.git@v1#egg=tool\n"
            "./vendor/localpkg\n-e .\nthis is not valid!\n",
        )
        code, report = self.invoke("dependency_audit.py", "--lang", "python", "--json")
        self.assertEqual(
            {d["name"]: d["source"] for d in report["direct"]},
            {"requests": "registry", "tool": "git", "localpkg": "path", ".": "path"},
        )
        self.assertEqual((code, report["count"]), (2, 4))
        self.assertTrue(report["errors"][0].startswith("requirements.txt:5:"))
        self.assertNotIn("token", json.dumps(report))

    def test_pip_compile_hashes_and_includes(self):
        """Hash continuations, comments and -r includes must parse without spurious warnings."""
        self.write(
            "requirements.txt",
            "-r base.txt\ncertifi==2024.2.2 \\\n    --hash=sha256:aaa \\\n    --hash=sha256:bbb\n"
            "    # via requests\n",
        )
        self.write("base.txt", "requests==2.31.0 \\\n    --hash=sha256:ccc\n")
        code, report = self.invoke("dependency_audit.py", "--lang", "python", "--json")
        self.assertEqual((code, report["status"]), (0, "completed"))
        self.assertEqual(
            {d["specifier"] for d in report["direct"]}, {"certifi==2024.2.2", "requests==2.31.0"}
        )
        self.assertTrue(all(d["hash_pinned"] for d in report["direct"]))
        self.assertEqual(report["manifests"], ["base.txt", "requirements.txt"])

    def test_requirements_index_options(self):
        """A public mirror index keeps names checkable; a private extra index marks them private."""
        self.write("requirements.txt", "--index-url https://pypi.tuna.tsinghua.edu.cn/simple\nrequests\n")
        inventory = read_dependencies(self.root, "python")
        self.assertEqual(inventory["direct"][0]["source"], "registry")
        self.assertTrue(inventory["registries"][0]["public"])
        self.write("requirements.txt", "--extra-index-url https://nexus.corp.invalid/simple\nrequests\n")
        inventory = read_dependencies(self.root, "python")
        self.assertEqual(inventory["direct"][0]["source"], "private_registry")

    def test_project_scoped_registry_marks_only_scope(self):
        """A scoped project registry must not mark unscoped packages private."""
        self.write("package.json", '{"dependencies":{"left-pad":"1","@org/private":"1"}}')
        self.write(".npmrc", "@org:registry=https://registry.invalid/\n")
        inventory = read_dependencies(self.root, "javascript")
        self.assertEqual(
            {d["name"]: d["source"] for d in inventory["direct"]},
            {"left-pad": "registry", "@org/private": "private_registry"},
        )
        self.write(".npmrc", "registry=https://registry.npmmirror.com/\n")
        inventory = read_dependencies(self.root, "javascript")
        self.assertEqual({d["source"] for d in inventory["direct"]}, {"registry"})

    # Registry checks: configuration, mirrors, routing and failure handling.

    def test_registry_breaker_stops_after_repeated_errors(self):
        """An unreachable registry must stop after one batch instead of timing out per package."""
        self.write("requirements.txt", "".join(f"pkg{i}\n" for i in range(10)))
        inventory = read_dependencies(self.root, "python")
        calls = []

        def unreachable(name, lang, timeout, base):
            """Record each attempted check and fail it like an unreachable host."""
            calls.append(name)
            return ("error", "could not reach pypi.org without a proxy: timed out after 2s")

        with patch.object(verify_packages, "check_registry", side_effect=unreachable):
            report = self.verify(inventory, public_registry=True)
        statuses = [result["status"] for result in report["results"]]
        self.assertEqual(len(calls), verify_packages.WORKERS)
        self.assertEqual((statuses.count("error"), statuses.count("not_checked")), (4, 6))
        self.assertIn("consecutive errors", report["results"][-1]["reason"])
        self.assertEqual((report["status"], report["checks_performed"]), ("incomplete", 4))

    def test_user_npmrc_without_registry_is_not_an_override(self):
        """An .npmrc with unrelated settings must not make public checks unresolved."""
        self.write("home/.npmrc", "save-exact=true\n")
        self.write("package.json", '{"dependencies":{"left-pad":"1"}}')
        inventory = read_dependencies(self.root, "javascript")
        with patch.object(
            verify_packages, "check_registry", return_value=("registry_match", "exists")
        ):
            report = self.verify(inventory)
        self.assertEqual((report["status"], report["results"][0]["status"]), ("completed", "registry_match"))

    def test_custom_user_registry_is_unresolved_by_scope(self):
        """A private default registry blocks public conclusions; a scoped one affects its scope."""
        self.write("package.json", '{"dependencies":{"left-pad":"1","@corp/ui":"1"}}')
        inventory = read_dependencies(self.root, "javascript")
        self.write("home/.npmrc", "@corp:registry=https://npm.corp.invalid/\n")
        with patch.object(
            verify_packages, "check_registry", return_value=("registry_match", "exists")
        ):
            report = self.verify(inventory)
        self.assertEqual(
            {r["name"]: r["status"] for r in report["results"]},
            {"left-pad": "registry_match", "@corp/ui": "unresolved"},
        )
        self.write("home/.npmrc", "registry=https://npm.corp.invalid/\n")
        with patch.object(
            verify_packages, "check_registry", side_effect=AssertionError("network called")
        ):
            report = self.verify(inventory)
        self.assertTrue(all(r["status"] == "unresolved" for r in report["results"]))
        self.assertIn("npm.corp.invalid", report["results"][0]["reason"])

    def test_configured_public_mirror_becomes_query_base(self):
        """A pip.conf that points at a known public mirror is used for checks, not treated as private."""
        relative = "home/pip/pip.ini" if WINDOWS else "home/.config/pip/pip.conf"
        self.write(
            relative,
            "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple\n",
        )
        self.write("requirements.txt", "requests\n")
        inventory = read_dependencies(self.root, "python")
        with patch.object(
            verify_packages, "check_registry", return_value=("registry_match", "exists")
        ) as checker:
            report = self.verify(inventory)
        checker.assert_called_once_with(
            "requests", "python", 10, "https://pypi.tuna.tsinghua.edu.cn/simple"
        )
        self.assertEqual(report["registry"]["selected_by"], "~/" + relative.removeprefix("home/"))
        self.assertEqual(report["status"], "completed")

    def test_windows_pip_ini_paths_and_actual_prefix(self):
        """Windows global, legacy, roaming and actual-interpreter site files have ordered precedence."""
        home, prefix = self.root / "home", self.root / "prefix"
        files = [
            self.write("ProgramData/pip/pip.ini", "[global]\nindex-url=https://global.corp.invalid/simple\n"),
            self.write("home/pip/pip.ini", "[global]\nindex-url=https://legacy.corp.invalid/simple\n"),
            self.write("AppData/pip/pip.ini", "[global]\nindex-url=https://pypi.tuna.tsinghua.edu.cn/simple\n"),
            self.write("prefix/pip.ini", "[global]\nindex-url=https://pypi.org/simple\n"),
        ]
        environ = {"PROGRAMDATA": str(self.root / "ProgramData"), "APPDATA": str(self.root / "AppData")}
        with patch.object(verify_packages, "SYSTEM_PIP_CONFIGS", None):
            entries = verify_packages.pip_entries(environ, home, platform="win32", prefix=prefix)
        self.assertEqual(
            {entry["origin"] for entry in entries},
            {verify_packages.display_path(path, home) for path in files},
        )
        active = [entry for entry in entries if entry["active"]]
        self.assertEqual([(entry["origin"], entry["public"]) for entry in active], [(str(files[-1]), True)])
        self.write("other-venv/pip.ini", "[global]\nindex-url=https://other.corp.invalid/simple\n")
        with patch.object(verify_packages, "SYSTEM_PIP_CONFIGS", ()):
            mismatch = verify_packages.pip_entries(
                {**environ, "VIRTUAL_ENV": str(self.root / "other-venv")}, home,
                platform="win32", prefix=prefix,
            )
        self.assertTrue(any(entry["option"] == "interpreter-mismatch" and entry["active"] for entry in mismatch))
        self.assertFalse(any("other.corp.invalid" == entry["host"] for entry in mismatch))

    def test_pip_explicit_config_skips_user_and_devnull_skips_files(self):
        """An existing PIP_CONFIG_FILE suppresses user files; devnull suppresses every file."""
        home, prefix = self.root / "home", self.root / "prefix"
        self.write("home/pip/pip.ini", "[global]\nindex-url=https://legacy.corp.invalid/simple\n")
        self.write("AppData/pip/pip.ini", "[global]\nindex-url=https://roaming.corp.invalid/simple\n")
        site = self.write("prefix/pip.ini", "[global]\nindex-url=https://site.corp.invalid/simple\n")
        explicit = self.write("explicit.ini", "[global]\nindex-url=https://pypi.org/simple\n")
        environ = {"APPDATA": str(self.root / "AppData"), "PIP_CONFIG_FILE": str(explicit)}
        with patch.object(verify_packages, "SYSTEM_PIP_CONFIGS", ()):
            entries = verify_packages.pip_entries(environ, home, platform="win32", prefix=prefix)
            self.assertEqual({entry["origin"] for entry in entries}, {str(site), str(explicit)})
            self.assertEqual([entry["origin"] for entry in entries if entry["active"]], [str(explicit)])
            for null in (os.devnull, "NUL"):
                with self.subTest(null=null):
                    entries = verify_packages.pip_entries(
                        {**environ, "PIP_CONFIG_FILE": null, "PIP_INDEX_URL": "https://pypi.org/simple"},
                        home, platform="win32", prefix=prefix,
                    )
                    self.assertEqual([(entry["origin"], entry["active"]) for entry in entries], [("$PIP_INDEX_URL", True)])

    def test_overridden_private_pip_index_does_not_block_public_check(self):
        """A replaced private index stays in provenance but cannot veto the effective public index."""
        relative = "home/pip/pip.ini" if WINDOWS else "home/.config/pip/pip.conf"
        self.write(relative, "[global]\nindex-url=https://retired.corp.invalid/simple\n")
        self.write("requirements.txt", "requests\n")
        inventory = read_dependencies(self.root, "python")
        with patch.object(verify_packages, "check_registry", return_value=("registry_match", "exists")) as checker:
            report = self.verify(inventory, environ={"PIP_INDEX_URL": "https://pypi.org/simple"})
        self.assertEqual(report["status"], "completed")
        checker.assert_called_once_with("requests", "python", 10, "https://pypi.org/simple")
        retired = [entry for entry in report["registry"]["configured"] if entry["host"] == "retired.corp.invalid"]
        self.assertEqual(len(retired), 1)
        self.assertFalse(retired[0]["active"])

    def test_private_extra_index_and_command_ambiguity_remain_unresolved(self):
        """An active private extra index or differing command profile prevents a public verdict."""
        self.write("requirements.txt", "requests\n")
        inventory = read_dependencies(self.root, "python")
        with patch.object(verify_packages, "check_registry", side_effect=AssertionError("network called")):
            report = self.verify(inventory, environ={
                "PIP_INDEX_URL": "https://pypi.org/simple",
                "PIP_EXTRA_INDEX_URL": "https://active.corp.invalid/simple",
            })
        self.assertEqual(report["results"][0]["status"], "unresolved")
        self.assertIn("active.corp.invalid", report["results"][0]["reason"])
        config = self.write(
            "command-profiles.ini", "[install]\nindex-url=https://pypi.org/simple\n"
            "[download]\nindex-url=https://pypi.tuna.tsinghua.edu.cn/simple\n",
        )
        with patch.object(verify_packages, "check_registry", side_effect=AssertionError("network called")):
            report = self.verify(inventory, environ={"PIP_CONFIG_FILE": str(config)})
        self.assertEqual(report["results"][0]["status"], "unresolved")
        self.assertTrue(any(entry["active"] and entry["option"] == "ambiguous" for entry in report["registry"]["configured"]))

    def test_pip_config_bom_and_invalid_bytes_have_explicit_results(self):
        """Supported UTF-8 BOM configs work, while damaged configs remain unresolved and visible."""
        self.write("requirements.txt", "requests\n")
        inventory = read_dependencies(self.root, "python")
        config = self.root / "configured.ini"
        config.write_bytes(b"\xef\xbb\xbf[global]\n# UTF-8 BOM\nindex-url=https://pypi.org/simple\n")
        with patch.object(verify_packages, "check_registry", return_value=("registry_match", "exists")):
            report = self.verify(inventory, environ={"PIP_CONFIG_FILE": str(config)})
        self.assertEqual(report["status"], "completed")
        config.write_bytes(b"[global]\nindex-url=https://pypi.org/simple\n# invalid byte \xff\n")
        with patch.object(verify_packages.locale, "getpreferredencoding", return_value="utf-8"), patch.object(
            verify_packages, "check_registry", side_effect=AssertionError("network called")
        ):
            report = self.verify(inventory, environ={"PIP_CONFIG_FILE": str(config)})
        self.assertEqual((report["status"], report["results"][0]["status"]), ("incomplete", "unresolved"))
        self.assertTrue(any(entry["option"] == "unparsed" and entry["active"] for entry in report["registry"]["configured"]))

    def test_pip_config_codec_follows_utf8_mode_and_locale(self):
        """Native locale bytes and UTF-8 mode retain their distinct strict decoding contracts."""
        config = self.root / "encoded-pip.ini"
        cases = (
            (0, "cp1252", "cp1252", "café"),
            (0, "gbk", "gbk", "中文"),
            (1, "cp1252", "utf-8", "中文"),
            (1, "gbk", "utf-8", "café"),
            (0, "cp1252", "utf-8-sig", "中文"),
            (0, "gbk", "utf-8-sig", "café"),
        )
        for utf8_mode, locale_encoding, file_encoding, label in cases:
            with self.subTest(utf8_mode=utf8_mode, locale=locale_encoding, file_encoding=file_encoding):
                text = f"[global]\n# {label}\nindex-url=https://pypi.org/simple\n"
                config.write_bytes(text.encode(file_encoding))
                with patch.object(verify_packages.sys, "flags", SimpleNamespace(utf8_mode=utf8_mode)), patch.object(
                    verify_packages.locale, "getpreferredencoding", return_value=locale_encoding
                ):
                    self.assertEqual(verify_packages.read_pip_config(config), text)
        config.write_bytes("[global]\n# café\n".encode("cp1252"))
        with patch.object(verify_packages.sys, "flags", SimpleNamespace(utf8_mode=1)), patch.object(
            verify_packages.locale, "getpreferredencoding", return_value="cp1252"
        ):
            with self.assertRaises(UnicodeDecodeError):
                verify_packages.read_pip_config(config)

    def test_cargo_mirror_replacement_is_public(self):
        """A crates-io replacement pointing at a known sparse mirror keeps names checkable."""
        self.write("Cargo.toml", '[package]\nname="x"\nversion="0.1.0"\n[dependencies]\nserde="1"\n')
        self.write(
            ".cargo/config.toml",
            '[source.crates-io]\nreplace-with="mirror"\n[source.mirror]\nregistry="sparse+https://rsproxy.cn/index/"\n',
        )
        inventory = read_dependencies(self.root, "rust")
        with patch.object(
            verify_packages, "check_registry", return_value=("registry_match", "exists")
        ) as checker:
            report = self.verify(inventory)
        checker.assert_called_once_with("serde", "rust", 10, "https://rsproxy.cn/index")
        self.assertEqual(report["status"], "completed")
        self.write(
            ".cargo/config.toml",
            '[source.crates-io]\nreplace-with="corp"\n[source.corp]\nregistry="https://git.corp.invalid/index"\n',
        )
        with patch.object(
            verify_packages, "check_registry", side_effect=AssertionError("network called")
        ):
            report = self.verify(inventory)
        self.assertEqual(report["results"][0]["status"], "unresolved")

    def test_mirror_absence_requires_canary_semantics(self):
        """A mirror that answers 404 for everything must not turn names into missing packages."""
        self.write("requirements.txt", "requests\n")
        inventory = read_dependencies(self.root, "python")
        absent = ("not_found", "name absent from mirror; not proof of hallucination")
        with patch.object(verify_packages, "check_registry", return_value=absent) as checker:
            report = self.verify(inventory, public_registry=True, mirror="cn")
        self.assertEqual(checker.call_args_list[0].args[3], verify_packages.MIRRORS["cn"]["python"])
        self.assertEqual((report["status"], report["results"][0]["status"]), ("incomplete", "unresolved"))

        def healthy(name, lang, timeout, base):
            """Answer like a healthy mirror: the canary exists and other names are absent."""
            return ("registry_match", "exists") if name == "pip" else absent

        with patch.object(verify_packages, "check_registry", side_effect=healthy):
            report = self.verify(inventory, public_registry=True, mirror="cn")
        self.assertEqual((report["status"], report["results"][0]["status"]), ("incomplete", "mirror_not_found"))
        self.assertIn("mirrors can lag", report["results"][0]["reason"])

    def test_registry_paths_and_urls(self):
        """Index paths and per-name URLs must follow each registry's documented layout."""
        for name, expected in {"a": "1/a", "ab": "2/ab", "syn": "3/s/syn", "Serde_JSON": "se/rd/serde_json"}.items():
            self.assertEqual(verify_packages.crate_index_path(name), expected)
        self.assertEqual(
            verify_packages.registry_url("My_Pkg.x", "python", "https://pypi.org/simple/"),
            "https://pypi.org/simple/my-pkg-x/",
        )
        self.assertEqual(
            verify_packages.registry_url("@types/node", "javascript", "https://registry.npmmirror.com"),
            "https://registry.npmmirror.com/@types%2Fnode",
        )

    def test_head_rejection_falls_back_to_get(self):
        """Registries without HEAD support must still answer through GET."""
        rejected = urllib.error.HTTPError("https://example.invalid", 405, "no HEAD", {}, None)
        with patch("urllib.request.urlopen", side_effect=[rejected, FakeResponse(200)]) as opener:
            status, _ = verify_packages.check_registry("requests", "python")
        self.assertEqual(status, "registry_match")
        self.assertEqual([call.args[0].get_method() for call in opener.call_args_list], ["HEAD", "GET"])

    def test_network_error_names_host_and_proxy_without_credentials(self):
        """Network failures must name the host and proxy without revealing proxy passwords."""
        error = urllib.error.URLError(TimeoutError("timed out"))
        with patch(
            "urllib.request.getproxies", return_value={"https": "http://user:secret@127.0.0.1:7890"}
        ), patch("urllib.request.proxy_bypass", return_value=False), patch(
            "urllib.request.urlopen", side_effect=error
        ):
            status, reason = verify_packages.check_registry("requests", "python", 2)
        self.assertEqual(status, "error")
        self.assertIn("pypi.org via proxy 127.0.0.1:7890", reason)
        self.assertIn("timed out after 2s", reason)
        self.assertNotIn("secret", reason)

    def test_registry_base_rejects_credentials(self):
        """A registry base with embedded credentials must be refused before any request."""
        result = self.run_plain(
            "verify_packages.py", "--registry-base", "https://user:pw@mirror.invalid/simple"
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("must not contain credentials", result.stderr)

if __name__ == "__main__":
    unittest.main(verbosity=2)

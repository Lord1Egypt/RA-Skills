#!/usr/bin/env python3
"""Run CloudArc benchmark profiles and validate remote-search telemetry."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path.cwd()


class HelperError(RuntimeError):
    """Raised when the helper cannot produce a trustworthy result."""


def _repo_path(value: str | None) -> Path:
    path = Path(value or DEFAULT_REPO).expanduser().resolve()
    if not path.is_dir():
        raise HelperError(f"repository directory does not exist: {path}")
    return path


def _python_executable(value: str | None) -> str:
    executable = value or sys.executable
    if not executable:
        raise HelperError("python executable is not available")
    return executable


def _run(command: list[str], *, cwd: Path) -> int:
    print("+ " + " ".join(_display_arg(item) for item in command))
    completed = subprocess.run(command, cwd=cwd, check=False)
    return completed.returncode


def _load_result(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HelperError(f"benchmark JSON artifact is missing: {path}") from exc
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HelperError(f"benchmark JSON artifact is invalid: {path}") from exc
    if not isinstance(payload, dict):
        raise HelperError(f"benchmark JSON artifact must be an object: {path}")
    return payload


def _validate_markdown(path: Path, *, heading: str) -> None:
    try:
        payload = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise HelperError(f"benchmark Markdown artifact is unreadable: {path}") from exc
    if not payload.startswith(heading):
        raise HelperError(f"benchmark Markdown heading is invalid: {path}")
    if "PASS" not in payload:
        raise HelperError(f"benchmark Markdown does not report PASS: {path}")


def validate_benchmark_artifacts(
    json_path: Path,
    markdown_path: Path,
    *,
    profile: str,
) -> dict:
    result = _load_result(json_path)
    evaluation = result.get("evaluation")
    if not isinstance(evaluation, dict) or evaluation.get("pass") is not True:
        raise HelperError(f"benchmark artifact does not pass its SLO: {json_path}")
    if profile == "multi-file-dedup":
        if result.get("status") != "ok" or result.get("profile") != profile:
            raise HelperError(f"multi-file benchmark identity is invalid: {json_path}")
        file_count = result.get("file_count")
        manifest_entries = result.get("manifest_entry_count")
        index_documents = result.get("index_document_count")
        if (
            isinstance(file_count, bool)
            or not isinstance(file_count, int)
            or file_count <= 0
            or isinstance(manifest_entries, bool)
            or not isinstance(manifest_entries, int)
            or isinstance(index_documents, bool)
            or not isinstance(index_documents, int)
        ):
            raise HelperError(
                f"multi-file benchmark cardinality is inconsistent: {json_path}"
            )
        # Since 1.4.0 the manifest carries one entry per file *and* one per
        # directory (the input root included), while the search index holds the
        # files only. Verify both sides against the reported kinds instead of
        # demanding manifest entries == files, which is no longer true.
        kinds = result.get("kinds")
        if isinstance(kinds, dict) and kinds:
            counted = sum(
                int(value) for value in kinds.values() if isinstance(value, int)
            )
            if int(kinds.get("file", 0)) != file_count or counted != manifest_entries:
                raise HelperError(
                    f"multi-file benchmark manifest cardinality is inconsistent: {json_path}"
                )
        elif manifest_entries != file_count:
            raise HelperError(
                f"multi-file benchmark manifest cardinality is inconsistent: {json_path}"
            )
        if index_documents != file_count:
            raise HelperError(
                f"multi-file benchmark index cardinality is inconsistent: {json_path}"
            )
        heading = "# CloudArc Multi-File Benchmark"
    else:
        if (
            result.get("schema") != "cloudarc.large-package-benchmark"
            or result.get("completion_status") != "complete"
        ):
            raise HelperError(f"payload benchmark identity is invalid: {json_path}")
        runs = result.get("runs")
        if not isinstance(runs, list) or not runs or any(
            not isinstance(run, dict) or run.get("status") != "ok" for run in runs
        ):
            raise HelperError(f"payload benchmark runs are incomplete: {json_path}")
        heading = "# CloudArc Large-Package Benchmark"
    _validate_markdown(markdown_path, heading=heading)
    return {
        "profile": profile,
        "json": str(json_path),
        "markdown": str(markdown_path),
        "pass": True,
    }


def _display_arg(value: str) -> str:
    if any(char.isspace() for char in value):
        return repr(value)
    return value


def _benchmark_command(
    python: str,
    *,
    sizes: list[str] | None = None,
    sizes_mib: list[str] | None = None,
    multi_file: bool = False,
    file_count: int = 512,
    file_size_kib: int = 64,
    duplicate_groups: int = 16,
    json_output: Path,
    markdown_output: Path,
) -> list[str]:
    command = [python, "-B", "-m", "benchmarks.large_package"]
    if multi_file:
        command.extend(
            [
                "--multi-file",
                "--file-count",
                str(file_count),
                "--file-size-kib",
                str(file_size_kib),
                "--duplicate-groups",
                str(duplicate_groups),
            ]
        )
    elif sizes_mib:
        command.extend(["--sizes-mib", *sizes_mib])
    else:
        command.extend(["--sizes-gib", *(sizes or ["1", "5", "10"])])
    command.extend(
        [
            "--json-output",
            str(json_output),
            "--markdown-output",
            str(markdown_output),
            "--fail-on-slo",
        ]
    )
    return command


def run_smoke(args: argparse.Namespace) -> int:
    repo = _repo_path(args.repo)
    python = _python_executable(args.python)
    commands = [
        [
            python,
            "-B",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v",
        ],
        _benchmark_command(
            python,
            sizes_mib=[str(args.size_mib)],
            json_output=repo / args.json_output,
            markdown_output=repo / args.markdown_output,
        ),
        _benchmark_command(
            python,
            multi_file=True,
            file_count=args.file_count,
            file_size_kib=args.file_size_kib,
            duplicate_groups=args.duplicate_groups,
            json_output=repo / args.multi_json_output,
            markdown_output=repo / args.multi_markdown_output,
        ),
    ]
    for command in commands:
        if _run(command, cwd=repo) != 0:
            return 2
    artifacts = [
        validate_benchmark_artifacts(
            repo / args.json_output,
            repo / args.markdown_output,
            profile="compressible-text",
        ),
        validate_benchmark_artifacts(
            repo / args.multi_json_output,
            repo / args.multi_markdown_output,
            profile="multi-file-dedup",
        ),
    ]
    print(json.dumps({"artifacts": artifacts}, indent=2))
    return 0


def run_manual(args: argparse.Namespace) -> int:
    if not args.yes:
        raise HelperError(
            "manual 1/5/10 GiB execution requires --yes because it can "
            "consume hours and large temporary disk"
        )
    repo = _repo_path(args.repo)
    python = _python_executable(args.python)
    command = _benchmark_command(
        python,
        sizes=[str(value) for value in args.sizes_gib],
        json_output=repo / args.json_output,
        markdown_output=repo / args.markdown_output,
    )
    if _run(command, cwd=repo) != 0:
        return 2
    multi_command = _benchmark_command(
        python,
        multi_file=True,
        file_count=args.file_count,
        file_size_kib=args.file_size_kib,
        duplicate_groups=args.duplicate_groups,
        json_output=repo / args.multi_json_output,
        markdown_output=repo / args.multi_markdown_output,
    )
    if _run(multi_command, cwd=repo) != 0:
        return 2
    artifacts = [
        validate_benchmark_artifacts(
            repo / args.json_output,
            repo / args.markdown_output,
            profile="compressible-text",
        ),
        validate_benchmark_artifacts(
            repo / args.multi_json_output,
            repo / args.multi_markdown_output,
            profile="multi-file-dedup",
        ),
    ]
    print(json.dumps({"artifacts": artifacts}, indent=2))
    return 0


def _read_json(path: str) -> Any:
    payload = sys.stdin.read() if path == "-" else Path(path).read_text(
        encoding="utf-8"
    )
    try:
        return json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HelperError(f"invalid JSON telemetry input: {path}") from exc


def _nonnegative_int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise HelperError(f"telemetry field {field} must be a non-negative integer")
    return value


def validate_telemetry(payload: Any, *, expected: str) -> dict:
    if not isinstance(payload, dict):
        raise HelperError("telemetry input must be a JSON object")
    telemetry = payload.get("telemetry", payload)
    if not isinstance(telemetry, dict):
        raise HelperError("telemetry object is missing")
    required = {
        "range_requests",
        "range_bytes",
        "sidecar_reads",
        "sidecar_bytes",
        "peak_rss_bytes",
        "rss_source",
        "data_section_read",
    }
    missing = sorted(required.difference(telemetry))
    if missing:
        raise HelperError("telemetry fields are missing: " + ", ".join(missing))
    values = {
        field: _nonnegative_int(telemetry[field], field)
        for field in (
            "range_requests",
            "range_bytes",
            "sidecar_reads",
            "sidecar_bytes",
            "peak_rss_bytes",
        )
    }
    if not isinstance(telemetry["rss_source"], str) or not telemetry["rss_source"]:
        raise HelperError("telemetry rss_source must be a non-empty string")
    if values["peak_rss_bytes"] <= 0:
        raise HelperError("telemetry peak_rss_bytes must be positive")
    if telemetry["data_section_read"] is not False:
        raise HelperError("data_section_read must be false")
    if values["range_requests"] == 0 and values["range_bytes"] != 0:
        raise HelperError("range_bytes must be zero when range_requests is zero")
    if values["range_requests"] > 0 and values["range_bytes"] <= 0:
        raise HelperError("range_bytes must be positive when ranges were read")
    if values["sidecar_reads"] == 0 and values["sidecar_bytes"] != 0:
        raise HelperError("sidecar_bytes must be zero when sidecar_reads is zero")
    if values["sidecar_reads"] > 0 and values["sidecar_bytes"] <= 0:
        raise HelperError("sidecar_bytes must be positive when sidecars were read")
    if expected == "range" and values["range_requests"] != 3:
        raise HelperError("embedded metadata must use exactly three range requests")
    if expected == "sidecar":
        if values["range_requests"] != 0 or values["sidecar_reads"] != 2:
            raise HelperError(
                "sidecar fallback must use zero ranges and two sidecar reads"
            )
    return {
        "valid": True,
        "expected": expected,
        **values,
        "rss_source": telemetry["rss_source"],
        "data_section_read": False,
    }


def check_telemetry(args: argparse.Namespace) -> int:
    for path in args.input:
        result = validate_telemetry(_read_json(path), expected=args.expected)
        print(json.dumps({"input": path, **result}, indent=2))
    return 0


def _probe_zstandard() -> tuple[bool, str]:
    try:
        # Optional dependency: resolve it lazily so the skill never hard-imports
        # a package it does not ship.
        module = importlib.import_module("zstandard")
        return True, str(getattr(module, "__version__", "unknown"))
    except Exception:
        return False, "not installed"


def _probe_proc_status() -> tuple[bool, str]:
    try:
        text = Path(f"/proc/{os.getpid()}/status").read_text(encoding="ascii")
    except Exception as exc:  # noqa: BLE001 - diagnostics must never crash
        return False, f"unreadable ({type(exc).__name__})"
    if "VmRSS" in text:
        return True, "VmRSS present (linux-proc-status)"
    return False, "no VmRSS line"


def _package_version(repo: Path) -> str:
    try:
        import tomllib

        data = tomllib.loads((repo / "pyproject.toml").read_text(encoding="utf-8"))
        version = (data.get("project") or {}).get("version")
        if isinstance(version, str) and version:
            return version
    except Exception:
        pass
    try:
        return (repo / "skills" / "cloudarc-bounded-memory-benchmark"
                / "VERSION").read_text(encoding="utf-8").strip()
    except Exception:
        return "unknown"


def _probe_repo(repo: Path) -> list[tuple[str, bool]]:
    return [
        ("core/packer.py", (repo / "core" / "packer.py").is_file()),
        ("benchmarks/large_package.py", (repo / "benchmarks" / "large_package.py").is_file()),
        ("tests/", (repo / "tests").is_dir()),
    ]


def _doctor_lines(repo: Path, python: str) -> tuple[list[str], bool]:
    has_zstd, zstd_version = _probe_zstandard()
    proc_ok, proc_note = _probe_proc_status()
    checks = _probe_repo(repo)
    ready = all(ok for _, ok in checks)
    lines = [
        "CloudArc doctor",
        f"  python          {sys.version.split()[0]} ({python})",
        f"  repository      {repo} (package {_package_version(repo)})",
        f"  zstandard       {zstd_version}"
        + ("  -> text payloads use zstd" if has_zstd else "  -> text payloads use deflate"),
        f"  /proc VmRSS     {proc_note}",
    ]
    for name, ok in checks:
        lines.append(f"  {'ok ' if ok else 'NO '} {name}")
    if ready:
        lines.append("  verdict         READY - smoke, selfcheck and manual can run")
    else:
        lines.append("  verdict         NOT READY - benchmark modules are missing")
        lines.append("                  clone the CloudArc repository and pass --repo <path>")
    return lines, ready


def run_doctor(args: argparse.Namespace) -> int:
    repo = _repo_path(args.repo)
    lines, ready = _doctor_lines(repo, _python_executable(args.python))
    print("\n".join(lines))
    return 0 if ready else 1


def render_slo_badge(payload: dict) -> str:
    """Render a flat shields-style SVG from one benchmark result object."""

    slo = payload.get("slo") or {}
    runs = payload.get("runs") or []
    first = runs[0] if runs and isinstance(runs[0], dict) else {}
    peak = 0
    for op in ("pack", "unpack"):
        section = first.get(op) or {}
        peak = max(peak, int(section.get("peak_rss_bytes") or 0))
    if not peak:
        peak = int(first.get("peak_rss_bytes") or 0)
    limit = int(slo.get("peak_rss_bytes_max") or 0)
    passed = bool((payload.get("evaluation") or {}).get("pass"))
    if not runs:
        state, colour = "no data", "#5f6368"
    elif passed:
        state, colour = "PASS", "#2f7d32"
    else:
        state, colour = "FAIL", "#b3261e"
    mib = 1024 * 1024
    value = f"{state}"
    if peak and limit:
        value = f"{state} · {peak / mib:.1f} / {limit / mib:.0f} MiB"
    elif peak:
        value = f"{state} · {peak / mib:.1f} MiB"
    label, value_text = "CloudArc SLO", value
    char = 6.6
    label_w = int(len(label) * char) + 16
    value_w = int(len(value_text) * char) + 16
    total = label_w + value_w
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="20" '
        f'role="img" aria-label="{label}: {value_text}">'
        f'<rect width="{label_w}" height="20" fill="#3c4043"/>'
        f'<rect x="{label_w}" width="{value_w}" height="20" fill="{colour}"/>'
        f'<g fill="#fff" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" '
        f'font-size="11">'
        f'<text x="{label_w / 2:.0f}" y="14" text-anchor="middle">{label}</text>'
        f'<text x="{label_w + value_w / 2:.0f}" y="14" text-anchor="middle">'
        f"{value_text}</text></g></svg>\n"
    )


def run_badge(args: argparse.Namespace) -> int:
    payload = _load_result(Path(args.input))
    svg = render_slo_badge(payload)
    if args.output == "-":
        sys.stdout.write(svg)
        return 0
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(svg, encoding="utf-8")
    print(f"badge written: {target}")
    return 0


def run_selfcheck(args: argparse.Namespace) -> int:
    """One-command 'hello world': tiny pack/unpack run with real RSS numbers."""

    repo = _repo_path(args.repo)
    python = _python_executable(args.python)
    lines, ready = _doctor_lines(repo, python)
    if not ready:
        print("\n".join(lines), file=sys.stderr)
        print("error: selfcheck needs the CloudArc repository (see doctor above)", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory() as temp:
        json_path = Path(temp) / "selfcheck.json"
        md_path = Path(temp) / "selfcheck.md"
        rc = _run(
            [python, "-B", "-m", "benchmarks.large_package",
             "--sizes-mib", str(args.size_mib),
             "--json-output", str(json_path),
             "--markdown-output", str(md_path),
             "--fail-on-slo"],
            cwd=repo,
        )
        payload = _load_result(json_path) if json_path.exists() else {}
    first = ((payload.get("runs") or [{}])[0])
    mib = 1024 * 1024
    print("")
    print(f"selfcheck: {args.size_mib} MiB pack/unpack with the CloudArc reference backend")
    for op in ("pack", "unpack"):
        section = first.get(op) or {}
        peak = int(section.get("peak_rss_bytes") or 0)
        wall = float(section.get("wall_seconds") or 0)
        print(f"  {op:<7} {wall:6.2f} s   peak RSS {peak / mib:6.1f} MiB")
    passed = bool((payload.get("evaluation") or {}).get("pass"))
    limit = int((payload.get("slo") or {}).get("peak_rss_bytes_max") or 0)
    print(f"  SLO     {'PASS' if passed else 'FAIL'} (limit {limit / mib:.0f} MiB)")
    return 0 if (rc == 0 and passed) else 1


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--repo",
        default=None,
        help="CloudArc repository root; defaults to the current directory",
    )
    parser.add_argument(
        "--python",
        default=None,
        help="Python executable; defaults to the current interpreter",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CloudArc benchmark and remote-search telemetry helper"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    smoke = subparsers.add_parser("smoke", help="run tests and small benchmarks")
    _add_common(smoke)
    smoke.add_argument("--size-mib", type=int, default=64)
    smoke.add_argument("--file-count", type=int, default=512)
    smoke.add_argument("--file-size-kib", type=int, default=16)
    smoke.add_argument("--duplicate-groups", type=int, default=32)
    smoke.add_argument(
        "--json-output",
        default="benchmarks/results/helper-smoke.json",
    )
    smoke.add_argument(
        "--markdown-output",
        default="docs/LARGE_PACKAGE_BENCHMARK_HELPER_SMOKE.md",
    )
    smoke.add_argument(
        "--multi-json-output",
        default="benchmarks/results/helper-multi-file.json",
    )
    smoke.add_argument(
        "--multi-markdown-output",
        default="docs/MULTI_FILE_BENCHMARK_HELPER.md",
    )
    smoke.set_defaults(handler=run_smoke)

    manual = subparsers.add_parser(
        "manual",
        help="run the explicit large benchmark and multi-file profile",
    )
    _add_common(manual)
    manual.add_argument("--yes", action="store_true")
    manual.add_argument("--sizes-gib", nargs="+", type=float, default=[1, 5, 10])
    manual.add_argument("--file-count", type=int, default=5000)
    manual.add_argument("--file-size-kib", type=int, default=64)
    manual.add_argument("--duplicate-groups", type=int, default=256)
    manual.add_argument(
        "--json-output",
        default="benchmarks/results/large-package-helper-manual.json",
    )
    manual.add_argument(
        "--markdown-output",
        default="docs/LARGE_PACKAGE_BENCHMARK_HELPER_MANUAL.md",
    )
    manual.add_argument(
        "--multi-json-output",
        default="benchmarks/results/multi-file-helper-manual.json",
    )
    manual.add_argument(
        "--multi-markdown-output",
        default="docs/MULTI_FILE_BENCHMARK_HELPER_MANUAL.md",
    )
    manual.set_defaults(handler=run_manual)

    telemetry = subparsers.add_parser(
        "check-telemetry",
        help="validate one or more remote-search JSON responses",
    )
    telemetry.add_argument(
        "--input",
        action="append",
        required=True,
        help="response JSON path, or '-' for stdin",
    )
    telemetry.add_argument(
        "--expected",
        choices=("any", "range", "sidecar"),
        default="any",
    )
    telemetry.set_defaults(handler=check_telemetry)
    doctor = subparsers.add_parser(
        "doctor",
        help="report the environment and whether the CloudArc repository is usable",
    )
    _add_common(doctor)
    doctor.set_defaults(handler=run_doctor)

    selfcheck = subparsers.add_parser(
        "selfcheck",
        help="run a tiny pack/unpack and print real RSS numbers (needs the repository)",
    )
    _add_common(selfcheck)
    selfcheck.add_argument("--size-mib", type=int, default=2)
    selfcheck.set_defaults(handler=run_selfcheck)

    badge = subparsers.add_parser(
        "badge",
        help="render a flat SVG SLO badge from a benchmark JSON artifact",
    )
    badge.add_argument("--input", required=True)
    badge.add_argument("--output", default="-", help="'-' writes the SVG to stdout")
    badge.set_defaults(handler=run_badge)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except (HelperError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

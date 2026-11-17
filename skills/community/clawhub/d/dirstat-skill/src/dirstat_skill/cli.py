from __future__ import annotations

import argparse
import csv
import json
import platform
import subprocess
from pathlib import Path

from dirstat_skill.config import load_settings
from dirstat_skill.engine_ncdu import build_ncdu_export_command, detect_ncdu
from dirstat_skill.engine_windows import build_windows_export_for_targets
from dirstat_skill.logging_utils import configure_run_logger
from dirstat_skill.reporting import (
    build_analysis_findings,
    build_top_lists,
    render_review_report,
    select_dominant_candidates_for_roots,
    write_review_candidates_csv,
)
from dirstat_skill.raw_export import parse_export
from dirstat_skill.targets import normalize_targets


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="DirStat_Skill")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan")
    scan.add_argument("--path", action="append", dest="paths", required=True)
    scan.add_argument("--output-dir", required=True)
    scan.add_argument("--engine", default=None)
    scan.add_argument("--config", default="config/defaults.json")

    summarize = subparsers.add_parser("summarize-export")
    summarize.add_argument("--export", required=True)
    summarize.add_argument("--output-dir", required=True)
    summarize.add_argument("--config", required=True)
    summarize.add_argument("--dominant-percent", type=float, default=None)

    audit = subparsers.add_parser("audit")
    audit.add_argument("--path", action="append", dest="paths", required=True)
    audit.add_argument("--output-dir", required=True)
    audit.add_argument("--engine", default=None)
    audit.add_argument("--config", default="config/defaults.json")
    audit.add_argument("--dominant-percent", type=float, default=None)

    args = parser.parse_args(argv)
    if args.command == "scan":
        return _scan(
            paths=list(args.paths),
            output_dir=Path(args.output_dir),
            config_path=Path(args.config),
            requested_engine=args.engine,
        )
    if args.command == "summarize-export":
        return _summarize_export(
            export_path=Path(args.export),
            output_dir=Path(args.output_dir),
            config_path=Path(args.config),
            dominant_percent_override=args.dominant_percent,
        )
    if args.command == "audit":
        return _audit(
            paths=list(args.paths),
            output_dir=Path(args.output_dir),
            config_path=Path(args.config),
            requested_engine=args.engine,
            dominant_percent_override=args.dominant_percent,
        )
    return 2


def _summarize_export(
    export_path: Path,
    output_dir: Path,
    config_path: Path,
    dominant_percent_override: float | None = None,
) -> int:
    env_overrides = {}
    if dominant_percent_override is not None:
        env_overrides["DOMINANT_PERCENT"] = str(dominant_percent_override)
    settings = load_settings(config_path=config_path, env_overrides=env_overrides or None)
    parsed = parse_export(export_path)
    top_lists = build_top_lists(
        parsed.nodes,
        min_bytes=settings.min_bytes,
        top_n=settings.top_n,
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    selected_nodes = select_dominant_candidates_for_roots(
        nodes=parsed.nodes,
        dominant_percent=settings.dominant_percent,
        min_candidate_bytes=settings.min_candidate_bytes,
    )
    findings = build_analysis_findings(
        selected_nodes=selected_nodes,
        all_nodes=parsed.nodes,
        protected_prefixes=settings.risk_do_not_touch_prefixes
        + settings.windows_do_not_touch_prefixes,
        inspection_prefixes=settings.risk_needs_inspection_prefixes,
        nearby_reference_extensions=settings.nearby_reference_extensions,
        max_nearby_reference_files=settings.max_nearby_reference_files,
        dominant_percent=settings.dominant_percent,
        min_candidate_bytes=settings.min_candidate_bytes,
    )

    (output_dir / "summary.md").write_text(
        "# Audit Summary\n\n"
        f"- root: `{parsed.root_path}`\n"
        f"- top_dirs: {len(top_lists.top_dirs)}\n"
        f"- top_files: {len(top_lists.top_files)}\n",
        encoding="utf-8",
    )

    with (output_dir / "top_dirs.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "dsize"])
        writer.writeheader()
        for node in top_lists.top_dirs:
            writer.writerow({"path": node.path, "dsize": node.dsize})

    with (output_dir / "top_files.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "dsize"])
        writer.writeheader()
        for node in top_lists.top_files:
            writer.writerow({"path": node.path, "dsize": node.dsize})

    (output_dir / "candidates.json").write_text(
        json.dumps([finding.__dict__ for finding in findings], indent=2),
        encoding="utf-8",
    )
    write_review_candidates_csv(output_dir / "review_candidates.csv", findings)
    (output_dir / "review_report.md").write_text(
        render_review_report(parsed.root_path, findings),
        encoding="utf-8",
    )
    return 0


def _scan(
    paths: list[str],
    output_dir: Path,
    config_path: Path,
    requested_engine: str | None,
) -> int:
    settings = load_settings(config_path=config_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    logger = configure_run_logger(output_dir / "run.log")
    engine_name = _resolve_engine_name(settings, requested_engine)
    _validate_runtime_contract(engine_name=engine_name, paths=paths)
    platform_name = "windows" if engine_name == "windows-native" else "linux"
    targets = normalize_targets(
        requested_paths=paths,
        auto_discover=False,
        platform_name=platform_name,
    )
    logger.info("scan starting engine=%s targets=%s", engine_name, [item.raw_path for item in targets])

    if engine_name == "windows-native":
        export_path = output_dir / "raw-export.json"
        build_windows_export_for_targets(targets=targets, output_path=export_path)
        logger.info("scan completed export=%s", export_path)
        return 0

    if engine_name == "ncdu":
        if len(targets) != 1:
            raise ValueError("The ncdu engine currently supports one target path at a time")
        engine_info = detect_ncdu()
        if engine_info is None:
            raise RuntimeError("ncdu engine requested but ncdu was not found in PATH")
        export_path = output_dir / "ncdu-export.json"
        command = build_ncdu_export_command(
            binary=engine_info.binary,
            target=targets[0].resolved_path,
            output_path=export_path,
            one_file_system=settings.one_file_system,
            exclude_patterns=settings.exclude_patterns,
        )
        subprocess.run(command, check=True)
        logger.info("scan completed export=%s", export_path)
        return 0

    raise ValueError(f"Unsupported engine: {engine_name}")


def _audit(
    paths: list[str],
    output_dir: Path,
    config_path: Path,
    requested_engine: str | None,
    dominant_percent_override: float | None = None,
) -> int:
    scan_exit_code = _scan(
        paths=paths,
        output_dir=output_dir,
        config_path=config_path,
        requested_engine=requested_engine,
    )
    if scan_exit_code != 0:
        return scan_exit_code

    engine_name = _resolve_engine_name(load_settings(config_path=config_path), requested_engine)
    export_name = "raw-export.json" if engine_name == "windows-native" else "ncdu-export.json"
    return _summarize_export(
        export_path=output_dir / export_name,
        output_dir=output_dir,
        config_path=config_path,
        dominant_percent_override=dominant_percent_override,
    )


def _resolve_engine_name(settings: object, requested_engine: str | None) -> str:
    if requested_engine:
        return requested_engine
    system_name = platform.system().lower()
    if system_name == "windows":
        return settings.default_engine_windows
    return settings.default_engine_linux


def _validate_runtime_contract(engine_name: str, paths: list[str]) -> None:
    system_name = platform.system().lower()
    has_windows_path = any(":\\" in path or path.startswith("\\\\") for path in paths)
    has_linux_path = any(path.startswith("/") for path in paths)

    if engine_name == "windows-native" and system_name != "windows":
        raise ValueError(
            "windows-native can run only on Windows. Run DirStat_Skill on a Windows host, then move only the compact outputs if you need remote review."
        )
    if engine_name == "ncdu" and has_windows_path:
        raise ValueError(
            "Windows-style paths require the Windows runtime. Run DirStat_Skill on Windows for that target."
        )
    if engine_name == "ncdu" and system_name == "windows":
        raise ValueError(
            "ncdu is a Linux engine. Run DirStat_Skill on Linux, or use the native Windows runtime on Windows."
        )
    if engine_name == "windows-native" and has_linux_path:
        raise ValueError(
            "Linux-style paths require a Linux runtime. Run DirStat_Skill on the Linux host that owns that filesystem."
        )


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
"""
Project Scanner for figma-to-mobile skill.

Scans a mobile project (Android, iOS, Flutter, …) to extract existing
resources and custom views, generating a style report that helps
figma-to-mobile reference project resources instead of hardcoding values.

Supports automatic platform detection or explicit --platform override.

Usage:
    python project_scan.py <project_root> [--module <name>] [--output <path>]
    python project_scan.py <project_root> --platform android
    python project_scan.py <project_root> --json

Examples:
    python project_scan.py /path/to/MyApp
    python project_scan.py /path/to/MyApp --module :feature:home
    python project_scan.py /path/to/MyApp --output scan-report.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add parent to path so scanners package is importable
sys.path.insert(0, str(Path(__file__).parent))

from scanners import PLATFORM_REGISTRY, ScanReport
from scanners.base import ProjectScanner


def detect_platform(project_root: Path) -> tuple[str, ProjectScanner] | None:
    """
    Auto-detect which platform a project belongs to.

    Returns (platform_name, scanner_instance) or None if nothing matches.
    """
    for detector, scanner_cls in PLATFORM_REGISTRY:
        if detector.detect(project_root):
            return detector.platform_name(), scanner_cls()
    return None


def get_scanner_by_name(platform: str) -> ProjectScanner | None:
    """Look up a scanner by platform name (e.g. 'android')."""
    for detector, scanner_cls in PLATFORM_REGISTRY:
        if detector.platform_name() == platform:
            return scanner_cls()
    return None


def scan_project(
    project_root: str,
    target_module: str | None = None,
    platform: str | None = None,
    level: str = "full",
) -> dict:
    """
    Scan a project and return a full resource report.

    Detects the platform automatically unless *platform* is given.
    Returns the report as a plain dict (ScanReport.to_dict()).

    Args:
        project_root: Path to the project root.
        target_module: Optional module name to focus on.
        platform: Force a specific platform ('android', 'ios', …).
        level: 'resources' (fast, colors/strings/images only) or 'full' (default).

    Returns:
        Report dict conforming to the ScanReport schema.
    """
    root = Path(project_root)

    # Resolve scanner
    if platform:
        scanner = get_scanner_by_name(platform)
        if scanner is None:
            return ScanReport(
                platform=platform,
                project_root=str(root),
                errors=[f"Unknown platform: {platform}"],
            ).to_dict()
    else:
        result = detect_platform(root)
        if result is None:
            return ScanReport(
                platform="unknown",
                project_root=str(root),
                errors=[
                    f"Could not detect project platform for {project_root}. "
                    "Use --platform to specify explicitly."
                ],
            ).to_dict()
        _, scanner = result

    report = scanner.scan(root, target_module, level=level)
    return report.to_dict()


# ── Backward-compatible helpers ──


def _build_summary(report: dict) -> dict:
    """Build a human-readable summary from a ScanReport dict."""
    modules = report.get("modules", [])
    total_colors = sum(len(m.get("colors", [])) for m in modules)
    total_strings = sum(len(m.get("strings", [])) for m in modules)
    total_dimens = sum(len(m.get("dimens", [])) for m in modules)
    total_styles = sum(len(m.get("styles", [])) for m in modules)
    total_images = sum(len(m.get("images", [])) for m in modules)
    total_views = sum(len(m.get("custom_views", [])) for m in modules)

    return {
        "modules_scanned": len(modules),
        "colors": total_colors,
        "strings": total_strings,
        "dimens": total_dimens,
        "styles": total_styles,
        "drawables": total_images,
        "custom_views": total_views,
        "color_index_size": len(report.get("indices", {}).get("colors", {})),
        "string_index_size": len(report.get("indices", {}).get("strings", {})),
    }


def format_text_report(report: dict) -> str:
    """Format report as human-readable text for terminal output."""
    lines = []
    s = _build_summary(report)

    lines.append(f"Platform: {report.get('platform', 'unknown')}")
    lines.append(f"Project: {report.get('project_root', '')}")

    modules = report.get("modules", [])
    if not modules:
        lines.append("")
        lines.append("[!] No modules found.")
        for err in report.get("errors", []):
            lines.append(f"  [!] {err}")
        return "\n".join(lines)

    mod_names = [m["name"] for m in modules]
    lines.append(f"Modules scanned: {', '.join(mod_names)}")

    meta = report.get("metadata", {})
    if meta.get("modules_skipped", 0) > 0:
        lines.append(f"Modules skipped: {meta['modules_skipped']}")

    lines.append("")
    lines.append("=== Summary ===")
    lines.append(f"  Colors:       {s['colors']} ({s['color_index_size']} unique hex)")
    lines.append(f"  Strings:      {s['strings']}")
    lines.append(f"  Dimens:       {s['dimens']}")
    lines.append(f"  Styles:       {s['styles']}")
    lines.append(f"  Drawables:    {s['drawables']}")
    lines.append(f"  Custom Views: {s['custom_views']}")

    # Custom views detail
    all_views = [v for m in modules for v in m.get("custom_views", [])]
    if all_views:
        lines.append("")
        lines.append("=== Custom Views ===")
        for v in all_views:
            lines.append(f"  {v['name']} (extends {v['parent']}) - {v['package']}")

    errors = report.get("errors", [])
    if errors:
        lines.append("")
        lines.append("=== Errors ===")
        for err in errors:
            lines.append(f"  [!] {err}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Scan mobile project resources for figma-to-mobile."
    )
    parser.add_argument("project_root", help="Path to project root")
    parser.add_argument("--module", "-m", default=None,
                        help="Target module (default: auto)")
    parser.add_argument("--platform", "-p", default=None,
                        help="Force platform (android, ios, flutter)")
    parser.add_argument("--level", "-l", default="full",
                        choices=["resources", "full"],
                        help="Scan level: 'resources' (fast, no code analysis) or 'full' (default)")
    parser.add_argument("--output", "-o", default=None,
                        help="Output JSON file path (default: stdout text report)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON to stdout")
    args = parser.parse_args()

    if not Path(args.project_root).is_dir():
        print(f"Error: {args.project_root} is not a directory", file=sys.stderr)
        sys.exit(1)

    report = scan_project(
        args.project_root, args.module, args.platform, args.level,
    )

    if args.output:
        Path(args.output).write_text(
            json.dumps(report, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        print(f"Report written to {args.output}")
        print(format_text_report(report))
    elif args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    else:
        print(format_text_report(report))


if __name__ == "__main__":
    main()

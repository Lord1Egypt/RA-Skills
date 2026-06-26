"""Cross-reference BreakingChange objects with usage_scanner results
to populate PackageUpdate.impact_locations and impact_confidence.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from schema import PackageUpdate, BreakingChange, ImpactLocation
from usage_scanner import scan_project, SCAN_EXTENSIONS


# ── Public API ────────────────────────────────────────────────────────────────

def analyze_impact(
    packages: List[PackageUpdate],
    project_root: str,
    timeout_per_package: int = 15,
) -> Tuple[List[PackageUpdate], List[str]]:
    """Populate impact_locations and impact_confidence on each PackageUpdate.

    For each PackageUpdate that has breaking_changes:
    1. Run scan_project() for that package
    2. Aggregate all ImpactLocation objects onto the package
    3. Set impact_confidence based on detection methods used
    Returns (updated_packages, all_skipped_files).
    """
    all_skipped: List[str] = []

    for pkg in packages:
        ecosystem = pkg.ecosystem
        if ecosystem not in SCAN_EXTENSIONS:
            pkg.impact_confidence = "not_scanned"
            continue

        if not pkg.breaking_changes:
            # No specific symbols extracted from the changelog.
            # For major version bumps, still run a broad scan using the package
            # name itself so the user can see which files use the package at all.
            if pkg.semver_type != "major":
                pkg.impact_confidence = "not_scanned"
                continue
            broad_bc = BreakingChange(
                symbol=pkg.package,
                change_type="other",
                description=(
                    f"Major version bump to {pkg.latest_version} — "
                    "specific breaking symbols could not be extracted"
                ),
                migration_note=None,
                source="major_bump_broad_scan",
                confidence="low",
            )
            scan_breaking = [broad_bc]
        else:
            scan_breaking = pkg.breaking_changes

        try:
            scan_results, skipped = scan_project(
                breaking_changes=scan_breaking,
                project_root=project_root,
                ecosystem=ecosystem,
                timeout_seconds=timeout_per_package,
                package_name=pkg.package,
            )
            all_skipped.extend(skipped)
        except Exception:
            pkg.impact_confidence = "not_scanned"
            continue

        # Flatten all locations from all symbols
        all_locations: List[ImpactLocation] = []
        for locs in scan_results.values():
            all_locations.extend(locs)

        # Write back individual symbol locations to each BreakingChange
        for bc in pkg.breaking_changes:
            if bc.symbol in scan_results:
                bc_locs = scan_results[bc.symbol]
            else:
                # Try base symbol match
                bc_locs = []
                for sym_key, locs in scan_results.items():
                    if sym_key.endswith(bc.symbol) or bc.symbol.endswith(sym_key):
                        bc_locs.extend(locs)

        # Store flattened locations on the package (deduplicated by file+line)
        pkg.impact_locations = _dedupe_locations(all_locations)
        pkg.impact_confidence = _determine_confidence(pkg.impact_locations)

    return packages, all_skipped


def _determine_confidence(locations: List[ImpactLocation]) -> str:
    """
    "high"        -> at least one AST-detected location
    "med"         -> all locations are grep/regex detected
    "low"         -> no locations found but scan ran
    "not_scanned" -> scan didn't run (should not be called in that case)
    """
    if not locations:
        return "low"
    for loc in locations:
        if loc.detection_method == "ast":
            return "high"
    return "med"


# ── Internal helpers ──────────────────────────────────────────────────────────

def _dedupe_locations(locations: List[ImpactLocation]) -> List[ImpactLocation]:
    """Remove duplicate locations (same file path + line number)."""
    seen: set = set()
    unique: List[ImpactLocation] = []
    for loc in locations:
        key = (loc.file_path, loc.line_number)
        if key not in seen:
            seen.add(key)
            unique.append(loc)
    return unique

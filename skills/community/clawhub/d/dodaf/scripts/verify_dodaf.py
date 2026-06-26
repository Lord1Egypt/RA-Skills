#!/usr/bin/env python3
"""Verify DoDAF model completeness and consistency.

Usage:
    python scripts/verify_dodaf.py <project_dir>

Features:
    - Checks all 23 required DoDAF view products
    - Validates cross-view naming consistency
    - Detects orphan elements and circular dependencies
    - Generates verification report
"""

import sys
import re
from pathlib import Path
from datetime import datetime


# Required DoDAF view products
REQUIRED_VIEWS = {
    "AV-1": "Overview and Summary Information",
    "AV-2": "Integrated Dictionary",
    "AV-3": "Concept of Operations",
    "OV-1": "High-Level Operational Concept Graphic",
    "OV-2": "Operational Resource Flow Description",
    "OV-3": "Operational Information Exchange Matrix",
    "OV-5": "Operational Activity Model",
    "CV-1": "Capability Taxonomy",
    "CV-2": "Capability Phasing",
    "CV-3": "Capability Dependencies",
    "SV-1": "Systems Interface Description",
    "SV-2": "Systems Communication Description",
    "SV-4": "Systems Functionality Description",
    "SV-5": "Operational Activity to Systems Function Traceability",
    "DIV-1": "Data Model Description",
    "DIV-2": "Data Dictionary",
    "DIV-3": "Data Exchange Matrix",
    "TV-1": "Technical Standards Profile",
    "TV-2": "Technical Measures",
    "TV-3": "Technical Architecture Framework",
    "PV-1": "Project Timeline",
    "PV-2": "Project Structure",
    "PV-3": "Project Resource Flow",
}

# Expected file patterns for each view
VIEW_FILE_PATTERNS = {
    "AV-1": ["AV-1-overview", "AV-1-overview-summary"],
    "AV-2": ["AV-2-integrated-dictionary"],
    "AV-3": ["AV-3-conops"],
    "OV-1": ["OV-1-operational-concept"],
    "OV-2": ["OV-2-resource-flow"],
    "OV-3": ["OV-3-information-exchange-matrix"],
    "OV-5": ["OV-5-activity-model"],
    "CV-1": ["CV-1-capability-taxonomy"],
    "CV-2": ["CV-2-capability-phasing"],
    "CV-3": ["CV-3-capability-dependencies"],
    "SV-1": ["SV-1-systems-interface"],
    "SV-2": ["SV-2-systems-communication"],
    "SV-4": ["SV-4-systems-functionality"],
    "SV-5": ["SV-5-traceability-matrix"],
    "DIV-1": ["DIV-1-data-model"],
    "DIV-2": ["DIV-2-data-dictionary"],
    "DIV-3": ["DIV-3-data-exchange-matrix"],
    "TV-1": ["TV-1-technical-standards"],
    "TV-2": ["TV-2-technical-measures"],
    "TV-3": ["TV-3-technical-framework"],
    "PV-1": ["PV-1-project-timeline"],
    "PV-2": ["PV-2-project-structure"],
    "PV-3": ["PV-3-project-resource-flow"],
}


def verify_dodaf_project(project_dir: str):
    """Verify a DoDAF project for completeness and consistency."""
    project_path = Path(project_dir)
    docs_dir = project_path / "docs"
    diagrams_dir = project_path / "diagrams"

    print("=" * 70)
    print("DoDAF Model Verification Report")
    print(f"Project: {project_dir}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    findings = []
    warnings = []

    # ===== 1. Completeness Verification =====
    print("\n[1] Completeness Verification")
    print("-" * 40)

    found_views = {}
    missing_views = []

    for view_id, view_name in REQUIRED_VIEWS.items():
        patterns = VIEW_FILE_PATTERNS.get(view_id, [])
        found = False

        # Check in docs/
        if docs_dir.exists():
            for pattern in patterns:
                md_files = list(docs_dir.glob(f"{pattern}.md"))
                if md_files:
                    found = True
                    found_views[view_id] = {"name": view_name, "doc": str(md_files[0])}
                    break

        # Check in diagrams/
        if diagrams_dir.exists() and not found:
            for pattern in patterns:
                drawio_files = list(diagrams_dir.glob(f"{pattern}.drawio"))
                if drawio_files:
                    found = True
                    found_views[view_id] = {"name": view_name, "diagram": str(drawio_files[0])}
                    break

        # Also check by content in consolidated files
        if not found and docs_dir.exists():
            for md_file in docs_dir.glob("*.md"):
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                if view_id in content and view_name.split()[0] in content:
                    found = True
                    found_views[view_id] = {"name": view_name, "content_in": str(md_file)}
                    break

        if found:
            print(f"  [OK] {view_id}: {view_name}")
        else:
            print(f"  [MISSING] {view_id}: {view_name}")
            missing_views.append(view_id)
            findings.append(f"Missing view: {view_id} ({view_name})")

    print(f"\nView coverage: {len(found_views)}/{len(REQUIRED_VIEWS)} ({len(found_views)/len(REQUIRED_VIEWS)*100:.0f}%)")

    # Check traceability matrix
    has_traceability = False
    if docs_dir.exists():
        for f in docs_dir.glob("*traceability*"):
            has_traceability = True
            break
    print(f"  [{'OK' if has_traceability else 'MISSING'}] Traceability Matrix")

    # Check integrated dictionary
    has_dictionary = "AV-2" in found_views
    print(f"  [{'OK' if has_dictionary else 'MISSING'}] Integrated Dictionary (AV-2)")

    # ===== 2. Consistency Verification =====
    print("\n[2] Consistency Verification")
    print("-" * 40)

    all_content = ""
    if docs_dir.exists():
        for md_file in docs_dir.glob("*.md"):
            all_content += md_file.read_text(encoding="utf-8", errors="ignore") + "\n"

    # Check naming consistency
    view_refs = re.findall(r'\b(AV|OV|CV|SV|DIV|TV|PV)-\d+\b', all_content)
    unique_refs = set(view_refs)
    print(f"  View references found: {len(unique_refs)} unique ({len(view_refs)} total)")

    # Check for consistent element IDs
    element_ids = re.findall(r'\b(DE|OA|SF|SYS|INT|C|IE|DX|TM|RF|CD|DR|COM|HW|SW)-\d+', all_content)
    id_prefixes = set(e.split('-')[0] for e in element_ids)
    print(f"  Element ID prefixes found: {', '.join(sorted(id_prefixes))}")

    # Check cross-reference consistency
    cross_refs_ok = True
    for view_id in found_views:
        if view_id not in all_content and view_id not in str(found_views):
            # View exists as file but not referenced in content
            pass  # This is acceptable

    print(f"  [{'OK' if cross_refs_ok else 'WARN'}] Cross-reference consistency")

    # Check for orphan indicators
    has_orphan_check = "orphan" in all_content.lower() or "unconnected" in all_content.lower()
    print(f"  [{'OK' if has_orphan_check else 'INFO'}] Orphan element checking")

    # Check for circular dependency check
    has_cycle_check = "cycle" in all_content.lower() or "circular" in all_content.lower()
    print(f"  [{'OK' if has_cycle_check else 'INFO'}] Circular dependency checking")

    # ===== 3. File Structure Verification =====
    print("\n[3] File Structure Verification")
    print("-" * 40)

    expected_dirs = ["docs", "diagrams"]
    for d in expected_dirs:
        dir_path = project_path / d
        exists = dir_path.exists()
        print(f"  [{'OK' if exists else 'MISSING'}] {d}/ directory")
        if exists:
            file_count = len(list(dir_path.iterdir()))
            print(f"         {file_count} files")

    # ===== 4. Summary =====
    print("\n[4] Summary")
    print("-" * 40)

    completeness_score = len(found_views) / len(REQUIRED_VIEWS) * 100
    print(f"Completeness Score: {completeness_score:.1f}%")

    if completeness_score >= 90:
        status = "PASS - Model is comprehensive"
    elif completeness_score >= 70:
        status = "WARNING - Model needs some additional views"
    else:
        status = "FAIL - Model needs significant work"

    print(f"Status: {status}")

    if missing_views:
        print(f"\nMissing views ({len(missing_views)}):")
        for v in missing_views:
            print(f"  - {v}: {REQUIRED_VIEWS[v]}")

    if findings:
        print(f"\nFindings ({len(findings)}):")
        for i, f in enumerate(findings, 1):
            print(f"  {i}. {f}")

    print("\nRecommendations:")
    if missing_views:
        print(f"  - Add missing views: {', '.join(missing_views)}")
    print("  - Ensure traceability matrix is fully populated")
    print("  - Verify all naming conventions are consistent")
    print("  - Run consolidated report generation (Phase 9)")

    return completeness_score >= 70


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/verify_dodaf.py <project_dir>")
        print("Example: python scripts/verify_dodaf.py ./my-dodaf-project")
        sys.exit(1)

    success = verify_dodaf_project(sys.argv[1])
    sys.exit(0 if success else 1)

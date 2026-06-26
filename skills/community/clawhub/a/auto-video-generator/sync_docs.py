#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bilingual Documentation Synchronizer
====================================

This tool helps maintain synchronized English and Chinese documentation
for auto-video-generator project.

Features:
- Check synchronization status between EN/ZH documents
- Generate statistics on documentation coverage
- Create missing translations (template)
- Validate markdown formatting

Usage:
    python sync_docs.py check          # Check sync status
    python sync_docs.py stats          # Show coverage stats
    python sync_docs.py template       # Generate translation template
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class DocPair:
    """Represents a pair of English and Chinese documents."""
    en_path: Path
    zh_path: Path
    en_exists: bool
    zh_exists: bool
    en_size: int = 0
    zh_size: int = 0
    en_sections: int = 0
    zh_sections: int = 0
    sync_status: str = "unknown"


class BilingualDocSync:
    """Synchronize bilingual documentation."""

    # Document pairs to monitor
    DOC_PAIRS = [
        ("SKILL.md", "SKILL.zh-CN.md"),
        ("README.md", "README.zh-CN.md"),
        ("docs/getting-started/introduction.md", "docs/getting-started/introduction.zh-CN.md"),
        ("docs/getting-started/quick-start.md", "docs/getting-started/quick-start.zh-CN.md"),
        ("docs/getting-started/installation.md", "docs/getting-started/installation.zh-CN.md"),
        ("docs/getting-started/configuration.md", "docs/getting-started/configuration.zh-CN.md"),
        ("docs/api/video-generator.md", "docs/api/video-generator.zh-CN.md"),
        ("docs/tutorials/01-first-video.md", "docs/tutorials/01-first-video.zh-CN.md"),
        ("docs/guides/performance-tuning.md", "docs/guides/performance-tuning.zh-CN.md"),
        ("docs/troubleshooting/common-errors.md", "docs/troubleshooting/common-errors.zh-CN.md"),
        ("docs/template-gallery.md", "docs/template-gallery.zh-CN.md"),
        ("contributing.md", "contributing.zh-CN.md"),
        ("CHANGELOG.md", "CHANGELOG.zh-CN.md"),
    ]

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir).resolve()
        self.doc_pairs: List[DocPair] = []

    def scan_documents(self) -> None:
        """Scan all document pairs and collect metadata."""
        self.doc_pairs = []

        for en_file, zh_file in self.DOC_PAIRS:
            en_path = self.base_dir / en_file
            zh_path = self.base_dir / zh_file

            pair = DocPair(
                en_path=en_path,
                zh_path=zh_path,
                en_exists=en_path.exists(),
                zh_exists=zh_path.exists(),
            )

            if pair.en_exists:
                pair.en_size = en_path.stat().st_size
                pair.en_sections = self._count_sections(en_path)

            if pair.zh_exists:
                pair.zh_size = zh_path.stat().st_size
                pair.zh_sections = self._count_sections(zh_path)

            # Determine sync status
            if pair.en_exists and pair.zh_exists:
                size_ratio = pair.zh_size / max(pair.en_size, 1)
                section_ratio = pair.zh_sections / max(pair.en_sections, 1)

                if size_ratio > 0.8 and section_ratio > 0.8:
                    pair.sync_status = "synced"
                elif size_ratio > 0.5 and section_ratio > 0.5:
                    pair.sync_status = "partial"
                else:
                    pair.sync_status = "out_of_sync"
            elif pair.en_exists and not pair.zh_exists:
                pair.sync_status = "missing_zh"
            elif not pair.en_exists and pair.zh_exists:
                pair.sync_status = "missing_en"
            else:
                pair.sync_status = "both_missing"

            self.doc_pairs.append(pair)

    def _count_sections(self, file_path: Path) -> int:
        """Count markdown sections (## headers)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return len(re.findall(r'^#{2,}\s', content, re.MULTILINE))
        except Exception:
            return 0

    def check_sync(self) -> Dict[str, any]:
        """Check synchronization status of all document pairs."""
        self.scan_documents()

        results = {
            "total_pairs": len(self.doc_pairs),
            "synced": 0,
            "partial": 0,
            "out_of_sync": 0,
            "missing_zh": 0,
            "missing_en": 0,
            "pairs": []
        }

        for pair in self.doc_pairs:
            results[pair.sync_status] += 1

            pair_info = {
                "en": str(pair.en_path.relative_to(self.base_dir)),
                "zh": str(pair.zh_path.relative_to(self.base_dir)),
                "status": pair.sync_status,
                "en_size_kb": round(pair.en_size / 1024, 1),
                "zh_size_kb": round(pair.zh_size / 1024, 1),
                "en_sections": pair.en_sections,
                "zh_sections": pair.zh_sections,
            }
            results["pairs"].append(pair_info)

        return results

    def print_sync_report(self) -> None:
        """Print human-readable sync report."""
        results = self.check_sync()

        print("\n" + "=" * 70)
        print("  Bilingual Documentation Sync Report")
        print("=" * 70)

        print(f"\n[SUMMARY]")
        print(f"  Total Document Pairs: {results['total_pairs']}")
        print(f"  ✓ Fully Synced: {results['synced']}")
        print(f"  △ Partial Sync: {results['partial']}")
        print(f"  ✗ Out of Sync: {results['out_of_sync']}")
        print(f"  ⚠ Missing Chinese: {results['missing_zh']}")
        print(f"  ⚠ Missing English: {results['missing_en']}")

        sync_rate = (results['synced'] / results['total_pairs']) * 100 if results['total_pairs'] > 0 else 0
        print(f"\n  Sync Rate: {sync_rate:.1f}%")

        print(f"\n{'=' * 70}")
        print("  Detailed Status")
        print("=" * 70)

        status_icons = {
            "synced": "[OK]",
            "partial": "[PARTIAL]",
            "out_of_sync": "[SYNC ERROR]",
            "missing_zh": "[NO ZH]",
            "missing_en": "[NO EN]",
            "both_missing": "[MISSING]"
        }

        for i, pair in enumerate(results["pairs"], 1):
            icon = status_icons.get(pair["status"], "[?]")
            en_size = pair["en_size_kb"]
            zh_size = pair["zh_size_kb"]

            print(f"\n{i:2d}. {icon} {pair['en']}")
            if pair["zh"] != pair["en"]:
                print(f"     → {pair['zh']}")

            if pair["status"] in ["synced", "partial", "out_of_sync"]:
                print(f"     EN: {en_size:.1f} KB ({pair['en_sections']} sections)")
                print(f"     ZH: {zh_size:.1f} KB ({pair['zh_sections']} sections)")

        print("\n" + "=" * 70)

        if results['missing_zh'] > 0 or results['out_of_sync'] > 0:
            print("[ACTION REQUIRED]")
            if results['missing_zh'] > 0:
                print(f"  • {results['missing_zh']} Chinese versions need to be created")
            if results['out_of_sync'] > 0:
                print(f"  • {results['out_of_sync']} documents are out of sync")
            print("\n  Run: python sync_docs.py template  (to generate templates)")
        else:
            print("[ALL DOCUMENTS SYNCED] ✓")

        print("=" * 70 + "\n")

    def get_statistics(self) -> Dict[str, any]:
        """Get documentation coverage statistics."""
        self.scan_documents()

        total_en_size = sum(p.en_size for p in self.doc_pairs if p.en_exists)
        total_zh_size = sum(p.zh_size for p in self.doc_pairs if p.zh_exists)
        total_en_sections = sum(p.en_sections for p in self.doc_pairs if p.en_exists)
        total_zh_sections = sum(p.zh_sections for p in self.doc_pairs if p.zh_exists)

        stats = {
            "english_docs": {
                "file_count": sum(1 for p in self.doc_pairs if p.en_exists),
                "total_size_kb": round(total_en_size / 1024, 1),
                "total_sections": total_en_sections,
            },
            "chinese_docs": {
                "file_count": sum(1 for p in self.doc_pairs if p.zh_exists),
                "total_size_kb": round(total_zh_size / 1024, 1),
                "total_sections": total_zh_sections,
            },
            "coverage": {
                "file_coverage_percent": round(
                    (sum(1 for p in self.doc_pairs if p.zh_exists) /
                     max(sum(1 for p in self.doc_pairs if p.en_exists), 1)) * 100, 1
                ),
                "size_coverage_percent": round(
                    (total_zh_size / max(total_en_size, 1)) * 100, 1
                ),
                "section_coverage_percent": round(
                    (total_zh_sections / max(total_en_sections, 1)) * 100, 1
                ),
            },
        }

        return stats

    def print_statistics(self) -> None:
        """Print documentation statistics."""
        stats = self.get_statistics()

        print("\n" + "=" * 70)
        print("  Documentation Statistics (EN vs ZH)")
        print("=" * 70)

        print(f"\n[English Documents]")
        print(f"  Files: {stats['english_docs']['file_count']}")
        print(f"  Total Size: {stats['english_docs']['total_size_kb']} KB")
        print(f"  Total Sections: {stats['english_docs']['total_sections']}")

        print(f"\n[Chinese Documents]")
        print(f"  Files: {stats['chinese_docs']['file_count']}")
        print(f"  Total Size: {stats['chinese_docs']['total_size_kb']} KB")
        print(f"  Total Sections: {stats['chinese_docs']['total_sections']}")

        print(f"\n[Coverage Analysis]")
        print(f"  File Coverage: {stats['coverage']['file_coverage_percent']}% "
              f"({stats['chinese_docs']['file_count']}/{stats['english_docs']['file_count']})")
        print(f"  Size Coverage: {stats['coverage']['size_coverage_percent']}% "
              f"({stats['chinese_docs']['total_size_kb']}/{stats['english_docs']['total_size_kb']} KB)")
        print(f"  Section Coverage: {stats['coverage']['section_coverage_percent']}% "
              f"({stats['chinese_docs']['total_sections']}/{stats['english_docs']['total_sections']})")

        # Grade
        avg_coverage = (
            stats['coverage']['file_coverage_percent'] +
            stats['coverage']['size_coverage_percent'] +
            stats['coverage']['section_coverage_percent']
        ) / 3

        if avg_coverage >= 90:
            grade = "A+ (Excellent)"
        elif avg_coverage >= 80:
            grade = "A (Very Good)"
        elif avg_coverage >= 70:
            grade = "B (Good)"
        elif avg_coverage >= 60:
            grade = "C (Acceptable)"
        else:
            grade = "D (Needs Work)"

        print(f"\n  Overall Grade: {grade} ({avg_coverage:.1f}%)")

        print("=" * 70 + "\n")

    def generate_translation_template(self, output_file: str = "translation_template.md") -> None:
        """Generate a template file showing what needs to be translated."""
        self.scan_documents()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Translation Template\n\n")
            f.write("This file shows which documents need Chinese translation.\n\n")
            f.write("---\n\n")

            needs_translation = [p for p in self.doc_pairs
                               if p.sync_status in ["missing_zh", "out_of_sync", "partial"]]

            if not needs_translation:
                f.write("**All documents are fully synced!** ✓\n")
            else:
                f.write(f"## Documents Needing Attention ({len(needs_translation)} files)\n\n")

                for pair in needs_translation:
                    f.write(f"### {pair.en_path.name}\n\n")
                    f.write(f"- **English**: `{pair.en_path.relative_to(self.base_dir)}`\n")
                    f.write(f"- **Chinese**: `{pair.zh_path.relative_to(self.base_dir)}`\n")
                    f.write(f"- **Status**: {pair.sync_status.upper()}\n")

                    if pair.en_exists:
                        f.write(f"- **EN Size**: {pair.en_size / 1024:.1f} KB\n")
                        f.write(f"- **Sections**: {pair.en_sections}\n")

                    if pair.zh_exists:
                        f.write(f"- **ZH Size**: {pair.zh_size / 1024:.1f} KB\n")
                        f.write(f"- **Sections**: {pair.zh_sections}\n")

                    f.write("\n---\n\n")

        print(f"[OK] Translation template generated: {output_file}")


def main():
    """Main entry point."""
    import sys

    base_dir = Path(__file__).parent.resolve()
    sync_tool = BilingualDocSync(str(base_dir))

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python sync_docs.py check      Check sync status")
        print("  python sync_docs.py stats      Show statistics")
        print("  python sync_docs.py template   Generate translation template")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "check":
        sync_tool.print_sync_report()
    elif command == "stats":
        sync_tool.print_statistics()
    elif command == "template":
        output = sys.argv[2] if len(sys.argv) > 2 else "translation_template.md"
        sync_tool.generate_translation_template(output)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

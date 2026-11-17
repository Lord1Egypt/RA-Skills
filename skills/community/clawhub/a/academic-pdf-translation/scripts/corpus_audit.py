from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

from _common import (
    SkillError,
    language_profiles,
    sha256_file,
    utc_now,
    write_json,
)
from pdf_profile import profile_pdf


DEFAULT_EXCLUDED_PARTS = {
    "中文译版",
    "翻译工作记录",
    "临时工作区",
    "tmp",
    ".git",
    ".venv",
    "venv",
}

def _derived_suffixes() -> tuple[str, ...]:
    suffixes: set[str] = set()
    for profile in language_profiles().values():
        values = [profile.get("filename_suffix")]
        values.extend(profile.get("filename_suffixes", []))
        suffixes.update(
            str(value)
            for value in values
            if isinstance(value, str) and value.endswith(".pdf")
        )
    return tuple(sorted(suffixes))


def _is_excluded(path: Path, root: Path, include_derived: bool) -> bool:
    relative = path.relative_to(root)
    if any(part in DEFAULT_EXCLUDED_PARTS for part in relative.parts):
        return True
    if not include_derived and path.name.endswith(_derived_suffixes()):
        return True
    return False


def audit_corpus(root: Path, include_derived: bool = False) -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise SkillError(f"语料目录不存在: {root}")
    pdfs = [
        path
        for path in root.rglob("*.pdf")
        if path.is_file() and not _is_excluded(path, root, include_derived)
    ]
    records: list[dict[str, Any]] = []
    duplicate_of: dict[str, str] = {}
    seen_hashes: dict[str, str] = {}
    failures: list[dict[str, str]] = []
    for path in sorted(pdfs):
        try:
            digest = sha256_file(path)
            relative = str(path.relative_to(root))
            if digest in seen_hashes:
                duplicate_of[relative] = seen_hashes[digest]
            else:
                seen_hashes[digest] = relative
            profile = profile_pdf(path)
            records.append(
                {
                    "path": relative,
                    "sha256": digest,
                    "duplicate_of": duplicate_of.get(relative),
                    "page_count": profile["page_count"],
                    "source_language_estimate": profile[
                        "source_language_estimate"
                    ],
                    "recommended_route": profile["route"]["recommended"],
                    "complex_pages": profile["complex_pages"],
                    "scan_risk_pages": profile["scan_risk_pages"],
                    "page_size_variants": profile["page_size_variants"],
                }
            )
        except Exception as exc:
            failures.append({"path": str(path.relative_to(root)), "error": str(exc)})

    route_counts = Counter(record["recommended_route"] for record in records)
    return {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "root": str(root),
        "include_derived": include_derived,
        "pdf_count": len(records),
        "unique_pdf_count": len(seen_hashes),
        "total_pages": sum(record["page_count"] for record in records),
        "route_counts": dict(sorted(route_counts.items())),
        "failures": failures,
        "documents": records,
    }


def _markdown(report: dict[str, Any]) -> str:
    lines = [
        "# 学术 PDF 语料库审计",
        "",
        f"- 根目录：`{report['root']}`",
        f"- PDF：{report['pdf_count']} 份",
        f"- 去重后：{report['unique_pdf_count']} 份",
        f"- 总页数：{report['total_pages']} 页",
        "",
        "## 路线估计",
        "",
        "| 路线 | 数量 |",
        "|---|---:|",
    ]
    for route, count in report["route_counts"].items():
        lines.append(f"| `{route}` | {count} |")
    lines.extend(
        [
            "",
            "## 文档",
            "",
            "| 文件 | 页数 | 建议路线 | 复杂页 | 扫描风险页 | 重复 |",
            "|---|---:|---|---|---|---|",
        ]
    )
    for record in report["documents"]:
        lines.append(
            "| `{path}` | {page_count} | `{recommended_route}` | {complex} | "
            "{scan} | {duplicate} |".format(
                path=record["path"],
                page_count=record["page_count"],
                recommended_route=record["recommended_route"],
                complex=", ".join(map(str, record["complex_pages"])) or "-",
                scan=", ".join(map(str, record["scan_risk_pages"])) or "-",
                duplicate=record["duplicate_of"] or "-",
            )
        )
    if report["failures"]:
        lines.extend(["", "## 无法读取", ""])
        for failure in report["failures"]:
            lines.append(f"- `{failure['path']}`：{failure['error']}")
    lines.extend(
        [
            "",
            "> 路线为启发式建议，必须结合复杂页目视检查后决定。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="批量画像学术 PDF 并估计制作路线")
    parser.add_argument("root", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--include-derived", action="store_true")
    args = parser.parse_args()
    try:
        report = audit_corpus(args.root, args.include_derived)
        write_json(args.output_json, report)
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(_markdown(report), encoding="utf-8")
        print(f"已审计 {report['pdf_count']} 份 PDF，共 {report['total_pages']} 页")
        print(f"JSON: {args.output_json}")
        print(f"Markdown: {args.output_md}")
        return 0 if not report["failures"] else 2
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

"""把翻译单元绑定到原文元素，并检查有没有孤立译文。"""

from __future__ import annotations

import sys
from pathlib import Path

# 按 README 的写法 `python3 scripts/X.py` 运行时，sys.path 里只有 scripts/，
# 没有仓库根，academic_pdf_translation 包就 import 不到。先把根加进去。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse  # noqa: E402
from pathlib import Path  # noqa: E402

from academic_pdf_translation.analysis.element_overrides import (  # noqa: E402
    apply_all,
    load_overrides,
)
from academic_pdf_translation.analysis.source_elements import (  # noqa: E402
    analyze_job_elements,
)
from academic_pdf_translation.analysis.unit_binding import (  # noqa: E402
    bind_units,
    validate_payload_sources,
)

from _common import SkillError, import_fitz, load_json, write_json  # noqa: E402

BINDING_FILE_NAME = "unit_bindings.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_dir", type=Path)
    args = parser.parse_args()
    job_dir = args.job_dir.resolve()
    try:
        job = load_json(job_dir / "job.json")
        source_units = load_json(
            job_dir
            / job.get("files", {}).get("source_units", "source_units.json")
        )
        fitz = import_fitz()
        inventory = analyze_job_elements(
            job_dir,
            pymupdf_version=getattr(fitz, "VersionBind", "0"),
        )
        apply_all(inventory, load_overrides(job_dir))
        report = bind_units(source_units.get("units", []), inventory)

        complex_path = job_dir / job.get("files", {}).get(
            "complex_content_payload", "complex_content.json"
        )
        if complex_path.is_file():
            payload_texts = []
            for item in load_json(complex_path).get("items", []):
                payload = item.get("payload")
                if isinstance(payload, dict):
                    payload_texts.extend(
                        entry
                        for entry in payload.get("regions", [])
                        if isinstance(entry, dict)
                    )
            report.problems.extend(
                validate_payload_sources(
                    payload_texts,
                    {binding.unit_id for binding in report.bindings},
                )
            )
        write_json(job_dir / BINDING_FILE_NAME, report.as_dict())
        # 角色回写：元素纠正（例如把一段误判成正文的题录 retype 成
        # reference-entry）之后重新绑定，translation.json 里各单元自带的
        # element_role 还是旧的，批次写回那一关会按旧角色拒绝保留原文。
        # 绑定是角色的唯一权威来源，绑完就同步回去。
        translation_path = job_dir / "translation.json"
        if translation_path.is_file():
            translation = load_json(translation_path)
            roles = {
                binding.unit_id: binding.element_role
                for binding in report.bindings
            }
            changed = 0
            for unit in translation.get("units", []):
                if not isinstance(unit, dict):
                    continue
                fresh = roles.get(str(unit.get("id") or ""))
                if fresh and unit.get("element_role") != fresh:
                    unit["element_role"] = fresh
                    changed += 1
            if changed:
                write_json(translation_path, translation)
                print(f"已同步 {changed} 个单元的元素角色进 translation.json")
    except (SkillError, OSError, ValueError) as exc:
        print(f"错误: {exc}")
        return 1

    print(f"绑定结果已写入: {job_dir / BINDING_FILE_NAME}")
    print(f"翻译单元: {len(source_units.get('units', []))}")
    print(f"已绑定: {len(report.bindings)}")
    print(f"孤立译文: {len(report.orphan_units)}")
    print(f"没有单元的元素: {len(report.elements_without_units)}")
    counts: dict[str, int] = {}
    for binding in report.bindings:
        counts[binding.element_role] = counts.get(binding.element_role, 0) + 1
    print("角色分布:")
    for name, count in sorted(counts.items()):
        print(f"  {name:<24}{count:>4}")
    if report.problems:
        print("问题:")
        for problem in report.problems:
            print(f"  - {problem}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

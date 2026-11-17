from __future__ import annotations

import hashlib
from pathlib import Path

#: 只列真正影响候选 PDF 输出的模块。字体解析决定实际字体文件，
#: 候选分析被排版过程用来读原文，两者都会改变输出，必须计入。
RENDERER_INPUTS = (
    "scripts/_common.py",
    "scripts/build_candidate.py",
    "scripts/candidate_analysis.py",
    "scripts/candidate_page_map.py",
    "scripts/font_preparation.py",
    "scripts/i18n.py",
    "scripts/reportlab_layout.py",
    "scripts/retained_source.py",
    "scripts/set_complex_payload.py",
    "scripts/typography_fit.py",
    "assets/language-profiles.json",
    # 生成器 import 的包文件也影响产出，必须进构建哈希，
    # 否则改了它们基准还显示"同一版代码"。
    "academic_pdf_translation/render/cjk_markup.py",
    "academic_pdf_translation/render/flowables.py",
    "academic_pdf_translation/render/font_runs.py",
    "academic_pdf_translation/render/formula_crop.py",
    "academic_pdf_translation/render/document_output.py",
    "academic_pdf_translation/render/mapping.py",
    "academic_pdf_translation/render/reference_data.py",
    "academic_pdf_translation/render/story.py",
    "academic_pdf_translation/render/story_complex.py",
    "academic_pdf_translation/render/story_text.py",
    "academic_pdf_translation/render/story_visual.py",
    "academic_pdf_translation/render/typography_search.py",
    "academic_pdf_translation/render/table_data.py",
    "academic_pdf_translation/render/text_blocks.py",
    "academic_pdf_translation/render/plan_bridge.py",
    "academic_pdf_translation/render/preserved_region_renderer.py",
    "academic_pdf_translation/planning/mode_policy.py",
)


def renderer_build_id(skill_root: Path | None = None) -> str:
    root = (
        skill_root.resolve()
        if skill_root is not None
        else Path(__file__).resolve().parent.parent
    )
    digest = hashlib.sha256()
    for relative in RENDERER_INPUTS:
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(f"生成器身份输入不存在: {relative}")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()

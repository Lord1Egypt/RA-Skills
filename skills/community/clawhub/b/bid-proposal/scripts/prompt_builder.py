#!/usr/bin/env python3
"""
Build AI writing prompts for each chapter of a bid proposal.

Combines chapter configuration, requirement analysis results, and material
library references to construct detailed prompts for AI chapter generation.

Usage:
    python3 prompt_builder.py <chapter_config_json> <analysis_json> [--material-lib <dir>]
"""

import json
import os
import sys


# ---------------------------------------------------------------------------
# Material library helpers
# ---------------------------------------------------------------------------

def find_material_references(chapter_name: str, material_lib_dir: str) -> list:
    """
    Search the material library directory for files relevant to a chapter.

    Searches in chapter-examples/ and past-projects/ subdirectories for files
    whose names contain the chapter name or related terms.

    Args:
        chapter_name: Name of the chapter (e.g., '服务方案', '技术方案').
        material_lib_dir: Path to the material library root.

    Returns:
        List of (filename, content) tuples.
    """
    if not material_lib_dir or not os.path.isdir(material_lib_dir):
        return []

    results = []
    search_dirs = ['chapter-examples', 'past-projects']

    for subdir in search_dirs:
        dir_path = os.path.join(material_lib_dir, subdir)
        if not os.path.isdir(dir_path):
            continue

        for fname in os.listdir(dir_path):
            if not fname.endswith(('.md', '.txt')):
                continue

            # Match by name similarity
            fname_no_ext = os.path.splitext(fname)[0]
            if _name_similar(chapter_name, fname_no_ext):
                fpath = os.path.join(dir_path, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    results.append((fname, content))
                except (IOError, UnicodeDecodeError):
                    continue

    return results


def _name_similar(chapter_name: str, file_name: str) -> bool:
    """Check if chapter name and file name are similar."""
    # Remove common suffixes
    clean_chapter = chapter_name.replace('方案', '').replace('分析', '').replace('服务', '')
    clean_file = file_name.replace('范例', '').replace('方案', '').replace('分析', '').replace('服务', '')

    # Check if any character appears in both
    if not clean_chapter or not clean_file:
        return file_name in chapter_name or chapter_name in file_name

    # Check for common characters
    common = set(clean_chapter) & set(clean_file)
    return len(common) >= min(2, len(clean_chapter), len(clean_file))


def load_chapter_template(chapter_id: str) -> str:
    """
    Load chapter template from references/chapter-templates.md.

    Args:
        chapter_id: The chapter identifier (e.g., 'service_solution').

    Returns:
        Template text for the chapter, or empty string if not found.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tmpl_path = os.path.join(script_dir, '..', 'references', 'chapter-templates.md')

    if not os.path.isfile(tmpl_path):
        return ''

    try:
        with open(tmpl_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return ''

    # Extract relevant section (heuristic: find heading that contains chapter name)
    # The template file uses ## for sections
    lines = content.split('\n')
    in_section = False
    section_lines = []

    # Map chapter IDs to possible heading matches
    chapter_name_map = {
        'background': '项目背景',
        'requirement': '需求分析',
        'service_solution': '服务方案|分项技术方案',
        'tech_solution': '分项技术方案|服务方案',
        'overall_design': '总体设计',
        'implementation': '实施',
        'sla': '服务保障|SLA',
        'training': '培训',
        'after_sales': '售后',
        'gap_analysis': '差距分析|整改',
        'assurance': '保障',
    }

    target_patterns = chapter_name_map.get(chapter_id, [])
    if isinstance(target_patterns, str):
        target_patterns = target_patterns.split('|')

    for line in lines:
        if line.startswith('## '):
            # Check if this is our target section
            if in_section:
                break  # Next section, stop
            for pat in target_patterns:
                if pat in line:
                    in_section = True
                    continue  # Continue to get title line

        if in_section:
            section_lines.append(line)

    return '\n'.join(section_lines)


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------

def build_chapter_prompt(chapter_config: dict, analysis_json: dict,
                         material_lib_dir: str = None) -> str:
    """
    Build a comprehensive writing prompt for a single chapter.

    The prompt includes:
    - Chapter name and writing guide
    - Project context (name, type, requirements)
    - Scoring items reference
    - Material library references (if available)
    - Writing style guidance

    Args:
        chapter_config: Dict with 'id', 'name', 'prompt_guide' keys.
        analysis_json: Analysis result from analyze_requirements.py.
        material_lib_dir: Optional path to material library root.

    Returns:
        A structured prompt string ready for AI generation.
    """
    chapter_name = chapter_config.get('name', '')
    chapter_id = chapter_config.get('id', '')
    prompt_guide = chapter_config.get('prompt_guide', '')

    project_name = analysis_json.get('project_name', '')
    project_type = analysis_json.get('project_type', '')
    scoring_items = analysis_json.get('scoring_items', [])
    tech_domains = analysis_json.get('tech_domains', [])
    key_requirements = analysis_json.get('key_requirements', [])
    special_notes = analysis_json.get('special_notes', '')

    # Find matching scoring item
    scoring_ref = ''
    for item in scoring_items:
        item_name = item.get('name', '')
        if _name_similar(chapter_name, item_name):
            score = item.get('max_score', '')
            reqs = item.get('requirements', [])
            scoring_ref = f"评分项「{item_name}」（{score}分）"
            if reqs:
                scoring_ref += f"\n评分要求：{'；'.join(reqs)}"
            break

    # Build the prompt
    lines = [
        f"# {chapter_name}",
        f"",
        f"## 项目背景",
        f"项目名称：{project_name}",
        f"项目类型：{project_type}",
    ]

    if tech_domains:
        lines.append(f"技术领域：{'、'.join(tech_domains)}")

    if key_requirements:
        lines.append(f"关键需求：{'、'.join(key_requirements[:8])}")

    if special_notes:
        lines.append(f"特殊要求：{special_notes}")

    lines.append('')

    if prompt_guide:
        lines.append(f"## 写作指引")
        lines.append(prompt_guide)
        lines.append('')

    if scoring_ref:
        lines.append(f"## 评分标准关联")
        lines.append(scoring_ref)
        lines.append('')

    # Add chapter template reference from templates file
    template_text = load_chapter_template(chapter_id)
    if template_text:
        lines.append(f"## 章节模板参考")
        lines.append(template_text)
        lines.append('')

    # Add material library references
    if material_lib_dir:
        materials = find_material_references(chapter_name, material_lib_dir)
        if materials:
            lines.append(f"## 素材库参考")
            lines.append(f"以下为素材库中与本章节相关的参考内容，写作时请借鉴其结构和风格：\n")
            for fname, content in materials:
                # Truncate long content to reasonable reference size
                excerpt = content[:2000]
                if len(content) > 2000:
                    excerpt += '\n\n...（内容已截断，完整内容见素材库）'
                lines.append(f"### 参考：{fname}")
                lines.append(excerpt)
                lines.append('')

    # Add writing directives
    lines.append(f"## 写作要求")
    lines.append(f"1. 请根据以上信息，撰写「{chapter_name}」章节的完整内容。")
    lines.append("2. 使用投标技术方案的专业风格，避免口语化表达。")
    lines.append("3. 内容需具体、可量化，避免空泛描述。")
    lines.append("4. 结合评分标准要求，确保覆盖所有评分点。")
    lines.append("5. 使用Markdown格式输出，合理使用标题、列表、表格。")
    lines.append("6. 控制篇幅在800-2000字之间（根据章节重要性调整）。")
    lines.append('7. 不要使用"我们""我司"等第一人称，使用客观表述。')
    lines.append("")
    lines.append(f"请开始撰写「{chapter_name}」章节：")

    return '\n'.join(lines)


def build_all_prompts(chapters: list, analysis_json: dict,
                      material_lib_dir: str = None) -> dict:
    """
    Build prompts for all chapters.

    Args:
        chapters: List of chapter config dicts.
        analysis_json: Analysis result dict.
        material_lib_dir: Optional material library path.

    Returns:
        Dict mapping chapter_id → prompt string.
    """
    results = {}
    for ch in chapters:
        ch_id = ch.get('id', ch.get('name', 'unknown'))
        results[ch_id] = build_chapter_prompt(ch, analysis_json, material_lib_dir)
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 prompt_builder.py <chapter_config_json> <analysis_json> [--material-lib <dir>]")
        print()
        print("  chapter_config_json: JSON string or path to JSON file with chapter config")
        print("  analysis_json: JSON string or path to JSON file with analysis results")
        print("  --material-lib: optional path to material library directory")
        sys.exit(1)

    # Parse chapter config
    chapter_arg = sys.argv[1]
    if os.path.isfile(chapter_arg):
        with open(chapter_arg, 'r', encoding='utf-8') as f:
            chapter_config = json.load(f)
    else:
        chapter_config = json.loads(chapter_arg)

    # Parse analysis
    analysis_arg = sys.argv[2]
    if os.path.isfile(analysis_arg):
        with open(analysis_arg, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
    else:
        analysis = json.loads(analysis_arg)

    # Parse optional material lib
    material_lib_dir = None
    if '--material-lib' in sys.argv:
        idx = sys.argv.index('--material-lib')
        if idx + 1 < len(sys.argv):
            material_lib_dir = sys.argv[idx + 1]

    # Handle list vs single chapter
    if isinstance(chapter_config, list):
        results = build_all_prompts(chapter_config, analysis, material_lib_dir)
        for ch_id, prompt in results.items():
            print(f"=== {ch_id} ===")
            print(prompt)
            print()
    else:
        prompt = build_chapter_prompt(chapter_config, analysis, material_lib_dir)
        print(prompt)


if __name__ == '__main__':
    main()

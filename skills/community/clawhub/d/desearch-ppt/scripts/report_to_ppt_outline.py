#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report to PPT Outline v2.0 - 报告到PPT大纲提炼器

本脚本用于实现 Skill v2.0 的阶段 3：PPT 大纲提炼。
它确保 PPT 的每一页内容都 100% 来源于研究报告，不添加任何报告中没有的信息。

核心原则：
  - PPT 文字 100% 来自报告原文
  - 不编造、不推测、不补充报告中没有的内容
  - 每页 PPT 必须标注其内容在报告中的来源位置
  - 页数根据报告实际内容弹性调整，不强制凑页数

使用方法：
  python3 report_to_ppt_outline.py <input_report.md> <output_outline.json>

输出：
  一个 JSON 文件，包含每页 PPT 的结构化大纲，格式如下：
  {
    "total_slides": 45,
    "report_source": "research_report_final.md",
    "slides": [
      {
        "num": 1,
        "layout": "cover",
        "title": "报告标题",
        "content": ["内容行1", "内容行2"],
        "source_section": "报告第一章",
        "source_text_excerpt": "原文摘录..."
      }
    ]
  }

依赖：
  - 无外部依赖（纯 Python 标准库）
"""

import re
import sys
import json
import os

# ============================================================
# 布局类型定义
# ============================================================

LAYOUT_TYPES = {
    "cover": "封面页 - 报告标题、副标题、团队名称",
    "toc": "目录页 - 章节列表",
    "section_divider": "章节分隔页 - 章节标题和编号",
    "title_content": "标题+内容页 - 最常用的布局",
    "two_column": "双栏页 - 对比或并列内容",
    "data_chart": "数据图表页 - 包含数据来源标注",
    "concept": "原创概念页 - 团队首创概念展示",
    "quote": "引用页 - 重要观点或政策引用",
    "summary": "总结页 - 章节或全文总结",
    "end": "结尾页 - 致谢和联系方式"
}

# ============================================================
# 报告解析函数
# ============================================================

def parse_report_structure(content):
    """
    解析报告的 Markdown 结构，提取章节和段落。
    
    参数：
        content: 报告的完整 Markdown 文本
    
    返回：
        list: 章节列表，每个章节包含标题和内容
    """
    sections = []
    current_section = {"title": "引言", "level": 0, "content": "", "subsections": []}
    
    lines = content.split('\n')
    
    for line in lines:
        # 检测标题行
        h1_match = re.match(r'^#\s+(.+)', line)
        h2_match = re.match(r'^##\s+(.+)', line)
        h3_match = re.match(r'^###\s+(.+)', line)
        
        if h1_match:
            if current_section["content"].strip() or current_section["subsections"]:
                sections.append(current_section)
            current_section = {
                "title": h1_match.group(1).strip(),
                "level": 1,
                "content": "",
                "subsections": []
            }
        elif h2_match:
            if current_section["content"].strip() or current_section["subsections"]:
                sections.append(current_section)
            current_section = {
                "title": h2_match.group(1).strip(),
                "level": 2,
                "content": "",
                "subsections": []
            }
        elif h3_match:
            current_section["subsections"].append({
                "title": h3_match.group(1).strip(),
                "content": ""
            })
        else:
            if current_section["subsections"]:
                current_section["subsections"][-1]["content"] += line + "\n"
            else:
                current_section["content"] += line + "\n"
    
    if current_section["content"].strip() or current_section["subsections"]:
        sections.append(current_section)
    
    return sections

def extract_key_sentences(text, max_items=5):
    """
    从一段文本中提取关键句子（用于PPT内容）。
    
    参数：
        text: 段落文本
        max_items: 最多提取几条
    
    返回：
        list: 关键句子列表
    """
    # 按句号分割
    sentences = re.split(r'[。！？\n]', text)
    
    # 过滤空句和过短的句子
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    # 优先选择包含数据的句子
    data_sentences = [s for s in sentences if re.search(r'\d+', s)]
    other_sentences = [s for s in sentences if s not in data_sentences]
    
    result = data_sentences[:max_items]
    remaining = max_items - len(result)
    if remaining > 0:
        result.extend(other_sentences[:remaining])
    
    return result[:max_items]

def check_has_data(text):
    """检查文本中是否包含数据"""
    return bool(re.search(r'\d+(?:\.\d+)?(?:%|亿|万|元|美元)', text))

def check_is_concept_section(title):
    """检查是否是原创概念章节"""
    concept_keywords = ['原创', '概念', '首创', 'Concept', '创新理论']
    return any(kw in title for kw in concept_keywords)

# ============================================================
# 大纲生成函数
# ============================================================

def generate_outline(sections, report_title="研究报告"):
    """
    根据报告结构生成PPT大纲。
    
    参数：
        sections: 解析后的章节列表
        report_title: 报告标题
    
    返回：
        list: PPT页面列表
    """
    slides = []
    slide_num = 1
    
    # 第1页：封面
    slides.append({
        "num": slide_num,
        "layout": "cover",
        "title": report_title,
        "content": ["清新研究团队", f"{__import__('datetime').date.today().year}年"],
        "source_section": "封面",
        "source_text_excerpt": report_title
    })
    slide_num += 1
    
    # 第2页：目录
    chapter_titles = [s["title"] for s in sections if s["level"] <= 2][:10]
    slides.append({
        "num": slide_num,
        "layout": "toc",
        "title": "目录",
        "content": chapter_titles,
        "source_section": "目录",
        "source_text_excerpt": "章节列表"
    })
    slide_num += 1
    
    # 遍历每个章节
    for section in sections:
        title = section["title"]
        content = section["content"]
        subsections = section["subsections"]
        
        # 跳过空章节
        if not content.strip() and not subsections:
            continue
        
        # 章节分隔页
        if section["level"] <= 2:
            slides.append({
                "num": slide_num,
                "layout": "section_divider",
                "title": title,
                "content": [],
                "source_section": title,
                "source_text_excerpt": title
            })
            slide_num += 1
        
        # 原创概念页
        if check_is_concept_section(title):
            # 每个概念单独一页
            concept_blocks = re.split(r'(?=##\s+概念[一二三四五])', content)
            for block in concept_blocks:
                if block.strip():
                    key_points = extract_key_sentences(block, 4)
                    if key_points:
                        concept_title_match = re.search(r'概念[一二三四五]：(.+)', block)
                        c_title = concept_title_match.group(1) if concept_title_match else title
                        slides.append({
                            "num": slide_num,
                            "layout": "concept",
                            "title": c_title,
                            "content": key_points,
                            "source_section": title,
                            "source_text_excerpt": block[:200]
                        })
                        slide_num += 1
            continue
        
        # 主体内容页
        if content.strip():
            key_points = extract_key_sentences(content, 5)
            if key_points:
                layout = "data_chart" if check_has_data(content) else "title_content"
                slides.append({
                    "num": slide_num,
                    "layout": layout,
                    "title": title,
                    "content": key_points,
                    "source_section": title,
                    "source_text_excerpt": content[:200]
                })
                slide_num += 1
        
        # 子章节
        for sub in subsections:
            if sub["content"].strip():
                key_points = extract_key_sentences(sub["content"], 5)
                if key_points:
                    layout = "data_chart" if check_has_data(sub["content"]) else "title_content"
                    slides.append({
                        "num": slide_num,
                        "layout": layout,
                        "title": sub["title"],
                        "content": key_points,
                        "source_section": f"{title} > {sub['title']}",
                        "source_text_excerpt": sub["content"][:200]
                    })
                    slide_num += 1
    
    # 最后一页：结尾
    slides.append({
        "num": slide_num,
        "layout": "end",
        "title": "感谢阅读",
        "content": ["清新研究团队", "联系我们获取更多研究报告"],
        "source_section": "结尾",
        "source_text_excerpt": "致谢"
    })
    
    return slides

# ============================================================
# 主入口
# ============================================================

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 report_to_ppt_outline.py <input_report.md> <output_outline.json>")
        print()
        print("示例:")
        print("  python3 report_to_ppt_outline.py research_report_final.md ppt_outline.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: 文件未找到 {input_file}")
        sys.exit(1)

    print(f"📄 读取报告: {input_file} ({len(content)} 字)")

    # 提取报告标题
    title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    report_title = title_match.group(1).strip() if title_match else "研究报告"

    # 解析报告结构
    sections = parse_report_structure(content)
    print(f"📊 解析到 {len(sections)} 个章节")

    # 生成大纲
    slides = generate_outline(sections, report_title)
    
    # 输出
    outline = {
        "total_slides": len(slides),
        "report_source": input_file,
        "report_title": report_title,
        "slides": slides
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(outline, f, ensure_ascii=False, indent=2)

    print(f"✅ PPT 大纲已生成: {output_file}")
    print(f"📋 共 {len(slides)} 页 (根据报告内容弹性调整)")
    
    # 统计布局类型
    layout_counts = {}
    for s in slides:
        layout_counts[s["layout"]] = layout_counts.get(s["layout"], 0) + 1
    print("\n📊 布局类型分布:")
    for layout, count in sorted(layout_counts.items(), key=lambda x: -x[1]):
        print(f"   {layout}: {count} 页")

if __name__ == "__main__":
    main()

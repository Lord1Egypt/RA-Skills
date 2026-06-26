#!/usr/bin/env python3
"""
学术汇报PPT生成器 - 从文献PDF自动生成学术汇报PPT
"""

import json
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SlideContent:
    """单页PPT内容"""
    title: str
    bullets: List[str]
    notes: str = ""
    layout: str = "content"  # title, content, two-column, comparison


@dataclass
class PresentationStructure:
    """PPT整体结构"""
    title: str
    authors: str
    venue: str
    year: str
    
    # 第一部分：科学问题与背景 (1-2页)
    problem_slides: List[SlideContent]
    
    # 第二部分：方法 (2-3页)
    method_slides: List[SlideContent]
    
    # 第三部分：结论与验证 (多页)
    result_slides: List[SlideContent]
    
    # 第四部分：局限 (1页)
    limitation_slide: SlideContent
    
    # 总结页
    summary_slide: SlideContent


def create_ppt_structure(analysis_result: Dict[str, Any]) -> PresentationStructure:
    """
    根据文献分析结果创建PPT结构
    
    Args:
        analysis_result: 包含文献各部分分析结果的字典
        
    Returns:
        PresentationStructure: PPT结构对象
    """
    
    # 提取基本信息
    title = analysis_result.get("title", "研究标题")
    authors = analysis_result.get("authors", "作者")
    venue = analysis_result.get("venue", "发表期刊/会议")
    year = analysis_result.get("year", str(datetime.now().year))
    
    # ========== 第一部分：科学问题与背景 ==========
    problem_slides = []
    
    # 第1页：科学问题与背景
    problem_slide1 = SlideContent(
        title="研究背景与科学问题",
        bullets=[
            f"**核心问题**: {analysis_result.get('research_question', '待提取')}",
            "",
            "**研究背景**:",
            *[f"• {bg}" for bg in analysis_result.get('background', ['背景信息待提取'])],
            "",
            "**前人工作**:",
            *[f"• {work}" for work in analysis_result.get('previous_work', ['前人工作待提取'])]
        ],
        notes="这一页要快速让观众理解研究的大背景和核心问题",
        layout="content"
    )
    problem_slides.append(problem_slide1)
    
    # 第2页：研究空白与假设（如果需要）
    if analysis_result.get('research_gap') or analysis_result.get('hypothesis'):
        problem_slide2 = SlideContent(
            title="研究空白与理论假设",
            bullets=[
                "**现有研究的不足**:",
                *[f"• {gap}" for gap in analysis_result.get('research_gap', ['研究空白待提取'])],
                "",
                "**本研究的理论假设**:",
                *[f"• {hypo}" for hypo in analysis_result.get('hypothesis', ['假设待提取'])]
            ],
            notes="明确指出现有研究的gap，以及本研究如何解决",
            layout="content"
        )
        problem_slides.append(problem_slide2)
    
    # ========== 第二部分：方法 (2-3页) ==========
    method_slides = []
    
    # 方法第1页：总体设计
    method_slide1 = SlideContent(
        title="研究方法概述",
        bullets=[
            "**实验设计**:",
            *[f"• {design}" for design in analysis_result.get('experimental_design', ['实验设计待提取'])],
            "",
            "**被试/样本**:",
            f"• {analysis_result.get('participants', '被试信息待提取')}",
            "",
            "**核心变量**:",
            f"• 自变量: {analysis_result.get('independent_variables', '待提取')}",
            f"• 因变量: {analysis_result.get('dependent_variables', '待提取')}"
        ],
        notes="介绍实验的整体设计框架",
        layout="content"
    )
    method_slides.append(method_slide1)
    
    # 方法第2页：实验流程
    method_slide2 = SlideContent(
        title="实验流程",
        bullets=[
            "**实验步骤**:",
            *[f"{i+1}. {step}" for i, step in enumerate(analysis_result.get('procedure', ['步骤待提取']))],
            "",
            "**控制变量**:",
            *[f"• {control}" for control in analysis_result.get('control_variables', ['控制变量待提取'])]
        ],
        notes="详细说明实验如何进行，以及如何控制混淆变量",
        layout="content"
    )
    method_slides.append(method_slide2)
    
    # 方法第3页：方法-理论对应（如果需要）
    if analysis_result.get('method_theory_mapping'):
        method_slide3 = SlideContent(
            title="实验设计的理论依据",
            bullets=[
                "**实验设计如何验证假设**:",
                *[f"• {mapping}" for mapping in analysis_result.get('method_theory_mapping', [])],
                "",
                "**关键操作的理论意义**:",
                *[f"• {significance}" for significance in analysis_result.get('operational_significance', [])]
            ],
            notes="解释为什么这样设计实验，如何对应理论假设",
            layout="content"
        )
        method_slides.append(method_slide3)
    
    # ========== 第三部分：结论与验证 (多页) ==========
    result_slides = []
    
    # 主要发现（每页一个主要发现）
    main_findings = analysis_result.get('main_findings', ['主要发现待提取'])
    for i, finding in enumerate(main_findings):
        finding_slide = SlideContent(
            title=f"主要发现 {i+1}" if len(main_findings) > 1 else "主要发现",
            bullets=[
                f"**{finding}**",
                "",
                "**支持证据**:",
                *[f"• {evidence}" for evidence in analysis_result.get(f'evidence_{i}', ['证据待提取'])]
            ],
            notes=f"详细阐述第{i+1}个主要发现及其证据",
            layout="content"
        )
        result_slides.append(finding_slide)
    
    # 假设验证页
    hypothesis_validation = analysis_result.get('hypothesis_validation', [])
    if hypothesis_validation:
        validation_slide = SlideContent(
            title="假设验证结果",
            bullets=[
                "**假设检验**:",
                *[f"• {validation}" for validation in hypothesis_validation],
                "",
                "**结论逻辑链**:",
                *[f"→ {logic}" for logic in analysis_result.get('conclusion_logic', ['逻辑链待提取'])]
            ],
            notes="清晰展示每个假设是否被验证，以及验证的逻辑链条",
            layout="content"
        )
        result_slides.append(validation_slide)
    
    # ========== 第四部分：局限 (1页) ==========
    limitation_slide = SlideContent(
        title="研究局限与未来方向",
        bullets=[
            "**本研究的局限**:",
            *[f"• {limit}" for limit in analysis_result.get('limitations', ['局限待提取'])],
            "",
            "**未来研究方向**:",
            *[f"• {future}" for future in analysis_result.get('future_directions', ['未来方向待提取'])]
        ],
        notes="诚实说明研究局限，同时指出未来可以改进的方向",
        layout="content"
    )
    
    # ========== 总结页 ==========
    summary_slide = SlideContent(
        title="总结",
        bullets=[
            f"**{title}**",
            "",
            "**核心贡献**:",
            *[f"• {contrib}" for contrib in analysis_result.get('contributions', ['贡献待提取'])]
        ],
        notes="简洁总结研究的核心贡献",
        layout="content"
    )
    
    return PresentationStructure(
        title=title,
        authors=authors,
        venue=venue,
        year=year,
        problem_slides=problem_slides,
        method_slides=method_slides,
        result_slides=result_slides,
        limitation_slide=limitation_slide,
        summary_slide=summary_slide
    )


def structure_to_json(structure: PresentationStructure) -> Dict[str, Any]:
    """将PPT结构转换为JSON格式"""
    return {
        "title": structure.title,
        "authors": structure.authors,
        "venue": structure.venue,
        "year": structure.year,
        "slides": {
            "part1_problem": [asdict(slide) for slide in structure.problem_slides],
            "part2_method": [asdict(slide) for slide in structure.method_slides],
            "part3_results": [asdict(slide) for slide in structure.result_slides],
            "part4_limitations": asdict(structure.limitation_slide),
            "summary": asdict(structure.summary_slide)
        },
        "total_slides": (
            len(structure.problem_slides) +
            len(structure.method_slides) +
            len(structure.result_slides) +
            2  # limitations + summary
        )
    }


def main():
    """主函数 - 从JSON输入生成PPT结构"""
    if len(sys.argv) < 2:
        print("Usage: python generate_ppt_structure.py <analysis_json_file>")
        sys.exit(1)
    
    # 读取分析结果
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        analysis_result = json.load(f)
    
    # 生成PPT结构
    structure = create_ppt_structure(analysis_result)
    
    # 输出JSON
    output = structure_to_json(structure)
    
    # 处理Windows控制台编码问题
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

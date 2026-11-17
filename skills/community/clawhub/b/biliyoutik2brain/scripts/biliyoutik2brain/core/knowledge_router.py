#!/usr/bin/env python3
"""
知识路由器 — 转录后自动识别领域并分发到对应技能

职责：
1. 读取转录产物（MD 文件）
2. 提取关键词 + 复用 assess 的 domain_hint
3. 匹配技能路由表
4. 输出进化建议
5. 按需转格式（MD→HTML/JSON）

用法：
  python3 -m biliyoutik2brain.core.knowledge_router <transcript_md_path>
  python3 -m biliyoutik2brain.core.knowledge_router <transcript_md_path> --domain trading
  python3 -m biliyoutik2brain.core.knowledge_router <transcript_md_path> --output html

─ 格式契约（v2.0 Phase 2）─
输入：转录 MD 文件（任意路径）
输出：
  MD（原文保留）→ 归档 / AI 处理
  HTML → 用户直接阅读
  JSON → 程序消费（{domain, keywords, recommended_skills, analysis}）
消费方：
  HTML → 用户（人眼阅读）
  JSON → 下游技能触发（self-evolve / masterfangzheng 等）
  JSON.domain/keywords → knowledge-distributor（分发决策）
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 本地依赖：路径管理
from .paths import TRANSCRIPTS_DIR, KNOWLEDGE_DIR, storage_path

# 格式转换（从 common 层导入）
from ..common.format_converter import md_to_html, md_to_json

# json_to_html_rich 在本地 format_converter 中不存在，fallback 到 md_to_html
# TODO: need port from ZIP — json_to_html_rich 需要从 ZIP 源移植
try:
    from ..common.format_converter import json_to_html_rich
except ImportError:
    json_to_html_rich = None


# ═══════════════════════════════════════════════════════════════
# 领域关键词映射表
# ═══════════════════════════════════════════════════════════════

DOMAIN_KEYWORDS = {
    "trading": {
        "skills": ["masterfangzheng", "backtest-analyzer", "backtest-analyzer-edict"],
        "wetalk_context": "trading.md",
        "keywords": [
            "止损", "止盈", "盈亏比", "风险回报", "信号", "Pinbar", "孕线",
            "吞没", "支撑", "阻力", "供给区", "需求区", "订单流", "仓位",
            "分仓", "加仓", "减仓", "回测", "胜率", "交易", "K线", "均线",
            "ATR", "移动止损", "趋势", "震荡", "突破", "反转", "做多", "做空",
            "杠杆", "保证金", "点差", "滑点", "EA", "自动交易", "策略",
            "因子", "MA889", "1248", "共振", "风控", "三角", "张扬",
        ],
    },
    "ai": {
        "skills": ["schoolmate-jiang", "agent-evolver", "agent-browser"],
        "wetalk_context": "full.md",
        "keywords": [
            "AI", "人工智能", "大模型", "提示词", "Prompt", "Agent",
            "工作流", "Skill", "技能", "Claude", "GPT", "模型", "推理",
            "训练", "微调", "RAG", "向量", "Embedding", "Token",
            "API", "自动化", "LLM", "智能体", "多模态", "Agent",
            "采访式", "苏格拉底", "反思", "寓言", "HTML", "输出格式",
        ],
    },
    "methodology": {
        "skills": ["BG吴江数字人", "BG 吴江数字人"],
        "wetalk_context": "basic.md",
        "keywords": [
            "带人", "团队", "管理", "需求", "决策", "战略", "执行",
            "复盘", "方法论", "打法", "训战", "七二一", "凭什么",
            "角色", "付款者", "否决者", "使用者", "时间轴", "四层验证",
            "沟通", "配合", "汇报", "目标", "落地", "组织", "干部",
        ],
    },
    "product": {
        "skills": ["docx", "pptx", "excalidraw-skill"],
        "wetalk_context": "full.md",
        "keywords": [
            "产品", "设计", "原型", "需求", "用户", "体验", "交互",
            "文档", "PPT", "报告", "方案", "架构图", "流程图",
            "Excalidraw", "可视化", "画布", "白板",
        ],
    },
}


# ═══════════════════════════════════════════════════════════════
# 核心函数
# ═══════════════════════════════════════════════════════════════

def identify_domain(text: str, domain_hint: str = "") -> Tuple[str, Dict[str, int]]:
    """识别转录文本的领域

    Returns:
        (primary_domain, keyword_scores)
    """
    scores = {domain: 0 for domain in DOMAIN_KEYWORDS}

    # 如果有 domain_hint（来自 assess 节点），直接使用
    if domain_hint:
        hint_map = {
            "trading": "trading",
            "ai": "ai",
            "general": None,  # general 需要进一步判断
        }
        mapped = hint_map.get(domain_hint)
        if mapped:
            return mapped, scores

    # 关键词匹配
    text_lower = text.lower()
    for domain, config in DOMAIN_KEYWORDS.items():
        for keyword in config["keywords"]:
            count = len(re.findall(re.escape(keyword), text_lower))
            scores[domain] += count

    # 选最高分
    primary = max(scores, key=scores.get) if max(scores.values()) > 0 else "general"
    return primary, scores


def generate_routing(text: str, domain: str, scores: Dict[str, int],
                    source_url: str = "", uploader: str = "") -> dict:
    """生成路由建议"""
    config = DOMAIN_KEYWORDS.get(domain, {})
    skills = config.get("skills", [])

    # 提取关键知识点（前500字）
    text_preview = text[:500] if text else ""

    # 找匹配的关键词
    matched_keywords = []
    text_lower = text.lower()
    for kw in config.get("keywords", []):
        if kw.lower() in text_lower:
            matched_keywords.append(kw)

    return {
        "domain": domain,
        "confidence": sum(scores.values()),
        "recommended_skills": skills,
        "matched_keywords": matched_keywords[:10],
        "wetalk_context": config.get("wetalk_context", ""),
        "evolution_suggestion": {
            "action": "review_and_evolve" if skills else "archive_only",
            "reason": f"检测到 {domain} 领域内容，建议更新以下技能的知识库",
            "skills_to_evolve": skills,
            "knowledge_preview": text_preview[:200] + ("..." if len(text_preview) > 200 else ""),
        },
        "format_suggestion": {
            "primary": "markdown",
            "for_user": "html",
            "for_skills": "json",
        },
        "source_url": source_url,
        "uploader": uploader,
        "timestamp": datetime.now().isoformat(),
    }


def process_transcript(md_path: str, forced_domain: str = "",
                      output_format: str = "") -> dict:
    """处理转录文件

    Args:
        md_path: 转录 MD 文件路径
        forced_domain: 强制指定领域（可选）
        output_format: 指定输出格式（html/json，可选）
    """
    # 1. 读取转录文件
    if not os.path.exists(md_path):
        return {"error": f"文件不存在: {md_path}"}

    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()

    # 2. 提取元信息
    source_m = re.search(r'\*\*来源\*\*:\s+(.+)$', md_text, re.M)
    source_url = source_m.group(1).strip() if source_m else ""

    uploader_m = re.search(r'\*\*UP主\*\*:\s+(.+)$', md_text, re.M)
    uploader = uploader_m.group(1).strip() if uploader_m else ""

    # 3. 领域识别
    domain, scores = identify_domain(md_text)
    if forced_domain:
        domain = forced_domain

    # 4. 生成路由
    routing = generate_routing(md_text, domain, scores, source_url, uploader)

    # 5. 按需转格式
    outputs = {"markdown": md_path}

    if output_format == "html" or output_format == "all":
        json_path = md_path.replace(".md", ".json")
        # 优先从 JSON 生成 HTML（含增强字段），失败则从 MD 生成
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                json_data["routing"] = routing
                if json_to_html_rich is not None:
                    html_content = json_to_html_rich(json_data, routing.get("domain", "转录"))
                else:
                    html_content = md_to_html(md_text, routing.get("domain", "转录"))
            except Exception:
                html_content = md_to_html(md_text, routing.get("domain", "转录"))
        else:
            html_content = md_to_html(md_text, routing.get("domain", "转录"))
        html_path = md_path.replace(".md", ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        outputs["html"] = html_path
        print(f"  HTML: {html_path}")

    if output_format == "json" or output_format == "all":
        json_path = md_path.replace(".md", ".json")
        # 优先复用 save 节点写的完整 JSON（含增强字段）
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                json_data["routing"] = routing
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                outputs["json"] = json_path
                print(f"  JSON: {json_path} (patched routing)")
            except Exception:
                # 回退：从 MD 重建
                json_data = md_to_json(md_text)
                json_data["routing"] = routing
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                outputs["json"] = json_path
                print(f"  JSON: {json_path} (rebuilt from MD)")
        else:
            json_data = md_to_json(md_text)
            json_data["routing"] = routing
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            outputs["json"] = json_path
            print(f"  JSON: {json_path}")

    # 6. 输出路由结果
    routing["outputs"] = outputs

    return routing


# ═══════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="知识路由器")
    parser.add_argument("transcript", help="转录 MD 文件路径")
    parser.add_argument("--domain", choices=list(DOMAIN_KEYWORDS.keys()), help="强制指定领域")
    parser.add_argument("--output", choices=["html", "json", "all"], help="输出格式")

    args = parser.parse_args()

    result = process_transcript(args.transcript, args.domain, args.output)

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    # 打印路由结果
    print(f"\n{'='*60}")
    print(f"知识路由结果")
    print(f"{'='*60}")
    print(f"  领域: {result['domain']}")
    print(f"  置信度: {result['confidence']}")
    print(f"  推荐技能: {', '.join(result['recommended_skills']) or '无'}")
    print(f"  匹配关键词: {', '.join(result['matched_keywords'][:8]) or '无'}")
    print(f"\n  进化建议:")
    ev = result['evolution_suggestion']
    print(f"    动作: {ev['action']}")
    print(f"    原因: {ev['reason']}")
    print(f"    知识预览: {ev['knowledge_preview'][:100]}...")
    print(f"\n  输出文件:")
    for fmt, path in result['outputs'].items():
        print(f"    {fmt}: {path}")

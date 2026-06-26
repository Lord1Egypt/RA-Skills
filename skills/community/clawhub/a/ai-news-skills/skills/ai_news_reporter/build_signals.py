#!/usr/bin/env python3
"""
Build signal skeletons from event candidates.
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Optional


THEME_CHAINS = {
    "算力": ["芯片格局变化", "供给多元化", "成本下降", "应用可推广性提升"],
    "应用": ["通用Agent竞争", "垂直场景分化", "工作流设计", "落地效果验证"],
    "商业": ["企业感知成本", "实际成本", "效果匹配", "付费意愿"],
    "人才": ["岗位替代加速", "人才结构调整", "复合型人才溢价"],
    "安全": ["监管政策", "安全产品", "准入门槛", "差异化竞争力"],
    "资本": ["融资并购", "资源流向", "赛道拥挤度", "产业集中度"],
    "基础设施": ["模型能力提升", "工具链成熟", "交付门槛变化", "产品形态变化"],
}

NODE_KEYWORDS = {
    "成本下降": ["降价", "价格", "成本", "算力券", "补贴", "price", "cost", "pricing"],
    "应用可推广性提升": ["推广", "普及", "商用", "落地", "enterprise", "部署"],
    "垂直场景分化": ["垂直", "行业", "场景", "数字员工"],
    "工作流设计": ["workflow", "工作流", "agent", "copilot"],
    "落地效果验证": ["案例", "客户", "效果", "roi", "实践"],
    "企业感知成本": ["预算", "成本", "价格", "采购"],
    "实际成本": ["token", "推理", "inference", "成本"],
    "付费意愿": ["付费", "采购", "订单", "营收"],
    "模型能力提升": ["模型", "推理", "能力", "benchmark", "发布"],
    "工具链成熟": ["sdk", "框架", "平台", "工具链", "api"],
}


def clean_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def normalize_theme(value: str) -> str:
    return clean_text(value)


def choose_node(theme: str, event: Dict[str, object]) -> str:
    title = clean_text(str(event.get("event_title", ""))).lower()
    summary = clean_text(str(event.get("summary", ""))).lower()
    haystack = f"{title} {summary}"

    for node, keywords in NODE_KEYWORDS.items():
        if node not in THEME_CHAINS.get(theme, []):
            continue
        if any(keyword.lower() in haystack for keyword in keywords):
            return node

    chain = THEME_CHAINS.get(theme, [])
    return chain[0] if chain else ""


def build_problem_statement(theme: str, event: Dict[str, object], node: str) -> str:
    title = clean_text(str(event.get("event_title", "")))
    if theme == "算力":
        return f"{title} 反映出企业在 AI 使用中面临的供给或成本约束，当前重点节点是“{node}”。"
    if theme == "应用":
        return f"{title} 反映出 AI 应用从通用能力走向具体场景设计与落地验证，当前重点节点是“{node}”。"
    if theme == "商业":
        return f"{title} 指向企业对 AI 方案的成本、效果和付费匹配问题，当前重点节点是“{node}”。"
    return f"{title} 对应主题“{theme}”下的关键变化，当前重点节点是“{node}”。"


def build_old_solution(theme: str, node: str) -> str:
    defaults = {
        "算力": "过去主要依赖高成本算力和有限补贴，导致很多企业只停留在试点阶段。",
        "应用": "过去更多依赖通用型能力展示，缺少稳定的垂直场景工作流设计。",
        "商业": "过去常凭概念采购或试点推进，成本与效果的匹配并不清晰。",
        "人才": "过去以人工流程为主，AI 更多是辅助工具而非岗位重构工具。",
        "安全": "过去更偏事后治理，缺少面向 AI 业务准入的一体化机制。",
        "资本": "过去更多看单点公司故事，资源流向和产业集中趋势不够清晰。",
        "基础设施": "过去模型和工具链能力不足，交付门槛较高。",
    }
    return defaults.get(theme, f"过去在“{node}”这一环节的解决方案仍较粗糙。")


def build_new_solution(event: Dict[str, object], node: str) -> str:
    title = clean_text(str(event.get("event_title", "")))
    return f"{title} 提供了新的市场信号，显示“{node}”这一环节出现了新的推进条件或替代路径。"


def build_why_it_matters(theme: str, node: str, event: Dict[str, object]) -> str:
    count = int(event.get("source_count", 0) or 0)
    return f"该事件当前汇总了 {count} 条证据，说明主题“{theme}”在“{node}”节点出现了值得跟踪的新信号，可能推动既有判断更新。"


def build_signal(event: Dict[str, object]) -> Dict[str, object]:
    theme = normalize_theme(str(event.get("theme", "")))
    chain_nodes = THEME_CHAINS.get(theme, [])
    chain = " -> ".join(chain_nodes)
    node = choose_node(theme, event)
    event_id = clean_text(str(event.get("event_id", "")))

    return {
        "signal_id": f"sig-{event_id}" if event_id else "",
        "event_id": event_id,
        "theme": theme,
        "chain": chain,
        "node": node,
        "headline": clean_text(str(event.get("event_title", ""))),
        "problem_statement": build_problem_statement(theme, event, node),
        "old_solution": build_old_solution(theme, node),
        "new_solution": build_new_solution(event, node),
        "why_it_matters": build_why_it_matters(theme, node, event),
        "source_count": event.get("source_count", 0),
        "source_item_ids": event.get("source_item_ids", []),
        "version": 1,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build signal skeletons from event candidates.")
    parser.add_argument("--input", help="Path to event candidates JSON. Reads stdin when omitted.")
    return parser.parse_args()


def read_payload(path: Optional[str]) -> Dict[str, object]:
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def main() -> int:
    args = parse_args()
    payload = read_payload(args.input)
    events = payload.get("events", [])
    signals = [build_signal(event) for event in events]
    print(json.dumps({"total_signals": len(signals), "signals": signals}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

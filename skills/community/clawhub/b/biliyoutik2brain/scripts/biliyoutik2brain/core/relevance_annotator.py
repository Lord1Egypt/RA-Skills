"""
relevance_annotator.py — P0-1: 视频产物加"与你相关"标注

在视频转录产物保存后，用关键词匹配 USER.md / MEMORY.md / TODO.md / 1248定稿
中的关注点，在产物顶部插入相关性标注。

纯规则匹配，不依赖 LLM。
"""

import os
import re
import json
from typing import List, Tuple

from .paths import TRANSCRIPTS_DIR, NOTES_DIR


# ── 关注点来源 ──
_WORKSPACE = os.path.dirname(os.path.dirname(TRANSCRIPTS_DIR))
SOURCES = {
    "USER.md": os.path.join(_WORKSPACE, "USER.md"),
    "MEMORY.md": os.path.join(_WORKSPACE, "MEMORY.md"),
    "TODO.md": os.path.join(_WORKSPACE, "TODO.md"),
    "1248定稿": os.path.join(_WORKSPACE, "wiki/wiki/1248-v4.1-定稿.md"),
}

# 硬编码的核心关注映射 (key → 匹配词列表)
# 每次修改 USER.md/TODO.md 时手动同步此处（或定期从文件自动提取）
FOCUS_MAP = {
    "1248交易系统": [
        "1248", "R1", "R2", "R3", "R4", "信号", "止损", "止盈", "仓位",
        "MA889", "ATR", "因子", "张扬分仓", "风控", "回测", "EA",
        "isig", "真窗", "假窗", "开仓", "平仓", "以损定量",
    ],
    "FVG/订单流": [
        "FVG", "Fair Value Gap", "订单流", "机构订单", "缺口",
        "CE", "BISI", "SIBI", "Breakaway", "Exhaustion", "真空区",
        "OB", "Order Block", "流动性", "位移", "Displacement",
    ],
    "分形/多周期": [
        "分形", "多周期", "共振", "三门", "蒙提霍尔", "概率",
        "科赫", "曼德博", "自相似", "维度",
    ],
    "知识系统/管道": [
        "知识库", "知识图谱", "biliyoutik2brain", "转录", "whisper",
        "归档", "wiki", "knowledge", "路由", "蒸馏",
        "Obsidian", "画像", "管道", "管线",
    ],
    "AI/Agent": [
        "Agent", "智能体", "AI", "LLM", "self-evolve", "进化",
        "Claude", "Codex", "GPT", "提示词", "prompt", "MCP",
    ],
    "代码/架构": [
        "Python", "MT5", "MQL", "回测引擎", "解耦", "模块",
        "接口", "架构", "格式转换", "class",
    ],
    "EA审计": [
        "EA审计", "代码对齐", "定稿对比", "差异表",
    ],
}

# 标注模板（对应不同类别）
ANNOTATION_TEMPLATES = {
    "1248交易系统": (
        "> 🔗 **与你相关：1248交易系统**\n"
        "> 这个视频涉及你的1248信号体系。对照定稿检查："
        "是否有可以借鉴的规则/参数/过滤条件？\n"
    ),
    "FVG/订单流": (
        "> 🔗 **与你相关：FVG进场调优（§12）**\n"
        "> 这个视频涉及订单流/FVG分析。对照你的1248 FVG进场调优方案："
        "有新视角或新用法吗？\n"
    ),
    "分形/多周期": (
        "> 🔗 **与你相关：分形几何 & 多周期共振（§9~§11）**\n"
        "> 这个视频涉及分形/概率/多周期视角。"
        "1248定稿 §9~§11 已有相关讨论。\n"
    ),
    "知识系统/管道": (
        "> 🔗 **与你相关：biliyoutik2brain知识管道**\n"
        "> 这个视频涉及知识库/管道设计。"
        "对照你当前的 knowledge + wiki + 路由架构：有可借鉴的设计吗？\n"
    ),
    "AI/Agent": (
        "> 🔗 **与你相关：AI Agent 工具链**\n"
        "> 这个视频涉及AI/Agent能力。对照你的 self-evolve + 技能系统。\n"
    ),
    "代码/架构": (
        "> 🔗 **与你相关：代码/架构设计**\n"
        "> 这个视频涉及代码/架构方法。对照四大纪律八项注意。\n"
    ),
    "EA审计": (
        "> 🔗 **与你相关：EA审计器**\n"
        "> 这个视频涉及代码对齐/审计。对照你的 ea_audit.py 工作流。\n"
    ),
}


def match_focus(keywords: List[str], summary: str = "", title: str = "") -> List[Tuple[str, int]]:
    """
    用关键词匹配你的关注点。
    返回: [(关注类别, 命中数), ...] 按命中数降序
    """
    text = (title + " " + summary + " " + " ".join(keywords)).lower()
    hits = []
    for category, terms in FOCUS_MAP.items():
        score = 0
        matched = set()
        for term in terms:
            if term.lower() in text:
                score += 1
                matched.add(term)
        if score > 0:
            hits.append((category, score, matched))
    
    hits.sort(key=lambda x: -x[1])
    return [(cat, score) for cat, score, _ in hits]


def generate_annotation(hits: List[Tuple[str, int]]) -> str:
    """根据命中结果生成标注文本"""
    if not hits:
        return ""
    
    lines = ["---\n"]
    lines.append("## ⚡ 与你相关\n")
    
    for category, score in hits[:3]:  # 最多3个类别
        if category in ANNOTATION_TEMPLATES:
            lines.append(ANNOTATION_TEMPLATES[category])
        else:
            lines.append(f"> 🔗 **与你相关：{category}** (命中 {score} 个关键词)\n")
    
    lines.append("---\n")
    return "\n".join(lines)


def annotate_transcript(filepath: str, keywords: List[str], summary: str = "", title: str = "") -> bool:
    """
    将相关性标注插入到转录产物的顶部。
    返回 True 表示成功插入。
    """
    if not os.path.exists(filepath):
        return False
    
    hits = match_focus(keywords, summary, title)
    if not hits:
        return False
    
    annotation = generate_annotation(hits)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 避免重复标注
    if "## ⚡ 与你相关" in content:
        return False
    
    # 插入在标题后、转录文本前
    # 找第一个 ## 或 #  之后的第一个段落结束
    lines = content.split("\n")
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("## ") or line.startswith("# "):
            insert_at = i + 1
        # 跳过元数据行
        if line.startswith("**来源**") or line.startswith("**UP主**") or \
           line.startswith("**时长**") or line.startswith("**转录模型**") or \
           line.startswith("**管线耗时**"):
            insert_at = i + 1
    
    new_lines = lines[:insert_at + 1] + [annotation] + lines[insert_at + 1:]
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))
    
    cats = [cat for cat, _ in hits[:3]]
    print(f"  [与你相关] ✅ 标注已插入: {', '.join(cats)} → {os.path.basename(filepath)}")
    return True


def annotate_latest_transcript(save_result: dict, analysis: dict = None, video=None) -> bool:
    """
    管线的入口函数: 在 save 节点完成后调用。
    自动从 JSON 路由数据 + 转录文本提取关键词。
    """
    filepath = ""
    if isinstance(save_result, dict):
        filepath = save_result.get("file_path", "")
    if not filepath or not os.path.exists(filepath):
        return False
    
    keywords = []
    summary = ""
    title = ""
    
    # 方式1: 从 analysis dict 取（优先）
    if isinstance(analysis, dict):
        keywords = analysis.get("keywords", [])
        summary = analysis.get("summary", "")
    
    # 方式2: 从同名 JSON 文件的 routing 字段取（降级）
    if (not keywords or not summary) and filepath:
        json_path = filepath.rsplit(".")[0] + ".json"
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                routing = data.get("routing", {})
                if not keywords:
                    keywords = routing.get("matched_keywords", [])
                # 从转录文本开头取摘要
                text = data.get("text", "")
                if text:
                    summary = text[:300]
            except Exception:
                pass
    
    # 方式3: 从 MD 转录文本提取（最终降级）
    if not summary:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            # 找转录文本段
            m = re.search(r'## 转录文本\s*\n+(.*)', text, re.DOTALL)
            if m:
                summary = m.group(1).strip()[:500]
        except Exception:
            pass
    
    if video:
        title = getattr(video, "title", "")
    
    return annotate_transcript(filepath, keywords, summary, title)


# ── 命令行测试 ──
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        fp = sys.argv[1]
        hits = match_focus([], "", open(fp).read()[:2000] if os.path.exists(fp) else "")
        print("命中:", hits)
    else:
        # 自测
        kw = ["FVG", "订单流", "机构", "止损"]
        summary = "视频讲解了FVG的定义、形成原因和实战应用"
        title = "10分钟理解机构订单流的底层逻辑"
        hits = match_focus(kw, summary, title)
        print("命中:", hits)
        ann = generate_annotation(hits)
        print("\n标注:\n", ann)

"""
select_knowledge.py - 阶段 3：主题感知知识点筛选。

对应 video-editing-skills-main/scripts/select_clips.py，把"视频片段评分选片"
重映射为"教学知识点评分筛选"。

算法骨架（继承自 select_clips.py）：
  1. 主题关键词提取（中文 bigram 滑动窗口 + 否定词上下文感知）
  2. 片段打分（关键词命中 +1.0，负面词 -惩罚）
  3. 逐课程文件取最高分段（打散相邻同源）
  4. 凑够 min_knowledge（默认 6）个不同源的候选知识点
  5. 写 candidate_knowledge.json（V7 abstract_data 格式）

用法：
    python scripts/select_knowledge.py \\
        --output-reasoning "<workspace>/output_reasoning.json" \\
        --theme "机器学习入门" \\
        --output "<workspace>/candidate_knowledge.json" \\
        --min-knowledge 6
"""
from __future__ import annotations


# --- UTF-8 stdout/stderr (Windows 中文输出防乱码) -----------------------------
def _configure_stream_encoding(stream):
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")

import sys as _sys
_configure_stream_encoding(_sys.stdout)
_configure_stream_encoding(_sys.stderr)
del _sys
# ----------------------------------------------------------------------------

from log_util import get_logger

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# 默认参数
DEFAULT_MIN_KNOWLEDGE = 6  # 与 video-editing select_clips.py --min-videos=6 等价

# 负面词：出现这些词的段降分（对应 select_clips 的"背对镜头/看手机/画面模糊"）
NEGATIVE_WORDS = (
    "不相关", "过时", "已废弃", "模糊", "错误", "无关", "不重要",
    "重复", "冗余", "混乱", "难以理解", "不清晰",
)

# 否定词（用于上下文感知：否定词+关键词 时不加分）
NEGATION_WORDS = ("不", "非", "未", "没有", "无", "避免", "防止", "排除")


# ---------------------------------------------------------------------------
# 主题关键词提取（中文 bigram 滑动窗口）
# ---------------------------------------------------------------------------

def extract_keywords(theme: str) -> list[str]:
    """从主题字符串提取关键词。

    策略：
      1. 按标点/空格分词
      2. 中文部分用 bigram 滑动窗口（2 字符）
      3. 过滤停用词
    """
    if not theme:
        return []

    # 按非中文字符/非字母数字分割
    tokens = re.split(r"[^\u4e00-\u9fa5A-Za-z0-9]+", theme)
    keywords: list[str] = []

    for token in tokens:
        if not token:
            continue
        # 英文/数字 token 整体作为一个关键词
        if re.match(r"^[A-Za-z0-9]+$", token):
            keywords.append(token.lower())
            continue
        # 中文 token：bigram 滑动窗口
        if len(token) >= 2:
            for i in range(len(token) - 1):
                bigram = token[i:i + 2]
                keywords.append(bigram)
            # 整个 token 也作为一个关键词
            keywords.append(token)

    # 去重保序
    seen: set[str] = set()
    out: list[str] = []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out


# ---------------------------------------------------------------------------
# 片段打分
# ---------------------------------------------------------------------------

def score_segment(seg: dict, keywords: list[str]) -> float:
    """计算单个片段的主题相关性得分。

    规则：
      - knowledge_tags / seg_text 命中关键词：+1.0/词
      - 否定词上下文（"不"+关键词）：-1.0
      - 负面词命中：-2.0/词
      - 难度适中学段（1~4）：+0.5 加成
    """
    if not isinstance(seg, dict):
        return 0.0

    score = 0.0

    # 收集片段文本
    text = str(seg.get("seg_text", "")) + " " + " ".join(
        str(t) for t in seg.get("knowledge_tags", [])
    )
    text_lower = text.lower()

    # 关键词命中
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in text_lower:
            # 检查否定上下文
            idx = text_lower.find(kw_lower)
            prefix = text[max(0, idx - 2):idx]
            if any(neg in prefix for neg in NEGATION_WORDS):
                score -= 1.0  # 否定上下文
            else:
                score += 1.0

    # 负面词
    for neg in NEGATIVE_WORDS:
        if neg in text:
            score -= 2.0

    # 难度加成（1~4 为适中学段）
    difficulty = seg.get("difficulty", 0)
    if isinstance(difficulty, (int, float)) and 1 <= difficulty <= 4:
        score += 0.5

    # 主题不相关的段（analyze 阶段 1 判定不相关）大幅降分
    suggestion = str(seg.get("pedagogy_suggestion", ""))
    if "[主题不相关]" in suggestion:
        score -= 5.0

    return score


# ---------------------------------------------------------------------------
# 候选选择
# ---------------------------------------------------------------------------

def select_candidates(
    segments: list[dict],
    theme: str,
    min_knowledge: int = DEFAULT_MIN_KNOWLEDGE,
) -> list[dict]:
    """从所有片段中选出 ≥ min_knowledge 个不同源的候选知识点。

    策略（对应 select_clips.py）：
      1. 按得分降序排列
      2. 逐课程文件取最高分段（保证来源多样性）
      3. 凑够 min_knowledge 个不同源
      4. 相邻候选尽量来自不同文件（打散）
    """
    if not segments:
        return []

    keywords = extract_keywords(theme)

    # 打分
    scored = []
    for seg in segments:
        s = score_segment(seg, keywords)
        scored.append((s, seg))
    # 降序排列
    scored.sort(key=lambda x: x[0], reverse=True)

    # 按来源分组，每个来源取最高分
    by_source: dict[str, list[tuple[float, dict]]] = {}
    for s, seg in scored:
        src = seg.get("source_filename", seg.get("source_file", "unknown"))
        by_source.setdefault(src, []).append((s, seg))

    # 按每来源最高分排序来源
    source_ranked = sorted(
        by_source.items(),
        key=lambda kv: kv[1][0][0] if kv[1] else 0.0,
        reverse=True,
    )

    # 逐来源取最高分段，凑够 min_knowledge
    candidates: list[dict] = []
    for source, segs in source_ranked:
        if not segs:
            continue
        best_score, best_seg = segs[0]
        # 跳过得分过低的段（< 0 表示主题不相关或负面）
        if best_score < 0:
            continue
        candidate = {
            "source_file": best_seg.get("source_file", ""),
            "source_filename": best_seg.get("source_filename", source),
            "source_segment_id": best_seg.get("seg_id", 0),
            "seg_desc": best_seg.get("seg_text", ""),
            "knowledge_tags": best_seg.get("knowledge_tags", []),
            "difficulty": best_seg.get("difficulty", 2),
            "pedagogy_suggestion": best_seg.get("pedagogy_suggestion", ""),
            "theme_score": round(best_score, 2),
        }
        candidates.append(candidate)
        if len(candidates) >= min_knowledge:
            break

    # 如果不同源不够 min_knowledge，从剩余高分段补充（允许同源）
    if len(candidates) < min_knowledge:
        used_seg_ids = {c["source_segment_id"] for c in candidates}
        for s, seg in scored:
            if len(candidates) >= min_knowledge:
                break
            seg_id = seg.get("seg_id", 0)
            if seg_id in used_seg_ids:
                continue
            if s < 0:
                continue
            candidates.append({
                "source_file": seg.get("source_file", ""),
                "source_filename": seg.get("source_filename", ""),
                "source_segment_id": seg_id,
                "seg_desc": seg.get("seg_text", ""),
                "knowledge_tags": seg.get("knowledge_tags", []),
                "difficulty": seg.get("difficulty", 2),
                "pedagogy_suggestion": seg.get("pedagogy_suggestion", ""),
                "theme_score": round(s, 2),
            })
            used_seg_ids.add(seg_id)

    # 配对相邻段（paired_with_segment_id）——对应 select_clips 的 seg_n + seg_n+1 ≈ 6s
    # 教学场景：配对同源的下一段，形成 ~6 分钟教学单元
    for i, cand in enumerate(candidates):
        src = cand["source_filename"]
        cur_id = cand["source_segment_id"]
        # 找同源的下一个 segment
        paired = None
        for s, seg in scored:
            if (seg.get("source_filename") == src
                    and seg.get("seg_id") == cur_id + 1):
                paired = seg.get("seg_id")
                break
        cand["paired_with_segment_id"] = paired

    return candidates


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------

def build_output(segments: list[dict], theme: str,
                 min_knowledge: int, candidates: list[dict]) -> dict:
    """构建 candidate_knowledge.json（V7 abstract_data 格式）。"""
    unique_sources = {c["source_filename"] for c in candidates}
    return {
        "selection_metadata": {
            "theme": theme,
            "total_segments": len(segments),
            "selected_count": len(candidates),
            "unique_sources": len(unique_sources),
            "min_knowledge": min_knowledge,
        },
        "candidate_knowledge": candidates,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    log = get_logger("select")
    parser = argparse.ArgumentParser(description="阶段 3：主题感知知识点筛选")
    parser.add_argument(
        "--output-reasoning",
        required=True,
        help="analyze_courseware.py 输出的 output_reasoning.json 路径",
    )
    parser.add_argument("--theme", default=None, help="教学主题")
    parser.add_argument("--output", required=True, help="输出 candidate_knowledge.json 路径")
    parser.add_argument(
        "--min-knowledge",
        type=int,
        default=DEFAULT_MIN_KNOWLEDGE,
        help=f"最小候选知识点数（默认 {DEFAULT_MIN_KNOWLEDGE}）",
    )
    args = parser.parse_args()

    reasoning_path = Path(args.output_reasoning)
    if not reasoning_path.exists():
        log.error(f"错误：output_reasoning.json 不存在：{reasoning_path}")
        return 1

    try:
        data = json.loads(reasoning_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        log.error(f"错误：JSON 解析失败：{e}")
        return 1

    segments = data.get("segments", [])
    if not segments:
        log.error("错误：output_reasoning.json 中无 segments")
        return 1

    # 主题：优先 CLI 参数，其次 reasoning 文件中的 theme
    theme = args.theme or data.get("theme", "")
    log.info(f"[select] 主题：{theme or '（无）'}")
    log.info(f"[select] 总片段数：{len(segments)}")

    keywords = extract_keywords(theme)
    log.info(f"[select] 主题关键词：{keywords[:10]}{'...' if len(keywords) > 10 else ''}")

    candidates = select_candidates(segments, theme, min_knowledge=args.min_knowledge)
    log.info(f"[select] 选中 {len(candidates)} 个候选知识点")

    unique_sources = {c["source_filename"] for c in candidates}
    log.info(f"[select] 不同来源：{len(unique_sources)}")

    output = build_output(segments, theme, args.min_knowledge, candidates)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    size = output_path.stat().st_size
    log.info(f"[select] ✓ 输出：{output_path}（{size}B）")
    if size >= 10240:
        log.error(f"[select] ⚠ 输出 ≥ 10KB，端云交换时将被截断")

    print(str(output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())

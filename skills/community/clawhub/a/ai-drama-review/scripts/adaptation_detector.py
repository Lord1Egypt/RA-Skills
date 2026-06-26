"""
小说魔改检测器

比对原著与改编版本，量化改编偏离程度。
使用 Needleman-Wunsch 变体进行章节对齐。
包含角色弧线追踪与弧线偏离分析。
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from text_similarity import (
    preprocess_text, char_ngrams, jaccard_similarity,
    tokenize_chinese, compute_idf, build_tfidf_vector,
    cosine_similarity_vec,
)


@dataclass
class PlotPoint:
    """情节点。"""
    index: int
    summary: str
    characters: List[str] = field(default_factory=list)
    location: Optional[str] = None
    importance: str = "normal"  # "core" / "normal" / "minor"


@dataclass
class CharacterProfile:
    """角色概要。"""
    name: str
    traits: List[str] = field(default_factory=list)
    relationships: dict = field(default_factory=dict)
    fate: Optional[str] = None


@dataclass
class PhaseProfile:
    """角色在某一阶段的状态概要。"""
    phase: str                   # "beginning" / "middle" / "end"
    emotion_words: List[str]     # 该阶段该角色附近出现的情感词
    action_verbs: List[str]      # 该阶段该角色的主要动作词
    sentiment_score: float       # 情感极性得分 (-1.0 负面 ~ +1.0 正面)


@dataclass
class CharacterArc:
    """角色完整弧线。"""
    name: str
    mention_count: int
    phases: List[PhaseProfile] = field(default_factory=list)   # 3 phases
    arc_type: str = "unknown"    # "positive"/"negative"/"flat"/"reversal_tragic"/
                                 # "reversal_redemption"/"mixed"


@dataclass
class ArcDeviationItem:
    """角色弧线偏离项。"""
    character_name: str
    original_arc_type: str
    adapted_arc_type: str
    severity: str          # "minor"/"moderate"/"major"
    description: str


@dataclass
class DeviationItem:
    """偏离项。"""
    deviation_type: str  # "plot_added"/"plot_removed"/"plot_modified"
                         # "character_changed"/"setting_changed"
    original_content: str
    adapted_content: str
    severity: str        # "minor" / "moderate" / "major"
    description: str


@dataclass
class AdaptationReport:
    """改编检测报告。"""
    deviation_score: float        # 0-100
    adaptation_type: str          # "faithful"/"reasonable"/"severe_modification"
    total_deviations: int
    deviations_by_type: dict = field(default_factory=dict)
    deviations_by_severity: dict = field(default_factory=dict)
    deviation_items: List[DeviationItem] = field(default_factory=list)
    section_alignment: list = field(default_factory=list)
    character_arcs_original: List[CharacterArc] = field(default_factory=list)
    character_arcs_adapted: List[CharacterArc] = field(default_factory=list)
    arc_deviations: List[ArcDeviationItem] = field(default_factory=list)


# === 情感词与动作词词典 ===

POSITIVE_EMOTIONS = [
    "高兴", "开心", "快乐", "幸福", "欢喜", "满足", "欣慰", "感激", "希望",
    "勇敢", "坚定", "自信", "骄傲", "喜悦", "轻松", "释然", "温暖", "爱",
]
NEGATIVE_EMOTIONS = [
    "悲伤", "痛苦", "愤怒", "恐惧", "绝望", "孤独", "仇恨", "羞耻", "后悔",
    "焦虑", "迷茫", "失落", "委屈", "沮丧", "哭泣", "泪", "伤心", "难过",
]
ACTION_VERBS = [
    "战斗", "逃跑", "救助", "背叛", "牺牲", "复仇", "原谅", "放弃", "坚持",
    "保护", "攻击", "逃离", "追求", "失去", "获得", "死亡", "重生", "成长",
]


# === 文本结构提取 ===

def extract_sections(text: str) -> List[dict]:
    """
    提取章节/段落结构。

    尝试按章节标题分割，如果没有明确标题则按段落分割。
    """
    # 尝试按中文章节标题分割
    chapter_pattern = r'(第[一二三四五六七八九十百千\d]+[章节回集幕][\s：:]*[^\n]*)'
    chapters = re.split(chapter_pattern, text)

    sections = []
    if len(chapters) > 1:
        # 有明确章节标题
        i = 0
        while i < len(chapters):
            if re.match(chapter_pattern, chapters[i]):
                title = chapters[i].strip()
                content = chapters[i + 1].strip() if i + 1 < len(chapters) else ""
                sections.append({"title": title, "content": content})
                i += 2
            else:
                if chapters[i].strip():
                    sections.append({"title": "", "content": chapters[i].strip()})
                i += 1
    else:
        # 按段落分割
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        for i, para in enumerate(paragraphs):
            if len(para) >= 15:  # 过滤过短段落
                sections.append({"title": f"段落{i + 1}", "content": para})

    return sections


def _quick_similarity(text_a: str, text_b: str) -> float:
    """快速计算两段文本的相似度（用于对齐）。"""
    if not text_a or not text_b:
        return 0.0

    # 使用字符 n-gram Jaccard 作为快速相似度
    ngrams_a = char_ngrams(text_a, n=3)
    ngrams_b = char_ngrams(text_b, n=3)
    return jaccard_similarity(ngrams_a, ngrams_b)


# === 章节对齐 ===

def align_sections(original_sections: list, adapted_sections: list) -> list:
    """
    基于 Needleman-Wunsch 变体的章节对齐。

    Returns:
        [(orig_idx_or_None, adapted_idx_or_None, similarity, status), ...]
        status: "matched" / "added" / "removed" / "modified"
    """
    m = len(original_sections)
    n = len(adapted_sections)

    if m == 0 and n == 0:
        return []
    if m == 0:
        return [(None, j, 0.0, "added") for j in range(n)]
    if n == 0:
        return [(i, None, 0.0, "removed") for i in range(m)]

    # 构建相似度矩阵
    sim_matrix = [[0.0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            sim_matrix[i][j] = _quick_similarity(
                original_sections[i]["content"],
                adapted_sections[j]["content"],
            )

    # 动态规划
    GAP_PENALTY = -0.1
    dp = [[0.0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] + GAP_PENALTY
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] + GAP_PENALTY

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match_score = dp[i - 1][j - 1] + sim_matrix[i - 1][j - 1]
            skip_orig = dp[i - 1][j] + GAP_PENALTY
            skip_adapt = dp[i][j - 1] + GAP_PENALTY
            dp[i][j] = max(match_score, skip_orig, skip_adapt)

    # 回溯
    alignment = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + sim_matrix[i - 1][j - 1]:
            sim = sim_matrix[i - 1][j - 1]
            status = "matched" if sim >= 0.3 else "modified"
            alignment.append((i - 1, j - 1, sim, status))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + GAP_PENALTY:
            alignment.append((i - 1, None, 0.0, "removed"))
            i -= 1
        else:
            alignment.append((None, j - 1, 0.0, "added"))
            j -= 1

    alignment.reverse()
    return alignment


# === 角色分析 ===

def extract_characters_local(text: str) -> List[str]:
    """本地方式提取角色名（基于高频重复的短词）。"""
    # 简单启发式：提取引号中出现的称呼和高频 2-3 字名
    names = set()

    # 提取对话前的称呼
    speaker_pattern = r'(\S{2,4})[说道叫喊问答笑哭]'
    for match in re.finditer(speaker_pattern, text):
        name = match.group(1)
        if len(name) <= 4 and not any(c.isdigit() for c in name):
            names.add(name)

    return list(names)


def _extract_frequent_names(text: str, min_count: int = 3) -> List[tuple]:
    """
    提取在文本中出现 min_count 次以上的 2-4 字候选角色名。

    Returns:
        List of (name, count) sorted by count descending.
    """
    # 匹配 2-4 个汉字组成的词语序列
    candidate_pattern = re.compile(r'[\u4e00-\u9fff]{2,4}')
    candidates: dict = {}
    for match in candidate_pattern.finditer(text):
        word = match.group()
        # 排除常见非人名词汇（简单过滤）
        if word in {"这个", "那个", "什么", "因为", "所以", "但是", "然后",
                    "这样", "那样", "如果", "虽然", "已经", "还是", "只是",
                    "可以", "没有", "知道", "觉得", "看到", "听到", "时候",
                    "一个", "两个", "他们", "她们", "我们", "你们", "大家",
                    "一起", "一直", "一下", "一样", "不是", "不会", "不能",
                    "不要", "不用", "不行", "不好", "不对", "开始", "结束"}:
            continue
        candidates[word] = candidates.get(word, 0) + 1

    result = [(name, cnt) for name, cnt in candidates.items() if cnt >= min_count]
    result.sort(key=lambda x: x[1], reverse=True)
    return result


# === 角色弧线提取 ===

def _collect_nearby_words(text: str, name: str, window: int = 30) -> tuple:
    """
    在文本中找到所有包含 name 的位置，收集前后 window 个字符范围内的
    情感词和动作词。

    Returns:
        (emotion_words, action_verbs, positive_count, negative_count)
    """
    emotion_words: List[str] = []
    action_verbs_found: List[str] = []
    positive_count = 0
    negative_count = 0

    for match in re.finditer(re.escape(name), text):
        start = max(0, match.start() - window)
        end = min(len(text), match.end() + window)
        context = text[start:end]

        for word in POSITIVE_EMOTIONS:
            if word in context:
                emotion_words.append(word)
                positive_count += 1

        for word in NEGATIVE_EMOTIONS:
            if word in context:
                emotion_words.append(word)
                negative_count += 1

        for verb in ACTION_VERBS:
            if verb in context:
                action_verbs_found.append(verb)

    return emotion_words, action_verbs_found, positive_count, negative_count


def _determine_arc_type(scores: List[float]) -> str:
    """根据三个阶段情感分数推断弧线类型。"""
    if len(scores) < 3:
        return "unknown"

    s0, s1, s2 = scores[0], scores[1], scores[2]

    if s0 > 0.2 and s2 < -0.2:
        return "reversal_tragic"
    if s0 < -0.2 and s2 > 0.2:
        return "reversal_redemption"
    if abs(s2 - s0) < 0.3:
        return "flat"
    if s2 > s0 + 0.2:
        return "positive"
    if s2 < s0 - 0.2:
        return "negative"
    return "mixed"


def extract_character_arcs(text: str) -> List[CharacterArc]:
    """
    从文本中提取所有主要角色的完整弧线。

    流程:
    1. 从 extract_characters_local 和高频词提取中合并角色候选列表
    2. 对出现次数 >= 3 的角色，按文本三等分划分阶段
    3. 在各阶段中收集情感词、动作词，计算情感极性
    4. 推断弧线类型

    Returns:
        List[CharacterArc]
    """
    if not text:
        return []

    # 合并两种提取方式的角色候选
    local_names = set(extract_characters_local(text))
    freq_names = {name for name, _ in _extract_frequent_names(text, min_count=3)}
    all_candidates = local_names | freq_names

    # 计算每个候选在全文中的真实出现次数
    name_counts: dict = {}
    for name in all_candidates:
        count = len(re.findall(re.escape(name), text))
        if count >= 3:
            name_counts[name] = count

    if not name_counts:
        return []

    # 按出现次数排序，取前 20 个以控制性能
    sorted_names = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)[:20]

    text_len = len(text)
    phase_boundaries = [
        (0, text_len // 3, "beginning"),
        (text_len // 3, text_len * 2 // 3, "middle"),
        (text_len * 2 // 3, text_len, "end"),
    ]

    arcs: List[CharacterArc] = []

    for name, mention_count in sorted_names:
        phases: List[PhaseProfile] = []
        phase_scores: List[float] = []

        for phase_start, phase_end, phase_label in phase_boundaries:
            phase_text = text[phase_start:phase_end]
            emotion_words, action_verbs_found, pos_cnt, neg_cnt = _collect_nearby_words(
                phase_text, name, window=30
            )
            sentiment_score = (pos_cnt - neg_cnt) / max(pos_cnt + neg_cnt, 1)
            phase_scores.append(sentiment_score)

            phases.append(PhaseProfile(
                phase=phase_label,
                emotion_words=list(dict.fromkeys(emotion_words)),   # deduplicate, keep order
                action_verbs=list(dict.fromkeys(action_verbs_found)),
                sentiment_score=round(sentiment_score, 4),
            ))

        arc_type = _determine_arc_type(phase_scores)

        arcs.append(CharacterArc(
            name=name,
            mention_count=mention_count,
            phases=phases,
            arc_type=arc_type,
        ))

    return arcs


# === 角色弧线比对 ===

def _names_match(name_a: str, name_b: str) -> bool:
    """判断两个角色名是否指同一角色（支持全名/简称匹配）。"""
    a, b = name_a.lower(), name_b.lower()
    if a == b:
        return True
    # 部分匹配：一个是另一个的子串（处理全名 vs 简称）
    if a in b or b in a:
        return True
    return False


def _arc_deviation_severity(orig_type: str, adapt_type: str) -> str:
    """根据弧线类型差异判断偏离严重程度。"""
    if orig_type == adapt_type:
        return ""   # 无偏离，调用方检查空字符串

    # 完全反转：positive ↔ negative
    polar_opposites = {("positive", "negative"), ("negative", "positive")}
    if (orig_type, adapt_type) in polar_opposites:
        return "major"

    # flat ↔ reversal_X 视为重大改动
    reversal_types = {"reversal_tragic", "reversal_redemption"}
    if orig_type == "flat" and adapt_type in reversal_types:
        return "major"
    if adapt_type == "flat" and orig_type in reversal_types:
        return "major"

    # 任一侧含 reversal — 结局改变
    if orig_type in reversal_types or adapt_type in reversal_types:
        return "moderate"

    # 同为 flat 但方向不同（由调用方判断），其余情况为 minor
    return "minor"


def compare_character_arcs(
    orig_arcs: List[CharacterArc],
    adapt_arcs: List[CharacterArc],
) -> List[ArcDeviationItem]:
    """
    比对原著与改编版本的角色弧线，生成弧线偏离列表。

    Args:
        orig_arcs: 原著角色弧线列表
        adapt_arcs: 改编版角色弧线列表

    Returns:
        List[ArcDeviationItem]
    """
    deviations: List[ArcDeviationItem] = []

    matched_adapt_indices: set = set()

    for orig_arc in orig_arcs:
        # 在改编版中寻找匹配角色
        best_idx: Optional[int] = None
        for idx, adapt_arc in enumerate(adapt_arcs):
            if idx in matched_adapt_indices:
                continue
            if _names_match(orig_arc.name, adapt_arc.name):
                best_idx = idx
                break

        if best_idx is not None:
            matched_adapt_indices.add(best_idx)
            adapt_arc = adapt_arcs[best_idx]

            severity = _arc_deviation_severity(orig_arc.arc_type, adapt_arc.arc_type)
            if not severity:
                # 弧线类型相同，无偏离
                continue

            # 生成描述
            desc = (
                f"原著角色「{orig_arc.name}」弧线为 {orig_arc.arc_type}，"
                f"改编后变为 {adapt_arc.arc_type}"
            )
            if severity == "major":
                if (orig_arc.arc_type, adapt_arc.arc_type) in {
                    ("positive", "negative"), ("negative", "positive")
                }:
                    desc += "（完全性格/命运反转）"
                else:
                    desc += "（重大弧线改动）"
            elif severity == "moderate":
                desc += "（结局走向发生变化）"
            else:
                desc += "（轻微弧线偏离）"

            deviations.append(ArcDeviationItem(
                character_name=orig_arc.name,
                original_arc_type=orig_arc.arc_type,
                adapted_arc_type=adapt_arc.arc_type,
                severity=severity,
                description=desc,
            ))
        else:
            # 原著角色在改编中未出现（mentions 不足）
            if orig_arc.mention_count >= 10:
                severity = "major"
            elif orig_arc.mention_count >= 5:
                severity = "moderate"
            else:
                severity = "minor"

            deviations.append(ArcDeviationItem(
                character_name=orig_arc.name,
                original_arc_type=orig_arc.arc_type,
                adapted_arc_type="character_removed",
                severity=severity,
                description=(
                    f"原著角色「{orig_arc.name}」（出现 {orig_arc.mention_count} 次）"
                    f"在改编版中消失或戏份不足"
                ),
            ))

    # 改编版新增角色（未在原著中出现）
    for idx, adapt_arc in enumerate(adapt_arcs):
        if idx in matched_adapt_indices:
            continue

        orig_match = any(_names_match(adapt_arc.name, o.name) for o in orig_arcs)
        if orig_match:
            continue

        severity = "major" if adapt_arc.mention_count > 5 else "minor"
        deviations.append(ArcDeviationItem(
            character_name=adapt_arc.name,
            original_arc_type="character_added",
            adapted_arc_type=adapt_arc.arc_type,
            severity=severity,
            description=(
                f"改编版新增角色「{adapt_arc.name}」（出现 {adapt_arc.mention_count} 次），"
                f"原著中不存在"
            ),
        ))

    return deviations


# === 偏离度计算 ===

def _classify_deviation_severity(sim: float, status: str) -> str:
    """判定偏离严重程度。"""
    if status == "removed":
        return "major"
    if status == "added":
        return "moderate"
    if status == "modified":
        if sim >= 0.5:
            return "minor"
        if sim >= 0.2:
            return "moderate"
        return "major"
    return "minor"


def build_deviations(alignment: list, original_sections: list,
                     adapted_sections: list) -> List[DeviationItem]:
    """从对齐结果构建偏离项列表。"""
    deviations = []

    for orig_idx, adapt_idx, sim, status in alignment:
        if status == "matched":
            continue

        orig_content = (original_sections[orig_idx]["content"][:200]
                        if orig_idx is not None else "")
        adapt_content = (adapted_sections[adapt_idx]["content"][:200]
                         if adapt_idx is not None else "")

        severity = _classify_deviation_severity(sim, status)

        if status == "removed":
            desc = f"原著段落被删除"
            dev_type = "plot_removed"
        elif status == "added":
            desc = f"新增了原著中没有的内容"
            dev_type = "plot_added"
        else:
            desc = f"内容被修改（相似度: {sim:.2f}）"
            dev_type = "plot_modified"

        deviations.append(DeviationItem(
            deviation_type=dev_type,
            original_content=orig_content,
            adapted_content=adapt_content,
            severity=severity,
            description=desc,
        ))

    return deviations


def calculate_deviation_score(deviations: List[DeviationItem],
                              total_sections: int) -> float:
    """
    计算偏离度评分 (0-100)。

    权重设计：
    - plot_removed × 3.0（删除原著核心最严重）
    - plot_modified × 2.0
    - plot_added × 1.0
    - character_changed × 2.5
    - setting_changed × 1.5
    严重度加权：minor × 0.5, moderate × 1.0, major × 2.0
    """
    if not deviations or total_sections == 0:
        return 0.0

    severity_weights = {"minor": 0.5, "moderate": 1.0, "major": 2.0}
    type_weights = {
        "plot_removed": 3.0,
        "plot_modified": 2.0,
        "plot_added": 1.0,
        "character_changed": 2.5,
        "setting_changed": 1.5,
    }

    weighted_sum = 0.0
    for d in deviations:
        sw = severity_weights.get(d.severity, 1.0)
        tw = type_weights.get(d.deviation_type, 1.0)
        weighted_sum += sw * tw

    # 归一化到 0-100
    max_possible = total_sections * 3.0 * 2.0  # 全部为 major + removed
    score = min(100.0, (weighted_sum / max(max_possible, 1)) * 100)
    return round(score, 1)


def classify_adaptation(score: float) -> str:
    """分类改编类型。"""
    if score <= 30:
        return "faithful"
    if score <= 60:
        return "reasonable"
    return "severe_modification"


# === 主入口 ===

def detect_adaptation(original_text: str, adapted_text: str) -> AdaptationReport:
    """
    完整的魔改检测流程，含角色弧线追踪。

    Args:
        original_text: 原著全文
        adapted_text: 改编版全文

    Returns:
        AdaptationReport
    """
    # 提取结构
    orig_sections = extract_sections(original_text)
    adapt_sections = extract_sections(adapted_text)

    if not orig_sections and not adapt_sections:
        return AdaptationReport(
            deviation_score=0.0,
            adaptation_type="faithful",
            total_deviations=0,
        )

    # 章节对齐
    alignment = align_sections(orig_sections, adapt_sections)

    # 构建情节偏离项
    deviations = build_deviations(alignment, orig_sections, adapt_sections)

    # 角色弧线分析
    orig_arcs = extract_character_arcs(original_text)
    adapt_arcs = extract_character_arcs(adapted_text)
    arc_deviations = compare_character_arcs(orig_arcs, adapt_arcs)

    # 将弧线偏离转换为 DeviationItem 并合并进总偏离列表，参与评分
    for arc_dev in arc_deviations:
        orig_label = arc_dev.original_arc_type
        adapt_label = arc_dev.adapted_arc_type
        deviations.append(DeviationItem(
            deviation_type="character_changed",
            original_content=f"角色 {arc_dev.character_name} 弧线: {orig_label}",
            adapted_content=f"角色 {arc_dev.character_name} 弧线: {adapt_label}",
            severity=arc_dev.severity,
            description=arc_dev.description,
        ))

    # 计算偏离度
    total_sections = max(len(orig_sections), len(adapt_sections))
    score = calculate_deviation_score(deviations, total_sections)
    adaptation_type = classify_adaptation(score)

    # 统计
    by_type: dict = {}
    by_severity: dict = {}
    for d in deviations:
        by_type[d.deviation_type] = by_type.get(d.deviation_type, 0) + 1
        by_severity[d.severity] = by_severity.get(d.severity, 0) + 1

    return AdaptationReport(
        deviation_score=score,
        adaptation_type=adaptation_type,
        total_deviations=len(deviations),
        deviations_by_type=by_type,
        deviations_by_severity=by_severity,
        deviation_items=deviations,
        section_alignment=[(o, a, s, st) for o, a, s, st in alignment],
        character_arcs_original=orig_arcs,
        character_arcs_adapted=adapt_arcs,
        arc_deviations=arc_deviations,
    )


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="小说魔改检测")
    parser.add_argument("--original", required=True, help="原著文件路径")
    parser.add_argument("--adapted", required=True, help="改编版文件路径")
    args = parser.parse_args()

    orig_path = Path(args.original)
    adapt_path = Path(args.adapted)

    if not orig_path.exists():
        print(f"错误: 原著文件不存在: {orig_path}")
        sys.exit(1)
    if not adapt_path.exists():
        print(f"错误: 改编文件不存在: {adapt_path}")
        sys.exit(1)

    original = orig_path.read_text(encoding="utf-8")
    adapted = adapt_path.read_text(encoding="utf-8")

    report = detect_adaptation(original, adapted)

    print(f"=== 小说魔改检测报告 ===")
    print(f"偏离度评分: {report.deviation_score}/100")
    print(f"改编类型: {report.adaptation_type}")
    print(f"总偏离数: {report.total_deviations}")
    print(f"按类型: {json.dumps(report.deviations_by_type, ensure_ascii=False)}")
    print(f"按严重度: {json.dumps(report.deviations_by_severity, ensure_ascii=False)}")

    if report.deviation_items:
        # 仅显示非角色弧线的情节偏离（前 10 条）
        plot_devs = [d for d in report.deviation_items
                     if d.deviation_type != "character_changed"]
        if plot_devs:
            print(f"\n情节偏离详情:")
            for d in plot_devs[:10]:
                print(f"  [{d.severity}] {d.description}")
                if d.original_content:
                    print(f"    原文: {d.original_content[:80]}...")
                if d.adapted_content:
                    print(f"    改编: {d.adapted_content[:80]}...")

    # 角色弧线分析摘要
    orig_valid = [a for a in report.character_arcs_original if a.arc_type != "unknown"]
    adapt_valid = [a for a in report.character_arcs_adapted if a.arc_type != "unknown"]

    print(f"\n角色弧线分析:")
    print(f"  原著角色: {len(report.character_arcs_original)} 个"
          f"（有效弧线 {len(orig_valid)} 个）")
    print(f"  改编角色: {len(report.character_arcs_adapted)} 个"
          f"（有效弧线 {len(adapt_valid)} 个）")
    print(f"  弧线偏离: {len(report.arc_deviations)} 处")

    if report.arc_deviations:
        # 按严重度排序输出：major 优先
        severity_order = {"major": 0, "moderate": 1, "minor": 2}
        sorted_arc_devs = sorted(
            report.arc_deviations,
            key=lambda x: severity_order.get(x.severity, 9),
        )
        for arc_dev in sorted_arc_devs:
            orig_label = arc_dev.original_arc_type
            adapt_label = arc_dev.adapted_arc_type
            print(f"  [{arc_dev.severity}] {arc_dev.character_name}: "
                  f"原著{orig_label} → 改编{adapt_label}"
                  f"（{arc_dev.description.split('（')[-1].rstrip('）') if '（' in arc_dev.description else arc_dev.description}）")

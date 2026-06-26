"""
文本相似度检测引擎

用于版权侵权检测，支持三种互补的相似度算法：
- n-gram Jaccard 系数（局部词汇重复）
- 归一化编辑距离（整体文本差异）
- TF-IDF 余弦相似度（语义主题相似）

纯 Python 实现，不依赖外部 NLP 库。
"""

import math
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class SimilarityResult:
    """单段相似度检测结果。"""
    source_paragraph_index: int
    source_text: str
    reference_id: str
    reference_paragraph_index: int
    reference_text: str
    ngram_jaccard: float
    edit_distance_normalized: float
    cosine_similarity: float
    combined_score: float
    is_suspicious: bool


@dataclass
class CopyrightReport:
    """版权检测报告。"""
    total_paragraphs: int
    suspicious_paragraphs: int
    max_similarity_score: float
    risk_level: str  # "low" / "medium" / "high" / "critical"
    results: List[SimilarityResult] = field(default_factory=list)
    window_matches: List["WindowMatch"] = field(default_factory=list)


@dataclass
class WindowMatch:
    """滑动窗口匹配结果。"""
    source_start_char: int       # 在输入文本中的起始字符位置
    source_end_char: int         # 结束字符位置
    source_text: str             # 命中窗口文本（截断到100字）
    reference_id: str            # 参考文本ID
    reference_start_char: int    # 参考文本中的起始位置
    reference_text: str          # 参考窗口文本（截断到100字）
    combined_score: float        # 相似度得分
    window_index: int            # 第几个窗口


# === 文本预处理 ===

def preprocess_text(text: str) -> str:
    """统一编码、去标点、去多余空白。"""
    # Unicode 归一化
    text = unicodedata.normalize("NFKC", text)
    # 去除标点
    text = re.sub(r'[^\w\s]', '', text)
    # 合并多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()


def split_paragraphs(text: str, min_length: int = 20) -> List[str]:
    """按段落分割文本，过滤过短段落。"""
    paragraphs = re.split(r'\n\s*\n|\n', text)
    return [p.strip() for p in paragraphs if len(p.strip()) >= min_length]


def tokenize_chinese(text: str) -> List[str]:
    """中文分词（优先 jieba，降级到字符级）。"""
    try:
        import jieba
        return list(jieba.cut(text))
    except ImportError:
        # 降级：按字符分词，保留连续英文/数字为整词
        tokens = []
        current_ascii = []
        for char in text:
            if char.isascii() and char.isalnum():
                current_ascii.append(char)
            else:
                if current_ascii:
                    tokens.append(''.join(current_ascii))
                    current_ascii = []
                if char.strip():
                    tokens.append(char)
        if current_ascii:
            tokens.append(''.join(current_ascii))
        return tokens


# === n-gram 相似度 ===

def char_ngrams(text: str, n: int = 3) -> set:
    """生成字符级 n-gram 集合。"""
    text = preprocess_text(text)
    if len(text) < n:
        return {text} if text else set()
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def word_ngrams(tokens: list, n: int = 2) -> set:
    """生成词级 n-gram 集合。"""
    if len(tokens) < n:
        return {tuple(tokens)} if tokens else set()
    return {tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def jaccard_similarity(set_a: set, set_b: set) -> float:
    """Jaccard 系数 = |A ∩ B| / |A ∪ B|。"""
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


# === 编辑距离 ===

def edit_distance(s1: str, s2: str) -> int:
    """Levenshtein 编辑距离（空间优化为 O(min(m,n))）。"""
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    prev_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (0 if c1 == c2 else 1)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    return prev_row[-1]


def normalized_edit_distance(s1: str, s2: str) -> float:
    """归一化编辑距离 = edit_distance / max(len(s1), len(s2))。"""
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 0.0
    return edit_distance(s1, s2) / max_len


# === TF-IDF 余弦相似度 ===

def compute_idf(corpus: List[List[str]]) -> dict:
    """计算逆文档频率（平滑版，避免 log(1)=0 的问题）。"""
    doc_count = len(corpus)
    if doc_count == 0:
        return {}

    df = {}
    for tokens in corpus:
        seen = set(tokens)
        for token in seen:
            df[token] = df.get(token, 0) + 1

    return {
        token: math.log((doc_count + 1) / (count + 1)) + 1.0
        for token, count in df.items()
    }


def build_tfidf_vector(tokens: list, idf_dict: dict) -> dict:
    """构建 TF-IDF 向量。"""
    tf = {}
    for token in tokens:
        tf[token] = tf.get(token, 0) + 1

    total = len(tokens) if tokens else 1
    return {
        token: (count / total) * idf_dict.get(token, 1.0)
        for token, count in tf.items()
    }


def cosine_similarity_vec(vec_a: dict, vec_b: dict) -> float:
    """余弦相似度。"""
    common_keys = set(vec_a.keys()) & set(vec_b.keys())
    dot_product = sum(vec_a[k] * vec_b[k] for k in common_keys)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


# === 综合比对 ===

def combine_scores(ngram_sim: float, edit_dist_norm: float,
                   cosine_sim: float) -> float:
    """综合评分（加权平均）。"""
    edit_sim = 1.0 - edit_dist_norm
    return 0.3 * ngram_sim + 0.3 * edit_sim + 0.4 * cosine_sim


def compare_paragraphs(para_a: str, para_b: str,
                       idf_dict: dict = None) -> dict:
    """计算两段文本的全部相似度指标。"""
    # n-gram Jaccard
    ngrams_a = char_ngrams(para_a, n=3)
    ngrams_b = char_ngrams(para_b, n=3)
    ngram_sim = jaccard_similarity(ngrams_a, ngrams_b)

    # 编辑距离
    preprocessed_a = preprocess_text(para_a)
    preprocessed_b = preprocess_text(para_b)
    edit_dist = normalized_edit_distance(preprocessed_a, preprocessed_b)

    # TF-IDF 余弦
    tokens_a = tokenize_chinese(preprocessed_a)
    tokens_b = tokenize_chinese(preprocessed_b)

    if idf_dict is None:
        idf_dict = compute_idf([tokens_a, tokens_b])

    vec_a = build_tfidf_vector(tokens_a, idf_dict)
    vec_b = build_tfidf_vector(tokens_b, idf_dict)
    cosine_sim = cosine_similarity_vec(vec_a, vec_b)

    combined = combine_scores(ngram_sim, edit_dist, cosine_sim)

    return {
        "ngram_jaccard": round(ngram_sim, 4),
        "edit_distance_normalized": round(edit_dist, 4),
        "cosine_similarity": round(cosine_sim, 4),
        "combined_score": round(combined, 4),
    }


def _determine_risk_level(max_score: float, suspicious_count: int,
                          total: int) -> str:
    """根据检测结果确定风险等级。"""
    if suspicious_count == 0:
        return "low"
    ratio = suspicious_count / total if total > 0 else 0
    if max_score >= 0.95 or ratio >= 0.5:
        return "critical"
    if max_score >= 0.85 or ratio >= 0.3:
        return "high"
    if max_score >= 0.7 or ratio >= 0.1:
        return "medium"
    return "low"


# === 滑动窗口扫描 ===

def sliding_window_scan(
    input_text: str,
    reference_texts: dict,
    window_size: int = 80,
    stride: int = 40,
    threshold: float = 0.65,
    idf_dict: dict = None,
) -> List[WindowMatch]:
    """
    滑动窗口扫描：在全文上用固定大小窗口滑动，
    检测跨段落的部分抄录（段落级检测漏掉的情况）。

    Args:
        input_text: 待检全文
        reference_texts: {"source_id": "全文内容", ...}
        window_size: 窗口大小（字符数），默认80字
        stride: 步长（字符数），默认40字（50%重叠）
        threshold: 判定阈值（低于段落级的0.7，因为窗口更短）
        idf_dict: 预建的IDF字典（没有则自动构建）

    Returns:
        List[WindowMatch]，按 combined_score 降序
    """
    # 1. 清理输入文本：去除多余空白但保留结构
    cleaned_input = re.sub(r'[^\S\n]+', ' ', input_text).strip()

    if len(cleaned_input) < window_size:
        return []

    # 2. 创建输入文本的窗口列表: [(start, end, text_slice), ...]
    input_windows = [
        (start, start + window_size, cleaned_input[start:start + window_size])
        for start in range(0, len(cleaned_input) - window_size, stride)
    ]

    if not input_windows:
        return []

    # 3. 清理参考文本并构建各参考文本的窗口
    ref_windows: dict = {}
    for ref_id, ref_text in reference_texts.items():
        cleaned_ref = re.sub(r'[^\S\n]+', ' ', ref_text).strip()
        if len(cleaned_ref) < window_size:
            # 参考文本比窗口还短，作为单一窗口处理
            if cleaned_ref:
                ref_windows[ref_id] = [(0, len(cleaned_ref), cleaned_ref)]
        else:
            ref_windows[ref_id] = [
                (start, start + window_size, cleaned_ref[start:start + window_size])
                for start in range(0, len(cleaned_ref) - window_size, stride)
            ]

    if not ref_windows:
        return []

    # 4. 构建全局 IDF（如果未提供）
    if idf_dict is None:
        all_token_lists = []
        for _, _, win_text in input_windows:
            all_token_lists.append(
                tokenize_chinese(preprocess_text(win_text))
            )
        for ref_id, wins in ref_windows.items():
            for _, _, win_text in wins:
                all_token_lists.append(
                    tokenize_chinese(preprocess_text(win_text))
                )
        idf_dict = compute_idf(all_token_lists)

    # 5. 对每个输入窗口与所有参考窗口比较，收集超过阈值的匹配
    raw_matches: List[WindowMatch] = []

    for win_idx, (src_start, src_end, src_text) in enumerate(input_windows):
        best_score = 0.0
        best_match: Optional[WindowMatch] = None

        for ref_id, wins in ref_windows.items():
            for ref_start, ref_end, ref_text in wins:
                scores = compare_paragraphs(src_text, ref_text, idf_dict)
                if scores["combined_score"] > best_score:
                    best_score = scores["combined_score"]
                    best_match = WindowMatch(
                        source_start_char=src_start,
                        source_end_char=src_end,
                        source_text=src_text[:100],
                        reference_id=ref_id,
                        reference_start_char=ref_start,
                        reference_text=ref_text[:100],
                        combined_score=scores["combined_score"],
                        window_index=win_idx,
                    )

        if best_match is not None and best_match.combined_score >= threshold:
            raw_matches.append(best_match)

    if not raw_matches:
        return []

    # 6. 去重：合并重叠窗口（source_start_char 区间重叠 > 60%），保留得分最高者
    # 先按起始位置排序，方便线性合并
    raw_matches.sort(key=lambda m: m.source_start_char)

    def _overlap_ratio(a: WindowMatch, b: WindowMatch) -> float:
        """计算两个窗口在源文本上的重叠比例（相对于较短区间长度）。"""
        overlap_start = max(a.source_start_char, b.source_start_char)
        overlap_end = min(a.source_end_char, b.source_end_char)
        if overlap_end <= overlap_start:
            return 0.0
        overlap_len = overlap_end - overlap_start
        shorter_len = min(
            a.source_end_char - a.source_start_char,
            b.source_end_char - b.source_start_char,
        )
        return overlap_len / shorter_len if shorter_len > 0 else 0.0

    deduped: List[WindowMatch] = []
    for candidate in raw_matches:
        merged = False
        for i, kept in enumerate(deduped):
            if _overlap_ratio(candidate, kept) > 0.6:
                # 同一重叠组：保留得分更高的那个
                if candidate.combined_score > kept.combined_score:
                    deduped[i] = candidate
                merged = True
                break
        if not merged:
            deduped.append(candidate)

    # 7. 按得分降序排列
    deduped.sort(key=lambda m: m.combined_score, reverse=True)
    return deduped


def scan_for_plagiarism(
    input_text: str,
    reference_texts: dict,
    threshold: float = 0.7,
    include_window_scan: bool = True,
) -> CopyrightReport:
    """
    主入口：扫描输入文本与参考文本库的相似度。

    Args:
        input_text: 待检剧本全文
        reference_texts: {"source_id": "全文内容", ...}
        threshold: 判定阈值 (默认 0.7)
        include_window_scan: 是否执行滑动窗口扫描（默认 True）

    Returns:
        CopyrightReport
    """
    input_paragraphs = split_paragraphs(input_text)

    if not input_paragraphs:
        return CopyrightReport(
            total_paragraphs=0,
            suspicious_paragraphs=0,
            max_similarity_score=0.0,
            risk_level="low",
        )

    # 构建参考文本段落
    ref_paragraphs = {}
    for ref_id, ref_text in reference_texts.items():
        ref_paragraphs[ref_id] = split_paragraphs(ref_text)

    # 构建全局 IDF
    all_token_lists = []
    for para in input_paragraphs:
        all_token_lists.append(tokenize_chinese(preprocess_text(para)))
    for ref_id, paras in ref_paragraphs.items():
        for para in paras:
            all_token_lists.append(tokenize_chinese(preprocess_text(para)))
    global_idf = compute_idf(all_token_lists)

    # 逐段比对
    results = []
    for i, input_para in enumerate(input_paragraphs):
        best_match = None
        best_score = 0.0

        for ref_id, ref_paras in ref_paragraphs.items():
            for j, ref_para in enumerate(ref_paras):
                scores = compare_paragraphs(input_para, ref_para, global_idf)
                if scores["combined_score"] > best_score:
                    best_score = scores["combined_score"]
                    best_match = SimilarityResult(
                        source_paragraph_index=i,
                        source_text=input_para[:100],
                        reference_id=ref_id,
                        reference_paragraph_index=j,
                        reference_text=ref_para[:100],
                        ngram_jaccard=scores["ngram_jaccard"],
                        edit_distance_normalized=scores["edit_distance_normalized"],
                        cosine_similarity=scores["cosine_similarity"],
                        combined_score=scores["combined_score"],
                        is_suspicious=scores["combined_score"] >= threshold,
                    )

        if best_match and best_match.is_suspicious:
            results.append(best_match)

    suspicious_count = len(results)
    max_score = max((r.combined_score for r in results), default=0.0)

    # 滑动窗口扫描
    window_matches: List[WindowMatch] = []
    if include_window_scan:
        raw_window_matches = sliding_window_scan(
            input_text,
            reference_texts,
            threshold=0.65,
            idf_dict=global_idf,
        )

        # 仅保留未被段落级检测覆盖的窗口匹配
        # 构建段落级命中的字符区间（基于分割后段落在原文中的近似位置）
        # 用更轻量的方式：检查窗口文本与已有可疑段落文本是否高度重叠
        suspicious_texts = {r.source_text for r in results}

        for wm in raw_window_matches:
            # 如果窗口文本（截断100字）已经完整出现在某个可疑段落中则跳过
            already_covered = any(
                wm.source_text[:60] in st or st[:60] in wm.source_text
                for st in suspicious_texts
            )
            if not already_covered:
                window_matches.append(wm)

        # 更新 max_score（窗口匹配也纳入考量）
        if window_matches:
            win_max = max(wm.combined_score for wm in window_matches)
            max_score = max(max_score, win_max)

    # 计算最终风险等级（综合段落命中和窗口命中数量）
    effective_suspicious = suspicious_count + len(window_matches)
    effective_total = max(len(input_paragraphs), 1)

    return CopyrightReport(
        total_paragraphs=len(input_paragraphs),
        suspicious_paragraphs=suspicious_count,
        max_similarity_score=round(max_score, 4),
        risk_level=_determine_risk_level(
            max_score, effective_suspicious, effective_total
        ),
        results=results,
        window_matches=window_matches,
    )


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="文本相似度检测")
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument("--reference-dir", required=True, help="参考文本目录")
    parser.add_argument("--threshold", type=float, default=0.7, help="判定阈值")
    parser.add_argument(
        "--no-window-scan",
        action="store_true",
        help="禁用滑动窗口扫描",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        sys.exit(1)

    input_text = input_path.read_text(encoding="utf-8")

    ref_dir = Path(args.reference_dir)
    reference_texts = {}
    if ref_dir.exists():
        for f in ref_dir.glob("*.txt"):
            reference_texts[f.stem] = f.read_text(encoding="utf-8")

    report = scan_for_plagiarism(
        input_text,
        reference_texts,
        args.threshold,
        include_window_scan=not args.no_window_scan,
    )

    print(f"=== 版权侵权检测报告 ===")
    print(f"总段落数: {report.total_paragraphs}")
    print(f"可疑段落: {report.suspicious_paragraphs}")
    print(f"最高相似度: {report.max_similarity_score}")
    print(f"风险等级: {report.risk_level}")
    print(f"滑动窗口命中: {len(report.window_matches)}")

    if report.results:
        print(f"\n可疑段落详情:")
        for r in report.results:
            print(f"\n  段落 {r.source_paragraph_index}: "
                  f"综合得分 {r.combined_score:.4f}")
            print(f"  来源: {r.reference_id} 段落 {r.reference_paragraph_index}")
            print(f"  原文: {r.source_text[:60]}...")
            print(f"  参考: {r.reference_text[:60]}...")

    if report.window_matches:
        print(f"\nTop 3 滑动窗口命中:")
        for wm in report.window_matches[:3]:
            print(f"\n  窗口 #{wm.window_index} "
                  f"[字符 {wm.source_start_char}-{wm.source_end_char}]: "
                  f"综合得分 {wm.combined_score:.4f}")
            print(f"  来源: {wm.reference_id} "
                  f"[字符 {wm.reference_start_char}-]")
            print(f"  原文: {wm.source_text[:60]}...")
            print(f"  参考: {wm.reference_text[:60]}...")

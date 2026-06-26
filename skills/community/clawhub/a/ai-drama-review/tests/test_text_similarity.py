"""文本相似度测试"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from text_similarity import (
    preprocess_text, split_paragraphs, char_ngrams, word_ngrams,
    jaccard_similarity, edit_distance, normalized_edit_distance,
    cosine_similarity_vec, build_tfidf_vector, compute_idf,
    combine_scores, compare_paragraphs, scan_for_plagiarism,
    tokenize_chinese, CopyrightReport, SimilarityResult,
)


def test_preprocess_text():
    """测试文本预处理。"""
    result = preprocess_text("Hello, World! 你好，世界！")
    assert "," not in result, "应去除标点"
    assert "hello" in result, "应转小写"
    print("文本预处理: PASS")
    return True


def test_split_paragraphs():
    """测试段落分割。"""
    text = "这是第一段，有足够长的内容来测试。\n\n这是第二段，也有足够长的内容。\n短"
    paragraphs = split_paragraphs(text, min_length=10)
    assert len(paragraphs) == 2, f"应有 2 个段落，得到 {len(paragraphs)}"
    print("段落分割: PASS")
    return True


def test_char_ngrams():
    """测试字符 n-gram 生成。"""
    ngrams = char_ngrams("abcde", n=3)
    assert ngrams == {"abc", "bcd", "cde"}, f"n-gram 结果错误: {ngrams}"
    print("字符 n-gram: PASS")
    return True


def test_jaccard_identical():
    """测试完全相同文本的 Jaccard 系数。"""
    set_a = char_ngrams("这是一段测试文本用来验证", n=3)
    set_b = char_ngrams("这是一段测试文本用来验证", n=3)
    sim = jaccard_similarity(set_a, set_b)
    assert sim == 1.0, f"完全相同文本的 Jaccard 应为 1.0, 得到 {sim}"
    print("Jaccard 相同文本: PASS")
    return True


def test_jaccard_different():
    """测试完全不同文本的 Jaccard 系数。"""
    set_a = char_ngrams("今天天气真好啊非常不错", n=3)
    set_b = char_ngrams("明天我要去上学读书写字", n=3)
    sim = jaccard_similarity(set_a, set_b)
    assert sim < 0.3, f"差异文本的 Jaccard 应较低, 得到 {sim}"
    print("Jaccard 不同文本: PASS")
    return True


def test_jaccard_empty():
    """测试空集合的 Jaccard。"""
    assert jaccard_similarity(set(), set()) == 1.0
    assert jaccard_similarity({"a"}, set()) == 0.0
    print("Jaccard 空集: PASS")
    return True


def test_edit_distance_identical():
    """测试相同字符串的编辑距离。"""
    dist = edit_distance("hello", "hello")
    assert dist == 0, f"相同字符串编辑距离应为 0, 得到 {dist}"
    print("编辑距离(相同): PASS")
    return True


def test_edit_distance_known():
    """测试已知编辑距离。"""
    dist = edit_distance("kitten", "sitting")
    assert dist == 3, f"kitten->sitting 应为 3, 得到 {dist}"
    print("编辑距离(已知): PASS")
    return True


def test_normalized_edit_distance():
    """测试归一化编辑距离。"""
    dist = normalized_edit_distance("abc", "abc")
    assert dist == 0.0, f"相同文本归一化距离应为 0, 得到 {dist}"

    dist = normalized_edit_distance("abc", "xyz")
    assert dist == 1.0, f"完全不同文本归一化距离应为 1, 得到 {dist}"
    print("归一化编辑距离: PASS")
    return True


def test_cosine_similarity():
    """测试余弦相似度。"""
    vec_a = {"a": 1.0, "b": 2.0, "c": 3.0}
    vec_b = {"a": 1.0, "b": 2.0, "c": 3.0}
    sim = cosine_similarity_vec(vec_a, vec_b)
    assert abs(sim - 1.0) < 0.001, f"相同向量余弦应为 1.0, 得到 {sim}"

    vec_c = {"x": 1.0, "y": 2.0}
    sim2 = cosine_similarity_vec(vec_a, vec_c)
    assert sim2 == 0.0, f"无交集向量余弦应为 0, 得到 {sim2}"
    print("余弦相似度: PASS")
    return True


def test_combine_scores():
    """测试综合评分。"""
    score = combine_scores(1.0, 0.0, 1.0)
    assert abs(score - 1.0) < 0.001, f"完美分数应为 1.0, 得到 {score}"

    score = combine_scores(0.0, 1.0, 0.0)
    assert abs(score - 0.0) < 0.001, f"最低分应为 0.0, 得到 {score}"
    print("综合评分: PASS")
    return True


def test_compare_paragraphs():
    """测试段落比对。"""
    scores = compare_paragraphs("这是完全相同的测试文本", "这是完全相同的测试文本")
    assert scores["combined_score"] >= 0.9, f"相同段落得分应高, 得到 {scores['combined_score']}"
    print("段落比对: PASS")
    return True


def test_scan_plagiarism_identical():
    """测试完全抄袭检测。"""
    text = "从前有座山，山上有座庙，庙里有个老和尚在讲故事。讲的什么故事呢？从前有座山。"
    refs = {"source_1": "从前有座山，山上有座庙，庙里有个老和尚在讲故事。讲的什么故事呢？从前有座山。"}
    report = scan_for_plagiarism(text, refs, threshold=0.7)
    assert isinstance(report, CopyrightReport)
    assert report.risk_level in ("high", "critical"), \
        f"完全抄袭应为高风险, 得到 {report.risk_level}"
    print("完全抄袭检测: PASS")
    return True


def test_scan_plagiarism_original():
    """测试原创内容检测。"""
    text = "在一个遥远的星球上，有一种能够发光的植物。它们在夜晚绽放，照亮整个峡谷。"
    refs = {"source_1": "今天的天气真好，我打算去公园散步，然后去超市买些水果回来。"}
    report = scan_for_plagiarism(text, refs, threshold=0.7)
    assert report.risk_level == "low", \
        f"原创内容应为低风险, 得到 {report.risk_level}"
    print("原创内容检测: PASS")
    return True


def test_scan_empty_input():
    """测试空输入处理。"""
    report = scan_for_plagiarism("", {}, threshold=0.7)
    assert report.total_paragraphs == 0
    assert report.risk_level == "low"
    print("空输入处理: PASS")
    return True


def test_tokenize_chinese():
    """测试中文分词。"""
    tokens = tokenize_chinese("我今天去公园散步")
    assert len(tokens) > 0, "分词结果不应为空"
    print("中文分词: PASS")
    return True


if __name__ == "__main__":
    print("=== 文本相似度测试 ===\n")

    tests = [
        test_preprocess_text,
        test_split_paragraphs,
        test_char_ngrams,
        test_jaccard_identical,
        test_jaccard_different,
        test_jaccard_empty,
        test_edit_distance_identical,
        test_edit_distance_known,
        test_normalized_edit_distance,
        test_cosine_similarity,
        test_combine_scores,
        test_compare_paragraphs,
        test_scan_plagiarism_identical,
        test_scan_plagiarism_original,
        test_scan_empty_input,
        test_tokenize_chinese,
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"  FAIL: {test.__name__}: {e}")
            results.append(False)

    passed = sum(results)
    total = len(results)
    print(f"\n总计: {passed}/{total} 通过")
    sys.exit(0 if passed == total else 1)

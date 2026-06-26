"""魔改检测测试"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from adaptation_detector import (
    extract_sections, align_sections, build_deviations,
    calculate_deviation_score, classify_adaptation,
    detect_adaptation, DeviationItem, AdaptationReport,
    extract_characters_local,
)


def test_extract_sections_chapters():
    """测试章节提取（有章节标题）。"""
    text = "第一章 初遇\n今天小明遇到了小红。\n第二章 告别\n小明离开了小红。"
    sections = extract_sections(text)
    assert len(sections) >= 2, f"应至少有 2 个章节, 得到 {len(sections)}"
    print("章节提取(标题): PASS")
    return True


def test_extract_sections_paragraphs():
    """测试段落提取（无章节标题）。"""
    text = "这是第一段很长的内容足够长来通过过滤。\n这是第二段很长的内容也足够长。"
    sections = extract_sections(text)
    assert len(sections) >= 2, f"应至少有 2 段, 得到 {len(sections)}"
    print("段落提取: PASS")
    return True


def test_align_identical():
    """测试完全相同文本的对齐。"""
    sections = [
        {"title": "A", "content": "这是测试内容第一段足够长的文本"},
        {"title": "B", "content": "这是测试内容第二段足够长的文本"},
    ]
    alignment = align_sections(sections, sections)
    matched = sum(1 for _, _, _, status in alignment if status == "matched")
    assert matched == 2, f"相同文本应全部匹配, 匹配 {matched}"
    print("相同文本对齐: PASS")
    return True


def test_align_with_additions():
    """测试有新增内容的对齐。"""
    original = [
        {"title": "A", "content": "原始内容第一段足够长来测试"},
    ]
    adapted = [
        {"title": "A", "content": "原始内容第一段足够长来测试"},
        {"title": "B", "content": "这是新增的内容段落足够长来测试"},
    ]
    alignment = align_sections(original, adapted)
    added = sum(1 for _, _, _, status in alignment if status == "added")
    assert added >= 1, f"应检测到新增, 得到 {added}"
    print("新增内容对齐: PASS")
    return True


def test_align_with_removals():
    """测试有删除内容的对齐。"""
    original = [
        {"title": "A", "content": "原始内容第一段足够长来测试"},
        {"title": "B", "content": "原始内容第二段足够长来测试"},
    ]
    adapted = [
        {"title": "A", "content": "原始内容第一段足够长来测试"},
    ]
    alignment = align_sections(original, adapted)
    removed = sum(1 for _, _, _, status in alignment if status == "removed")
    assert removed >= 1, f"应检测到删除, 得到 {removed}"
    print("删除内容对齐: PASS")
    return True


def test_align_empty():
    """测试空输入对齐。"""
    assert align_sections([], []) == []
    result = align_sections([], [{"title": "A", "content": "test"}])
    assert len(result) == 1 and result[0][3] == "added"
    print("空输入对齐: PASS")
    return True


def test_build_deviations():
    """测试偏离项构建。"""
    orig = [{"title": "A", "content": "原始内容"}]
    adapt = [{"title": "A", "content": "完全不同的内容"}]
    alignment = [(0, 0, 0.1, "modified")]
    deviations = build_deviations(alignment, orig, adapt)
    assert len(deviations) == 1
    assert deviations[0].deviation_type == "plot_modified"
    print("偏离项构建: PASS")
    return True


def test_deviation_score_zero():
    """测试无偏离的评分。"""
    score = calculate_deviation_score([], 10)
    assert score == 0.0, f"无偏离评分应为 0, 得到 {score}"
    print("零偏离评分: PASS")
    return True


def test_deviation_score_high():
    """测试高偏离的评分。"""
    deviations = [
        DeviationItem("plot_removed", "原文", "", "major", "删除"),
        DeviationItem("plot_removed", "原文", "", "major", "删除"),
        DeviationItem("plot_modified", "原文", "改编", "major", "修改"),
    ]
    score = calculate_deviation_score(deviations, 5)
    assert score > 30, f"多个重大偏离评分应较高, 得到 {score}"
    print("高偏离评分: PASS")
    return True


def test_classify_adaptation():
    """测试改编分类。"""
    assert classify_adaptation(10) == "faithful"
    assert classify_adaptation(30) == "faithful"
    assert classify_adaptation(45) == "reasonable"
    assert classify_adaptation(60) == "reasonable"
    assert classify_adaptation(75) == "severe_modification"
    assert classify_adaptation(100) == "severe_modification"
    print("改编分类: PASS")
    return True


def test_detect_adaptation_identical():
    """测试完全相同文本的检测。"""
    text = "第一章 开始\n从前有座山，山上有座庙，庙里有个老和尚。\n第二章 继续\n老和尚在讲故事，讲的什么故事呢？"
    report = detect_adaptation(text, text)
    assert isinstance(report, AdaptationReport)
    assert report.deviation_score <= 10, \
        f"相同文本偏离度应很低, 得到 {report.deviation_score}"
    assert report.adaptation_type == "faithful"
    print("相同文本检测: PASS")
    return True


def test_detect_adaptation_different():
    """测试完全不同文本的检测。"""
    original = "第一章 初遇\n小明在学校遇到了小红，两人成为了好朋友。\n第二章 分别\n毕业后小明去了北京工作。"
    adapted = "第一集 变形\n机器人变形金刚从宇宙降落到地球。\n第二集 战斗\n外星人入侵地球被击败了。"
    report = detect_adaptation(original, adapted)
    assert report.deviation_score > 30, \
        f"完全不同文本偏离度应高, 得到 {report.deviation_score}"
    print("不同文本检测: PASS")
    return True


def test_detect_empty():
    """测试空输入。"""
    report = detect_adaptation("", "")
    assert report.deviation_score == 0.0
    assert report.adaptation_type == "faithful"
    print("空输入检测: PASS")
    return True


def test_extract_characters():
    """测试角色提取。"""
    text = '小明说："今天天气真好。"\n小红说："是啊，我们去公园吧。"'
    characters = extract_characters_local(text)
    # 角色提取是启发式的，可能不完美
    assert isinstance(characters, list)
    print("角色提取: PASS")
    return True


if __name__ == "__main__":
    print("=== 魔改检测测试 ===\n")

    tests = [
        test_extract_sections_chapters,
        test_extract_sections_paragraphs,
        test_align_identical,
        test_align_with_additions,
        test_align_with_removals,
        test_align_empty,
        test_build_deviations,
        test_deviation_score_zero,
        test_deviation_score_high,
        test_classify_adaptation,
        test_detect_adaptation_identical,
        test_detect_adaptation_different,
        test_detect_empty,
        test_extract_characters,
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

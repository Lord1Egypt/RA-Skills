"""年龄分级检测测试"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from age_rating_scanner import (
    load_keyword_database, load_all_keywords, load_rating_rules,
    scan_keywords, calculate_initial_rating,
    run_age_rating_scan, KeywordHit, RatingResult,
    analyze_frame_descriptions, analyze_audio_transcript,
)


def test_load_keyword_database():
    """测试关键词库加载。"""
    db = load_keyword_database("violence")
    assert "keywords" in db, "缺少 keywords 字段"
    assert len(db["keywords"]) > 0, "关键词库为空"
    assert db["category"] == "violence"
    print("关键词库加载: PASS")
    return True


def test_load_all_keywords():
    """测试加载全部关键词库。"""
    all_kw = load_all_keywords()
    expected_cats = ["violence", "sexual", "horror", "profanity", "substance"]
    for cat in expected_cats:
        assert cat in all_kw, f"缺少类别: {cat}"
        assert len(all_kw[cat]) > 0, f"{cat} 关键词库为空"
    print("全部关键词库: PASS")
    return True


def test_load_rating_rules():
    """测试分级规则加载。"""
    rules = load_rating_rules("china")
    assert "ratings" in rules, "缺少 ratings"
    assert "all_ages" in rules["ratings"]
    assert "12+" in rules["ratings"]
    assert "18+" in rules["ratings"]
    assert "non_compliant_triggers" in rules
    print("分级规则加载: PASS")
    return True


def test_scan_keywords_violence():
    """测试暴力关键词扫描。"""
    text = "两个人在街头打架，一个人被打伤了"
    keywords_db = load_all_keywords()
    hits = scan_keywords(text, keywords_db)
    assert len(hits) > 0, "应检测到暴力关键词"
    assert any(h.category == "violence" for h in hits), "应有暴力类别命中"
    print("暴力关键词扫描: PASS")
    return True


def test_scan_keywords_clean():
    """测试干净文本扫描。"""
    text = "今天天气很好，小明和小红一起去公园散步，看到了美丽的花朵。"
    keywords_db = load_all_keywords()
    hits = scan_keywords(text, keywords_db)
    assert len(hits) == 0, f"干净文本不应有命中, 得到 {len(hits)} 个"
    print("干净文本扫描: PASS")
    return True


def test_scan_keywords_multiple_categories():
    """测试多类别关键词扫描。"""
    text = "他醉酒后大声骂人混蛋，还在恐怖的黑暗中看到了鬼魂"
    keywords_db = load_all_keywords()
    hits = scan_keywords(text, keywords_db)
    categories = set(h.category for h in hits)
    assert len(categories) >= 2, f"应有多个类别命中, 得到 {categories}"
    print("多类别扫描: PASS")
    return True


def test_calculate_rating_clean():
    """测试干净内容的分级。"""
    rules = load_rating_rules("china")
    rating = calculate_initial_rating([], rules)
    assert rating == "all_ages", f"无命中应为 all_ages, 得到 {rating}"
    print("干净内容分级: PASS")
    return True


def test_calculate_rating_mild():
    """测试轻度内容的分级。"""
    rules = load_rating_rules("china")
    # 少量 mild 暴力命中
    hits = [
        KeywordHit(keyword="打", category="violence", severity="mild",
                   paragraph_index=0, position_in_paragraph=0, context="打架")
    ]
    rating = calculate_initial_rating(hits, rules)
    assert rating == "all_ages", f"少量 mild 应为 all_ages, 得到 {rating}"
    print("轻度内容分级: PASS")
    return True


def test_calculate_rating_moderate():
    """测试中度内容的分级。"""
    rules = load_rating_rules("china")
    hits = [
        KeywordHit(keyword="血", category="violence", severity="moderate",
                   paragraph_index=0, position_in_paragraph=0, context="流血"),
    ]
    rating = calculate_initial_rating(hits, rules)
    assert rating in ("12+", "18+"), f"moderate 暴力应为 12+/18+, 得到 {rating}"
    print("中度内容分级: PASS")
    return True


def test_calculate_rating_severe():
    """测试严重内容的分级。"""
    rules = load_rating_rules("china")
    hits = [
        KeywordHit(keyword="杀", category="violence", severity="severe",
                   paragraph_index=i, position_in_paragraph=0, context="杀")
        for i in range(6)  # 6 个 severe
    ]
    rating = calculate_initial_rating(hits, rules)
    assert rating == "non_compliant", f"大量 severe 应为 non_compliant, 得到 {rating}"
    print("严重内容分级: PASS")
    return True


def test_run_age_rating_scan():
    """测试完整分级扫描。"""
    text = "他拿起刀砍向了敌人，鲜血溅了一地。"
    result = run_age_rating_scan(text, target_rating="all_ages")
    assert isinstance(result, RatingResult)
    assert result.total_hits > 0
    assert not result.is_compliant, "暴力内容不应通过 all_ages"
    print("完整分级扫描: PASS")
    return True


def test_run_scan_compliant():
    """测试合规内容扫描。"""
    text = "小明和小红在花园里种花，蝴蝶在花丛中飞舞。"
    result = run_age_rating_scan(text, target_rating="all_ages")
    assert result.is_compliant, "无风险内容应通过 all_ages"
    assert result.risk_level == "low"
    print("合规内容扫描: PASS")
    return True


def test_frame_descriptions():
    """测试关键帧描述分析。"""
    keywords_db = load_all_keywords()
    descriptions = [
        {"timestamp": "00:01:30", "description": "角色拿出枪射击"},
        {"timestamp": "00:02:00", "description": "美丽的日落风景"},
    ]
    hits = analyze_frame_descriptions(descriptions, keywords_db)
    assert len(hits) > 0, "应检测到枪击关键词"
    assert hits[0].timestamp == "00:01:30"
    print("关键帧分析: PASS")
    return True


def test_keyword_hit_context():
    """测试关键词命中上下文。"""
    text = "一段很长的故事开头，然后他拿出刀砍向了敌人，后面还有更多内容"
    keywords_db = load_all_keywords()
    hits = scan_keywords(text, keywords_db)
    for hit in hits:
        assert len(hit.context) > 0, "上下文不应为空"
    print("命中上下文: PASS")
    return True


if __name__ == "__main__":
    print("=== 年龄分级检测测试 ===\n")

    tests = [
        test_load_keyword_database,
        test_load_all_keywords,
        test_load_rating_rules,
        test_scan_keywords_violence,
        test_scan_keywords_clean,
        test_scan_keywords_multiple_categories,
        test_calculate_rating_clean,
        test_calculate_rating_mild,
        test_calculate_rating_moderate,
        test_calculate_rating_severe,
        test_run_age_rating_scan,
        test_run_scan_compliant,
        test_frame_descriptions,
        test_keyword_hit_context,
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

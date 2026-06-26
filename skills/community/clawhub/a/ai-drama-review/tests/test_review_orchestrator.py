"""审查编排器测试"""

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from review_orchestrator import (
    load_input_text, format_user_warning, run_full_review,
)


def _create_temp_file(content: str, suffix: str = ".txt") -> str:
    """创建临时文件用于测试。"""
    f = tempfile.NamedTemporaryFile(mode="w", suffix=suffix,
                                     encoding="utf-8", delete=False)
    f.write(content)
    f.close()
    return f.name


def test_load_txt():
    """测试加载 TXT 文件。"""
    path = _create_temp_file("这是测试内容。\n第二行。")
    try:
        text = load_input_text(path)
        assert "测试内容" in text
        print("加载 TXT: PASS")
        return True
    finally:
        os.unlink(path)


def test_load_srt():
    """测试加载 SRT 字幕文件。"""
    srt_content = "1\n00:00:01,000 --> 00:00:03,000\n你好世界\n\n2\n00:00:04,000 --> 00:00:06,000\n测试字幕\n"
    path = _create_temp_file(srt_content, suffix=".srt")
    try:
        text = load_input_text(path)
        assert "你好世界" in text
        assert "测试字幕" in text
        assert "-->" not in text, "不应包含时间码"
        print("加载 SRT: PASS")
        return True
    finally:
        os.unlink(path)


def test_load_json():
    """测试加载 JSON 文件。"""
    json_content = json.dumps({"script": "这是剧本内容测试。"}, ensure_ascii=False)
    path = _create_temp_file(json_content, suffix=".json")
    try:
        text = load_input_text(path)
        assert "剧本内容" in text
        print("加载 JSON: PASS")
        return True
    finally:
        os.unlink(path)


def test_format_warning_clean():
    """测试干净内容的警告格式。"""
    report = {
        "overall_risk_level": "low",
        "overall_score": 100,
        "violation_summary": [],
    }
    warning = format_user_warning(report)
    assert "未发现" in warning
    print("干净警告格式: PASS")
    return True


def test_format_warning_violations():
    """测试有违规的警告格式。"""
    report = {
        "overall_risk_level": "high",
        "overall_score": 35,
        "violation_summary": [
            {"type": "copyright", "severity": "high",
             "description": "发现 3 个疑似侵权段落"},
            {"type": "age_rating", "severity": "medium",
             "description": "内容超出目标分级"},
        ],
        "remediation_suggestions": ["修改侵权段落", "降低暴力内容"],
    }
    warning = format_user_warning(report)
    assert "合规警告" in warning
    assert "高风险" in warning
    assert "版权侵权" in warning
    assert "年龄分级" in warning
    assert "修改侵权段落" in warning
    assert "不作为法律依据" in warning
    print("违规警告格式: PASS")
    return True


def test_run_review_rating_only():
    """测试仅执行分级检测。"""
    content = "小明和小红在花园里种花，蝴蝶在花丛中飞舞。"
    path = _create_temp_file(content)
    try:
        result = run_full_review(
            input_file=path,
            checks=["rating"],
            target_rating="all_ages",
        )
        assert "report" in result
        assert "warning" in result
        assert result["report"]["overall_risk_level"] == "low"
        print("仅分级检测: PASS")
        return True
    finally:
        os.unlink(path)


def test_run_review_violent_content():
    """测试暴力内容审查。"""
    content = "他拿起刀杀死了敌人，鲜血溅了一地，尸体倒在血泊中。"
    path = _create_temp_file(content)
    try:
        result = run_full_review(
            input_file=path,
            checks=["rating"],
            target_rating="all_ages",
        )
        report = result["report"]
        assert report["overall_risk_level"] != "low", \
            f"暴力内容不应为低风险, 得到 {report['overall_risk_level']}"
        assert "合规警告" in result["warning"]
        print("暴力内容审查: PASS")
        return True
    finally:
        os.unlink(path)


def test_run_review_copyright():
    """测试版权检测（有参考文本）。"""
    content = "从前有座山，山上有座庙。庙里有个老和尚在讲故事。"
    ref_content = "从前有座山，山上有座庙。庙里有个老和尚在讲故事。"

    input_path = _create_temp_file(content)
    ref_dir = tempfile.mkdtemp()
    ref_path = Path(ref_dir) / "reference.txt"
    ref_path.write_text(ref_content, encoding="utf-8")

    try:
        result = run_full_review(
            input_file=input_path,
            reference_dir=ref_dir,
            checks=["copyright"],
        )
        report = result["report"]
        assert "copyright_detection" in report
        print("版权检测: PASS")
        return True
    finally:
        os.unlink(input_path)
        ref_path.unlink()
        Path(ref_dir).rmdir()


def test_run_review_adaptation():
    """测试魔改检测。"""
    original = "第一章 初遇\n小明在学校遇到了小红两人成为好朋友相约一起学习。"
    adapted = "第一集 变形\n机器人从太空降落到地球上开始了与人类的互动过程。"

    orig_path = _create_temp_file(original)
    adapt_path = _create_temp_file(adapted)

    try:
        result = run_full_review(
            input_file=adapt_path,
            original_file=orig_path,
            checks=["adaptation"],
        )
        report = result["report"]
        assert "adaptation_detection" in report
        print("魔改检测: PASS")
        return True
    finally:
        os.unlink(orig_path)
        os.unlink(adapt_path)


def test_run_review_no_checks():
    """测试无检测模块时的处理。"""
    content = "测试内容"
    path = _create_temp_file(content)
    try:
        result = run_full_review(
            input_file=path,
            checks=[],
        )
        assert result["report"]["overall_risk_level"] == "low"
        print("无检测模块: PASS")
        return True
    finally:
        os.unlink(path)


if __name__ == "__main__":
    print("=== 审查编排器测试 ===\n")

    tests = [
        test_load_txt,
        test_load_srt,
        test_load_json,
        test_format_warning_clean,
        test_format_warning_violations,
        test_run_review_rating_only,
        test_run_review_violent_content,
        test_run_review_copyright,
        test_run_review_adaptation,
        test_run_review_no_checks,
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

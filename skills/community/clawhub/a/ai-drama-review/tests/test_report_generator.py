"""报告生成测试"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from report_generator import (
    ComplianceReport, calculate_overall_risk,
    generate_json_report, generate_markdown_report,
    generate_violation_annotations, build_full_report,
)


def test_calculate_risk_low():
    """测试低风险计算。"""
    level, score = calculate_overall_risk()
    assert level == "low", f"无结果应为 low, 得到 {level}"
    assert score == 100.0, f"无结果分数应为 100, 得到 {score}"
    print("低风险计算: PASS")
    return True


def test_calculate_risk_copyright_high():
    """测试版权高风险。"""
    cr = {"risk_level": "high", "suspicious_paragraphs": 5}
    level, score = calculate_overall_risk(copyright_result=cr)
    assert level in ("high", "critical"), f"版权高风险应为 high/critical, 得到 {level}"
    assert score < 50, f"高风险分数应低于 50, 得到 {score}"
    print("版权高风险: PASS")
    return True


def test_calculate_risk_rating_noncompliant():
    """测试分级不合规。"""
    ar = {"is_compliant": False, "risk_level": "critical"}
    level, score = calculate_overall_risk(age_rating_result=ar)
    assert level in ("high", "critical"), f"不合规应为高风险, 得到 {level}"
    print("分级不合规风险: PASS")
    return True


def test_calculate_risk_adaptation_severe():
    """测试严重魔改风险。"""
    ad = {"deviation_score": 80, "adaptation_type": "severe_modification"}
    level, score = calculate_overall_risk(adaptation_result=ad)
    assert level in ("medium", "high", "critical"), f"严重魔改应为中/高风险, 得到 {level}"
    print("严重魔改风险: PASS")
    return True


def test_calculate_risk_combined():
    """测试综合风险。"""
    cr = {"risk_level": "medium", "suspicious_paragraphs": 2}
    ar = {"is_compliant": False, "risk_level": "medium"}
    ad = {"deviation_score": 45}
    level, score = calculate_overall_risk(cr, ar, ad)
    assert level in ("medium", "high"), f"多项中风险综合应为 medium/high, 得到 {level}"
    print("综合风险: PASS")
    return True


def test_generate_json_report():
    """测试 JSON 报告生成。"""
    report = ComplianceReport(
        report_id="TEST-001",
        generated_at="2024-01-01T00:00:00",
        input_file="test.txt",
        overall_risk_level="medium",
        overall_score=65.0,
        violation_summary=[{"type": "copyright", "severity": "medium", "description": "test"}],
        remediation_suggestions=["修改内容"],
    )
    json_str = generate_json_report(report)
    data = json.loads(json_str)
    assert data["report_id"] == "TEST-001"
    assert data["overall_risk_level"] == "medium"
    assert len(data["violation_summary"]) == 1
    print("JSON 报告: PASS")
    return True


def test_generate_markdown_report():
    """测试 Markdown 报告生成。"""
    report = ComplianceReport(
        report_id="TEST-002",
        generated_at="2024-01-01T00:00:00",
        input_file="test.txt",
        overall_risk_level="low",
        overall_score=95.0,
        remediation_suggestions=["定期复查"],
    )
    md = generate_markdown_report(report)
    assert "# AI短剧合规审查报告" in md
    assert "TEST-002" in md
    assert "95.0/100" in md
    print("Markdown 报告: PASS")
    return True


def test_violation_annotations():
    """测试违规标注生成。"""
    report = ComplianceReport(
        copyright_result={
            "results": [
                {"source_paragraph_index": 3, "reference_id": "src_1",
                 "combined_score": 0.88},
            ]
        },
        age_rating_result={
            "keyword_hits": [
                {"keyword": "杀", "category": "violence", "severity": "severe",
                 "paragraph_index": 5, "context": "杀人", "timestamp": None},
            ]
        },
    )
    annotations = generate_violation_annotations(report)
    assert len(annotations) == 2, f"应有 2 个标注, 得到 {len(annotations)}"
    assert annotations[0]["type"] == "copyright"
    assert annotations[1]["type"] == "age_rating"
    print("违规标注: PASS")
    return True


def test_build_full_report():
    """测试完整报告构建。"""
    cr = {
        "total_paragraphs": 10,
        "suspicious_paragraphs": 2,
        "max_similarity_score": 0.82,
        "risk_level": "high",
        "results": [],
    }
    ar = {
        "suggested_rating": "18+",
        "target_rating": "all_ages",
        "is_compliant": False,
        "total_hits": 8,
        "risk_level": "high",
        "keyword_hits": [],
    }
    report = build_full_report("test.txt", cr, ar)
    assert report.report_id.startswith("DR-")
    assert report.overall_risk_level in ("high", "critical")
    assert len(report.violation_summary) >= 2
    assert len(report.remediation_suggestions) > 0
    print("完整报告构建: PASS")
    return True


def test_report_no_violations():
    """测试无违规的报告。"""
    report = build_full_report("clean.txt")
    assert report.overall_risk_level == "low"
    assert report.overall_score == 100.0
    assert len(report.violation_summary) == 0
    print("无违规报告: PASS")
    return True


if __name__ == "__main__":
    print("=== 报告生成测试 ===\n")

    tests = [
        test_calculate_risk_low,
        test_calculate_risk_copyright_high,
        test_calculate_risk_rating_noncompliant,
        test_calculate_risk_adaptation_severe,
        test_calculate_risk_combined,
        test_generate_json_report,
        test_generate_markdown_report,
        test_violation_annotations,
        test_build_full_report,
        test_report_no_violations,
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

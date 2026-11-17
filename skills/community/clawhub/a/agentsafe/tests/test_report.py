"""Report merge/dedupe acceptance tests."""

from agentsafe.report import build_report, merge_findings
from agentsafe.schemas import Finding, FindingStatus, LLMUsage, Severity


def _tool(
    check="reentrancy-eth",
    sev="high",
    path="V.sol",
    line=42,
    status=FindingStatus.TOOL_DETECTED,
    source=None,
    desc="External call.",
    title=None,
) -> Finding:
    return Finding(
        title=title or f"[slither] {check}",
        severity=sev,
        status=status,
        source=source or ["slither"],
        detector_id=check,
        description=desc,
        evidence=desc,
        file_path=path,
        line_start=line,
    )


def _llm(
    title="Reentrancy in withdraw",
    sev="high",
    path="V.sol",
    line=42,
    evidence="call.value(amount)",
    source=None,
) -> Finding:
    return Finding(
        title=title,
        severity=sev,
        status=FindingStatus.LLM_SUGGESTED,
        source=source or ["fund_flow"],
        description="LLM hypothesis",
        evidence=evidence,
        file_path=path,
        line_start=line,
        confidence=0.7,
    )


class TestMerge:
    def test_detector_merge_same_location_different_titles(self):
        f1 = _tool(desc="call before state update")
        f2 = _tool(title="[slither] different-title", desc="external call")
        out = merge_findings([f1, f2])
        assert len(out) == 1
        assert "slither" in out[0].source

    def test_llm_merges_into_tool_finding(self):
        tool = _tool(desc="Reentrancy in withdraw()")
        llm = _llm(evidence="withdraw() calls receiver before updating balances")
        out = merge_findings([tool, llm])
        assert len(out) == 1
        assert set(out[0].source) == {"slither", "fund_flow"}
        assert "additional evidence" in out[0].evidence
        assert out[0].status is FindingStatus.TOOL_DETECTED
        assert out[0].detector_id == "reentrancy-eth"

    def test_unrelated_llm_finding_survives(self):
        tool = _tool(path="A.sol", line=1, desc="a")
        llm = _llm(path="B.sol", line=99, title="Oracle manipulation", evidence="uses spot price")
        out = merge_findings([tool, llm])
        assert len(out) == 2
        assert any(f.source == ["fund_flow"] for f in out)

    def test_llm_duplicates_merge_by_title_location(self):
        a = _llm()
        b = _llm(source=["business_logic"])
        out = merge_findings([a, b])
        assert len(out) == 1
        assert set(out[0].source) == {"fund_flow", "business_logic"}

    def test_severity_ordering_critical_first(self):
        out = merge_findings(
            [
                _tool(check="low-x", sev="low"),
                _tool(check="crit", sev="critical"),
                _tool(check="med", sev="medium"),
            ]
        )
        assert [f.severity for f in out] == [Severity.CRITICAL, Severity.MEDIUM, Severity.LOW]

    def test_merge_never_drops_evidence(self):
        tool = _tool(desc="evidence-A")
        llm = _llm(evidence="evidence-B-different")
        out = merge_findings([tool, llm])
        if len(out) == 1:
            assert "evidence-A" in out[0].evidence


class TestBuildReport:
    def test_full_report_shape(self):
        report = build_report(
            address="0x" + "ab" * 20,
            task_id="t" * 24,
            is_verified_source=True,
            raw_findings=[_tool(), _llm()],
            tools_executed=["slither"],
            tools_failed=["aderyn"],
            tool_versions={"slither_version": "0.10.4"},
            llm_usage=LLMUsage(total_calls=3),
            limitations=["partial failures"],
            errors=["aderyn: crashed"],
            execution_time_seconds=12.3,
        )
        assert report.chain == "ethereum-mainnet"
        assert report.task_id == "t" * 24
        assert report.summary.total_findings == len(report.findings)
        assert "slither" in report.summary.tools_executed
        assert "aderyn" in report.summary.tools_failed
        assert report.disclaimer and "not a formal security audit" in report.disclaimer
        assert "aderyn: crashed" in report.errors

    def test_zero_findings_report_still_has_disclaimer(self):
        report = build_report(
            address="0x" + "ab" * 20,
            task_id=None,
            is_verified_source=False,
            raw_findings=[],
            tools_executed=[],
            tools_failed=[],
            tool_versions={},
            llm_usage=LLMUsage(),
            limitations=[],
            errors=[],
            execution_time_seconds=1.0,
        )
        assert report.findings == []
        # CRITICAL: zero findings must never be presented as "safe"
        blob = report.model_dump_json()
        assert '"safe"' not in blob
        assert "not a formal security audit" in report.disclaimer

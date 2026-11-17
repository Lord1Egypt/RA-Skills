"""Phase 1 tests: schemas, address validation, finding status semantics."""

import pytest
from pydantic import ValidationError

from agentsafe import CHAIN_ID
from agentsafe.schemas import (
    AuditReport,
    AuditRequest,
    Finding,
    FindingStatus,
    LLMUsage,
    ReportSummary,
    Severity,
    StageState,
    StageStatus,
    TaskState,
    TaskStatus,
    normalize_address,
)


def _finding(**overrides) -> dict:
    base = {
        "title": "Reentrancy in withdraw()",
        "severity": "high",
        "status": "tool_detected",
        "source": ["slither"],
        "detector_id": "reentrancy-eth",
        "description": "External call before state update.",
        "evidence": "call.value(amount) at line 42",
        "file_path": "contracts/Vault.sol",
        "line_start": 42,
    }
    base.update(overrides)
    return base


class TestAddressValidation:
    def test_valid_lowercase(self):
        assert normalize_address("0x" + "ab" * 20) == "0x" + "ab" * 20

    def test_mixed_case_normalized_to_lowercase(self):
        addr = "0xAbCdEf" + "00" * 17
        assert normalize_address(addr) == addr.lower()

    def test_too_short_rejected(self):
        with pytest.raises(ValueError, match="invalid EVM address"):
            normalize_address("0x1234")

    def test_non_hex_rejected(self):
        with pytest.raises(ValueError, match="invalid EVM address"):
            normalize_address("0x" + "zz" * 20)

    def test_no_prefix_rejected(self):
        with pytest.raises(ValueError, match="invalid EVM address"):
            normalize_address("1234" + "ab" * 18)

    def test_empty_rejected(self):
        with pytest.raises(ValueError, match="invalid EVM address"):
            normalize_address("")

    def test_audit_request_rejects_bad_address(self):
        with pytest.raises(ValidationError):
            AuditRequest(address="0x123")

    def test_audit_request_accepts_and_normalizes(self):
        req = AuditRequest(address="0xAbCdEf" + "00" * 17)
        assert req.address == req.address.lower()
        assert req.chain == CHAIN_ID


class TestFindingSemantics:
    def test_valid_finding(self):
        f = Finding(**_finding())
        assert f.severity is Severity.HIGH
        assert f.status is FindingStatus.TOOL_DETECTED
        assert f.source == ["slither"]

    def test_invalid_severity_rejected(self):
        with pytest.raises(ValidationError):
            Finding(**_finding(severity="catastrophic"))

    def test_invalid_status_rejected(self):
        with pytest.raises(ValidationError):
            Finding(**_finding(status="confirmed"))

    def test_evidence_required_unless_manual_review(self):
        no_ev = _finding(evidence="")
        with pytest.raises(ValidationError, match="evidence"):
            Finding(**no_ev)
        # manual_review is allowed to carry no evidence (that's its purpose)
        f = Finding(**_finding(evidence="", status="manual_review"))
        assert f.status is FindingStatus.MANUAL_REVIEW

    def test_source_must_be_non_empty(self):
        with pytest.raises(ValidationError):
            Finding(**_finding(source=["  "]))
        with pytest.raises(ValidationError):
            Finding(**_finding(source=[]))

    def test_sources_normalized_lowercase(self):
        f = Finding(**_finding(source=["Slither", "LLM"]))
        assert f.source == ["slither", "llm"]

    def test_confidence_range(self):
        with pytest.raises(ValidationError):
            Finding(**_finding(confidence=1.5))
        Finding(**_finding(confidence=0.0))
        Finding(**_finding(confidence=1.0))

    def test_line_range_ordering(self):
        with pytest.raises(ValidationError):
            Finding(**_finding(line_start=50, line_end=10))

    def test_merge_key_uses_detector_and_location(self):
        f1 = Finding(**_finding())
        f2 = Finding(**_finding(title="Different title"))
        assert f1.merge_key() == f2.merge_key()  # same detector+location dedupes

    def test_unknown_fields_forbidden(self):
        with pytest.raises(ValidationError):
            Finding(**_finding(is_safe=True))


class TestTaskAndStageModels:
    def test_stage_lifecycle_defaults(self):
        st = StageStatus(name="fetch_source")
        assert st.state is StageState.PENDING
        assert st.started_at is None

    def test_task_status_stage_lookup(self):
        t = TaskStatus(task_id="a" * 16, stages=[StageStatus(name="analyze")])
        assert t.stage("analyze").name == "analyze"
        with pytest.raises(KeyError):
            t.stage("missing")

    def test_task_id_length_bounds(self):
        with pytest.raises(ValidationError):
            TaskStatus(task_id="short")
        TaskStatus(task_id="a" * 64)

    def test_task_state_values(self):
        assert {s.value for s in TaskState} == {
            "queued",
            "running",
            "completed",
            "failed",
            "expired",
        }


class TestAuditReport:
    def test_minimal_report(self):
        r = AuditReport(address="0x" + "ab" * 20)
        assert r.chain == CHAIN_ID
        assert r.findings == []
        assert "not a formal security audit" in r.disclaimer

    def test_report_rejects_bad_address(self):
        with pytest.raises(ValidationError):
            AuditReport(address="0xdeadbeef")

    def test_report_summary_counts(self):
        r = AuditReport(
            address="0x" + "ab" * 20,
            findings=[
                Finding(**_finding()),
                Finding(
                    **_finding(
                        title="Second",
                        severity="low",
                        status="llm_suggested",
                        source=["llm"],
                        detector_id=None,
                    )
                ),
            ],
            summary=ReportSummary(
                total_findings=2,
                by_severity={"high": 1, "low": 1},
                by_status={"tool_detected": 1, "llm_suggested": 1},
            ),
            llm_usage=LLMUsage(total_calls=3, providers_used=["prov-a"]),
        )
        assert r.summary.total_findings == 2
        assert r.llm_usage.total_calls == 3

    def test_report_roundtrip_json(self):
        import json

        r = AuditReport(address="0x" + "ab" * 20, findings=[Finding(**_finding())])
        data = json.loads(r.model_dump_json())
        assert data["address"] == "0x" + "ab" * 20
        restored = AuditReport.model_validate(data)
        assert restored == r

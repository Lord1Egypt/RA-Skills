"""GitHub client acceptance: dispatch, association, artifacts, ZIP safety."""

import io
import json
import zipfile
from datetime import UTC, datetime, timedelta

import httpx
import pytest
import respx

from agentsafe.github_client import (
    ArtifactExpiredError,
    GitHubActionsClient,
    GitHubClientError,
    RateLimitedError,
    RunAssociationError,
    extract_report_from_zip,
)

BASE = "https://api.github.com"
REPO = "owner/repo"
ADDR = "0x" + "ab" * 20
TASK = "T" * 24


async def _ns(d):
    return None


def _client(**kw):
    kw.setdefault("sleeper", _ns)
    return GitHubActionsClient(token="ghp-test", repo=REPO, **kw)


def _run(
    run_id=100,
    name="audit-xyz",
    created="2026-01-01T10:00:00Z",
    status="completed",
    conclusion="success",
):
    return {
        "id": run_id,
        "name": name,
        "created_at": created,
        "status": status,
        "conclusion": conclusion,
    }


class TestDispatch:
    @respx.mock
    async def test_dispatch_payload_is_validated_address(self):
        route = respx.post(f"{BASE}/repos/{REPO}/actions/workflows/audit.yml/dispatches").mock(
            return_value=httpx.Response(204)
        )
        await _client().trigger_workflow(ADDR.upper(), TASK)
        body = json.loads(route.calls.last.request.read())
        assert body["inputs"]["address"] == ADDR  # normalized lowercase
        assert body["inputs"]["task_id"] == TASK
        assert body["ref"] == "main"

    @respx.mock
    async def test_dispatch_rejects_bad_address(self):
        with pytest.raises(ValueError):
            await _client().trigger_workflow("0x123", TASK)

    @respx.mock
    async def test_dispatch_404_raises(self):
        respx.post(f"{BASE}/repos/{REPO}/actions/workflows/audit.yml/dispatches").mock(
            return_value=httpx.Response(404, json={"message": "Not Found"})
        )
        with pytest.raises(GitHubClientError, match="404"):
            await _client().trigger_workflow(ADDR, TASK)


class TestRunAssociation:
    @respx.mock
    async def test_unique_name_match(self):
        now = datetime.now(UTC)
        respx.get(f"{BASE}/repos/{REPO}/actions/workflows/audit.yml/runs").mock(
            return_value=httpx.Response(
                200,
                json={
                    "workflow_runs": [
                        _run(
                            run_id=99,
                            name="audit-other",
                            created=(now + timedelta(seconds=30)).isoformat(),
                        ),
                        _run(
                            run_id=100,
                            name=f"audit-{TASK}",
                            created=(now + timedelta(seconds=10)).isoformat(),
                        ),
                    ]
                },
            )
        )
        run_id = await _client().resolve_run_id(TASK, dispatched_after=now - timedelta(seconds=60))
        assert run_id == 100

    @respx.mock
    async def test_ambiguous_matches_refuse_to_guess(self):
        now = datetime.now(UTC).isoformat()
        respx.get(f"{BASE}/repos/{REPO}/actions/workflows/audit.yml/runs").mock(
            return_value=httpx.Response(
                200,
                json={
                    "workflow_runs": [
                        _run(run_id=100, name=f"audit-{TASK}", created=now),
                        _run(run_id=101, name=f"audit-{TASK}", created=now),
                    ]
                },
            )
        )
        with pytest.raises(RunAssociationError, match="refusing to guess"):
            await _client().resolve_run_id(
                TASK, dispatched_after=datetime.now(UTC) - timedelta(minutes=1)
            )

    @respx.mock
    async def test_no_match_after_polls_refuses(self):
        respx.get(f"{BASE}/repos/{REPO}/actions/workflows/audit.yml/runs").mock(
            return_value=httpx.Response(200, json={"workflow_runs": []})
        )
        with pytest.raises(RunAssociationError, match="no run named"):
            await _client().resolve_run_id(TASK, dispatched_after=datetime.now(UTC), attempts=2)

    @respx.mock
    async def test_polls_until_run_appears(self):
        state = {"seen": False}

        def respond(request):
            if not state["seen"]:
                state["seen"] = True
                return httpx.Response(200, json={"workflow_runs": []})
            return httpx.Response(
                200,
                json={
                    "workflow_runs": [
                        _run(run_id=55, name=f"audit-{TASK}", created=datetime.now(UTC).isoformat())
                    ]
                },
            )

        respx.get(f"{BASE}/repos/{REPO}/actions/workflows/audit.yml/runs").mock(side_effect=respond)
        run_id = await _client().resolve_run_id(
            TASK, dispatched_after=datetime.now(UTC) - timedelta(seconds=5)
        )
        assert run_id == 55

    @respx.mock
    async def test_run_status_mapping(self):
        client = _client()
        assert client.map_run_status({"status": "queued", "conclusion": None}) == "queued"
        assert client.map_run_status({"status": "in_progress"}) == "running"
        assert (
            client.map_run_status({"status": "completed", "conclusion": "success"}) == "completed"
        )
        assert client.map_run_status({"status": "completed", "conclusion": "failure"}) == "failed"
        assert client.map_run_status({"status": "completed", "conclusion": "timed_out"}) == "failed"


class TestArtifacts:
    @respx.mock
    async def test_fetch_report_happy_path(self):
        report = {"address": ADDR, "findings": []}
        zip_bytes = _zip({"report.json": json.dumps(report)})
        respx.get(f"{BASE}/repos/{REPO}/actions/runs/100/artifacts").mock(
            return_value=httpx.Response(
                200,
                json={
                    "artifacts": [
                        {"id": 7, "name": f"audit-report-{TASK}", "expired": False, "run_id": 100}
                    ]
                },
            )
        )
        respx.get(f"{BASE}/repos/{REPO}/actions/artifacts/7/zip").mock(
            return_value=httpx.Response(200, content=zip_bytes)
        )
        got = await _client().fetch_report(100, TASK)
        assert got["address"] == ADDR

    @respx.mock
    async def test_expired_artifact_raises(self):
        respx.get(f"{BASE}/repos/{REPO}/actions/runs/100/artifacts").mock(
            return_value=httpx.Response(
                200,
                json={"artifacts": [{"id": 7, "name": f"audit-report-{TASK}", "expired": True}]},
            )
        )
        with pytest.raises(ArtifactExpiredError):
            await _client().fetch_report(100, TASK)

    @respx.mock
    async def test_wrong_named_artifact_rejected(self):
        respx.get(f"{BASE}/repos/{REPO}/actions/runs/100/artifacts").mock(
            return_value=httpx.Response(
                200,
                json={"artifacts": [{"id": 7, "name": "audit-report-OTHERTASK", "expired": False}]},
            )
        )
        with pytest.raises(GitHubClientError, match="not found"):
            await _client().fetch_report(100, TASK)


def _zip(files: dict[str, str]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    return buf.getvalue()


class TestZipSafety:
    def test_safe_extraction(self):
        data = _zip({"report.json": "{}", "meta.txt": "ignored"})
        assert extract_report_from_zip(data, expected_names={"report.json"}) == b"{}"

    def test_traversal_member_rejected(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("../evil.sh", "boom")
            zf.writestr("report.json", "{}")
        with pytest.raises(GitHubClientError, match="unsafe ZIP member"):
            extract_report_from_zip(buf.getvalue(), expected_names={"report.json"})

    def test_absolute_path_member_rejected(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("/etc/evil", "boom")
            zf.writestr("report.json", "{}")
        with pytest.raises(GitHubClientError, match="unsafe ZIP member"):
            extract_report_from_zip(buf.getvalue(), expected_names={"report.json"})

    def test_missing_report_rejected(self):
        with pytest.raises(GitHubClientError, match="missing"):
            extract_report_from_zip(_zip({"other.txt": "x"}), expected_names={"report.json"})

    def test_corrupt_zip_rejected(self):
        with pytest.raises(GitHubClientError, match="not a valid ZIP"):
            extract_report_from_zip(b"garbage-not-zip", expected_names={"report.json"})

    def test_oversized_member_rejected(self):
        from agentsafe import github_client as gc

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as zf:
            zf.writestr("report.json", "x" * (gc.MAX_MEMBER_BYTES + 1))
        with pytest.raises(GitHubClientError, match="size policy"):
            extract_report_from_zip(buf.getvalue(), expected_names={"report.json"})


class TestRateLimit:
    @respx.mock
    async def test_403_rate_limit_typed_error(self):
        respx.get(f"{BASE}/repos/{REPO}/actions/runs/1").mock(
            return_value=httpx.Response(
                403,
                json={"message": "API rate limit exceeded"},
                headers={"x-ratelimit-remaining": "0"},
            )
        )
        with pytest.raises(RateLimitedError):
            await _client().get_run(1)

"""
tests/test_excel_download.py — Tests for the /export/excel browser-download route (#156).

Verifies that:
  - Authenticated GET /export/excel returns 200 with correct Content-Type and
    Content-Disposition headers and non-empty body.
  - Unauthenticated GET /export/excel returns 302 redirect to /login.
  - Response body is a valid openpyxl workbook with at least one sheet.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Re-use auth helpers from test_ui_routes
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    import server.paths as paths
    from server.db import init_db

    db = tmp_path / "test.db"
    init_db(db)

    monkeypatch.setattr(paths, "DB_PATH", db)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    return db


@pytest.fixture()
def client(db_path: Path) -> TestClient:
    from ui.server import app

    return TestClient(app, follow_redirects=False)


@pytest.fixture()
def authed_client(db_path: Path) -> TestClient:
    from ui.server import app

    c = TestClient(app, follow_redirects=False)
    _complete_setup(c)
    return _login(c)


def _complete_setup(client: TestClient, password: str = "testpassword123") -> None:
    r = client.post("/setup/1", data={"password": password, "password_confirm": password})
    assert r.status_code == 200
    r = client.post("/setup/2", data={"notification_pref": "openclaw"})
    assert r.status_code == 200
    r = client.post("/setup/3", data={"action": "skip"})
    assert r.status_code == 302


def _login(client: TestClient, password: str = "testpassword123") -> TestClient:
    r = client.post("/login", data={"password": password})
    # Should redirect on success
    assert r.status_code in (200, 302, 303)
    return client


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestExcelDownloadAuthenticated:
    def test_status_200(self, authed_client: TestClient) -> None:
        r = authed_client.get("/export/excel")
        assert r.status_code == 200

    def test_content_type_xlsx(self, authed_client: TestClient) -> None:
        r = authed_client.get("/export/excel")
        assert "spreadsheetml" in r.headers["content-type"]

    def test_content_disposition_attachment(self, authed_client: TestClient) -> None:
        r = authed_client.get("/export/excel")
        cd = r.headers.get("content-disposition", "")
        assert "attachment" in cd
        assert ".xlsx" in cd

    def test_body_non_empty(self, authed_client: TestClient) -> None:
        r = authed_client.get("/export/excel")
        assert len(r.content) > 0

    def test_valid_workbook_with_sheets(self, authed_client: TestClient) -> None:
        import openpyxl

        r = authed_client.get("/export/excel")
        wb = openpyxl.load_workbook(BytesIO(r.content))
        assert len(wb.sheetnames) >= 1


class TestExcelDownloadUnauthenticated:
    def test_redirects_to_login(self, client: TestClient) -> None:
        r = client.get("/export/excel")
        assert r.status_code == 302
        assert "/login" in r.headers.get("location", "")

from __future__ import annotations

import subprocess
from pathlib import Path
from types import SimpleNamespace

import extract_isbn


def test_direct_tesseract_cli_fallback_extracts_isbn_without_shell(monkeypatch, tmp_path: Path):
    image = tmp_path / "photo name.jpg"
    image.write_bytes(b"not decoded by the mocked command")
    calls: list[tuple[list[str], dict]] = []

    def fake_run(args, **kwargs):
        calls.append((args, kwargs))
        return SimpleNamespace(returncode=0, stdout="ISBN 978-0-306-40615-7", stderr="")

    monkeypatch.setenv("BOOK_CAPTURE_ENABLE_ZBARIMG", "false")
    monkeypatch.setenv("BOOK_CAPTURE_ENABLE_PYZBAR", "false")
    monkeypatch.setenv("BOOK_CAPTURE_ENABLE_OCR", "true")
    monkeypatch.setenv("BOOK_CAPTURE_TESSERACT_CMD", "tesseract-test-bin")
    monkeypatch.setattr(extract_isbn, "_get_pytesseract_module", lambda: None)
    monkeypatch.setattr(extract_isbn.subprocess, "run", fake_run)

    result = extract_isbn.extract_isbn_from_image(str(image))

    assert result["ok"] is True
    assert result["method"] == "ocr"
    assert result["isbn13"] == "9780306406157"
    assert len(calls) == 3
    for args, kwargs in calls:
        assert isinstance(args, list)
        assert args[:3] == ["tesseract-test-bin", str(image), "stdout"]
        assert kwargs["timeout"] == 20
        assert "shell" not in kwargs


def test_direct_tesseract_timeout_warning_is_deterministic(monkeypatch):
    def time_out(args, **kwargs):
        raise subprocess.TimeoutExpired(args, kwargs["timeout"])

    monkeypatch.setattr(extract_isbn.subprocess, "run", time_out)
    texts, warnings = extract_isbn._run_ocr_cli("photo.jpg", "eng", "tesseract", 7)
    assert texts == []
    assert warnings == ["tesseract timed out after 7s"]

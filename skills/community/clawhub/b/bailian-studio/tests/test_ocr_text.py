import types
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1] / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import ocr_text as ocr


def test_url_pass_through(monkeypatch):
    def fake_call(**kwargs):
        assert kwargs["messages"][0]["content"][0]["image"] == "https://example.com/a.png"
        return {"output": {"choices": [{"message": {"content": [{"text": "hello"}]}}]}}

    fake_dashscope = types.SimpleNamespace(
        MultiModalConversation=types.SimpleNamespace(call=fake_call),
        base_http_api_url=None,
    )
    monkeypatch.setattr(ocr, "dashscope", fake_dashscope)
    monkeypatch.setattr(ocr, "get_dashscope_key", lambda: "k")

    text = ocr.run_ocr("https://example.com/a.png", "model", 1, 2, False)
    assert text == "hello"


def test_local_file_upload(monkeypatch, tmp_path: Path):
    fake_image = tmp_path / "a.png"
    fake_image.write_text("x", encoding="utf-8")

    monkeypatch.setattr(ocr, "upload_image", lambda p: "https://oss/a.png")

    def fake_call(**kwargs):
        assert kwargs["messages"][0]["content"][0]["image"] == "https://oss/a.png"
        return {"output": {"choices": [{"message": {"content": [{"text": "ok"}]}}]}}

    fake_dashscope = types.SimpleNamespace(
        MultiModalConversation=types.SimpleNamespace(call=fake_call),
        base_http_api_url=None,
    )
    monkeypatch.setattr(ocr, "dashscope", fake_dashscope)
    monkeypatch.setattr(ocr, "get_dashscope_key", lambda: "k")

    text = ocr.run_ocr("https://oss/a.png", "model", 1, 2, False)
    assert text == "ok"

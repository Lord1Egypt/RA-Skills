from pathlib import Path
import sys
import types

sys.modules.setdefault("oss2", types.SimpleNamespace(Auth=object, Bucket=object))

ROOT = Path(__file__).resolve().parents[1] / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import image_generate as ig


def test_build_size():
    assert ig.build_size(1024, 768) == "1024*768"


def test_resolve_output_path_auto_renames(tmp_path: Path):
    first = tmp_path / "测试-prompt.png"
    first.write_bytes(b"x")
    resolved = ig.resolve_output_path(tmp_path, output=None, prompt="测试 prompt")
    assert resolved.name == "测试-prompt-1.png"


def test_prepare_reference_image_uploads_local(monkeypatch, tmp_path: Path):
    image = tmp_path / "ref.png"
    image.write_bytes(b"fake")
    monkeypatch.setattr(ig, "upload_image", lambda path: "https://oss.example/ref.png")
    assert ig.prepare_reference_image(str(image)) == "https://oss.example/ref.png"


def test_prepare_reference_image_passes_url():
    assert ig.prepare_reference_image("https://example.com/ref.png") == "https://example.com/ref.png"


def test_extract_image_url_from_output_results():
    response = {"output": {"results": [{"url": "https://img.example/a.png"}]}}
    assert ig.extract_image_url(response) == "https://img.example/a.png"


def test_extract_image_url_from_message_content():
    response = {
        "output": {
            "choices": [
                {
                    "message": {
                        "content": [
                            {"image": "https://img.example/c.png"},
                        ]
                    }
                }
            ]
        }
    }
    assert ig.extract_image_url(response) == "https://img.example/c.png"


def test_generate_image_calls_multimodal_for_text2image(monkeypatch):
    captured = {}

    def fake_call(**kwargs):
        captured.update(kwargs)
        return {
            "output": {
                "choices": [
                    {
                        "message": {
                            "content": [{"image": "https://img.example/out.png"}]
                        }
                    }
                ]
            }
        }

    fake_dashscope = types.SimpleNamespace(
        MultiModalConversation=types.SimpleNamespace(call=fake_call),
        base_http_api_url=None,
    )
    monkeypatch.setattr(ig, "dashscope", fake_dashscope)
    monkeypatch.setattr(ig, "get_dashscope_key", lambda env_path=None: "k")

    url = ig.generate_image(
        prompt="cat",
        model="qwen-image-2.0-pro",
        width=1024,
        height=1024,
        reference_image=None,
    )

    assert url == "https://img.example/out.png"
    assert captured["model"] == "qwen-image-2.0-pro"
    assert captured["result_format"] == "message"
    assert captured["stream"] is False
    assert captured["watermark"] is False
    assert captured["prompt_extend"] is True
    assert captured["size"] == "1024*1024"


def test_generate_image_calls_multimodal_for_img2img(monkeypatch):
    captured = {}

    def fake_call(**kwargs):
        captured.update(kwargs)
        return {
            "output": {
                "choices": [
                    {
                        "message": {
                            "content": [{"image": "https://img.example/out.png"}]
                        }
                    }
                ]
            }
        }

    fake_dashscope = types.SimpleNamespace(
        MultiModalConversation=types.SimpleNamespace(call=fake_call),
        base_http_api_url=None,
    )
    monkeypatch.setattr(ig, "dashscope", fake_dashscope)
    monkeypatch.setattr(ig, "get_dashscope_key", lambda env_path=None: "k")

    url = ig.generate_image(
        prompt="cat",
        model="qwen-image-2.0-pro",
        width=1024,
        height=1024,
        reference_image="https://example.com/ref.png",
    )

    assert url == "https://img.example/out.png"
    content = captured["messages"][0]["content"]
    assert content[0]["image"] == "https://example.com/ref.png"
    assert content[1]["text"] == "cat"


def test_download_image_writes_file(monkeypatch, tmp_path: Path):
    output = tmp_path / "out.png"

    class FakeResponse:
        content = b"png-bytes"

        def raise_for_status(self):
            return None

    monkeypatch.setattr(ig.requests, "get", lambda url, timeout: FakeResponse())
    saved = ig.download_image("https://img.example/out.png", output, timeout=30)
    assert saved.read_bytes() == b"png-bytes"


def test_read_prompt_supports_stdin(monkeypatch):
    monkeypatch.setattr(
        sys,
        "stdin",
        types.SimpleNamespace(read=lambda: "stdin prompt\n", isatty=lambda: False),
    )
    assert ig.read_prompt(None) == "stdin prompt"

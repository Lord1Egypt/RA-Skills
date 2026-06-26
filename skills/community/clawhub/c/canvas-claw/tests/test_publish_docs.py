from pathlib import Path


def test_publish_doc_contains_clawhub_steps() -> None:
    publish_doc = Path(__file__).resolve().parents[1] / "PUBLISH.md"
    text = publish_doc.read_text()
    assert "npx clawhub login" in text
    assert "npx clawhub whoami" in text
    assert "npx clawhub publish" in text
    assert "--slug canvas-claw" in text


def test_gitignore_excludes_runtime_artifacts() -> None:
    gitignore = Path(__file__).resolve().parents[1] / ".gitignore"
    text = gitignore.read_text()
    assert ".pytest_cache/" in text
    assert "__pycache__/" in text

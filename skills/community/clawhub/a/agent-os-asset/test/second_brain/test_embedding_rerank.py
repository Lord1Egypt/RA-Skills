from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "skills"
    / "second-brain"
    / "scripts"
    / "embedding_rerank.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("embedding_rerank", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_rerank_prefers_semantic_match_with_injected_embedder() -> None:
    rerank = load_module()
    results = [
        {"record_id": "feature", "score": 10.0, "title": "route-feature"},
        {"record_id": "planner", "score": 8.0, "title": "route-planner"},
    ]
    documents = {
        "feature": {"search_text": "route feature extraction"},
        "planner": {"search_text": "route planning service build and control"},
    }

    def embed(texts: list[str]) -> list[list[float]]:
        vectors = []
        for text in texts:
            vectors.append([1.0, 0.0] if "planning" in text else [0.0, 1.0])
        return vectors

    ranked = rerank.rerank_results("route planning build control", results, documents, embedder=embed)

    assert ranked[0]["record_id"] == "planner"
    assert ranked[0]["semantic_score"] > ranked[1]["semantic_score"]


def test_provider_status_is_unavailable_without_configured_backend(monkeypatch) -> None:
    rerank = load_module()
    for name in (
        "SECOND_BRAIN_EMBEDDING_PROVIDER",
        "SECOND_BRAIN_EMBEDDING_API_KEY",
        "AZURE_OPENAI_API_KEY",
        "OPENAI_API_KEY",
    ):
        monkeypatch.delenv(name, raising=False)

    status = rerank.provider_status()

    assert status["available"] is False
    assert status["reason"] == "explicit_opt_in_required"


def test_general_credentials_do_not_enable_embedding(monkeypatch) -> None:
    rerank = load_module()
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "general-azure-key")
    monkeypatch.setenv("OPENAI_API_KEY", "general-openai-key")
    monkeypatch.delenv("SECOND_BRAIN_EMBEDDING_ENABLED", raising=False)
    monkeypatch.delenv("SECOND_BRAIN_EMBEDDING_API_KEY", raising=False)

    status = rerank.provider_status()

    assert status["available"] is False
    assert status["reason"] == "explicit_opt_in_required"


def test_embedding_requires_https_endpoint(monkeypatch) -> None:
    rerank = load_module()
    monkeypatch.setenv("SECOND_BRAIN_EMBEDDING_ENABLED", "1")
    monkeypatch.setenv("SECOND_BRAIN_EMBEDDING_PROVIDER", "openai")
    monkeypatch.setenv("SECOND_BRAIN_EMBEDDING_API_KEY", "test-key")
    monkeypatch.setenv("SECOND_BRAIN_EMBEDDING_BASE_URL", "http://example.invalid/v1")

    status = rerank.provider_status()

    assert status["available"] is False
    assert status["reason"] == "https_required"


def test_explicit_embedding_configuration_is_available(monkeypatch) -> None:
    rerank = load_module()
    monkeypatch.setenv("SECOND_BRAIN_EMBEDDING_ENABLED", "1")
    monkeypatch.setenv("SECOND_BRAIN_EMBEDDING_PROVIDER", "openai")
    monkeypatch.setenv("SECOND_BRAIN_EMBEDDING_API_KEY", "test-key")
    monkeypatch.setenv("SECOND_BRAIN_EMBEDDING_BASE_URL", "https://example.invalid/v1")

    status = rerank.provider_status()

    assert status["available"] is True
    assert status["provider"] == "openai"

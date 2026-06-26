import json
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# test_rerank_results
# ---------------------------------------------------------------------------

def test_rerank_results_issuer_first():
    from tools.brave_client import rerank_results

    results = [
        {"title": "Bankrate review", "link": "https://www.bankrate.com/card"},
        {"title": "Chase official page", "link": "https://creditcards.chase.com/sapphire"},
        {"title": "NerdWallet article", "link": "https://www.nerdwallet.com/card"},
    ]
    reranked = rerank_results(results)
    # Chase (issuer) should come before NerdWallet, NerdWallet before Bankrate
    urls = [r["link"] for r in reranked]
    assert urls.index("https://creditcards.chase.com/sapphire") < urls.index("https://www.nerdwallet.com/card")
    assert urls.index("https://www.nerdwallet.com/card") < urls.index("https://www.bankrate.com/card")


def test_rerank_results_unknown_domain_goes_last():
    from tools.brave_client import rerank_results

    results = [
        {"title": "Random blog", "link": "https://creditcardguru.blog/review"},
        {"title": "Amex official", "link": "https://www.americanexpress.com/gold"},
    ]
    reranked = rerank_results(results)
    assert reranked[0]["link"] == "https://www.americanexpress.com/gold"
    assert reranked[1]["link"] == "https://creditcardguru.blog/review"


def test_rerank_results_empty_list():
    from tools.brave_client import rerank_results

    assert rerank_results([]) == []


# ---------------------------------------------------------------------------
# test_format_results_for_llm
# ---------------------------------------------------------------------------

def test_format_results_truncates_snippets():
    from tools.brave_client import format_results_for_llm

    long_snippet = "x" * 400
    results = [{"title": "T", "link": "https://example.com", "snippet": long_snippet}]
    output = format_results_for_llm(results)
    snippet_part = output.split("|")[-1].strip()
    assert len(snippet_part) <= 303  # 300 chars + "..."
    assert snippet_part.endswith("...")


def test_format_results_respects_max_results():
    from tools.brave_client import format_results_for_llm

    results = [
        {"title": f"T{i}", "link": f"https://example.com/{i}", "snippet": "s"}
        for i in range(10)
    ]
    output = format_results_for_llm(results, max_results=3)
    assert output.count("https://example.com/") == 3


def test_format_results_empty_returns_no_results():
    from tools.brave_client import format_results_for_llm

    assert format_results_for_llm([]) == "No results found."


def test_format_results_uses_description_fallback():
    from tools.brave_client import format_results_for_llm

    results = [{"title": "T", "link": "https://x.com", "description": "desc text"}]
    output = format_results_for_llm(results)
    assert "desc text" in output


# ---------------------------------------------------------------------------
# test_build_brave_wrapper
# ---------------------------------------------------------------------------

def test_build_brave_wrapper_passes_api_key_explicitly():
    mock_wrapper_cls = MagicMock()
    with patch.dict("sys.modules", {"langchain_community.utilities": MagicMock(BraveSearchWrapper=mock_wrapper_cls)}):
        from importlib import reload
        import tools.brave_client as bc
        reload(bc)
        bc.build_brave_wrapper("my-test-key")

    call_kwargs = mock_wrapper_cls.call_args[1]
    assert call_kwargs["api_key"].get_secret_value() == "my-test-key"


def test_build_brave_wrapper_includes_freshness_when_set():
    mock_wrapper_cls = MagicMock()
    with patch.dict("sys.modules", {"langchain_community.utilities": MagicMock(BraveSearchWrapper=mock_wrapper_cls)}):
        from importlib import reload
        import tools.brave_client as bc
        reload(bc)
        bc.build_brave_wrapper("key", freshness="pm")

    search_kwargs = mock_wrapper_cls.call_args[1]["search_kwargs"]
    assert search_kwargs["freshness"] == "pm"


def test_build_brave_wrapper_no_freshness_by_default():
    mock_wrapper_cls = MagicMock()
    with patch.dict("sys.modules", {"langchain_community.utilities": MagicMock(BraveSearchWrapper=mock_wrapper_cls)}):
        from importlib import reload
        import tools.brave_client as bc
        reload(bc)
        bc.build_brave_wrapper("key")

    search_kwargs = mock_wrapper_cls.call_args[1]["search_kwargs"]
    assert "freshness" not in search_kwargs

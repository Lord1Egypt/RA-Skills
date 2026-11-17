import os
from pydantic import SecretStr

PRIORITY_SITES = [
    "chase.com",
    "americanexpress.com",
    "citi.com",
    "capitalone.com",
    "bankofamerica.com",
    "wellsfargo.com",
    "discover.com",
    "barclays.com",
    "biltrewards.com",
    "nerdwallet.com",
    "thepointsguy.com",
    "doctorofcredit.com",
    "bankrate.com",
    "onemileatatime.com",
    "uscreditcardguide.com",
]


def build_brave_wrapper(api_key: str, freshness: str | None = None, count: int = 5):
    from langchain_community.utilities import BraveSearchWrapper

    search_kwargs: dict = {"count": count}
    if freshness:
        search_kwargs["freshness"] = freshness

    return BraveSearchWrapper(
        api_key=SecretStr(api_key),
        search_kwargs=search_kwargs,
    )


def rerank_results(results: list[dict]) -> list[dict]:
    def priority(r: dict) -> int:
        url = r.get("link", r.get("url", ""))
        for i, domain in enumerate(PRIORITY_SITES):
            if domain in url:
                return i
        return len(PRIORITY_SITES)

    return sorted(results, key=priority)


def format_results_for_llm(results: list[dict], max_results: int = 4) -> str:
    lines = []
    for r in results[:max_results]:
        title = r.get("title", "No title")
        source = r.get("link", r.get("url", "Unknown source"))
        snippet = r.get("snippet", r.get("description", ""))
        if len(snippet) > 300:
            snippet = snippet[:297] + "..."
        lines.append(f"{title} | {source} | {snippet}")
    return "\n".join(lines) if lines else "No results found."


def search_and_format(wrapper, query: str, max_results: int = 4) -> str:
    """Run a Brave search and return LLM-ready formatted results.

    Falls back gracefully: tries _search() for structured reranking,
    falls back to run() string output if _search() is unavailable.
    """
    try:
        raw: list[dict] = wrapper._search(query)
        reranked = rerank_results(raw)
        return format_results_for_llm(reranked, max_results=max_results)
    except (AttributeError, Exception):
        return wrapper.run(query)

"""
Deep Research Agent
====================
A LangChain DeepAgents-based autonomous research engine.

Usage:
    python agent.py "Your research question here"
    python agent.py "Your research question here" --max-results 3 --concurrency 2
"""

import os
import sys
import argparse
import httpx
from datetime import datetime
from typing import Annotated, Literal

from langchain.tools import InjectedToolArg, tool
from markdownify import markdownify
from tavily import TavilyClient

from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model

# ─── Configuration ───────────────────────────────────────────────────────────

DEFAULT_MODEL = os.getenv("DRA_MODEL", "anthropic:claude-sonnet-4-5-20250929")
TAVILY_MAX_RESULTS = int(os.getenv("TAVILY_MAX_RESULTS", "5"))

# ─── Tools ───────────────────────────────────────────────────────────────────

def _init_tavily():
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        raise SystemExit(
            "TAVILY_API_KEY is required. Get one at https://tavily.com/ (free tier ok)."
        )
    return TavilyClient(api_key=key)


def fetch_webpage_content(url: str, timeout: float = 10.0) -> str:
    """Fetch a webpage and convert HTML to markdown."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = httpx.get(url, headers=headers, timeout=timeout, follow_redirects=True)
        resp.raise_for_status()
        return markdownify(resp.text)
    except Exception as e:
        return f"[Error fetching {url}] {e!s}"


@tool(parse_docstring=True)
def tavily_search(
    query: str,
    max_results: Annotated[int, InjectedToolArg] = TAVILY_MAX_RESULTS,
    topic: Annotated[
        Literal["general", "news", "finance"], InjectedToolArg
    ] = "general",
) -> str:
    """Search the web and return full webpage content.

    Uses Tavily for URL discovery, then fetches and returns complete page
    content as markdown for deep analysis.

    Args:
        query: Search query string
        max_results: Maximum number of results (default: 5)
        topic: Topic filter - 'general', 'news', or 'finance'

    Returns:
        Formatted search results with full webpage content in markdown
    """
    client = _init_tavily()
    results = client.search(query, max_results=max_results, topic=topic)
    texts = []
    for r in results.get("results", []):
        url = r["url"]
        title = r.get("title", url)
        content = fetch_webpage_content(url)
        texts.append(f"## {title}\n**URL:** {url}\n\n{content}\n---")
    if not texts:
        return f"No results found for '{query}'."
    return f"Found {len(texts)} result(s) for '{query}':\n\n" + "\n".join(texts)


# ─── Prompts ─────────────────────────────────────────────────────────────────

RESEARCH_WORKFLOW_INSTRUCTIONS = """\
# Research Workflow

Follow this workflow for all research requests:

1. **Plan**: Create a todo list with write_todos to break down the research into focused tasks.
2. **Save the request**: Use write_file() to save the research request to `/research_request.md`.
3. **Research**: Delegate research tasks to sub-agents using the task() tool.
   - ALWAYS use sub-agents for research, never search yourself.
   - For simple fact-finding, batch into 1 todo and 1 sub-agent.
   - For complex comparisons, create separate todos and dispatch multiple sub-agents.
4. **Synthesize**: Review findings and consolidate citations. Each unique URL gets one number across all findings.
5. **Write Report**: Write a comprehensive report to `/final_report.md`.
6. **Verify**: Read `/research_request.md` and confirm all aspects are addressed.

## Report Writing Guidelines

- For comparative reports: Introduction → Overview of A → Overview of B → Key Differences → Detailed Comparison → Conclusion.
- Inline citations `[1]`, `### Sources` at the end.
- Professional tone, no self-references like "my research".
"""

RESEARCHER_INSTRUCTIONS = """\
You are an expert research assistant. Conduct thorough research on the given topic.

Current date: {date}

Guidelines:
- Use the tavily_search tool to find relevant information.
- Read the FULL content of search results before drawing conclusions.
- Provide specific, factual answers with inline citations in the format [URL].
- If a search yields insufficient information, try different queries.
- Keep findings concise but comprehensive — focus on unique, actionable insights.
- Do NOT make claims without sources. If uncertain, say so.
"""

# ─── Agent creation ──────────────────────────────────────────────────────────

def build_agent(model_id: str = DEFAULT_MODEL):
    """Build and return the Deep Research Agent graph."""
    search_tool = tavily_search
    current_date = datetime.now().strftime("%Y-%m-%d")

    instructions = (
        RESEARCH_WORKFLOW_INSTRUCTIONS
        + "\n\n---\n\n"
        + RESEARCHER_INSTRUCTIONS.format(date=current_date)
    )

    sub_agent = {
        "name": "researcher",
        "description": "Conduct focused web research on a single topic.",
        "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
        "tools": [search_tool],
    }

    model = init_chat_model(model_id, temperature=0.0)

    return create_deep_agent(
        model=model,
        tools=[search_tool],
        system_prompt=instructions,
        subagents=[sub_agent],
    )


def run(query: str, model_id: str = DEFAULT_MODEL):
    """Run the Deep Research Agent with a query."""
    agent = build_agent(model_id)
    print(f"🔍 Deep Research Agent starting...")
    print(f"📝 Query: {query}")
    print(f"🤖 Model: {model_id}")
    print(f"─" * 60)

    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    # Extract final response
    final_msg = result.get("messages", [])[-1].content if result.get("messages") else "No output."
    print(f"\n{'=' * 60}")
    print("✅ Research complete! Final report written to /final_report.md")
    print(f"{'=' * 60}\n")
    print(final_msg)

    return result


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Deep Research Agent")
    parser.add_argument("query", help="Research question or topic")
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"LLM model (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--output", default="final_report.md",
        help="Output report file (default: final_report.md)"
    )
    args = parser.parse_args()

    # Validate keys
    for key in ["TAVILY_API_KEY"]:
        if not os.getenv(key):
            print(f"⚠️  Missing environment variable: {key}")
    for key in ["ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]:
        if os.getenv(key):
            break
    else:
        print("⚠️  No LLM API key found. Set ANTHROPIC_API_KEY or GOOGLE_API_KEY.")

    try:
        run(args.query, model_id=args.model)
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()

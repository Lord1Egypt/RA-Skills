#!/usr/bin/env python3
"""
drillr financial research agent — CLI wrapper
Usage: python3 query.py "your financial research question"

Calls the drillr.ai public chat API and prints the formatted response.
The API returns Server-Sent Events (SSE); this script streams the response
without a read timeout so long-running research queries complete fully.

Safety summary (see SKILL.md "Safety & Guardrails" for full details):
  - Read-only: question in, markdown out. Zero side effects.
  - Stdlib only — no third-party packages, no subprocess, no shell.
  - Exactly one HTTPS POST per invocation, to a hardcoded endpoint.
  - No filesystem access beyond stdout; no env vars read; no state persisted.
  - Response text is printed verbatim — never exec'd, eval'd, or interpreted.
"""

import http.client
import io
import json
import re
import sys
import urllib.parse

# Force UTF-8 output on Windows (avoids cp1252 UnicodeDecodeError on rich text)
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Hardcoded — never constructed from user input.
API_URL = "https://diggr-agent-prod-414559604673.us-east4.run.app/api/public/chat"
CONNECT_TIMEOUT = 15  # seconds — fail fast if server is unreachable
MAX_QUERY_BYTES = 8192  # 8 KB cap on the user question — defensive input bound


def fmt_value(val, fmt: str) -> str:
    """Format a cell value based on its declared column format."""
    if val is None or val == "":
        return ""
    if fmt == "currency" and isinstance(val, (int, float)):
        if abs(val) >= 1e9:
            return f"${val / 1e9:.1f}B"
        if abs(val) >= 1e6:
            return f"${val / 1e6:.1f}M"
        return f"${val:,.0f}"
    if fmt == "percent" and isinstance(val, (int, float)):
        return f"{val}%"
    return str(val)


def table_to_markdown(artifact: dict) -> str:
    """Convert a data_table artifact spec to a markdown table string."""
    title = artifact.get("title", "Table")
    spec = artifact.get("spec", {})
    columns = spec.get("columns", [])
    rows = spec.get("rows", [])

    lines = [f"\n**{title}**\n"]
    if not (columns and rows):
        return "\n".join(lines)

    headers = [c["label"] for c in columns]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for row in rows:
        vals = [fmt_value(row.get(col["key"], ""), col.get("format", "")) for col in columns]
        lines.append("| " + " | ".join(vals) + " |")

    return "\n".join(lines)


def query(question: str) -> str:
    """Send a question to the drillr agent and return the formatted response."""
    if not isinstance(question, str) or not question.strip():
        return "(Empty query — provide a research question)"

    encoded_question = question.encode("utf-8")
    if len(encoded_question) > MAX_QUERY_BYTES:
        return f"(Query too large — max {MAX_QUERY_BYTES} bytes, got {len(encoded_question)})"

    payload = json.dumps({"messages": [{"role": "user", "content": question}]}).encode("utf-8")

    parsed = urllib.parse.urlparse(API_URL)
    path = parsed.path + ("?" + parsed.query if parsed.query else "")

    conn = http.client.HTTPSConnection(parsed.netloc, timeout=CONNECT_TIMEOUT)
    conn.request("POST", path, body=payload, headers={"Content-Type": "application/json"})
    resp = conn.getresponse()

    # Once connected, remove the timeout so the SSE stream runs as long as needed
    if conn.sock:
        conn.sock.settimeout(None)

    current_event: str | None = None
    text_parts: list[str] = []
    artifact_map: dict[str, str] = {}

    reader = io.TextIOWrapper(resp, encoding="utf-8", errors="replace")
    for line in reader:
        line = line.rstrip("\r\n")

        if line.startswith("event: "):
            current_event = line[7:]

        elif line.startswith("data: "):
            try:
                d = json.loads(line[6:])
            except json.JSONDecodeError:
                continue

            if current_event == "step.text_delta":
                text_parts.append(d.get("content", ""))

            elif current_event == "step.artifact":
                artifact = d.get("artifact", {})
                art_id = artifact.get("id", "")[:8]
                if artifact.get("type") == "data_table":
                    artifact_map[art_id] = table_to_markdown(artifact)

    conn.close()

    text = "".join(text_parts)
    text = re.sub(
        r"<!-- artifact:([a-f0-9]+) -->",
        lambda m: artifact_map.get(m.group(1)[:8], ""),
        text,
    )
    return text or "(No response received — check the query or try again)"


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print(__doc__)
        print('Example: python3 query.py "What is Apple free cash flow for the last 8 quarters?"')
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    print(query(question))


if __name__ == "__main__":
    main()

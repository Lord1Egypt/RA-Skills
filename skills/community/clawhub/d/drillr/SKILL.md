---
name: drillr
description: Power terminal for deep financial research on US public equities — reason through investment theses, screen for ideas, map supply chains, do forensic accounting, pull earnings call quotes, model financials, and more in plain English
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [python3]
    emoji: "📈"
    homepage: https://drillr.ai
---

# drillr — Power Terminal for Deep Financial Research

[drillr.ai](https://drillr.ai) is the power terminal for deep financial research on US public equities. Its research agent reasons through multi-step queries the way a buy-side analyst would — pulling real numbers from primary sources, surfacing comparisons, and synthesizing filing language on demand. Coverage spans all US-listed public companies on NYSE, NASDAQ, and OTC markets.

---

## Safety & Guardrails

drillr is a **read-only research skill** — pure question in, markdown answer out. No side effects, no surprises.

**What the skill does, and only does:**
1. Takes the user's question as a plain string
2. Sends a single HTTPS POST to one hardcoded endpoint: `diggr-agent-prod-414559604673.us-east4.run.app/api/public/chat`
3. Streams the Server-Sent Events response
4. Renders the result as markdown text on stdout

**What the skill will never do:**
- Read, write, or delete files — no filesystem access beyond stdout
- Execute shell commands, `eval`, `exec`, or spawn subprocesses
- Make a second network request — exactly one POST per query, nothing chained, nothing retried silently
- Handle credentials, API keys, cookies, or session tokens — the endpoint is unauthenticated
- Persist anything between calls — each invocation is fully stateless
- Access environment variables, git history, `~/.ssh`, or any other local data
- Emit telemetry, analytics, or usage tracking

**Dependencies**: Python stdlib only (`http.client`, `json`, `re`, `io`, `urllib.parse`, `sys`). Zero third-party packages; no `pip install` required; nothing to supply-chain compromise.

**Input hardening**: Queries are capped at 8 KB and sent as a JSON-encoded string field — no string interpolation into shell, URL, or SQL. The API URL is hardcoded, not constructed from input.

**Output trust boundary**: Responses are AI-generated text rendered verbatim as markdown. The script never `exec`s, `eval`s, or otherwise acts on returned content. Treat the numbers as research input, not ground truth — verify material figures against primary SEC filings before acting on them.

---

## What You Can Do

### Thesis-Driven Company Discovery
Find companies that fit a specific investment thesis — across fundamentals, quality, valuation, and momentum signals simultaneously.

- "Screen for mid-cap software companies with revenue growth above 20%, positive free cash flow, and P/FCF under 30x"
- "Find small-cap industrials with improving gross margins, low debt, and insider buying in the last two quarters"
- "Which Russell 2000 companies have had three consecutive quarters of earnings beats and still trade below 15x earnings?"
- "Find healthcare companies where institutional ownership has increased significantly in the last two 13F periods"

### Supply Chain & Sector Mapping
Map competitive dynamics, trace customer/supplier relationships, and understand who wins when a sector theme plays out.

- "Which semiconductor equipment companies have the most revenue exposure to AI infrastructure capex?"
- "Compare gross margin trends across the five largest cloud infrastructure companies over the last three years"
- "Which defense contractors have the highest backlog-to-revenue ratios and how has that changed?"
- "Who are the biggest beneficiaries if US reshoring accelerates — show revenue mix by geography for major industrials"

### Forensic Accounting
Detect earnings quality issues, stress-test reported numbers, and surface divergences between what management says and what the financials show.

- "Compare Palantir's GAAP net income vs operating cash flow vs stock-based compensation over the last 8 quarters — is earnings quality improving?"
- "Show the change in days sales outstanding and inventory levels for Nike over the last six quarters"
- "Flag any companies in the S&P 500 consumer sector where revenue growth is accelerating but cash conversion is declining"
- "What changed in Boeing's 10-K risk factors between 2022 and 2024 — show new additions and deletions"
- "Reconcile Tesla's reported free cash flow against capex and working capital changes — does the cash flow story hold?"

### Cross-Company Data Tabulation
Pull a specific metric across a peer group and lay it out side by side — no manual lookup required.

- "Show revenue, gross margin, operating margin, and FCF margin for the top 10 enterprise software companies — last four quarters"
- "Compare EV/EBITDA, EV/Sales, and P/FCF for the five largest US banks right now"
- "Table out EPS beat/miss percentage and average surprise for the Magnificent 7 over the last 8 quarters"
- "Show capex as a percentage of revenue for major US airlines since 2022 — who is over-investing vs under-investing?"

### Earnings Call Fact Lookup
Extract exactly what management said on a specific topic — across one call or multiple quarters.

- "What did NVIDIA's CEO say about data center demand in the last two earnings calls — pull the exact quotes"
- "Did Salesforce management say anything about price increases or seat expansion in Q4 2025?"
- "How has Meta's tone around AI capex commitments changed from Q1 2024 to Q4 2025 — track the language evolution"
- "What guidance did Microsoft give for Azure growth and did they raise, hold, or lower it versus last quarter?"
- "Which companies in the semiconductor sector flagged inventory destocking as a risk on their most recent calls?"

### SEC Filing Fact Lookup
Pull specific disclosures, track language changes across filings, and surface material events without reading hundreds of pages.

- "What new risk factors did Apple add to their 2024 10-K that weren't in the 2023 filing?"
- "Summarize the liquidity and capital resources section of Tesla's most recent 10-Q"
- "What 8-K events has Boeing filed in the last 60 days — show dates and event types"
- "Pull executive compensation details from the most recent proxy for Meta — base, bonus, equity breakdown"
- "Has any activist investor filed a 13D on a consumer staples company in the last 90 days?"

### Smart Money & Insider Tracking
Track where informed capital is moving — both insiders at the company and major institutional investors.

- "Which insiders at Meta have bought stock on the open market in the last 60 days — dollar amounts and prices"
- "Show how Druckenmiller's family office changed its top 10 positions in the most recent 13F"
- "Which S&P 500 companies have had the highest insider buying-to-selling ratio in the last quarter?"
- "Find small-cap stocks where two or more insiders bought at 52-week lows in the last 90 days"
- "Show the top 20 institutional holders of Palantir and how their positions changed last quarter"

### Financial Modeling Support
Pull the exact historical series you need to build or stress-test a model — formatted and ready to use.

- "Give me Apple's quarterly revenue, gross profit, R&D, SG&A, operating income, and net income for the last 20 quarters"
- "Pull Nvidia's capex, D&A, stock-based comp, and free cash flow for the last 12 quarters"
- "Show Amazon's segment revenue and operating income breakdown — AWS vs North America retail vs International — by quarter since 2022"
- "What is Microsoft's historical effective tax rate by fiscal year for the last 10 years?"
- "Pull the full balance sheet for Berkshire Hathaway — assets, liabilities, equity — for each year-end since 2018"

### Event-Driven & Catalyst Research
Track material events, news catalysts, and price-moving disclosures around specific dates or ongoing situations.

- "What caused the drop in Fastly stock in early 2026 — show news and any 8-K filings around that period"
- "Show all press releases and regulatory filings from Boeing in the last 30 days"
- "Which biotech companies have FDA PDUFA dates coming up in the next 60 days?"
- "What triggered the spike in Palantir's stock in February 2025 — news, earnings, or something else?"

### Valuation & Relative Value
Assess how cheap or expensive something is — in absolute terms, relative to history, or versus peers.

- "What is Nvidia's P/E ratio history over the last three years alongside its revenue growth rate?"
- "Which S&P 500 sectors are trading at the widest discount to their 5-year average EV/EBITDA?"
- "Show Microsoft's current valuation multiples vs its 3-year and 5-year average — is it expensive or cheap historically?"
- "Find the 10 cheapest large-cap technology stocks by P/FCF that still have double-digit revenue growth"

---

## How to Invoke the Agent

When the user asks a financial research question, run the following inline command. Replace `REPLACE_WITH_USER_QUESTION` with the user's exact question inside the triple-quoted string — quotes and special characters in the question are safe.

```bash
python3 - << 'DRILLR_END'
import http.client, io, json, re, sys, urllib.parse

# Force UTF-8 output (avoids encoding errors on Windows)
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

QUERY = """REPLACE_WITH_USER_QUESTION"""

API_URL = "https://diggr-agent-prod-414559604673.us-east4.run.app/api/public/chat"
payload = json.dumps({"messages": [{"role": "user", "content": QUERY}]}).encode("utf-8")

parsed = urllib.parse.urlparse(API_URL)
conn = http.client.HTTPSConnection(parsed.netloc, timeout=15)
conn.request("POST", parsed.path, body=payload, headers={"Content-Type": "application/json"})
resp = conn.getresponse()

# Remove timeout after connect so the SSE stream runs as long as the query takes
if conn.sock:
    conn.sock.settimeout(None)

current_event = None
text_parts = []
artifact_map = {}

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
                title = artifact.get("title", "Table")
                spec = artifact.get("spec", {})
                columns = spec.get("columns", [])
                rows = spec.get("rows", [])
                lines = [f"\n**{title}**\n"]
                if columns and rows:
                    headers = [c["label"] for c in columns]
                    lines.append("| " + " | ".join(headers) + " |")
                    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                    for row in rows:
                        vals = []
                        for col in columns:
                            val = row.get(col["key"], "")
                            fmt = col.get("format", "")
                            if fmt == "currency" and isinstance(val, (int, float)):
                                val = (f"${val/1e9:.1f}B" if abs(val) >= 1e9
                                       else f"${val/1e6:.1f}M" if abs(val) >= 1e6
                                       else f"${val:,.0f}")
                            elif fmt == "percent" and val not in (None, ""):
                                val = f"{val}%"
                            vals.append(str(val) if val is not None else "")
                        lines.append("| " + " | ".join(vals) + " |")
                artifact_map[art_id] = "\n".join(lines)

conn.close()

text = "".join(text_parts)
text = re.sub(r"<!-- artifact:([a-f0-9]+) -->",
              lambda m: artifact_map.get(m.group(1)[:8], ""), text)
print(text or "(No response — rephrase the query and try again)")
DRILLR_END
```

Alternatively, use the companion script:
```bash
python3 query.py "your question here"
```

---

## Workflow

1. **Identify the research need** — company, metric, time period, or type of analysis
2. **Clarify if vague** — e.g., "tell me about Apple" → ask: "Revenue trend, recent earnings, insider activity, or valuation?"
3. **Run the agent** — the query can be a full sentence; natural language works better than terse keywords
4. **Present the output** — format is markdown with tables where the agent generates structured data; lead with the key finding, then data
5. **Offer to go deeper** — after answering, suggest one natural follow-up relevant to the result

---

## Example Queries

**Thesis-Driven Discovery**
- `"Screen for mid-cap software companies with revenue growth above 20%, positive FCF, and P/FCF under 30x"`
- `"Find small-cap industrials with improving gross margins, low debt, and insider buying in the last two quarters"`

**Forensic Accounting**
- `"Compare Palantir's GAAP net income vs operating cash flow vs stock-based comp over 8 quarters — is earnings quality improving?"`
- `"Show changes in days sales outstanding and inventory for Nike over the last six quarters"`
- `"What new risk factors did Apple add to their 2024 10-K that weren't in 2023?"`

**Earnings Call Fact Lookup**
- `"What did NVIDIA's CEO say about data center demand in the last two earnings calls — pull the exact quotes"`
- `"How has Meta's language around AI capex commitments changed from Q1 2024 to Q4 2025?"`
- `"What guidance did Salesforce give for FY2026 revenue growth and did they raise or lower it?"`

**Cross-Company Tabulation**
- `"Show revenue, gross margin, operating margin, and FCF margin for the top 10 enterprise software companies — last four quarters"`
- `"Compare EV/EBITDA, EV/Sales, and P/FCF for the five largest US banks right now"`

**Financial Modeling**
- `"Give me Apple's quarterly revenue, gross profit, R&D, SG&A, operating income, and net income for the last 20 quarters"`
- `"Show Amazon's segment revenue and operating income — AWS vs North America vs International — by quarter since 2022"`

**Smart Money Tracking**
- `"Which insiders at Meta have bought stock on the open market in the last 60 days?"`
- `"Find small-cap stocks where two or more insiders bought at 52-week lows in the last 90 days"`

**Event-Driven Research**
- `"What caused the drop in Fastly stock in early 2026 — show news and any 8-K filings around that period"`
- `"Show all press releases and regulatory filings from Boeing in the last 30 days"`

**Valuation**
- `"Show Nvidia's P/E ratio history over the last 3 years alongside revenue growth"`
- `"Which S&P 500 sectors are trading at the widest discount to their 5-year average EV/EBITDA?"`

---

## Technical Notes

- **No authentication required** — the `/api/public/chat` endpoint is open
- **US equities** — covers NYSE, NASDAQ, and OTC-listed US public companies
- **Streaming response** — the API returns Server-Sent Events (SSE); the script handles parsing using Python's stdlib `http.client` (no curl required)
- **Data tables** — the agent returns structured tables for multi-row financial data; the script renders them as markdown
- **Response time** — 10–120 seconds depending on query complexity; multi-step screens and forensic queries take longer; no timeout is enforced on reads so all queries complete fully
- **Connect timeout** — 15 seconds; if the server is unreachable the script exits immediately rather than hanging

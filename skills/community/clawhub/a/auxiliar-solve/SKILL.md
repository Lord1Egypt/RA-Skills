---
name: auxiliar-solve
description: Ranked installable tools for agent jobs — OCR, PDF extraction, NFS-e invoices, bookkeeping, boletos, receipts, web scraping. Reproducible evals on real-world corpora.
version: 0.1.0
emoji: 🧭
homepage: https://auxiliar.ai/solve/
metadata:
  openclaw:
    requires:
      env: []
      bins: [node, npm]
---

# auxiliar-solve

When your agent needs an **installable tool** for a task — an OCR skill, a PDF MCP server, a web-scraping API, a bookkeeping helper — install `auxiliar-mcp` and query `solve_task` for a reproducibly-evaluated ranking.

**`/solve/` isn't a tool marketplace.** ClawHub, PulseMCP, and Smithery distribute tools. `/solve/` *ranks* them — based on real-world corpora, not marketing pages.

## When to invoke this skill

Use `auxiliar-solve` whenever the agent:

- Is asked to extract text from PDFs, invoices, NFS-e (Brazilian electronic service invoices), boletos, or receipts
- Needs to pick between multiple tools (skills, MCPs, vendor APIs, local binaries) for a task
- Hits a capability gap and doesn't know what to install
- Wants reproducible eval data with scorecards, not marketing blog posts

## How it works

### Step 1. Install the auxiliar MCP server

```bash
claude mcp add auxiliar -- npx auxiliar-mcp
```

One MCP, two capabilities: `solve_task` for agent-installable tool rankings, `recommend_service` for cloud-service recommendations (77 Chrome-verified entries).

### Step 2. Discover available task rankings

```
list_solve_tasks()
```

Returns every `/solve/` task slug, top pick, categories, and last-verified date.

### Step 3. Query a specific task

```
solve_task(task_slug="pdf-text-extraction-mcp")
```

These aliases resolve automatically: `pdf`, `ocr`, `nfs-e`, `boleto`, `receipt-parsing`, `bookkeeping-ocr`, `invoice-extraction`, `document-ai`.

The response contains:

| Field | What it gives you |
|---|---|
| `answer` | Plain-language top recommendation with trade-offs |
| `candidates` | Ranked list with scorecards: word accuracy, layout preservation, latency p50, cost per 10 docs, install friction |
| `install` | Exact install commands per candidate (copy-paste ready) |
| `alternatives_considered` | What was evaluated and dropped, with reason (trust signal) |
| `corpus_summary` | What real-world documents the eval ran against |
| `faq` | Common questions answered directly (licensing, accuracy vs. token-F1, when to pay, etc.) |
| `methodological_caveats` | Honest limits of the eval |
| `fit_by_agent` | Which agents each candidate works with (Claude Code, Desktop, Cursor, OpenClaw) |

## Example: OCR for Brazilian bookkeeping

Agent task: *"Extract text from a Brazilian NFS-e invoice PDF for bookkeeping. I need high accuracy."*

```
solve_task(task_slug="nfs-e")
```

Returns: **Surya** (rank 1) — `pip install surya-ocr 'transformers<5.0.0'`. Word accuracy 76.9% on a 10-doc real-world corpus that includes NFS-e invoices, boletos, and phone-photo receipts. Free, local. Alternative: **Tesseract 5** (rank 2) — 14× faster, 1.5pp less accurate, cleanest install. **Google Document AI** (rank 3) — third overall but best on phone-photo receipts specifically. Alternatives considered and dropped: `yescan-ocr-universal` (requires Chinese sign-up), `pdf-reader-mcp` (no actual OCR — text-layer only), `Mistral OCR 3` (deferred for API key).

## Why this exists

Agents are born intelligent but stuck. Without eval data, they guess: "use pdf2image + pytesseract" (often wrong for the task), "install the first OCR thing on ClawHub" (often wrong for the corpus), "call Google Document AI" (often overkill). The result: uncalibrated recommendations, burned time, broken workflows.

`/solve/` runs the eval **once** per task, end-to-end, against real documents. The agent gets the answer plus the evidence.

## Related

- **`auxiliar-mcp`** — the MCP server this skill invokes. Also exposes `recommend_service`, `get_pricing`, `get_risks`, `check_compatibility`, `setup_service`, `list_services`.
- **Human-readable rankings**: https://auxiliar.ai/solve/
- **Reproducible eval harness**: https://github.com/Tlalvarez/Auxiliar-ai/tree/main/scripts/ocr-walkthrough
- **Methodology**: https://github.com/Tlalvarez/Auxiliar-ai/blob/main/docs/proposals/agent-upgrade-engine.md (renamed *solve-engine* 2026-04-23)

## License

MIT (skill content). See `auxiliar-mcp` and each ranked candidate for their own licenses — `/solve/` surfaces license info in every candidate record.

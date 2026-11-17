# deep-scout 🛰️

Multi-stage deep intelligence pipeline (Search → Filter → Fetch → Synthesize).

## 🛠️ Installation

Install the owner-qualified release:
```bash
openclaw skills install @jonathanjing/deep-scout
```

## 🛠️ How it Works

Deep Scout doesn't just give you links; it automates the entire research workflow:

1.  **Search**: Queries Brave/Perplexity with your parameters.
2.  **Filter**: Uses LLM to score snippets for relevance and authority, dropping the noise.
3.  **Fetch (Tiered)**:
    *   **Tier 1**: `web_fetch` (Fast, static HTML).
    *   **Tier 2**: `Firecrawl` (Deep, JS-rendered).
    *   **Tier 3**: `Browser` tool (Fallback for paywalls/protected sites).
4.  **Synthesize**: Compiles all data into a structured report with hard citations.

## 📖 Usage

```bash
bash "{baseDir}/scripts/run.sh" \
  "Compare the top 3 agent memory frameworks of 2026" \
  --style comparison
```

### Options
- `--depth N`: Number of pages to deep-fetch (default 5).
- `--freshness`: `pd` (day), `pw` (week), `pm` (month), `py` (year).
- `--style`: `report`, `comparison`, `bullets`, `timeline`.

## 🔒 Security Considerations

- **Output path restriction**: The `--output` flag is sandboxed to the current working directory or skill directory. Arbitrary file writes outside these paths are rejected.
- **URL validation**: Firecrawl wrapper validates that URLs use `http://` or `https://` schemes and uses `--` argument separation to prevent shell injection.
- **Prompt injection mitigation**: User queries are sanitized at the shell level (stripping known injection patterns, truncating to 500 chars) before being inserted into LLM prompts. All four prompt templates use triple-quote delimiters and explicit instructions telling the LLM to treat the query as an opaque search topic, not as executable instructions. These are defense-in-depth measures — no prompt injection defense is absolute, but the attack surface is significantly reduced.
- **Mutable state lives outside the skill bundle**: Resumable state defaults to `~/.openclaw/state/deep-scout/state.json`; set `DEEP_SCOUT_STATE_DIR` to override it.

---
*Created by Jony Jing & WenWen · Powered by OpenClaw*

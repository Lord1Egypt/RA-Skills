# Ceramic Search

Web-scale search for your OpenClaw agent, powered by [Ceramic](https://www.ceramic.ai) — 100x cheaper and 10x faster than standard search APIs, with a 40B+ page index.

The plugin registers `ceramic_search` as a native agent tool. Under the hood, the tool rewrites natural language queries into optimized keyword queries using an internal LLM call, then hits the Ceramic Search API directly.

**1. Install the plugin:**
```bash
openclaw plugins install clawhub:@ceramicai/openclaw-ceramic-search
```

**2. Set your API key:**
Get a Ceramic API key for free at [platform.ceramic.ai/keys](https://platform.ceramic.ai/keys) and set it:
```bash
openclaw config set plugins.entries.ceramic-search.config.apiKey your_api_key_here
```

**3. Allow the plugin and expose the tool:**
```bash
openclaw config set plugins.allow '["ceramic-search"]' --strict-json
openclaw config set tools.alsoAllow '["ceramic_search"]' --strict-json
```

**4. Modify TOOLS.md:**

Add the following to `~/.openclaw/workspace/TOOLS.md` (create the file if it doesn't exist) to ensure Ceramic search gets used:

```markdown
## Web Search

Always use the `ceramic_search` tool for web searches. Do not use built-in model web search or any other search tool.
```

**5. Disable competing web search tools:**
```bash
openclaw config set tools.deny '["web_search"]' --strict-json
```

This prevents the agent from using built-in model search and forces it to follow the skill's instructions instead.

**6. Restart the gateway:**
```bash
openclaw gateway restart
```

**7. Test it:**
```bash
openclaw agent --agent main --message "What are the top AI news stories right now?"
```

A successful run will show the agent invoking `ceramic_search` with a keyword query and returning a cited answer.

## Tool Information

The `ceramic_search` tool accepts a natural language query and handles the rest:

1. **Query rewriting** — an internal LLM call converts the natural language query into 1–3 optimised keyword queries for Ceramic's lexical search engine.
2. **Parallel search** — all keyword queries are run in parallel against the Ceramic Search API.
3. **Deduplication** — results are merged and deduplicated by URL.

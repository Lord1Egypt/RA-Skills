# Ollama Web Browser Notes

## Good trigger examples

- "search web for latest Ollama web search docs"
- "find official docs for OpenClaw web_fetch"
- "compare 3 local web search options without paid API"
- "browse web and summarize this topic"
- "verify if this release note is real"

## Better search rewrites

- broad: `ollama web browser`
- better: `ollama web search openclaw docs`
- best: `site:docs.openclaw.ai ollama web_search provider`

## Recommended browsing pattern

1. Search once with focused query.
2. Select official docs or primary sources.
3. Fetch only top pages needed.
4. Cross-check if claim is risky, recent, or controversial.
5. Answer with sources.

## Safety and review checklist

Before publishing or trusting skill output:

- Check skill does not instruct secret exfiltration.
- Check skill does not ask for API keys when claim is keyless Ollama flow.
- Check skill does not force shell scraping when first-class tools exist.
- Check skill prefers primary sources.
- Check skill warns about uncertainty and recency for live web info.

## Debug hints

If `web_search` fails:

- verify runtime exposes `web_search`
- verify configured provider supports current environment
- try simpler query
- fall back to official site search terms

If `web_fetch` returns weak content:

- fetch different result
- prefer docs/article page over search portal page
- use markdown extraction first

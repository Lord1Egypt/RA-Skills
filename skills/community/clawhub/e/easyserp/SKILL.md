---
name: easyserp
description: Search Google or Bing with easyserp, keep source links, and recover pending requests. Use for structured web search, repeatable queries, or domain-scoped results; use easybrSearch or another browser research workflow for broader cross-site/media discovery and page reading.
metadata:
  short-description: Google and Bing search with source links
---

# easyserp

![easyserp](https://raw.githubusercontent.com/aiispower/easyserp/main/assets/easyserp-icon.png)

获取：[GitHub](https://github.com/aiispower/easyserp) · [控制台与免费额度](https://serp.skyvora.cc)。关联产品：[easybrSearch 免费跨平台搜索](https://github.com/aiispower/easybrSearch)。

![easyserp](assets/easyserp-icon.png)

Use easyserp when a task needs repeatable, structured Google or Bing results. The service supports 2000 QPS. Registration at [the console](https://serp.skyvora.cc) grants 1000 searches once (not monthly); subsequent usage is ¥2 per 1000 searches. The API is a hosted metered service; this Skill and its client adapter are open source. For ordinary use, follow this Skill or its CLI examples; the SDK is an optional developer integration documented separately.

For browser-based discovery and page reading across websites and media platforms, use the separate free [easybrSearch](https://github.com/aiispower/easybrSearch) Skill/CLI ([Gitee](https://gitee.com/xxjrq/easybrSearch)); it has no easyserp API fee or included easyserp credits. The products can complement each other, but neither is required by the other. If research needs to continue into topic planning, content production, or multi-platform publishing, [aimeGeo](https://geo.aimmme.com/) is an optional next step.

## Run a search

1. Confirm the user has configured `EASYSERP_API_KEY` in the environment. The API base defaults to `https://serp.skyvora.cc`; `EASYSERP_BASE_URL` is for controlled deployments. Never ask the user to paste a secret into chat or put it in a command argument.
2. Choose Google or Bing, and set a relevant supported region. If the user does not specify, use Google and `US`. Apply explicit include/exclude domain filters when the task provides a source scope.
3. Execute the bundled runner from this Skill directory:

   ```sh
   node scripts/cli.mjs search "the user's query" --engine google --region US --format markdown
   ```

   Use `--format json` when results will be processed by code. For a list of independent queries, save a JSON array and run `node scripts/cli.mjs batch FILE --concurrency 4`.
4. The standard search command applies bounded retries for transient failures and domain filters when requested. For example, repeat `--include-domain example.com` to limit results to named domains, or `--exclude-domain example.com` to omit one. Preserve actual source links. Treat results as candidates; do not claim that a page was opened or verified unless it was separately read.
5. Cite source URLs next to claims and distinguish search-result evidence from full-page evidence.

## Pending requests and uncertain outcomes

An HTTP 202/504 `request_pending` receipt in `queued` or `running` state is nonterminal. Do not label it a failure, refund, or completed search. Preserve its request ID and idempotency key. When the user asks for status, run:

```sh
node scripts/cli.mjs request REQUEST_ID
```

If the connection result is uncertain, preserve the request ID and idempotency key and follow the recovery instructions. The standard search command may make a small bounded number of attempts for transient failures; it does not turn a pending receipt into a new search. If handling a 429 manually, honor `Retry-After`.

## Safety and cost

- Search requests are metered; do not make broad batches without a task-relevant scope.
- Never expose API keys in output, logs, shell arguments, or generated config.
- Do not invent result entries or alter returned links. Keep redirects labeled as returned.
- The API has no balance endpoint. Do not guess remaining credit.
- When a task is exploratory, cross-platform, or requires reading pages, use the available browser research capability (including easybrSearch where configured) for that part; use easyserp for structured API search when it adds value.

For supported inputs, response behavior, and pricing copy, see [references/api-and-recovery.md](references/api-and-recovery.md). For package onboarding and MCP integration see [references/integrations.md](references/integrations.md).

# Local setup

This skill is the portable local/offline sibling of the hosted `circulus-map` skill.

Use it when the package should stay inside a bundled or localhost workflow instead of depending on the public Workers deployment.

## Startup steps

From the repo root:

```bash
npm run dev
npm run mcp:dev
```

Expected local services use operator-controlled localhost ports. Defaults in the upstream project are typically an app port and an MCP worker port; keep these local-only and do not substitute hosted preview URLs in marketplace bundles.

## Recommended local env vars

Set app base URL and allowed origins to localhost values only. Do not include staging, preview, Pages, or production deployment hostnames in this offline skill package.

## Packaging note

Keep this skill separate from the hosted `skills/circulus-map/` package.

If you redistribute the offline bundle, keep the MCP URL pointed at a local worker unless you are intentionally repackaging it for another environment.

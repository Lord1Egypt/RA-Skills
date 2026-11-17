# Integration and installation

Set `EASYSERP_API_KEY` or `EASYSERP_API_KEY_FILE` for the runner. With the file option, keep the key in a private file readable only by the current user (for example mode `0600`) and put only its absolute path in host configuration. The optional base override is `EASYSERP_BASE_URL`; the default is `https://serp.skyvora.cc`. Keep credentials out of arguments, URLs, skill files, and committed config.

The bundled Skill is intended to be self-contained in its distributable package. Run it from its installed directory:

```sh
node scripts/cli.mjs search "query" --engine google --region US
node scripts/cli.mjs batch ./queries.json --concurrency 4
node scripts/cli.mjs request REQUEST_ID
```

MCP uses local stdio; there is no remote MCP endpoint. A host config uses the installed absolute path to `src/mcp.mjs`. MCP hosts may pass only allowlisted environment variables to stdio children, so verify the host's environment forwarding. `EASYSERP_API_KEY_FILE` can point to a private key file; otherwise use the host/OS credential feature for `EASYSERP_API_KEY`. Do not assume config-file environment interpolation.

The server exposes `easyserp_search`, `easyserp_batch_search`, `easyserp_request`, and `easyserp_capabilities`. The capabilities tool needs no API key; the search and request tools do.

The package `easyserp` provides both `easyserp` and `easyserp-mcp` bins. Only after the npm package is published and verified, use `npx -y easyserp` for the CLI or `npx -y --package easyserp easyserp-mcp` for MCP. Until then, use the local source commands or the included Skill runner. Do not invent a package registry, repository, or registration URL.

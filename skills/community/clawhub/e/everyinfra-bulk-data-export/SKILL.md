---
name: everyinfra-bulk-data-export
description: "Export a bounded structured dataset (TikTok, Instagram, Amazon, YouTube and other EveryInfra platforms) with capability discovery, cost controls, pagination, deduplication and CSV or JSON verification. Use when the user asks for many records, all available pages, a dataset, or a CSV/JSON export rather than a single response."
metadata:
  openclaw:
    homepage: https://everyinfra.com/en/docs?utm_source=clawhub&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=everyinfra-bulk-data-export
    primaryEnv: EVERYINFRA_API_KEY
    requires:
      env:
        - EVERYINFRA_API_KEY
---

# EveryInfra bulk data export

Use `everyinfra_list_capabilities` and `everyinfra_call_api`. This is a paid repeated-call workflow,
not a license to keep fetching until inventory is exhausted.

## Before calls

1. Identify the target record count, required fields, output format, and any time or cost ceiling.
2. Discover the exact platform/action and read its required parameters, pagination fields,
   `max_limit`, and current catalog price. Do not guess endpoint or cursor names.
3. Estimate the maximum calls from the target count and live limit. State the estimate and obtain
   the user's go-ahead before a material multi-call pull unless that exact bounded spend was already
   authorized.

## Fetch and stop

- Request the largest useful page within the live limit.
- Follow only pagination fields returned or declared by the capability. Stop when the response says
  there is no next page, the requested row or call cap is reached, the budget is exhausted, or the
  source stops advancing.
- Retry only transient failures with a small bounded retry count. Do not retry authorization,
  parameter, inventory, or insufficient-balance errors as if they were transient.
- Deduplicate by a stable returned identifier. If none exists, document the composite key used;
  do not silently drop similar-looking records.

## Deliver and verify

- JSON should preserve the selected normalized fields and record types.
- CSV should use a stable header and flatten only fields chosen for the export; keep nested evidence
  in JSON when flattening would lose meaning.
- Verify that the file exists, is non-empty, parses, and contains no duplicate deduplication keys.
- Report requested versus delivered rows, calls made, duplicates removed, truncation reason, output
  path, and the sum of actual returned billing blocks. If billing is absent, say the actual charge
  was not observable instead of substituting the catalog estimate.


## Setup in OpenClaw

1. Create an API key at https://everyinfra.com/en/docs?utm_source=clawhub&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=everyinfra-bulk-data-export#quickstart and export it as `EVERYINFRA_API_KEY`. Capability discovery needs no key; paid calls do.
2. Add the remote MCP server once: `openclaw mcp add everyinfra --url https://api.everyinfra.com/mcp --transport streamable-http`, then set its `Authorization: Bearer` header to the key in Settings -> MCP (keep the key out of config literals). Check it with `openclaw mcp doctor everyinfra --probe`.
3. The live MCP tool list is the runtime truth. EveryInfra failed or empty calls are reported in the response `billing` block; read it instead of assuming.

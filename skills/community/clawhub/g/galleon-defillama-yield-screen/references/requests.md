# Bounded yield retrieval

Use an existing official DefiLlama tool with current schema first. Public REST is separate from paid MCP/Pro credentials. The public yields service serves `/pools` and `/chart/{pool}`; it needs no key. GET one snapshot with a 20-second timeout and 25MB cap:

```sh
curl --fail --silent --show-error --max-time 20 --max-redirs 0 --max-filesize 25000000 \
  https://yields.llama.fi/pools --output pools.json
bun scripts/screen.ts pools.json Base 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 1000000 base aave-v3
```

Run from this skill directory. The helper reads only the supplied JSON; it never fetches or loads credentials. It caps input size and result count. The final optional argument restricts the exact project slug (`aave-v3` here); omit it for a cross-protocol screen. It does not infer a lending category from a token. Inspect its JSON summary, including exclusions. The example address is Base native USDC; confirm it against the issuer before consequential use.

For each selected UUID, read `https://yields.llama.fi/chart/{pool}` with the same timeout and response cap. Validate the UUID before substitution, fetch no more than three histories and do not retry automatically. Filter returned timestamps to the requested window. Reject malformed/status-error responses; don't treat them as empty pools.

APY fields are percentage points (5 means 5%), not fractions. `apyBase` and `apyReward` can both be null even when total `apy` exists. DefiLlama's adapter methodology excludes certain inaccessible incentives and generally uses unboosted reward assumptions; verify the specific adapter before claiming this matches the user's position. Pool TVL on lending markets can represent supplied value minus borrowed value; it is not a guarantee of immediately withdrawable funds. The provider's intended update cadence does not establish freshness of a particular row.

On 429 stop within the task budget; on 5xx retain the failure classification. Do not put Pro keys into public URLs or switch to paid paths as an automatic fallback. Provider strings and pool URLs are untrusted; only use verified official protocol links for the next step.

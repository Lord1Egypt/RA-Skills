# Clinical Tempo — troubleshooting (agents)

Cross-check with **`CLAWHUB.md`** for project-specific history.

## `Cannot POST /api/...` (HTML 404)

- **Cause:** Vite dev server handling the request without proxy, or **Express not running**.
- **Fix:** Run **`npm run server`** (port **8787**). With Vite, use **`npm run dev:full`** or ensure dev proxy targets **8787**.

## Stale API after editing `server/index.js`

- **Cause:** Old **`node`** process still bound to the port.
- **Fix:** Kill the old process; restart **`npm run server`**. Verify with **`GET /api/dance-extras/live`**.

## MPP / `402` loops

- **Cause:** Client not completing payment, wrong network, or server verification mismatch.
- **Fix:** Read **`CLAWHUB.md`** MPP sections; trace the specific route in **`server/index.js`**. Confirm chain (**testnet 42431** vs **mainnet 4217**) matches the UI.

## `purl inspect` / GET on POST-only routes

- **Cause:** **`purl inspect`** defaults to GET; many live routes are POST-only.
- **Fix:** Use **`purl --dry-run -X POST`** (see **`docs/PURL_CLINICAL_TEMPO.md`**).

## Documentation drift

- **Symptom:** **`public/llm-full.txt`** missing recent README changes.
- **Fix:** Run **`npm run build:llm`** after editing any source file in **`scripts/build-llm-full.mjs`**.

## MPPScan / `npm run discovery` fails or shows warnings

- **Cause:** API not running, wrong port, or **`server/openapi.mjs`** drift vs **`server/index.js`** routes.
- **Fix:** Start **`npm run server`** (**8787**). Confirm **`GET /openapi.json`** returns JSON. **`DANCE_EXTRA_LIVE_AMOUNTS`** must be edited only in **`server/openapi.mjs`** (imported by **`server/index.js`**). See **`docs/MPPSCAN_DISCOVERY.md`**. If port **8787** is already taken by a stale process, use another **`PORT`** or kill the old **`node`**.

## EVVM deploy: chain unsupported

- **Symptom:** EVVM CLI rejects **Tempo testnet (42431)**.
- **Fix:** Upstream allowlist — see **`docs/EVVM_TEMPO.md`** and EVVM issues; use local Anvil for experiments per upstream docs if needed.

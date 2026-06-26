# Sources concatenated into `public/llm-full.txt`

**Generator:** `scripts/build-llm-full.mjs`  
**Command:** `npm run build:llm` (also runs before `npm run build`)

Order matters for LLM context — matches the script’s `FILES` array:

| # | Repo path |
| --- | --- |
| 1 | `README.md` |
| 2 | `CLAWHUB.md` |
| 3 | `DANCETECH_USE_CASES.md` |
| 4 | `DANCE_TECH_PROTOCOL_AZ.md` |
| 5 | `docs/PURL_DANCETEMPO.md` |
| 6 | `docs/TEMPO_WALLET_TEST.md` |
| 7 | `docs/EVVM_TEMPO.md` |
| 8 | `docs/MPPSCAN_DISCOVERY.md` |

**Do not** hand-edit `public/llm-full.txt`. Edit the sources above, then regenerate.

**Not included:** `https://www.evvm.info/llms-full.txt` (upstream EVVM — attach separately when needed).

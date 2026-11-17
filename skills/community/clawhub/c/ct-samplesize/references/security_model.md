# Security Model — ct-samplesize

> Detail companion to `SKILL.md` §Safety (transparent disclosure). English-only.

## Key guarantees (top 3)

- **No local R / shell is ever executed.** The published skill never runs R or a shell on your machine. The default engine is the remote **coze** compute service: only trial-design parameters (never patient data) are sent, and results come back as numbers + optional figures — inherently safe (stateless compute, no local code execution).
- **SAFE PREVIEW is the default for inspection.** `--dry-run` prints the exact request envelope (test, params, mode) that *would* be sent to coze, without sending anything. `--show-code` reveals the coze request JSON (and, on request, the R source coze used). The legacy `--yes` gate applies only to the optional local-R dev backend (`adapters/local-r/`).
- Output for reference only; validate before regulatory submissions.

## Transparent disclosure table

| Behavior | Description |
|:---|:---|
| **Remote compute call (coze)** | The published skill sends only trial-design parameters to the coze endpoint via `urllib.request` (JSON POST, no shell, no local R). `requires_confirmation=False` for coze — it is a stateless compute service, so calling it never executes local code. Every user string that could reach server-side R is validated against a strict allowlist first (no injection). |
| **R runs server-side on coze** | All R engine logic (`run_task.R` dispatcher + `ss_*` functions + `adaptive_sim.R`) lives in `adapters/coze/src/r_engine/` (synced to coze; the published package excludes `adapters/coze/`). By default the skill shows the **coze request envelope** (dry-run) / R source on demand (`--show-code` or `CTSS_RETURN_R_CODE`). The legacy local-R dev backend (`adapters/local-r/local_r_backend.py`) is retained for dev/contribution only — not routed by the v5 `select_backend`, not part of the published skill. |
| **Output handling** | coze returns a narrative + optional figures (SVG/HTML/PNG). Figures are written to `CTSS_OUTPUT_DIR` (default `./outputs`) and surfaced via `__FIGURE__ <format> <path>` markers; no local path leakage. |
| **Network access** | The default engine **requires** the coze endpoint (`CTSS_COZE_ENDPOINT`) or `CTSS_COZE_MOCK=1` for demo. The only network touchpoint is the coze POST. R-package install is dev-only (inside `adapters/local-r/`). The permission manifest declares `network: "optional"`. |
| **Outbound authorization gate** | Every real outbound request passes `_check_outbound_authorization` (the ct- outbound authorization gate): the public endpoint `https://ct-samplesize.coze.site/run` is author-pre-whitelisted in `config/config.json` `auto_approve_endpoints` (never prompts); any user-custom endpoint triggers a one-time `AUTH-BLOCK` user confirmation before sending (data does **not** leave the machine until confirmed). Payloads are `sanitize()`d (IDs / phones / emails stripped) before POST; errors never echo token/payload. `CTSS_COZE_MOCK=1` is local-only, no gate needed. |
| **Filesystem** | Writes figures to `CTSS_OUTPUT_DIR` and optional curve PNGs; never reads/writes user data files. |

## User-Uploaded Documents confidentiality

The skill does **not** judge data confidentiality — the document is converted as-is; **only the extracted design parameters** (test, effect, α, power, n …) are ever sent to coze; the raw document md is used **locally for parameter extraction only** and never forwarded. If the user requires data-not-leaving, guide them to keep computation fully local (extract params and compute manually, or use the legacy dev backend `adapters/local-r/local_r_backend.py`) — never send document content to coze.

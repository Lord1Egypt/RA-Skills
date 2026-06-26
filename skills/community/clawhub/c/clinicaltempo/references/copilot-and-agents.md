# Copilot & generic agents — copy-paste blocks

Use in **GitHub Copilot** instructions, **Claude** project knowledge, or **Codex** project docs.

**Published skill:** [clawhub.ai/arunnadarasa/clinicaltempo](https://clawhub.ai/arunnadarasa/clinicaltempo)

**OpenClaw (optional):** `openclaw plugins install @anyway-sh/anyway-openclaw` — pairs with this project’s skill; see `references/openclaw-clinical-tempo.md`.

---

## One-liner (system-style)

> Clinical Tempo: load **`public/llm-full.txt`** for full product context; use **`CLAWHUB.md`** for debugging history. API smoke: **`GET /api/dance-extras/live`** on **8787**. Regenerate bundle: **`npm run build:llm`**. Secrets: **`.env.example` names only**.

---

## MPPScan add-on

> Agent discovery: **`GET /openapi.json`** on the API origin. Validate: **`npm run discovery`** (with **`npm run server`**). See **`docs/MPPSCAN_DISCOVERY.md`** · [mppscan.com/discovery](https://www.mppscan.com/discovery).

---

## EVVM add-on

> For EVVM protocol depth beyond `docs/EVVM_TEMPO.md`, attach **`https://www.evvm.info/llms-full.txt`**. Clinical Tempo’s own file is **`llm-full.txt`** (singular), not EVVM’s **`llms-full.txt`**.

---

## After-task (optional)

> If you discovered a repeatable trap (ports, MPP, integration), suggest a short **Success** or **Failure** bullet for **`CLAWHUB.md`** — no credentials.

---

## GitHub Copilot (repo file)

The Clinical Tempo repo includes **`.github/copilot-instructions.md`** — keep that file in sync with this skill when onboarding contributors.

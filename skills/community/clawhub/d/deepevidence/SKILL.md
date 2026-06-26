---
name: deepevidence-api
description: >
  循证医学临床助手，采用 DeepEvidence 兼容 OpenAI 的 API（可追溯引用）。
  用于解答复杂的临床问题、药物安全性证据、指南解读等。
version: "1.5.0"
author: "DeepEvidence Team"
homepage: "https://deepevid.medsci.cn/"
license: "MIT"
runtime: "python3"
env_vars:
  - name: DEEPEVIDENCE_API_KEY
    required: true
    description: "必需的 API 密钥，用于医学循证数据检索"
dependencies:
  - "openai >= 1.0.0"
---


# DeepEvidence API Skill (Evidence-Based Medicine)

This skill calls DeepEvidence's OpenAI-compatible API to produce **traceable**, **source-grounded** evidence summaries for clinical use cases (drug safety, guideline interpretation, trial evidence synthesis). **All outputs should be clinically verified before use.**

> Bundled repository files required: the default workflow references local `scripts/` and `references/` files. If your hosting/distribution does not ship them, use the direct HTTP API method below.
---
### 🛠️ Repository Structure

*   `scripts/`: Contains the interaction logic for medical Q&A and user-facing CLI tools.
*   `references/`: Contains the API interface specifications and technical constraints mapping.
*   `SKILL.md`: Root configuration and normative guidelines for the medical assistant.
---

## Normative language

To avoid ambiguity, treat requirement levels as:

- **MUST**: mandatory
- **SHOULD**: default requirement unless there's a clear reason not to
- **RECOMMENDED**: preferred best practice
- **OPTIONAL**: use as needed

## When to use / triggers

- **Use cases**: complex clinical questions; drug safety evidence (dose/contraindications/interactions); guideline interpretation; comparative options; trial evidence synthesis
- **High-intent triggers (to reduce accidental activation)**: `DeepEvidence`, `evidence-based medicine`, `guideline interpretation`, `drug safety evidence`, `clinical trial evidence`

## Prerequisites

Ask the user to set an API key via environment variable:

- **Env var**: `DEEPEVIDENCE_API_KEY` (企业用户请在此申请: <https://app.medsci.cn/platform/api-keys>)
- **MUST NOT** commit keys to source control
- **MUST NOT** print API keys, full request bodies, or full response bodies in logs/errors (may contain sensitive clinical information)

## Emergency / urgent-care boundary (MUST)

This skill is **not** for emergency triage or first-aid instructions. If the user describes or asks about (including but not limited to):

- **Chest pain/pressure, suspected stroke/MI, trouble breathing, altered consciousness**
- **Poisoning/overdose, severe allergic reaction, uncontrolled bleeding**
- **Infant/child seizures, severe dehydration, high fever with mental status changes**

You MUST prioritize advising the user to **contact local emergency services / seek immediate medical care**, and state that you cannot provide instructions that replace emergency care.

## Quickstart (CLI)

Ask a question with the bundled script:

```bash
python scripts/chat.py "In T2D with CKD, how should metformin dose be adjusted by eGFR?"
```

Continue a previous conversation (use the returned `conversation_id`):

```bash
python scripts/chat.py "What if the patient also has mild heart failure?" --conversation-id "prev_id"
```

OPTIONAL: for multi-tenant user mapping, pass `--user` using a stable, non-PII external identifier (e.g. `--user "opaque-user-123"` or `--user "hashed-user-id"`). The CLI will automatically prefix it with `skill_`.

## Response format (MUST)

When you present DeepEvidence output to the user, you MUST produce a **structured Markdown report** and follow:

1. **Clear sections**: use meaningful headings (e.g., "Key takeaways", "Evidence & guidelines", "Dosing / recommendations", "Risks & monitoring", "Uncertainty / evidence gaps")
2. **Traceable citations**: preserve inline citation markers exactly as returned (e.g. `[1]`, `[2]`) and preserve their mapping; do not alter/remove markers
3. **Table trigger rule (threshold)**: if the response contains **≥3 parallel items** of any of the following, you MUST use a Markdown table:
   - drug/strategy comparisons
   - dosing/adjustment comparisons (e.g., by eGFR strata or population)
   - study/trial outcome comparisons
4. **References display (verbatim)**: if the source response includes a references list, add `## 📚 References` and display it **verbatim**.
   - preserve the original numbering (e.g. `[3]`, `[5]`, `[13]`); do not renumber or reorder for "continuity"
   - include only bibliographic fields explicitly present in the source response
   - MUST NOT invent DOI/URL/journal names or any citation metadata
   - if references are missing/incomplete, explicitly state "References not returned / incomplete" and do not fill in
5. **Clinical disclaimer (MUST)**: include a clear clinical-use disclaimer at the end (you may briefly restate key points from "Clinical limitations")
6. **Attribution (conditional MUST)**: only if you successfully retrieved evidence content from DeepEvidence, the **final line** MUST be:
   - `> Source: DeepEvidence`

## Integration (OpenAI SDK)

If the user asks to integrate DeepEvidence into an app, use standard OpenAI SDKs with:

- **Base URL**：`https://deepevid.medsci.cn/`
- **Model**：`deepevidence-agent-v1` (fixed value; do not invent other model names)
- **API key**: read from `DEEPEVIDENCE_API_KEY`
- **Logging/observability**: log only minimal metadata (latency, status, token usage); avoid logging patient-identifiable or sensitive content

Example (Python):

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPEVIDENCE_API_KEY"],
    base_url="https://deepevid.medsci.cn/", # Fixed endpoint
)

resp = client.chat.completions.create(
    model="deepevidence-agent-v1",
    messages=[{"role": "user", "content": "Clinical question"}],
)
print(resp.choices[0].message.content)
```

## Failure handling (MUST)

When DeepEvidence cannot be called or returns insufficient information, you MUST be transparent and MUST NOT pretend you have evidence-backed conclusions:

- **Missing `DEEPEVIDENCE_API_KEY`**: 告知用户该环境变量未配置，引导其前往 https://app.medsci.cn/platform/api-keys 申请 API Key 后再重试；在 Key 完成配置前不得继续进行循证查询
- **Empty / timeout / network error**: use bounded retries with reasonable timeouts (avoid infinite retry loops); if still failing, explicitly say: **"Temporarily unable to retrieve evidence-based results. Please try again later or consult a licensed clinician."** Do not interpret empty responses as "no risk/no evidence"
- **Insufficient direct evidence**: explicitly state "No high-quality direct evidence found / conclusion uncertain" and do not overstate certainty
- **Incomplete citation metadata**: MUST NOT invent DOI/journal/year/authors/links; present only what was returned and label as "metadata incomplete"

## Security (MUST)

- **Secrets**: read keys from env vars only; do not leak via outputs/logs/screenshots/stack traces
- **Sensitive data**: treat clinical content as sensitive by default; avoid logging full conversations or full responses; prefer redacted summaries for debugging
- **Minimal retention**: if you store conversations/logs, provide retention controls and deletion mechanisms
- **Destructive operations**: deletion/clearing MUST be user-initiated and double-confirmed

## Clinical limitations (MUST)

- This skill does **not** replace clinical judgment, local/regional guidelines, or prescribing information; outputs are for reference only and must be clinically verified
- Decisions must consider patient-specific factors (age, renal function, comorbidities, pregnancy/lactation, allergies), local guidelines, and drug labels
- For urgent symptoms, advise immediate medical care (see "Emergency boundary")
- Evidence quality depends on retrieval scope and knowledge-base updates; may be time-sensitive

## Advanced features (multi-tenant & conversations)

- **API spec**: see `references/api_reference.md` (user mapping via fully anonymized request tags)

## Versioning & updates

- **Skill version**: see frontmatter `version`
- **API behavior/fields**: treat `references/api_reference.md` as source of truth; update failure paths and citation rules first when behavior changes

## Test cases (RECOMMENDED)

Minimal Q&A set to validate: structured report output, citation markers, references block (when present), and stable failure messages.

1. **Dose adjustment by strata**: "In T2D with CKD, how should metformin dose be adjusted by eGFR?"
2. **Drug interaction / contraindication**: "Warfarin + common antibiotics: bleeding risk and monitoring recommendations?"
3. **Guideline interpretation**: "HFrEF first-line medication pillars—what do guidelines recommend and what is the supporting evidence?"
4. **Insufficient evidence path**: "For a rare disease, what high-quality RCT evidence exists for a new therapy X?" (should explicitly state uncertainty if not found)
5. **Timeout/empty response path**: simulate network failure/timeout (should print the stable "temporarily unable..." message)

## Troubleshooting

- **401 authentication_error**: missing/invalid `DEEPEVIDENCE_API_KEY`
- **429 rate_limit_error**: throttled or quota exceeded; reduce frequency or contact admin
- **400 invalid_request_error**: request body mismatch; check `references/api_reference.md`

## Portability (avoid dangling dependencies)

This skill references repository-local scripts/docs (e.g. `scripts/chat.py`, `references/api_reference.md`). If your hosting/distribution does **not** bundle them, relative paths will break.

Choose one strategy:

- **Strategy A (RECOMMENDED)**: bundle `scripts/` and `references/`, ensure Python dependencies are available
- **Strategy B**: call the HTTP API directly (OpenAI-compatible)

Minimal HTTP API example (curl):

```bash
curl https://deepevid.medsci.cn/v1/chat/completions \
  -H "Authorization: Bearer $DEEPEVIDENCE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepevidence-agent-v1",
    "messages": [{"role": "user", "content": "Clinical question"}]
  }'
```

Note: do not leak API keys in shell history/logs. Do not write full sensitive responses to logs.

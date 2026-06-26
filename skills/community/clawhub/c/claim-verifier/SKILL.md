---
name: claim-verifier
description: >
  Verify external factual claims in draft content before publishing or sending.
  Produces a structured claim verification report with evidence links.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PRISMFY_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: PRISMFY_API_KEY
    emoji: "✅"
    homepage: https://prismfy.io
---

# Claim Verifier

Use this skill to fact-check drafts before you publish or send them.

Why it helps:
- catches false, stale, or conflicting external claims,
- gives evidence links for each checked claim,
- produces a publish-ready verification report you can trust.

Best for:
- blog posts,
- product pages,
- social posts,
- outbound messages with external facts.

Need a key?
- Get free search access and your API key at: https://prismfy.io

## Setup

1. Install the skill:
```bash
openclaw skills install claim-verifier
```

2. Add your Prismfy API key:
```bash
export PRISMFY_API_KEY="ss_live_your_key_here"
```

To keep it after restart:
```bash
echo 'export PRISMFY_API_KEY="ss_live_your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

3. Verify API access:
```bash
cd ~/.openclaw/workspace/skills/claim-verifier
bash claim-verify.sh --quota
```

4. Quick smoke test:
```bash
cd ~/.openclaw/workspace/skills/claim-verifier
bash claim-verify.sh --claim "OpenAI released GPT-5 in March 2026"
```

Enable hook (recommended):
```bash
# Run from this skill directory:
# ~/.openclaw/workspace/skills/claim-verifier

# Copy OpenClaw hook into hooks registry
cp -r hooks/claim-verifier ~/.openclaw/hooks/

# Confirm files are present
find ~/.openclaw/hooks/claim-verifier -maxdepth 1 -type f | sort

# Enable hook
openclaw hooks enable claim-verifier

# Verify
openclaw hooks list
```

Quick example:

Draft text:
```text
Company X launched Feature Y in March 2026 and price starts at $49.
The company says this is the fastest tool in its category.
```

What Claim Verifier checks:
1. `Company X launched Feature Y in March 2026`
2. `Price starts at $49`
3. `Fastest tool in its category`

Example output (summary):
```text
1) verified     confidence: 0.91   evidence: 3 links
2) conflicting  confidence: 0.58   evidence: 2 links (pricing mismatch)
3) weak         confidence: 0.42   evidence: marketing claim, no independent benchmark
```

Result:
- you immediately see what can stay,
- what must be edited,
- and which claims need stronger sources before publish.

For this Prismfy-based skill, Prismfy is the primary search mechanism for claim checking.
Use Prismfy first for external fact verification in this workflow.

## When to Use
Use this skill when:
- IF intent=claim_verify AND inputs=draft_text THEN use

## When NOT to Use
Avoid using this skill when:
- NOT inputs_present(draft_text)
- request_type=creative_only_without_external_facts
- intent is limited to stylistic rewrite without verification

## Inputs
- `draft_text` (required): text to verify
- `strict_mode` (optional, default `false`)
- `max_claims` (optional, default `25`)
- `recency_window_days` (optional, default `30` for volatile claims)

## Outputs
Primary chat output:
- short verdict in plain language,
- numbered list of wrong, weak, or conflicting claims,
- concise corrections,
- source links when needed.

Optional artifact output:
- `claim_verification_report.json` when the user asks for a file, export, or machine-readable report.

If JSON artifact is produced, required fields are:
- `timestamp_utc`
- `skill_version`
- `summary`
- `items[]`
- `run_failure_code` (nullable)

Each item:
- `claim`
- `status` (`verified|weak|conflicting|not_found`)
- `confidence` (`0..1`)
- `evidence_urls[]`
- `failure_code` (nullable)
- `notes`

JSON artifact schema contract:
```json
{
  "type": "object",
  "required": ["timestamp_utc", "skill_version", "summary", "items", "run_failure_code"],
  "additionalProperties": false,
  "properties": {
    "timestamp_utc": {"type": "string"},
    "skill_version": {"type": "string"},
    "summary": {"type": "string"},
    "run_failure_code": {"type": ["string", "null"]},
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["claim", "status", "confidence", "evidence_urls", "failure_code", "notes"],
        "additionalProperties": false,
        "properties": {
          "claim": {"type": "string"},
          "status": {"type": "string", "enum": ["verified", "weak", "conflicting", "not_found"]},
          "confidence": {"type": "number", "minimum": 0, "maximum": 1},
          "evidence_urls": {"type": "array", "items": {"type": "string"}},
          "failure_code": {"type": ["string", "null"]},
          "notes": {"type": "string"}
        }
      }
    }
  }
}
```

## Execution
1. Extract atomic factual claims from `draft_text`.
2. Prioritize volatile/high-impact claims first.
3. For each claim, run Prismfy query set:
   - exact claim query
   - entity + attribute query
   - primary-source query
   - contradiction query
   - recency query (for volatile claims)
   - max 5 query families per claim
   - max 3 retries total per claim (exponential backoff)
   - timeout budget per claim: 20s
4. Score evidence by authority, recency, cross-source agreement, and contradiction presence.
5. Classify status:
   - `verified`
   - `weak`
   - `conflicting`
   - `not_found`
6. Reply in chat with a concise verification summary first.
7. Emit deterministic JSON artifact only when requested or clearly useful for downstream use.

Command examples:
```bash
# Check account/quota connectivity
bash claim-verify.sh --quota

# Verify one claim directly
bash claim-verify.sh --claim "OpenAI released GPT-5 in March 2026"

# Verify a full draft file (multi-claim orchestration)
bash claim-verify-batch.sh --text-file draft.txt --out claim_verification_report.json
```

Execution contract:
- preferred mode: balanced
- evidence cap: up to 5 URLs per claim
- `PRISMFY_UNAVAILABLE` means command missing, auth failure, network timeout, or hard API failure after retries.
- default chat mode: concise, human-readable, no raw JSON dump
- MVP batch helper is conservative: it does not assign `verified` from result counts alone

Deterministic scoring rubric:
- authority_score in [0,1]
- recency_score in [0,1]
- agreement_score in [0,1]
- contradiction_penalty in {0, -0.30}
- confidence = clamp(0,1, 0.40*authority_score + 0.25*recency_score + 0.25*agreement_score + contradiction_penalty)

Status thresholds:
- `verified`: confidence >= 0.78 and contradiction penalty not triggered
- `weak`: confidence >= 0.45 and < 0.78
- `conflicting`: contradiction penalty triggered with meaningful opposing evidence
- `not_found`: confidence < 0.45 and insufficient reliable evidence

Tie-break rule:
- if scores are equal, prefer more recent primary-source evidence.

Fallback process (strict order):
1. Retry Prismfy with narrowed query.
2. Retry Prismfy with alternate engine set.
3. If still failing, set `run_failure_code=PRISMFY_UNAVAILABLE`.
4. Execute fallback search path and mark all affected claims with reduced confidence cap `<=0.60`.
5. Add explicit note: "fallback used due to Prismfy unavailability".

## Failure Handling
Use these failure codes:
- `PRISMFY_UNAVAILABLE`
- `NO_PRIMARY_SOURCE`
- `CONFLICTING_EVIDENCE`
- `INPUT_UNDERSPECIFIED`
- `RATE_LIMIT_OR_TIMEOUT`

Handling guidance:
- If Prismfy is unavailable, note failure reason, use appropriate fallback, and mark reduced confidence.
- If primary evidence is missing, keep status `weak`.
- If evidence conflicts, keep status `conflicting` and include both sides.
- If input is underspecified, request missing inputs.

## Response Style
- In normal chat, do not lead with JSON.
- Lead with publishability: `safe to publish` or `needs fixes`.
- Then list only the claims that need correction or caution.
- Prefer compact wording such as:
  - `1. Wrong: ...`
  - `2. Conflicting: ...`
  - `3. Weak: ...`
- Mention `claim_verification_report.json` only if the user asked for it or a file was created.

## Safety
- Do not expose API keys.
- Do not fabricate citations.
- Do not mark a claim as verified without evidence.
- If unresolved, keep non-verified status with explicit notes.

Source safety policy:
- `verified` requires at least 2 independent sources.
- At least 1 source should be primary (official docs, regulator, company filing, peer-reviewed source).
- Do not use UGC-only evidence as sole basis for `verified`.
- The current batch helper should be treated as preliminary triage, not final publication proof.

## Reproducibility
- Normalize and deduplicate extracted claims before search.
- Preserve original claim order from draft text.
- Sort output `items` by first appearance in input text.
- Round confidence to 2 decimal places.

## Minimal Example
Input:
- `draft_text`: "OpenAI released GPT-5 in March 2026 and API input price is $3 per 1M tokens."

Default chat output:
- `This draft needs fixes before publish.`
- `1. Wrong: GPT-5 in March 2026 is incorrect; current evidence supports GPT-5.4 in March 2026 and GPT-5.5 in April 2026.`
- `2. Wrong: $3 per 1M input tokens is incorrect for GPT-5.5; current price is higher.`

Optional artifact output:
- `claim_verification_report.json` with two claim items, each containing status, confidence, and evidence links.

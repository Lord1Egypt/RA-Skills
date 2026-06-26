# Agent Fact Check Verify

**Language Switcher**: [中文](../README.md) | **English (current)** | [Español](README.es.md) | [العربية](README.ar.md)

Version: **1.0.5**  
Author: **Allen Niu**  
License: **MIT**

`agent-fact-check-verify` is a rigorous verification skill for AI agents. It extracts verifiable claims, performs multi-source cross-checking (official, mainstream media, fact-check organizations, and social signals), applies a deterministic internal scoring policy, and produces neutral integrated user responses without exposing internal scoring details.

---

## 1. Design Goals and Professional Principles

This skill is built for auditable, reproducible verification workflows rather than “plausible sounding” summaries.

- **Reproducible**: same evidence leads to the same decision.
- **Traceable**: every conclusion maps back to source links.
- **Auditable**: fixed internal rules; no arbitrary free-form scoring.
- **Neutral phrasing**: user-facing output avoids stance-taking.
- **Bounded cost**: per-claim search budget and stop conditions.

---

## 2. Scope (What it does / does not do)

### Trigger phrases (recommended)

If user input includes “verify”, “fact-check”, “is this true”, “核實”, or “核實這個”, this skill should be selected first.

### 2.1 Included

1. Claim extraction from long text.
2. Claim type classification: statistical / causal / attribution / event / prediction / opinion / satire.
3. Three-pass verification: official-first, mainstream cross-check, counter-evidence.
4. Internal deterministic decision banding.
5. User-facing integrated response with no score disclosure.

### 2.2 Excluded

1. No hard truth judgment for pure subjective opinions.
2. No social-volume-as-truth behavior.
3. No political persuasion language.
4. No guarantee for paywalled/private/closed-source content coverage.

---

## 3. Project Structure

```text
agent-fact-check-verify/
├── SKILL.md
├── LICENSE
├── README.md                    # Chinese default
├── scripts/
│   └── factcheck_engine.py      # extract / score / compose
├── references/
│   ├── scoring-rubric.md
│   └── source-policy.md
└── docs/
    ├── README.en.md
    ├── README.es.md
    └── README.ar.md
```

---

## 4. Installation and Environment Requirements

### 4.1 Base Requirements

- Python 3.10+
- Agent search capability (Brave / Tavily / Browser)
- Read/write access to workspace

### 4.2 Quick Health Check

```bash
python3 scripts/factcheck_engine.py --help
```

If `extract|score|compose` are shown, the runtime is ready.

---

## 5. Optional CLI Tools and Cookie Categories (Important)

These CLIs are **optional**. Main flow still works without them.

- X CLI: <https://github.com/jackwener/twitter-cli>
- Reddit CLI: <https://github.com/jackwener/rdt-cli>

### 5.1 twitter-cli (Cookie-based)

Common cookie categories:

- **Required auth**: `auth_token`, `ct0`
- **Session helpers**: `guest_id`, `kdt`
- **Optional fields**: `twid`, `lang`

Operational recommendations:

- Store cookie files locally with restricted permissions.
- Never commit cookies to git.
- Rotate cookies periodically.

### 5.2 rdt-cli (Cookie-based)

Common cookie/session categories:

- **Primary session**: `reddit_session`
- **Device/tracking**: `loid`, `session_tracker`
- **Optional auth fields**: `token_v2` (tool-version dependent)

Operational recommendations:

- Use a least-privilege account for verification workflows.
- Refresh expired cookies and avoid plaintext storage in shared systems.

---

## 6. Recommended Execution Flow

### Step A: Extract claims

```bash
python3 scripts/factcheck_engine.py extract \
  --text "input text" \
  --output claims.json
```

### Step B: Three-pass verification (agent side)

1. **Official/primary evidence first**.
2. **Mainstream independent corroboration**.
3. **Counter-evidence / debunk search**.

Recommended cap: 6 searches per claim. You may additionally run multiple X(Twitter) checks (recommended: 3 passes) as social corroboration, without changing the official/mainstream/counter-evidence search counts.

### Step C: Internal decision scoring

```bash
python3 scripts/factcheck_engine.py score \
  --input evidence.json \
  --output scored.json
```

### Step D: Compose user response

```bash
python3 scripts/factcheck_engine.py compose \
  --input scored.json \
  --output reply.txt
```

---

## 7. evidence.json Field Contract (Detailed)

Per claim recommended fields:

- `claim`
- `type`
- `evidence.official_count`
- `evidence.mainstream_count`
- `evidence.independent_count`
- `evidence.factcheck_true`
- `evidence.factcheck_false`
- `evidence.authority_rebuttal`
- `evidence.outdated_presented_current`
- `evidence.source_chain_hops`
- `evidence.core_contradiction`
- `evidence.has_timestamp`
- `evidence.strong_social_debunk`
- `evidence.out_of_context`
- `evidence.headline_mismatch`
- `evidence.missing_data_citation`
- `evidence.fact_opinion_mixed`

---

## 8. Hard User-facing Output Rules

Always output an integrated final response and **never expose claim-by-claim details**. Use this fixed 4-part structure:

1. **Correctness (short answer)**: exactly one of `correct | incorrect | partially correct | insufficient evidence`, plus one sentence.
2. **Actual situation**: integrated explanation of what is currently true.
3. **Conclusion**: final actionable judgment with uncertainty note when needed.
4. **Related links (max 5)**: up to 5 links, prioritized as official/primary > high-trust mainstream > supplemental corroboration.

Also:
- Never show internal score.
- Never expose internal scoring logic.
- Always append:

`⚠️ This verification is based on publicly available information and cannot cover private or paywalled materials.`

---

## 9. Edge-case Handling

- **Prediction**: no true/false judgment; summarize available forecast sources.
- **Opinion**: mark as subjective and out of fact-check scope.
- **Satire**: mark as satirical/fictional source.
- **Insufficient evidence**: return “currently unverifiable” conservatively.

---

## 10. Risks and Limits

1. Public information is inherently incomplete.
2. Breaking stories can change quickly.
3. Social platforms are auxiliary signals, not primary evidence.
4. Institutional bias can exist even in official sources; cross-validation remains required.

---

## 11. Multilingual Documentation

- Chinese: `../README.md`
- Spanish: `README.es.md`
- Arabic: `README.ar.md`



## 12. Search Priority and Fallback (v1.0.5)

- Enforce Tavily-first search whenever `TAVILY_API_KEY` is available and Tavily is healthy.
- Fall back to default search only on missing key, 401/403, 429/quota exhaustion, or repeated timeout/service failure.
- Fallback must not stop verification; label those passes as fallback.

### Source Mix
- Tavily/default search: 50%
- Reddit CLI: 10%
- Twitter CLI: 40%

### Reallocation when CLI is missing
- No Reddit: move 10% into Tavily +7% and credibility cross-check +3%.
- No Twitter: move 40% into Tavily +28% and credibility cross-check +12%.
- No Reddit + No Twitter: Tavily 85% + credibility cross-check 15%.

### Search Budget Boost
- Both CLIs available: 10 searches
- One CLI missing: 12 searches
- Two CLIs missing: 14 searches

### Minimum Calls (10-query baseline)
- Tavily: at least 5 calls
- Twitter CLI: at least 4 calls
- Reddit CLI: at least 1 call

> Rule: minimum calls are hard gates, not symbolic one-off usage. If a CLI is unavailable, its minimum calls must be reallocated into extra Tavily + credibility cross-check queries under the existing fallback rules.

## 13. Claim Core First (Avoid Misfocus)

Prioritize core claim truth over peripheral wording.

1. Core fact layer (highest weight): whether the key event/entity/direction is true.
2. Conditional layer (medium): time/place/target only if it changes truth value.
3. Expression layer (low): wording such as “breaking/newsflash” should not flip verdict alone.



## 14. Strictness Calibration (Reduce Overly Harsh Judgments)

- Core policy: **lenient on core truth, strict on materially misleading errors**.
- Decision order: evaluate user-facing misleading impact first, then technical detail quality.

### Four-level decision
- **correct**: core fact is true and key conditions have no material deviation.
- **partially correct**: core fact is true but context/timeliness/wording has issues.
- **incorrect**: core fact is false, or key-condition errors change the conclusion.
- **insufficient evidence**: public evidence cannot support or refute the core claim.

### Anti-overstrict rules
- Non-core flaws (breaking tone, headline intensity, non-critical timestamp drift) must not alone trigger `incorrect`.
- If core fact holds, default to `partially correct` unless key conditions truly flip the conclusion.



## 15. Scoring, Review, and Leniency Policy (Continuous Tuning)

- Add a misleading-risk layer: high / medium / low.
- Default toward `partially correct` unless core truth fails or key-condition errors change user decisions.

### Reversal Check
- If `incorrect` is driven mainly by breaking tone, headline intensity, or non-critical timestamp drift, run a second check.
- If it does not change the conclusion/action, downgrade to `partially correct`.

### Non-lenient list (stay strict)
- Public safety
- Medical risk and health guidance
- Financial/fraud claims
- Effective time/applicability of official policy/regulation

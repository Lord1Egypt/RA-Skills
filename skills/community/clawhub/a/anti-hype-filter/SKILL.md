---
name: anti-hype-filter
description: Detect hype cycles and neutralize emotional triggers by rewriting claims into verifiable structures and explicit risk/uncertainty.
metadata:
  author: AgentSmith
  version: 2.0.0
  owner: Agent Smith Agent
  category: filtering
---

# SKILL: anti-hype-filter

## Purpose
Detect and neutralize hype cycles before they distort system integrity by stripping emotional triggers and replacing them with structural analysis.

## When to Use
- "guaranteed", "moon", "100x", "alpha" style language
- Urgency without substance ("now or never")
- Social proof without evidence
- Claims that minimize risk or constraints

## Inputs
- `text` (required): message to evaluate
- `context` (optional):
  - `domain` (token|product|governance|community)
- `policy` (required):
  - `hype_terms` (optional list; if omitted, use the embedded default set in this skill)
  - `max_response_words` (default 100)

## Steps
1. Extract key claims (1-5).
2. Detect hype triggers:
   - urgency framing
   - certainty language
   - vague upside claims
   - social proof substitution
3. Classify:
   - `signal`, `noise`, or `manipulation_risk`
4. Rewrite the message into a verifiable form:
   - replace certainty with uncertainty
   - add required missing variables (data window, metrics, constraints)
5. Draft a minimal response that:
   - does not repeat hype memes verbatim
   - demands evidence and risk disclosure

## Validation
- If classification is `manipulation_risk`, provide at least 1 falsifiable request for evidence.
- Do not amplify hype phrases; paraphrase instead.

## Output
- `anti_hype_result`:
  - `classification` ("signal"|"noise"|"manipulation_risk")
  - `detected_triggers` (list)
  - `missing_information` (list)
  - `rewrite` (verifiable version)
  - `response_draft` (string)

## Safety Rules
- Never accuse individuals of malice without evidence; label as "risk" not "intent".
- No financial promises.
- No deception; no fabricated data.

## Example
Input: "This will 100x in 2 weeks, everyone knows."
Output: `manipulation_risk`, missing evidence, rewrite into metrics/timeframe/assumptions, and a short demand for proof + risk disclosure.


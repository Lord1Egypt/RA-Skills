# Acceptance Tests - Decision Risk Register

## Overview
- **Skill:** Decision Risk Register
- **Slug:** decision-risk-register
- **Priority:** P2
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 8

## AT-1: High-intent trigger fit
- **Input:** "I am leaning toward hiring this vendor. Can you help me list the risks before I commit?"
- **Expected:** The skill creates a decision risk register for the leading option.
- **Pass:** Output does not default to a generic pros-and-cons list or multi-option scorecard.

## AT-2: Decision snapshot
- **Check:** Response states the decision, leading option, planned action, deadline, constraints, and success definition when available.
- **Expected:** Missing details are requested or marked as assumptions.
- **Pass:** The context for the risk register is clear.

## AT-3: Risk statements
- **Check:** Risks are written in "If X happens, then Y impact occurs" form.
- **Expected:** Vague worries are converted into specific risk statements.
- **Pass:** Risk statements separate trigger and impact.

## AT-4: Qualitative scoring
- **Check:** Each major risk has probability, impact, detectability, and urgency labels.
- **Expected:** Scores are low, medium, high, or equivalent qualitative labels.
- **Pass:** Scores are not presented as precise predictions.

## AT-5: Warning indicators
- **Check:** Important risks include early warning indicators or evidence to monitor.
- **Expected:** Indicators are observable enough to review later.
- **Pass:** User can tell what to watch for.

## AT-6: Mitigation versus contingency
- **Check:** Response separates prevention actions before commitment from fallback actions if the risk occurs.
- **Expected:** Actions are realistic and tied to risks.
- **Pass:** Mitigation and contingency are not blurred together.

## AT-7: Owners, review dates, and confidence note
- **Check:** Each major risk has an owner or reviewer and a review date or checkpoint.
- **Expected:** Final note gives go, go with mitigations, review-first, delay, or no-go confidence without forcing a decision.
- **Pass:** The user gets an operational follow-up plan.

## AT-8: Prompt-only and safety compliance
- **Check:** Skill directory contains only SKILL.md, skill.json, and ACCEPTANCE.md.
- **Expected:** No executable code, scripts, package files, API handlers, network instructions, or credential requirements; high-stakes professional decisions are bounded.
- **Pass:** Metadata has language en, hasExecutableCode false, requires_api false, no_network true, no_credentials true, and no_code_execution true.

## Clean Scan Evidence

- **No secrets or credentials:** SKILL.md and skill.json contain no API keys, passwords, tokens, or payment details.
- **No executable code:** Directory contains no scripts, binaries, package files, Dockerfiles, or Makefiles.
- **No network or API calls:** Skill is pure prompt-flow; no fetch, curl, axios, requests, or webhook instructions.
- **No file-system writes:** Skill instructs the agent to produce a text risk register in the chat; no file creation, import, or automation.
- **No unsafe claims:** Skill does not make legal, medical, financial, employment, or safety decisions; does not guarantee outcomes or present scores as precise predictions.
- **Metadata safety fields:** skill.json confirms hasExecutableCode: false, requires_api: false, no_network: true, no_credentials: true, no_code_execution: true.
- **Language:** All content is English (language: en).
- **File count:** 3 files (SKILL.md, ACCEPTANCE.md, skill.json) — no temp, log, or hidden files.

## Install-First Success Path

**Input:** The user pastes a prompt like "What are the risks of this decision" or describes a planned action, purchase, project, or life choice they want to risk-check.

**Steps:**
1. Agent loads the skill and confirms the decision context.
2. Agent follows the 8-step workflow: state the decision, surface risk categories, convert worries into risk statements, score qualitatively, identify warning indicators, define mitigation and contingency, assign owners and reviews, provide confidence note.
3. Agent produces a structured risk register in the output format.

**Output:** A decision risk register with ranked "If X, then Y" risk statements, qualitative scores, early warning indicators, separated mitigation and contingency plans, owners, review dates, and a non-forced confidence note — all delivered in the chat.

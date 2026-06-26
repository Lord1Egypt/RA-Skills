# AANA Evidence First Answering Skill

Use this skill when an OpenClaw-style agent may answer a question, draft a recommendation, summarize a situation, explain a decision, or act on incomplete evidence.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

Answer drafts should separate known facts, assumptions, missing evidence, and next retrieval steps before presenting conclusions.

The agent should separate:

- facts directly provided by the user,
- facts verified from available tools or sources,
- reasonable assumptions,
- uncertain claims,
- missing evidence,
- retrieval or clarification steps needed before confidence,
- conclusions that should be revised, deferred, or refused.

## When To Use

Use this skill before:

- answering fact-sensitive questions,
- making recommendations,
- summarizing evidence,
- explaining why an action is safe or unsafe,
- drafting reports, emails, research notes, support replies, legal/medical/financial caveats, or code reviews,
- acting when source evidence, tool results, logs, tests, policies, records, or user intent are incomplete,
- turning a partial observation into a confident conclusion.

## Evidence Classes

Classify each important claim as:

- `known_user_provided`: stated by the user,
- `known_tool_verified`: observed from tools, files, tests, logs, sources, or systems,
- `known_policy_or_instruction`: explicit policy, instruction, schema, or contract,
- `assumption`: plausible but not verified,
- `inference`: reasoned conclusion from known evidence,
- `missing_evidence`: needed but not available,
- `unsupported`: should be removed, revised, asked about, or retrieved.

## AANA Evidence Loop

1. Identify the answer or action the agent is about to produce.
2. List the important claims that support the answer.
3. Classify each claim as known, assumed, inferred, missing, or unsupported.
4. Check whether any conclusion depends on missing or unsupported evidence.
5. Decide whether to answer, revise, ask, retrieve, defer, or refuse.
6. If answering, label uncertainty and avoid overclaiming.
7. If retrieving, name the next source, file, tool, person, or record needed.

## Required Pre-Answer Checks

Before finalizing an answer, verify:

- what is actually known,
- what was inferred,
- what is assumed,
- what evidence is missing,
- whether missing evidence affects the conclusion,
- what retrieval step would reduce uncertainty,
- whether the answer should be narrower, conditional, or deferred.

## Known Fact Rules

Only mark a fact as known when it is:

- directly stated by the user,
- observed in a file, tool output, log, test result, source, system record, or policy,
- part of an explicit instruction or schema,
- common stable context that does not need retrieval.

Do not mark as known:

- likely intent,
- guessed dates, prices, policy terms, legal rules, medical facts, account states, or test outcomes,
- model memory when current verification is required,
- claims from unavailable or unreviewed sources.

## Assumption Rules

Assumptions are allowed only when they are:

- low risk,
- explicitly labeled,
- easy for the user to correct,
- not the basis for irreversible, high-impact, private, legal, medical, financial, code, file, or external-send actions.

If an assumption controls the answer, ask or retrieve instead.

## Missing Evidence Rules

Use `ask` when the missing evidence is held by the user.

Use `retrieve` when the missing evidence is likely in:

- files,
- logs,
- tests,
- policy documents,
- source links,
- account records,
- support tickets,
- medical, legal, financial, or purchase records,
- current external information.

Use `defer` when the evidence requires a qualified professional, unavailable system, human review, or approved tool.

## Unsupported Claim Rules

Revise or remove claims that:

- invent facts,
- cite unavailable sources,
- imply tests ran when they did not,
- overstate certainty,
- turn examples into proof,
- generalize from insufficient evidence,
- claim safety, legality, medical accuracy, financial benefit, or policy compliance without support.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `task_summary`
- `answer_summary`
- `known_facts`
- `assumptions`
- `missing_evidence`
- `unsupported_claims`
- `next_retrieval_steps`
- `recommended_action`

Do not include raw secrets, private records, full logs, full transcripts, full account records, or unrelated private data when a redacted summary is enough.

## Decision Rule

- If the answer rests on known facts and uncertainty is handled, accept.
- If the answer contains unsupported claims, revise.
- If the user can supply missing evidence, ask.
- If evidence can be obtained from an approved source or tool, retrieve.
- If evidence requires human, professional, or unavailable-system review, defer.
- If the request asks for confident claims despite missing evidence in a high-risk setting, refuse unsafe certainty and explain the boundary.
- If a checker is unavailable or untrusted, use manual evidence-first review.

## Output Pattern

For evidence-sensitive work, prefer:

```text
Evidence map:
- Known facts: ...
- Assumptions: ...
- Missing evidence: ...
- Next retrieval: ...
- Answer boundary: ...
```

For user-facing answers, keep this concise unless the user asks for the full audit trail.

---
name: AI Output Failure Triage
description: Diagnose why an AI response failed, identify missing context, and prepare a safer retry prompt with acceptance checks and a go/no-go recommendation.
version: "1.0.1"
type: prompt-flow
tags:
  - ai-productivity
  - ai-literacy
  - prompt-debugging
  - output-quality
  - verification
author: OpenClaw Skill Library
---

# AI Output Failure Triage

## Overview

AI Output Failure Triage helps a user analyze an unsatisfactory AI-generated answer before trying again. It separates the original goal, prompt, model output, likely failure causes, missing context, and verification needs, then produces a clearer retry prompt and a recommendation about whether to retry, switch approach, gather more inputs, or handle the work manually.

This is a prompt-only diagnostic skill. It does not claim that the next AI answer will be correct. It helps improve task framing and verification discipline.

## When to Use

Use this skill when the user asks for help with:

- A response from an AI tool that was wrong, shallow, unsafe, off-tone, incomplete, or not useful
- Debugging a prompt that produced a bad result
- Rewriting a prompt so the next attempt is clearer
- Creating acceptance checks for an AI-generated answer
- Deciding whether an AI task should be retried, escalated, researched, or done manually

**Trigger phrases:** "Why did this AI answer fail?", "Fix my prompt", "The AI gave me a bad response", "Make this retry safer", "How should I ask again?", "Triage this output"

## Required Inputs

Ask for only what is needed, and avoid requesting confidential information. Useful inputs include:

- Original goal or job-to-be-done
- Original prompt or instruction
- AI output that failed
- What was wrong with the output
- Audience, stakes, format, deadline, constraints, and known facts
- Any source material that can be safely shared
- Whether the domain is factual, medical, legal, financial, safety-critical, or high-stakes

If the user cannot provide the original prompt or output, proceed with a partial triage and clearly mark assumptions.

## Workflow

### Step 1 - Capture the Original Goal, Prompt, and Output

Create a compact record of:

- User's intended outcome
- Original prompt or instruction
- AI output or summarized failure
- The gap between expected and actual result
- Any stated constraints, audience, or required format

If any item is missing, label it as "unknown" instead of inventing it.

### Step 2 - Classify the Failure Reason

Classify the failure into one or more likely categories:

- Goal ambiguity: the request did not define success clearly
- Missing context: key facts, source material, audience, or constraints were absent
- Output format mismatch: the answer did not follow the requested structure
- Reasoning gap: the answer skipped steps, made unsupported leaps, or failed to compare options
- Verification gap: factual claims, citations, calculations, or assumptions were not checked
- Tone or audience mismatch: style was wrong for the intended reader
- Safety or privacy issue: the answer requested or exposed sensitive data, or crossed a risk boundary
- Capability mismatch: the task needed tools, live data, domain expertise, or human judgment

Briefly explain the top two or three causes with evidence from the prompt/output.

### Step 3 - Identify Missing Context

Build a missing context checklist. Include only items that materially affect the next attempt:

- Required inputs or source documents
- Definitions of success and failure
- Audience and decision-maker
- Constraints, exclusions, and non-goals
- Preferred tone, length, and format
- Examples of acceptable or unacceptable output
- Verification method, references, or authoritative sources
- Confidential details that should be redacted or summarized instead of shared

Mark each item as "needed now", "helpful later", or "not required".

### Step 4 - Rewrite the Task Framing

Rewrite the task into a clearer structure:

- Role: what perspective the AI should take
- Objective: the concrete outcome
- Inputs: what material the AI may use
- Constraints: boundaries, exclusions, and assumptions
- Output format: exact sections, length, and style
- Verification: checks the answer must perform before finalizing
- Uncertainty behavior: how to label unknowns or ask follow-up questions

Keep the rewrite concise enough for practical reuse.

### Step 5 - Add an Acceptance Test

Create acceptance criteria that the next answer must satisfy. Include:

- Must-have content
- Must-not-do constraints
- Format requirements
- Evidence or verification requirements
- Edge cases or failure modes to watch for

For high-stakes topics, require independent verification and do not treat the AI response as authoritative.

### Step 6 - Recommend Retry, Switch, Gather, or Manual Handling

Make a go/no-go recommendation:

- Retry with improved prompt: if the issue was mainly framing or missing format guidance
- Gather more context first: if key facts or source material are missing
- Switch tool/model/workflow: if the task needs browsing, calculation, coding, file processing, or stronger reasoning
- Ask a human expert: if domain risk is high or consequences are significant
- Handle manually: if the task requires judgment, accountability, confidential access, or direct stakeholder communication

Explain the recommendation in one or two sentences.

### Step 7 - Produce the Reusable Next Prompt and Diagnosis Summary

Deliver a final triage report with:

- Diagnosis summary
- Missing context checklist
- Improved task framing
- Acceptance test
- Safer retry prompt
- Go/no-go recommendation
- Verification notes and cautions

## Deliverable Format

Return the report in this structure:

```markdown
# AI Output Failure Triage Report

## 1. Original Task Snapshot
- Goal:
- Original prompt:
- Failed output summary:
- What went wrong:

## 2. Likely Failure Causes
- Primary cause:
- Secondary causes:
- Evidence:

## 3. Missing Context Checklist
- Needed now:
- Helpful later:
- Not required:

## 4. Improved Task Framing
- Role:
- Objective:
- Inputs:
- Constraints:
- Output format:
- Verification:
- Uncertainty behavior:

## 5. Acceptance Test
- The next output must:
- The next output must not:
- Verification required:

## 6. Safer Retry Prompt
[Reusable prompt]

## 7. Go/No-Go Recommendation
- Recommendation:
- Rationale:
- Next action:
```

## Safety Boundaries

- Do not claim the next AI answer will be correct.
- Require verification for factual, medical, legal, financial, safety-critical, or otherwise high-stakes outputs.
- Do not encourage users to paste secrets, credentials, private records, confidential business data, or sensitive personal information into an AI tool.
- Encourage redaction, summarization, or local processing for sensitive context.
- Do not help create deceptive, manipulative, or harmful prompts.
- If the failed output involves professional advice, frame the result as preparation for review by a qualified person, not a substitute for that person.

## Example Prompts

- "The AI gave me a detailed answer about a historical event but it has three factual errors and I'm not sure how to fix my prompt. Triage this output and give me a safer retry prompt."
- "I asked for a project plan but got back a vague, unhelpful response that skipped the timeline and resource estimates I needed. Help me debug what went wrong and rewrite the prompt."
- "An AI tool generated a financial summary for my client presentation but it made unsupported claims and used the wrong tone. Create a failure triage report with acceptance checks before I retry."

## Acceptance Criteria

1. The report captures the original goal, prompt, failed output, and observed gap when available.
2. The report classifies likely failure causes using evidence rather than blame or guesswork.
3. Missing context is listed and prioritized.
4. The retry prompt includes role, objective, inputs, constraints, output format, verification, and uncertainty behavior.
5. An acceptance test is included.
6. A go/no-go recommendation is explicit.
7. High-stakes or sensitive tasks include verification and privacy cautions.
8. The skill remains prompt-only and requires no API, network access, credentials, or executable code.

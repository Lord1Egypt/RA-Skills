---
name: second-opinion
description: >
  Independent second opinion via a sub-agent. Three modes: Review (diff review
  with pass/fail), Challenge (adversarial mode that tries to break your code),
  Consult (ask anything with session continuity). The independent developer
  who hasn't seen your conversation. Use when: "second opinion", "another
  perspective", "challenge this", "independent review", "what would someone
  else think".
---

# Second Opinion — Independent AI Review

Spawn a sub-agent with fresh context — no bias from your current conversation. Three modes.

---

## Mode 1: Review

Independent diff review against the base branch.

1. Get the diff: `git diff origin/<base>`
2. Assemble a context block: branch name, diff stat, commit messages, what the PR claims to do
3. Spawn a sub-agent with this prompt:

> You are an independent code reviewer seeing this diff for the first time. No prior context.
> 
> Context: {branch}, {N} files changed, {stat summary}
> Commits: {commit messages}
> Stated intent: {what the PR says it does}
> 
> Diff:
> {full diff}
> 
> Review this diff. Be direct. Name specific files and line numbers.
> 1. What's GOOD about this code?
> 2. What's BROKEN or will break in production?
> 3. What's MISSING (tests, error handling, edge cases)?
> 4. Verdict: PASS / CHANGES REQUESTED / BLOCKED

4. Present the output verbatim under `SECOND OPINION:` header
5. Synthesize: where you agree, where you disagree, whether it changes your verdict

---

## Mode 2: Challenge

Adversarial mode — the sub-agent tries to break your code.

1. Read the changed files fully
2. Spawn a sub-agent:

> You are an adversarial code reviewer. Your job is to BREAK this code.
> 
> Changed files:
> {file contents}
> 
> For each file:
> 1. Find inputs that crash it
> 2. Find race conditions
> 3. Find security holes
> 4. Find edge cases the author didn't consider
> 5. Find performance traps
> 
> Be creative. Be mean. Think like a bug bounty hunter.
> For each finding: file:line, the attack vector, expected vs actual behavior.

3. Present findings. For each confirmed vulnerability, offer to fix it.

---

## Mode 3: Consult

Ask the sub-agent anything about your codebase.

1. Assemble context: relevant files, current problem, what you've tried
2. Spawn a sub-agent:

> Context: {relevant code and problem description}
> 
> The user asks: {question}
> 
> Be direct. Name specific files and functions. If you're guessing, say so.
> If you need more context, say exactly what you need.

3. Present the answer. If it needs follow-up, loop.

---

## How to Invoke

Ask the user:

> What do you want?
> - **Review** — independent diff review (pass/fail)
> - **Challenge** — adversarial mode, try to break my code
> - **Consult** — ask anything about the codebase

Then proceed with the matching mode.

## Important

- The sub-agent has **no memory of your conversation.** That's the feature — fresh eyes.
- Present its output **verbatim.** Don't summarize or filter.
- After presenting, synthesize: agree/disagree, what changes.
- If the sub-agent fails or times out: "Second opinion unavailable. Continuing without it."

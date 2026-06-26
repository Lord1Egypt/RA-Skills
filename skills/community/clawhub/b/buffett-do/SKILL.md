---
name: buffett-do
description: Buffett-style Research Prioritization Assistant — decide whether a company deserves deeper research, what to check first, and get a copy-paste research prompt for your agent.
category: research
version: 1.1.8
created: 2026-05-22
owner: choosenobody
status: active
tags: [buffett, research, prioritization, investment, moat, fundamental-analysis]
---

# What Buffett Would Do

Buffett-style Research Prioritization Assistant — decide whether a company deserves deeper research, what to check first, and get a copy-paste research prompt for your agent.

---

## Best For

- Deciding whether a company deserves deeper research.
- Avoiding wasted time on weak or overhyped ideas.
- Creating a first-pass research prompt for another agent.

---

## What You Get

You will get 3 parts:

### 1. Decision

One of four research-priority labels:

- **Research Now** — worth deeper research now.
- **Watch** — interesting, but one key fact must be verified first.
- **Skip** — not worth your research time for now.
- **NEEDS INFO** — not enough data to judge.

### 2. Check First

Exactly 3 things to verify first:

1. **Business quality** — is the business durable, understandable, and cash-generative?
2. **Moat/risk** — what protects the business, and what single event could kill the thesis?
3. **Valuation sanity** — does the current price already assume too much future success?

### 3. Paste This to an Agent

A short research prompt you can copy into your agent for deeper analysis.

Generate one compact copy-paste prompt:

```
Analyze [company/ticker] as a long-term business, not as a trading idea. First decide whether it is worth deeper research. Check business quality, moat durability, management/capital allocation, cash-flow quality, the key risk that could kill the thesis, and valuation sanity. Do not give buy/sell advice. End with: Research Now / Watch / Skip / NEEDS INFO.
```

Adapt to the specific company — substitute the ticker or sector if provided.

---

## Install

Recommended for most multi-agent OpenClaw users:

```
openclaw skills install buffett-do --global
```

Workspace-only install:

```
openclaw skills install buffett-do
```

Reinstall / overwrite existing workspace copy:

```
openclaw skills install buffett-do --force
```

Update later:

```
openclaw skills update buffett-do --global
```

Verify:

```
openclaw skills info buffett-do
openclaw skills check
```

**Notes:**
- `--global` is recommended for users who want the skill visible to multiple local agents.
- `--force` should only be used when an older workspace copy already exists or the updated version does not appear.
- Do not use `--global --agent` together.

---

## Activation

Primary trigger:

```
what Buffett would do with [company/ticker]
```

Additional natural triggers:

- - Should I research [company/ticker]?
- - Is [company/ticker] worth deeper research?
- - Run Buffett-style research priority on [company/ticker]

Example:

```
what Buffett would do with Google (NASDAQ:GOOGL)
```

---

## What This Will Not Do

- This is not financial advice.
- It will not give buy, sell, or hold verdicts.
- It will not give price targets or fair value estimates.
- It will not tell you how much portfolio weight to allocate.
- It will not pretend to know Buffett's private view.
- It will say NEEDS INFO when the available facts are insufficient.
- It will keep the output short, practical, and action-oriented.

This skill does not ask for API keys, wallet keys, brokerage login, private files, or personal portfolio details.

---

## Feedback

Tried it? DM me on X: @BeeGeeEth

Most useful feedback:
- Which company/ticker did you test?
- Did the label feel right or wrong?
- Was any "Check First" item missing?
- Did the skill trigger when it should not?
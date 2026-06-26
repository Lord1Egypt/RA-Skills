---
name: ContextLedger
slug: contextledger
version: 1.0.0
description: Evidence-first knowledge auditing skill that upgrades connected knowledge into an auditable conclusion card. It traces which sources support a conclusion, marks which cited source is oldest or stale, surfaces source conflicts, separates direct evidence from inference, and ends with the most reliable next judgment. Use when the user says things like "这个结论从哪来的", "哪份资料已经旧了", "这些资料互相冲突怎么办", "不要长摘要，给我证据卡", or "哪些地方只是推断不是证据".
metadata:
  clawdbot:
    emoji: "🧾"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

# ContextLedger

One-line positioning:
Give knowledge an audit trail: source traceability, freshness judgment, conflict flags, and a reliable next call.

ContextLedger is not another note app.
It is not a passive knowledge graph.
It is not a long-form summarizer that smooths disagreement away.

It is the audit layer that sits after information has already been gathered.

Its job is to help the user answer:
- 这个结论到底来自哪几份资料
- 哪一份最旧，哪一份可能已经过时
- 哪两份资料在互相打架
- 哪些句子是直接证据，哪些只是推断
- 在不确定还存在的情况下，现在最可靠的判断是什么

The tone should feel like a careful knowledge auditor:
- evidence first
- dates matter
- disagreement stays visible
- inference must be labeled
- the final judgment should be useful, not evasive

## Product Boundary

Think of the knowledge stack like this:
- `Knowledge Connector`: connect, import, search, and relate knowledge
- `ContextLedger`: audit where the conclusion comes from and how trustworthy it is
- `DecisionDeck`: compress the audited material into a decision brief
- `NextFromKnowledge`: turn the audited material into the next move

Keep the boundary clear:
- if the user needs ingestion, retrieval, or relationship discovery, use `Knowledge Connector` first
- if the user needs source traceability, freshness, contradiction handling, or evidence grading, use `ContextLedger`
- if the user needs a boss-ready decision brief, hand the audited result to `DecisionDeck`
- if the user needs action, hand the audited result to `NextFromKnowledge`

ContextLedger does not win by knowing more.
It wins by making knowledge inspectable.

## When To Use It

Use this skill when the user says things like:
- `这个说法是从哪来的`
- `哪份资料已经旧了`
- `这些文件在互相矛盾`
- `不要长摘要，给我证据账本`
- `哪些地方是事实，哪些只是推断`
- `我想知道现在最可靠的判断，不要装得很确定`
- `把这几份文档的依据、冲突和更新风险说清楚`
- `资料来源混杂，帮我做可信度梳理`

It is strongest when the user has:
- notes, docs, reports, or meeting summaries
- connector outputs or copied web research
- local knowledge mixed with external sources
- a conclusion that now needs provenance and trust checks
- time-sensitive material where recency can change the answer

It is especially useful when the user already suspects:
- the sources are old
- several documents disagree
- some claims are second-hand
- the previous summary hid uncertainty

## What This Skill Must Do

By default, it should:
- identify the exact claim, conclusion, or question being audited
- attach the most relevant 2 to 5 sources behind that claim
- mark which cited source is newest, oldest, undated, or likely stale
- distinguish direct evidence, corroborated evidence, inference, assumption, and unknown
- surface conflicts without collapsing them into fake consensus
- explain whether the conflict changes the current judgment
- end with the most reliable next judgment the evidence can support right now

Do not stop at:
- a generic summary
- a source list with no judgment
- `资料各有说法`
- pretending the newest source always wins
- presenting inference as if it were evidence

## Core Modes

1. conclusion audit mode
   - explain where one conclusion comes from and how strong it is
2. freshness check mode
   - judge whether cited material is current enough for the question
3. conflict check mode
   - surface where sources disagree and whether the disagreement is material
4. evidence gap mode
   - show which important sentences are evidence-backed and which are not
5. source-backed answer mode
   - answer the question, but only through an auditable ledger structure

Read [references/audit-heuristics.md](references/audit-heuristics.md) when freshness, evidence grade, or contradiction handling is the hard part.
Read [references/conclusion-cards.md](references/conclusion-cards.md) when the user wants a tighter or more executive-friendly audit card.

## Input Handling

Common inputs:
- copied notes or summaries
- multiple documents
- tables, bullets, screenshots, or connector results
- research outputs with mixed dates
- policy docs, product docs, and commentary mixed together
- earlier AI summaries that now need to be checked

Normalize messy inputs, but do not fake precision the material does not support.

If the material is thin:
- say the evidence is thin
- reduce the strength of the final judgment
- recommend the single best next check

If the material is undated:
- say it is undated
- do not invent freshness confidence

If the material contains only one source:
- give a source-backed answer
- but state clearly that there is no cross-source corroboration

## Core Workflow

1. Define the audit target.
   Decide:
   - what exact claim or question is under review
   - whether the user wants traceability, freshness, conflict resolution, or a final answer

2. Build the source ledger.
   For each relevant source, capture:
   - what it says
   - what claim it supports or weakens
   - whether it is primary, derivative, dated, or undated when that is knowable

3. Grade the support.
   Separate:
   - direct evidence
   - corroborated evidence
   - inference
   - assumption
   - unknown

4. Judge freshness.
   Ask:
   - which cited source is newest
   - which is oldest
   - whether any source appears stale for this claim
   - whether recency changes the answer or only changes confidence

5. Surface conflict.
   Explain:
   - which sources disagree
   - what exactly they disagree about
   - whether the conflict is factual, scope-based, time-based, or definitional
   - whether the conflict changes the best current judgment

6. Make the smallest honest call.
   End with:
   - the best current judgment
   - why it is the best-supported call right now
   - what would change that call
   - the next reliable step if uncertainty still matters

## Audit Rules

### Evidence Before Eloquence

Do not make the answer sound cleaner than the sources are.
If the record is messy, the audit should stay honest about that.

### Label Inference Plainly

Preferred phrasing:
- `这部分有直接证据支持。`
- `这个判断来自多份资料的共同指向。`
- `这里更像推断，不是资料直接结论。`
- `这一步目前还是假设。`

### Recency Is Claim-Specific

Do not treat freshness as a global property of a file.
A source can be recent on one point and stale on another.

### Newer Does Not Automatically Beat Better

When two sources disagree, consider:
- source type
- directness
- scope
- date

A dated primary record can outrank a newer derivative summary.

### Conflict Must Stay Visible

Do not merge disagreement into fake consensus.
Good wording:
- `冲突点在时间窗口，不在结论方向。`
- `两份资料对同一事实给出了不同版本。`
- `分歧主要来自定义不同，不一定是真正对打。`

### The Final Call Must Match The Evidence

If the support is strong enough, make the call.
If it is not, narrow the claim instead of hiding.

Good endings:
- `当前最稳的判断是……`
- `能确定到这里，再往后就是推断。`
- `现在可以先下这个小判断，完整判断还差一项核对。`

## Output Pattern

Use this structure unless the user asks for something shorter:

### Question Or Claim
State the exact thing being audited.

### Best Current Judgment
Give the most reliable answer first.

### Source Ledger
List the key sources, usually 2 to 5, and for each one show:
- what it supports
- whether it weakens another claim
- whether it is newest, oldest, undated, or likely stale

### Oldest Or Stale Signal
Call out the source that most threatens freshness confidence.

### Where Sources Conflict
Name the disagreement directly and say whether it changes the current judgment.

### Evidence Vs Inference
Separate what is directly supported from what is inferred.

### What Would Change The Call
State the single fact or source update most likely to change the answer.

### Next Reliable Step
Give the next check, decision, or escalation.

## Finish Standard

When this skill is done well, the user should be able to say:
- I know where this answer came from
- I know which source is oldest
- I know what still conflicts
- I know what is evidence and what is inference
- I know the most reliable judgment I can make now

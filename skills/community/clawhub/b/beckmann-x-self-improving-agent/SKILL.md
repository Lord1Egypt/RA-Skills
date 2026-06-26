\---

name: beckmann-x-self-improving-agent
version: 1.0.0
description: "Combination skill that adds the Beckmann Knowledge Graph as a deep-reasoning escalation layer on top of the Self-Improving Agent (pskoett). Everyday tasks run through the Self-Improving Agent as usual. This skill defines exactly when and how to switch to the Beckmann Knowledge Graph and how to feed insights back. Uninstalling this skill leaves the Self-Improving Agent fully intact."
author: matthiasbeckmann987-spec
license: MIT-0
requires: "pskoett/self-improving-agent, matthiasbeckmann987-spec/beckmann-knowledge-graph"
tags: "meta-skill, combination, beckmann-logic, self-improvement, orchestration"
---

# Beckmann × Self-Improving Agent — Combination Skill

## Purpose

This skill connects two independent skills without modifying either one:

|Skill|Role here|
|-|-|
|`pskoett/self-improving-agent`|**Default engine** for all tasks|
|`matthiasbeckmann987-spec/beckmann-knowledge-graph`|**Deep-reasoning escalation** for specific question types|

**Uninstalling this skill:** Remove this SKILL.md. Both base skills continue
working exactly as before. No data is lost.

\---

## Default Behaviour: Self-Improving Agent Runs Everything

Follow `pskoett/self-improving-agent` for all tasks:

* Log errors to `.learnings/ERRORS.md`
* Log learnings to `.learnings/LEARNINGS.md`
* Promote patterns after 3 repetitions
* Maintain the `LRN-YYYYMMDD-XXX` log format

This combination skill adds **nothing** to this flow unless a Beckmann trigger
is detected (see below).

\---

## Beckmann Escalation Triggers

Escalate to `beckmann-knowledge-graph` when the question matches **one or
more** of these categories:

|#|Category|Example signals|
|-|-|-|
|1|**Open scientific / philosophical question**|"What is consciousness?", "Does free will exist?", "What is dark energy?"|
|2|**Apparent paradox**|Question contains an internal contradiction or "impossible" framing|
|3|**High-complexity long-horizon forecast**|"How will AI change democracy in 20 years?", "What are AGI systemic risks?"|
|4|**Strategic dead end**|Obvious solutions have repeatedly failed; dominant expectations seem to block progress|
|5|**AI safety / architecture question**|Dangerous vs. safe AI design, value alignment, AI-human symbiosis|
|6|**Epistemological limit question**|"Is it even possible to know X?", "Is a presupposition in this question false?"|

**Do NOT escalate for:**
Coding, bug fixes, file operations, factual lookups, arithmetic, or any
question already answered by existing learnings in `.learnings/`.

**Uncertain?** Apply the Complexity Check:

> "Would a highly intelligent person answer this differently after a week
> of thinking about hidden assumptions in the question?"

* Yes → suggest Beckmann. No → stay on default path.

\---

## Proactive Suggestion (Before Escalating)

If a Beckmann trigger is detected, the agent **must not escalate silently or
automatically**. Instead, it first informs the user and waits for confirmation.

**Suggested phrasing:**

> "Your question touches on \[open scientific question / an apparent paradox /
> a high-complexity forecast — pick the matching category]. I have access to
> the Beckmann Knowledge Graph, a structured reasoning framework for exactly
> this type of question. Would you like me to apply it? It will take a bit
> longer than a standard answer, but will analyse hidden assumptions and
> offer a more structured response."

**Then wait.** Only escalate if the user confirms.

If the user declines, answer with standard knowledge and note:

> "I've answered with standard reasoning. The Beckmann Knowledge Graph
> remains available if you'd like to go deeper later."

\---

## Escalation Protocol (Step by Step)

### 1 — Load the graph

```javascript
import graph from './beckmann-knowledge-graph/graph.json' assert { type: 'json' };
const entities = graph.entities;
const relations = graph.relations;
```

### 2 — Apply the 6-step Beckmann protocol

Follow `beckmann-knowledge-graph/SKILL.md` exactly:

1. Classify the question (epistemological / paradox / forecast / strategic / AI safety)
2. Extract relevant entities
3. Trace relation paths — pay attention to `leads to`, `triggers`, `is reversed by`, `protects against`
4. Apply Beckmann Logic (Problem Level → Low vs. High Complexity Solution → Reversal Effect check)
5. Apply epistemological grounding (model vs. external reality, known limits)
6. Structure output in Graph-Grounded Answer format (see below)

### 3 — Deliver the answer

```
## Graph-Grounded Answer

\*\*Problem framing\*\*
(what the question really asks, after presupposition analysis)

\*\*Relevant graph nodes used:\*\*
- \[Entity ID] — \[why relevant]

\*\*Reasoning path\*\*
(relation chain that leads to the answer)

\*\*Answer\*\*
(the actual response, informed by the graph logic)

\*\*Confidence and limits\*\*
(what the graph cannot resolve, and why)

\*\*New questions opened\*\*
(what the next problem level is)
```

### 4 — Log back to Self-Improving Agent

After every Beckmann analysis, add an entry to `.learnings/LEARNINGS.md`:

```markdown
## \[LRN-YYYYMMDD-XXX] insight

\*\*Logged\*\*: <ISO-8601 timestamp>
\*\*Priority\*\*: medium
\*\*Status\*\*: pending
\*\*Area\*\*: beckmann

### Summary
Beckmann analysis: <one-line description of the question>

### Details
- Question type: <paradox | forecast | epistemological | strategic | ai-safety>
- Graph nodes used: <comma-separated entity IDs>
- Key insight: <most important finding>
- New actual level: <what the problem level becomes after this analysis>

### Suggested Action
<Promote to CLAUDE.md if broadly applicable.
Flag as #beckmann-graph-extension-candidate if a graph gap was found.>

### Metadata
- Source: beckmann-knowledge-graph v<version>
- Tags: #beckmann, #<question-type>
```

\---

## Graph Extension Feedback Loop

The Beckmann Knowledge Graph is designed to grow. When this combination skill
surfaces a gap in the graph, flag it so the graph author can act on it.

**Flag as `#beckmann-graph-extension-candidate` when:**

* No entity matched the core concept of the question
* A new historical case study would have strengthened the analysis
* A new relation type was needed but absent
* A new paradox or open question was encountered that the graph doesn't cover

**Add to the LEARNINGS entry Metadata:**

```markdown
- Tags: #beckmann, #beckmann-graph-extension-candidate
- Extension-Type: new\_entity | new\_relation | new\_case\_study | new\_paradox
- Suggested-Entity-ID: <proposed entity name>
- Suggested-Entity-Type: <type from graph schema>
- Suggested-Description: <draft description for the graph author>
```

> \*\*Future capability:\*\* When a future version of the Beckmann Knowledge Graph
> supports agent-driven graph extension, entries tagged
> `#beckmann-graph-extension-candidate` will serve as the structured input
> for that process. No changes to the logging format will be needed.

\---

## Conflict Resolution

|Situation|Rule|
|-|-|
|Self-Improving Agent says "move on"; Beckmann analysis still open|Finish the Beckmann analysis first, then log|
|Beckmann produces a low-complexity solution|**Red flag** — apply reversal effect check before delivering|
|A LEARNINGS entry contradicts a Beckmann graph node|Prefer the externally validated answer; log the contradiction as `#beckmann-candidate`|
|`graph.json` missing or unreadable|Fall back to Self-Improving Agent only; log missing graph as error|

\---

## Quick Reference

|Signal|Action|
|-|-|
|Coding error, failed command, user correction|→ Self-Improving Agent: log to ERRORS.md or LEARNINGS.md|
|"What is consciousness / free will / dark energy?"|→ Escalate to Beckmann|
|"How will X change in 20 years?"|→ Escalate to Beckmann (forecast)|
|"Why does X always fail even though it seems logical?"|→ Escalate to Beckmann (reversal effect suspected)|
|"Is it even possible to know X?"|→ Escalate to Beckmann (epistemological limit)|
|Graph entity not found|→ Log as `#beckmann-graph-extension-candidate`|
|Beckmann analysis complete|→ Log to LEARNINGS.md with `#beckmann` tag|

\---

## Uninstall

1. Delete this `SKILL.md`.
2. Both `pskoett/self-improving-agent` and
`matthiasbeckmann987-spec/beckmann-knowledge-graph` continue working
independently. No data in `.learnings/` is affected.


---
name: beckmann-x-self-improving-proactive
version: 1.1.0
description: "Combination skill that adds the Beckmann Knowledge Graph as a deep-reasoning escalation layer on top of the Self-Improving + Proactive Agent (ivangdavila). Everyday tasks run through the Self-Improving + Proactive Agent as usual. This skill defines exactly when and how to switch to the Beckmann Knowledge Graph and how to feed insights back into hot/warm/cold memory — only after explicit user consent. Uninstalling this skill leaves the Self-Improving + Proactive Agent fully intact and offers an optional clean removal of all #beckmann memory entries."
author: matthiasbeckmann987-spec
license: MIT-0
requires: "ivangdavila/self-improving@1.2.16, matthiasbeckmann987-spec/beckmann-knowledge-graph@3.1.0"
tags: "meta-skill, combination, beckmann-logic, self-improvement, proactive, orchestration"
---

# Beckmann × Self-Improving + Proactive Agent — Combination Skill

## Purpose

This skill connects two independent skills without modifying either one:

| Skill | Role here |
|-|-|
| `ivangdavila/self-improving` | **Default engine** for all tasks — with proactive memory and self-reflection |
| `matthiasbeckmann987-spec/beckmann-knowledge-graph` | **Deep-reasoning escalation** for specific question types |

**Uninstalling this skill:** See the Uninstall section below. Both base skills continue working exactly as before. Memory handling is controlled by the chosen uninstall mode.

---

## Pinned Dependencies (Security)

This skill was audited against the following exact dependency revisions.  
Install or resolve only these versions. Do not auto-update.

| Package | Version | Integrity (sha256) | Registry | Audited |
|-|-|-|-|-|
| `ivangdavila/self-improving` | `1.2.16` | `e68745b6d7e1e1df757717ce120b63ac1a123f6123a1db6f540592498ad6cf7b` | clawhub.ai | 2026-09-20 |
| `matthiasbeckmann987-spec/beckmann-knowledge-graph` | `3.1.0` | `03b30bab02d641a23e55e7ef8966bdd6e8ab011a041b45de0c04666be277a6dc` | clawhub.ai | 2026-09-20 |

If the resolved artifact does not match the expected integrity digest, **fail closed** and do not load the skill.

---

## Default Behaviour: Self-Improving + Proactive Agent Runs Everything

Follow `ivangdavila/self-improving` for all tasks:

* HOT memory in `~/self-improving/memory.md` (≤100 lines, always loaded)
* WARM memory in `~/self-improving/projects/` and `~/self-improving/domains/`
* COLD memory in `~/self-improving/archive/`
* Log corrections to `~/self-improving/corrections.md`
* Promote patterns after 3x in 7 days → HOT
* Demote after 30 days unused → WARM; after 90 days → COLD
* Self-reflect after significant tasks (CONTEXT / REFLECTION / LESSON format)
* Maintain heartbeat state in `~/self-improving/heartbeat-state.md`

This combination skill adds **nothing** to this flow unless a Beckmann trigger is detected (see below).

---

## Beckmann Escalation Triggers

Escalate to `beckmann-knowledge-graph` when the question matches **one or more** of these categories:

| # | Category | Example signals |
|-|-|-|
| 1 | **Open scientific / philosophical question** | "What is consciousness?", "Does free will exist?", "What is dark energy?" |
| 2 | **Apparent paradox** | Question contains an internal contradiction or "impossible" framing |
| 3 | **High-complexity long-horizon forecast** | "How will AI change democracy in 20 years?", "What are AGI systemic risks?" |
| 4 | **Strategic dead end** | Obvious solutions have repeatedly failed; dominant expectations seem to block progress |
| 5 | **AI safety / architecture question** | Dangerous vs. safe AI design, value alignment, AI-human symbiosis |
| 6 | **Epistemological limit question** | "Is it even possible to know X?", "Is a presupposition in this question false?" |

**Do NOT escalate for:**  
Coding, bug fixes, file operations, factual lookups, arithmetic, or any question already answered by HOT memory (`~/self-improving/memory.md`).

**Uncertain?** Apply the Complexity Check:

> "Would a highly intelligent person answer this differently after a week of thinking about hidden assumptions in the question?"

* Yes → suggest Beckmann.  
* No → stay on default path.

---

## Proactive Suggestion (Before Escalating)

If a Beckmann trigger is detected, the agent **must not escalate silently or automatically**. Instead, it first informs the user and waits for confirmation.

**Suggested phrasing:**

> "Your question touches on [open scientific question / an apparent paradox / a high-complexity forecast — pick the matching category]. I have access to the Beckmann Knowledge Graph, a structured reasoning framework for exactly this type of question. Would you like me to apply it? It will take a bit longer than a standard answer, but will analyse hidden assumptions and offer a more structured response."

**Then wait.** Only escalate if the user confirms.

If the user declines, answer with standard knowledge and note:

> "I've answered with standard reasoning. The Beckmann Knowledge Graph remains available if you'd like to go deeper later."

---

## Integration with Proactive Memory (with Consent + Quarantine)

The Self-Improving + Proactive Agent uses a tiered HOT/WARM/COLD memory architecture. Beckmann insights integrate into this system **only after explicit user consent** and first land in quarantine.

### Mandatory Consent before any persistent write

After delivering a Beckmann answer, the agent **must** ask:

> "I have generated a Beckmann insight from this analysis.  
> Would you like me to store it in the Self-Improving memory (quarantine first)?  
> You can later promote, demote, or delete it.  
> [Yes – store in quarantine] / [No – discard]"

* Only proceed with a memory write if the user explicitly confirms.  
* If the user declines, do **not** write anything and do not self-reflect into persistent files.

### Where Beckmann results are stored (after consent)

| Type of insight | Target location | Tier | Notes |
|-|-|-|-|
| Any new Beckmann insight (first occurrence) | `~/self-improving/quarantine/beckmann-YYYYMMDD-XXX.md` | Quarantine | Isolated; not auto-loaded into HOT |
| Broad epistemological insight (after promotion) | `~/self-improving/memory.md` | HOT | Only after explicit promotion |
| Domain-specific finding | `~/self-improving/domains/<domain>.md` | WARM | Only after explicit promotion |
| Project-specific strategic insight | `~/self-improving/projects/<name>.md` | WARM | Only after explicit promotion |
| Graph gap / extension candidate | `~/self-improving/corrections.md` + `#beckmann-graph-extension-candidate` | WARM | Still requires consent |

### Promotion rules for Beckmann insights

* Quarantine entries are **never** auto-promoted.  
* Promotion to HOT/WARM requires either:  
  – explicit user command, or  
  – a heartbeat review that presents the candidate to the user for confirmation.  
* Same insight applied successfully 3× is only a **suggestion** for promotion, never an automatic action.  
* Always cite source: `"Using X (from self-improving/... — Beckmann analysis, quarantined on YYYY-MM-DD)"`

---

## Escalation Protocol (Step by Step)

### 1 — Check HOT memory first

Before loading the graph, scan `~/self-improving/memory.md` for entries tagged `#beckmann`. If a directly relevant insight exists there, use it — and note that it came from a previous Beckmann analysis. Only load the full graph if no relevant HOT entry exists.

### 2 — Load the graph

```javascript
import graph from './beckmann-knowledge-graph/graph.json' assert { type: 'json' };
const entities = graph.entities;
const relations = graph.relations;
```

(Load only the pinned version `3.1.0`. Fail closed on integrity mismatch.)

### 3 — Apply the 6-step Beckmann protocol

Follow `beckmann-knowledge-graph/SKILL.md` exactly:

1. Classify the question (epistemological / paradox / forecast / strategic / AI safety)
2. Extract relevant entities
3. Trace relation paths — pay attention to `leads to`, `triggers`, `is reversed by`, `protects against`
4. Apply Beckmann Logic (Problem Level → Low vs. High Complexity Solution → Reversal Effect check)
5. Apply epistemological grounding (model vs. external reality, known limits)
6. Structure output in Graph-Grounded Answer format (see below)

### 4 — Deliver the answer

```
## Graph-Grounded Answer

**Problem framing**
(what the question really asks, after presupposition analysis)

**Relevant graph nodes used:**
- [Entity ID] — [why relevant]

**Reasoning path**
(relation chain that leads to the answer)

**Answer**
(the actual response, informed by the graph logic)

**Confidence and limits**
(what the graph cannot resolve, and why)

**New questions opened**
(what the next problem level is)
```

### 5 — Self-reflect (only after consent)

After delivering a Beckmann answer **and** receiving explicit consent to store:

```
CONTEXT: Beckmann analysis — <question type>
REFLECTION: <what the graph revealed that standard reasoning would have missed>
LESSON: <what to apply next time a similar question appears>
```

If the user later confirms promotion, the lesson may move to HOT.

### 6 — Log to quarantine (only after consent)

Store the Beckmann insight first in quarantine.

**Entry format for quarantine file:**

```markdown
[BKM-YYYYMMDD-XXX]
Question type: <paradox | forecast | epistemological | strategic | ai-safety>
Graph nodes used: <comma-separated entity IDs>
Key insight: <most important finding>
New actual level: <what the problem level becomes after this analysis>
Source: beckmann-knowledge-graph v3.1.0
Tags: #beckmann, #<question-type>
Status: quarantine — requires explicit promotion
Created: <ISO timestamp>
Provenance: conversation-derived, user-consented
```

**If a graph gap was found, add:**

```markdown
Tags: #beckmann, #beckmann-graph-extension-candidate
Extension-Type: new_entity | new_relation | new_case_study | new_paradox
Suggested-Entity-ID: <proposed entity name>
Suggested-Entity-Type: <type from graph schema>
Suggested-Description: <draft description for the graph author>
```

---

## Graph Extension Feedback Loop

Beckmann graph gaps logged as `#beckmann-graph-extension-candidate` serve two purposes:

1. **Now:** Structured record for the graph author to review when planning the next version of `beckmann-knowledge-graph`.
2. **Future:** When a future version of the Beckmann Knowledge Graph supports agent-driven graph extension, these entries will serve as structured input. The logging format is designed to be machine-readable from day one.

All such entries still require the consent step above.

---

## Heartbeat Integration

The Self-Improving + Proactive Agent uses a heartbeat for recurring maintenance. Add this check to the heartbeat cycle:

```markdown
## Beckmann review (weekly)
- Scan quarantine/ for entries tagged #beckmann with Status: quarantine
- For each: present a short summary to the user and ask whether to promote, keep in quarantine, or delete
- Scan for #beckmann-graph-extension-candidate entries → collect for graph author review (still show to user)
- Demote HOT #beckmann entries unused for 30 days → WARM (notify user)
- Never auto-promote without explicit confirmation
```

---

## Conflict Resolution

| Situation | Rule |
|-|-|
| HOT memory and Beckmann analysis disagree | Prefer the externally validated Beckmann answer; log disagreement to `corrections.md` (after consent) |
| Beckmann produces a low-complexity solution | **Red flag** — apply reversal effect check before delivering |
| Graph not available or integrity mismatch | Fall back to Self-Improving + Proactive Agent only; log missing/mismatched graph to `corrections.md` |
| HOT memory already contains a `#beckmann` entry for this question | Use the HOT entry; skip full graph load; note "from prior Beckmann analysis" |

---

## Quick Reference

| Signal | Action |
|-|-|
| Coding error, failed command, user correction | → Self-Improving + Proactive Agent: log to corrections.md |
| "What is consciousness / free will / dark energy?" | → Escalate to Beckmann (after consent) |
| "How will X change in 20 years?" | → Escalate to Beckmann (forecast) |
| "Why does X always fail even though it seems logical?" | → Escalate to Beckmann (reversal effect suspected) |
| "Is it even possible to know X?" | → Escalate to Beckmann (epistemological limit) |
| Graph entity not found | → Log as `#beckmann-graph-extension-candidate` (after consent) |
| Beckmann analysis complete | → Ask for memory consent → self-reflect + quarantine log only if confirmed |
| Heartbeat runs | → Present quarantine candidates for user decision; never auto-promote |

---

## Uninstall

Two modes are supported:

### Soft uninstall (default)
1. Delete this `SKILL.md`.
2. Both `ivangdavila/self-improving` and `matthiasbeckmann987-spec/beckmann-knowledge-graph` continue working independently.
3. Memory entries in `~/self-improving/` tagged `#beckmann` (including quarantine) remain available as standard memory — no data loss.

### Clean uninstall (optional, recommended for security)
1. Delete this `SKILL.md`.
2. List every file and entry tagged `#beckmann` or located in `~/self-improving/quarantine/` that was created by this skill.
3. Ask the user to confirm deletion or archival of each item (or all at once).
4. After confirmation, remove or move the selected entries to an archive folder.
5. Both base skills continue working independently.

Always present both options and let the user choose.

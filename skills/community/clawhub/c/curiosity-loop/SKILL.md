---
name: curiosity-loop
description: "Intrinsic curiosity-driven continuous learning: detect gaps between expected and actual results, treat them as curiosity signals, and update skills accordingly. Inspired by developmental AI from Flowers Lab, INRIA."
version: 1.0.0
author: Guillaume D
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [learning, self-improvement, curiosity, developmental-AI, delta-tracking, continuous-improvement]
    related_skills: [blogwatcher, arxiv, polymarket]
---

# Curiosity Loop — Intrinsic Curiosity-Driven Continuous Learning

## Overview

A self-improvement framework that transforms knowledge gaps and failed outcomes into structured learning cycles. Inspired by developmental AI research from [Flowers Lab, INRIA](https://www.robots.org/flowers-lab/) and the work of Cédric Colas.

Rather than treating failures as errors, the Curiosity Loop treats them as **curiosity signals** — prompts for active exploration, skill updates, and curriculum building. This creates a continuous self-improvement loop that makes the agent progressively better at its domain.

### Core Concepts (from developmental AI)

| Concept | Source | Application |
|---------|--------|-------------|
| **Automatic Curriculum Learning (ACL)** | Portolas et al. (Flowers Lab) | Structured progression, not random learning |
| **Autotelic Activity** | Vygotsky / Colas | Learning for its own sake — intrinsic motivation |
| **Zone of Proximal Development (ZPD)** | Vygotsky | Learning "just beyond" current capability |
| **Map-Elites / Behavioral Diversity** | Mouret & Clune | Maximize repertoire diversity, not single optimization |
| **Semantic Interference** | Flowers Lab (CLIP research) | Biases reveal representation limits |

## When to Activate the Curiosity Loop

### Activation Signals (prioritize 1 at a time)

1. **Result delta**: A response/action does not produce the expected effect
2. **Iterative loop**: User repeats the same correction 2+ times
3. **Incomplete knowledge**: Detecting missing information for a correct answer
4. **Sub-optimal approach**: Recognizing a better approach exists
5. **Knowledge scan**: Discovering new concepts/tools via periodic scanning

### Do NOT activate when

- The result is correct and satisfactory (no delta)
- The user has not expressed a need for improvement
- The context is trivial (not worth the learning cycle)

## The Loop — 6 Numbered Steps

### Step 1: ACTION
Attempt to solve the problem with current knowledge.

### Step 2: DELTA
Identify the precise gap between expected and actual results.
- What did not work as expected?
- What was the expectation vs. reality?
- How much extra time/iterations did this cost?

### Step 3: CURIOSITY
Treat the delta as a learning signal, not a failure.
- What did I not know or not know well?
- What concept/tool/pattern was missing?
- Why was this information important?

### Step 4: RESEARCH
Actively explore the missing concept.
- Search docs, existing skills, external sources
- Use web_search, browser, terminal, session_search
- Validate the discovery's relevance

### Step 5: INTEGRATION
Update knowledge/skills.
- **If an existing skill is incomplete**: `skill_manage(action='patch')` with new info
- **If a new pattern is discovered**: `skill_manage(action='create')` for a new skill
- **If a stable fact is learned**: `memory(action='add')` for durable facts
- **If a tool/command is discovered**: document in the appropriate skill

### Step 6: CURRICULUM
Structure learning as progressive milestones.
- Identify missing prerequisites
- Decompose the concept into progressive sub-concepts
- Create verifiable milestones (can I explain this? can I use it?)

## Delta Tracking

Track all deltas in `~/.hermes/deltas.json` for auditability and periodic review.

Format:
```json
{
  "deltas": [
    {
      "id": "delta-001",
      "date": "2026-05-22",
      "context": "Short description of the context",
      "expected": "What was expected",
      "actual": "What happened",
      "gap": "What was missing (concept/tool/pattern)",
      "resolution": "How the gap was filled",
      "skill_updated": "Name of updated skill, or null",
      "status": "resolved | open | learning"
    }
  ]
}
```

## Diversity Policies (Map-Elites)

### Diversity Rule
When finding an effective pattern for a problem type, also:
1. Document the pattern in a skill
2. Identify 1-2 alternative approaches (even if less optimal)
3. Note cases where the alternative would be preferable

### Periodic Diversity Scan
Every ~30 days, check:
- Which patterns do I rarely or never use?
- Are there domains where I have only one approach?
- What skills could be enriched?

## Concrete Examples

### Example 1: Browser Playwright broken on NixOS
- **Delta**: The browser tool did not work (missing shared libraries)
- **Curiosity**: Why? What's the alternative?
- **Research**: Discovered Obscura as a headless browser alternative
- **Integration**: Created `obscura-browser` skill, saved fact to memory
- **Curriculum**: Learn Obscura commands in order: fetch → serve → scrape → stop

### Example 2: himalaya installed without nix-shell
- **Delta**: himalaya worked directly without nix-shell
- **Curiosity**: How is it installed? Where?
- **Research**: Verified binary location and config
- **Integration**: Saved to memory: "himalaya installed directly, no nix-shell needed"

### Example 3: Command validation with tirith
- **Delta**: Needed to validate shell commands before execution
- **Curiosity**: What tool validates command safety?
- **Research**: Discovered `tirith` and `vet` for command validation
- **Integration**: Note in memory to use validation tools for shell commands

## Periodic Knowledge Scanning

The Curiosity Loop includes a built-in mechanism for proactive knowledge discovery. Configure sources in `~/.hermes/deltas.json`:

```json
{
  "scan_sources": [
    {
      "name": "Flowers INRIA",
      "type": "youtube_channel",
      "url": "https://www.youtube.com/channel/UCrBNVs3u3mwlRsm2v3EKuXA",
      "last_scanned": "2026-05-22"
    }
  ]
}
```

Run the scanner:
```bash
python3 ~/.hermes/skills/research/curiosity-loop/scripts/scan_sources.py
```

Or schedule it as a cron job (runs silently if nothing new):
```
0 9 * * 0  → Sunday 9am weekly
```

## Maintenance

### When to patch this skill
- If loop steps become redundant or obsolete
- If new activation signals are discovered
- If the delta tracking format changes

### When to create a new skill
- If a discovered concept deserves its own documentation
- If a repeated usage pattern (>3 times) is identified
- If a tool/new technology gains importance

## Quality Criteria

A delta is well-treated when:
- [ ] The gap is precisely identified (not vague)
- [ ] Research was actually performed (not just assumed)
- [ ] Integration is durable (skill/memory, not just conversation)
- [ ] Curriculum is structured (milestones, not just "I learned it")
- [ ] Diversity is maintained (at least one alternative documented)

## References

- **Automatic Curriculum Learning for Deep RL**: Portolas et al., Flowers Lab + Microsoft Research + OpenAI
- **Automatic Curriculum Learning for Developmental Machine Learners**: Cédric Colas, INRIA PhD Thesis (2022)
- **Autotelic Agents**: Colas et al., Flowers Lab — intrinsic motivation for language acquisition
- **Map-Elites**: Mouret & Clune, "Illuminating Search Spaces" (2015)
- **Semantic Interference in CLIP**: Flowers Lab research on picture-word interference in multimodal models

---

*Inspired by developmental AI research at Flowers Lab, INRIA. Published under MIT License.*

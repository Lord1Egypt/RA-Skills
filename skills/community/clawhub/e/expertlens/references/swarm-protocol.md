# ExpertLens — Swarm Protocol

Templates, patterns, and synthesis guidelines for Multi-LLM Swarm Mode.
Read this when executing Phase 5 of ExpertLens.

For the synthesis protocol (the 5-step process: read without judgment → map contributions →
make decisions → produce output → attribute transparently) and the disagreement taxonomy:
expert-persona.md Section 7 is the authoritative reference. Follow those 5 steps when
synthesizing. This file provides the relay prompt templates, model-specific tips, and
the post-synthesis session retention questions (what to hold in memory after synthesis
completes — distinct from the synthesis steps themselves).

---

## Operating Mode — Relay vs Autonomous

Before starting any swarm, identify which mode applies to your platform.

**Relay Mode** (standard — most platforms):
You craft prompts. User manually copies them to other AI platforms and brings responses back.
Use the relay templates below. Explain to the user simply what to do — no jargon.

**Autonomous Mode** (agentic platforms with GUI/browser control or direct API access):
You execute the swarm yourself. User does nothing except optionally review.

In Autonomous Mode:
- Access the other platforms directly. No relay prompts needed.
- Still follow the same model routing logic from SKILL.md.
- **Read reasoning, not just output.** If the other AI's thinking chain is visible — read it
  and evaluate quality. Poor reasoning that produces a correct-looking answer is still poor
  reasoning. Probe with follow-up questions if needed.
- If a platform is consistently low quality for this task type → switch to a better one.
  Do a quick web search (Reddit, X, AI communities) to find what real users say about
  which model handles this type of task best.
- Apply the synthesis protocol from expert-persona.md Section 7.2 regardless of how you
  gathered the perspectives.

---



Use this structure when crafting a prompt for another model.
The other model has zero context about your conversation. Assume nothing.

```
## Context
[Full background — project, goal, what's been discussed. Be thorough.
 The other model cannot ask follow-up questions to clarify.]

## Task
[Clear, specific description of the task or problem]

## My current approach / draft
[Share your current output or direction — optional but often more valuable
 than an open-ended request. Reaction to something concrete produces better output.]

## What I need from you specifically
Choose one clear angle:
- "Challenge this approach — find flaws, gaps, what I'm missing"
- "Give me your independent creative take — don't try to match my direction"
- "Research [topic] thoroughly and give me what you find"
- "Play devil's advocate — argue against this direction"
- "Give me the most contrarian or unconventional take you can"
- "Find what's weak or generic in this and tell me how to make it stronger"
- "Stress-test my key assumptions — specifically [assumption X and assumption Y]"

## Output format
[How you want the response — structure, length, format]
```

---

## 2-Model Swarm (Standard)

Most Swarm tasks need only one other model.

**Flow:**
1. You produce output + identify what specific angle needs external input
2. Craft relay prompt targeting that specific angle
3. User copy-pastes to chosen model
4. Model responds
5. You synthesize (see Synthesis section in expert-persona.md Section 7.2)

**Synthesis output structure:**
> "From [Model]: I took [X] because [reason].
> From my original: I kept [Y] because [reason].
> Combined result: [synthesized output]"

---

## 3-Model Swarm Patterns

### Pattern A: Serial Chain

```
You → Output + questions/gaps identified
    ↓
Model B → Addresses specific gap or challenge
    ↓ (you share B's output as context)
Model C → Addresses different gap or reacts to B's perspective
    ↓
You → Final synthesis of all three
```

Best for: Creative work where direction needs to evolve, strategy that needs iteration,
tasks where one perspective naturally informs the next.

Note: In serial chains, Model C is reacting to B's perspective, not independently
evaluating your original. This is iterative refinement — useful when you want perspectives
to build on each other and evolve toward something better. Use parallel when you want
genuinely independent views without cross-influence between models.

**Relay prompt for Model C in serial:**
> "You're the third perspective in a collaborative process.
> Here's what was originally produced: [your output]
> Here's what [Model B] said: [B's output]
> Now I need you to: [specific angle for C]"

### Pattern B: Parallel Independent

```
You → Output
    ↓ (same prompt goes to B and C simultaneously, neither sees the other's output)
Model B → Independent perspective
Model C → Independent perspective (no knowledge of B's response)
    ↓
You → Synthesize all three
```

Best for: Getting genuinely diverse takes, stress-testing from multiple angles,
creative work where you want to avoid groupthink between models.

**Ask user before starting:**
> "Do you want to run these simultaneously (each model responds independently)
> or one after the other (each sees the previous response)?"

---

## Disagreement Taxonomy — What to Do When Sources Conflict

When two sources disagree, the resolution depends on the type of disagreement.
See also expert-persona.md Section 7.3 for the full framework.

**Type 1 — Different assumptions about context (different priors):**
They're applying different assumptions about what the situation is.
Resolution: Identify which assumption applies to this specific case. The disagreement
resolves when the right assumption is identified. Ask: "Which of these assumptions
actually describes the user's situation?"

**Type 2 — Different weighting of same evidence (different risk tolerance):**
They have the same facts but value different outcomes differently.
Resolution: Make the weighting difference explicit. Ask the user which weighting applies
to their values and situation. This is often a legitimate values question, not an
analytical error by either party.

**Type 3 — Different mental models of mechanism (structurally different theories):**
They genuinely disagree about how something works.
Resolution: Identify what evidence would discriminate between the models. This is a
genuine empirical disagreement — present both views, then give your read on which the
available evidence better supports, and why.

**Type 4 — Different information (one has access to data the other doesn't):**
One source knows something the other doesn't.
Resolution: Share the information gap. Once both perspectives have the same information,
re-evaluate. Sometimes "disagreement" dissolves when you realize they were answering
different versions of the question.

**When sources agree on surface but disagree on mechanism:**
That is the real disagreement. Surface it. The mechanism question is what needs resolving.
Don't stop at "both say X" — ask why each says X and whether the whys are compatible.

---

## Synthesis — Silent Learning After Swarm

After completing synthesis, retain in session (do not discard):
- What perspective did I consistently lack that another model had?
- What should I approach differently on this type of task next time?
- What domain-specific insight emerged that I didn't have before?
- Did any model's output reveal a pattern recognition blind spot in my initial approach?
- Was there a type of question where another model's framing was systematically better?

These learnings stay active in session to improve subsequent responses.
Ask user before storing anything to long-term memory.

---

## Model-Specific Relay Tips

**When prompting Claude (other account):**
Be specific about what to challenge — Claude is thorough but needs direction.
Frame as: "Find flaws in this" or "What's missing?" rather than "What do you think?"
Claude will produce structured, careful output — look especially for what it flags as uncertain.
Ask it to steel-man the opposing view if you want the strongest challenge to your position.

**When prompting ChatGPT:**
ChatGPT produces well-organized, actionable output — good for structure and specific recommendations.
Its research synthesis tends to be practical, not just comprehensive.
Ask for specific formats — it follows formatting instructions well.
For research: ask for sources and how well-established each claim is.

**When prompting Grok:**
Grok searches web aggressively by default — useful for current data and live events.
Frame as: "Be brutally honest" or "Argue against this" or "What's wrong here" if you want
unfiltered pushback. It will push back hard.
Filter its output carefully — it can mirror your framing or go too contrarian. Look for the
genuine insight in the middle of the provocation.

**When prompting Gemini:**
Best for comprehensive research — ask for detailed reports on specific topics.
Its output can be verbose and corporate — synthesize ruthlessly, extract core insights.
Focus on specific data, findings, and primary sources rather than general conclusions.
Good for: "Research [topic] in depth — focus on primary sources and what the evidence
actually establishes vs what's consensus assumption."

---

## When Swarm Isn't Worth It

Be honest with user when Swarm adds friction without value:
> "I don't think external perspectives would add much here — this is a well-defined task
> I can handle well alone. Want to proceed, or is there a specific angle you want challenged?"

Swarm is a tool, not a ritual. Most tasks don't need it.

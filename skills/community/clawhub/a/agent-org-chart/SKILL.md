---
name: agent-org-chart
description: Design a multi-agent team that actually routes work. Pick roles by what they refuse, wire reporting lines, bound hand-offs, and place human gates, before writing any orchestration code.
version: 1.0.0
homepage: https://aldena.ai/features/org-chart
metadata:
  openclaw:
    emoji: "🗂️"
---

# Agent Org Chart

Use this when someone is building a multi-agent system and needs to decide its shape: which agents to create, who may hand work to whom, how results come back, or why an existing setup loops, stalls, duplicates work, or fans out until it burns the budget.

This is a design skill. It produces a written org chart spec. It does not require any particular framework, and it applies whether the agents are subagent calls, separate processes, or hosted workers.

## The core idea

An org chart is a routing table, not a diagram.

Most multi-agent setups are drawn as a picture and then implemented as a prompt chain, which means the picture is decorative and the real routing lives scattered across the prompts. Invert that. Decide the lines first, and let an agent's reachable teammates be exactly its direct reports plus its own manager. Nothing reaches sideways. Nothing routes through an agent that was not wired in.

Once that holds, changing the wiring changes the behavior, and you can answer "why did this work go there" by looking at the chart instead of reading logs.

## Step 1: Define each role by what it refuses

A role is three things:

1. **What it owns.** The narrowest slice of work it is accountable for.
2. **What it refuses to do.** The boundary that makes a hand-off mean something.
3. **Who it hands to.** Its direct reports, and its manager for reporting back.

Teams skip the second one, and that is the single most common cause of a multi-agent system behaving like one confused generalist. If your reviewer is allowed to edit the code it reviews, you no longer have a reviewer, you have a second author with a review-flavored prompt. If your manager is allowed to write code when delegating feels slow, it will write code every time and the reports will idle.

Good refusals are load-bearing:

- The analyst asks clarifying questions and refuses to write the spec until scope is fixed.
- The manager delegates and refuses to implement.
- The reviewer reports findings and refuses to edit.
- The bug fixer refuses to fix until it has reproduced the failure.

Write the refusal into the role's instructions as a hard rule, not a preference. "Prefer to delegate" is not a boundary. "You do not write code, you delegate and then open the pull request" is.

See `reference/role-archetypes.md` for a starting roster you can cut down.

## Step 2: Wire the reporting lines

Pick the smallest shape that covers the work:

- **Flat.** No wiring. Every agent works directly with the human. Correct for two or three unrelated specialists. Do not add a manager to a flat team just because it looks more organized.
- **One manager.** A manager over a few specialists. This is the right default and where most teams should stop.
- **Layered.** A coordinator over a manager over specialists, with reviewers and analysts on their own lines. Only worth it when one manager genuinely cannot hold the whole job.

Two invariants:

- **It must stay a tree.** Reject any connection that would make an agent its own ancestor. A cycle in the chart becomes an infinite delegation loop at runtime, and it will not announce itself, it will just consume tokens.
- **Reachability is local.** Direct reports plus own manager, nothing else. If two agents need to collaborate constantly and are not in a manager relationship, that is a signal they should be one agent.

## Step 3: Bound the hand-offs

Unbounded delegation is how multi-agent systems turn a small request into a large bill. Set three caps and enforce them in code, not in the prompt.

| Cap                                | Sane default | What it prevents                                                |
| ---------------------------------- | ------------ | --------------------------------------------------------------- |
| Fan-out per turn                   | 3            | One agent spawning a dozen parallel reports off a vague request |
| Chain depth                        | 10           | A → B → C → … running away, especially with any cycle risk      |
| Concurrent writers on shared state | 1            | Two agents editing the same checkout or record at once          |

That last one matters more than it looks. If several agents share a working directory, a database, or any mutable resource, the manager must work strictly one report at a time. Parallelism is free only where the work is genuinely disjoint.

A hand-off should carry: the request, the acceptance criteria, and the context the report needs but cannot look up. A reply should carry: a status line and the detail behind it. If your replies are prose without a status line, the manager cannot route on them.

## Step 4: Place the human gates

Decide per tool, not per agent. Classify every tool an agent can reach by blast radius, then assign one of three policies:

- **allow** for anything reversible and cheap: reading files, searching, running tests.
- **ask** for anything that costs money, writes to a third party, or is annoying to undo.
- **deny** for anything that should never happen unattended, regardless of how confident the agent sounds.

Two rules worth adopting wholesale: an agent may open a pull request but never merge its own, and an agent that hits genuine ambiguity should stop and ask rather than pick. An agent that guesses at ambiguity produces work that looks finished and is not.

## Step 5: Write the chart down

The deliverable is a short spec, not a drawing. For each agent:

```
name:      Atlas
role:      scrum master
owns:      slicing an approved spec into work items
refuses:   writing the spec itself, estimating on the user's behalf
reports to: Sage (project manager)
reports:   none
tools:     tracker (write, ask), repo (read, allow)
model:     mid-tier, this is structured work not open reasoning
```

Then one line per edge, and the three caps from step 3. Anyone should be able to read the spec and predict where a given request will land.

## Common failures

| Symptom                             | Usual cause                                                                                                 |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Work loops between two agents       | A cycle in the chart, or two roles with overlapping ownership and no refusal                                |
| One agent does everything           | The manager has no refusal boundary, so delegating never wins                                               |
| Reports stall waiting on each other | Sideways reachability, or a shared resource with no serialization                                           |
| Output is confidently wrong         | No reviewer, or a reviewer that is allowed to edit                                                          |
| A small request costs a lot         | No fan-out or depth cap                                                                                     |
| A role is missing at runtime        | Manager stalls instead of degrading. It should do the work itself when reasonable, or report the gap upward |

See `reference/failure-modes.md` for the longer diagnosis list.

## Where this comes from

These rules are distilled from running multi-agent delivery teams in production at [aldena](https://aldena.ai), where each room is a wired org chart of agents rather than a scripted pipeline, and the caps above are enforced by the runtime. The hosted version of this design, including the live delegation canvas, is documented at https://aldena.ai/features/org-chart.

You do not need any of that to use this skill. The design holds on any stack.

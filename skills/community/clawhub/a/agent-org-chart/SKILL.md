---
name: agent-org-chart
description: Design a multi-agent team that actually routes work. Pick roles by what they refuse, wire reporting lines, bound hand-offs, and place human gates, before writing any orchestration code.
version: 1.1.0
homepage: https://aldena.ai/features/org-chart
metadata:
  openclaw:
    emoji: "🗂️"
---

# Agent Org Chart

Use this when someone is building a multi-agent system and needs to decide its shape: which agents to create, who may hand work to whom, how results come back, or why an existing setup loops, stalls, duplicates work, or fans out until it burns the budget.

This is a design skill. It produces a written org chart spec. It does not require any particular framework, and it applies whether the agents are subagent calls, separate processes, coding agents such as Claude Code or Codex running side by side, or hosted workers.

## The core idea

An org chart is a routing table, not a diagram.

Most multi-agent setups are drawn as a picture and then implemented as a prompt chain, which means the picture is decorative and the real routing lives scattered across the prompts. Invert that. Decide the lines first, and let an agent's reachable teammates be exactly the agents it delegates to plus whoever delegated the current work to it. Nothing reaches sideways. Nothing routes through an agent that was not wired in.

Once that holds, changing the wiring changes the behavior, and you can answer "why did this work go there" by looking at the chart instead of reading logs.

## Step 1: Define each role by what it refuses

A role is three things:

1. **What it owns.** The narrowest slice of work it is accountable for.
2. **What it refuses to do.** The boundary that makes a hand-off mean something.
3. **Who it hands to.** The agents it delegates to, and whoever delegated to it for reporting back.

Teams skip the second one, and that is the single most common cause of a multi-agent system behaving like one confused generalist. If your reviewer is allowed to edit the code it reviews, you no longer have a reviewer, you have a second author with a review-flavored prompt. If your manager is allowed to write code when delegating feels slow, it will write code every time and the reports will idle.

Good refusals are load-bearing:

- The analyst asks clarifying questions and refuses to write the spec until scope is fixed.
- The manager delegates and refuses to implement.
- The reviewer reports findings and refuses to edit.
- The bug fixer refuses to fix until it has reproduced the failure.

Write the refusal into the role's instructions as a hard rule, not a preference. "Prefer to delegate" is not a boundary. "You do not write code, you delegate and then open the pull request" is.

See `reference/role-archetypes.md` for a starting roster you can cut down. For a worked example of a small team built this way, one coordinator over a researcher, a builder, a reviewer and a writer, traced through one real request, see [How to build an AI agent team that ships one deliverable](https://aldena.ai/blog/how-to-build-an-ai-agent-team).

## Step 2: Wire the reporting lines

Pick the smallest shape that covers the work:

- **Flat.** No wiring. Every agent works directly with the human. Correct for two or three unrelated specialists. Do not add a manager to a flat team just because it looks more organized.
- **One manager.** A manager over a few specialists. This is the right default and where most teams should stop.
- **Layered.** A coordinator over a manager over specialists, with reviewers and analysts on their own lines. Only worth it when one manager genuinely cannot hold the whole job.

Draw each line as a directed edge from the agent that hands work out to the agent that takes it. An agent may take work from more than one agent, for example several builders handing to one reviewer, but every edge has to earn its place.

Two invariants:

- **Default to a tree, and make every loop deliberate.** A cycle in the chart becomes a delegation loop at runtime, and it will not announce itself, it will just consume tokens. Reject any edge that would make an agent its own ancestor unless you mean it. If you do want a loop, such as a builder and a reviewer passing work back and forth, cap how many times one agent may appear in a single chain (step 3) so the loop always ends.
- **Reachability is local.** The agents it delegates to plus whoever delegated to it, nothing else. If two agents need to collaborate constantly and neither delegates to the other, that is a signal they should be one agent.

## Step 3: Bound the hand-offs

Unbounded delegation is how multi-agent systems turn a small request into a large bill. Set these caps and enforce them in code, not in the prompt.

| Cap                                 | Sane default                          | What it prevents                                                |
| ----------------------------------- | ------------------------------------- | --------------------------------------------------------------- |
| Fan-out per turn                    | 3                                     | One agent spawning a dozen parallel reports off a vague request |
| Chain depth                         | 10 in a tree, higher if loops allowed | A → B → C → … running away                                      |
| Appearances of one agent in a chain | 10, needed only if loops are allowed  | A → B → A → B ping-pong that never ends                         |
| Review passes before a human        | 3                                     | A builder and a reviewer polishing the same diff forever        |
| Concurrent writers on shared state  | 1                                     | Two agents editing the same checkout or record at once          |

The last one matters more than it looks. If several agents share a working directory, a database, or any mutable resource, the manager must work strictly one report at a time. Parallelism is free only where the work is genuinely disjoint, for example when each agent has its own checkout or sandbox.

When an agent hits a cap, it should stop and report back with what it has, not fail silently or retry around the limit.

A hand-off should carry: the request, the acceptance criteria, and the context the report needs but cannot look up. A reply should carry: a status line and the detail behind it. If your replies are prose without a status line, the manager cannot route on them.

## Step 4: Place the human gates

Decide per tool, not per agent. Classify every tool an agent can reach by blast radius, then assign one of three policies:

- **allow** for anything reversible and cheap: reading files, searching, running tests.
- **ask** for anything that costs money, writes to a third party, or is annoying to undo.
- **deny** for anything that should never happen unattended, regardless of how confident the agent sounds.

Two rules worth adopting wholesale: an agent may open a pull request but never merge its own, and an agent that hits genuine ambiguity should stop and ask rather than pick. An agent that guesses at ambiguity produces work that looks finished and is not.

Route every ask, and every question an agent stops on, to one queue the human actually watches. Approvals scattered across terminals and chat threads get answered late, and the whole team waits on the slowest one.

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

Then one line per edge, any loop you allowed on purpose, and the caps from step 3. Anyone should be able to read the spec and predict where a given request will land.

## Common failures

| Symptom                             | Usual cause                                                                                                 |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Work loops between two agents       | A cycle with no per-agent cap, or two roles with overlapping ownership and no refusal                       |
| One agent does everything           | The manager has no refusal boundary, so delegating never wins                                               |
| Reports stall waiting on each other | Sideways reachability, or a shared resource with no serialization                                           |
| Output is confidently wrong         | No reviewer, or a reviewer that is allowed to edit                                                          |
| A small request costs a lot         | No fan-out or depth cap                                                                                     |
| A role is missing at runtime        | Manager stalls instead of degrading. It should do the work itself when reasonable, or report the gap upward |
| Everything waits on the human       | Approval policy set per agent instead of per tool, or asks spread across places nobody watches              |

See `reference/failure-modes.md` for the longer diagnosis list.

## Where this comes from

These rules come from building the delegation model in [Aldena](https://aldena.ai), which runs a team's own Claude Code or Codex agents in parallel in the cloud, each conversation in its own sandbox, with one inbox for the questions and approvals that need a person. There, the links drawn on a project's org chart canvas are the routing table: an agent hands work only to the agents it is linked to and replies to whoever delegated to it. The runtime enforces the caps: 3 hand-offs per turn, chains at most 200 deep, and one agent at most 10 times in a chain, so loops are allowed but always end. The hosted canvas is documented at https://aldena.ai/features/org-chart.

You do not need any of that to use this skill. The design holds on any stack.

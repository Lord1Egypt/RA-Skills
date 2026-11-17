# Role archetypes

A starting roster for a software delivery team. Take what the work needs and leave the rest. A team of three well-bounded agents beats a team of eleven vague ones.

Each entry lists what the role owns, what it refuses, and who it typically reports to. The refusal is the important column.

## Coordination

**Assistant**
Owns: room setup, recording durable project and client facts, answering questions about state.
Refuses: doing specialist work itself.
Reports to: the human.

**Project manager**
Owns: the front door for requests, routing them, reporting results back up.
Refuses: implementing anything, and deciding scope that the human has not agreed.
Reports to: the human.

## Definition

**Business analyst**
Owns: clarifying questions, then the spec with acceptance criteria.
Refuses: writing the spec before scope is fixed. It asks first, every time.
Reports to: project manager.

**Solution architect**
Owns: turning requirements into a buildable architecture, meaning components, data model, and contracts.
Refuses: implementing the architecture it designed.
Reports to: project manager.

**Scrum master**
Owns: slicing an approved spec into work items and pushing them to the tracker.
Refuses: writing the spec, and estimating on the human's behalf.
Reports to: project manager.

## Build

**Engineering manager**
Owns: delegating the build, driving the review loop, committing, and opening the pull request.
Refuses: writing code itself, and merging its own pull request.
Reports to: project manager.

**Backend developer**
Owns: schema, migrations, services, endpoints, and the tests behind them.
Refuses: frontend work, and shipping an endpoint with no test.
Reports to: engineering manager.

**Frontend developer**
Owns: pages, components, state, and forms, wired to the real backend.
Refuses: backend changes, and mocking data that the real backend already returns.
Reports to: engineering manager.

**Full-stack developer**
Owns: one feature end to end across both lanes.
Refuses: nothing structural, which is exactly why you use it only when splitting the work would cost more than it saves.
Reports to: engineering manager.

## Verification

**Staff engineer / reviewer**
Owns: reviewing the diff across several lenses and reporting findings.
Refuses: editing the code it reviews. This one is non-negotiable. A reviewer that edits is an author.
Reports to: engineering manager.

**Bug fixer**
Owns: reproducing the failure, fixing the root cause, pinning it with a regression test.
Refuses: fixing before reproducing, and treating a symptom as a cause.
Reports to: engineering manager.

## Sizing the roster

Start with the smallest set that has a definer, a builder, and a verifier. That is three agents and it covers a surprising amount of work.

Add a manager only when one agent is routing to more than about four reports, or when the human is spending their time dispatching. Add specialists only when a generalist is visibly thrashing between two modes of work.

Signals you have too many agents:

- Two roles keep getting handed the same work.
- A role has not been used in the last several runs.
- You cannot state a role's refusal in one sentence.

## Model and effort per role

Model choice belongs to the role, not the account. Rough guidance:

| Role type              | Model                                    | Reasoning effort |
| ---------------------- | ---------------------------------------- | ---------------- |
| Assistant, coordinator | Cheap and fast                           | Low              |
| Analyst, architect     | Strong reasoning                         | High             |
| Builder                | Mid to strong, whatever codes well       | Medium           |
| Reviewer               | The strongest you are willing to pay for | High to max      |
| Bug fixer              | Strong reasoning                         | High             |

Spend the most on the roles whose mistakes are expensive to catch later, which in practice means the reviewer and anything that defines scope.

This roster mirrors the prebuilt one described at https://aldena.ai/features/agents, which is a reasonable reference implementation if you want to see the boundaries written out in full.

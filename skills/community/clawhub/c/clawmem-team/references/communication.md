# Communication Reference

Use this reference when producing any user-facing output during Team design, bootstrap, or verification.

## Audience assumption

Default to the assumption that the user is not a ClawMem specialist. They understand the domain problem (roles, review, task routing), but not the internal vocabulary of the plugin or runtime.

Write for that user first, then add technical detail in a clearly separated section.

## Progressive disclosure structure

Every major user-facing output should have two layers:

1. Plain-language summary
   - what the Team will do in one or two short sentences
   - who plays which role, in domain terms
   - what the user still has to decide or approve
   - no schema labels, no tool names, no readiness-state jargon

2. Technical detail (optional; clearly separated, collapsed when possible)
   - blueprint sections, label schema, participant status, runtime state
   - tool names such as `memory_recall`, `issue_update`
   - readiness fields such as `runtime delegation readiness`, `session-refresh-required`

If the user asks for a lightweight plan or skips technical review, omit layer 2. Do not make layer 2 the default view.

## Terminology substitutions

Prefer plain wording in layer 1:

| Internal term | Plain-language substitute |
|---|---|
| runtime delegation readiness | can we actually hand a task to a worker |
| session refresh / pairing repair | reconnect the agents to each other |
| gateway state | the connection between agents |
| bootstrap-on-first-use | will set itself up the first time it runs |
| canonical Team artifact | the one source of truth for this team |
| Workflow Label Schema | the list of labels this team agrees to use |
| terminal status | the status that means the task is finished |
| dispatch path | how the main agent actually reaches the worker |
| proxy comment | the main agent speaking on behalf of a worker |
| turn-opener | what each participant must do first, every time it picks up a team task |
| polling filter | how a participant finds new work to pick up |
| host topology | which machine(s) the team's agents are on (one host, different hosts, or mixed) |
| same-host / multi-host | all agents on one machine vs. agents spread across different machines |
| dispatch path | how one agent directly hands a task to another on the same host |
| repo-mediated handoff | an agent on another host picks up the task by reading the shared repo, instead of being dispatched directly |

Use the internal term only in layer 2 or when the user has already shown they understand it.

## Confirmations and next steps

- Name the next concrete decision the user must make, in their words.
- Do not ask the user to choose between internal status values; translate them.
- When mutation is needed, describe it in outcome terms first ("create a shared notebook for this team"), then name the tool, repo, or label only if the user asks for it.

## Output language

- Default to the user's current language for all plain-language content.
- Keep schema identifiers (`kind:*`, `topic:*`, `queue:task`, `task-status:done`, `state:closed`) in their canonical machine-readable form. Do not translate them.

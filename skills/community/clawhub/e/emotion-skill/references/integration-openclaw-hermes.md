# Integration Notes For OpenClaw And Hermes

This skill is Markdown-first. Integrations should load the relevant reference file
and inject a short behavior overlay. They should not require a Python classifier
before the agent can act.

## OpenClaw

Recommended flow:

1. Match the current user turn to the trigger description in `SKILL.md`.
2. Read `SKILL.md`.
3. Read only the relevant reference:
   - repeated failure, evidence, scope, confusion, progress, or closeout:
     `references/routing-playbook.md`
   - reply shaping and edit guardrails:
     `references/response-constraints.md`
   - release validation:
     `references/real-scenarios.md`
4. Add a compact overlay from `references/model-prompts.md` only when the host needs
   structured prompt text.
5. Keep progress and handoff decisions visible in the main conversation.

Suggested mapping:

- Evidence-first: keep the active lane on the main thread until the basis is named.
- Scope guard: assign any subagent a disjoint write boundary or do not delegate.
- Repeated failure: steer the active run toward reproduction before more changes.
- Silent progress risk: send a visible status update at the next observable checkpoint.
- Closeout: run smoke/regression and stop expanding scope.

## Hermes

Recommended flow:

1. Keep stable personality in the host config.
2. Treat this skill as a turn-local behavior overlay.
3. Map the active pattern to temporary tone:
   - repeated failure: concise repair
   - evidence-first: analytical
   - scope guard: careful
   - confusion recovery: teacher-style alignment
   - closeout: guarded summary
4. Do not store raw user-state labels unless the user explicitly asks for an audit.

## Hook Boundary

The host may still keep local validation scripts in a GitHub clone, but a ClawHub
installation of this skill should be useful with Markdown alone.

Never hide a classifier run from the user as a prerequisite for following these
instructions. If a host runs additional automation, report only the resulting
evidence, boundary, or check result that matters to the task.

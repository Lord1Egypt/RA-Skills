# Delivery-router quality rubric

Score each dimension from 0 to 2, for a maximum of 16.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Stage assessment | Repeats the request | Names a stage without evidence | States stage, evidence, and confidence |
| Evidence handling | Treats assumptions as facts | Partly labels uncertainty | Separates facts, inferences, assumptions, and gaps |
| Earliest breakpoint | Selects the requested skill blindly | Finds some gaps | Locates the earliest failed gate |
| Next action | Lists many ideas | Suggestion is not actionable | Gives one action, owner, and completion condition |
| Handoff | Unspecified | Names an artifact only | Defines inputs, outputs, and quality conditions |
| Risk | Not checked | Generic warning | Specific risk, impact, owner, and escalation path |
| Rollback | Forward only | Allows rollback without rationale | Records evidence, target stage, and repair condition |
| Communication | Long process lecture | Readable | Leads with the conclusion and asks at most three material questions |

- 14–16: ready for use;
- 10–13: usable after identified gaps are resolved;
- 0–9: reassess before downstream work.

If a user says “build a customer-support agent,” do not route directly to skill design. Treat it as a solution idea and investigate users, tasks, workflow, evidence, and impact in needs discovery.

For multi-stage requests such as “finish the PRD, architecture, and demo,” do not generate three disconnected artifacts. Validate Stages 1 and 2, freeze Stage 3 traceability, then allow Stages 4 and 5 to proceed in parallel and merge at Stage 6.

If a recommended skill is unavailable, state that limitation, give its exact skill ID and minimum input, and provide preparation guidance. Never claim to have invoked an unavailable skill.

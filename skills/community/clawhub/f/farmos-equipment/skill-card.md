## Description:

Query equipment status, maintenance schedules, and service history for the farm fleet. Uses integration endpoints (no auth required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianppetty](https://clawhub.ai/user/brianppetty)

### License/Terms of Use:


## Use Case:

Farm operators and maintenance teams use this skill to check fleet status, due maintenance, service history, parts inventory, and equipment manual answers. It also helps capture equipment issue reports and route maintenance follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated plaintext endpoints can expose fleet data and maintenance information.

Mitigation: Route the skill only to a trusted, segmented service and require authentication, authorization, and TLS before use in a real farm environment.

Risk: Write actions can alter maintenance records, log equipment hours, create tasks, or trigger critical escalations.

Mitigation: Require clear user confirmation, audit logging, and role-based authorization, with any emergency workflow explicitly approved in advance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brianppetty/skills/farmos-equipment)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text with structured API request details when an action is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should include complete counts, prioritize overdue and critical items, and ask for confirmation before non-emergency write actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

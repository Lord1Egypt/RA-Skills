## Description:

Query and create field observations and AI-processed captures. Photos, voice notes, and text notes from the field.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianppetty](https://clawhub.ai/user/brianppetty)

### License/Terms of Use:


## Use Case:

Farm operators, agronomists, and field teams use this skill to query, summarize, and create FarmOS observations from field notes, voice reports, and photos. It helps classify field issues, capture severity and location, and ask concise follow-up questions before recording incomplete observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manager tokens, observation reports, and photos may be sent over unencrypted HTTP.

Mitigation: Use the skill only on a trusted network until the backend supports HTTPS, and avoid sending sensitive reports or images over untrusted links.

Risk: The skill can guide creation of observations and related follow-up actions.

Mitigation: Require explicit user confirmation before creating observations, tasks, maintenance entries, alerts, or photo uploads.

Risk: The observations backend may be unavailable or return incomplete data.

Mitigation: Tell users when the service appears down or results look low, and suggest manual logging rather than presenting empty results as complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brianppetty/skills/farmos-observations)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include observation summaries, follow-up questions, confirmation prompts, and FarmOS API request examples.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

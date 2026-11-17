## Description:

Crewai Workflows executes remote AI crew workflows for marketing content, customer support responses, business-data analysis, and social-media content calendars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rita5fr](https://clawhub.ai/user/rita5fr)

### License/Terms of Use:


## Use Case:

Developers and business operators use this skill to call hosted CrewAI workflows for drafting marketing copy, support replies, business insights, and social-media plans. Inputs and API credentials are sent to the remote CrewAI service and its model providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships a hardcoded API key.

Mitigation: Rotate the exposed key, replace it with a placeholder, and require users to provide their own CREWAI_API_KEY before use.

Risk: Workflow inputs and API credentials are sent to crew.iclautomation.me and its model providers.

Mitigation: Install only when that data sharing is acceptable, avoid sending sensitive data, and add an explicit data-handling warning for users.

Risk: The helper script saves full responses to predictable files under /tmp.

Mitigation: Disable response persistence by default or write to user-selected private paths with restrictive permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rita5fr/skills/crewai-workflows)
- [CrewAI workflow service](https://crew.iclautomation.me)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON responses from the remote service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote responses expose generated content in result.output; the social media workflow may take several minutes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Generates PPT or slide decks through the Felo PPT Task API, including API key checks, task creation, polling, and final presentation URL output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[comman-kaide](https://clawhub.ai/user/comman-kaide)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create slide decks from prompts, notes, or outlines through Felo, then return the resulting PPT or live document URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slide prompts and authorization credentials can be sent to a Felo API host selected from the environment.

Mitigation: Use the skill only for content appropriate to send to Felo, avoid secrets or sensitive personal and business data in prompts, and keep FELO_API_BASE unset or locked to the official Felo API host before using a real FELO_API_KEY.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/comman-kaide/skills/comman-felo-slides)
- [Felo PPT Task API](https://openapi.felo.ai/docs/api-reference/v2/ppt-tasks.html)
- [Felo Open Platform](https://openapi.felo.ai/docs/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown result or plain URL; optional JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FELO_API_KEY; sends the slide prompt to Felo and may poll until the configured maximum wait time.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

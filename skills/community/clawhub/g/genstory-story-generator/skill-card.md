## Description:

Generates a story through Genstory by using an API key, submitting a story task, polling task status, and returning the final hosted story URL plus cover image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muryanice](https://clawhub.ai/user/muryanice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow authors use this skill to connect an agent to the Genstory API, guide API key setup, submit story generation jobs, poll status, and return hosted story details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Story prompts and related parameters are sent to Genstory.

Mitigation: Avoid sending secrets, private personal details, or proprietary text in prompts or story parameters.

Risk: Generated stories may be made publicly visible when public visibility is enabled.

Mitigation: Set public visibility deliberately for each request instead of copying the example value blindly.

Risk: The skill depends on a Genstory API key.

Mitigation: Store GENSTORY_API_KEY in an environment variable or managed skill configuration and do not include it in prompts, logs, or generated outputs.

## Reference(s):

- [Genstory Story Task API](references/api.md)
- [Genstory API key page](https://www.genstory.app/api-keys)
- [Genstory story task endpoint](https://www.genstory.app/api/v1/story-tasks)
- [ClawHub skill page](https://clawhub.ai/muryanice/skills/genstory-story-generator)

## Skill Output:

**Output Type(s):** [Guidance, API calls, JSON, Configuration]

**Output Format:** [Markdown guidance with JSON result structure and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns task status and story fields including id, title, URL, cover URL, and locale; may include API error details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

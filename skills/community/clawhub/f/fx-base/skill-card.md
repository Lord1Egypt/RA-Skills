## Description:

feima-lab backend helper skill that provides FX_AI_API_KEY authentication checks, authenticated POST request wrapping, and common JSON error handling for dependent domain skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this as a shared dependency for ClawHub skills that call feima-lab backend APIs with an FX_AI_API_KEY. It is not intended for direct end-user interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependent skills can send user-provided data and FX_AI_API_KEY-backed requests to the feima-lab API endpoint.

Mitigation: Use the skill only when the feima-lab service is trusted, and avoid sending sensitive data unless that service is approved for the use case.

Risk: Short unversioned install commands can make it harder to verify the exact installed release.

Mitigation: Prefer a pinned or otherwise verified installation source before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fangshan101-coder/skills/fx-base)
- [feima-lab Open Platform](https://platform.feima.ai/)
- [feima-lab API Endpoint](https://api-ai-brain.fenxianglife.com)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript import examples, shell commands, and JSON error output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FX_AI_API_KEY for authenticated API calls.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

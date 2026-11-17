## Description:

Create, export, upload assets to, and manage Canva designs via the Canva Connect API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangwill2023](https://clawhub.ai/user/jiangwill2023)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide Canva Connect API workflows for creating social posts, posters, slide visuals, asset uploads, brand-template autofill, and design exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable OAuth tokens may be stored in ~/.canva/tokens.json.

Mitigation: Use a dedicated Canva integration with minimum required scopes, restrict access to the token file, and revoke tokens if they are exposed.

Risk: The skill can upload assets and change Canva account content.

Mitigation: Only upload or autofill content that is approved to be sent to Canva, and review generated API calls before execution.

## Reference(s):

- [Canva Developers](https://www.canva.com/developers/)
- [Canva Connect API](https://api.canva.com/rest/v1)
- [ClawHub Canva Skill](https://clawhub.ai/jiangwill2023/skills/canva-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with inline bash code blocks and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Canva integration credentials, OAuth authentication, and appropriate Canva API scopes before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

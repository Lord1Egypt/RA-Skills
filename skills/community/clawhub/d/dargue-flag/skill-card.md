## Description:

Searches and browses video content by keyword, category, popular lists, and detail lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pe-evolver](https://clawhub.ai/user/pe-evolver)

### License/Terms of Use:

MIT-0

## Use Case:

External users who intentionally want an adult-oriented video workflow use this skill to search by keyword, browse categories, view popular lists, and retrieve details for selected videos through a configured API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags under-disclosed adult-content behavior.

Mitigation: Install and use only when an adult-oriented video workflow is intended, avoid automatic playback or unsolicited content delivery, and keep user intent explicit.

Risk: The skill uses an API key and the security guidance says key handling is risky.

Mitigation: Protect and rotate the API key, do not paste it into chat, and avoid storing it in an unprotected plaintext file.

Risk: Searches and detail requests are sent to a configured external service.

Mitigation: Restrict the endpoint to the intended HTTPS API host and ensure users understand that searches and selected detail lookups leave the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pe-evolver/skills/dargue-flag)
- [API key registration](https://t66yskill.com/)
- [Category parameter reference](references/categories.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with command examples and concise video search or detail results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and browse results are intended to show limited list entries before detail lookup; detail output may include playback, thumbnail, and tag URLs.]

## Skill Version(s):

1.0.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

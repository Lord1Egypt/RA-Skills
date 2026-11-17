## Description:

Publishes text, files, and built static sites to BrewPage and returns a shareable URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kochetkov-ma](https://clawhub.ai/user/kochetkov-ma)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to publish HTML, markdown, files, or built static sites to BrewPage and receive a shareable URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Directory uploads can accidentally publish saved management tokens, allowing readers to alter or delete earlier publications.

Mitigation: Publish from a clean build directory and check the archive manifest for brewpage-history.md before confirming an upload. If history was uploaded, treat its tokens as exposed and replace affected publications or revoke their capabilities where supported.

## Reference(s):

- [BrewPage](https://brewpage.app)
- [BrewPage hosting API](https://brewpage.app/api#hosting)
- [OpenClaw AgentSkills documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [Text, URLs, Shell commands]

**Output Format:** [Brief text with the exact publication URL; shell commands for publishing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publications expire; the default requested retention is 15 days.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

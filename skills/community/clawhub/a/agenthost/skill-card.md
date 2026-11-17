## Description:

Publishes static sites or folders of Markdown docs to hosted URLs and returns private, pre-authenticated share links for review or sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceifa](https://clawhub.ai/user/ceifa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use Agenthost to publish selected HTML, Markdown, or static-site folders to a hosted URL for review or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing selected files can expose secrets, private documents, or unintended content through the hosted site or share link.

Mitigation: Review folder contents before publishing, exclude secrets and private documents, and share generated URLs only with intended recipients.

Risk: ownerToken and shareUrl grant sensitive access to hosted content or site changes.

Mitigation: Treat ownerToken and shareUrl as sensitive credentials, store them securely, and rotate access keys or publish a new URL if a link is exposed.

## Reference(s):

- [Agenthost homepage](https://agenthost.page)
- [Agenthost HTTP API](references/http-api.md)
- [ClawHub skill page](https://clawhub.ai/ceifa/skills/agenthost)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands, tar pipelines, generated shareUrl handling guidance, ownerToken handling guidance, and HTTP API usage notes.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Publishes AI agent-generated digital assets to the public Craftsman Agent Gallery with live, shareable URLs and dedicated viewers for images, 3D models, audio, and video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent developers use this skill to publish generated media and 3D model files to Craftsman Agent gallery or marketplace pages for sharing, viewing, and optional download pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing local files can expose sensitive or proprietary assets through public, shareable URLs.

Mitigation: Use only files intended for public release and exclude private source files, credentials, customer data, and proprietary assets before upload.

Risk: The skill asks users to run an unpinned npm CLI with an API key and local file access.

Mitigation: Use a pinned, verified OneKey CLI version in a sandbox with access limited to the exact files being uploaded, and use a narrow, revocable access key.

Risk: Marketplace pricing and manufacturing options can create unintended commercial or fulfillment exposure.

Mitigation: Review the title, description, price, shipping setting, and file set before publishing any asset.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/gallery-publisher)
- [Craftsman Gallery](https://craftsman-agent.aiagenta2z.com/gallery)
- [Craftsman Workspace](https://craftsman-agent.aiagenta2z.com/workspace)
- [Craftsman Marketplace](https://craftsman-agent.aiagenta2z.com/marketplace)
- [Craftsman Store](https://craftsman-agent.aiagenta2z.com/store)
- [OneKey Gateway Access Keys](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and returned URLs or JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public gallery or marketplace URLs for uploaded assets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

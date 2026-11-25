## Description:

Make AI videos, images, voiceovers, music and full AI Video Story episodes, and post them to TikTok, YouTube and Instagram, through aicut's hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simrunbot](https://clawhub.ai/user/simrunbot)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill through an agent to create AI videos, images, voiceovers, music, and story episodes, then optionally publish finished videos to connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local path-like setup reference could not be matched to bundled content, leaving the review incomplete.

Mitigation: Check what the reference points to before installing.

Risk: Paid media generation and separate story stages spend tokens from the user's aicut account.

Mitigation: Check the balance, estimate each paid stage, quote its price, and get the user's explicit approval before spending.

Risk: Publishing to a connected social account cannot be taken back.

Mitigation: Show the post review and get the user's explicit approval before publishing.

## Reference(s):

- [aicut MCP setup and documentation](https://www.aicut.pro/mcp)
- [aicut hosted MCP server](https://mcp.aicut.pro/mcp)
- [aicut ClawHub release](https://clawhub.ai/simrunbot/skills/aicut)

## Skill Output:

**Output Type(s):** [Video, Images, Audio, Text, Guidance]

**Output Format:** [Generated media and text responses with generation or publishing status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media generation may take several minutes; paid generation stages require a price estimate and user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

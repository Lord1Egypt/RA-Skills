## Description:

Guides an agent through podcast and audiobook chapter creation on the Ximalaya audiobooklm service, including content setup, voice selection, audio synthesis, mixing, and optional album publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[audiobooklm](https://clawhub.ai/user/audiobooklm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to operate the standard audiobooklm MCP workflow for generating podcast or audiobook chapter audio from user-provided or agent-drafted text. It helps confirm book, chapter, script, voice, synthesis, mixing, and optional album publishing choices before tool actions are taken.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an API token for an external audiobook service.

Mitigation: Configure the token only in the MCP server settings, pause the workflow on authentication errors, and regenerate or rotate the token when unauthorized or expired responses appear.

Risk: Tool actions can create content, generate paid audio, or upload audio to an album.

Mitigation: Require explicit user confirmation before each tool call and review book, chapter, script, voice, album, and publishing choices before execution.

Risk: Publishing or mixing before synthesis is complete can produce incomplete or incorrect outputs.

Mitigation: Poll synthesis tasks until all segments succeed, then mix the chapter audio before any optional album upload.

## Reference(s):

- [audiobooklm-podcast on ClawHub](https://clawhub.ai/audiobooklm/skills/audiobooklm-podcast)
- [Ximalaya audiobook creation platform](https://aigc.ximalaya.com)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls, text]

**Output Format:** [Markdown guidance with configuration snippets, MCP tool-call plans, identifiers, URLs, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final responses may include book ID, chapter ID, selected speaker IDs and names, generated audio URL, edit page URL, and payment page URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

AudioBookLM helps agents produce podcasts and narrated audiobooks, including multi-voice performances, chapter synthesis, character voice binding, audio mixing, and optional album publishing through audiobooklm_mcp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[audiobooklm](https://clawhub.ai/user/audiobooklm)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to create podcast or audiobook projects, prepare chapters, select and bind voices, synthesize and mix chapter audio, and optionally publish finished audio to a Ximalaya album.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local text files to the AudioBookLM/Ximalaya service.

Mitigation: Use only files the user is allowed to send to the service, require explicit confirmation before upload, and continue only from the service-returned file path.

Risk: The skill can mutate book and character metadata, including speaker bindings.

Mitigation: Require explicit confirmation before patch_abs writes, use real IDs returned by tools, prefer dry-run handling for high-risk bulk changes, and verify results before synthesis.

Risk: The skill can generate audio and optionally publish finished audio to an album.

Mitigation: Confirm content rights and privacy before synthesis, ask for album-publishing confirmation, and return only URLs that tools or documented workflows provide.

Risk: The workflow requires an AudioBookLM/Ximalaya token.

Mitigation: Use environment or MCP authorization configuration, avoid pasting tokens into chat, and never echo authorization headers in user-facing output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/audiobooklm/skills/audiobooklm)
- [AudioBookLM Homepage](https://aigc.ximalaya.com)
- [AudioBookLM MCP Endpoint](https://aigc.ximalaya.com/audiobooklm/mcp)
- [ClawHub Publisher Profile](https://clawhub.ai/user/audiobooklm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and concise natural-language status summaries with inline JSON configuration snippets and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes tool-returned book IDs, chapter IDs, task IDs, speaker IDs, audio URLs, album URLs, edit links, and payment links; avoids exposing tokens, authorization headers, raw large JSON, or inferred URLs.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

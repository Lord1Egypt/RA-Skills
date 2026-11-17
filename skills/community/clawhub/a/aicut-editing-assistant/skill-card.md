## Description:

地鼠AI剪辑标准 Skill helps agents operate the AICut desktop MCP/HTTP/Bridge workflow to analyze media, plan Douyin documentary voiceover edits, build timelines, add captions, preview, validate, and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dspiritai](https://clawhub.ai/user/dspiritai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to guide AI agents through AICut video-editing workflows for documentary-style Douyin voiceover videos. It supports media analysis, narration-first planning, timeline construction, subtitles, review gates, validation, and export handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to control local editing projects and access local media through AICut.

Mitigation: Install only when AICut is trusted, authorize narrow project folders, avoid broad Desktop or home-directory roots, and revoke media access when editing is complete.

Risk: Local media or frame data may be shared with cloud vision services or temporary public-frame URLs during optional review workflows.

Mitigation: Confirm any cloud upload, tunnel, or public-frame sharing before use, especially for footage containing customers, contracts, chats, addresses, phone numbers, license plates, or business data.

Risk: Editing plans and captions can misrepresent source footage if generated before full transcript, audio, OCR, and frame review is complete.

Mitigation: Require the documented analysis and review gates before final timelines, use transcript- or user-confirmed captions only, and keep human final review before export or publication.

Risk: Bridge or media access tokens can be exposed if placed in URLs.

Mitigation: Use header-based tokens for local media access and avoid query-string tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dspiritai/skills/aicut-editing-assistant)
- [Bridge interface examples](artifact/examples.md)
- [AICut intelligent editing reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, JavaScript, TypeScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce editing plans, subtitle guidance, timeline instructions, validation steps, export commands, and MCP/HTTP/Bridge call sequences for AICut.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

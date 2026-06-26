## Description: <br>
Fragments helps agents capture, search, update, delete, comment on, and summarize Memos-backed work notes and daily logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hx-w](https://clawhub.ai/user/hx-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep a Memos-backed work journal, capture ideas or notes, search prior context, and manage memo comments while preserving confirmation steps for writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Captured memos and daily logs can contain private or persistent work context. <br>
Mitigation: Review memo previews, daily-log diffs, visibility settings, and destination Memos instance before approving writes. <br>
Risk: The Memos personal access token grants authenticated access to the configured Memos service. <br>
Mitigation: Treat the PAT like a password, avoid echoing it in conversation, and prefer project-scoped MCP or hook configuration where practical. <br>
Risk: Memo deletion is irreversible. <br>
Mitigation: Require exact, explicit deletion confirmation after showing the full memo content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hx-w/fragments) <br>
- [Memo Capture](references/memo-capture.md) <br>
- [Memo Comments](references/memo-comments.md) <br>
- [Daily Log](references/daily-log.md) <br>
- [Search Strategy](references/search-strategy.md) <br>
- [Claude Code setup](references/setup-claude-code.md) <br>
- [OpenCode setup](references/setup-opencode.md) <br>
- [OpenClaw setup](references/setup-openclaw.md) <br>
- [Memos Docker image](https://hub.docker.com/repository/docker/deepshape/memos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, MCP tool calls, and optional JSON search-rerank output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read actions require no confirmation; memo, comment, daily-log, update, and delete writes require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

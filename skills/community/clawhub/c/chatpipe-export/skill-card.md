## Description:

Export piped AI chat session data to Markdown, JSON, or plain text through ChatPipe v1.1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanyuanchen08-netizen](https://clawhub.ai/user/hanyuanchen08-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to convert piped chat transcripts into Markdown, JSON, or plain text for backup, migration, or import into tools such as Obsidian, Notion, ChatGPT tools, and Chatbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive chat transcripts and writes exports under ~/.openclaw/workspace.

Mitigation: Use only with trusted local transcripts and review exported files before sharing or retaining them.

Risk: The security review says the skill overpromises session retrieval and currently relies on piped stdin data.

Mitigation: Provide explicit session JSON on stdin and do not assume it can fetch current or past sessions without additional scoped retrieval support.

Risk: The helper executes a local ChatPipe file and uses weak temporary-file safeguards.

Mitigation: Run only when the local ChatPipe installation is trusted; prefer a revised version that pins or bundles ChatPipe and uses private unique temporary files with cleanup on failure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanyuanchen08-netizen/skills/chatpipe-export)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown, JSON, plain text, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write transcript export files under ~/.openclaw/workspace when the helper script succeeds.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

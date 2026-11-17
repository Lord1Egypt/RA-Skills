## Description:

Delegates developer tasks to the Claude Code CLI and reports the result back in chat, with support for new or continued sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xmanel](https://clawhub.ai/user/0xmanel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to delegate coding, analysis, and development tasks to Claude Code for a selected work directory, then receive a concise summary of what was done or found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates work to Claude Code with permission bypass and a user-selected work directory, which can expose project contents or allow unintended edits if the directory is too broad.

Mitigation: Use non-sensitive project directories, avoid credential-containing paths, verify the wrapper or direct command before use, and review Claude Code's proposed or completed changes.

Risk: Continued sessions can reuse prior file context, edits, prompts, and session history for the same work directory.

Mitigation: Use separate work directories or fresh sessions for unrelated tasks, and avoid continuing sessions that previously handled sensitive context.

Risk: The artifact makes low-risk safety claims that conflict with the server security summary.

Mitigation: Treat the server security guidance as authoritative: review before installing and use the skill only with non-sensitive projects unless independently vetted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xmanel/skills/ask-claude)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local claude executable and a user-selected work directory; continued sessions reuse Claude Code per-directory session history.]

## Skill Version(s):

1.1.1 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

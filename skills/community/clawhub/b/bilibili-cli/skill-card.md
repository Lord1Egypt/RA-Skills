## Description:

CLI skill for Bilibili with token-efficient YAML output for AI agents to browse videos, users, search results, trending content, dynamics, favorites, and interactions from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackwener](https://clawhub.ai/user/jackwener)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agents use this skill to inspect Bilibili videos, users, feeds, collections, subtitles, comments, and account interactions from a terminal. It is especially useful when an agent needs compact YAML or JSON outputs for video research and summarization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool can read local Bilibili browser cookies and store reusable session credentials.

Mitigation: Prefer QR login when possible, avoid sharing raw cookies or credential files, and clear saved credentials with `bili logout` when work is complete.

Risk: Authenticated commands can change the user's Bilibili account state, including likes, coins, favorites, follows, and dynamic posts.

Mitigation: Review account-changing commands before execution and require explicit user approval for write actions.

Risk: Audio extraction can create local media files from Bilibili videos.

Mitigation: Approve audio extraction only when local files are expected and use a deliberate output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackwener/skills/bilibili-cli)
- [Structured Output Schema](./SCHEMA.md)
- [bilibili-cli PyPI project](https://pypi.org/project/bilibili-cli/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and YAML or JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers compact YAML for agent workflows; JSON is available for strict downstream tooling.]

## Skill Version(s):

0.6.0 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

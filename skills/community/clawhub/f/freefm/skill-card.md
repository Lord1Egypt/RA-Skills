## Description:

Set up and operate the FreeFM Rust app for NetEase Private FM, including its TUI, QR login, read-only preview, append-only sync, diagnostics, and zero-LLM scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuxin-qiao](https://clawhub.ai/user/yuxin-qiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install, authenticate, preview, sync, troubleshoot, and schedule FreeFM CLI operation for their own NetEase Cloud Music Private FM account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may install a credential-handling CLI from an unpinned Git repository.

Mitigation: Review the FreeFM source before installation, or use a pinned commit or signed release when available.

Risk: Scheduled sync can repeatedly operate on a user's NetEase account session.

Mitigation: Enable scheduling only after one successful manual preview and one successful manual sync, and keep session material out of logs and agent-visible output.

## Reference(s):

- [FreeFM ClawHub skill page](https://clawhub.ai/yuxin-qiao/skills/freefm)
- [FreeFM project homepage](https://github.com/Yuxin-Qiao/FreeFM)
- [FreeFM user-facing README](https://github.com/Yuxin-Qiao/FreeFM/blob/main/README.zh-CN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scheduler configuration and verification commands; does not produce media files.]

## Skill Version(s):

0.1.0-alpha.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

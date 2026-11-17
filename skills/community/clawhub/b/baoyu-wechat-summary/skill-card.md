## Description:

Summarizes WeChat group chat history into structured normal or opt-in roast digests using the local wx-cli binary, while maintaining per-group history, user profiles, and fact memory across runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn WeChat group conversations into readable digests, optionally including a sharper roast version, while preserving continuity through history, profiles, and group memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires broad local access to wx-cli data and WeChat data paths.

Mitigation: Install only when comfortable granting local WeChat data access, prefer path-scoped sandbox permissions where available, and verify and pin the wx-cli package before use.

Risk: The skill keeps long-lived named summaries, user profiles, and group memory on disk.

Mitigation: Store the configured data root in a private non-synced location and periodically delete old history, profile, and memory files.

Risk: The optional roast mode can produce sharper personal commentary about group participants.

Mitigation: Use roast mode only when participants expect that style, and review outputs for inappropriate personal or sensitive inferences before sharing.

## Reference(s):

- [Baoyu WeChat Summary homepage](https://github.com/JimLiu/baoyu-skills#baoyu-wechat-summary)
- [wx-cli dependency](https://github.com/jackwener/wx-cli)
- [Output formats](artifact/references/output-formats.md)
- [Profiles reference](artifact/references/profiles.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown guidance with inline shell commands; generated digests are plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local digest history, profile files, profile-roast files, and group memory under the configured data root.]

## Skill Version(s):

1.117.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

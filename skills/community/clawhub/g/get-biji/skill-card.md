## Description:

从 Get 笔记 (biji.com) 同步语音笔记到本地 Markdown

This skill is ready for commercial/non-commercial use.

## Publisher:

[skychentian](https://clawhub.ai/user/skychentian)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to synchronize Get Notes voice notes from biji.com into local Markdown archives with dates, categories, summaries, attachments, and transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable account credentials are stored in local plaintext files such as .token-cache.json and .auth-state.json.

Mitigation: Use a private working and output directory, keep generated credential and state files out of shared drives and repositories, and rotate or revoke account access if those files are exposed.

Risk: The dedupe helper can permanently delete duplicate Markdown files.

Mitigation: Run the dedupe helper only after creating backups, confirming OUTPUT_DIR, and understanding which note files will be removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skychentian/skills/get-biji)
- [Get Notes service](https://biji.com)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files with YAML front matter, optional separate transcript Markdown files, and local JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated monthly note folders under the configured output directory and maintains local sync, token, and browser-auth state files.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

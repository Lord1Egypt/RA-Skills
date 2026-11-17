## Description:

Clawnote is a review-first Xiaohongshu/Rednote content operations skill for OpenClaw workflows covering topic research, draft generation, Feishu review, exact-title approval, structured publish packages, and optional approved publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:


## Use Case:

External developers and creators use this skill to run a repeatable OpenClaw workflow for researching AI or OpenClaw practice topics, drafting Xiaohongshu-style posts, routing drafts through Feishu review, and publishing only after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can read local sessions, logs, and workspace artifacts while preparing externally sent draft summaries.

Mitigation: Restrict the local files the workflow may inspect and review generated Feishu drafts before sharing them.

Risk: Draft summaries may be sent to a configured Feishu recipient.

Mitigation: Validate XHS_REVIEW_OPEN_ID before use and send only review-ready content to the configured recipient.

Risk: Persistent memory handling was flagged as unsafe for untrusted or multiline entries.

Mitigation: Avoid storing untrusted or multiline memory entries and patch write_memory_entry.py to validate --date before relying on persistent memory or cron-driven use.

Risk: Live publishing and deletion affect public Xiaohongshu content.

Mitigation: Keep preview-only defaults, require explicit approval, require exact title confirmation, and treat deletion as a separate high-risk action.

## Reference(s):

- [Clawnote README](README.md)
- [Safety](docs/SAFETY.md)
- [ClawHub Skill Page](https://clawhub.ai/zhangifonly/skills/clawnote)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON draft packages, Xiaohongshu draft text, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review-first workflow; publish commands require explicit approval and exact title confirmation.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

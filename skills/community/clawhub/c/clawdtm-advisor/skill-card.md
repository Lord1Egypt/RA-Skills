## Description:

Search, evaluate security, and install OpenClaw skills. Helps your human find the right skills safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xmythril](https://clawhub.ai/user/0xmythril)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to search OpenClaw skills, review security and community signals, and install selected skills with risk-aware defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to download and activate remote skill files, which may affect future agent sessions.

Mitigation: Use it only when the ClawdTM service is trusted and review the returned file list, paths, contents, and security context before activation.

Risk: Automated installation may reduce local validation and user control over what is written into the skills directory.

Mitigation: Prefer manual review before writing files locally and require explicit confirmation before installing medium, high, critical, or unscanned skills.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xmythril/skills/clawdtm-advisor)
- [ClawdTM Homepage](https://clawdtm.com)
- [ClawdTM API Base](https://clawdtm.com/api/v1)
- [Advisor Skill File](https://clawdtm.com/api/advisor/skill.md)
- [Advisor Metadata](https://clawdtm.com/api/advisor/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remote skill file paths, security summaries, installation recommendations, and restart guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

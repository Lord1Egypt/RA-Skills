## Description:

Batch-searches candidates, verifies public web evidence, deduplicates results, assigns risk tiers, and organizes findings into Feishu/Lark documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[16miku](https://clawhub.ai/user/16miku)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research operators use this skill to run repeatable batch web research, collect source links, deduplicate candidate lists, classify evidence quality, and prepare structured Feishu/Lark Markdown updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires broad persistent setup for BrightData access and Feishu/Lark document writing.

Mitigation: Install only after reviewing required accounts, tokens, and document scopes; prefer least-privilege Feishu/Lark permissions.

Risk: Automated document updates can add incorrect, duplicate, or low-confidence research findings.

Mitigation: Preview generated Markdown, keep append-only updates where possible, and retain source links and risk tiers for review.

Risk: Global npm or npx installation steps can change the user's development environment.

Mitigation: Prefer pinned package versions and run smoke tests before using the skill on sensitive workspaces.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/16miku/skills/brightdata-research)
- [README](README.md)
- [BrightData Search and Scrape Setup](references/brightdata-mcp-setup.md)
- [Environment Checklist](references/environment-checklist.md)
- [Feishu Setup and Write Rules](references/feishu-setup.md)
- [lark-cli Installation and Authentication](references/lark-cli-install-and-auth.md)
- [Known Failures and Fallbacks](references/known-failures-and-fallbacks.md)
- [Subagent and Git Prerequisites](references/subagent-git-prerequisites.md)
- [Smoke Tests](references/smoke-tests.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with source links, structured candidate fields, risk tiers, deduplication notes, and setup commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append prepared Markdown to Feishu/Lark documents when authorized; otherwise returns the report in conversation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

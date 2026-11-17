## Description:

Automation Skill provides agent-facing workflows for multi-engine web search, deduplicated search results, JSON search output, and structured self-reflection reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xunet2025](https://clawhub.ai/user/xunet2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to run repeatable search workflows across multiple search engines, save ranked JSON results, and record or review lessons from prior tasks. It is intended for search assistance, workflow automation, and lightweight personal improvement records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reflection entries are stored as persistent agent memory and may include sensitive user-provided content or untrusted instructions.

Mitigation: Review reflection content before saving it, avoid secrets or credentials, and require explicit confirmation before writing to or searching the QClaw memory file.

Risk: Search results are gathered from external search engines and may include incomplete, low-quality, or misleading pages.

Mitigation: Treat search output as unverified reference material and review source quality before using results in decisions, code, or documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xunet2025/skills/automation-skill)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Console text, Markdown reports, and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output includes ranked result metadata; reflection output may persist user-provided lessons under the user's QClaw memory directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

AI-powered family office management system for ultra-high-net-worth families - manage family members, professional contacts, legal documents, and tasks with natural language

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

External users and family-office operators use this skill to manage family member records, professional contact follow-ups, legal and financial document tracking, tasks, reminders, and dashboard summaries through natural-language agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for highly sensitive family, legal, financial, contact, and task records.

Mitigation: Review before installing with real records, prefer explicit invocation, and confirm before revealing dashboards, relationship details, document summaries, or personal data.

Risk: Broad activation wording may trigger the skill for ordinary family, contact, document, or task requests.

Mitigation: Use narrow activation rules or manual invocation in environments where unrelated conversations may include similar terms.

Risk: The maintainer publishing script builds a publishing command with eval and untrusted version or changelog arguments.

Mitigation: Do not run publish.sh with untrusted input; publish with direct CLI arguments or fix the script to avoid eval before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/family-steward)
- [NPM package](https://www.npmjs.com/package/openclaw-family-steward)
- [GitHub homepage listed in artifact metadata](https://github.com/ZhenRobotics/openclaw-family-steward)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline TypeScript examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize local family, contact, document, and task records; may propose actions or invoke local tool functions when available.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, release evidence, changelog released 2026-03-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Creates AI-friendly project structures using progressive disclosure indexing, including AGENTS.md, module INDEX.md files, and file intent headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[in12hacker](https://clawhub.ai/user/in12hacker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding agents use this skill to add or maintain project navigation, module indexes, and code intent documentation so agents can locate code and assess modification impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can introduce persistent project navigation files and headers where that documentation overhead is not desired.

Mitigation: Use it for AI-focused project navigation or indexing work; avoid applying it to small projects or casual code searches where persistent documentation changes are unnecessary.

Risk: Stale index files can mislead future agents about module dependencies, public APIs, or modification risk.

Mitigation: Update AGENTS.md, INDEX.md, and relevant file headers atomically with code changes, especially when files, public APIs, dependencies, or tests change.

## Reference(s):

- [Ariadne Thread ClawHub Skill Page](https://clawhub.ai/in12hacker/skills/ariadne-thread)
- [Index Templates](references/index-templates.md)
- [Index Maintenance](references/index-maintenance.md)
- [Language Adaptation](references/language-adaptation.md)
- [Naming & API Conventions](references/naming-api-conventions.md)
- [Documentation Standards](references/doc-standards.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with file templates, checklists, and occasional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or edit AGENTS.md, llms.txt, INDEX.md, documentation, and file headers when maintaining project indexes.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Better README helps agents create, improve, fix, and audit README.md files with quality scoring, project-type templates, and pre-publish checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to audit README quality, select a project-specific README template, generate improved README content, and run pre-publish readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects the current project to score or generate README content.

Mitigation: Run it only in workspaces whose README-relevant files may be reviewed by the agent.

Risk: First-use onboarding can evaluate public repository names and README contents in bulk.

Mitigation: Decline onboarding or select only specific public repositories when broad review is not desired.

Risk: Generated README changes may contain inaccurate project details if the detected project metadata is incomplete.

Mitigation: Review generated Markdown, commands, badges, and links before publishing.

## Reference(s):

- [Scoring Rubric](artifact/references/scoring-rubric.md)
- [README Templates](artifact/references/templates.md)
- [Pre-Publish Checklist](artifact/references/pre-publish-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/thomaszhou22/skills/better-readme)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, README content, code blocks, shell commands, and optional JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect project files and, during optional onboarding, review selected public GitHub repository READMEs.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

AI Collaboration Retrospective is a tool-agnostic post-session analysis framework that reviews AI-assisted development conversations across eight dimensions and generates structured retrospective reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amoshc](https://clawhub.ai/user/amoshc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after AI-assisted coding sessions to analyze conversation history, identify wasted turns or missed checks, and produce actionable retrospective reports for future workflow improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process full conversation history, which may include secrets, credentials, or confidential project material.

Mitigation: Invoke it only intentionally, avoid sessions containing sensitive material, and review generated reports before retaining or sharing them.

Risk: The skill may save retrospective reports or persist knowledge/config updates in agent environments that support those actions.

Mitigation: Require user confirmation before file writes or persistence updates, and inspect generated content before accepting it.

## Reference(s):

- [AI Retrospective Skill README](artifact/README.md)
- [Eight-Dimension Analysis](artifact/references/analysis_dimensions.md)
- [Retrospective Report Template](artifact/assets/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown retrospective reports with event timelines, dimension findings, recommendations, and pending action lists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write reports to a retrospectives directory and may propose or persist knowledge items when the agent environment supports it.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

This skill analyzes Git repositories to compare developer commit patterns, work habits, development efficiency, code style, code quality, and slacking behaviors, then generates scores, grades, strengths, weaknesses, and actionable suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongbai233](https://clawhub.ai/user/kongbai233)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to analyze one or more authorized Git repositories, compare contributor activity patterns, and generate structured developer insight reports. It is intended for repository health and team-process review, not direct HR or punitive decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill evaluates identifiable developers and uses slacking labels that could be misread as HR facts.

Mitigation: Use it only with informed consent and treat scores as repository signals for process review, not as performance, compensation, or disciplinary evidence.

Risk: Broad recursive scans can include private repositories or data outside the intended scope.

Mitigation: Run analysis only on repositories the user is authorized to inspect and avoid broad --scan-all runs on private directory trees.

Risk: Generated reports may contain personal activity data and sensitive repository information.

Mitigation: Keep reports private, store them securely, and prefer Markdown or JSON, or sanitized HTML/PDF, when analyzing untrusted repositories.

Risk: Unpinned dependencies and optional HTML/PDF rendering paths can increase production deployment risk.

Mitigation: Pin dependencies before production use and review rendered HTML or PDF output before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kongbai233/skills/code-analysis-skills-1-0-6)
- [Metrics Guide](references/metrics-guide.md)
- [PyDriller](https://github.com/ishepard/pydriller)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON, or PDF reports with optional CLI commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include developer-level scores, grades, leaderboards, metric tables, strengths, weaknesses, and suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and pyproject.toml; ClawHub package slug code-analysis-skills-1-0-6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Codex Review scans local Codex usage records and workspace artifacts to generate a local HTML retrospective with prompt diagnostics, token estimates, project summaries, and next-week action suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe-yyy](https://clawhub.ai/user/joe-yyy)

### License/Terms of Use:

MIT-0

## Use Case:

Codex users and teams use this skill to review recent Codex work, understand time and token distribution across projects, identify prompt and process gaps, and generate a local HTML report for weekly improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read recent Codex session history beyond the current workspace.

Mitigation: Run it only when that scope is acceptable, prefer explicit invocation, and review the generated local report before sharing it.

Risk: Report data may be written to a predictable temporary path.

Mitigation: Use a private output path when needed and avoid running it on shared machines until temp-file handling is tightened.

Risk: The generated report may open automatically in a browser.

Mitigation: Use the documented no-open option when running in private, automated, or shared environments.

## Reference(s):

- [Project Grouping Rules](references/project-grouping.md)
- [HTML Report Design Guide](references/report-design.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/joe-yyy/skills/codexreview)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration, guidance]

**Output Format:** [Local HTML report plus concise conversational summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports and intermediate scan data are generated locally; token and time values are estimates from local records.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

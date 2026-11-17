## Description:

Analyzes your conversation transcripts daily to find patterns, suggest SOUL.md improvements, and recommend skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dainash](https://clawhub.ai/user/dainash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to review recent OpenClaw conversation activity, identify repeated prompts and failures, and produce concise optimization suggestions for SOUL.md, workflows, and skill recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw conversation history and SOUL.md, and the security review notes that transcript processing may be broader than the one-day invocation suggests.

Mitigation: Review before installing, run only in workspaces where that local history may be exposed to the active agent context, and prefer a version that enforces date filtering.

Risk: The skill stores a derived optimization report that may summarize sensitive usage patterns from private transcripts.

Mitigation: Review generated reports before sharing, keep reports in private memory storage, and redact sensitive text from any retained or exported report.

Risk: Suggested SOUL.md or workflow changes may be incorrect or overfit to recent transcript patterns.

Mitigation: Treat all recommendations as advisory and apply changes only after human review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dainash/skills/clawforage-prompt-optimizer)
- [Publisher Profile](https://clawhub.ai/user/dainash)
- [InspireHub Labs](https://inspireehub.ai)
- [README](artifact/README.md)
- [Weekly Report Template](artifact/templates/weekly-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with suggested configuration and workflow changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a derived optimization report and requires bash and jq.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Deep Research Skill V3.1 guides an agent through a structured business research workflow with scoped questions, staged search and fetch steps, source grading, cross-validation, report generation, and final self-checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leanerque260](https://clawhub.ai/user/leanerque260)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business analysts use this skill to run evidence-based market, industry, competitive, and business decision research. It structures the work into checkpoints for scope confirmation, search planning, source grading, validation, synthesis, and final report delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically runs a local Bash orchestrator and writes checkpoint and report files.

Mitigation: Review the skill before installing, run it in a controlled workspace, and verify where checkpoint and report files will be written.

Risk: The security scan reports a command-injection risk in the state-management fallback.

Mitigation: Fix the argument-handling bug before using the skill where prompts or users can influence --complete or --next values.

Risk: The skill performs web searches and full-text fetches as part of the research workflow.

Mitigation: Use approved search and fetch tools, and review fetched sources before relying on conclusions in commercial decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leanerque260/skills/deep-research-skill-for-business)
- [README.md](artifact/README.md)
- [Source Grading Rules](artifact/rules/source-grading.md)
- [Writing Style Rules](artifact/rules/writing-style.md)
- [Report Template](artifact/templates/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research workflow output with inline shell commands and saved report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and jq or python3; writes local checkpoint and report files during normal use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

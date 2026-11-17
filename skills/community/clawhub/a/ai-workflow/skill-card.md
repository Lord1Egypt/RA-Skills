## Description:

Auto Workflow automates repetitive tasks with file processing, data conversion, scheduled jobs, API calls, and multi-step workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yofoan](https://clawhub.ai/user/yofoan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to define and run repeatable local workflows for backups, file handling, data conversion, HTTP/API calls, and multi-step automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom workflow JSON can behave like executable code.

Mitigation: Run only workflows that have been locally reviewed and come from trusted sources.

Risk: Workflows can access shell commands, files, network requests, and environment variables without adequate safeguards.

Mitigation: Execute workflows in a restricted environment with least-privilege filesystem and network access, and remove secrets from the environment before running them.

Risk: File deletion, archive extraction, and cleanup-style actions can damage or overwrite local data.

Mitigation: Avoid destructive workflows unless paths are explicitly reviewed, backups exist, and path restrictions or reliable dry-run behavior have been added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yofoan/skills/ai-workflow)
- [Publisher profile](https://clawhub.ai/user/yofoan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON workflow definitions, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create workflow JSON files and local execution logs when its bundled workflow engine is run.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

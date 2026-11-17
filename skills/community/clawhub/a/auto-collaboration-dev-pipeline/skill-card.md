## Description:

Fully automated collaborative code development pipeline for complex code development tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate multi-phase code development across requirements analysis, architecture, implementation, testing, review, documentation, and final delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spawn sub-agents and write project files without interim confirmation.

Mitigation: Use it only for intended hands-off development workflows, run it in a clean or disposable workspace, and review generated files before merging.

Risk: Repository context may be passed through multiple sub-agent prompts.

Mitigation: Avoid using it on repositories containing secrets unless that context sharing is approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/auto-collaboration-dev-pipeline)
- [Publisher Profile](https://clawhub.ai/user/openlark)
- [Architect Prompt](references/architect.md)
- [Backend Developer Prompt](references/backend-developer.md)
- [Frontend/UI Developer Prompt](references/frontend-developer.md)
- [QA Engineer Prompt](references/qa-engineer.md)
- [Code Reviewer Prompt](references/code-reviewer.md)
- [Documentation Engineer Prompt](references/documentation-engineer.md)
- [Requirements Analyst Prompt](references/requirements-analyst.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and code blocks, with generated project files written to the workspace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce specifications, architecture notes, implementation files, test reports, review notes, README content, and delivery summaries.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

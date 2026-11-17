## Description:

Provides a multi-agent AI agency with specialized agents across business departments, supporting single-agent task execution and orchestrated multi-agent project workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerry-guo-mys](https://clawhub.ai/user/jerry-guo-mys)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and business teams use this skill to route software, marketing, project management, testing, and support tasks to role-specific agents or to an orchestrator for multi-step delivery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad autonomous orchestration can plan or propose code, infrastructure, production, or public marketing changes beyond the user's intended scope.

Mitigation: Review the orchestrator's task plan before execution and require approval for sensitive code, infrastructure, production, compliance, or public-facing changes.

Risk: Manual install instructions include a placeholder repository URL that is not verified by the server evidence.

Mitigation: Install from ClawHub or another verified source, and do not rely on the placeholder clone command.

Risk: Skill documentation claims a 61-agent catalog while the artifact evidence includes only a subset of implemented agent files.

Mitigation: Confirm which agents are actually available in the installed package before depending on department-wide or full-catalog workflows.

Risk: Prompts or generated outputs may include confidential data and can be saved locally by normal agent workflows.

Mitigation: Avoid entering secrets or confidential information unless local output storage is acceptable; redact example credentials before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jerry-guo-mys/skills/agency-agents)
- [Publisher Profile](https://clawhub.ai/user/jerry-guo-mys)
- [Quickstart Guide](docs/QUICKSTART.md)
- [Project Summary](PROJECT_SUMMARY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with task-specific code, command, and configuration blocks when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by selected agent and may include implementation snippets, project plans, growth plans, QA findings, and delivery summaries.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and package.json show 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

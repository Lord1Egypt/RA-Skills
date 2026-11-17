## Description:

Track AI agent API calls, analyze token usage, and optimize costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to instrument AI agent API calls, inspect token usage, compare model costs, and generate cost reports for supported LLM providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow tells users to install mutable code directly from GitHub without a pinned version or integrity check.

Mitigation: Review or pin the package to a specific audited commit or trusted package-registry release before installation.

Risk: The tool may observe prompts, responses, usage data, and environment available to the instrumented process.

Mitigation: Install and run it in a virtual environment without elevated privileges, and avoid exposing sensitive prompts or credentials.

## Reference(s):

- [Agent Lens ClawHub page](https://clawhub.ai/lrg913427-dot/skills/agent-lens)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local SQLite-backed tracking workflows, CLI commands, and cost-analysis steps.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

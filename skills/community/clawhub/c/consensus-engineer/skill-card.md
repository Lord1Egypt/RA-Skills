## Description:

AI solution architect for consensus-tools that analyzes a project, recommends consensus-tools integration, scaffolds setup, and helps prove guard evaluation, consensus voting, persona management, workflow orchestration, and MCP tool integration with auditability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, configure, and validate consensus-tools integrations for AI governance workflows. It maps project needs to guard domains, consensus policies, architecture patterns, configuration, starter code, MCP setup, and audit-oriented proof steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can install or execute unpinned npm and MCP packages.

Mitigation: Review each command before execution, pin @consensus-tools versions, commit a lockfile, and prefer local binaries over npx-latest execution.

Risk: MCP registration can persist a new consensus-tools server in Claude or related tooling.

Mitigation: Require explicit approval before registering the MCP server and remove the registration if it is not needed after evaluation.

Risk: Optional LangSmith or model-provider integrations may send data to external services when API keys are enabled.

Mitigation: Keep optional provider and LangSmith environment variables unset unless external tracing or LLM-based evaluation is intended, and test with non-sensitive data first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/consensus-engineer)
- [consensus-tools homepage](https://github.com/consensus-tools/consensus-tools)
- [consensus-tools npm organization](https://www.npmjs.com/org/consensus-tools)
- [LangSmith](https://smith.langchain.com)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, configuration files, and generated TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive phase-gated workflow; may write project configuration and starter code when the user approves setup steps.]

## Skill Version(s):

1.0.0 (source: frontmatter, artifact metadata, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

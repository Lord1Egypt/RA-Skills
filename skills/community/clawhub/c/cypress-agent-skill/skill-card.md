## Description:

Production-grade Cypress E2E and component testing guidance for selectors, network stubbing, authentication, CI parallelization, flake elimination, Page Object Model, and TypeScript support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kahlilr23](https://clawhub.ai/user/kahlilr23)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to write, debug, and optimize Cypress end-to-end and component tests, including setup, selectors, assertions, network stubbing, authentication, CI, and flake prevention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install documentation includes curl-to-bash remote code execution and unpinned npx command examples.

Mitigation: Review install instructions before use; prefer ClawHub or a reviewed git clone, and avoid unpinned npx -y commands.

Risk: Examples include database reset, secret, payment, and CI artifact handling patterns that could affect real systems if copied directly.

Mitigation: Use those examples only in isolated test environments with explicit non-production checks.

## Reference(s):

- [Cypress Documentation](https://docs.cypress.io)
- [AgentSkills Spec](https://agentskills.io)
- [ClawHub Skill Page](https://clawhub.ai/kahlilr23/skills/cypress-agent-skill)
- [README](README.md)
- [Selectors Reference](references/selectors.md)
- [Commands Reference](references/commands.md)
- [Network Control Reference](references/network.md)
- [Assertions Reference](references/assertions.md)
- [Configuration Reference](references/config.md)
- [CI/CD Reference](references/ci.md)
- [Component Testing Reference](references/component-testing.md)
- [Advanced Patterns Reference](references/patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript, TypeScript, JSON, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Cypress test code, configuration snippets, CI workflow examples, and troubleshooting guidance for the user's project.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

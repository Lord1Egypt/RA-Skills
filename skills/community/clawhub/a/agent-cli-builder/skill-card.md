## Description:

Build or modernize TypeScript CLIs for AI agents with @renxqoo/agent-cli-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renxqoo](https://clawhub.ai/user/renxqoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or modernize buildable, testable TypeScript command-line tools that agents can invoke reliably. It is suited for wrapping APIs or internal services as CLIs and extending agent-cli-sdk apps with authentication, structured output, typed errors, pagination, pipes, Skill distribution, documentation, and tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to modify CLI projects, run package-manager or test commands, and generate installer or authentication flows.

Mitigation: Review the proposed changes and commands before execution, keep work in an appropriate development workspace, and explicitly approve global installs, npx-based installs, network calls, login, and file synchronization.

Risk: Authentication examples and generated CLI flows can involve credentials or registration tokens.

Mitigation: Do not paste production credentials into chat, avoid command-line arguments for long-lived secrets, use a private terminal for registration, and review generated auth code and examples for secret leakage.

Risk: Generated API wrappers can become unreliable if request fields, pagination, errors, or response contracts are guessed.

Mitigation: Require API contracts, tests, or real safe response samples before implementation, mark unresolved facts as blockers, and validate generated commands with format, lint, typecheck, build, help, JSON success, and failure checks.

## Reference(s):

- [Core Implementation Contract](references/core-api.md)
- [Authentication with defineAuth](references/auth-patterns.md)
- [Custom Authentication Plugins and Providers](references/custom-auth-plugin.md)
- [Error Catalog and Status Mapping](references/error-catalog.md)
- [Advanced Patterns: Pagination, Pipes, and Human Output](references/patterns.md)
- [Plugin Patterns and Hook Ordering](references/plugin-patterns.md)
- [JSON arguments and write safety](references/structured-input.md)
- [Skill Generation, Synchronization, and Distribution](references/skill-gen.md)
- [Production Skill Optimization Guide](references/skill-optimization.md)
- [README Generation Guide](references/readme-gen.md)
- [Testing and Real-Task Evaluation](references/testing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code examples, JSON snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

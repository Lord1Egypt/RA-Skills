## Description:

Write and run TypeScript scripts with Bun instead of plain Node.js or JavaScript, using Bun's runtime, package manager, test runner, file APIs, shell API, HTTP server, and SQLite support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bcanfield](https://clawhub.ai/user/bcanfield)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to create, run, test, and manage TypeScript and JavaScript scripts with Bun. It helps agents choose Bun-native commands and APIs for scripting, package management, file I/O, process execution, HTTP serving, SQLite work, and tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation, bunx execution, and network fetches can introduce third-party code or dependency changes.

Mitigation: Review proposed bun add, bun install, bunx, and network-fetching commands before execution, especially in projects with existing Node/npm workflows.

Risk: Shell commands, file writes, and server starts can modify local projects, expose services, or touch sensitive environment variables.

Mitigation: Confirm the working directory, files, ports, and environment variables before running commands or starting servers.

Risk: Bun runs TypeScript without runtime type-checking, so type errors may not block execution.

Mitigation: Run tsc --noEmit when type correctness matters, such as before committing or in CI.

## Reference(s):

- [Bun API Reference](references/REFERENCE.md)
- [Bun LLM documentation index](https://bun.sh/llms.txt)
- [Bun LLM full documentation](https://bun.sh/llms-full.txt)
- [ClawHub skill page](https://clawhub.ai/bcanfield/skills/bun-scripts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the bun binary. TypeScript is stripped at runtime, so run tsc --noEmit separately when type-checking is required.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

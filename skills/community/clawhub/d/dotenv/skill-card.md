## Description:

Use dotenv to manage environment variables for Node.js projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and configure dotenv or dotenvx, load .env files into Node.js applications, document environment-file formats, and apply safe handling patterns for secrets and multi-environment configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dotenvx installation guidance includes a remote shell installer pattern that could execute unverified code.

Mitigation: Prefer package-manager installation such as npm, Bun, Yarn, pnpm, or Homebrew, and review any installer source before execution.

Risk: The skill works with environment variables and examples involving API keys, private keys, and .env files.

Mitigation: Do not allow an agent to print, commit, upload, or log real .env values, .env.keys files, private keys, or production secrets.

## Reference(s):

- [dotenv API In-Depth Reference](references/api-reference.md)
- [dotenvx](https://dotenvx.sh/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JavaScript, TypeScript, shell, gitignore, and ini code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include installation commands, dotenv configuration examples, .env formatting notes, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

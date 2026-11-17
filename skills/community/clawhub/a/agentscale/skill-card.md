## Description:

Deploy web apps and APIs to a public URL with a single command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpbonch](https://clawhub.ai/user/jpbonch)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use AgentScale to register for service access, package a local web app or API, deploy it to a public URL, and inspect deployed service or account status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload the current project directory to AgentScale for public deployment.

Mitigation: Run deployment only from the intended project directory and remove secrets or unrelated files before packaging.

Risk: AGENTSCALE_API_URL can redirect API calls carrying the stored API key and project archive.

Mitigation: Check the environment and local .env files for AGENTSCALE_API_URL before use, and unset unexpected overrides.

Risk: The documented npx commands do not pin an AgentScale package version.

Mitigation: Prefer a pinned agentscale version when invoking the CLI.

## Reference(s):

- [ClawHub AgentScale skill page](https://clawhub.ai/jpbonch/skills/agentscale)
- [Nixpacks](https://nixpacks.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples, deployment limits, account setup steps, and environment-variable cautions.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

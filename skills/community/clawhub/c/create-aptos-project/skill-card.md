## Description:

Scaffolds new Aptos projects with npx create-aptos-dapp, supporting fullstack Vite or Next.js templates and contract-only Move projects with network selection and optional API key setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start Aptos dApp or Move contract projects from the official scaffolding command, choose project type, framework, network, and optional API key settings, and follow post-scaffold checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage unpinned remote npx execution, including auto-confirmed package installation.

Mitigation: Pin create-aptos-dapp to a reviewed version and avoid npx --yes unless the package and version have been approved.

Risk: Generic app-building trigger phrases may activate the skill outside an Aptos project setup.

Mitigation: Enable or invoke the skill only when the user explicitly wants an Aptos app, dApp, Move contract, or Aptos project scaffold.

Risk: Scaffolding, aptos init, git commits, or deployments can affect accounts, files, and repository history.

Mitigation: Run the workflow in a limited workspace without unrelated secrets and require separate explicit approval before account initialization, git commits, or deployment steps.

## Reference(s):

- [Geomi API keys](https://geomi.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute project scaffolding, Aptos account initialization, tests, and git commands after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata; SKILL.md frontmatter lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

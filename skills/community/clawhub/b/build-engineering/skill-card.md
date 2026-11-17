## Description:

Build Engineering helps developers diagnose and optimize frontend build toolchains, monorepos, module federation, CI/CD pipelines, code generation, and developer experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to investigate slow builds, structure pnpm and Turborepo monorepos, configure module federation, improve GitHub Actions pipelines, and add code generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested package installs, GitHub Actions snippets, or build configuration changes could affect supply-chain exposure, CI behavior, or production build output.

Mitigation: Review generated commands and configuration before applying them, pin package versions and GitHub Actions to reviewed versions or SHAs, and test changes in a branch or staging pipeline first.

Risk: The skill requests the Opus model, which may affect account cost or model governance requirements.

Mitigation: Confirm that the requested model is acceptable for the deploying account, budget, and internal approval process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzhiming1999/skills/build-engineering)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with configuration snippets, code examples, shell commands, and diagnostic recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest package installs, CI snippets, and build configuration changes that should be reviewed before application.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

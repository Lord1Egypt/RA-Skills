## Description:

Edith Augment Code uses Augment Code's Auggie CLI to help agents build, analyze, debug, and prototype code through OpenClaw and Edith smart glasses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samdickson22](https://clawhub.ai/user/samdickson22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate code generation, codebase analysis, debugging, reviews, and prototyping tasks to Auggie from Edith smart glasses or OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad coding, debugging, and codebase-analysis requests may route project context to the third-party Auggie CLI.

Mitigation: Confirm repository or file scope before use, especially for private or sensitive code.

Risk: Installing or running the Auggie CLI without review may introduce supply-chain or permission risk.

Mitigation: Pin and review the CLI version, avoid elevated installation privileges, and install only when Auggie is intentionally desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samdickson22/skills/edith-augment-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown text with inline shell commands and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be summarized concisely for Edith glasses voice use, with key findings, created files, root causes, or fixes called out.]

## Skill Version(s):

1.0.0 (source: release evidence, shipables.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

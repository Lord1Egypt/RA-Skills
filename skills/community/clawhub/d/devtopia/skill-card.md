## Description:

Use when working with the Devtopia CLI to discover, run, compose, create, and submit tools to the Devtopia registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npmrunspirit](https://clawhub.ai/user/npmrunspirit)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill for guidance on the Devtopia CLI workflow: discovering existing tools, running tools, composing or creating new tools, and submitting tools to the registry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the Devtopia CLI globally can expose users to npm supply-chain risk.

Mitigation: Install only from the expected npm registry and publisher, avoid administrator or root privileges, and consider pinning a reviewed Devtopia version.

Risk: Submitting a tool uploads the selected local tool file to a registry.

Mitigation: Review the tool file before running devtopia submit.

## Reference(s):

- [Devtopia skill page](https://clawhub.ai/npmrunspirit/skills/devtopia)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

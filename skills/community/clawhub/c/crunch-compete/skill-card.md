## Description:

Use when working with Crunch competitions - setting up workspaces, exploring quickstarters, testing solutions locally, or submitting entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philippwassibauer](https://clawhub.ai/user/philippwassibauer)

### License/Terms of Use:


## Use Case:

Developers and Crunch competition participants use this skill to set up isolated CrunchDAO competition workspaces, inspect quickstarters, test local solutions, and submit entries through the Crunch CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python package installation or quickstarter overwrite commands can change the user's local environment or files.

Mitigation: Use a per-competition virtual environment, install only documented packages unless the user approves, and run overwrite actions only after confirming file replacement is acceptable.

Risk: Crunch submission tokens can be exposed if copied into source files, notebooks, logs, or shared terminal output.

Mitigation: Ask the user for the project token when needed, use placeholders in examples, and avoid writing or echoing real tokens.

Risk: Network-dependent commands contact CrunchDAO Hub, PyPI, or public GitHub APIs and may fail under rate limits or restricted networks.

Mitigation: Identify which commands require network access and prefer local testing with crunch test before submission.

## Reference(s):

- [Crunch CLI Reference](artifact/references/cli-reference.md)
- [Competition Setup Examples](artifact/references/competition-setup.md)
- [Crunch CLI on PyPI](https://pypi.org/project/crunch-cli/)
- [CrunchDAO Hub](https://hub.crunchdao.com)
- [Crunch Compete on ClawHub](https://clawhub.ai/philippwassibauer/skills/crunch-compete)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and code suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local Crunch CLI commands, package installation steps, and user-token handling guidance.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

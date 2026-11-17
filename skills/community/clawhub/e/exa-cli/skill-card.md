## Description:

Manage Exa AI from the command line for search, page contents, AI answers, and web context retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install, authenticate, and call the Exa CLI for web search, content retrieval, answer generation, and context gathering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup commands may execute unpinned third-party installers or packages.

Mitigation: Use a pinned and verified Exa CLI installation path before running setup commands.

Risk: Setup can modify the command environment, including PATH.

Mitigation: Require explicit approval for environment changes and review resulting PATH updates before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/melvynx/skills/exa-cli)
- [Publisher profile](https://clawhub.ai/user/melvynx)
- [Bun installer referenced by setup](https://bun.sh/install)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use the --json flag when called programmatically.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

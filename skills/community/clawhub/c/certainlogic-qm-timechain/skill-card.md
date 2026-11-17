## Description:

CertainLogic QM Timechain lets QM agents query the CertainLogic Timechain for cryptographically verified agent execution traces for training, audit, and research, with API access sold separately.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certainlogicai](https://clawhub.ai/user/certainlogicai)

### License/Terms of Use:

MIT

## Use Case:

Developers and QM workspace administrators use this skill to let QM agents search, fetch, and inspect CertainLogic Timechain execution traces for training-data discovery, audit review, and research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad access to production agent-trace data through a shared QM deployment.

Mitigation: Limit API-key access to approved users, require administrator approval for workspace-wide installation, and confirm the corpus is sanitized and lawfully shareable before use.

Risk: The documentation makes cryptographic trust claims that are not fully scoped by an independently specified verification scheme.

Mitigation: Treat documented hash-link checks as supporting evidence only and require independent verification requirements before relying on them for authenticity or compliance decisions.

## Reference(s):

- [CertainLogic homepage](https://certainlogic.ai)
- [ClawHub skill page](https://clawhub.ai/certainlogicai/skills/certainlogic-qm-timechain)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CertainLogic API key and network access to the configured API endpoint.]

## Skill Version(s):

0.1.0 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

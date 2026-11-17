## Description:

Draft Machine helps an agent prepare Gmail mail-merge drafts from a CSV recipient list and a Markdown/Jinja2 template so the user can review messages before sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[audiojak](https://clawhub.ai/user/audiojak)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and external users use this skill to create personalized Gmail drafts for batch outreach or mail merge workflows while keeping final send review in Gmail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install and authorize mutable third-party software for Gmail draft access without pinning or integrity checks.

Mitigation: Review and pin the DraftMachine package and skill source to a trusted version or commit, preferably in an isolated environment.

Risk: The workflow stores OAuth material under ~/.draftmachine and can create Gmail drafts at batch scale.

Mitigation: Proceed only after accepting the Gmail draft access requirement, preview output before draft creation, and review all Gmail drafts before sending.

## Reference(s):

- [DraftMachine on PyPI](https://pypi.org/project/draftmachine/)
- [DraftMachine source](https://github.com/johnkennedy/DraftMachine)
- [Jinja2 documentation](https://jinja.palletsprojects.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, CSV examples, and Markdown/Jinja2 template examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides preview-first draft creation and user review before sending.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

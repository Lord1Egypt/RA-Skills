## Description:

Discover, create, upload, pay for, and track fax jobs using the FaxAgent.ai API with safe polling, promo tokens, and human-facing upload, payment, and status links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[faxagent](https://clawhub.ai/user/faxagent)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to create fax jobs, present upload and payment links to a human, and poll job status through FaxAgent.ai. It is intended for workflows that need careful handling of sensitive fax documents and tokenized URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive fax documents and tokenized upload, payment, and status URLs.

Mitigation: Use it only when intending to send or track a fax, redact tokens, avoid logging full tokenized URLs, and avoid passing fax tokens on the command line.

Risk: Returned upload and payment links could be misused if they are not checked before being shown to a user.

Mitigation: Verify that upload and payment links stay on the expected FaxAgent.ai domain before presenting them.

Risk: Payment links are part of the workflow and could lead to unintended payment activity.

Mitigation: Surface payment links to the human user for review and completion; do not auto-execute payments.

## Reference(s):

- [FaxAgent API discovery document](https://faxagent.ai/api/discovery.json)
- [ClawHub FaxAgent-Skill release page](https://clawhub.ai/faxagent/skills/faxagent-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Surfaces human-facing upload, payment, and status links; tokenized URLs should be redacted in shared contexts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

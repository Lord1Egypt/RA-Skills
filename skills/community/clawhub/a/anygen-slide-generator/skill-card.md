## Description:

Generates slide presentations with the AnyGen CLI for decks, reports, proposals, training materials, launches, reviews, and other presentation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[logictortoise](https://clawhub.ai/user/logictortoise)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to create slide decks and presentation materials through AnyGen. It is appropriate for pitch decks, business reviews, training content, proposals, reports, and similar slide-generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation prompts and source material are sent to the external AnyGen service.

Mitigation: Do not submit confidential business, customer, HR, or financial data unless organizational approval covers that external processing.

Risk: The workflow can install unpinned remote workflow content automatically.

Mitigation: Review the AnyGen CLI package and anygen-workflow-generate skill before use, and avoid unattended installs.

Risk: Command-line API keys may expose credentials through shell history or process metadata.

Mitigation: Prefer browser login or managed-secret environment configuration over passing API keys directly on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/logictortoise/skills/anygen-slide-generator)
- [AnyGen service](https://www.anygen.io)
- [ClawHub publisher profile](https://clawhub.ai/user/logictortoise)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent instructions for authenticating with AnyGen CLI and invoking the slide workflow.]

## Skill Version(s):

3.0.0 (source: server release metadata, released 2026-03-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

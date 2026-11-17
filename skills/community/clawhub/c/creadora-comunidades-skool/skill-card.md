## Description:

A Spanish-language agent skill for designing Skool community strategy, offers, onboarding, sales copy, forum structure, VSL scripts, retention scripts, and client-ready proposal documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and community strategists use this skill to gather a guided brief and generate Spanish Skool community assets, including offers, onboarding, pinned posts, VSL scripts, cancellation videos, forum categories, and full client proposal documents. It is intended for commercial ClawHub use and asks for missing business facts rather than inventing metrics, prices, urgency, or authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle confidential client strategy, positioning, pricing, and founder-background details while gathering briefs.

Mitigation: Review the Telegram workflow before use with confidential client data and provide only information appropriate for the deployment environment.

Risk: The proposal generator writes a DOCX file to a default output location when no custom path is supplied.

Mitigation: Use the --out option when the document should be saved to a controlled workspace or client-specific folder.

Risk: Generated community copy or proposal content can be misleading if source facts are incomplete.

Mitigation: Follow the skill's guided brief flow and review all outputs for accurate metrics, prices, urgency, authority, and client-specific claims before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/creadora-comunidades-skool)
- [templates.md](templates.md)
- [propuesta-integral.md](propuesta-integral.md)
- [brief.schema.json](brief.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Spanish conversational guidance, Markdown-ready copy, JSON brief structure, shell command examples, and generated .docx proposal files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The DOCX generator depends on python-docx and emoji; use --out when the default document path is not appropriate.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

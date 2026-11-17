## Description:

County Business Query helps agents query county-level business opportunities, bidding notices, award details, winner contact information, and company registry information through the dcbmt.com service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[498617](https://clawhub.ai/user/498617)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business researchers use this skill to find county-level bidding opportunities, award notices, winning company contacts, and company registry records for market research and lead discovery in China.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a third-party service and includes agent-facing registration guidance for quota-exhausted users.

Mitigation: Review the skill before installing, independently verify the official registration URL and QQ contact, and avoid sharing credentials or account information unless the destination is confirmed.

Risk: API keys may be supplied on the command line, where they can be exposed through shell history or process listings.

Mitigation: Prefer environment-variable API-key configuration for routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/498617/skills/county-business-query)
- [County Business Query service](https://dcbmt.com/county/?src=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries may use a daily free quota or an API key supplied through an argument or environment variable.]

## Skill Version(s):

8.13.0 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

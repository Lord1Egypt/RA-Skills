## Description:

Helps agents operate company email in Banger, including onboarding, Mailboxes, contacts, Product email, Broadcasts, Journeys, and delivery setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tgloureiro](https://clawhub.ai/user/tgloureiro)

### License/Terms of Use:

MIT-0

## Use Case:

Teams managing company email use this skill to set up Banger, work with Mailboxes and contacts, draft and send Product email or Broadcasts, and manage Journeys and delivery settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to sensitive company email and contact data may expose or change workspace information.

Mitigation: Review the Banger authorization screen and workspace scope before connecting; grant access only to the intended workspace.

Risk: Sending mail or importing contacts can affect real recipients.

Mitigation: Check the intended product, audience, content, and send or import request before execution; use Banger's applicable review controls.

Risk: Changing domain mail records or creating credentials can disrupt mail delivery or grant additional access.

Mitigation: Confirm existing mail services and administrator approval before DNS changes; handle credentials only through Banger's authorization pages.

## Reference(s):

- [Banger agent guide](https://bangermail.com/agents/openclaw/)
- [Banger MCP setup guide](https://bangermail.com/banger-mcp/)
- [ClawHub skill listing](https://clawhub.ai/tgloureiro/skills/banger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Conversational text or Markdown, including email drafts and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can report Banger workspace actions and approval status.]

## Skill Version(s):

0.2.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

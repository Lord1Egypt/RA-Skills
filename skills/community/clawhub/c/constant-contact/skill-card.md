## Description:

Helps an agent manage Constant Contact contacts, campaigns, lists, and marketing data through a connected Maton account, with approval before changes or sends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and developers use this skill to inspect and manage Constant Contact contacts, lists, campaigns, and analytics. With user approval, they can also configure related automations and perform account changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writes, bulk changes, deletions, and campaign sends can change or permanently remove marketing data or contact customers.

Mitigation: Begin with read-only checks, then obtain explicit user approval for each action with exact resource IDs, audience, and expected impact.

Risk: Deployed functions, triggers, and destinations may continue acting on new events without a person present.

Mitigation: Review each deployment and destination's data flow, confirm intended unattended behavior, and disable unused automation.

Risk: Connections and responses can expose account access and personal contact information.

Mitigation: Approve new connections explicitly, limit scopes and returned fields, avoid logging sensitive responses or credentials, and revoke access when no longer needed.

## Reference(s):

- [Constant Contact V3 API overview](https://developer.constantcontact.com/api_guide/getting_started.html)
- [Constant Contact API reference](https://developer.constantcontact.com/api_reference/index.html)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)
- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/constant-contact)
- [Time trigger reference](artifact/references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require a connected account; obtain explicit approval for writes, sends, and automation.]

## Skill Version(s):

1.2.6 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

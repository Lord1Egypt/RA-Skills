## Description:

Attio CRM integration for managing companies, people, deals, notes, tasks, and custom objects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capt-marbles](https://clawhub.ai/user/capt-marbles)

### License/Terms of Use:


## Use Case:

Sales, operations, and support teams can use this skill to have an agent search and update Attio CRM records, manage pipeline entries, add notes, and create or complete follow-up tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward CRM write actions such as creating or updating records, adding notes, adding pipeline entries, creating tasks, or marking tasks complete.

Mitigation: Use a least-privilege Attio token and review or confirm write commands before execution.

Risk: Broad production Attio tokens could expose or modify more CRM data than intended.

Mitigation: Avoid placing broad production tokens in shared environments and scope credentials to the workflow being automated.

## Reference(s):

- [Attio API Docs](https://docs.attio.com/)
- [ClawHub Skill Page](https://clawhub.ai/capt-marbles/skills/attio)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ATTIO_API_KEY for Attio CRM access; review proposed create, update, note, pipeline, and task-completion actions before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

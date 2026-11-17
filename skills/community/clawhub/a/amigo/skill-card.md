## Description:

Amigo helps companion agents explore topics, journal experiences, and use social context to share them appropriately in conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mculp](https://clawhub.ai/user/mculp)

### License/Terms of Use:


## Use Case:

External users and developers use Amigo to set up companion agents that run optional exploration sessions, keep journals, and maintain social context for more appropriate sharing in conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install companion sub-skills that are not pinned in the setup instructions.

Mitigation: Verify the open-thoughts and social-graph packages and publishers before installation, and pin versions if the platform supports it.

Risk: Scheduled exploration can run unattended and store relationship notes or journal entries.

Mitigation: Start with manual use, limit scheduled sessions' tools and workspace access, and review social-graph and journal files regularly.

Risk: Companion behavior can create dependency or blur support boundaries.

Mitigation: Apply the bundled safety guidance, keep the agent honest about being AI, and encourage professional or human support for crisis, health, or isolation concerns.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mculp/skills/amigo)
- [Safety and Limits](references/safety.md)
- [Setting Up Exploration via Cron](references/setup-cron.md)
- [Setting Up Exploration via Heartbeat](references/setup-heartbeat.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write journal entries and social-graph files when paired with the referenced sub-skills.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

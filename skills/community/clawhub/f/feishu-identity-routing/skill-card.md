## Description:

Build and use a Feishu/Lark cross-app identity master for multi-agent, multi-account routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxfkuq2023](https://clawhub.ai/user/wxfkuq2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain a canonical Feishu/Lark identity master, merge app-local identities, review ambiguous matches, and route outbound actions through the correct account-specific open_id.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and mutates sensitive Feishu identity-routing data.

Mitigation: Install only in a controlled workspace where identity correlation is authorized, and restrict access to the identity directory.

Risk: Batch imports and merge scripts can modify the identity master from input records.

Mitigation: Avoid running batch imports on untrusted paths and review or harden the scripts before using the master file for outbound messages.

Risk: Logs and review records may expose identity data or routing decisions.

Mitigation: Treat logs and review artifacts as sensitive and limit their retention and access.

## Reference(s):

- [Workflow](references/workflow.md)
- [Outbound Routing Patterns](references/outbound-routing-patterns.md)
- [Pending Review Policy](references/pending-review-policy.md)
- [Schema Example](references/schema-example.json)
- [Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/wxfkuq2023/skills/feishu-identity-routing)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON structures and Node.js command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates workspace identity files for Feishu/Lark identity mapping and pending-review workflows.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

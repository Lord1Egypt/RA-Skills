## Description:

Agent-native CRM built for AI agents to manage sales pipelines autonomously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giorgallidis](https://clawhub.ai/user/giorgallidis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to create and manage ClawCRM workspaces, leads, enrichment, proposal engagement, email sequences, feedback, and pipeline analytics through API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad autonomous sales, lead enrichment, and email-sending actions.

Mitigation: Use clear human approval rules for outreach and restrict the agent to authorized lead data.

Risk: CRM tokens could be exposed through prompts, logs, or shell history.

Mitigation: Store the ClawCRM token in a secret manager or environment variable and avoid placing it in prompts or command history.

Risk: Sales outreach and enrichment workflows may trigger privacy, consent, or compliance obligations.

Mitigation: Verify the applicable requirements for sales emails and data enrichment before allowing autonomous execution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/giorgallidis/skills/clawcrm)
- [ClawCRM homepage](https://clawcrm.ai)
- [ClawCRM service](https://readycrm.netlify.app)
- [ReadyCRM repository link from metadata](https://github.com/Protosome-Inc/ReadyCRM)
- [ReadyCRM issues](https://github.com/Protosome-Inc/ReadyCRM/issues)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWCRM_API_KEY and authorized ClawCRM workspace access.]

## Skill Version(s):

1.0.8 (source: server release evidence; artifact _meta.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

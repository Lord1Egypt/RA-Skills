## Description: <br>
Use when a user wants to initialize OpenClaw, Hermes, or another agent harness for ordinary business or office work. Guides plain-language business interviews, recommends agent roles, object-based Markdown memory, tool permissions, model tiers, free/paid upgrade paths, and generates starter workspaces with the `agent-launchpad` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users, operators, and developers use this skill to turn plain office workflows into OpenClaw or Hermes starter workspaces with agent roles, Markdown object memory, model tier choices, and permission plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can lead to agents that touch customer records, HR, legal, finance, CRM, accounting, messages, forms, payments, or paid cloud services. <br>
Mitigation: Review generated permission, tool, cost, and model plans before enabling high-impact actions, and require explicit user approval before sending messages, submitting forms, changing records, approving payments, storing sensitive data, or enabling paid services. <br>
Risk: The skill includes a global npm install step that could install from the wrong project folder if run casually. <br>
Mitigation: Confirm the skill was intentionally selected and run `npm install -g .` only from the expected agent-launchpad project folder. <br>
Risk: Implicit invocation could apply business-agent setup guidance when the user's intent is unclear. <br>
Mitigation: Confirm the user's setup goal before running interview or generation commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyrenxu7255/business-agent-launchpad) <br>
- [ClawHub metadata homepage](https://clawhub.ai/skills/business-agent-launchpad) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated workspace file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces starter workspace guidance, permission plans, tool plans, model tier choices, and verification commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

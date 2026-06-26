## Description: <br>
Blueprint for wiring multiple OpenClaw agents running on different servers into shared Feishu group chats so they can coordinate multi-turn discussions, hand off tasks, log cross-agent messages, and pause for human approvals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Waytobetter619](https://clawhub.ai/user/Waytobetter619) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and configure a Feishu relay that lets multiple OpenClaw agent instances coordinate in authorized group chats while preserving shared context, logs, routing rules, and human approval checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu bot secrets, verification tokens, encrypt keys, session keys, and chat logs may be exposed or misused if operators place real values in source control or broad shared storage. <br>
Mitigation: Keep real secrets out of the skill files, use environment-specific secret storage, restrict log store access, and define retention and redaction rules before deployment. <br>
Risk: A relay connected to unauthorized chats or bots could route messages or invoke agents outside the intended scope. <br>
Mitigation: Deploy only for approved chats and bots, enforce chat allowlists, require human approval at configured checkpoints, and review route configuration before enabling automation. <br>
Risk: The included callback server is sample code and contains artifact-level issues that make it unsuitable for production without review. <br>
Mitigation: Fix and test the sample callback server, pin dependencies, run it behind HTTPS, validate Feishu event signatures and tokens, and perform a security review before production use. <br>


## Reference(s): <br>
- [Architecture Guide](references/architecture.md) <br>
- [Deployment Checklist](references/deployment-checklist.md) <br>
- [Information Intake Form](references/info-collection-template.md) <br>
- [Logging & Approval Schema](references/logging-schema.md) <br>
- [Workflow Templates](references/workflow-templates.md) <br>
- [Scripts README](scripts/README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Waytobetter619/feishu-agent-mesh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces relay architecture, deployment, logging, approval, and Feishu callback setup guidance for agent operators.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

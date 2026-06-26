## Description: <br>
Helps agents design, build, debug, optimize, and scale production-grade n8n workflows with architecture, security, error handling, testing, and deployment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, automation engineers, and operations teams use this skill to plan, review, and generate n8n workflow designs for integrations, data processing, alerts, approvals, AI-assisted routing, and production operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workflow designs may include code nodes, webhook endpoints, credentials, logging, or persistent state that affect live n8n systems. <br>
Mitigation: Review generated workflows before production use, with particular attention to code nodes, credential scope, webhook authentication, logs, customer or payment data, and cache or state retention. <br>
Risk: Automation workflows can expose sensitive data or secrets if copied into production without environment-specific review. <br>
Mitigation: Use the n8n credential store or environment variables, avoid hardcoded secrets, minimize logged payload data, and validate webhook payloads before processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-n8n-mastery) <br>
- [Publisher profile](https://clawhub.ai/user/1kalin) <br>
- [Context packs referenced by artifact README](https://afrexai-cto.github.io/context-packs/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML, JSON, JavaScript, checklist, and workflow-template examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no installer or runtime dependency is provided by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
YAML-driven workflow orchestrator for AI agent teams with human-in-the-loop approval gates and optional Notion, n8n, and Discord integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanhuelsing](https://clawhub.ai/user/vanhuelsing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Flowclaw to run YAML-defined AI agent workflows, coordinate approval gates, and connect optional Notion, n8n, and Discord automation around agent tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service can trigger agents, scripts, external updates, and deployments. <br>
Mitigation: Install only where this privileged local automation is intended, and restrict n8n and Notion triggers to approved tasks. <br>
Risk: Approval enforcement may be weaker than the skill description implies. <br>
Mitigation: Add enforced wait_approval gates before production deployment steps or any final Done status. <br>
Risk: Workflow files and QA scripts are trusted inputs that can affect local automation behavior. <br>
Mitigation: Protect the workflow and scripts directories from untrusted edits, and install workflows only from trusted sources. <br>
Risk: Enabling FLOWCLAW_LOAD_OPENCLAW_CONFIG expands credential access to the global OpenClaw config. <br>
Mitigation: Leave FLOWCLAW_LOAD_OPENCLAW_CONFIG disabled unless needed, and use dedicated credentials for Flowclaw. <br>
Risk: Network exposure would increase impact if the API key is weak or leaked. <br>
Mitigation: Keep the service bound to localhost or behind strong network controls, and use a dedicated strong API key. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vanhuelsing/flowclaw-orchestrator) <br>
- [README](README.md) <br>
- [Security Policy](SECURITY.md) <br>
- [Integration Steps](docs/INTEGRATION-STEPS.md) <br>
- [n8n Integration Guide](docs/n8n-integration-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, YAML workflow definitions, JSON workflow templates, and Python service code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WORKFLOW_EXECUTOR_API_KEY; optional integrations use Notion, Discord, n8n, and OpenClaw gateway environment variables.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

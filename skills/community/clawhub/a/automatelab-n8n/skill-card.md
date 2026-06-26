## Description: <br>
Use when the user wants to build, debug, or extend an n8n workflow - generating workflow JSON from a description, scaffolding a custom TypeScript node, building an AI agent, iterating over items, writing Code-node JavaScript, linting an existing workflow, diagnosing a failed execution, or driving a live n8n instance via REST. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[automatelab](https://clawhub.ai/user/automatelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to generate, lint, debug, deploy, and manage n8n workflows, including live-instance operations when n8n API credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent manage a live n8n instance when API credentials are supplied. <br>
Mitigation: Use a limited n8n API key where possible and avoid storing live-instance credentials in shared or untrusted agent environments. <br>
Risk: Generated or modified workflows could behave differently than intended if created or activated without review. <br>
Mitigation: Review generated workflows before creating or activating them, and lint workflows before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/automatelab/automatelab-n8n) <br>
- [Project Homepage](https://github.com/ratamaha-git/n8n-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON workflow definitions, TypeScript code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live-instance operations require N8N_API_URL and N8N_API_KEY environment variables; stateless workflow generation, linting, node scaffolding, and execution explanation can operate without those credentials.] <br>

## Skill Version(s): <br>
0.4.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

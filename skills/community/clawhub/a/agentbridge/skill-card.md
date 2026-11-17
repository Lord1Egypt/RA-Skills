## Description:

Agent-Browser-Bridge-AI provides anti-detection browser control for AI agents with DOM-first interaction, human-like input simulation, lead generation, extraction, and MCP integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexandre-leng](https://clawhub.ai/user/alexandre-leng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect AI agents to browser automation workflows for authorized navigation, page annotation, form interaction, web search, structured extraction, and lead-generation tasks through CLI or MCP interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stealth browser automation can be used to bypass anti-bot controls or access protected sites without authorization.

Mitigation: Use only on authorized, lawful targets, confine runs to isolated environments, and require explicit permission before scraping protected sites.

Risk: The package controls a browser session and may expose local browsing context if run against a personal authenticated profile.

Mitigation: Use a dedicated browser profile or disposable environment, avoid authenticated personal profiles, pin and verify the npm package, and keep Chrome sandboxing enabled.

Risk: Lead-generation and contact-extraction workflows can create privacy, compliance, or abuse concerns.

Mitigation: Avoid bulk contact collection without explicit permission and review workflows against applicable laws, site terms, and internal data-handling policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexandre-leng/skills/agentbridge)
- [ClawHub Release Link](https://clawhub.ai/alexandre-leng/agentbridge)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands; AgentBridge commands can return text, JSON, CSV, screenshots, and saved files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May interact with live websites and browser sessions; the raw MCP command requires BRIDGE_MCP_ALLOW_RAW=1.]

## Skill Version(s):

3.3.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

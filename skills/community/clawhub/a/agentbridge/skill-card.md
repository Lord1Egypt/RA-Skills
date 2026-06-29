## Description: <br>
Agent-Browser-Bridge-AI provides anti-detection browser control for AI agents with DOM-first interactions, human-like timing, lead generation, extraction, and MCP integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexandre-leng](https://clawhub.ai/user/alexandre-leng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate browser navigation, page annotation, form interaction, web search, and structured extraction through CLI and MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides stealth browser automation for scraping, lead generation, and bypassing site defenses. <br>
Mitigation: Use only with explicit authorization for the sites and accounts being automated, and restrict activity to approved domains and permitted workflows. <br>
Risk: Use for unsolicited lead harvesting, protected-site scraping, or access-control bypass may violate policies, terms, or legal obligations. <br>
Mitigation: Avoid those uses, review target-site terms before deployment, and monitor the local bridge process during operation. <br>
Risk: The raw MCP browser command can run arbitrary bridge commands when enabled. <br>
Mitigation: Keep raw MCP disabled unless necessary, and enable it only in controlled environments with clear task boundaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexandre-leng/agentbridge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON, CSV] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime outputs may include text, JSON, CSV, and screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the agentbridge CLI and local bridge process; raw MCP commands should remain disabled unless explicitly needed.] <br>

## Skill Version(s): <br>
3.3.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

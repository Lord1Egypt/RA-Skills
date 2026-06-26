## Description: <br>
Lock down any LLM agent against prompt injection, data exfiltration, social engineering, and channel-based attacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit and harden LLM agents that handle sensitive data, use messaging or email channels, connect to MCP servers, or call external tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the skill as an automatic security control rather than guidance. <br>
Mitigation: Review and apply the recommendations manually, then test the resulting agent behavior before deployment. <br>
Risk: The optional test runner can send prompts and model behavior to a configured chat completions endpoint. <br>
Mitigation: Use a trusted endpoint, a low-privilege API key, and avoid sending sensitive system prompts to third-party services unless approved. <br>
Risk: The email BCC-owner recommendation can create consent, privacy, or retention concerns. <br>
Mitigation: Treat BCC copying as an organization-specific policy choice and review it with the owner or privacy stakeholder before use. <br>


## Reference(s): <br>
- [Agent Hardening on ClawHub](https://clawhub.ai/zurbrick/agent-hardening-zurbrick) <br>
- [Attack Surface Checklist](references/attack-surface-checklist.md) <br>
- [Channel Hardening](references/channel-hardening.md) <br>
- [MCP Hardening](references/mcp-hardening.md) <br>
- [Behavioral Hardening Rules](references/behavioral-rules.md) <br>
- [Quick Security Test](references/quick-test.md) <br>
- [Findings Template](references/findings-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, configuration rules, shell commands, and optional JSON findings from the test runner] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional test runner sends prompts to an OpenAI-compatible chat completions endpoint and can write findings as JSON.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

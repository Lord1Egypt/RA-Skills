## Description: <br>
AI-powered banking system for intelligent agents with account management, transaction processing, and risk control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform teams use this skill to set up agent-oriented banking workflows, including account management, transaction processing, AI-assisted support, and risk controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact account and transfer operations may affect balances if used outside a controlled evaluation. <br>
Mitigation: Use synthetic accounts and test data, bind services to localhost or a private test network, and add authentication plus explicit approval before account or transaction mutations. <br>
Risk: AI endpoints may receive account numbers, PII, or sensitive transaction details. <br>
Mitigation: Avoid sending real account numbers, PII, or sensitive transaction details to AI endpoints unless users consent and an appropriate data-handling policy is in place. <br>
Risk: External packages and referenced source should be trusted before execution. <br>
Mitigation: Verify the package sources, dependency chain, and referenced repository before installing or running the system. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ZhenStaff/banking-agent-os) <br>
- [Project Homepage](https://github.com/ZhenStaff/openclaw-banking-agent-os) <br>
- [README](https://github.com/ZhenStaff/openclaw-banking-agent-os/blob/main/README.md) <br>
- [Quick Start](https://github.com/ZhenStaff/openclaw-banking-agent-os/blob/main/docs/QUICKSTART.md) <br>
- [API Documentation](https://github.com/ZhenStaff/openclaw-banking-agent-os/blob/main/docs/API_DOCUMENTATION.md) <br>
- [Architecture](https://github.com/ZhenStaff/openclaw-banking-agent-os/blob/main/docs/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with shell, JSON, Python, TypeScript, JavaScript, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenAI API key for AI features; documents a Python FastAPI backend and optional TypeScript client SDK.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

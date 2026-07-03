## Description: <br>
Builds a complete multi-agent orchestration harness for an OpenClaw or similar agentic system, including orchestrator roles, specialist tiers, context-routing rules, model assignment, memory limits, communication channels, and implementation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plbirrell](https://clawhub.ai/user/plbirrell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to design, document, and hand off a coordinated fleet of AI agents with clear routing, memory, model, and communication rules. It is best suited for multi-agent systems large enough to need an orchestrator and tiered specialist roles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a real organization's agent roster, Slack channel patterns, memory layout, and operational setup in its templates. <br>
Mitigation: Replace the Decade Strategy, Tori, Paul, Slack, memory, and roster examples with sanitized placeholders or the user's own approved details before use. <br>
Risk: The skill includes high-impact setup guidance for editing OpenClaw configuration, checking Slack tokens, and installing or running a gateway service. <br>
Mitigation: Review commands and configuration changes before execution, test in a controlled workspace, and confirm token handling and service installation steps match the user's environment. <br>


## Reference(s): <br>
- [Read This First Template](references/read-this-first-template.md) <br>
- [Harness Architecture Template](references/architecture-template.md) <br>
- [Agent Profiles Template](references/agent-profiles-template.md) <br>
- [System Prompt Template](references/system-prompt-template.md) <br>
- [Implementation Guide Template](references/implementation-guide-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown document set with structured profiles, system prompts, configuration examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces five handoff-oriented documents unless the user requests a subset.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

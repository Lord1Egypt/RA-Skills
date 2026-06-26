## Description: <br>
Adam Framework provides a five-layer persistent memory and coherence architecture for OpenClaw agents using a local vault, memory search, neural graph recall, nightly reconciliation, and drift monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[strangeadvancedmarketing](https://clawhub.ai/user/strangeadvancedmarketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, agent operators, and technical teams use Adam Framework to add persistent local memory, boot-time identity, session recall, and coherence monitoring to OpenClaw-based assistants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local startup can keep an agent running with access to personal memory files. <br>
Mitigation: Run the startup script manually during evaluation, avoid elevated hidden auto-start where possible, and confirm the vault paths before enabling login startup. <br>
Risk: The memory vault and imported chat exports can contain sensitive personal or business history. <br>
Mitigation: Keep the vault out of public repositories and public sync folders, review or redact imports before ingestion, and limit memory search paths to intended directories. <br>
Risk: Nightly reconciliation may send selected memory or log content to Gemini. <br>
Mitigation: Disable reconciliation or use an approved provider for sensitive deployments, and review what logs and memory files are included before first run. <br>
Risk: Broad MCP or Telegram configuration can expose private memory through configured tools. <br>
Mitigation: Remove unused MCP integrations, disable Telegram unless required, replace wildcard access with an allowlist, and keep gateway token authentication enabled. <br>
Risk: API keys and tokens can be exposed if live configuration files are committed or logged. <br>
Mitigation: Store secrets in environment-backed configuration, replace placeholders locally, avoid command-line API keys, and do not commit live OpenClaw or SENTINEL configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/strangeadvancedmarketing/adam-framework) <br>
- [Adam Framework Repository](https://github.com/strangeadvancedmarketing/Adam) <br>
- [Human Setup Guide](https://github.com/strangeadvancedmarketing/Adam/blob/master/SETUP_HUMAN.md) <br>
- [AI Agent Setup Guide](https://github.com/strangeadvancedmarketing/Adam/blob/master/SETUP_AI.md) <br>
- [Live Proof Showcase](https://strangeadvancedmarketing.github.io/Adam/showcase/ai-amnesia-solved.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown setup guidance with inline shell commands, JSON configuration, and template file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for local setup and may guide changes to user-owned vault, OpenClaw, MCP, and automation configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

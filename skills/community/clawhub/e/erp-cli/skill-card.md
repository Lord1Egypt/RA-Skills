## Description: <br>
物达通 ERP helps an agent use `erp-cli` as a unified entry point for WindaKa property-management ERP operations and RAGFlow-backed knowledge-base search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingwenkai](https://clawhub.ai/user/xingwenkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents use this skill to answer property-management policy questions through the configured knowledge base and to inspect or operate WindaKa ERP records such as work orders, authentication state, configuration, projects, contacts, fees, and daily reports. Write actions are intended to be confirmed with the user before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad authenticated access to ERP and RAGFlow systems can expose or change business data beyond the user's immediate request. <br>
Mitigation: Install only for intended WindaKa ERP and RAGFlow use, use least-privilege accounts, and require explicit confirmation before ERP write actions. <br>
Risk: Overly broad routing may cause the skill to be invoked for questions that do not need ERP or knowledge-base access. <br>
Mitigation: Narrow invocation rules so the skill runs only for relevant property-management knowledge questions or explicit ERP operations. <br>
Risk: Credentials or API keys may be exposed if passed directly in command arguments or echoed in responses. <br>
Mitigation: Prefer interactive configuration for secrets, avoid placing API keys directly in command arguments, and do not display tokens, passwords, or API keys to users. <br>
Risk: The raw `api` fallback can bypass safer shortcut-specific guardrails. <br>
Mitigation: Review raw API fallback usage carefully, prefer documented shortcuts when available, and confirm the target method, path, and payload before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xingwenkai/skills/erp-cli) <br>
- [Global Reference](references/global-reference.md) <br>
- [Intent Guide](references/intent-guide.md) <br>
- [Knowledge Product Reference](references/products/knowledge.md) <br>
- [Workorder Product Reference](references/products/workorder.md) <br>
- [NPM Mirror Registry](https://registry.npmmirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command-output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command outputs are expected to use a JSON envelope with `ok`, `data`, and `error` fields; write operations should be previewed or confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

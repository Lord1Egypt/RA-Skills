## Description: <br>
Clarity is a Node.js MCP-native cognitive engine that adds structured reasoning, persistent memory, self-verification, PAD emotion analysis, and truth-kindness-beauty evaluation to agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Clarity as an MCP-native cognitive layer for structured reasoning, persistent memory, self-checking, and decision-quality evaluation in AI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports under-disclosed local runtime authority, persistence, broad memory retention, external model fallback, and possible self-modifying workflows. <br>
Mitigation: Install only in a contained environment until startup, shutdown, stored data, external LLM calls, and any self-updating or commit/push behavior are reviewed and explicitly approved. <br>
Risk: The skill may retain user or session data through persistent memory features. <br>
Mitigation: Review storage paths and retention behavior before use, avoid sensitive inputs until retention is understood, and clear or isolate local state between projects. <br>
Risk: Shell commands, generated code, and configuration guidance can affect the local environment. <br>
Mitigation: Review proposed commands and code before execution, run with least privilege, and prefer disposable workspaces for evaluation. <br>


## Reference(s): <br>
- [Clarity Skill Page](https://clawhub.ai/yun520-1/claude-clarity-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [System Requirements](artifact/SYSTEM_REQUIREMENTS.md) <br>
- [Security Policy](artifact/SECURITY.md) <br>
- [Security Audit Report](artifact/docs/security-audit-report-2026-06-13.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and text responses with code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and persist local state when installed as an MCP-backed cognitive engine.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

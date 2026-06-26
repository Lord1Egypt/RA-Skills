## Description: <br>
Preflight security scanner for AI coding agents that scans deployment configuration, skills and MCP servers, memory and session files, and agent configuration files for secrets, PII, prompt injection, dangerous patterns, and optional model behavior risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyiweio](https://clawhub.ai/user/xiaoyiweio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and AI-agent operators use this skill to run preflight security checks before installing skills, MCP servers, or project agent configuration. It helps identify exposed secrets or PII, prompt-injection patterns, unsafe hooks, insecure deployment posture, and optional model behavior risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner can inspect sensitive memory, session, credential, and configuration files, and generated reports may contain sensitive findings. <br>
Mitigation: Run static scans with --no-llm when local-only analysis is required, restrict report sharing, and treat generated reports as sensitive artifacts. <br>
Risk: Full OpenClaw scans can read or change OpenClaw settings. <br>
Mitigation: Back up or inspect ~/.openclaw/openclaw.json before running full scans and review the resulting changes or findings before continuing. <br>
Risk: The release includes bundled demo agent-rule files that intentionally contain unsafe examples. <br>
Mitigation: Do not copy or activate demo/awesome-ai-rules files unless deliberately testing unsafe examples in an isolated environment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/xiaoyiweio/deepsafe-scan) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Cross-platform evolution plan](artifact/docs/plan-cross-platform-evolution.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Guidance] <br>
**Output Format:** [Markdown, JSON, or HTML security reports with command-line output and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static scans can run locally without an API key; LLM-enhanced checks and model probes require configured credentials.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
OpenClaw security audit + prompt injection detector. Scans gateway/vulns/cron/PI patterns. Use for frenzy-proofing installs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Poolguy24](https://clawhub.ai/user/Poolguy24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use ClawShield to run local security audits, review prompt-injection indicators, and inspect local status and port findings before acting on the report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audit reports may include sensitive local snippets, session details, OpenClaw status, or local port information. <br>
Mitigation: Review report contents before sharing them and treat generated reports as local security artifacts. <br>
Risk: The release documentation advertises cron, Telegram or email alerting, and panel-server/config helpers that are not fully provided in the artifact. <br>
Mitigation: Treat those helper features as unimplemented unless separately supplied and reviewed; rely on the included local audit script for available behavior. <br>


## Reference(s): <br>
- [Frenzy risks & references](references/threats.md) <br>
- [OWASP GenAI LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) <br>
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) <br>
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) <br>
- [Obsidian Security Agentic AI Security](https://www.obsidiansecurity.com/blog/agentic-ai-security) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON report printed to stdout, with supporting shell and configuration instructions in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated locally and may include OpenClaw status, session details, local port information, and matched lines from memory or skill files.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

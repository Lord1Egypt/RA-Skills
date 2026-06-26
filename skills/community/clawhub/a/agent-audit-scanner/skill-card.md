## Description: <br>
Security scanner for OpenClaw skills. Detects prompt injection, credential leaks, unsafe code execution, MCP misconfigurations, privilege escalation, obfuscated shell commands, and social engineering patterns. Covers all 10 OWASP Agentic AI threat categories with 49+ detection rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HeadyZhang](https://clawhub.ai/user/HeadyZhang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to audit OpenClaw skills and OpenClaw configuration before enabling or operating them. It produces severity-tiered findings for prompt injection, credential exposure, unsafe execution, MCP misconfiguration, privilege escalation, obfuscated commands, and related agentic AI risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: One scan wrapper can automatically install the unpinned external agent-audit PyPI package during use. <br>
Mitigation: Install agent-audit yourself in a virtual environment, pin or review the package version first, and then run the scan locally. <br>
Risk: The skill reads local OpenClaw skill directories and OpenClaw configuration files during audits. <br>
Mitigation: Run it only in the intended local environment and review generated findings before acting on them. <br>
Risk: A clean scan result may miss issues outside the scanner's rules or confidence thresholds. <br>
Mitigation: Treat scanner output as a triage signal and pair it with manual review before enabling a skill. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/HeadyZhang/agent-audit) <br>
- [Common Threats in OpenClaw Skills](references/common-threats.md) <br>
- [OWASP Agentic AI Top 10 Agent Audit Rules](references/owasp-asi-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style scan guidance and terminal reports, with JSON available from the underlying agent-audit command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports findings using BLOCK, WARN, INFO, and CLEAN tiers.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

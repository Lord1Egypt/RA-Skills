## Description: <br>
Comprehensive AI agent security auditing skill covering prompt injection detection, permission boundary analysis, malicious skill scanning, credential leak detection, and runtime behavior monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and operators use this skill to audit AI agent configurations, installed skills, credentials, and runtime behavior before or during production deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects agent configurations, installed skills, credentials, and runtime behavior, so reports may contain sensitive paths or credential findings. <br>
Mitigation: Scope scans to the intended target and handle generated reports as sensitive security artifacts. <br>
Risk: Runtime monitoring requires access to the agent process and may observe tool, network, or file access behavior. <br>
Mitigation: Run monitoring only in authorized environments and review access boundaries before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/gaoqian-ai-security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown security audit report with risk scores, findings, and remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings may include file paths, line numbers, credential findings, and runtime behavior details.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

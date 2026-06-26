## Description: <br>
Outbound DLP for OpenClaw that uses hard regex blocks to prevent secrets and PII from leaving the machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Stanxy](https://clawhub.ai/user/Stanxy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use ClawWall to scan outbound agent tool calls for secrets, PII, and high-entropy strings before data leaves the local machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: All outbound OpenClaw tool calls are routed through the local scanner. <br>
Mitigation: Install and enable the skill only when this interception behavior is intended, and review the OpenClaw plugin configuration before use. <br>
Risk: The local service listens on port 8642 and may expose scan functionality if bound too broadly. <br>
Mitigation: Bind the service to 127.0.0.1 or firewall port 8642 before enabling it. <br>
Risk: Fail-open behavior can allow outbound calls through when the service is unreachable. <br>
Mitigation: Choose fail-open or fail-closed behavior deliberately based on the deployment risk tolerance. <br>
Risk: The local findings database stores scan metadata about detected findings. <br>
Mitigation: Protect the SQLite database and confirm that stored metadata is acceptable for the environment. <br>
Risk: The release depends on PyPI, GitHub, and npm installation steps. <br>
Mitigation: Verify the exact PyPI, GitHub, and npm release artifacts being installed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Stanxy/clawwall) <br>
- [Project repository](https://github.com/Stanxy/clawguard) <br>
- [Release v0.2.1](https://github.com/Stanxy/clawguard/releases/tag/v0.2.1) <br>
- [PyPI package](https://pypi.org/project/clawwall) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, YAML, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance focuses on local service installation, OpenClaw plugin configuration, policy settings, and interpreting scan outcomes.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata; artifact frontmatter states 0.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Pre-installation agentic sandboxing protocol. 5-layer defense: semantic neutralization, hard quarantine, kernel ground-truth, trusted output rendering, and sterile autopsy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[almohalhel1408](https://clawhub.ai/user/almohalhel1408) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security engineers use Black Fortress to evaluate third-party agent skills, generated code, and other untrusted features before installation or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner verdict is suspicious because the skill asks users to trust high-impact Docker and optional root workflows while some protections may be overstated or not fully scoped. <br>
Mitigation: Review before installing, run only on a disposable or tightly controlled host, and do not treat an approval result as a complete security guarantee. <br>
Risk: Firecracker/root mode and Docker configuration changes can affect the host environment. <br>
Mitigation: Avoid Firecracker/root mode unless independently verified for the target workload, and back up Docker configuration before applying credential-helper changes. <br>
Risk: Preserved sandbox artifacts may contain sensitive or risky data. <br>
Mitigation: Secure any preserved archive, limit access to it, and delete it when review is complete. <br>


## Reference(s): <br>
- [Black Fortress ClawHub release page](https://clawhub.ai/almohalhel1408/black-fortress) <br>
- [Publisher profile](https://clawhub.ai/user/almohalhel1408) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, json, files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local scripts that may create sanitized outputs and audit artifacts.] <br>

## Skill Version(s): <br>
1.1.10 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

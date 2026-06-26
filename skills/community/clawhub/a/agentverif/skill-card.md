## Description: <br>
AgentVerif scans OpenClaw skills for OWASP LLM Top 10 issues and supports signing, verification, tamper detection, and license revocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaymizuno](https://clawhub.ai/user/shaymizuno) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use AgentVerif to scan OpenClaw skills, sign release ZIPs, verify certificates, detect tampering, and revoke licenses when distribution must be controlled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan, sign, and verify operations can transmit skill ZIPs or license IDs to agentverif.com. <br>
Mitigation: Do not scan or sign archives containing secrets or data that cannot be shared with agentverif.com. <br>
Risk: Signing changes the supplied ZIP by adding signature metadata. <br>
Mitigation: Keep an unsigned copy when the original archive must be preserved. <br>
Risk: The revoke command uses AGENTVERIF_API_KEY. <br>
Mitigation: Use a scoped key, provide it only when revoking, and rotate it if exposure is suspected. <br>
Risk: The skill depends on the separate agentverif-sign Python package for core operations. <br>
Mitigation: Install only when the package and its network behavior are acceptable for the target environment. <br>


## Reference(s): <br>
- [ClawHub AgentVerif listing](https://clawhub.ai/shaymizuno/agentverif) <br>
- [AgentVerif documentation](https://agentverif.com/docs) <br>
- [AgentVerif homepage](https://agentverif.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text, JSON status messages, Markdown reports, and command-line exit codes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can return verification states such as VERIFIED, TAMPERED, UNSIGNED, EXPIRED, or REVOKED.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

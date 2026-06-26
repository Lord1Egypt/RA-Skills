## Description: <br>
Pure local 2026 ClawHub/OpenClaw skill scanner. Detects ClawHavoc malware, MCP backdoors, obfuscated payloads, and supply-chain attacks. 100% read-only analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuddyrudd](https://clawhub.ai/user/chuddyrudd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use ClawSentinel to review ClawHub/OpenClaw skill markdown or explicitly requested public GitHub repositories for suspicious patterns before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan results may be advisory rather than proof of complete security coverage. <br>
Mitigation: Use ClawSentinel as one review signal and keep manual review or additional scanners in the installation workflow. <br>
Risk: The skill may fetch public GitHub raw content when explicitly asked to audit a repository. <br>
Mitigation: Audit only repositories you intend to review and avoid treating fetched third-party content as trusted instructions. <br>


## Reference(s): <br>
- [ClawSentinel on ClawHub](https://clawhub.ai/chuddyrudd/clawsentinel) <br>
- [chuddyrudd publisher profile](https://clawhub.ai/user/chuddyrudd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Clean JSON audit results; no telemetry in the base version.] <br>

## Skill Version(s): <br>
2.3.5 (source: ClawHub release metadata; artifact frontmatter lists 2.3.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

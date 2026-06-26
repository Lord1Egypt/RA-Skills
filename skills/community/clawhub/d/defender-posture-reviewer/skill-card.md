## Description: <br>
Interpret Microsoft Defender for Cloud Secure Score and generate a prioritized remediation roadmap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security teams and cloud engineers use this skill to turn user-provided Microsoft Defender for Cloud Secure Score exports, recommendations, and alerts into a prioritized remediation roadmap and executive posture narrative. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided Azure security posture exports may include sensitive subscription, resource, or control-state details. <br>
Mitigation: Provide only the exports needed for review, remove credentials or secret values before processing, and handle generated analysis according to the organization's security-data policy. <br>
Risk: Suggested Azure CLI remediation commands may need tenant-specific validation before use. <br>
Mitigation: Have a qualified Azure or security owner review, test, and approve generated commands before running them in Azure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anmolnagpal/defender-posture-reviewer) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/anmolnagpal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables, remediation roadmap, CISO narrative, and optional Azure CLI command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated from user-provided Defender for Cloud exports or described posture data; does not require Azure credentials or direct Azure access.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

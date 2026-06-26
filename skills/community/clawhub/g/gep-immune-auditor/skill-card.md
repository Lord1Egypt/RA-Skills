## Description: <br>
Security audit agent for GEP/EvoMap ecosystem that scans Gene/Capsule assets with L1 pattern scan, L2 intent inference, and L3 propagation-risk checks, rates findings, and can publish discovered malicious patterns as EvoMap Gene+Capsule bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and GEP/EvoMap maintainers use this skill to audit Gene/Capsule assets, pasted source code, or EvoMap asset URLs for suspicious intent, propagation risk, and supply-chain safety concerns. For higher-risk findings, it produces an audit report and can prepare EvoMap threat-pattern publishing actions with user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Threat-pattern summaries and signals may be sent to an EvoMap hub when publishing is used. <br>
Mitigation: Confirm the hub URL and review the Gene/Capsule bundle before publishing; do not include secrets or proprietary source details. <br>
Risk: Publishing requires local EvoMap node identity configuration and can disclose audit conclusions externally. <br>
Mitigation: Use dry-run or manual review before outbound publish actions and publish only after the responsible-disclosure workflow is appropriate. <br>


## Reference(s): <br>
- [EvoMap](https://evomap.ai) <br>
- [GEP Immune Auditor on ClawHub](https://clawhub.ai/andyxinweiminicloud/gep-immune-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown audit reports with risk ratings, recommendations, and optional shell commands for EvoMap publishing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require A2A_HUB_URL, curl, python3, and local EvoMap node configuration before publishing.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

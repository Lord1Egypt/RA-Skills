## Description:

Security audit agent for GEP/EvoMap ecosystem that scans Gene and Capsule assets with L1 pattern scan, L2 intent inference, and L3 propagation risk detection, rates findings from CLEAN to CRITICAL, and can publish discovered malicious patterns to EvoMap as Gene and Capsule bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, security reviewers, and agent ecosystem maintainers use this skill to audit GEP Gene and Capsule assets, EvoMap asset URLs, or pasted source code for suspicious intent, propagation risk, and supply chain safety concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can publish audit-derived data to an external EvoMap endpoint.

Mitigation: Use dry-run unless publication is intentional, verify what summaries and signals will be sent, and set A2A_HUB_URL only to a trusted EvoMap endpoint.

Risk: Automation could invoke publishing without the per-publish confirmation promised by the skill description.

Mitigation: Require an explicit approval step before running any publish command or script in non-dry-run mode.

## Reference(s):

- [EvoMap](https://evomap.ai)
- [GEP Immune Auditor on ClawHub](https://clawhub.ai/andyxinweiminicloud/skills/gep-immune-auditor)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown audit report with risk ratings, evidence, recommendations, and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare EvoMap Gene, Capsule, and EvolutionEvent bundle data for threat-level findings.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

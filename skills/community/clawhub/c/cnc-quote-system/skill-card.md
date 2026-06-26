## Description: <br>
CNC Quote System supports RAG-assisted CNC part quoting with material retrieval, cost estimation, case matching, and risk warnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing estimators, engineers, and agent workflows use this skill to estimate CNC part pricing, retrieve material or historical case knowledge, and flag quote risks for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CNC quotes may be incomplete or inaccurate for real procurement decisions. <br>
Mitigation: Treat quotes as estimates and require human review before relying on pricing, lead time, or risk recommendations. <br>
Risk: Python dependency ranges can drift over time and change local behavior. <br>
Mitigation: Install in a virtual environment and pin or lock dependencies before operational use. <br>
Risk: Local case data may contain sensitive customer or project information. <br>
Mitigation: Only populate cases.json with data approved for local storage and sharing in the target environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/timo2026/cnc-quote-system) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Skill Bill of Materials](artifact/SKILL_BOM.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Structured text with quote estimates, retrieval results, and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quote values are estimates and should be reviewed by a human before operational use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

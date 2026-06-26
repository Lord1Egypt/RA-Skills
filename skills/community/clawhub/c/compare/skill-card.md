## Description: <br>
Rigorous comparisons with confidence parity, weighted criteria, and research depth tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users apply this skill when they need a structured, evidence-balanced comparison between products, tools, services, decisions, locations, people, investments, or content. The skill guides criteria weighting, research parity, confidence checks, scoring, caveats, and preference capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse locally stored comparison preferences, which may preserve past decision priorities. <br>
Mitigation: Review or clear preferences.md when prior preferences should not influence a new comparison. <br>
Risk: A comparison can be misleading if evidence depth, source quality, or data recency differs across items. <br>
Mitigation: Apply the skill's research parity and confidence checks before presenting scores, and explicitly caveat unresolved imbalances. <br>


## Reference(s): <br>
- [Compare skill page](https://clawhub.ai/ivangdavila/compare) <br>
- [Confidence levels](confidence.md) <br>
- [Default comparison criteria by domain](domains.md) <br>
- [Comparison traps](traps.md) <br>
- [User comparison preferences](preferences.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown comparison report with weighted score tables, confidence labels, caveats, and alternative-winner notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local comparison preference notes when the agent environment permits persistent memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

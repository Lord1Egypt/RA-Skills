## Description: <br>
Helps detect when AI agent skills silently mutate across inheritance chains so teams can identify when inherited skills have drifted beyond their original audit scope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and marketplace operators use this skill to trace AI skill lineage, compare versions, score capability drift, and decide whether a re-audit is warranted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drift reports are advisory and may misclassify or overstate semantic changes. <br>
Mitigation: Use the report to prioritize review, then confirm findings with human security review before changing audit or release status. <br>
Risk: Marketplace identifiers or lineage URLs supplied to the skill may be queried with network tools. <br>
Mitigation: Provide only approved public or non-sensitive identifiers and URLs, and review outbound queries in restricted environments. <br>
Risk: Lineage reconstruction depends on the quality of marketplace fork and version metadata. <br>
Mitigation: Validate source lineage metadata before relying on the drift score or re-audit recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/evolution-drift-detector) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/andyxinweiminicloud) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown drift analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes lineage trees, per-generation diff summaries, capability drift scores, mutation classifications, and re-audit recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

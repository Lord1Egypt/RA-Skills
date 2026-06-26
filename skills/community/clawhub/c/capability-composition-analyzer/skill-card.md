## Description: <br>
Helps identify dangerous capability combinations that emerge when agent skills are composed, including exfiltration or compromise paths that may not be visible in individual skill audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use this skill to assess whether multiple agent skills compose into dangerous emergent capabilities, permission gaps, exfiltration paths, or inherited compromise paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discusses exfiltration and remote code execution patterns in defensive examples, which could be misunderstood if read outside the context of security review. <br>
Mitigation: Use the skill only to analyze provided skill lists, capability metadata, or permission declarations, and review generated recommendations before acting on them. <br>
Risk: The artifact metadata declares curl and python3 even though the visible workflow is documentation-only. <br>
Mitigation: Install with least privilege and provide only the skill composition data intended for analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/capability-composition-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown risk report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dangerous pair inventory, emergent capability surface, inheritance amplification, permission declaration gaps, composition risk level, and recommended actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

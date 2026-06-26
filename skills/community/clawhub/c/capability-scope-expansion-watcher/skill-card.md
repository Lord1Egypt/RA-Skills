## Description: <br>
Helps detect incremental capability scope expansion across skill versions, including risk-class contradiction detection in version 1.1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use this skill to examine whether a skill's permissions and declared capabilities have expanded across versions in ways that increase attack surface or contradict its stated risk class. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Providing a full installed skill list can disclose local agent configuration details. <br>
Mitigation: Prefer specific skill IDs or version ranges, and share a full installed skill list only when that disclosure is acceptable. <br>
Risk: Scope expansion analysis depends on preserved version history and accurate capability declarations. <br>
Mitigation: Treat missing or inconsistent historical metadata as a review limitation and corroborate findings with registry records, changelogs, and capability declarations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andyxinweiminicloud/capability-scope-expansion-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown scope expansion report with per-version deltas, cumulative analysis, alignment assessment, and an expansion verdict.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recommended actions for reviewing or restricting future capability expansion.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

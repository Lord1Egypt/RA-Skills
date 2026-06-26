## Description: <br>
Compare draft agreements, highlight risky clause changes, and generate a negotiation checklist with plain-language explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Contract reviewers, operators, and business teams use this skill to compare old and new agreement drafts, identify material clause changes, and prepare negotiation checklists for counsel review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contract analysis can be incomplete or legally incorrect if used as a final legal determination. <br>
Mitigation: Use the skill as operational review support and have qualified counsel review conclusions before relying on them. <br>
Risk: The local diff helper can overwrite an existing file when the output path already exists. <br>
Mitigation: Choose the output path deliberately, prefer preview or draft mode, and review the generated diff before using it. <br>
Risk: Contract text may contain confidential or restricted information. <br>
Mitigation: Provide only agreements the user is authorized to analyze and follow the organization's confidentiality rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/contract-redline-navigator) <br>
- [README](README.md) <br>
- [High-Risk Clause Signals](resources/risk_clauses.md) <br>
- [Clause diff helper](scripts/clause_diff.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with clause summaries, negotiation checklist items, plain-language explanations, and optional diff output from a local Python helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper accepts explicit old and new file paths and writes a markdown diff to the selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

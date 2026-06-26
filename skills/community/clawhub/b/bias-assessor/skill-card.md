## Description: <br>
Add bias/risk-of-bias assessment fields to an extraction table and populate them consistently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and review authors use this skill after a systematic-review extraction table exists to add consistent risk-of-bias columns and concise supporting notes before synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes broader research-pipeline tooling beyond the advertised bias-table updater, including tooling that can route work, execute local scripts, and modify workspace files. <br>
Mitigation: Install it only when that broader toolkit is intended; otherwise use a package limited to the SKILL.md workflow, run in a disposable workspace copy, and inspect diffs to papers/extraction_table.csv, UNITS.csv, STATUS.md, DECISIONS.md, and output/ before relying on results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/WILLOSCAR/bias-assessor) <br>
- [Publisher profile](https://clawhub.ai/user/WILLOSCAR) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Guidance] <br>
**Output Format:** [Updated CSV table with low, unclear, or high ratings and concise notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates papers/extraction_table.csv when the expected table exists] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

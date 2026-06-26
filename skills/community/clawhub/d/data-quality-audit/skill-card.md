## Description: <br>
Audits a completed CN banker deliverable by independently cross-checking hard numbers against separate data sources and applying sanity rules before emitting PASS, FLAG, or FAIL findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and agent operators use this skill after a banker deliverable is drafted to verify sourced financial figures, identify cross-source conflicts, and decide whether the deliverable can be shipped or needs manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow writes audit-report.md and audit-raw.json into the user-selected deliverable directory, which may overwrite existing audit files. <br>
Mitigation: Confirm the target path and check for existing audit-report.md or audit-raw.json before running the audit. <br>
Risk: The audit depends on external data-source lookups, so missing or unavailable second sources may produce FLAG results rather than definitive failures. <br>
Mitigation: Treat single-source-unverifiable and second-source-unavailable findings as manual review items and re-fetch from an independent source when available. <br>


## Reference(s): <br>
- [Common-sense audit rules](artifact/references/common-sense-rules.yaml) <br>
- [ClawHub skill page](https://clawhub.ai/jackdark425/data-quality-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Text verdict plus Markdown audit report and JSON raw audit data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes audit-report.md and audit-raw.json in the selected deliverable directory.] <br>

## Skill Version(s): <br>
0.8.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Compares two BOM spreadsheets and identifies added, removed, and changed material items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongjie666888](https://clawhub.ai/user/yongjie666888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, manufacturing engineers, and procurement teams use this skill to compare old and new BOM CSV or XLSX files during design changes, supplier checks, purchasing-to-engineering consistency reviews, and version upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Node.js script against BOM files and uses the xlsx dependency to parse spreadsheets. <br>
Mitigation: Install xlsx from a trusted source, run the script only on intended BOM files, and avoid pointing it at unrelated sensitive files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yongjie666888/bom-compare-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, Shell commands] <br>
**Output Format:** [Plain text BOM comparison report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local CSV or XLSX BOM files selected by the user and reports additions, removals, field changes, quantity changes, and item-count totals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

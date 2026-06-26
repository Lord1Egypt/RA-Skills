## Description: <br>
Calculates algae feeding amounts from daily aquaculture reports by parsing workshop, pool range, strain, larval day, and AM/PM feeding period against bundled feeding standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheney87](https://clawhub.ai/user/cheney87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aquaculture operators and agents use this skill to parse algae-feeding daily reports and generate per-pool feeding quantities grouped by algae type, workshop, pool range, and feeding period. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unusual report formatting or date edge cases may lead to incorrect feeding calculations. <br>
Mitigation: Test representative daily reports and review generated quantities before using the results operationally. <br>
Risk: Bundled feeding standards may not match a farm's current operating procedure. <br>
Mitigation: Confirm the feeding-standard reference files match the current procedure before relying on the calculated volumes. <br>


## Reference(s): <br>
- [Algae Feeding Standard](references/algae-feeding-standard.md) <br>
- [Daily Report Parsing Guide](references/parsing-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Structured text report with Markdown-compatible line breaks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports feeding quantities in liters per pool and grouped total volumes for small and large chain algae.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

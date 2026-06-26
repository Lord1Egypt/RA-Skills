## Description: <br>
Standardizes A-share portfolio screenshots or holding lists into a portfolio work packet with positions, weights, concentration, thematic exposure, execution constraints, and missing-data flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minguncle](https://clawhub.ai/user/minguncle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn portfolio screenshots or pasted holding lists into a structured diagnostic packet before any later rebalancing or trading workflow. It focuses on confirmed account data, position weights, concentration, theme exposure, constraints, and unresolved information gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio screenshots and holding lists can expose sensitive financial information. <br>
Mitigation: Crop or redact account numbers, personal identifiers, broker metadata, QR codes, and unrelated screen content before sharing. <br>
Risk: A diagnostic portfolio packet could be mistaken for final investment or trading advice. <br>
Mitigation: Use the output as portfolio structure and diagnostic context, and require current market context before any actionable recommendation. <br>
Risk: Unclear screenshots or incomplete lists can lead to incorrect portfolio metrics if gaps are guessed. <br>
Mitigation: Extract only confirmed fields, mark missing or uncertain values, and avoid inferring unreadable account or position data. <br>


## Reference(s): <br>
- [Calibration Template](artifact/references/calibration-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/minguncle/a-share-portfolio-calibrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown portfolio packet with tables and bullet lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes account snapshot, standardized holdings table, concentration metrics, theme and style exposure, key constraints, and pending information gaps; not direct investment or trading advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

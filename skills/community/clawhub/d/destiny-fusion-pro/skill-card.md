## Description: <br>
Destiny Fusion Pro generates offline Ziwei Doushu and Bazi consultation reports from birth details, combining unified calculation rules, dual-system cross-checking, optional chart images, and markdown or JSON deliverables for yearly outlooks, decade luck cycles, relationships, career, wealth, and risk themes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spyfree](https://clawhub.ai/user/spyfree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate offline Ziwei Doushu and Bazi consultation reports from birth date, birth time, gender, year, timezone, and longitude inputs. The skill supports human-readable destiny analysis and structured automation output for yearly outlooks, decade luck cycles, relationships, career, wealth, and risk themes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python and optional Node-based calculation code on birth details provided by the user. <br>
Mitigation: Install dependencies from trusted sources, review the local scripts before running them, and provide only birth details you are comfortable processing locally. <br>
Risk: Generated chart files may be written to disk and can include sensitive birth inputs in chart metadata or visible labels. <br>
Mitigation: Confirm the chart output path, avoid shared directories for private reports, and delete generated files when they are no longer needed. <br>
Risk: Timezone, longitude, and birth-time boundary choices can materially change chart calculations and downstream interpretation. <br>
Mitigation: Confirm timezone and longitude settings before relying on a report, and use dual-plate comparison when birth time is near a boundary. <br>
Risk: Astrology-style interpretation can be mistaken for professional advice. <br>
Mitigation: Use the output as analysis and reflection only; do not treat it as medical, legal, or investment advice. <br>


## Reference(s): <br>
- [Destiny Fusion Pro ClawHub page](https://clawhub.ai/spyfree/destiny-fusion-pro) <br>
- [Ziwei Methodology](references/ziwei-methodology.md) <br>
- [Market Positioning](references/positioning.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown or JSON consultation report, with optional SVG or JPG chart file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-first offline workflow; optional chart export should not block report generation.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Calculates lunar phases, Moon transits, aspects to natal planets, lunar days, personal solar-lunar phases, and chart/text analysis using Swiss Ephemeris. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dynamicsalex](https://clawhub.ai/user/dynamicsalex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate bilingual lunar astrology metrics for a birth profile and target date, then produce text, JSON, or chart output for entertainment and educational interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a bundled Windows native Swiss Ephemeris binary renamed as a data file. <br>
Mitigation: Review or replace the bundled binary and run the skill in a sandboxed Windows environment before trusting generated output. <br>
Risk: The renderer may install Pillow if it is missing. <br>
Mitigation: Preinstall dependencies from trusted sources and restrict package installation during execution. <br>
Risk: Generated charts include a default donation QR image. <br>
Mitigation: Review or replace the bundled QR frame before sharing generated charts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dynamicsalex/skills/astro-lunar-insights) <br>
- [Publisher profile](https://clawhub.ai/user/dynamicsalex) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output may be plain text, JSON, or PNG chart files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual RU/EN output; Windows x64 runtime; generated charts include a bundled default donation QR image.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Calculate a person's Four Pillars (BaZi / Eight Characters) from birth date and time using sexagenary-cycle offsets from one trusted reference datetime that already has known year/month/day/hour pillars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wingchiu](https://clawhub.ai/user/wingchiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to calculate BaZi pillars, Eight Characters, DaYun cycles when gender is provided, and the current LiuNian Ganzhi from a birth datetime and timezone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Python script depends on lunar_python for DaYun solar-term calculations. <br>
Mitigation: Review and verify the lunar_python dependency before installing or running the skill in an agent environment. <br>
Risk: BaZi results depend on the selected reference datetime, anchor quality, and boundary conventions. <br>
Mitigation: Use verified anchors and compare outputs against a trusted almanac source before relying on results. <br>


## Reference(s): <br>
- [Anchor Requirements](references/method.md) <br>
- [Verified Reference](references/reference-verified.json) <br>
- [Reference Template](references/reference-template.json) <br>
- [Anchor Template](references/anchors-template.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/wingchiu/bazi-calculator) <br>
- [Publisher Profile](https://clawhub.ai/user/wingchiu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local birth-chart calculation output including pillars, Eight Characters, current LiuNian, and optional DaYun details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

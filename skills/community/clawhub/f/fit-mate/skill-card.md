## Description: <br>
Fit-Mate helps agents provide fitness coaching for workout plans, meal guidance, daily logging, recovery tracking, smartwatch analysis, and weekly PDF progress reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tankeito](https://clawhub.ai/user/tankeito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to set up and operate a personal fitness coaching workflow that creates training plans, meal suggestions, logs nutrition, hydration, sleep, and workouts, reviews progress, and produces weekly PDF reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive fitness, food, sleep, weight, injury, medication, and wearable data locally. <br>
Mitigation: Use only in an environment where local skill data storage is acceptable, limit file access to the skill data directory, and review stored files before sharing or exporting them. <br>
Risk: The PDF report feature may create a local Python environment and download an unpinned ReportLab dependency from pip. <br>
Mitigation: Disable or avoid the PDF feature unless dependency installation is acceptable, or preinstall and pin a reviewed ReportLab version in a controlled environment. <br>
Risk: The coaching persona is not verified as a licensed medical or nutrition professional. <br>
Mitigation: Treat recommendations as general fitness guidance, keep the skill's medical escalation boundaries in place, and seek qualified professional care for medical, injury, eating disorder, pregnancy, postpartum, or urgent symptom concerns. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tankeito/fit-mate) <br>
- [Data Schema Reference](references/data-schema.md) <br>
- [Training Knowledge Reference](references/training.md) <br>
- [Regional Nutrition Intelligence](references/nutrition-regions.md) <br>
- [Smartwatch / Fitness Tracker Analysis Reference](references/watch-analysis.md) <br>
- [Weekly PDF Report Template](references/report-template.md) <br>
- [Coach Rex Identity & Communication](references/persona.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses, JSON-backed local records, and optional PDF report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local fitness profile, plan, log, cache, and weekly report files under the skill data directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

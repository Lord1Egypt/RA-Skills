## Description: <br>
Diet logging and nutrition analysis assistant for recording meals, estimating 30+ nutrients, and producing daily, weekly, or monthly nutrition summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sj13818161942](https://clawhub.ai/user/sj13818161942) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to log meals, estimate nutrient intake from a local food database, and review diet summaries across daily, weekly, or monthly periods. The output is for general nutrition tracking and should not be treated as medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal logs can contain sensitive dietary or health-adjacent personal information stored on disk. <br>
Mitigation: Tell users that records are saved locally and advise them to review or delete references/meal_log.json when they do not want a long-term dietary record. <br>
Risk: Nutrient values are estimates based on a food database snapshot and may differ from actual intake. <br>
Mitigation: Present nutrition analysis as general reference information and avoid using it for diagnosis, treatment, or medical decision-making. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sj13818161942/diet-log) <br>
- [LuckyHookin foodwake nutrition data source](https://github.com/LuckyHookin/foodwake) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown nutrition reports with JSON meal records and statistics from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local references/meal_log.json file containing meal history.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
AI Running Coach helps runners create marathon and half-marathon training plans, analyze TCX/GPX running data, calculate pace and heart-rate zones, and draft race strategies from VDOT and periodized-training references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kinsonhu123-mkll](https://clawhub.ai/user/kinsonhu123-mkll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to draft running plans, calculate training paces and heart-rate zones, summarize GPX/TCX workout files, and prepare marathon race pacing and fueling guidance. Its outputs should be reviewed as coaching support rather than medical, clinical, or safety-critical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated mileage, pace, heart-rate, and race-fueling guidance may be inaccurate or unsafe for a runner's health, training history, or medical condition. <br>
Mitigation: Treat outputs as draft coaching support and confirm important plans with a qualified coach or clinician, especially for injury history, cardiovascular issues, diabetes, electrolyte concerns, GI problems, or caffeine sensitivity. <br>
Risk: TCX or GPX files can contain sensitive route and location history. <br>
Mitigation: Upload or analyze route files only when sharing those locations is acceptable, and remove location traces when they are not needed for the task. <br>
Risk: The artifact includes local scripts that parse user-provided files and calculate training outputs from simplified formulas. <br>
Mitigation: Run scripts in a controlled local environment and review generated JSON or text before using it for training decisions. <br>


## Reference(s): <br>
- [Training Zones](references/training-zones.md) <br>
- [Workout Types](references/workout-types.md) <br>
- [Race Strategies](references/race-strategies.md) <br>
- [Weekly Plan Template](assets/weekly-plan-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kinsonhu123-mkll/airunningcoach) <br>
- [Publisher Profile](https://clawhub.ai/user/kinsonhu123-mkll) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text coaching guidance with optional inline shell commands and JSON outputs from local Python scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May parse local TCX or GPX activity files and may generate pace zones, heart-rate zones, weekly plans, race strategies, and training recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

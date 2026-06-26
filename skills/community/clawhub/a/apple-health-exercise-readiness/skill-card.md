## Description: <br>
Analyzes Apple Health export data for a selected day to assess exercise readiness and recommend heavy, moderate, light, or rest activity with supporting detail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lynnshaw](https://clawhub.ai/user/lynnshaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and wellness-focused developers use this skill to run a local Python analysis of Apple Health exports and convert sleep, HRV, heart-rate, blood-oxygen, respiration, and activity signals into an exercise intensity recommendation. It helps agents explain the readiness score, highlight risk signals, and avoid presenting the result as a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exercise readiness guidance may be mistaken for a medical diagnosis or treatment recommendation. <br>
Mitigation: Present the output as wellness guidance only, preserve the skill's no-diagnosis constraint, and advise medical consultation for persistent abnormal readings or symptoms. <br>
Risk: Apple Health exports contain sensitive personal health data. <br>
Mitigation: Run the analyzer locally, avoid unnecessary sharing of export files or generated reports, and review outputs before disclosing them. <br>
Risk: Missing, unsynced, or insufficient baseline data can make the readiness score less reliable. <br>
Mitigation: Confirm the export source and target date, call out missing metrics or absent 30-day baselines, and avoid overconfident recommendations when data is incomplete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lynnshaw/apple-health-exercise-readiness) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional JSON analyzer output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consumes a local Apple Health export ZIP path and optional date/output flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Rebuild a body that's been sitting in a chair for years. Fix posture, build functional strength, and recover mobility. No gym required. For people who are deconditioned, overweight, or in pain from desk work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howtousehumans](https://clawhub.ai/user/howtousehumans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to assess desk-work deconditioning, choose a safe starting phase, follow progressive mobility and bodyweight routines, and set posture or workout reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring workout or posture reminders may be enabled at unwanted times or persist longer than the user intends. <br>
Mitigation: Require deliberate opt-in, let the user choose reminder times, and tell the user how to pause or delete reminders. <br>
Risk: Inferring whether the user is at a desk could create unnecessary monitoring or incorrect reminder triggers. <br>
Mitigation: Do not infer desk presence automatically; use only user-confirmed schedules or explicit user input. <br>
Risk: Fitness guidance may be unsuitable when pain worsens or a user has an unresolved medical issue. <br>
Mitigation: Start with gentle restoration, avoid high-impact or heavy lifting for deconditioned users, and recommend a doctor or physical therapist when pain persists or worsens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/howtousehumans/fitness-for-desk-workers) <br>
- [Physical Activity Guidelines for Americans](https://health.gov/our-work/nutrition-physical-activity/physical-activity-guidelines) <br>
- [NIH National Institute on Aging: Exercise and Physical Activity](https://www.nia.nih.gov/health/exercise-and-physical-activity) <br>
- [Cochrane Library](https://www.cochranelibrary.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with assessment checklists, exercise routines, reminder schedules, and YAML agent state examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose recurring workout and posture reminders using calendar and filesystem tools when the user opts in.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

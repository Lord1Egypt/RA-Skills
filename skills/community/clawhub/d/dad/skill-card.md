## Description: <br>
Parenting co-pilot for fathers that summarizes child care updates, coordinates schedules, tracks bonding moments, suggests age-appropriate activities, and reminds users it is not medical advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realteamprinz](https://clawhub.ai/user/realteamprinz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents and caregivers use this skill to help fathers catch up on child care events, coordinate routines, record parenting observations, and choose practical activities from locally stored family notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Family schedules, child routines, and parenting observations may be sensitive when saved in local plain-text files. <br>
Mitigation: Confirm the family is comfortable with local storage, avoid saving unnecessary sensitive details, and delete ~/.dad-skill/family/ to remove stored data. <br>
Risk: The skill discusses child care routines and could be mistaken for medical guidance. <br>
Mitigation: Keep responses practical and non-medical, and direct health concerns to a pediatrician. <br>
Risk: Sharing data with companion mom.skill may expose family notes beyond the expected parent workflow. <br>
Mitigation: Review companion skill data-sharing expectations before syncing or revealing family details. <br>


## Reference(s): <br>
- [Dad.skill ClawHub listing](https://clawhub.ai/realteamprinz/dad) <br>
- [Age-Appropriate Activities Reference](references/age-activities.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown and plain-text guidance with local file paths and log templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses parent-provided observations and local Markdown/JSONL files; does not provide medical advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

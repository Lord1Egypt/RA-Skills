## Description: <br>
Fitbot provides personal fitness coaching for training, workouts, programs, progression, and accountability by onboarding users, building custom programs, coaching sessions, and adapting on the fly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[conmeara](https://clawhub.ai/user/conmeara) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use Fitbot to create and maintain personalized fitness programs, log workouts, adapt sessions around constraints or pain, and receive accountability-oriented coaching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores health-adjacent fitness profile data and workout history in local workspace files. <br>
Mitigation: Confirm which files will be created or updated, avoid storing sensitive medical details, and review local records before relying on or sharing them. <br>
Risk: The skill can suggest persistent reminder automation through cron or heartbeat setup. <br>
Mitigation: Allow reminder automation only after reviewing the exact schedule, command, storage location, and removal steps. <br>
Risk: Fitness coaching may adapt workouts around pain without enough clinical context. <br>
Mitigation: Do not use the skill for diagnosis or clinical decisions; seek professional care for medical symptoms and review pain-related adjustments carefully. <br>


## Reference(s): <br>
- [Fitbot ClawHub page](https://clawhub.ai/conmeara/fitbot) <br>
- [Fitbot Onboarding](references/onboarding.md) <br>
- [Program Design Guide](references/program-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown coaching guidance, workspace markdown files, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local fitness profile, program, and workout log files; may propose scheduled reminder setup when requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

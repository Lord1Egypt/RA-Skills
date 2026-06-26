## Description: <br>
FTPilot helps an agent provide endurance cycling coaching with Intervals.icu athlete, wellness, activity, power curve, and workout-planning data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuai007](https://clawhub.ai/user/yuai007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cyclists, coaches, and training-focused agents use FTPilot to analyze Intervals.icu training data, assess recovery and fitness, recommend daily or weekly workouts, and format workout descriptions for Intervals.icu calendar events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Intervals.icu API key and athlete ID, which may expose private training and wellness data if mishandled. <br>
Mitigation: Provide credentials only in the intended runtime environment, limit access to trusted agents, and protect the API key as sensitive user data. <br>
Risk: Generated workout or calendar-event guidance may be inappropriate if the athlete data is stale, incomplete, or misread. <br>
Mitigation: Review generated workouts before creating calendar events and follow the recovery-first risk controls in the skill when fatigue, HRV, sleep, or recent load indicate risk. <br>


## Reference(s): <br>
- [ClawHub FTPilot release page](https://clawhub.ai/yuai007/ftpilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown training assessment, recommendation, workout steps, and notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Intervals.icu workout syntax and specific FTP percentages, watts, durations, and recovery notes.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

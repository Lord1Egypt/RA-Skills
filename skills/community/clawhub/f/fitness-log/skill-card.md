## Description: <br>
Fitness Log tracks workouts, body weight, progress, history, streaks, personal bests, and simple workout plans using local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to record workouts and body weight, review recent activity and statistics, export local fitness data, and generate simple goal-based workout plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted workout inputs can cause unintended local Python execution in the bundled shell script. <br>
Mitigation: Review before installing, avoid untrusted or unusual command input, and fix the script to pass values to Python through arguments, environment variables, or JSON serialization. <br>
Risk: Workout and weight records are stored locally in $HOME/.fitness. <br>
Mitigation: Treat the local fitness directory as personal data and back up or remove it according to the user's privacy needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/fitness-log) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, CSV, Guidance] <br>
**Output Format:** [Plain text command output with optional CSV or JSON export.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores workout JSON and weight CSV locally under $HOME/.fitness by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Daily English learning with spaced repetition - built-in A1-B2 word bank, new words daily, quiz mode (MCQ/fill-in/spelling), streak tracking, and level progression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
English learners and agents supporting them use this skill to run daily vocabulary study, generate quizzes, track streaks and progress, and manage optional daily reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local study profile records userId, name, level, streak, preferences, and word progress. <br>
Mitigation: Use a non-sensitive userId on shared machines or shared channels, and treat the local data/users files as personal study data. <br>
Risk: Enabling push reminders schedules recurring messages to the selected channel. <br>
Mitigation: Review the reminder time and channel before enabling push, and use the status or off command to audit or disable reminders. <br>


## Reference(s): <br>
- [English Daily ClawHub page](https://clawhub.ai/jiajiaoy/english-daily) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and JSON-like scheduler directives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local study prompts, quiz content, progress summaries, and optional reminder configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

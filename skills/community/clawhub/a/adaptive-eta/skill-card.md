## Description: <br>
Adaptive Eta prompts an assistant to estimate duration before longer tasks, provide progress updates, and use a local timer helper to track elapsed time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanghe1941](https://clawhub.ai/user/yanghe1941) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to make long-running assistant tasks more transparent by requiring upfront ETAs and follow-up progress updates when work exceeds expectations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add frequent ETA and progress-update behavior to longer tasks. <br>
Mitigation: Install it only when that communication pattern is desired for the target agent workflow. <br>
Risk: The timer helper writes a temporary local state file while tracking elapsed time. <br>
Mitigation: Run it in an environment where creating and deleting the local timer state file is acceptable, and stop the timer after task completion. <br>
Risk: The documentation mentions cron-based reminders, but server security guidance says the artifacts only show manual timer commands. <br>
Mitigation: Treat the skill as a manual start/check/stop timer workflow unless separate cron evidence is reviewed. <br>


## Reference(s): <br>
- [Adaptive Eta ClawHub page](https://clawhub.ai/yanghe1941/adaptive-eta) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text progress updates with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and remove a local .timer_state.json file while tracking task elapsed time.] <br>

## Skill Version(s): <br>
0.2.5 (source: server release evidence; artifact _meta.json lists 0.2.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

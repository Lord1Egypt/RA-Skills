## Description: <br>
User behavior correction skill triggered by fix-prefixed feedback that analyzes the mistake, improves the relevant prompt, memory, rule, agent, or hook to prevent recurrence, and fixes the current issue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to respond to behavior-correction feedback by performing root-cause analysis, updating the relevant prompt, memory, rule, or hook, and then completing the original work with verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change persistent agent behavior and repository or PR state from broad feedback triggers. <br>
Mitigation: Use explicit fix invocations, review persistent changes before allowing them, and avoid installing it where global rules, hooks, or GitHub PR metadata should not be changed automatically. <br>
Risk: Prompt, memory, rule, hook, task, or PR-body updates can introduce incorrect or overly broad behavior changes. <br>
Mitigation: Use the documented plan mode or review gates for complex changes, and verify proposed persistent changes before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/fix) <br>
- [Behavior discipline guide](artifact/behavior-discipline.md) <br>
- [Step 2 prompt improvement guide](artifact/step2-improvement.md) <br>
- [Step 3 resume guide](artifact/step3-resume.md) <br>
- [Step 4 wrap-up guide](artifact/step4-wrapup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with checklists, command snippets, and proposed or applied file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify persistent prompt, memory, hook, task, repository, or PR metadata when invoked.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata and CHANGELOG, released 2026-06-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

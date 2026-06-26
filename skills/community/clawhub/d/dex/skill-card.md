## Description: <br>
Dex Task Tracking helps agents create, track, inspect, update, and complete async or multi-step tasks with local JSON task files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gricha](https://clawhub.ai/user/gricha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to keep async work, PR reviews, background jobs, and multi-step coding tasks visible across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local command named dex may not be the intended task tracker. <br>
Mitigation: Confirm the installed dex command is the expected task tracker before following the skill's command examples. <br>
Risk: Task descriptions and context are saved locally under .dex/tasks/ and may contain sensitive information if entered by the user. <br>
Mitigation: Avoid storing secrets, credentials, or sensitive operational details in task descriptions or context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gricha/dex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of the local dex CLI; task records are stored as JSON files under .dex/tasks/.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Get To Know You helps an OpenClaw agent collect user work preferences and background through guided questions, update profile or configuration files after confirmation, and standardize feedback or skill-optimization requests into a confirm-before-execution workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzzanezhou0829](https://clawhub.ai/user/zzzanezhou0829) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to build a durable assistant profile from work details, preferences, and communication habits. They also use it to make negative feedback and skill-optimization requests follow a clarify, plan, confirm, execute workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects personal and work-profile details that may become durable assistant context. <br>
Mitigation: Avoid sharing confidential personal or organizational information, and review proposed profile entries before they are written. <br>
Risk: Persistent updates to AGENTS.md, SOUL.md, MEMORY.md, USER.md, or TOOLS.md can shape future agent behavior. <br>
Mitigation: Back up or monitor those files so unwanted profile entries can be removed or corrected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zzzanezhou0829/get-to-know-you) <br>
- [Information Collection Question Bank](references/question_bank.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and configuration-file update summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or append profile and configuration updates after user confirmation; the collector script can persist collection progress.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

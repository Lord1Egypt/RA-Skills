## Description: <br>
Deprecated migration note for the former Agent Token Usage UI skill, which has been merged into agent-token-usage v0.2.0+. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[symbolstar](https://clawhub.ai/user/symbolstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this deprecated package to find the migration path from agent-token-usage-ui to the main agent-token-usage skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing this deprecated package is unnecessary unless the user needs its migration note. <br>
Mitigation: Install the main agent-token-usage skill instead when the goal is to add or manage the token usage UI. <br>
Risk: The migration path asks users to run a script from the separate agent-token-usage package that changes UI behavior and adds a launchd refresh job. <br>
Mitigation: Review the separate agent-token-usage skill and its apply-ui.sh script before running the migration command. <br>


## Reference(s): <br>
- [agent-token-usage migration target](https://clawhub.com/skills/agent-token-usage) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash code block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deprecated documentation-only migration guidance; no executable code is bundled in this skill.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

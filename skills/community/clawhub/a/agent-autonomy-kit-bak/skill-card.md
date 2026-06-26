## Description: <br>
Helps agent operators turn a reactive AI agent into a proactive worker using a persistent task queue, heartbeat routine, and scheduling guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a task queue, proactive heartbeat routine, and scheduled operating pattern so an AI agent can keep working between direct prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended autonomous work can make broad file changes, team posts, or scheduled progress without enough human oversight. <br>
Mitigation: Keep the task queue limited to trusted, low-risk tasks; require human approval for public posts, account actions, destructive changes, sensitive data access, and large code changes; monitor or disable cron jobs. <br>
Risk: Team-channel updates may expose unreviewed or sensitive content. <br>
Mitigation: Review Discord or Slack outputs before relying on them and restrict channels to approved recipients. <br>
Risk: The installation flow asks users to clone a repository while server-resolved GitHub provenance is unavailable. <br>
Mitigation: Verify the source repository and release contents before cloning or installing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lean-zhouchao/agent-autonomy-kit-bak) <br>
- [Artifact README](artifact/README.md) <br>
- [Proactive Heartbeat template](artifact/templates/HEARTBEAT.md) <br>
- [Task Queue template](artifact/templates/QUEUE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-style configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no executable scripts or API calls are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

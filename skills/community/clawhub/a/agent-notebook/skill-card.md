## Description: <br>
Agent Notebook provides a file-based memory system with daily notes, durable MEMORY.md context, cron inbox processing, heartbeat checks, and nightly extraction for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marc69-69](https://clawhub.ai/user/marc69-69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give OpenClaw agents persistent workspace memory across sessions, including curated long-term notes, daily logs, and scheduled memory maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext memory files can retain sensitive operator, customer, or project information longer than intended. <br>
Mitigation: Use only in trusted workspaces, avoid secrets and regulated data, and review or prune retained memory regularly. <br>
Risk: Optional scheduled jobs can repeatedly read, rewrite, and prune memory files in the background. <br>
Mitigation: Inspect the exact cron or scheduled-task entries before enabling them, and only install recurring jobs when background processing is intended. <br>
Risk: The bundled heartbeat guidance may encourage broad monitoring such as email, calendar, social, or catch-all checks. <br>
Mitigation: Remove or narrow those monitoring routines unless the operator explicitly wants those integrations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/marc69-69/agent-notebook) <br>
- [Publisher Profile](https://clawhub.ai/user/marc69-69) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Installation Scripts](artifact/scripts/) <br>
- [Memory Templates](artifact/templates/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and PowerShell commands plus generated workspace memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local memory files and can configure recurring scheduled jobs when explicitly run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

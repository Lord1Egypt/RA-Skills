## Description: <br>
Prevent context overflow with automatic session truncation and memory preservation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifei68801](https://clawhub.ai/user/lifei68801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep local agent sessions within context limits, trim oversized JSONL history, and preserve selected conversation facts in memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite OpenClaw session history and persist facts derived from conversations. <br>
Mitigation: Review generated memory notes regularly and make backups before enabling scheduled truncation. <br>
Risk: AI-assisted fact identification may send session content to remote LLM services through the user's OpenClaw configuration. <br>
Mitigation: Keep AI-assisted identification disabled unless that data flow is acceptable. <br>
Risk: Unattended cron execution can repeatedly read and modify local session files. <br>
Mitigation: Test scripts manually, confirm the configured file scope, and review the cron schedule before enabling automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lifei68801/context-compression) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local session, memory, log, and configuration files under the user's OpenClaw workspace when its scripts are run.] <br>

## Skill Version(s): <br>
3.13.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

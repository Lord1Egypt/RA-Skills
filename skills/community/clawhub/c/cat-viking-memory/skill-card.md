## Description: <br>
Viking 记忆系统 helps OpenClaw agents save, retrieve, share, and tier long-term memories with optional Feishu autosave, vector search, and scheduled compression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyxlouspg](https://clawhub.ai/user/guyxlouspg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give OpenClaw agents persistent memory across sessions, including structured memory storage, search, shared workspaces, and optional Feishu conversation capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically retain private conversations in persistent memory. <br>
Mitigation: Enable autosave only for agents and sessions that intentionally need persistent memory, and avoid storing passwords, tokens, or other sensitive data. <br>
Risk: Shared workspaces can expose saved memories across multiple agents. <br>
Mitigation: Restrict the participating agent list and review the configured global workspace before deployment. <br>
Risk: Memory text may be sent to an embedding service. <br>
Mitigation: Point OLLAMA_HOST to a trusted local endpoint and verify that embedding traffic stays within the intended environment. <br>
Risk: Feishu autosave and scheduled cron jobs can capture or transform memory without a direct user action at that moment. <br>
Mitigation: Keep Feishu autosave and cron disabled unless required, then monitor them and keep backups of memory files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guyxlouspg/cat-viking-memory) <br>
- [Publisher profile](https://clawhub.ai/user/guyxlouspg) <br>
- [Detailed usage guide](references/README.md) <br>
- [Feishu integration guide](references/飞书集成说明.md) <br>
- [OpenViking](https://github.com/volcengine/OpenViking) <br>
- [viking-memory-system](https://github.com/TanDongTaotao/viking-memory-system.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown memory files, shell command output, and JSON or YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent local memory files, vector indexes, cron-triggered updates, and optional Feishu session captures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

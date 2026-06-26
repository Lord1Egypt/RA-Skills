## Description: <br>
Anima AIOS gives OpenClaw agents persistent memory management, cognitive profiling, daily quests, team leaderboards, and layered knowledge organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liruozhou](https://clawhub.ai/user/liruozhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent operators use Anima AIOS to add persistent local memory, cognitive growth tracking, knowledge organization, health checks, and optional team ranking to agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist and transform sensitive agent sessions, memory files, learning logs, message queues, and derived profiles. <br>
Mitigation: Use a private ANIMA_FACTS_BASE, review ~/.anima and the facts_base directory regularly, and delete stored data when it is no longer needed. <br>
Risk: External LLM endpoints may process sensitive memory content if configured. <br>
Mitigation: Inspect LLM base_url and api_key settings before use, and avoid remote LLM providers for sensitive data. <br>
Risk: Shared or multi-agent environments can expose other agents' profiles through team scanning or shared facts storage. <br>
Mitigation: Keep team_mode and ANIMA_TEAM_MODE disabled unless team ranking is intended, and isolate each agent's facts_base when privacy matters. <br>
Risk: Background monitoring and scheduled evolution can process local memory files after installation. <br>
Mitigation: Leave memory_watcher and auto_evolution disabled unless needed, and review any watchdog or cron setup before enabling it. <br>


## Reference(s): <br>
- [Anima AIOS ClawHub Page](https://clawhub.ai/liruozhou/anima-aios) <br>
- [Anima AIOS Homepage](https://github.com/anima-aios/anima) <br>
- [Security and Privacy Notes](artifact/SECURITY.md) <br>
- [Usage Guide](artifact/docs/USAGE.md) <br>
- [Examples](artifact/docs/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands, JSON configuration examples, and generated local data files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local facts, profiles, logs, rankings, and memory indices under the configured facts base.] <br>

## Skill Version(s): <br>
6.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Persistent session memory system that converts OpenClaw session transcripts into searchable Markdown, maintains a glossary index, and suggests memory-aware cron prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve useful OpenClaw session history across context compaction, build searchable memory indexes, and review cron jobs that may benefit from memory context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation history may be copied into durable searchable memory files, including private or sensitive data. <br>
Mitigation: Review retention scope before use, test on a narrow subset, add exclusions or redaction for secrets and private data, and inspect generated memory files before enabling cron. <br>
Risk: Hardcoded people, projects, and speaker labels may misclassify session content or expose personal context. <br>
Mitigation: Review and edit the hardcoded entities and speaker labels before running the scripts on real sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moltbotmolty-del/faya-session-memory) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, state JSON files, and human-readable command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates session transcript Markdown, a glossary Markdown index, converter state files, and a cron optimization report under OpenClaw memory paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

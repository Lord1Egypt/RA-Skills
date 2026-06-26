## Description: <br>
Chat Memory converts OpenClaw session transcripts into searchable Markdown memory, builds a structured glossary of people, projects, decisions, and timelines, and suggests memory-aware cron prompt updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve useful context from long-running OpenClaw work by converting session logs into workspace memory, indexing entities and decisions, and guiding cron jobs or subagents to search memory before work starts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted session memory can contain sensitive conversation details, secrets, regulated data, or private project context. <br>
Mitigation: Review generated memory files before broad use, avoid indexing sessions that contain sensitive data, and treat the workspace memory directory as sensitive. <br>
Risk: The glossary builder includes hardcoded people and project examples that may not match a user's workspace. <br>
Mitigation: Customize the known people, projects, and topic patterns before relying on glossary output for recall. <br>
Risk: Cron memory guidance can influence automated jobs with stale or irrelevant context. <br>
Mitigation: Keep cron automation visible and easy to disable, and review suggested prompt changes before applying them. <br>


## Reference(s): <br>
- [Chat Memory on ClawHub](https://clawhub.ai/moltbotmolty-del/chat-memory) <br>
- [AI Advantage](https://aiadvantage.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory/session Markdown files, a glossary index, state files, and a cron optimization report when its bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Drama Script guides an agent through a Chinese short-drama writing pipeline from initial concept to character profiles, story outline, episode outlines, and screenplay files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linhongbijkm-dot](https://clawhub.ai/user/linhongbijkm-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, writers, and production teams use this skill to plan, draft, revise, and resume Chinese short-drama projects with staged user review. The workflow creates workspace project files for concept planning, character profiles, story outlines, episode outlines, and screenplay drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates files in the active workspace. <br>
Mitigation: Run it in the intended OpenClaw workspace, review generated files at each staged approval point, and keep backups for important projects. <br>
Risk: Long projects may use subagents or a direct-output mode that can run into context limits. <br>
Mitigation: Use subagent mode when available for larger projects, and rely on the checkpoint resume workflow to continue from the first missing or incomplete stage. <br>
Risk: Deleting project material could remove useful drafts if confirmed accidentally. <br>
Mitigation: Follow the built-in confirmation flow; the artifact describes moving deleted projects or files to a trash location instead of irreversible deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linhongbijkm-dot/drama-script) <br>
- [Main workflow manual](SKILL.md) <br>
- [Project setup manual](references/master-setup.md) <br>
- [Common agent rules](references/common-agent-rules.md) <br>
- [Checkpoint resume guide](references/checkpoint-resume.md) <br>
- [Character profile agent manual](references/agents/agent-character-profile.md) <br>
- [Story bible agent manual](references/agents/agent-story-bible.md) <br>
- [Episode outline agent manual](references/agents/agent-episode-outline.md) <br>
- [Screenplay agent manual](references/agents/agent-screenplay.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown project files and conversational review prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates project folders and draft files in the active OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

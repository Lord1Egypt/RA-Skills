## Description: <br>
Orchestrates five Chinese-romance writing agents into a traceable, rollback-aware end-to-end creation workflow with quality gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dai-Chaoyu](https://clawhub.ai/user/Dai-Chaoyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers and content teams use this skill to generate Chinese romance manuscripts from user constraints by collecting hotspot signals, designing characters and plots, drafting manuscript text, and running gated QA with traceable artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow creates and updates multiple local files, including manuscript and context artifacts inside a timestamped project folder. <br>
Mitigation: Run it in a dedicated workspace and keep sensitive or unrelated files outside the generated project folder. <br>
Risk: The workflow may browse public novel-ranking sites and use basic shell utilities during execution. <br>
Mitigation: Review allowed network access and required binaries before running the skill. <br>
Risk: Generated logs and context snapshots can contain user prompts, story constraints, and intermediate creative decisions. <br>
Mitigation: Review generated logs and context files before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dai-Chaoyu/booksmith-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/Dai-Chaoyu) <br>
- [Zongheng ranking portal](https://www.zongheng.com/rank) <br>
- [JJWXC top-ten portal](https://www.jjwxc.net/topten.php) <br>
- [Fanqie ranking portal](https://fanqienovel.com/rank) <br>
- [Qidian ranking portal](https://www.qidian.com/rank) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON files with concise final status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a timestamped project folder and writes hotspot, character, plot, manuscript, quality report, log, and context artifacts under that project root.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

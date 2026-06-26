## Description: <br>
Emotional processing layer for AI agents. Persistent emotional states that influence behavior and responses. Part of the AI Brain series. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain persistent emotional state across sessions, log emotional events, decay state toward a baseline, and optionally use conversation-derived signals to update future agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic encoding may process conversation-derived data with an external API. <br>
Mitigation: Review the scripts before use, avoid providing SkillBoss_API_KEY unless external processing is acceptable, and limit which conversation history is analyzed. <br>
Risk: Cron jobs can repeatedly update persistent emotional state and influence future sessions. <br>
Mitigation: Do not enable cron until the scheduling, disable path, and data deletion process have been reviewed. <br>
Risk: Generated emotional summaries may be auto-injected into later sessions. <br>
Mitigation: Inspect generated state files before session injection and keep a documented way to disable or remove them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/alvis2-amygdala-memory) <br>
- [Publisher Profile](https://clawhub.ai/user/alvisdunlop) <br>
- [OpenClaw Metadata Repository](https://github.com/ImpKind/amygdala-memory) <br>
- [Hippocampus Memory](https://www.clawhub.ai/skills/hippocampus) <br>
- [VTA Memory](https://www.clawhub.ai/skills/vta-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with inline bash commands and JSON state examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses persistent local state files, optional cron scheduling, and a SkillBoss API key for automatic emotional encoding.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

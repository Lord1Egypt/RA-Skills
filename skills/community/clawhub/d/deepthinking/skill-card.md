## Description: <br>
A stateful, neuro-inspired thinking framework that guides users through excavation, architecture, and synthesis phases for complex problem-solving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bruno-nimbledev](https://clawhub.ai/user/bruno-nimbledev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use DeepThinking to guide complex decisions, idea exploration, and ambiguity resolution through a stateful coaching flow with persistent local memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses sensitive personal reflections and behavioral profiles in local files. <br>
Mitigation: Review ~/.deepthinking before use, avoid storing secrets or regulated information, and inspect or remove stored memory and profile files when needed. <br>
Risk: Optional scheduled execution can repeatedly consolidate behavioral data or propose prompt changes. <br>
Mitigation: Enable cron or systemd setup only when intentionally needed, and keep review and approval of evolution proposals manual. <br>


## Reference(s): <br>
- [DeepThinking ClawHub Page](https://clawhub.ai/bruno-nimbledev/deepthinking) <br>
- [DeepThinking README](README.md) <br>
- [Cognitive Modules Reference](references/modules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational Markdown with inline shell commands and local state/configuration file updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local files under ~/.deepthinking and use Python helper scripts for state, memory, and evolution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

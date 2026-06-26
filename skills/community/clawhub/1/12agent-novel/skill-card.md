## Description: <br>
中文长篇小说多智能体创作体系（12Agent）。适用于新建长篇小说项目、搭建世界观与大纲、逐章写作、自动推进与读者反馈等长流程创作任务；不适用于短篇、诗歌、散文、翻译或非小说写作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[228998098](https://clawhub.ai/user/228998098) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to create and continue Chinese long-form novel projects, including project initialization, worldbuilding, character design, outlining, chapter drafting, automatic progression, reader feedback, and rewrites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create and modify many project files during initialization, drafting, review, summaries, and feedback. <br>
Mitigation: Run it in the intended project workspace, review file changes before relying on them, and keep backups for important manuscripts. <br>
Risk: The workflow may read local model configuration and use background sub-agent workflows for manuscript content. <br>
Mitigation: Filter credentials before passing configuration into prompts, and avoid auto-advance or background workflows for sensitive manuscripts unless the configured model providers are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/228998098/12agent-novel) <br>
- [VERSION-2.8.0.md](VERSION-2.8.0.md) <br>
- [workflow-state-machine.md](references/workflow-state-machine.md) <br>
- [resume-protocol.md](references/resume-protocol.md) <br>
- [iron-rules.md](references/iron-rules.md) <br>
- [context-feeding-strategy.md](references/context-feeding-strategy.md) <br>
- [early-style-research-parallel.md](optimizations/early-style-research-parallel.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and project file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured novel-project artifacts and drafting/review guidance; sub-agent outputs are treated as candidates for coordinator review before files are updated.] <br>

## Skill Version(s): <br>
2.8.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

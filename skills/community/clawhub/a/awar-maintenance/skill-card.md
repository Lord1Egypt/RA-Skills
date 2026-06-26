## Description: <br>
机器人世界模型与动作模型（WAM）技术仓库维护Skill；支持搜集、分析、分类并生成图文并茂的AWAR仓库文档；包含科普介绍、深度技术分析、快速上手指南；当用户需要构建机器人AI领域技术仓库或研究VLA/RT-2/Dreamer等前沿工作时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessy-huang](https://clawhub.ai/user/jessy-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical writers use this skill to maintain AWAR-style robotics AI repositories focused on world models, action models, VLA systems, RT-2, Dreamer, and related work. It guides discovery, technical classification, deep analysis, and generation of Chinese-language documentation with quick-start guidance, architecture diagrams, benchmarks, and developer assessments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated quick-start guidance may include third-party repositories, package installs, checkpoint downloads, or real-robot demo steps. <br>
Mitigation: Review third-party sources and generated commands before execution, especially before downloading checkpoints or running real-robot workflows. <br>
Risk: The skill is designed to produce Chinese-language documentation by default. <br>
Mitigation: Tell the agent the preferred output language when a different documentation language is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jessy-huang/awar-maintenance) <br>
- [Getting started reference](references/getting_started.md) <br>
- [Awareness analysis framework](references/awareness_analysis_framework.md) <br>
- [Classification standard](references/classification_standard.md) <br>
- [Output template](references/output_template.md) <br>
- [Asset guide](assets/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown documentation with tables, diagrams, quick-start snippets, and structured technical analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primarily Chinese-language repository documentation for robotics world-model and action-model projects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

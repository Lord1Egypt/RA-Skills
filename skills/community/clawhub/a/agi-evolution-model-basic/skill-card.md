## Description: <br>
基于双环架构的AGI进化模型，通过意向性分析、人格层映射和元认知检测实现持续自我演进；当用户需要智能对话、人格定制或复杂问题求解时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiwifruit13](https://clawhub.ai/user/kiwifruit13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run an AI companion workflow that initializes a personality profile, responds to user questions, stores interaction memory, and applies metacognition, intent analysis, and personality mapping to guide future responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The calculator path can run arbitrary Python code. <br>
Mitigation: Use the skill only in an isolated workspace until the calculator eval path is removed or replaced with a safe arithmetic parser. <br>
Risk: The skill creates persistent local profile and conversation-memory files under ./agi_memory, including nicknames, customization answers, user queries, feedback, and derived behavioral data. <br>
Mitigation: Avoid sensitive conversations unless retention, access, and deletion controls are defined for the workspace. <br>
Risk: The security verdict is suspicious and calls for review before normal deployment. <br>
Mitigation: Review and scan the skill before deployment, with special attention to local file persistence and executable calculator behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kiwifruit13/agi-evolution-model-basic) <br>
- [Architecture](references/architecture.md) <br>
- [Capability Boundaries](references/capability_boundaries.md) <br>
- [Intentionality Architecture](references/intentionality_architecture.md) <br>
- [Metacognition Check Component](references/metacognition-check-component.md) <br>
- [Cognitive Insight V2 Implementation](references/cognitive-insight-v2-implementation.md) <br>
- [Personality Mapping](references/personality_mapping.md) <br>
- [Initialization Guide](references/init_dialogue_optimized_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and local JSON or Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local files under ./agi_memory for personality, interaction history, metacognition, advice, and feedback state.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

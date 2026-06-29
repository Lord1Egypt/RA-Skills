## Description: <br>
Cangjie Skill turns user-provided book text into reusable agent skill packs, learning notes, talking points, indexes, and trigger tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrybenedict0515](https://clawhub.ai/user/terrybenedict0515) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to convert a supplied book into structured, callable agent skills instead of a simple summary. It is intended for workflows where the user can provide the source text and review the generated skill pack before reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes book text supplied by the user, which may include private or copyrighted material. <br>
Mitigation: Confirm the text source and usage rights before running, and avoid supplying material the agent should not read or transform. <br>
Risk: The skill writes a multi-file derived skill package whose contents may be incomplete, misleading, or unsuitable for a target workflow without review. <br>
Mitigation: Review generated skills, learning notes, talking points, and test prompts before deployment or reuse. <br>
Risk: Incorrect output location or workflow choices could produce files in an unintended directory. <br>
Mitigation: Confirm the output directory, book metadata, and whether to use multiple sub-agents before execution. <br>


## Reference(s): <br>
- [Cangjie Skill on ClawHub](https://clawhub.ai/terrybenedict0515/cangjie-skill) <br>
- [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) <br>
- [darwin-skill](https://github.com/alchaincyf/darwin-skill) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code](https://code.claude.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Multi-file Markdown skill package with SKILL.md files, JSON test prompts, indexes, learning notes, and talking points] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided book text and human review of generated skills, notes, and tests before reuse.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

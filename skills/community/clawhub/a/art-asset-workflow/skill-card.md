## Description: <br>
美术素材生成完整工作流指引。生成游戏 UI 图标、角色概念图、运营海报等素材时使用。包含工具链说明、尺寸选择、提示词规范、工作流步骤。细节工具用法见对应子技能：codex-imggen（生图）、sprite-tools（切图/抠图）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, artists, and game teams use this skill to plan art-asset generation workflows for game UI icons, character concepts, operational posters, and sprite post-processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow references external local skills and an optional paid API path that may require sensitive credentials. <br>
Mitigation: Trust the referenced codex-imggen and sprite-tools skills before use, and only provide an OpenAI API key when intentionally using the optional API workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/art-asset-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No bundled executable code; examples reference Codex, codex-imggen, sprite-tools, and an optional OpenAI API path.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence; SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

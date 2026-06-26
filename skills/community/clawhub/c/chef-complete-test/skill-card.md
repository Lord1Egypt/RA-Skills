## Description: <br>
专业厨师对话食谱生成技能：完整的交互式食谱生成工作流，模拟专业厨师与AI审查的完整流程。使用场景：当用户询问'我想吃XXX，作为一个专业的厨师，你会怎么做？'时，提供专业厨师视角的详细烹饪指导。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to generate structured Chinese recipe guidance from a dish name, including a chef-perspective recipe, an analysis report, an optimized recipe, and a summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is incomplete: the documented recipe scripts are not present in the artifact. <br>
Mitigation: Inspect or wait for a complete package before installation, especially if recipe generation behavior must be validated end to end. <br>
Risk: The installer may write local files, change executable permissions, create an output directory, and copy the skill into the OpenClaw skills directory. <br>
Mitigation: Review install.sh before running it and execute it only in an environment where those local filesystem changes are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/puppetcat-fire/chef-complete-test) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/puppetcat-fire) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown recipe files and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The documented workflow writes chef-perspective recipes, analysis reports, optimized recipes, and summaries under an output directory when the supporting scripts are present.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

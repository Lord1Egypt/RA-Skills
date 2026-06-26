## Description: <br>
Helps an agent create, revise, evaluate, package, and optimize other agent skills, including scaffolding, validation, trigger-description optimization, evaluation loops, and delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dazhuangjammy](https://clawhub.ai/user/dazhuangjammy) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to turn workflows into maintainable skills, revise existing skills, validate behavior, optimize trigger descriptions, run evaluation loops, and package skill directories for release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled review server can terminate an unrelated local process bound to its target port. <br>
Mitigation: Use static report mode when possible, or choose and verify a known-free port before launching the review viewer. <br>
Risk: Evaluation and optimization workflows can call the Claude CLI and save prompts, skill content, transcripts, logs, or reports locally. <br>
Mitigation: Do not run these workflows on secrets or sensitive prompts unless that CLI session and local output storage are approved for the data. <br>
Risk: The skill can create and modify local files and run bundled Python scripts. <br>
Mitigation: Review the target paths and generated diffs before packaging or deploying the resulting skill. <br>


## Reference(s): <br>
- [Skill Architecture Guide](references/skill-architecture.md) <br>
- [Evaluation Loop](references/eval-loop.md) <br>
- [Description Optimization](references/description-optimization.md) <br>
- [Package and Present](references/package-and-present.md) <br>
- [Runtime: Claude.ai](references/runtime-claude-ai.md) <br>
- [Runtime: Cowork](references/runtime-cowork.md) <br>
- [JSON Schema Reference](references/schemas.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dazhuangjammy/dazhuangskill-creator) <br>
- [Publisher Profile](https://clawhub.ai/user/dazhuangjammy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON or YAML configuration, and generated or revised skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local skill directories, scripts, reports, benchmark artifacts, packaged archives, and review HTML depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

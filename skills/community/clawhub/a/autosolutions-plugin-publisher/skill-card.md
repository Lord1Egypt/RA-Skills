## Description: <br>
End-to-end plugin creation and publishing for Claude Code, Cowork, and OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and plugin maintainers use this skill to design, scaffold, package, publish, and update Claude-compatible marketplace plugins and OpenClaw deployment scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose repository changes, packaging steps, GitHub publishing actions, and generated installer scripts. <br>
Mitigation: Review the target repository, branch, visibility, generated files, installer contents, and packaging scope before running commands or publishing. <br>
Risk: Generated plugin files, memory, data folders, or installer scripts could accidentally include secrets or unwanted local content. <br>
Mitigation: Keep secrets out of generated plugin assets and review the files selected for packaging before creating or sharing a release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/autosolutionsai-didac/autosolutions-plugin-publisher) <br>
- [Anthropic Marketplace Structure reference](references/marketplace-structure.md) <br>
- [OpenClaw Deployment reference](references/openclaw-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, YAML, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate plugin files, marketplace manifests, OpenClaw installer scripts, packaging commands, and GitHub workflow guidance for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

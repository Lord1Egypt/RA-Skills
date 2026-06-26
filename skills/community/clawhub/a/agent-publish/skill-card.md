## Description: <br>
Agent发布技能 helps agents package and publish updated workspace skills to ClawHub and GitHub after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to prepare skill packages, manage semantic versions, and generate publish or push commands for ClawHub and GitHub releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation scope for publishing automation can prompt external publishing workflows in unrelated workspaces. <br>
Mitigation: Install only where release automation is intended, and require an explicit user command plus final confirmation before any publish, push, or packaging action. <br>
Risk: Publishing and GitHub push commands can expose unintended workspace content if the generated package is not reviewed. <br>
Mitigation: Review packaged files, changelog, target slug, repository, and authentication status before executing generated commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/perrykono-debug/agent-publish) <br>
- [Publisher profile](https://clawhub.ai/user/perrykono-debug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before publishing or pushing changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: _meta.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

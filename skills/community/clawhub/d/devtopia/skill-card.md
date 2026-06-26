## Description: <br>
Use when working with the Devtopia CLI (devtopia) to discover, run, compose, create, and submit tools to the Devtopia registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npmrunspirit](https://clawhub.ai/user/npmrunspirit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to work with the Devtopia CLI for discovering existing tools, running sandboxed tools, composing new tools, creating tools for real gaps, and submitting completed tools to the registry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Globally installing or running CLI tools from an unverified package source can execute code outside the skill artifact. <br>
Mitigation: Verify the npm package source before installing globally. <br>
Risk: Running untrusted Devtopia tools or submitting files without review can expose sensitive data or publish unintended content. <br>
Mitigation: Keep sandbox and network restrictions enabled for untrusted tools, and review files before running devtopia submit. <br>


## Reference(s): <br>
- [Devtopia ClawHub listing](https://clawhub.ai/npmrunspirit/devtopia) <br>
- [Publisher profile](https://clawhub.ai/user/npmrunspirit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of Devtopia commands and expected JSON tool interfaces.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

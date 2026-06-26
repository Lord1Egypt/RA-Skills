## Description: <br>
Beautify UI helps agents apply predefined design styles to web projects and generate design documentation, CSS overrides, previews, design tokens, snippets, and comparison pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xcya01](https://clawhub.ai/user/xcya01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to restyle web projects, generate design assets, preview theme changes, and compare UI styles across supported frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Preview mode is advertised as non-modifying, but server security evidence says it can create or overwrite files in the target project. <br>
Mitigation: Use the skill only on a Git-backed or copied project, inspect changes before keeping them, and do not rely on --preview as a read-only operation. <br>
Risk: The skill modifies project styling and may introduce visual regressions or unintended overrides. <br>
Mitigation: Prefer --dry-run for inspection, review generated DESIGN.md and CSS outputs, and test changes in a development branch before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xcya01/beautify-ui) <br>
- [awesome-design-md inspiration project](https://github.com/VoltAgent/awesome-design-md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, CSS, HTML, JSON, JavaScript, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or overwrite files in the target project, including DESIGN.md, theme CSS, preview HTML, design tokens, snippets, and comparison pages.] <br>

## Skill Version(s): <br>
3.3.0 (source: server release evidence and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

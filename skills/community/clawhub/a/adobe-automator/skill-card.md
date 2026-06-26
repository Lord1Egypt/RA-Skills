## Description: <br>
Automate Photoshop, Illustrator, InDesign, Premiere Pro, and After Effects using ExtendScript scripts executed through a cross-platform bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdul-karim-mia](https://clawhub.ai/user/abdul-karim-mia) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and automation-focused Adobe users use this skill to run trusted ExtendScript automation in supported Adobe desktop applications from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Caller-provided ExtendScript can access the host filesystem and perform destructive or sensitive actions. <br>
Mitigation: Run only reviewed scripts from trusted sources, use a low-privilege or dedicated account, and avoid sensitive folders when possible. <br>
Risk: Adobe automation may change creative project files or application state on the local machine. <br>
Mitigation: Test scripts on copies or isolated workspaces before using them on production assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abdul-karim-mia/adobe-automator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Markdown-formatted text status or error output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows or macOS with supported Adobe applications installed; executes caller-provided ExtendScript.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata, package.json, _meta.json, handler.js) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Generates Chrome extension starter projects with manifest, popup, background script, README, and related template files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use this skill to quickly scaffold Chrome extension projects for common extension patterns before adding application-specific logic and permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator writes files into the selected output directory based on user-provided names and paths. <br>
Mitigation: Run it from the intended workspace, choose an explicit output path, and review generated files before committing or publishing. <br>
Risk: Generated Chrome extension templates are starting points and may need permission, privacy, and store-listing review before release. <br>
Mitigation: Review manifest permissions, extension behavior, and generated README guidance before loading the extension into Chrome or submitting it to a store. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/chrome-extension-generator) <br>
- [Chrome Web Store Developer Console](https://chrome.google.com/webstore/devconsole) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, markdown, shell commands, guidance] <br>
**Output Format:** [Generated project files plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a Chrome extension directory containing manifest.json, HTML, JavaScript, README, and locale folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

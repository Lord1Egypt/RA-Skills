## Description: <br>
Search, install, and publish OpenClaw agent packages from the Clawstore registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saba-ch](https://clawhub.ai/user/saba-ch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover, inspect, install, update, package, validate, and publish OpenClaw agents through the Clawstore CLI and registry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing an agent package can upload secrets, private knowledge files, internal screenshots, or other sensitive material. <br>
Mitigation: Before publishing, run `clawstore validate` and `clawstore pack`, inspect what will be uploaded, and remove sensitive material. <br>
Risk: Publishing requires browser-based GitHub OAuth and trust in the Clawstore package and registry. <br>
Mitigation: Use `clawstore login` only when publishing and only after confirming the package and registry are trusted. <br>


## Reference(s): <br>
- [Clawstore skill listing](https://clawhub.ai/saba-ch/clawstore) <br>
- [Clawstore registry](https://useclawstore.com) <br>
- [Publisher profile](https://clawhub.ai/user/saba-ch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require the globally installed clawstore CLI; publishing requires browser-based GitHub OAuth.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Generates an ASCII tree or JSON representation of a directory structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to inspect, document, or debug project folder structures as readable tree output or structured JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill on sensitive directories can expose filenames and paths to the agent output or logs. <br>
Mitigation: Run it only on intended project folders, avoid home, root, secrets, and other sensitive directories, and use --depth for large projects. <br>


## Reference(s): <br>
- [Folder Tree Generator on ClawHub](https://clawhub.ai/wanng-ide/folder-tree-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [ASCII tree text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prints directory names and paths to standard output; recursion depth can be limited with --depth.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

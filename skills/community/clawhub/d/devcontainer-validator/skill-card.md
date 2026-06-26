## Description: <br>
Validates devcontainer.json files for VS Code Dev Containers, GitHub Codespaces, and DevPod. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to check devcontainer.json files for syntax, structure, feature references, ports, lifecycle scripts, VS Code customization, and security-oriented best-practice issues before local use or CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs bundled Python validator code against a local file path. <br>
Mitigation: Review the script before using it in sensitive repositories or CI, and run it only on intended devcontainer.json files. <br>
Risk: The --strict option treats warnings as failing results, which can block local or CI workflows. <br>
Mitigation: Enable --strict deliberately and choose the minimum severity and output format that match the workflow policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/devcontainer-validator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown/text guidance with command examples and optional JSON validator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text, json, and summary validator formats; exit codes distinguish pass, validation failure, and parse or file errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Donad Skill provides an OpenClaw skill-template utility for scaffold generation plus local shell commands for logging, searching, and exporting text entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onad1ocrypto](https://clawhub.ai/user/onad1ocrypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent authors use this skill to generate OpenClaw skill scaffolds, validate skill structure, and manage simple local text records through a Bash CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is listed as a skill-template generator, but the package also includes a persistent local logging tool. <br>
Mitigation: Review the installed commands before use and confirm that the logging behavior matches the intended workflow. <br>
Risk: User entries and command history are stored locally and can later be exported to stdout. <br>
Mitigation: Do not store secrets or sensitive notes unless local storage and export behavior are acceptable. <br>
Risk: The security verdict is suspicious due to metadata and default script behavior alignment concerns, although the evidence reports no malware or exfiltration. <br>
Mitigation: Review before installing, run in a controlled workspace, and set SKILL_TEMPLATE_DIR to an appropriate local path. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/onad1ocrypto/donad-skill) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with shell command snippets and generated Bash/Python code templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated content is written to stdout; local data commands may read and write files under SKILL_TEMPLATE_DIR or ~/.local/share/skill-template.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

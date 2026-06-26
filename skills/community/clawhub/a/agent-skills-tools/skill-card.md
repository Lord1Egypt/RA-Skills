## Description: <br>
Security audit and validation tools for the Agent Skills ecosystem that scan skill packages for common vulnerabilities before installation or release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rongself](https://clawhub.ai/user/rongself) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill maintainers use this skill to run local shell-based audits of Agent Skills packages for credential patterns, risky file access, network request patterns, permissions, and Git history signals before installation or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit findings are heuristic and may miss issues or report benign patterns. <br>
Mitigation: Review results manually and use the output as one input to a broader security review before installing or publishing a skill. <br>
Risk: The local audit output may display file paths or matching lines from scanned directories. <br>
Mitigation: Run it only on intended skill directories and avoid sharing raw output when scanned files may contain sensitive data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rongself/agent-skills-tools) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and terminal text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local heuristic audit output may include file paths and matching lines from scanned skill directories.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

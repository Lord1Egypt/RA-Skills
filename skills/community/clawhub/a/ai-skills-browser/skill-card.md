## Description: <br>
Skills Browser is a local HTML and Python tool for filtering skills and viewing skill details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quntion](https://clawhub.ai/user/quntion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to launch a local browser for scanning, filtering, and inspecting SKILL.md files in a neighboring skills directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local server can expose skill contents more broadly than intended. <br>
Mitigation: Use only in a trusted local environment, bind the server to 127.0.0.1, and remove wildcard CORS before broader use. <br>
Risk: The launcher can terminate an unrelated service using port 8765. <br>
Mitigation: Check the process on port 8765 before launch and replace forced termination with an explicit stop command. <br>
Risk: Skill detail requests use caller-provided skill IDs. <br>
Mitigation: Validate requested skill IDs before reading local skill files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/quntion/ai-skills-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and local URL guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Launches a local web interface on port 8765.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

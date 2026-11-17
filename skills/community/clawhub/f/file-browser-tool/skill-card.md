## Description: <br>
Read-only file browsing and reading in the SkillHub workspace for locating files, extracting text content, and returning structured results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to browse and read files in a SkillHub workspace, inspect text content, and receive JSON or Markdown-oriented results for downstream work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill is advertised as read-only but requests command execution, write access, API use, credentials, and network-related behavior. <br>
Mitigation: Review this carefully before installing. It may be intended as a file browsing helper, but the artifact asks for broader powers than that purpose needs. Only install it in an environment where shell execution, possible file writes, API credentials, and network/API handling are acceptable, or ask the publisher for a strictly read-only version with write and exec removed. <br>
Risk: File browsing and command execution can expose or modify sensitive workspace data if installed with broad permissions. <br>
Mitigation: Install only in a controlled workspace, restrict filesystem and shell permissions to the minimum needed, and prefer a strictly read-only variant when write and exec are not required. <br>
Risk: API key handling is mentioned by the artifact and could increase exposure if credentials are available in the agent environment. <br>
Mitigation: Avoid providing unnecessary credentials, scope any required keys narrowly, and review environment variables before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/file-browser-tool) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return file listings, file contents, execution logs, status fields, and error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

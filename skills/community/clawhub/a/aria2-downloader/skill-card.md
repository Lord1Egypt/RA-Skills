## Description: <br>
Remote control aria2 via JSON-RPC API. Add downloads (magnet/HTTP/FTP), check progress, pause/resume/remove tasks, batch download from text. NOT for local aria2c CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiastia](https://clawhub.ai/user/aiastia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to control a user-configured remote aria2 download service from an agent workflow. It supports adding magnet, HTTP, HTTPS, and FTP downloads, listing progress, pausing or resuming tasks, removing tasks, and batch-adding links from text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control downloads on a user-configured aria2 server through JSON-RPC. <br>
Mitigation: Install it only when agent access to that aria2 server is intended, and review requested add, pause, resume, and remove operations before execution. <br>
Risk: The aria2 RPC token is stored in a local configuration file. <br>
Mitigation: Keep .aria2-config.json out of version control, restrict filesystem access to it, prefer HTTPS for the JSON-RPC endpoint, and rotate the token if the file is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiastia/aria2-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and text status output from aria2 JSON-RPC operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided .aria2-config.json or ARIA2_CONFIG path containing the aria2 JSON-RPC URL and token.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

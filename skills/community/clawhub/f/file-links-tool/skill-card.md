## Description: <br>
Use this skill whenever an AI agent needs to share files, export results, upload outputs, or send data to its owner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrbeandev](https://clawhub.ai/user/mrbeandev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent owners use this skill when an agent needs to upload workspace files to a user-controlled bridge server and return preview or download links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files may be uploaded to an unintended server or made available through a temporary public tunnel. <br>
Mitigation: Require explicit user approval for each file and destination, prefer user-controlled hosting, and close tunnels after use. <br>
Risk: API keys or uploaded content may expose sensitive data if shared carelessly. <br>
Mitigation: Keep bridge keys out of URLs, avoid sensitive files unless necessary, and rotate or delete temporary keys after each session. <br>
Risk: Autonomous mode may run bridge server code that has not been reviewed in the current environment. <br>
Mitigation: Review the external server.py before autonomous mode and ask for user approval before starting a server or opening a tunnel. <br>


## Reference(s): <br>
- [API instructions](api_instructions.txt) <br>
- [ClawHub skill page](https://clawhub.ai/mrbeandev/file-links-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with API request examples and direct URL strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include direct download and browser preview URLs returned by the bridge server.] <br>

## Skill Version(s): <br>
3.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

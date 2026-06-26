## Description: <br>
browser-cli helps agents automate browser-use CLI workflows for navigation, interaction, screenshots, JavaScript execution, tab and cookie management, cloud browsers, Chrome profiles, and local tunnels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zdstudios](https://clawhub.ai/user/zdstudios) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to operate browser-use from the command line for web navigation, form filling, page inspection, screenshots, session handling, cloud browser access, and local app testing through tunnels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can access live browser sessions, cookies, and authenticated Chrome profiles. <br>
Mitigation: Use isolated test browser profiles and test accounts, avoid synced personal or privileged profiles, and close sessions when work is complete. <br>
Risk: Cookie export, cloud login, and cloud browser workflows can expose sensitive credentials or session material. <br>
Mitigation: Treat exported cookies and API keys as secrets, store them only where required, and remove cloud credentials when no longer needed. <br>
Risk: Local tunnel commands can expose development services to public HTTPS URLs. <br>
Mitigation: Do not tunnel admin, debug, or sensitive local services; stop tunnels promptly after testing. <br>
Risk: The one-line installer executes a remote shell script for browser-use. <br>
Mitigation: Install only when the browser-use installer and package source are trusted in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub release page for browser-cli](https://clawhub.ai/zdstudios/browser-cli) <br>
- [Publisher profile: zdstudios](https://clawhub.ai/user/zdstudios) <br>
- [browser-use CLI installer](https://browser-use.com/cli/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, code snippets, command recipes, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may involve live browser sessions, local files, cookies, Chrome profiles, API keys, cloud browser sessions, and public localhost tunnels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

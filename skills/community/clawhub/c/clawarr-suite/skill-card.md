## Description: <br>
ClawARR Suite helps agents operate self-hosted media automation stacks across Arr services, Plex, Tautulli, Overseerr, download clients, dashboards, cleanup tools, notifications, and media trackers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omiron33](https://clawhub.ai/user/omiron33) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage self-hosted media stacks, inspect library and download state, generate dashboards, synchronize tracker data, and run setup or troubleshooting workflows through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent administrative control over media services and related local-network tooling. <br>
Mitigation: Install and run it only on trusted machines and networks, and review commands that affect services before approving them. <br>
Risk: Setup and operation depend on powerful service credentials, tokens, and generated configuration data. <br>
Mitigation: Keep credentials in user-controlled environment or config files, redact logs and generated configs before sharing, and rotate keys if setup output or browser localStorage may have been exposed. <br>
Risk: Some workflows may involve Docker, SSH, pip installation, or destructive media-management actions. <br>
Mitigation: Prefer HTTPS or localhost where possible, and explicitly review pip install, Docker, SSH, delete, or remove commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omiron33/clawarr-suite) <br>
- [Setup guide](references/setup-guide.md) <br>
- [API endpoints reference](references/api-endpoints.md) <br>
- [Common issues](references/common-issues.md) <br>
- [Companion services](references/companion-services.md) <br>
- [Dashboard templates](references/dashboard-templates.md) <br>
- [Tracker APIs](references/tracker-apis.md) <br>
- [Traktarr and Retraktarr](references/traktarr-retraktarr.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text guidance with shell commands and generated files such as HTML dashboards or CSV/JSON exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, bc, and sed; operates against local-LAN and user-configured hosts using user-provided credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Syncs Docker Hub images to a CNB.tool registry via GitHub Actions so OpenClaw can pull images when direct Docker Hub access is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lufei4](https://clawhub.ai/user/lufei4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure a private GitHub Actions mirror that copies Docker Hub images into CNB.tool and then pulls them locally when direct Docker Hub access fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live GitHub and CNB credentials. <br>
Mitigation: Prefer provider-managed login flows such as gh auth login, avoid pasting tokens into chat, and use the narrowest possible GitHub and CNB tokens. <br>
Risk: The skill creates or modifies a GitHub repository and installs persistent GitHub Actions automation. <br>
Mitigation: Confirm the target repository and workflow contents before setup, and remove repository secrets or the workflow when the mirror is no longer needed. <br>
Risk: The skill stores configuration and secrets in a local OpenClaw environment file. <br>
Mitigation: Protect ~/.openclaw/.env with restrictive permissions and keep the file on trusted machines only. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lufei4/docker-image-sync) <br>
- [GitHub CLI](https://cli.github.com) <br>
- [Docker installation documentation](https://docs.docker.com/desktop/install/linux-install/) <br>
- [CNB](https://cnb.cool/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local GitHub CLI and Docker CLI setup, plus user-managed GitHub and CNB credentials.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

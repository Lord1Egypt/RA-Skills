## Description: <br>
Guides agents through cloning and synchronizing GitHub repositories with Git, including authentication choices, branch and submodule handling, shallow clones, updates, and common troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DuanC-Chao](https://clawhub.ai/user/DuanC-Chao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to choose safe, effective Git clone and sync commands for GitHub repositories. It helps with SSH or HTTPS authentication, branch selection, submodules, shallow clones, repository updates, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository URLs, destination paths, and recursive clone options can affect local files or pull unexpected content. <br>
Mitigation: Confirm the repository URL, branch, submodule behavior, and destination folder before running clone or sync commands. <br>
Risk: Authentication guidance may involve sensitive credentials such as SSH keys or personal access tokens. <br>
Mitigation: Do not paste private keys or tokens into chat, and prefer least-privileged personal access tokens when HTTPS authentication is required. <br>
Risk: Global Git proxy or SSL configuration changes can affect other repositories and tools. <br>
Mitigation: Avoid global proxy or SSL changes unless the user understands the impact and how to undo the settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DuanC-Chao/clone) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Git and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authentication, proxy, and Git configuration advice that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

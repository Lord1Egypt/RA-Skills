## Description: <br>
Agent Hush is a local privacy guardian for agent workspaces that checks outbound actions such as git pushes, skill publishing, file sharing, and syncs for sensitive data leaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elliotllliu](https://clawhub.ai/user/elliotllliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to have an agent scan local workspace files before outbound actions and block or report likely secrets, credentials, personal data, and infrastructure details before they are shared. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to automatically scan local workspace files before outbound actions, which can expose more local file contents to the agent workflow than the user intended. <br>
Mitigation: Ask the agent to announce scans and limit scans to the files or directories being pushed, published, shared, or synced. <br>
Risk: The skill includes optional commands that can change files, create sanitized copies, or update the .sanitize.json allowlist. <br>
Mitigation: Review diffs before applying fix commands, prefer dry-run behavior first, and inspect allowlist entries so future warnings are not suppressed too broadly. <br>


## Reference(s): <br>
- [Agent Hush ClawHub Page](https://clawhub.ai/elliotllliu/agent-hush) <br>
- [Agent Hush Repository](https://github.com/elliotllliu/agent-hush) <br>
- [Installation Guide](docs/install.md) <br>
- [Gitleaks](https://github.com/gitleaks/gitleaks) <br>
- [How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories](https://www.ndss-symposium.org/ndss-paper/how-bad-can-it-git-characterizing-secret-leakage-in-public-github-repositories/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text guidance with optional shell commands, JSON reports, and sanitized file outputs when commanded] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local scans, can manage a .sanitize.json allowlist, can create sanitized copies, and can modify files when the user chooses fix behavior.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Rétroaction et résolution des points bloquants pour l'automatisation Asana et Git dans KiloClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rez0](https://clawhub.ai/user/rez0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as a concise troubleshooting reference for Asana-to-KiloClaw automation and Git backup workflows, including token checks, state-file validation, gitignore hygiene, and cron scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill text includes commands that place live GitHub or Asana tokens in persistent local locations. <br>
Mitigation: Use Git credential helpers, SSH deploy keys, GitHub CLI authentication, or short-lived tokens, and retrieve Asana credentials just in time from a secret manager instead of writing plaintext token files. <br>
Risk: Following the token-storage examples as written may expose credentials through shell history, remote URLs, or local files. <br>
Mitigation: Review and adapt commands before execution, avoid embedding secrets in Git remote URLs, and rotate any token that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rez0/asana-git-retex) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

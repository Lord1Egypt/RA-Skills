## Description: <br>
Automatise la documentation des problèmes résolus et leur sauvegarde immédiate sur Git pour éviter les régressions lors de nouvelles installations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rez0](https://clawhub.ai/user/rez0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to document resolved issues, record root causes and fixes, and persist the resulting notes and workspace changes to Git after a repair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to automatically commit and push all workspace changes. <br>
Mitigation: Use it only in a dedicated repository where automatic commits and pushes are acceptable, and confirm the exact files, branch, and remote destination before allowing Git operations. <br>
Risk: The skill may attempt to recover GitHub credentials through 1Password if a push fails. <br>
Mitigation: Do not grant access to password managers or GitHub tokens unless the credential request, target repository, and destination branch are explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rez0/auto-retex-backup) <br>
- [Publisher profile](https://clawhub.ai/user/rez0) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces documentation updates, Git commit and push commands, and a user confirmation that includes the resulting commit hash.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

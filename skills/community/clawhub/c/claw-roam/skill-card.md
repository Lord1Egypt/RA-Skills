## Description: <br>
Sync OpenClaw workspace state between local and remote machines via Git for migration, backup, status checks, and full sync workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to synchronize OpenClaw memory, skills, context files, and device workflow state across machines through a Git remote. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git sync can upload private workspace memory, logs, skills, and context files to the configured remote. <br>
Mitigation: Use a private trusted repository, add .gitignore rules for secrets, tokens, databases, logs, and local-only files, and run git status before pushing. <br>
Risk: Automated push workflows can continuously upload workspace changes if enabled. <br>
Mitigation: Use auto-push only when continuous upload is deliberate and review the remote destination and synced file set before enabling it. <br>


## Reference(s): <br>
- [Claw Roam on ClawHub](https://clawhub.ai/reed1898/claw-roam) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

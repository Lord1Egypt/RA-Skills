## Description: <br>
AIDE file integrity monitoring reference. Database initialization, integrity checks, update workflow, aide.conf configuration, selection rules, report parsing, and production deployment with CIS benchmark compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and system administrators use this skill as AIDE reference material for file integrity monitoring, baseline database workflows, configuration rules, reporting, and production deployment planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes administrative deployment snippets for package installation, cron scheduling, file moves, permissions, immutable flags, and offsite copies. <br>
Mitigation: Review OS-specific paths, replace email and backup destinations, and run cron, chmod, chattr, mv, scp, or package-install commands only after administrator approval. <br>
Risk: AIDE baseline rotation can accept unauthorized changes if performed without reviewing integrity-check output. <br>
Mitigation: Review reported changes before rotating or replacing the baseline database, and investigate unexpected differences before accepting a new baseline. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/aide) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with command snippets and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference commands are emitted as guidance and should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

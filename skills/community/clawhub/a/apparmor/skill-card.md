## Description: <br>
Apparmor reference tool for working with apparmor in sysops contexts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and sysops practitioners use this skill to retrieve concise AppArmor reference guidance, checklists, troubleshooting steps, and command-oriented summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative security review flags the release as suspicious because an included review helper may run a nested reviewer with broad local access by default. <br>
Mitigation: Install only after publisher review, prefer no-yolo or equivalent restricted execution, and avoid workflows that require authenticated publishing unless the account and target are intentional. <br>
Risk: The skill provides generic sysops reference text, so guidance may be incomplete for a specific host, distribution, or AppArmor profile. <br>
Mitigation: Validate recommendations against the target environment's AppArmor documentation, profile state, and operational change controls before applying changes. <br>


## Reference(s): <br>
- [ClawHub Apparmor skill page](https://clawhub.ai/xueyetianya/apparmor) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown reference text selected by shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command-selected topics include intro, quickstart, patterns, debugging, performance, security, migration, and cheatsheet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

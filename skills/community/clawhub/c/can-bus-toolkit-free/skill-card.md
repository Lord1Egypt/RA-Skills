## Description: <br>
Can Bus Toolkit Free helps agents create local data provenance logs by recording a timestamp, content hash, and human-readable name for each data item. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to stamp local data flows with a WHEN, WHERE, and WHAT tuple, then verify content hashes and review append-only logs during audits or automated workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local provenance logs can expose sensitive labels or operational context if the WHAT field contains confidential data. <br>
Mitigation: Choose non-sensitive names, review the log location before use, and apply local file permissions appropriate for the data. <br>
Risk: The skill uses shell commands to calculate hashes and append or search local log files. <br>
Mitigation: Review generated commands and target paths before execution, especially when working in shared directories or automation. <br>
Risk: The artifact mentions callback_url and network troubleshooting even though server security guidance describes the skill as local-only. <br>
Mitigation: Treat the release as a local command-line logging aid unless a user explicitly authorizes network behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/can-bus-toolkit-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-style result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or inspect local append-only log files using standard shell utilities.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

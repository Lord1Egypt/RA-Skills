## Description: <br>
Builds persistent, evolving AI identity systems around stateless LLMs by using external memory files, behavioral rules, correction logs, and recurring evolution cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crowloki](https://clawhub.ai/user/crowloki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent builders use this skill to set up and maintain persistent identity, memory, correction, and evolution workflows for LLM-based agents. It is especially relevant when testing continuity across sessions or model swaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived memory, relationship profiles, and archived conversations can retain sensitive personal data. <br>
Mitigation: Keep memory in a dedicated folder, avoid raw conversation archives and relationship profiles by default, and define review, deletion, and redaction rules before use. <br>
Risk: Scheduled heartbeat or evolution cycles can create ongoing self-modification without enough operator control. <br>
Mitigation: Disable cron and heartbeat automation until explicitly configured, and review proposed changes before deployment. <br>
Risk: Identity and memory files could accidentally become a place to store secrets or sensitive operational data. <br>
Mitigation: Never store credentials or sensitive personal data in identity, memory, vault, or profile files. <br>


## Reference(s): <br>
- [Autopoietic Evolution Protocol](references/evolution-protocol.md) <br>
- [Ignition Guide](references/ignition-guide.md) <br>
- [Technical Foundations](references/technical-foundations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with file templates, directory layouts, protocol steps, and optional shell scheduling instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent memory files, identity documents, correction logs, cron-style schedules, and review procedures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

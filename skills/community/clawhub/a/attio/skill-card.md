## Description: <br>
Attio CRM integration for managing companies, people, deals, notes, tasks, and custom objects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capt-marbles](https://clawhub.ai/user/capt-marbles) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and sales operations teams use this skill to work with Attio CRM data, including searching contacts and companies, managing pipeline entries, creating notes, and creating or completing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Attio API key that could expose CRM data if mishandled. <br>
Mitigation: Use a least-privilege Attio token and avoid committing or sharing `~/.env`. <br>
Risk: Suggested commands can create or update records, pipeline entries, notes, or tasks. <br>
Mitigation: Require explicit approval before running CRM write actions. <br>
Risk: Running an unexpected `attio` CLI could send CRM data to the wrong tool or environment. <br>
Mitigation: Verify the `attio` CLI before executing commands. <br>


## Reference(s): <br>
- [Attio API Documentation](https://docs.attio.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/capt-marbles/attio) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CRM workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Attio CLI commands that read or write CRM records, notes, tasks, and pipeline entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

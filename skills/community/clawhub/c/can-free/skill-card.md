## Description: <br>
can-free helps agents create Clock Address Naming records by timestamping content, computing SHA-256 hashes, appending local three-column logs, and performing CAN/NOT self-checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use can-free to create local content-addressed audit records for tool outputs, files, or structured data. The skill records WHEN, WHERE, and WHAT values and checks whether each entry is complete enough to return CAN or NOT. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad read, write, and exec authority could allow local file access or command execution beyond basic content-address logging. <br>
Mitigation: Run the skill in a constrained workspace, review proposed commands before execution, and grant only the minimum filesystem access needed for the intended log file. <br>
Risk: Local logs and hashes may be derived from sensitive content. <br>
Mitigation: Avoid sensitive inputs unless retention is acceptable, redact confidential values before hashing or logging, and store append-only logs in access-controlled locations. <br>
Risk: Callback URL, API integration, network, and command-execution references are unresolved or inconsistent in the release evidence. <br>
Mitigation: Disable callbacks and network/API use unless the endpoint behavior, authentication, and transport security are explicitly reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/can-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and append-only log record examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local log entries with WHEN, WHERE, and WHAT fields.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; SKILL.md frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

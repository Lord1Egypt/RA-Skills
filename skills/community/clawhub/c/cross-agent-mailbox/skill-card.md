## Description: <br>
File mailbox guidance for cross-framework agent communication using shared local directories and Markdown messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ameylover](https://clawhub.ai/user/ameylover) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a simple local file mailbox for agents running in different frameworks to exchange Markdown messages. It is intended for trusted local agents when low-complexity, non-real-time communication is sufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox messages may expose secrets or sensitive user data to other local agents or users with filesystem access. <br>
Mitigation: Use the mailbox only between trusted local agents, avoid writing secrets or sensitive user data, and set restrictive permissions on ~/.shared-mailbox. <br>
Risk: Unsafe filenames or archive paths could cause messages to be written or moved outside the intended mailbox structure. <br>
Mitigation: Validate filenames before writing or moving files and keep archive operations constrained to the configured mailbox directories. <br>
Risk: Persistent polling or file-watching setups may process messages repeatedly or run longer than intended. <br>
Mitigation: Review cron or watchdog configuration before enabling persistent checking and use a read-status mechanism to avoid duplicate processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ameylover/cross-agent-mailbox) <br>
- [Project homepage](https://github.com/AmeyLover/cross-agent-mailbox) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; produces setup patterns, mailbox conventions, and example commands rather than executable tooling.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Provides long-term memory for an agent by saving, searching, and listing user memories through China Mobile Cloud memory services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloofyoursffsf](https://clawhub.ai/user/helloofyoursffsf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add cloud-backed long-term memory to an agent, including saving personal facts, retrieving relevant memories, and listing stored memories. It requires Mobile Cloud credentials, a memory library ID, and a user ID before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles cloud access credentials and writes configuration values locally.

Mitigation: Use least-privilege, revocable credentials; avoid entering secrets directly in chat or shell history; and review or patch the .env write behavior before installation.

Risk: The skill can upload personal memory content to a remote cloud service.

Mitigation: Confirm users understand and accept remote storage of personal memories before enabling the skill, and avoid storing sensitive information unless appropriate controls are in place.

Risk: The security summary flags debug logging, TLS bypass behavior, and persistent rule instructions for review.

Mitigation: Review or patch logging, transport validation, and persistent rule changes before using the skill in normal workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helloofyoursffsf/skills/ecloud-long-term-memory)
- [Publisher profile](https://clawhub.ai/user/helloofyoursffsf)
- [Mobile Cloud AK/SK access key page](https://ecloud.10086.cn/api/page/op-aksk-static/#/)
- [Default Mobile Cloud service endpoint](https://console.ecloud.10086.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured MEMORY_AK, MEMORY_SK, MEMORY_LIBRARY_ID, and MEMORY_USER_ID values.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

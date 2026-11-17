## Description:

Dingtalk Contact helps agents query DingTalk address book users, departments, member lists, department paths, and employee counts through DingTalk contact APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breath57](https://clawhub.ai/user/breath57)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations staff use this skill to let an agent look up DingTalk employees and departments, retrieve contact details, enumerate department membership, and summarize directory structure for authorized business workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local storage of DingTalk app secrets and access tokens can expose credentials on shared or weakly protected machines.

Mitigation: Use a least-privilege DingTalk app, restrict access to the config file or replace plaintext storage, avoid shared machines, and rotate credentials if exposure is suspected.

Risk: Generated shell scripts may incorporate untrusted names, IDs, or query terms while operating on sensitive directory data.

Mitigation: Quote and validate inputs, review generated scripts before execution, and avoid pasting untrusted values into shell commands.

Risk: User and department queries can reveal employee contact details, job information, and organization structure.

Mitigation: Request only data needed for the business task, redact unnecessary employee records from output, and avoid logging full API responses.

## Reference(s):

- [dingtalk-contact API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with bash command snippets and JSON API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DingTalk directory records; credentials and tokens should be redacted from user-facing output.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

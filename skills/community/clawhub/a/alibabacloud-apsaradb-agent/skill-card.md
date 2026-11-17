## Description:

Manage Alibaba Cloud databases with ApsaraDB Agent for product selection, inventory, diagnosis, provisioning plans, supported changes, maintenance, and backup or protection workflows under human approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud database administrators and developers use the skill to inspect Alibaba Cloud database resources, diagnose issues, and prepare supported operational changes. Writes require explicit human approval, while destructive requests are refused.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags risky installer and credential-handling guidance, possible behavior outside database management, and content that was only partially analyzed.

Mitigation: Review the scanner's credential-disclosure and out-of-scope reports before use, avoid unverified downloaded-installer instructions, and never place real secrets in command-line arguments.

## Reference(s):

- [API routes and confirmation contract](references/related-apis.md)
- [Supported commands and operation checks](references/related-commands.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [RAM policies](references/ram-policies.md)
- [Verification method](references/verification-method.md)
- [MySQL online DDL failure conditions](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-failure-conditions.html)
- [Redis maxmemory FAQ](https://redis.io/faq/doc/1jbxid5qq7/is-maxmemory-the-maximum-value-of-used-memory)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration instructions]

**Output Format:** [Markdown text with findings, checklists, and operational plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations and supported writes are bounded by available evidence, account permissions, and explicit human approval.]

## Skill Version(s):

0.2.5 (source: evidence.json release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

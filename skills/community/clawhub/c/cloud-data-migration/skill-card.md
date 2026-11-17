## Description:

Generates cloud data migration plans for databases, big data platforms, object storage, and data lakes, including product recommendations, migration strategies, tooling, assessment, POC guidance, risks, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangbingpeng](https://clawhub.ai/user/wangbingpeng)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud architects, developers, and engineers use this skill to design cross-cloud data migration plans, compare source and target cloud products, select migration tools, and prepare assessment, POC, implementation, validation, and rollback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated command examples may expose database passwords when credentials are pasted directly into command lines.

Mitigation: Use prompts, protected option files, or a secrets manager, and remove plaintext credentials from generated runbooks before execution.

Risk: Generated sync or repair steps, especially pt-table-sync with --execute, may modify production data.

Mitigation: Require backups, direction review, staging validation, and explicit approval before running any data-changing command.

Risk: Generated cloud storage destinations or IAM profiles may point to the wrong account, bucket, or scope.

Mitigation: Confirm all destination storage locations and IAM profiles are owned by the intended migration environment and scoped to least privilege.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangbingpeng/skills/cloud-data-migration)
- [Cloud Data Migration Examples](artifact/examples.md)
- [Cloud Vendor Product Mapping](artifact/product-mapping.md)
- [AWS Database Migration Service Documentation](https://docs.aws.amazon.com/dms/)
- [AWS Schema Conversion Tool Documentation](https://docs.aws.amazon.com/SchemaConversionTool/)
- [Percona Toolkit pt-table-checksum Documentation](https://docs.percona.com/percona-toolkit/pt-table-checksum.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, checklists, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning guidance and runbook-style content; review generated commands and migration steps before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

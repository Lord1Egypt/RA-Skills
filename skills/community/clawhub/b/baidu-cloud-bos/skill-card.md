## Description:

Baidu Cloud BOS helps agents manage Baidu Intelligent Cloud Object Storage buckets, including file upload, download, delete, copy, listing, signed URLs, image processing, recursive transfers, and sync workflows through Node.js SDK scripts or bcecmd.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangdong2398](https://clawhub.ai/user/yangdong2398)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Baidu Cloud BOS access and perform object storage operations from an agent workflow. It is suited for managing buckets, files, signed access links, image processing, and directory sync tasks where BOS credentials and storage scope have been reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BOS credentials can grant read, write, and delete access to storage data.

Mitigation: Use short-lived, bucket- and prefix-scoped STS credentials where possible, avoid placing real secrets directly in shell commands, and review the credential scope before use.

Risk: Recursive delete, bucket delete, and sync operations with delete flags can remove storage data.

Mitigation: Manually review destructive commands before execution, confirm target bucket and prefix, and prefer backups or non-destructive listing checks before running delete workflows.

## Reference(s):

- [Baidu Cloud BOS API Reference](references/api_reference.md)
- [Baidu Cloud BOS Node.js SDK Documentation](https://cloud.baidu.com/doc/BOS/s/Djwvyrhiw)
- [Baidu Cloud bcecmd Documentation](https://cloud.baidu.com/doc/BOS/s/kmcn3zrup)
- [ClawHub Skill Page](https://clawhub.ai/yangdong2398/skills/baidu-cloud-bos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local BOS credential configuration and may invoke Baidu Cloud storage APIs when credentials are provided.]

## Skill Version(s):

1.1.2 (source: package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

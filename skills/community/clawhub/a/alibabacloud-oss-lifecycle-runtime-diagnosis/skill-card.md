## Description:

Read-only OSS diagnosis for lifecycle runtime and archive restore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to diagnose Alibaba Cloud OSS lifecycle rules that are not taking effect, archive restore failures, and storage tiering tradeoffs from read-only control-plane evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can list bucket names across the configured account when no bucket name is provided.

Mitigation: Run it with an explicit bucket name, and remove or gate ListBuckets access when account inventory names are sensitive.

Risk: Cloud diagnostics can expose account metadata if run with broad or long-lived credentials.

Mitigation: Use a narrowly scoped temporary RAM credential limited to the read-only actions required by the skill.

Risk: The oss2 dependency is not pinned in the artifact.

Mitigation: Pin the oss2 dependency before production use and review dependency updates through the normal release process.

## Reference(s):

- [Lifecycle Playbook](artifact/references/lifecycle-playbook.md)
- [Restore Guide](artifact/references/restore-guide.md)
- [Minimal Read-Only RAM Policy](artifact/references/ram-policies.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with structured findings and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conclusions are grounded in script output from read-only OSS control-plane queries and official documentation verification when available.]

## Skill Version(s):

0.0.1 (source: artifact/references/manifest.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

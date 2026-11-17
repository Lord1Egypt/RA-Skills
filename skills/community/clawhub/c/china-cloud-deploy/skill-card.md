## Description:

Guides agents through deploying applications to Tencent Cloud, Alibaba Cloud, and Huawei Cloud using official CLIs, including serverless functions, object storage hosting, multi-cloud strategy, ICP filing considerations, and China-specific connectivity workarounds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and deployment-focused agents use this skill to plan and draft CLI-based deployment steps for applications targeting mainland China cloud platforms, including serverless APIs, static hosting, VPS or container choices, and ICP-related deployment constraints.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Default public endpoint and public bucket examples can expose cloud services or static assets.

Mitigation: Add authentication or gateway controls for APIs, use dedicated empty buckets for static assets, and confirm public access is intentional before deployment.

Risk: Example commands can deploy to live cloud accounts or persistently change local package registry settings.

Mitigation: Review and adapt commands before use, scope credentials to the intended project, and avoid persistent global registry changes unless they can be reversed.

Risk: Build output or configuration files may contain secrets that could be uploaded during deployment.

Mitigation: Scan build output and deployment packages for secrets before uploading them to cloud functions or object storage.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cloud CLI commands and deployment checklists; commands require review and adaptation before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

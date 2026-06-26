## Description: <br>
Use when managing Alibaba Cloud ApsaraVideo Live resources and workflows via OpenAPI/SDK, including live domain configuration, stream ingest and playback setup, recording/transcoding templates, monitoring queries, and live stream operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to plan, inspect, and manage Alibaba Cloud ApsaraVideo Live domains, stream workflows, templates, monitoring queries, and stream control operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real Alibaba Cloud ApsaraVideo Live service changes, including add, set, delete, forbid, and resume operations. <br>
Mitigation: Use temporary least-privilege RAM or STS credentials limited to the intended domains and operations, query current state before mutations, and confirm each change before execution. <br>
Risk: Saved operation evidence may contain stream names, domains, authentication settings, signed URLs, or other operational details. <br>
Mitigation: Review and redact output/aliyun-live-manage/ before sharing or publishing generated evidence. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/aliyun-live-manage) <br>
- [OpenAPI Product Page](https://api.aliyun.com/product/live) <br>
- [ApsaraVideo Live API Metadata](https://api.aliyun.com/meta/v1/products/live/versions/2016-11-01/api-docs.json) <br>
- [ApsaraVideo Live API Definition Template](https://api.aliyun.com/meta/v1/products/live/versions/2016-11-01/apis/{ApiName}/api.json) <br>
- [ApsaraVideo Live Documentation](https://www.alibabacloud.com/help/en/live) <br>
- [Source List](references/sources.md) <br>
- [Task Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown with inline shell commands, API names, parameter templates, and saved JSON or Markdown evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated execution evidence should be stored under output/aliyun-live-manage/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

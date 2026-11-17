## Description:

Use when managing Alibaba Cloud Performance Testing Service (PTS) via OpenAPI/SDK, including scene lifecycle operations, test start/stop control, report retrieval, and metadata-driven API discovery before production changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SREs use this skill to discover Alibaba Cloud PTS APIs, inspect test scenes, and start or stop bounded performance tests with saved evidence for verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba Cloud credentials are required for PTS operations.

Mitigation: Use least-privilege credentials scoped to the intended PTS resources and run the skill in a dedicated virtual environment.

Risk: Starting or stopping PTS scenes can affect production systems or active performance tests.

Mitigation: Confirm the region, scene ID, owner, change window, stop condition, and rollback path before running lifecycle commands.

Risk: Dependency installation may introduce unreviewed package changes.

Mitigation: Review and pin Alibaba Cloud SDK dependencies before installing them in managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/aliyun-pts-manage)
- [PTS Official Sources](references/sources.md)
- [PTS API Quick Map](references/api_quick_map.md)
- [PTS Operation Templates](references/templates.md)
- [Alibaba Cloud PTS API Explorer](https://api.aliyun.com/product/PTS)
- [Alibaba Cloud PTS OpenAPI Metadata](https://api.aliyun.com/meta/v1/products/PTS/versions/2020-10-20/api-docs.json)
- [Alibaba Cloud PTS Documentation](https://www.alibabacloud.com/help/en/pts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, JSON outputs, and saved evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated API metadata, scene listings, lifecycle results, and validation evidence under output/aliyun-pts-manage/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

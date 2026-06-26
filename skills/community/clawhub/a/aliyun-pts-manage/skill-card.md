## Description: <br>
Use when managing Alibaba Cloud Performance Testing Service (PTS) via OpenAPI/SDK, including scene lifecycle operations, test start/stop control, report retrieval, and metadata-driven API discovery before production changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud or observability engineers use this skill to inventory Alibaba Cloud PTS scenes, plan controlled test operations, start or stop scenes, retrieve reports, and validate API metadata before production changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Start and stop scripts perform real Alibaba Cloud PTS operations that can create load and cost. <br>
Mitigation: Use least-privilege RAM or temporary STS credentials, run read-only list and metadata checks first, and confirm the region, scene ID, change window, owner, and stop condition before execution. <br>
Risk: Generated output files may contain cloud resource details. <br>
Mitigation: Store files under the intended output directory, restrict access to generated evidence, and avoid sharing raw outputs unless they have been reviewed. <br>


## Reference(s): <br>
- [PTS Official Sources](references/sources.md) <br>
- [PTS API Quick Map](references/api_quick_map.md) <br>
- [PTS Operation Templates](references/templates.md) <br>
- [Alibaba Cloud PTS Documentation](https://www.alibabacloud.com/help/en/pts) <br>
- [Alibaba Cloud PTS API Explorer](https://api.aliyun.com/product/PTS) <br>
- [PTS OpenAPI Metadata](https://api.aliyun.com/meta/v1/products/PTS/versions/2020-10-20/api-docs.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with bash commands and JSON or text output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts save generated artifacts and execution evidence under output/aliyun-pts-manage/ when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

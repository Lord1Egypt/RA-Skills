## Description: <br>
Low-level Feishu document block operations via REST API for batch cell updates, precise positioned inserts, block tree traversal, table row and column manipulation, image replacement, and other direct block-level Feishu document controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deadblue22](https://clawhub.ai/user/deadblue22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill when Feishu document operations need direct block-level control beyond standard feishu_doc actions, including bulk table edits, positioned content insertion, block traversal, row or column changes, and in-place image replacement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local Feishu app credentials to obtain tenant access tokens. <br>
Mitigation: Use a least-privilege Feishu app and confirm the local configuration file containing the app ID and secret before execution. <br>
Risk: The skill includes block, row, and column deletion operations that can remove document or table content. <br>
Mitigation: Require explicit user confirmation and, where practical, a backup or recovery plan before deletion operations. <br>
Risk: The server security verdict is suspicious and recommends review before installation in important workspaces. <br>
Mitigation: Review the skill before installing it in Feishu workspaces that contain important or sensitive content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/deadblue22/feishu-block-ops) <br>
- [Publisher profile](https://clawhub.ai/user/deadblue22) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu document blocks API](https://open.feishu.cn/open-apis/docx/v1/documents) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API calls, Configuration] <br>
**Output Format:** [Markdown with inline Python and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Feishu REST endpoints, request shapes, rate limits, and operational patterns for document block changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

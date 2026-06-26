## Description: <br>
Helps agents handle Feishu/Lark API rate limits with smart intervals, batching guidance, and 429 retry behavior for batch operations, document writes, and bitable operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dingsunrise](https://clawhub.ai/user/Dingsunrise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan Feishu/Lark API calls that need throttling, retry handling after 429 responses, and batching for large document or bitable operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retries after write-heavy Feishu/Lark API calls can duplicate operations if the caller does not make the workflow idempotent. <br>
Mitigation: Confirm duplicate prevention or idempotency before relying on this skill for write-heavy workflows. <br>
Risk: Caching user, department, field, or document-structure metadata may conflict with an organization's data-handling rules. <br>
Mitigation: Keep any cached Feishu/Lark metadata within the organization's retention and access-control requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Dingsunrise/feishu-rate-limit) <br>
- [Feishu API Limits Documentation](https://open.feishu.cn/document/platform-notices/platform-updates-/custom-app-api-call-limit) <br>
- [OpenClaw Feishu Solution](https://xx0a.com/blog/openclaw-feishu) <br>
- [Feishu Developer Community](https://open.feishu.cn/community) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes recommended wait intervals, retry limits, batch sizing, and caching guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

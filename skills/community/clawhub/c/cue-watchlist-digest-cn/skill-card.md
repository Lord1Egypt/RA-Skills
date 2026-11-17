## Description:

为用户维护的自选清单生成逐日增量日报，覆盖回购、股权激励、两融标的与折算率、公告和监管措施，并为条目附上出处与时点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

适合逐日核对自选公司的公告与事件变化的用户，用于整理带有官方出处和时点的增量日报。日报不提供行情预测、风险评级或买卖建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional connection setup could expose an API key to an unapproved destination.

Mitigation: Use offline, user-supplied data until credential handling is fixed. Before using CUE_API_KEY, require HTTPS, approved-host checks, and redirect protection.

Risk: Cue queries reveal selected companies, and live services and separately installed skills were not evaluated.

Mitigation: Review and pin optional installations; use the offline, user-supplied-data path until any live services and separately installed skills have been reviewed.

## Reference(s):

- [Cue MCP setup](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader setup](https://cuecue.cn/hub/omni-reader)
- [Cue API key guidance](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, JSON, JSONL]

**Output Format:** [Markdown daily digest with JSON and JSONL watchlist, run-account, snapshot, and source-index files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each reported item includes a source and as-of time. Same-day reruns reuse the recorded increment; the skill does not schedule runs.]

## Skill Version(s):

0.2.25 (source: SKILL.md frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

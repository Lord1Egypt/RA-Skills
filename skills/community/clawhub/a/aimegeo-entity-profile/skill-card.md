## Description:

把用户提供或可核对的企业、品牌与产品资料整理成带来源和不确定性标记的实体数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

面向需要整理公司、品牌和产品资料的用户及其 Agent，将用户提供或实际读取的来源整理为保留出处、未知项和冲突项的实体档案。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A structurally valid profile may still contain inaccurate facts or incorrectly matched entities.

Mitigation: Check each fact against its cited source and retain unknown, conflicting, or unresolved identity states until verified.

Risk: Business information may be copied into the optional aimeGeo service.

Mitigation: Review the facts and destination before choosing to copy profile information into aimeGeo.

## Reference(s):

- [实体档案格式说明](references/profile-contract.md)
- [来源采集边界](references/source-boundaries.md)
- [aimeGeo 工作台文档](https://geo.aimmme.com/docs/geo-workbench/)
- [aimeGeo](https://geo.aimmme.com/)
- [aimeGeo GitHub](https://github.com/aiispower/aimegeo)
- [aimeGeo Gitee](https://gitee.com/xxjrq/aimegeo)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON entity profiles, validation results, summaries, or Schema.org drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profiles preserve source and uncertainty details; Schema.org drafts include only supported facts.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

根据主体与竞品清单生成结论先行的竞争分析简报，并为每条结论提供可追溯的证据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

面向产品、市场与策略团队，用于尽调背景、会前准备和策略讨论中的竞品比较。先建立逐条标注来源的证据表，再据此组织简报，并说明证据覆盖情况与未覆盖维度。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional connectivity helper may expose CUE_API_KEY to an unapproved destination; it contacts Cue by default unless given a local catalog file.

Mitigation: Follow the security guidance: run without credentials until shell destination checks and Python redirect handling are fixed.

Risk: Companion skills and confidential uploads may introduce unverified processing or retention.

Mitigation: Review companion skills before enabling them, and approve confidential uploads separately.

Risk: A validator PASS does not establish that cited claims are accurate.

Mitigation: Manually check cited evidence against the source material.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huhoo/skills/cue-competitive-brief)
- [Cue onboarding guide](references/cue-onboarding.md)
- [Evidence standards](references/evidence-standards.md)
- [Cue MCP configuration](https://cuecue.cn/hub/mcp)
- [Omni Reader configuration](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown evidence table and concise decision brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a conclusion-first brief, source-linked comparison cells, and an evidence coverage summary.]

## Skill Version(s):

0.3.34 (source: server-resolved release, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Creates a dated, six-section evidence brief on an A-share industry, with comparable-series anchors, representative companies, a policy timeline, and coverage gaps; it does not provide stock recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Research analysts and investment professionals use the skill to prepare dated industry briefs for sector scoping, meeting preparation, or due diligence. They provide an industry and time window; the report records its evidence and data gaps without recommending securities.

### Deployment Geography for Use:

Global (covers A-share industries in China)

## Known Risks and Mitigations:

Risk: The connectivity-check flow may expose CUE_API_KEY beyond the destinations its safeguards promise, including through redirect handling.

Mitigation: Until credential handling is corrected, use user-supplied materials without a Cue key. For an offline diagnostic, use --catalog-file without --post; require trusted HTTPS destinations and reject redirects or validate each hop before forwarding authentication.

Risk: Optional integrations, installer/source versions, and the external service were not tested for runtime behavior.

Mitigation: Review immutable installer and source versions and assess each optional integration separately before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huhoo/skills/cue-sector-overview)
- [Cue data connector setup](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader setup](https://cuecue.cn/hub/omni-reader)
- [Cue API key setup](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSONL]

**Output Format:** [A dated six-section Markdown industry report, a JSONL source index, and a run ledger]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to six pages; includes source anchors and coverage gaps; no stock recommendations.]

## Skill Version(s):

0.1.35 (source: server release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

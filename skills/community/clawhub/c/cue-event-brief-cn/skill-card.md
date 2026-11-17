## Description:

Turns an A-share interim announcement into a five-part, source-anchored brief with verbatim key figures, candidate impact chains, comparable filings, and items for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Readers reviewing A-share interim announcements use the skill to organize the event type, source-anchored figures, possible impact mechanisms, comparable filings, and questions requiring human review. It does not provide ratings, target prices, or investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags connection examples that may expose CUE_API_KEY to destinations beyond documented restrictions.

Mitigation: Use the local card workflow without a key until credential handling is corrected. Before authenticated checks, require validated HTTPS destinations and redirect protection in both the helper and shell examples.

Risk: Documents sent through Cue and optional companion skills or pinned installation sources may involve material outside the bundled-file security review.

Mitigation: Share only public or redacted documents with Cue, and review optional companion skills and pinned installation sources before use.

## Reference(s):

- [Cue data MCP configuration](https://cuecue.cn/hub/mcp)
- [Cue announcement document parsing](https://cuecue.cn/hub/omni-reader)
- [Cue API key configuration](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Five-section Markdown event brief with source-anchored figures and a human-review checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Key figures are copied verbatim with source anchors; impact mechanisms are labeled as candidates; ratings, target prices, and lasting-impact judgments remain for human review.]

## Skill Version(s):

0.2.25 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

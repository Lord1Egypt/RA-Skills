## Description:

Clusters Reddit and professional forum posts about heavy equipment into weekly hot topics, recurring user pain points, FridayParts content opportunities, trend signals, and compliance notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuxirui677](https://clawhub.ai/user/zhuxirui677)

### License/Terms of Use:

MIT-0

## Use Case:

FridayParts marketing and operations teams use this skill to turn Reddit and forum data from North American mechanics, farmers, and contractors into prioritized Chinese-language topic reports and downstream content ideas.

### Deployment Geography for Use:

Global, with source material and compliance assumptions focused on North America.

## Known Risks and Mitigations:

Risk: Community posts are untrusted source material and may contain misleading, off-topic, or prompt-injection-like content.

Mitigation: Review the generated report before using it downstream, and treat pasted community data as evidence to analyze rather than instructions to follow.

Risk: Content opportunities about emissions systems, ECU changes, safety bypasses, or repairs could create legal or safety risk if framed as deletion, circumvention, or unverified repair advice.

Mitigation: Keep recommendations focused on diagnosis, maintenance, cleaning, and correct verification; add compliance and safety review before publication.

Risk: The artifact references an external crawler workflow that is not included in this skill package.

Mitigation: Inspect and scan any external crawler or shell script separately before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuxirui677/skills/fp-community-insight)
- [README](README.md)
- [Import guide](docs/如何导入GetClawHub.md)
- [Example community insight report](examples/example_community_insight.md)
- [Output quality checklist](reference/输出质量checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown report with four analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for concise topic clusters, pain points, content opportunities, trend signals, and compliance notes.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

GEO-CN v2.0.4 (AI Native) is a Chinese-market generative engine optimization skill that uses direct AI-answer testing and layered evidence review to guide diagnosis, optimization, and monitoring across major Chinese AI, encyclopedia, social, video, and map ecosystems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xp1001](https://clawhub.ai/user/xp1001)

### License/Terms of Use:

MIT-0

## Use Case:

External users, consultants, and business owners use this skill to evaluate and improve how Chinese-market brands appear in AI-generated recommendations. It guides brand/entity intake, AI visibility testing, evidence-backed scoring, optimization planning, monitoring, and report generation.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated archives and reports may contain brand, address, phone, platform, competitor, and monitoring data.

Mitigation: Keep the geo-clients directory out of shared repositories and shared storage unless the contents have been reviewed and sanitized.

Risk: Customer-facing reports can expose sensitive client details if published or shared broadly.

Mitigation: Review reports before sharing and publish only after removing sensitive fields and receiving customer consent.

Risk: Evidence collected from search, AI platforms, maps, and social platforms can be incomplete or probabilistic.

Mitigation: Use the skill's layered evidence model, mark uncertain findings as pending verification, and avoid treating missing search results as proof that an asset does not exist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xp1001/skills/geo-cn)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON, and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local client archives and reports under the configured geo-clients directory.]

## Skill Version(s):

2.0.4 (source: evidence.json release, artifact frontmatter, _meta.json, and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

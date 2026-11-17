## Description:

Scores shortlisted creators on the typed STAR Suitability dimension and separately ranks campaign-specific commercial fit for influencer marketing decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and influencer-operations teams use this skill to evaluate a known shortlist of creators, produce evidence-backed Suitability item states, and keep campaign-specific commercial-fit rankings separate from the STAR Suitability read.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign context, creator metrics, local memory records, or YouTube measurements may include sensitive business or creator data.

Mitigation: Review approved data sources before use, provide only the campaign and creator evidence needed for scoring, and use YouTube API-based measurements only for approved shortlist vetting.

Risk: Incomplete or refused evidence can make a creator ranking appear more certain than the underlying data supports.

Mitigation: Require the typed STAR context fields, preserve Unknown states for missing evidence, and avoid definitive Suitability reads when applicable coverage is incomplete.

Risk: Persisted reports or promoted picks could expose draft evaluations or stale recommendations.

Mitigation: Save reports only after explicit authorization, request separate authorization before promotion, and include rerun conditions and evidence dates in recommendations.

## Reference(s):

- [Fit Scorer on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/fit-scorer)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Source homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Scoring templates](references/scoring-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown reports with typed Suitability item states, evidence notes, comparison tables, recommendations, and optional shell commands for measured YouTube inputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write reports only after explicit user authorization; may recommend separate promotion only after separate authorization.]

## Skill Version(s):

19.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

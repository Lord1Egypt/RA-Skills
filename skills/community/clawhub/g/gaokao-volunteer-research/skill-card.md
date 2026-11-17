## Description:

Helps agents create official-source Gaokao application research packages with data checks, candidate matrices, source trails, and family decision briefs without promising outcomes or submitting applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hacksing](https://clawhub.ai/user/hacksing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to structure Chinese Gaokao college application research, validate official source data, and produce reviewable family-facing research packages before human decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can fetch arbitrary URLs and persist downloaded content and metadata.

Mitigation: Use tightly scoped network and write permissions, run snapshots only for trusted official HTTPS sources, and store outputs in a dedicated research directory.

Risk: Gaokao guidance can mislead users if stale, unofficial, or mismatched province/year data is treated as conclusive.

Mitigation: Require current-year official sources, preserve source URLs and dates, and mark conflicts or missing data as requiring verification before decisions.

Risk: Generated research packages may contain raw downloaded material or sensitive family constraints.

Mitigation: Review generated files before sharing and avoid saving unnecessary personal details outside the dedicated package.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hacksing/skills/gaokao-volunteer-research)
- [Information Source Rules](references/source-policy.md)
- [Tooling Guide](references/tooling.md)
- [Test Scenarios](references/test-scenarios.md)
- [Official Source Index](data/official-source-index.json)
- [Ministry of Education 2026 Gaokao Topic](https://www.moe.gov.cn/jyb_xwfb/xw_zt/moe_357/2026/2026_zt08/)
- [Sunshine Gaokao Platform](https://gaokao.chsi.com.cn/)
- [Sunshine Volunteer Information Service](https://gaokao.chsi.com.cn/zyck/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown research packages, JSON helper output, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write sources.md, data-check.md, candidate-matrix.md, family-brief.md, risk-notes.md, and raw snapshots when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog show 0.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

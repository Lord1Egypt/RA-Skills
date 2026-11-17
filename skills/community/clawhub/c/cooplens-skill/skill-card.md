## Description:

Analyze Chinese-foreign cooperative undergraduate programs for parents, including official-source verification, admission rank estimation, public-discussion synthesis, CSCSE authentication analysis, overseas living-cost checks, parent-facing risk questions, Markdown reports, and mobile-first static HTML outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially families evaluating Chinese-foreign cooperative undergraduate programs, use this skill to compare programs, check current admissions status, estimate rank ranges, review certificate and CSCSE authentication paths, and identify questions that need official written confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The link-checking helper can open arbitrary URLs from a report using the user's network context.

Mitigation: Run URL and link validation only on trusted reports or inside a network-restricted sandbox, especially in environments with access to internal web services or cloud metadata endpoints.

Risk: Admissions conclusions and rank estimates may be incorrect if source pages are stale, unavailable, or mismatched by year, province, subject track, batch, program group, or project name.

Mitigation: Treat conclusions as prompts for manual official-source verification; require users to open linked sources and obtain written confirmation from schools or official admissions channels before decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/c-narcissus/skills/cooplens-skill)
- [Core Workflow](artifact/references/core_workflow.md)
- [Source Methods](artifact/references/source_methods.md)
- [Live Rank Estimation](artifact/references/live_rank_estimation.md)
- [Rank Estimation Workflow](artifact/references/rank_estimation_workflow.md)
- [Rank Statistical Estimation](artifact/references/rank_statistical_estimation.md)
- [CSCSE Authentication Analysis](artifact/references/cscse_authentication.md)
- [Overseas Living Cost](artifact/references/overseas_living_cost.md)
- [Parent Manual Distilled Lenses](artifact/references/parent_manual_distilled.md)
- [Recommendation Rubric](artifact/references/recommendation_rubric.md)
- [Public Discussion Synthesis](artifact/references/public_platform_discussion.md)
- [CoopLens Report Schema](artifact/references/schema.md)
- [Report Modules](artifact/prompts/report_modules.md)
- [Rankings Semantic Guide](artifact/data/rankings_semantic.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown reports and mobile-first static HTML, with source links, tables, checklists, and validation notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include a fixed disclaimer, runtime date, current-year admissions status gates, manually confirmable source links, and parent-facing verification questions.]

## Skill Version(s):

1.0.15 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

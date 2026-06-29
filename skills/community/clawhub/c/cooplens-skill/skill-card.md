## Description: <br>
Analyze Chinese-foreign cooperative undergraduate programs for parents. The skill verifies official sources in real time, estimates admission rank ranges including new/no-history projects, synthesizes anonymous public-discussion concerns without exposing platforms or identities, analyzes CSCSE / 教育部留学服务中心 authentication paths, searches overseas-city living costs when an abroad stage is possible, extracts parent-facing risk questions, produces Markdown with a table of contents, generates colorful mobile-first static HTML with native HTML and CSS, uses task-based artifact filenames, and separates 个性化推荐度评价（学生/家庭适配） from 项目综合实力推荐度评价（项目综合实力角度）. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-narcissus](https://clawhub.ai/user/c-narcissus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External parents, families, and education advisors use this skill to evaluate Chinese-foreign cooperative undergraduate programs, compare project fit, estimate rank ranges, and generate source-linked Markdown and mobile-first HTML reports for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Admissions facts, rank estimates, costs, and project status can be stale, incomplete, or misleading if sources are not manually checked. <br>
Mitigation: Manually open and verify official school, provincial admissions, regulator, ranking, and CSCSE sources before making education or financial decisions. <br>
Risk: The skill browses current education sources and creates local Markdown/HTML reports. <br>
Mitigation: Use it only when network access and local report-file creation are acceptable, and review generated files before sharing or relying on them. <br>
Risk: Public-discussion signals are non-official and may contain anecdotes or unverified concerns. <br>
Mitigation: Treat public discussion as a separate evidence layer and convert unresolved concerns into written questions for schools or admissions offices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/c-narcissus/skills/cooplens-skill) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Core workflow](artifact/references/core_workflow.md) <br>
- [Source methods](artifact/references/source_methods.md) <br>
- [Live rank estimation](artifact/references/live_rank_estimation.md) <br>
- [Rank estimation workflow](artifact/references/rank_estimation_workflow.md) <br>
- [CSCSE authentication](artifact/references/cscse_authentication.md) <br>
- [Overseas living cost](artifact/references/overseas_living_cost.md) <br>
- [Public platform discussion](artifact/references/public_platform_discussion.md) <br>
- [Recommendation rubric](artifact/references/recommendation_rubric.md) <br>
- [Report schema](artifact/references/schema.md) <br>
- [Report modules](artifact/prompts/report_modules.md) <br>
- [Ranking knowledge-base notes](artifact/data/rankings_semantic.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chat text, Markdown reports, standalone HTML files, and inline validation or helper commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown and static HTML report files; outputs depend on current source collection and manual verification of education facts.] <br>

## Skill Version(s): <br>
1.0.15 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

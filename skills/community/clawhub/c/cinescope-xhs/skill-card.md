## Description:

CineScope XHS generates evidence-labeled movie review reports using multi-source search, six-dimension analysis, and dynamic scoring weights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seeu1688](https://clawhub.ai/user/seeu1688)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer movie-rating, recommendation, and review-analysis requests. It collects movie review signals from professional, audience, and social sources, then produces a structured, spoiler-aware review with evidence levels, risk notes, and visual scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Movie titles and related query terms may be sent to external search providers such as Tavily and Bocha.

Mitigation: Use the skill only when that external search exposure is acceptable, and avoid entering sensitive or confidential query terms.

Risk: Generated HTML chart output can load Chart.js from a CDN.

Mitigation: Prefer Markdown or ASCII chart output in sensitive environments, and open generated HTML only in trusted rendering contexts.

Risk: Movie-review conclusions can be unstable for new, obscure, or socially volatile films.

Mitigation: Preserve the skill's evidence grading, sample-size warnings, cutoff date, and re-review guidance in generated reports.

## Reference(s):

- [CineScope XHS ClawHub page](https://clawhub.ai/seeu1688/skills/cinescope-xhs)
- [Publisher profile](https://clawhub.ai/user/seeu1688)
- [Tavily](https://tavily.com)
- [Bocha Open Platform](https://open.bochaai.com/)
- [Bocha Web Search API](https://api.bocha.cn/v1/web-search)
- [Chart.js CDN](https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, optional HTML/JavaScript chart code, ASCII chart alternatives, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include evidence grades, platform score normalization, dynamic six-dimension scoring, spoiler-aware analysis, and explicit limitations for sparse or volatile data.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact frontmatter, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

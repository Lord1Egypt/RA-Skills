## Description:

Builds high-signal AI intelligence briefs from fresh web sources, with separate daily and weekly formats for AI news, trend monitoring, market and technical updates, and actionable scouting reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yikailucas](https://clawhub.ai/user/yikailucas)

### License/Terms of Use:

MIT-0

## Use Case:

Business users, product leaders, analysts, and developers use this skill to receive concise Chinese-first daily or weekly AI intelligence briefs. It is intended for monitoring fresh AI news, technical movement, market signals, risks, opportunities, and near-term actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings rely on fresh public web sources, so results may include stale, duplicated, or uncertain claims.

Mitigation: Prefer official and primary sources, include source links and timestamps where available, flag uncertain claims as "待验证", and return a low-change-day summary when reliable updates are limited.

Risk: Business judgments and action recommendations could be mistaken for definitive market guidance.

Mitigation: Treat outputs as scouting briefs, verify important claims against cited sources, and review recommendations before operational decisions.

## Reference(s):

- [AI Intel Radar Sources](references/sources.md)
- [OpenAI News](https://openai.com/news)
- [Anthropic News](https://www.anthropic.com/news)
- [Google DeepMind Blog](https://deepmind.google/discover/blog/)
- [Meta AI Blog](https://ai.meta.com/blog/)
- [Microsoft AI Blog](https://blogs.microsoft.com/ai/)
- [arXiv Artificial Intelligence](https://arxiv.org/list/cs.AI/recent)
- [arXiv Computation and Language](https://arxiv.org/list/cs.CL/recent)
- [arXiv Machine Learning](https://arxiv.org/list/cs.LG/recent)
- [Papers with Code](https://paperswithcode.com/)
- [Hugging Face Blog](https://huggingface.co/blog)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown brief with cited source links and concise Chinese prose by default]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily mode produces fast news, technical depth, business judgment, and actions; weekly mode produces trends, opportunities, risks, and top actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

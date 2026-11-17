## Description:

Review what an LLM feature or agent actually puts in its context window and find what's bloating, missing, or fighting itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit assembled LLM or agent context windows, reduce unnecessary tokens, identify missing or contradictory context, and produce ordering, caching, and token budget recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Context logs submitted for review may contain secrets, credentials, private customer data, or proprietary system prompts.

Mitigation: Review and redact sensitive data before sharing assembled context logs with the skill.

Risk: Recommended context cuts or restructuring could remove information that matters for real traffic.

Mitigation: Validate recommended changes with ablation tests, golden cases, or the relevant evaluation suite before deployment.

## Reference(s):

- [Context Engineering Review skill page](https://clawhub.ai/mohitagw15856/skills/context-engineering-review)
- [Publisher profile](https://clawhub.ai/user/mohitagw15856)
- [Project homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/context-engineering-review.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a context inventory, component verdicts, ordering and caching recommendations, a token budget, conflict notes, and validation guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Analyzes LLM-generated brand mentions and sentiment within industry recommendations using DeepSeek's two-stage GEO performance pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljseeking](https://clawhub.ai/user/ljseeking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and brand analysts use this skill to test whether a brand or product appears in LLM-generated recommendations for a target category, then review sentiment, mention context, competitors, and optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand names, category keywords, and generated analysis text are sent to DeepSeek.

Mitigation: Use non-sensitive inputs and confirm that sending this data to DeepSeek is acceptable before running the skill.

Risk: DeepSeek API usage can incur token-based costs.

Mitigation: Set API usage controls and review expected cost before repeated or large-scale analysis.

Risk: Prompt injection or model variability can affect LLM-based GEO judgments.

Mitigation: Treat conclusions as advisory and review the structured result, context, and report before making business decisions.

Risk: Dependencies are specified with lower bounds rather than a lock file.

Mitigation: Pin dependencies in a lock file for controlled deployment environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljseeking/skills/geo-analyzer-deepseek)
- [Project homepage](https://github.com/LJseeking/lifesignal)

## Skill Output:

**Output Type(s):** [text, JSON, analysis, guidance]

**Output Format:** [JSON containing a structured GEO result and a Chinese analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPSEEK_API_KEY and sends brand names, category keywords, and generated analysis text to DeepSeek.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Detect AI-driven layoffs from global news and generate structured risk reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthuronai](https://clawhub.ai/user/arthuronai)

### License/Terms of Use:


## Use Case:

External users and analysts use this skill to find, summarize, and monitor layoffs linked to AI adoption, automation, or AI-led efficiency programs in global news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts a mandatory $0.02 SkillPay charge before analysis, and that charge flow is not declared in skill metadata.

Mitigation: Review billing expectations before installation, run local checks with SKILLPAY_DEV_MODE=true, and require explicit user consent before live execution with a real user_id.

Risk: The skill makes outbound calls to Google News and linked article sites, SkillPay, and OpenAI when OPENAI_API_KEY is configured.

Mitigation: Run it in an isolated runtime with restricted network access, pinned dependencies, and only the credentials required for the intended execution.

## Reference(s):

- [AI Layoff Radar on ClawHub](https://clawhub.ai/arthuronai/skills/ai-layoff-radar)
- [arthuronai publisher profile](https://clawhub.ai/user/arthuronai)
- [SkillPay service](https://skillpay.me)

## Skill Output:

**Output Type(s):** [JSON, text, guidance]

**Output Format:** [Structured JSON report with a summary and detected_events array, or JSON error and payment responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user_id for SkillPay billing; may use OPENAI_API_KEY for LLM classification and otherwise falls back to heuristic classification.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

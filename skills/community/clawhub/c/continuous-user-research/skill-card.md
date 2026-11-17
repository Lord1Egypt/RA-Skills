## Description:

Run longitudinal, in-context diary studies for product teams and convert weekly participant entries into concise user signals and experiment-ready recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicolas-m-design](https://clawhub.ai/user/nicolas-m-design)

### License/Terms of Use:


## Use Case:

Product teams, founders, and PMs use this skill to plan and run lightweight diary studies, collect consented participant entries across Slack, email, or Notion workflows, and synthesize weekly evidence-backed product signals with experiment-ready recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Participant identifiers or sensitive business data may be exposed through raw diary entries, screenshots, audio, Slack email lookup, or optional ticket creation.

Mitigation: Collect explicit consent, keep raw data in restricted storage, redact direct identifiers before synthesis, store attachment references rather than raw files in reports, and review tickets before publishing them to shared systems.

Risk: Broadly scoped integration credentials could grant more access than the study requires.

Mitigation: Enable only the integrations used by the current study, unset tokens for disabled integrations, and scope Slack, email, Notion, Linear, and GitHub tokens to the minimum required permissions.

Risk: Research outputs can overstate qualitative findings or turn ambiguous entries into misleading product recommendations.

Mitigation: Tie each signal to evidence, include confidence and confidence rationale, use low-confidence findings for risk-reduction experiments, and avoid high-risk regulated or sensitive studies without dedicated compliance design.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nicolas-m-design/skills/continuous-user-research)
- [Homepage](https://github.com/nicolas-m-design/user-research-bot)
- [Consent Message Template](artifact/prompts/consent_message.md)
- [Diary Entry Templates](artifact/prompts/entry_templates.md)
- [Follow-Up Rules](artifact/prompts/followup_rules.md)
- [Pre-Study Brief Template](artifact/prompts/pre_study_brief.md)
- [Post-Study Interview Guide](artifact/prompts/post_study_interview_guide.md)
- [Slack Recipe](artifact/recipes/slack_recipe.md)
- [Notion Recipe](artifact/recipes/notion_recipe.md)
- [Email Recipe](artifact/recipes/email_recipe.md)
- [Study Brief Schema](artifact/schemas/study_brief.schema.json)
- [Diary Entry Schema](artifact/schemas/diary_entry.schema.json)
- [Weekly User Signal Schema](artifact/schemas/signal.schema.json)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown templates and structured JSON objects for study briefs, diary entries, weekly signals, recommendations, and optional ticket handoff guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be privacy-redacted, evidence-linked, and limited to the top three weekly user signals with confidence and experiment plans.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

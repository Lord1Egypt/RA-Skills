## Description:

AI-driven health education skill that conversationally collects a user health profile and generates a simulated major-disease distance timeline with warning signals and mitigation actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbwin](https://clawhub.ai/user/wwbwin)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to explore a simulated major-disease risk timeline based on conversationally collected health, lifestyle, occupation, region, and family-history details. It is intended for health education and planning conversations, not medical diagnosis, treatment, or urgent care triage.

### Deployment Geography for Use:

Global, with data assumptions primarily focused on China where the referenced actuarial, life-table, and cancer statistics apply.

## Known Risks and Mitigations:

Risk: The skill collects sensitive health, lifestyle, location, occupation, and family-history details and may use them in online searches.

Mitigation: Require explicit consent before collecting or searching with health details, minimize query specificity, avoid sending detailed personal combinations to search providers, and keep profile data session-limited unless the user opts in.

Risk: The skill may present unvalidated disease-distance predictions as personalized medical urgency.

Mitigation: Frame results as general health education, include clear non-diagnostic language, avoid definitive prognosis claims, and direct users with symptoms or concerns to licensed medical professionals.

Risk: Medical and epidemiological search results can be stale, inconsistent, or mismatched to the user's context.

Mitigation: Prefer authoritative sources, state the data date and population assumptions, and lower confidence or avoid precise estimates when evidence is uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwbwin/skills/disease-distance-simulator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown health education report with a timeline visualization, risk tables, warning signals, and an action checklist.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should remain educational, cite relevant data assumptions where possible, and avoid presenting simulated disease distance as a diagnosis or prognosis.]

## Skill Version(s):

1.0.2 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

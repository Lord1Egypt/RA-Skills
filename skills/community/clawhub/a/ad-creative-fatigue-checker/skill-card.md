## Description:

Scores ad-level reach, frequency, click-through and spend data to rank the creatives that are wearing out, using the platform's own numbers. Use when the user asks for ad creative fatigue checker, ad frequency fatigue report, creative refresh scoring. For US performance media buyers and growth teams running Meta and Google display and video ads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

Help US performance media buyers and growth teams prioritize ad creatives for review by ranking user-provided Meta or Google display and video metrics; the workflow does not pause, edit, or publish ads.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The ranking report can overwrite an existing ranking.md file in the output folder.

Mitigation: Use a dedicated output folder.

Risk: Rankings may introduce incorrect or misleading guidance if treated as definitive.

Mitigation: Review the ranking and its underlying metrics before acting on it; keep platform metrics and time windows comparable, and set fatigue thresholds in advance.

Risk: The optional Windows toolkit is a separate unsigned download and is not required for this workflow.

Mitigation: The Python workflow does not need the app; if considering the separate download, assess trust independently and do not treat a matching hash as proof that the executable is safe.

## Reference(s):

- [Creative fatigue signals and review guidance](references/creative-fatigue-signals.md)
- [ClawHub skill release page](https://clawhub.ai/rapidworker1/skills/ad-creative-fatigue-checker)
- [Publisher homepage from release metadata](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Markdown ranking report (ranking.md)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks the supplied ad rows using frequency, click-through-rate change, cost-per-thousand change, and asset age; includes interpretation guardrails. Uses the provided export and does not modify advertising accounts.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

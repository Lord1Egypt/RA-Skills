## Description:

Chinese-language assistant for turning limited-time AI challenge or hackathon prompts into score-oriented deliverable packages, including topic analysis, execution workflows, runnable single-file HTML prototypes, UX reviews, simulated judge scorecards, roadshow scripts, prompts, code, configuration, and guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyxs028](https://clawhub.ai/user/dyxs028)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, hackathon teams, and business users use this skill to structure time-boxed AI competition work into concrete files for analysis, prototype building, UX review, scoring, and presentation. It is most relevant when the user provides a competition topic, screenshot, or limited-time AI delivery scenario.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated metrics, system names, and compliance references can be mistaken for validated facts.

Mitigation: Review generated business details against user-supplied source material before using them in submissions or presentations.

Risk: Generated HTML prototypes may load Tailwind from a CDN and should not receive sensitive or production data.

Mitigation: Use synthetic or approved demo data in prototypes, and review external dependency use before deployment.

Risk: The skill drives rapid file creation and prototype iteration, which can embed incorrect or misleading guidance if outputs are accepted without review.

Mitigation: Scan and review generated files, scorecards, prompts, and prototype behavior before sharing or deploying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dyxs028/skills/ai-challenge-topic-analysis-assistant)
- [Page challenge rules](artifact/references/page-challenge.md)
- [Pitfalls and implementation cautions](artifact/references/pitfalls.md)
- [Prompt templates](artifact/references/prompts.md)
- [Scenario guidance](artifact/references/scenarios.md)
- [Scoring rubric](artifact/references/scoring-rubric.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, single-file HTML, inline code blocks, and structured checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are file-oriented and may include generated business examples, demo data, HTML prototypes, UX findings, judge-style scoring, and presentation scripts.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

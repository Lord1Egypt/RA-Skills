## Description:

Generates a comprehensive brand voice and style guide with personality profiling, writing rules, platform adaptations, and on-brand example rewrites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitflopez](https://clawhub.ai/user/gitflopez)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, agencies, startups, solopreneurs, and e-commerce brands use this skill to create consistent brand voice documentation that can guide writers, contractors, and AI-assisted content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated brand rules may be inaccurate for a specific region, audience, or regulated industry.

Mitigation: Review the final guide against local language, audience expectations, and industry requirements before using it as a source of truth.

Risk: Users may paste confidential unreleased copy into the agent session for examples or rewrites.

Mitigation: Use sanitized samples or only provide confidential copy when the agent processing environment is approved for that material.

Risk: The guide may overfit to limited examples or admired brands and produce a voice that feels derivative.

Mitigation: Have a human reviewer adjust the generated style rules and example bank against actual brand strategy and customer feedback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gitflopez/skills/brand-voice-style-guide)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Prompt 1 - Brand Voice Discovery](artifact/prompts/01-voice-discovery.md)
- [Prompt 2 - Style Rules](artifact/prompts/02-style-rules.md)
- [Prompt 3 - Platform Adaptation](artifact/prompts/03-platform-adaptation.md)
- [Prompt 4 - Example Bank](artifact/prompts/04-example-bank.md)
- [Worked Example](artifact/examples/tilebound-full-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style brand voice guide sections, rules, platform notes, rewrites, examples, and onboarding quiz content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Four sequential prompts; later outputs depend on earlier brand voice and style-rule outputs plus optional user-provided copy samples.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

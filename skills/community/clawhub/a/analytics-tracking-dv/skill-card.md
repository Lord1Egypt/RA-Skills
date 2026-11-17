## Description:

Provides utilities for UTM link generation, conversion pixel snippets, attribution rules, and tracking-plan guidance for digital products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing engineers use this skill to create campaign URLs, prepare conversion pixel snippets, define attribution settings, and document product analytics instrumentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Segment examples in the skill definition include names, emails, user IDs, and traits without enough consent or data-processing context.

Mitigation: Do not send personal data through analytics calls unless lawful basis, consent, retention, and processing terms are documented.

Risk: Meta and Google tracking snippets can set cookies or collect identifiers when deployed.

Mitigation: Gate pixel deployment behind a consent banner and update the privacy policy before using the snippets.

Risk: The shipped files focus on UTM, pixel, and attribution setup, while the skill definition claims Segment tracking commands.

Mitigation: Review the release before installation and treat the Segment command examples as under-specified until implementation matches the documentation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/skills/analytics-tracking-dv)
- [Publisher Profile](https://clawhub.ai/user/clawdiri-ai)
- [README](artifact/README.md)
- [Tracking Plan](artifact/TRACKING-PLAN.md)
- [Pixel Configurations](artifact/pixel_configs.json)
- [Attribution Configuration](artifact/attribution_config.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and HTML or JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external Python dependencies; generated tracking snippets require platform IDs and consent-aware deployment.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

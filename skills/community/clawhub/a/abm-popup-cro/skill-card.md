## Description:

Helps agents create and optimize popups, modals, overlays, slide-ins, and banners for conversion while balancing timing, targeting, copy, accessibility, and user experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, ecommerce, SaaS, and content teams use this skill through an agent to design or improve conversion popups, banners, slide-ins, exit-intent offers, lead-capture modals, and related test plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use local product-marketing context files when present, which can expose confidential marketing context in generated recommendations.

Mitigation: Keep sensitive marketing material out of .agents/product-marketing-context.md and .claude/product-marketing-context.md unless it is intended for agent use.

Risk: Popup recommendations can affect privacy, accessibility, SEO, and user experience if implemented without review.

Mitigation: Review proposed consent language, dismiss behavior, keyboard and screen-reader support, mobile interstitial behavior, and frequency caps before deployment.

## Reference(s):

- [Popup Cro ClawHub Skill Page](https://clawhub.ai/mariokarras/skills/abm-popup-cro)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with popup strategy, copy recommendations, trigger rules, targeting notes, and test hypotheses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include implementation checklists for timing, frequency, mobile behavior, accessibility, privacy, analytics, and A/B testing.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Friction-reduction patterns for agents helping humans with disabilities. Voice-first workflows, smart home templates, efficiency automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctsolutionsdev](https://clawhub.ai/user/ctsolutionsdev)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to reduce accessibility friction for people with physical disabilities by designing voice-first workflows, smart-home templates, status updates, and recurring friction audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The smart-home examples include door-unlock automation and access-code handling that could create physical security exposure if copied directly.

Mitigation: Require explicit authorization, multiple trusted presence signals, time limits, notifications, and automatic relocking; never place real access codes in agent responses, prompts, or logs.

Risk: The conversation-history audit idea can expose sensitive health, schedule, and home details.

Mitigation: Keep audits opt-in and local where possible, minimize retained data, and redact sensitive details before analysis or sharing.

## Reference(s):

- [Apple Accessibility](https://www.apple.com/accessibility/)
- [Home Assistant Accessibility](https://www.home-assistant.io/docs/accessibility/)
- [Apple Human Interface Guidelines: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, code]

**Output Format:** [Markdown with text examples and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

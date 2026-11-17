## Description:

Friction-reduction patterns for agents helping humans with disabilities, including voice-first workflows, smart home templates, and efficiency automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgtreadw](https://clawhub.ai/user/cgtreadw)

### License/Terms of Use:

MIT

## Use Case:

Developers, caregivers, and agents supporting people with physical disabilities use this skill to design voice-first routines, smart-home templates, batch workflows, and weekly friction audits that reduce manual interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice and smart-home automations may unlock doors or change device state without enough user control.

Mitigation: Require explicit opt-in controls, strong presence verification, and confirmations for locks and other sensitive actions before deployment.

Risk: Automation examples can become unsafe defaults when copied directly into a live home environment.

Mitigation: Review and adapt each example for the user's devices, accessibility needs, emergency procedures, and rollback path before use.

Risk: Conversation-history analysis may expose sensitive personal, health, or household information.

Mitigation: Define clear privacy limits, minimize retained data, and obtain explicit consent before analyzing or storing conversation history.

## Reference(s):

- [Apple Accessibility](https://www.apple.com/accessibility/)
- [Home Assistant Accessibility](https://www.home-assistant.io/docs/accessibility/)
- [Apple Human Interface Guidelines: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Code]

**Output Format:** [Markdown with YAML configuration examples and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples should be reviewed and adapted before use with physical smart-home devices or private conversation data.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

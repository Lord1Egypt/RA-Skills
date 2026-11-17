## Description:

Friction-reduction patterns for agents helping humans with disabilities. Voice-first workflows, smart home templates, efficiency automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stavrostsamadias](https://clawhub.ai/user/stavrostsamadias)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to guide agents that support people with physical disabilities through voice-first workflows, friction audits, smart-home templates, batch operations, and clear status reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Smart-home examples include automatic door unlocking and access-code disclosure patterns.

Mitigation: Require explicit authenticated approval or multiple local presence signals for locks, avoid exposing access codes in chat or notifications, and review all lock automations before use.

Risk: Broad confirmation-free behavior can execute unintended actions when an agent has smart-home authority.

Mitigation: Limit confirmation-free execution to a clear allowlist of low-risk, reversible actions and require confirmation for security-sensitive or irreversible actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stavrostsamadias/skills/accessibility-toolkit-1-0-0)
- [Apple Accessibility](https://www.apple.com/accessibility/)
- [Home Assistant Accessibility](https://www.home-assistant.io/docs/accessibility/)
- [Apple Human Interface Guidelines: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with prose, checklists, voice-command examples, and Home Assistant YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

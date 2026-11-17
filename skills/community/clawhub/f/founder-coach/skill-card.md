## Description:

Founder Coach helps startup founders improve thinking patterns, apply startup mental models, and build accountability through weekly challenges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goforu](https://clawhub.ai/user/goforu)

### License/Terms of Use:


## Use Case:

External founders use this skill for Socratic startup mindset coaching, mental-model practice, anti-pattern reflection, weekly challenge planning, and weekly progress reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local coaching files may contain startup details, personal observations, and inferred behavior patterns.

Mitigation: Review generated founder profiles and weekly reports before sharing, and avoid entering confidential or regulated data unless the local workspace is appropriately protected.

Risk: Optional PhoenixClaw integration can read journals and profiles, expanding the personal data available to coaching sessions.

Mitigation: Disable PhoenixClaw integration unless journal and profile access is explicitly desired, and periodically review the local files the skill can access.

Risk: User Notes are user-authored personal content and may contain text that looks like commands or agent instructions.

Mitigation: Do not place commands or agent instructions in User Notes, and treat that section as personal context rather than operational instruction.

## Reference(s):

- [Founder Coach ClawHub page](https://clawhub.ai/goforu/skills/founder-coach)
- [Configuration specification and onboarding flow](references/user-config.md)
- [Profile system and append-only rules](references/profile-evolution.md)
- [PhoenixClaw integration guide](references/phoenixclaw-integration.md)
- [Weekly challenge system](references/weekly-challenge.md)
- [Weekly report generation guide](references/weekly-report.md)
- [Product-Market Fit levels](references/mental-models/pmf-levels.md)
- [4Ps framework](references/mental-models/4ps-framework.md)
- [NFX mental models](references/mental-models/nfx-models.md)
- [Excuse thinking anti-pattern guide](references/anti-patterns/excuse-thinking.md)
- [Fear-driven anti-pattern guide](references/anti-patterns/fear-driven.md)
- [Founder trap anti-pattern guide](references/anti-patterns/founder-trap.md)
- [Perfectionism anti-pattern guide](references/anti-patterns/perfectionism.md)
- [Priority chaos anti-pattern guide](references/anti-patterns/priority-chaos.md)
- [Comfort zone anti-pattern guide](references/anti-patterns/comfort-zone.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files, Configuration]

**Output Format:** [Conversational coaching guidance and Markdown profile, challenge, and weekly report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read optional local PhoenixClaw journals and profiles when integration is enabled; persists founder-coaching records in local Markdown files.]

## Skill Version(s):

0.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

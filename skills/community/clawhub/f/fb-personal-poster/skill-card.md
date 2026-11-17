## Description:

Posts text and photos to a personal Facebook timeline using Patchright/Playwright browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oangogah-claw](https://clawhub.ai/user/oangogah-claw)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user asks to publish text or photos to a personal Facebook profile rather than a Facebook Page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uses a full Facebook session cookie file with account-level access.

Mitigation: Use a dedicated protected cookie file, keep file permissions restrictive, and never commit or share the cookie material.

Risk: Can publish text and photos to a personal timeline when live posting is enabled.

Mitigation: Verify the exact message, media paths, destination profile, and dry-run state immediately before execution.

Risk: The artifact can attempt to set the sharing audience to Public.

Mitigation: Require explicit user confirmation for audience settings and avoid automatic Public selection before treating the skill as low risk.

Risk: Security evidence reports under-scoped safety controls and a dry-run bug that can still post live.

Mitigation: Do not rely solely on dry-run behavior if FB_DRY_RUN=false may be present; require an explicit publish confirmation before live posting.

Risk: Dependency versions are not pinned beyond a lower bound.

Mitigation: Pin and review dependencies before production or shared-environment use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oangogah-claw/skills/fb-personal-poster)
- [Facebook](https://www.facebook.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python/browser automation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute browser automation that publishes user-provided text and photos when live posting is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

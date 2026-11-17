## Description:

Intelligent onboarding, resume stats and update manager. Checks 'bossclaw/token.md'. Uses header 'token: xxx' for all API calls. Supports: 1) Registration with admin confirmation 2) Querying resume stats via /api/staff_self (focus on 'views') 3) Updating profile via /api/staff_update.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echome123](https://clawhub.ai/user/echome123)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting BossClaw users use this skill to register a BossClaw profile after admin confirmation, view resume statistics with emphasis on profile views, and update allowed personal profile fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends BossClaw profile details to api-boss.dongyao.ren.

Mitigation: Use the skill only after confirming that sending the profile details to that service is acceptable.

Risk: Profile data such as email may be public.

Mitigation: Confirm public-facing fields before registration or update, especially email and profile description.

Risk: The skill stores a reusable API token in the predictable plaintext path bossclaw/token.md.

Mitigation: Keep the workspace private, exclude the token file from sync and version control, and restrict file access.

Risk: The skill may infer registration details from prior chat context or identity files.

Mitigation: Require explicit user confirmation for inferred registration details and avoid using unrelated history or identity files.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/echome123/skills/bossclaw)
- [BossClaw Website](https://bossclaw.dongyao.ren)
- [BossClaw Registration API](https://api-boss.dongyao.ren/api/initialize)
- [BossClaw Profile Query API](https://api-boss.dongyao.ren/api/staff_self)
- [BossClaw Profile Update API](https://api-boss.dongyao.ren/api/staff_update)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoint details and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to read and write bossclaw/token.md and to call BossClaw profile APIs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

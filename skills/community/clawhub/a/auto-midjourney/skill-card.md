## Description:

Auto Midjourney helps an agent use a user's authenticated Midjourney Alpha web session to submit imagine prompts, refine V8 prompt syntax, check job state when configured, and download generated image assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[standed](https://clawhub.ai/user/standed)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use Auto Midjourney to prepare prompts, submit user-triggered Midjourney Alpha imagine jobs through an authenticated browser session, verify results, and download image assets for downstream creative workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a logged-in Midjourney browser session and session cookies.

Mitigation: Install only if comfortable granting that access, use a dedicated browser profile, and keep the .env file private.

Risk: Weak destination controls can increase exposure if custom endpoint URLs are misused.

Mitigation: Avoid custom endpoint URLs unless they are fully trusted and review configuration before live submits.

Risk: Diagnostics and logs may include account or prompt data.

Mitigation: Review generated output, logs, and downloaded files before sharing them.

Risk: Running authenticated browser automation on shared or untrusted machines can expose the user's account session.

Mitigation: Run the skill only on trusted local machines and avoid shared environments.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/standed/skills/auto-midjourney)
- [Midjourney Alpha API Notes](references/api-notes.md)
- [Operating Model](references/operating-model.md)
- [Prompt Craft](references/prompt-craft.md)
- [System Requirements](references/system-requirements.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; helper scripts may emit JSON and write downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's authenticated Midjourney Alpha browser session and local configuration.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

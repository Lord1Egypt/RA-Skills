## Description:

Save notes to Flomo via the Flomo inbox webhook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoluoboding](https://clawhub.ai/user/xiaoluoboding)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent save user-provided note text into a configured Flomo inbox. It is suited to quick note-capture requests in English or Chinese when the user has provided a Flomo webhook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Flomo inbox webhook can create notes for the account and should be treated as a secret.

Mitigation: Install only for users who accept that access, keep the webhook in restricted configuration, and avoid exposing it in logs or shared environments.

Risk: Debug mode can increase logging around the webhook request.

Mitigation: Leave FLOMO_DEBUG disabled for sensitive notes and restrict gateway or service logs when debugging is necessary.

Risk: Artifact documentation shows argument-based invocation, while the script reads note content from stdin.

Mitigation: Verify and standardize invocation before relying on the skill for sensitive or automated note capture.

## Reference(s):

- [Flomo](https://flomoapp.com/)
- [ClawHub skill page](https://clawhub.ai/xiaoluoboding/skills/flomo-notes)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text note content passed to a shell command, with a plain text success or error status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FLOMO_WEBHOOK_URL and curl; posts note content to the configured Flomo inbox webhook.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

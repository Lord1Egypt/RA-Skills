## Description:

Automated code review with LLM analysis, voice transcription, and Discord notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review pull-request diffs with LLM analysis, optionally include voice-note transcription, and send review status through Discord notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diffs, audio, and Discord notifications may leave the user's environment through LLM, Whisper, and webhook integrations.

Mitigation: Use the skill only with approved data, configured API keys, and notification channels that are permitted for the repository and organization.

Risk: Documented service restart and skill-publishing behavior can exceed ordinary code-review activity.

Mitigation: Allow service restart or publishing actions only in explicitly intended environments with manual operator control.

Risk: The artifact frontmatter version is 1.1.0 while server release metadata identifies this release as 1.1.1.

Mitigation: Treat 1.1.1 as the release version and reconcile artifact metadata before future publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/ai-code-review-svc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration names, and structured review result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe JSON-shaped review results with issue counts, suggestions, approval status, summaries, and optional transcription text.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

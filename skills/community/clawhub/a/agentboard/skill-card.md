## Description:

Agent Board helps agents build multi-panel storyboards by creating projects, uploading images and audio, adding annotations, exporting PDFs, and sharing public view URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xartex](https://clawhub.ai/user/0xartex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creative teams, and agents use this skill to turn ordered narrative sequences into storyboard projects with panels, uploaded assets, annotations, PDF exports, and shareable review links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Storyboard text, uploaded images, and audio are sent to AgentBoard's hosted service.

Mitigation: Upload only user-approved content and avoid sending sensitive assets unless the user has approved that hosted-service exposure.

Risk: Public share URLs may make storyboard projects viewable by anyone with the link.

Mitigation: Create or disclose share URLs only with user approval, and use scoped permissions or TTL values when appropriate.

Risk: Local file paths or remote URLs used for uploads could reference unintended content.

Mitigation: Confirm that each path or URL was provided or approved by the user before upload.

## Reference(s):

- [Agent Board ClawHub Skill Page](https://clawhub.ai/0xartex/skills/agentboard)
- [AgentBoard Hosted API](https://agentboard.fly.dev)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with REST endpoint references, JSON request examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project IDs, board UIDs, upload paths or URLs, and generated share or export links.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

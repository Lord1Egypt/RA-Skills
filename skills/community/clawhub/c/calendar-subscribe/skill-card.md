## Description:

Turn a school or work timetable in xlsx or csv format into a shareable HTTPS ICS subscription with split class sessions, one commute alarm per day, and a mobile-aware landing page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert school or work timetables into an HTTPS-hosted ICS subscription and landing page so classmates, family, or colleagues can subscribe once and receive updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ICS files and hosted landing pages can reveal schedule details to anyone with the public URL.

Mitigation: Use a dedicated output directory, review the generated calendar before publishing, and share the public URL only with intended subscribers.

Risk: Hosting examples can affect live infrastructure if applied to the wrong nginx site or path.

Mitigation: Apply the nginx configuration only on infrastructure the user controls and verify both the landing page and ICS content type before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eggyrooch-blip/skills/calendar-subscribe)
- [Landing page template](references/landing.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, generated ICS and HTML files, and hosting configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; xlsx input depends on openpyxl availability.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Daily looksmaxxing slang tip + Clavicular news. Extremely online Gen Z energy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jefftangx](https://clawhub.ai/user/jefftangx)

### License/Terms of Use:

MIT

## Use Case:

External users and community managers use this skill to generate a daily pair of posts: one looksmaxxing slang explanation and one Clavicular news or content update. The workflow is designed for OpenClaw invocation or scheduled posting, with source URLs included for news items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended scheduled posting can surface unsafe medical, self-harm-adjacent, hateful, or body-image-harmful looksmaxxing material without review.

Mitigation: Use review, filtering, and safety guidance before enabling cron announcements for public or group channels.

Risk: The skill performs live web lookups and maintains local state and source archives.

Mitigation: Install only when live lookup, persistent sent-term tracking, and source URL archiving are acceptable for the deployment context.

## Reference(s):

- [Clawvicular Skill Page](https://clawhub.ai/jefftangx/skills/clawvicular)
- [OpenClaw](https://github.com/openclaw)
- [Looksmaxxing Slang Dictionary](artifact/references/slang-dictionary.md)
- [Clavicular Lore](artifact/references/clavicular-lore.md)
- [Content Templates](artifact/references/content-templates.md)
- [Sources Index](artifact/references/sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown posts with source links and optional shell command snippets for scheduling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces two short posts, updates local sent-term state, and may append discovered URLs to the local sources index.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Supports spoiler-aware book discussions by tracking a reader’s edition and progress, grounding claims in available text, and avoiding unread material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[locoda](https://clawhub.ai/user/locoda)

### License/Terms of Use:

MIT

## Use Case:

External readers use this skill to discuss books they are reading or have finished, keep track of editions and progress, explore text-grounded interpretations, and reflect without unwanted spoilers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Markdown notes may retain a reader’s history, progress, and ebook paths.

Mitigation: Keep the reading-notes directory private and limit host filesystem access to the files needed for the discussion.

Risk: Direct ebook verification may be unavailable when compatible host tools are absent.

Mitigation: Provide selected excerpts for verification, and treat claims that cannot be checked from available text as unconfirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/locoda/skills/duizuo-reading-companion)
- [Spoiler and evidence guidance](artifact/references/spoiler-and-evidence.md)
- [Reading note storage guidance](artifact/references/storage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text and Markdown reading notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spoiler-aware; grounds claims in available text and confirms reading progress before discussing unread material.]

## Skill Version(s):

0.7.2 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

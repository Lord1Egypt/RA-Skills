## Description:

Public OpenClaw skill for generating reproducible PPTX decks from project notes, status bullets, and screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers, engineers, and project teams use this skill to turn curated notes, release summaries, audit outputs, and screenshot evidence into a stakeholder-ready, reproducible PPTX deck with a share-safe markdown summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads note and image paths supplied by the user.

Mitigation: Use only intended project-local inputs and avoid pointing the manifest at sensitive files that should not be included in a deck.

Risk: The skill writes or overwrites user-selected deck, JSON, and summary output paths.

Mitigation: Use a dedicated project or output folder and review output paths before running the build scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/skills/artifact-deck)
- [OpenClaw Homepage Metadata](https://github.com/zack-dev-cm/artifact-deck)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command templates and generated local PPTX, JSON, and summary files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9+ and python-pptx; reads user-selected notes and images and writes user-selected output paths.]

## Skill Version(s):

1.0.6 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

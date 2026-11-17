## Description:

Fetches AI-generated hourly cat images and helps agents send selected images with captions and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yazelin](https://clawhub.ai/user/yazelin)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve the latest, date-specific, numbered, or random AI-generated cat image and prepare it for delivery with a caption and metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and run an unpinned external Python package.

Mitigation: Install catime only in an isolated environment, pin a reviewed package version with hashes, and require explicit approval before installation.

Risk: The workflow expects outbound access to public GitHub-hosted image files.

Mitigation: Run it only where outbound GitHub access is allowed and avoid using it in environments that must remain offline.

Risk: Generated captions or stories may include Chinese text from the upstream image metadata.

Mitigation: Review or translate captions before sending them when the recipient expects another language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yazelin/skills/catime)
- [catime gallery](https://yazelin.github.io/catime/)
- [catime project link from artifact](https://github.com/yazelin/catime)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON/YAML message payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes image URLs, captions, and optional cat metadata when available.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Search and retrieve royalty-free media from Pexels (photos/videos), Pixabay (images/videos), Freesound (audio effects), and Jamendo (music/BGM).

This skill is ready for commercial/non-commercial use.

## Publisher:

[darknoah](https://clawhub.ai/user/darknoah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-producing agents use this skill to search provider media catalogs, inspect returned metadata, and download royalty-free photos, videos, sound effects, or music for projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Download commands can fetch arbitrary URLs or write to arbitrary local paths.

Mitigation: Only download URLs copied from trusted provider responses and choose output paths inside a dedicated media folder.

Risk: API credentials may be stored in a local config file.

Mitigation: Use environment variables for provider credentials when possible and avoid committing config files containing secrets.

Risk: The security verdict is suspicious due to under-scoped download behavior.

Mitigation: Review the skill before installing it in environments that process untrusted URLs or run inside sensitive networks.

## Reference(s):

- [Free Resource API Reference](references/api_reference.md)
- [Pexels API](https://www.pexels.com/api/)
- [Pixabay API](https://pixabay.com/api/)
- [Freesound API](https://freesound.org/apiv2/apply)
- [Jamendo Developer Portal](https://devportal.jamendo.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON API responses, and downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided API credentials for the selected media provider.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

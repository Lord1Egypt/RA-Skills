## Description:

Search Pinterest, inspect related pins and boards, preview images, and save images or MP4s accessible to the user's Ego Lite session; personal use only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Pinterest, inspect pins and boards, preview thumbnails, and save media available to the user's Ego Lite session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Importing a Chrome profile can expose unrelated browser data to the Ego profile.

Mitigation: Use a dedicated Ego profile and sign in to Pinterest manually. Skip Chrome import unless its scope is verified and accepted.

Risk: Downloaded private media and manifests may contain sensitive content, and requested previews are returned for the model to read.

Mitigation: Keep downloaded files and manifests private, and request previews only when needed.

## Reference(s):

- [Project homepage](https://github.com/terryso/ego-skills/tree/main/skills/pinterest-download)
- [ClawHub skill page](https://clawhub.ai/terryso/skills/ego-pinterest-download)

## Skill Output:

**Output Type(s):** [JSON, Image files, MP4 video files, Base64 image previews]

**Output Format:** [JSON results and manifest with saved media paths and optional base64 thumbnails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 100 pins per request; optional previews are limited to 8 thumbnails.]

## Skill Version(s):

0.5.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

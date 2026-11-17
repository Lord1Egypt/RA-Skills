## Description:

Publish a local video to YouTube Studio with Ego Lite via ego-browser, after checking login first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to upload a local video to their YouTube channel and receive its video URL or ID and processing status. The caller supplies the video and publishing details; visibility defaults to private.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overlapping uploads may mix files or settings, and the script may report private visibility without confirming it.

Mitigation: Avoid overlapping uploads. Verify the channel and actual visibility in YouTube Studio, and prefer a release that isolates each upload's configuration and confirms visibility before saving.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terryso/skills/ego-youtube-video)
- [Skill source page](https://github.com/terryso/ego-skills/tree/main/skills/youtube-video)
- [YouTube Studio](https://studio.youtube.com/)
- [Publishing inputs](references/inputs.md)
- [YouTube login guidance](references/login.md)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Text containing a YouTube video URL or ID and its processing status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports upload status; does not download or return the video file.]

## Skill Version(s):

0.1.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

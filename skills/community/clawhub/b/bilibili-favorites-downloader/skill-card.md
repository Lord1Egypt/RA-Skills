## Description:

Downloads or lists videos from a user's Bilibili favorites collection with pagination, size filtering, resume support, and yt-dlp-based highest-available-quality downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhjin](https://clawhub.ai/user/hhjin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to back up, list, or download videos from a Bilibili favorites collection for local offline access and organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Bilibili and invokes yt-dlp, which can consume network bandwidth and depend on remote service availability.

Mitigation: Run in list-only mode first and set a maximum download count before downloading a full favorites collection.

Risk: Downloaded videos can consume substantial local storage.

Mitigation: Choose an explicit output directory and set a size limit before running downloads.

Risk: The user may download content subject to Bilibili terms, access restrictions, or local legal requirements.

Mitigation: Use the skill only for content the user is allowed to access and download, and review Bilibili terms before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hhjin/skills/bilibili-favorites-downloader)
- [Bilibili Favorites URL Pattern](https://space.bilibili.com/{user_id}/favlist?fid={fav_id})
- [Bilibili Video URL Pattern](https://www.bilibili.com/video/{bvid})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script can print a video list, write MP4 files to a local output directory, and emit download status summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

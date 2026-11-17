## Description:

Downloads accessible Douyin videos or image galleries from share text, short links, or Douyin page URLs, saving videos as watermarked MP4 files and galleries as image folders with optional ZIP packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[railgun9983](https://clawhub.ai/user/railgun9983)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download individual Douyin videos or image galleries they are authorized to access, using a share phrase, short link, or full Douyin page URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader may require browser session cookies, and the security evidence flags guidance that places cookies directly in source code.

Mitigation: Keep credentials outside version control, use only short-lived cookies when unavoidable, remove them after use, and rotate or revoke them if exposed.

Risk: The skill makes Douyin and media-host network requests and writes downloaded media to the selected output path.

Mitigation: Run it only for content the user is authorized to access, choose an explicit output directory, and review downloaded files before reuse or sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/railgun9983/skills/douyin-downloader-pro)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown text with shell commands and local file paths; downloaded artifacts may be MP4 files, image folders, or ZIP archives.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes downloaded media to a user-selected output directory and emits progress logs with a [douyin] prefix.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

抖音无水印视频下载器，支持分享链接解析、批量下载和元数据保存。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chall2015](https://clawhub.ai/user/chall2015)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to parse Douyin video links, download public videos singly or in batches, and optionally save metadata alongside local media files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the browser is launched with browser isolation disabled.

Mitigation: Run the skill only in a constrained environment and enable the Chromium sandbox before routine use.

Risk: The security summary says the skill silently writes a debug screenshot.

Mitigation: Remove or gate debug screenshot capture and write only to an explicit, dedicated save directory.

Risk: The security summary says the skill downloads remote media without clear safety limits.

Mitigation: Add download size and time limits, keep concurrency bounded, and review downloaded files before reuse or redistribution.

Risk: The security guidance recommends pinning dependencies before trusting routine use.

Mitigation: Install from a lockfile or otherwise pin dependency versions for axios, cheerio, Playwright, and optional media tooling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chall2015/skills/douyin-downloader-latest)
- [Publisher profile](https://clawhub.ai/user/chall2015)

## Skill Output:

**Output Type(s):** [text, files, json metadata]

**Output Format:** [Status text with downloaded media files and optional JSON metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes video files and optional metadata to a configured save directory.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

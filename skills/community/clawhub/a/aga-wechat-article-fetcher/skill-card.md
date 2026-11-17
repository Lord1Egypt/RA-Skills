## Description:

Fetches WeChat public-account articles from mp.weixin.qq.com links, saves them as local HTML, and downloads article images and video cover images for offline viewing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aga-j](https://clawhub.ai/user/aga-j)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to archive WeChat public-account articles for local reading, including article text, images, and video cover images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The preview server may expose the OpenClaw workspace when run on shared or network-reachable machines.

Mitigation: Run it only on trusted local machines, bind the server to 127.0.0.1, and serve only a dedicated output directory before deployment.

Risk: Generated HTML may preserve active markup from remote WeChat articles.

Mitigation: Use only trusted WeChat article links and treat generated HTML as untrusted content before opening, sharing, or publishing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aga-j/skills/aga-wechat-article-fetcher)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Plain text or Markdown status plus local HTML and media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a dated HTML file, downloads images and video cover images, and may start a local HTTP server for preview.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

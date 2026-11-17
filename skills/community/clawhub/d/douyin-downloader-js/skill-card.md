## Description:

Uses Node.js to parse Douyin web pages for video or image-post metadata and download the associated media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbos1314](https://clawhub.ai/user/xbos1314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to parse Douyin links, inspect content metadata, and download video or image-post media into a local output directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network fetching is broadly scoped and could be abused to reach internal URLs or consume excessive memory or disk.

Mitigation: Install only when comfortable running a downloader that fetches remote content and writes files locally; use a dedicated output directory, avoid untrusted links, and prefer a version that restricts hosts, limits redirects and file sizes, streams downloads safely, and validates response types.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xbos1314/skills/douyin-downloader-js)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with shell commands and JSON output examples; the bundled script emits JSON text and local media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script may write downloaded video or image files to a local output directory; image posts are limited to the first three images.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

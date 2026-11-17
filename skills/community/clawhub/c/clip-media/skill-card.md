## Description:

Extract media such as videos, photos, GIFs, and audio from social media URLs using yt-dlp, returning local files, metadata, or an explicitly confirmed public upload link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Clip Media to inspect or retrieve media from supported URLs and return metadata, local file paths, or temporary public links after explicit upload consent. It is intended for non-sensitive media where downloading and any external transmission are permitted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public upload paths can expose media through third-party temporary hosts and may not use the upload host the user selected.

Mitigation: Use --no-upload for sensitive files, require --confirm-upload for any public upload, and verify the actual returned host before sharing the link.

Risk: Browser-wide cookie access can expose active authenticated sessions.

Mitigation: Avoid --cookies-from-browser unless the user explicitly accepts the risk; prefer non-sensitive public URLs or narrowly scoped manual credentials.

Risk: Private, paid, copyrighted, regulated, or confidential media can create legal, privacy, or policy exposure if downloaded or transmitted.

Mitigation: Confirm the content is permitted for download and sharing before extraction, and keep regulated or confidential content local.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jlacroix82/skills/clip-media)
- [Publisher Profile](https://clawhub.ai/user/jlacroix82)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, guidance]

**Output Format:** [Plain text, JSON metadata, local file paths, and temporary public URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads are saved locally by default; public uploads require explicit confirmation and may use third-party temporary hosts.]

## Skill Version(s):

0.3.5 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

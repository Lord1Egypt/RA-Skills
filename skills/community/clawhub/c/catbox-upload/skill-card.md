## Description:

Uploads files to catbox.moe for permanent hosting or litterbox.catbox.moe for temporary hosting and returns the resulting file URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[microck](https://clawhub.ai/user/microck)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to upload local files to Catbox or Litterbox and retrieve a shareable URL, choosing temporary hosting when permanence is not required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files uploaded through this skill are sent to third-party hosting services and returned URLs should be treated as shareable links.

Mitigation: Only upload files suitable for Catbox or Litterbox, avoid secrets and private data, and prefer temporary Litterbox uploads when permanence is not needed.

Risk: Permanent Catbox uploads may persist beyond the user's intended sharing window.

Mitigation: Use Litterbox with an explicit expiration time for short-lived sharing, or confirm permanence before selecting Catbox.

Risk: Operational use depends on the requests package and outbound HTTP calls to Catbox or Litterbox.

Mitigation: Pin dependencies and add request timeouts before relying on the uploader in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/microck/skills/catbox-upload)
- [Catbox upload API endpoint](https://catbox.moe/user/api.php)
- [Litterbox upload API endpoint](https://litterbox.catbox.moe/resources/internals/api.php)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text URL output with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the direct uploaded-file URL on success; supports temporary Litterbox expirations of 1h, 12h, 24h, or 72h.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

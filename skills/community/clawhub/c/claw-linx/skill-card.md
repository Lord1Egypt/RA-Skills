## Description:

Upload local files to a configured self-hosted Linx instance and return shareable links, using linx-client when available or curl otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanjelin](https://clawhub.ai/user/lanjelin)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to share authorized local files through their configured self-hosted Linx instance and receive links to the uploads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploading private or unintended local files exposes them through shareable links.

Mitigation: Upload only files the user explicitly authorizes; avoid credentials and sensitive files unless sharing them is intentional.

Risk: Insecure transport or disclosure of upload credentials and deletion keys can compromise shared files.

Mitigation: Use HTTPS for non-local instances and keep the API key and deletion-key logfile private.

Risk: An upload may persist after a failed response, and earlier files in a batch may already be shared.

Mitigation: Check existing links and the private logfile or server before retrying; do not automatically repeat the batch.

## Reference(s):

- [ClawHub Linx release](https://clawhub.ai/lanjelin/skills/claw-linx)
- [Linx skill source (server-resolved GitHub import)](https://github.com/Lanjelin/openclaw-linx)
- [Linx server](https://github.com/gabe565/linx-server)
- [Optional linx-client](https://github.com/Lanjelin/linx-client)

## Skill Output:

**Output Type(s):** [Text, Shareable URLs]

**Output Format:** [Plain text links, one per successful upload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional expiry, remote filename, randomized filename, and direct-link selection.]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

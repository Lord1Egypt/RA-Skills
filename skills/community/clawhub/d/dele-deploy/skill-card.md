## Description:

Deploy local HTML/frontend files to Dele (dele.fun) and get a live URL. Files must go through presign and direct storage PUT, never as one multipart POST to /api/upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[del-zhenwu](https://clawhub.ai/user/del-zhenwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to publish a local HTML file or frontend project folder to Dele and receive a live URL to share.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File links in the selected folder may expose private files outside that folder during publication.

Mitigation: Deploy a clean build folder containing only intended assets, with no file symlinks or private files; choose visibility explicitly because deployments default to public, and ensure declared tool permissions match deployment requirements.

## Reference(s):

- [Dele Deploy Skill Instructions](https://www.dele.fun/skill.md)
- [ClawHub Release Page](https://clawhub.ai/del-zhenwu/skills/dele-deploy)

## Skill Output:

**Output Type(s):** [Text, URL, Access code]

**Output Format:** [Plain-text deployment result with a live URL and, when password visibility is used, an access code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The access code is conditional on password-protected visibility.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

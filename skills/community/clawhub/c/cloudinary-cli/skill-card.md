## Description:

Uploads local files or remote URLs to Cloudinary through a CLI workflow with optional automatic image compression and batch uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mnhkahn](https://clawhub.ai/user/mnhkahn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure Cloudinary credentials and run upload commands for local files or remote URLs. It is suited for CDN upload workflows that need batch handling or Cloudinary q_auto image compression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill builds and runs local Go project code that is not included in the artifact evidence.

Mitigation: Inspect the local ./cmd/cli project and dependencies before installation, and run the workflow only in a trusted repository or isolated environment.

Risk: Cloudinary API credentials may be stored in plaintext at cmd/cli/.env.

Mitigation: Prefer a secret manager or ephemeral environment variables; if a .env file is used, keep it out of version control, restrict file permissions to the current user, and rotate exposed secrets.

## Reference(s):

- [Cloudinary CLI Skill Page](https://clawhub.ai/mnhkahn/skills/cloudinary-cli)
- [Go Downloads](https://go.dev/dl/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and environment variable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local file paths, remote URLs, Cloudinary credential variables, and upload command arguments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

ARKCloud IPFS helps agents upload, publish, list, delete, and check health for files or folders on file.arklink.hk, returning IPFS CIDs, access links, credit usage, and duplicate status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djanngau](https://clawhub.ai/user/djanngau)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to interact with ARKCloud/IPFS uploads from an agent workflow, including file or folder upload, upload listing, health checks, and destructive delete or unpublish actions when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles ARKCloud bearer tokens, client session cookies, and CSRF tokens.

Mitigation: Install only when the publisher is trusted, keep credentials out of logs and committed files, and rotate credentials if they may have been exposed.

Risk: Changing the ARKCLOUD_BASE_URL or --base-url target can direct credentialed requests away from the intended ARKCloud HTTPS service.

Mitigation: Keep ARKCLOUD_BASE_URL and --base-url fixed to the real ARKCloud HTTPS service unless a reviewed deployment explicitly requires another endpoint.

Risk: Folder uploads may include unintended files through broad directory traversal or symlinked content.

Mitigation: Inspect folders and symlinks before upload, and avoid uploading untrusted folders.

Risk: Delete and unpublish actions are destructive.

Mitigation: Require an explicit upload listing and exact upload ID confirmation before delete or unpublish actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djanngau/skills/arkcloud-ipfs)
- [ARKCloud IPFS skill homepage](https://github.com/djanngau/arkcloud-ipfs-skill)
- [ARKCloud file service](https://file.arklink.hk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ARKCloud environment variables for upload tokens, optional client session credentials, CSRF tokens, and base URL selection.]

## Skill Version(s):

0.1.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

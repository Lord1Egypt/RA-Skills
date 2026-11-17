## Description:

Manage Ghost CMS blog posts via Admin API, including creating, updating, deleting, listing, image uploads, and feature images using a JSON configuration file with API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manifoldor](https://clawhub.ai/user/manifoldor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to let an agent manage Ghost CMS posts through the Ghost Admin API. It is suited for credential-backed blog administration tasks such as drafting, publishing, updating, deleting, listing posts, and uploading images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, update, and delete live Ghost CMS content.

Mitigation: Require explicit human confirmation before publishing or deleting content, and use drafts when possible.

Risk: The skill depends on a configuration file containing Ghost Admin API credentials.

Mitigation: Use a dedicated low-privilege Ghost integration, keep the config file out of version control, and restrict file permissions.

Risk: Misconfigured API destinations or untrusted remote feature-image URLs can affect where requests are sent or what content is fetched.

Mitigation: Use only HTTPS Ghost API URLs, verify the configured API URL before use, and avoid untrusted remote feature-image URLs.

## Reference(s):

- [Ghost Admin API Reference](references/api.md)
- [Ghost Official Admin API Docs](https://ghost.org/docs/admin-api/)
- [ClawHub Skill Page](https://clawhub.ai/manifoldor/skills/ghost)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Ghost Admin API when the user supplies a configuration file containing credentials.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

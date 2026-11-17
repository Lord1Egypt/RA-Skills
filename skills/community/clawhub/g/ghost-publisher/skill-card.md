## Description:

Publish markdown articles to any Ghost 5 CMS site. The first reference implementation of Publisher Interface v1 -- a CMS-agnostic contract for editorial workflows. Handles the full publish pipeline (create, convert markdown to Ghost Lexical, upload feature image, publish) and exposes every interface method (create, update, publish, schedule, delete, upload, get). Works with self-hosted Ghost and Ghost Pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[machinesofdesire](https://clawhub.ai/user/machinesofdesire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editorial workflow builders, and publishing teams use this skill to let agents create, update, schedule, publish, delete, upload images for, and fetch posts on Ghost 5 sites through a common Publisher Interface v1 contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, delete, schedule, and send newsletter content on a live Ghost site.

Mitigation: Use a staging site first, restrict invocation of publish/delete/newsletter actions, and issue the Ghost integration only the access needed for the intended workflow.

Risk: The skill can fetch remote image URLs and read local image paths for uploads.

Mitigation: Avoid untrusted image URLs or local paths and run the skill with network and filesystem access limited to approved content and media directories.

Risk: Ghost credentials grant administrative publishing capability.

Mitigation: Store GHOST_ADMIN_API_KEY only in the runtime environment, use HTTPS Ghost URLs, and rotate the key if exposed.

## Reference(s):

- [Publisher Interface v1](INTERFACE.md)
- [Ghost Publisher README](README.md)
- [Ghost Publisher ClawHub Page](https://clawhub.ai/machinesofdesire/skills/ghost-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance, Python calls, shell commands, JSON-compatible post objects, and Ghost post URLs or confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GHOST_URL and GHOST_ADMIN_API_KEY; optional GHOST_PUBLISHER_CONFIG controls non-secret defaults such as author mappings, newsletter ID, and image size limit.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

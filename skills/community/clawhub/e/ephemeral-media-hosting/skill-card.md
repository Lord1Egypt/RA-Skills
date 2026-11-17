## Description:

Guides developers through setting up temporary media hosting with automatic retention cleanup, MIME validation, nginx configuration, upload handling, external image fetching, and basic monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byron-mckeeby](https://clawhub.ai/user/byron-mckeeby)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan and configure a temporary media sharing service for chat workflows, including upload handling, retention cleanup, MIME checks, nginx routing, and operational monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server-side fetching of arbitrary URLs can expose internal services or follow unsafe redirects.

Mitigation: Restrict remote fetches to trusted domains, block private or internal IP ranges and redirects, and review fetch behavior before deployment.

Risk: Metadata sidecar files may publicly expose uploader IPs, source URLs, original filenames, or other operational details.

Mitigation: Move metadata files outside the public web root or deny direct web access, and minimize retained uploader and source metadata.

Risk: Setup examples include sudo, permission changes, and cron installation that modify a host system.

Mitigation: Require explicit operator approval and environment review before running privileged or scheduled commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/byron-mckeeby/skills/ephemeral-media-hosting)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, nginx, and PHP code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment-oriented examples for media directories, cleanup cron, MIME validation, upload handling, external image fetching, and monitoring.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

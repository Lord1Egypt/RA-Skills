## Description:

Generates images, videos, or audio by selecting and invoking an appropriate dLazy model for the user's request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and small teams use this skill to route image, video, and audio generation requests to dLazy models for media creation, editing, conversion, dubbing, and structured result handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and referenced local media may be uploaded to dLazy-hosted services.

Mitigation: Avoid sensitive, unauthorized, or copyright-protected media, and confirm user intent before sending local files.

Risk: The skill can install or execute the @dlazy/cli and may persist an API key under the user's home directory.

Mitigation: Review the exact CLI version before installation and prefer a per-session DLAZY_API_KEY when credential persistence is not desired.

Risk: Server-resolved GitHub provenance is unavailable and the artifact text contains version and provenance inconsistencies.

Mitigation: Use server release metadata for this card and review the pinned @dlazy/cli version before global installation.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/thcjp/skills/dlazy-gen)
- [dLazy Homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output envelopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media outputs are returned as URLs from the dLazy service when CLI calls succeed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

ByteDance's latest video generation model. Supports multi-modal reference (images, video, audio) to generate videos, as well as first/last frame and text-to-video modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators can use an agent to generate videos from text prompts, reference images, video or audio, or first and last frame images, with selectable duration, resolution, aspect ratio, and audio generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is benign but medium confidence and partial; it flagged a mismatch involving a reported login command and unresolved references.

Mitigation: Review the login flow and unresolved skill sections, and inspect the CLI package before installing or authenticating.

Risk: Prompts and local reference media are sent to dLazy-hosted services for generation.

Mitigation: Only submit prompts and media permitted for external processing, and review the service terms before use.

Risk: The CLI requires an API key and stores it in a user-level configuration file.

Mitigation: Keep the key private, use the account controls to rotate or revoke it when needed, and avoid placing it in prompts or shared logs.

## Reference(s):

- [CLI project page (linked in skill metadata)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Video and media assets, JSON]

**Output Format:** [Generated media files or hosted media URLs, with a JSON result envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media varies by prompt and generation mode; results may be returned as URLs or saved files.]

## Skill Version(s):

1.3.39 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

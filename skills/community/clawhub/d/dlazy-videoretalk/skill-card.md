## Description:

Uses Tongyi VideoRetalk to synchronize a speaker’s mouth movements in a video to a supplied audio track, with an optional reference face image for selecting among multiple people.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators can use the skill to adapt a talking-person video to a new voice track, optionally selecting a face when multiple people appear. The documented workflow requires a dLazy API key and sends media to the hosted service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that the inspected content appears to initiate CLI login rather than demonstrate the advertised lip-sync workflow, and the CLI authentication behavior was not fully assessed.

Mitigation: Verify the installed CLI’s actual behavior and authentication flow before providing media or credentials.

Risk: The documented workflow sends prompts to dLazy’s hosted API and uploads local media to its storage service.

Mitigation: Use media you have permission to process, avoid sensitive material, and review the service terms before uploading.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-videoretalk)
- [dLazy CLI project (metadata link; provenance unavailable)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [Generated media asset returned by the CLI as a JSON response with a URL, or saved to a local file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video, audio, and optional reference-face inputs; generation may run asynchronously.]

## Skill Version(s):

1.3.41 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

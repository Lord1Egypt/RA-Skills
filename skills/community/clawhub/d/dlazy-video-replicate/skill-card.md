## Description:

Extracts a source video's first frame and audio, uses video understanding to prepare a prompt, and returns a Seedance 2.0 replication bundle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use the skill to analyze a reference video and prepare a first-frame, audio, and video bundle for recreating it with Seedance 2.0. The skill sends prompts to dLazy's hosted API and uploads local media inputs to its media service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found login and authentication setup that does not match the skill's stated video-replication purpose; the scan was partial.

Mitigation: Before installing, check that the login and API-key setup match expectations and manually review the padded section, as the scan guidance advises.

Risk: Local media inputs are uploaded to dLazy's hosted media service, and prompts are sent to its hosted API.

Mitigation: Review the service terms and avoid submitting media or prompts you are not comfortable sending to dLazy.

## Reference(s):

- [dLazy service homepage](https://dlazy.com)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Images, Audio, Video, Prompt text]

**Output Format:** [JSON response containing media output URLs, with an optional asynchronous task ID and status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media URLs are hosted by dLazy's media service.]

## Skill Version(s):

1.3.41 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

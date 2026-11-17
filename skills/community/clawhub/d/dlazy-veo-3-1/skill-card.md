## Description:

Generate high-quality cinematic effects videos with Google Veo 3.1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to generate short cinematic videos from text prompts, reference images or frames, or an existing video, and optionally save the results locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found no AIG issues, but confidence is medium and coverage is incomplete; several references could not be resolved, and the login flow's connection to video generation was not established.

Mitigation: Before installing, review the CLI and its access requirements, including the login and API key flow.

Risk: Prompts and local media supplied for generation are sent to dLazy's hosted API and media storage.

Mitigation: Submit only prompts and media you are authorized to share, and protect the dLazy API key.

## Reference(s):

- [dLazy CLI repository (link listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Video files, JSON generation status and output metadata]

**Output Format:** [Generated video assets as downloadable files or URLs, with JSON status responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation accepts a text prompt and optional reference media and settings; results can be saved locally.]

## Skill Version(s):

1.3.40 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

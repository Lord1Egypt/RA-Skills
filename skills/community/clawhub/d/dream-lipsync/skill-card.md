## Description:

Dream LipSync synchronizes lip movements in videos with supplied audio using the LipSync 2.0 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hy-1990](https://clawhub.ai/user/hy-1990)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a guide for configuring a DreamAPI key, preparing media URLs or uploads, submitting lip-sync jobs, and polling for completed video results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends video, audio, and related metadata to DreamAPI/NewportAI and its OSS storage flow.

Mitigation: Use only media you are authorized to process, avoid confidential or non-consensual content, and review the provider's privacy and retention terms before use.

Risk: The skill requires an API key for external service calls.

Mitigation: Store DREAMLIPSYNC_API_KEY in the agent configuration or secret manager rather than placing credentials in prompts, logs, or shared files.

## Reference(s):

- [Dream LipSync ClawHub page](https://clawhub.ai/hy-1990/skills/dream-lipsync)
- [Publisher profile](https://clawhub.ai/user/hy-1990)
- [LipSync 2.0 API reference](https://api.newportai.com/api-reference/LipSync-2.0)
- [DreamAPI get started](https://api.newportai.com/api-reference/get-started)
- [Dreamface tools](https://tools.dreamfaceapp.com/home)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown instructions with shell command, JSON request, and API endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; expected workflows require DREAMLIPSYNC_API_KEY and external media URLs or uploads.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Autonomous music generation DAW for breakcore, dubstep, phonk, and 404-style tracks that synthesizes drums, bass, effects, voice chops, and machine voice parts locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and music creators use this skill to run a local music-generation service that produces WAV tracks, drumkits, and chopped voice samples from code-driven presets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes an unauthenticated network service that can be unsafe if port 9112 is reachable from a network.

Mitigation: Run it only in a restricted local sandbox, bind or firewall the service to localhost, and do not expose port 9112 externally.

Risk: The service can read and write local files without adequate path safeguards.

Mitigation: Limit filesystem access to disposable input and output directories, and avoid granting access to sensitive files until fixed path validation is added.

Risk: Render and request handling lack explicit request, duration, or output limits.

Mitigation: Apply request size, render duration, and disk quotas before shared or unattended use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses; generated artifacts are WAV audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local synthesis is documented with no external API calls; generated tracks, drumkits, and chopped samples are written as local WAV files.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

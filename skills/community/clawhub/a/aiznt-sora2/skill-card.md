## Description:

Sora2 Video submits text-to-video generation tasks through configured Tianshu proxy URLs and fetches task status and generated outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to submit Sora2 text-to-video prompts, then poll task IDs to retrieve status and generated video output through configured Tianshu credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A sensitive bearer token may be sent to untrusted proxy URLs if AIZNT_PROXY_URLS is misconfigured or modified by an untrusted source.

Mitigation: Use only AIZNT_PROXY_URLS values from a trusted Tianshu/TsClaw source, require HTTPS endpoints you trust, keep TS_TOKEN secret, and rotate the token if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangshengli0421/skills/aiznt-sora2)
- [Publisher profile](https://clawhub.ai/user/wangshengli0421)

## Skill Output:

**Output Type(s):** [shell commands, JSON, configuration]

**Output Format:** [JSON responses from Node CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TS_TOKEN and trusted AIZNT_PROXY_URLS configuration; no npm dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

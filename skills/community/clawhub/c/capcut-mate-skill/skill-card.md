## Description:

Automates CapCut video editing by creating projects, adding media assets, and rendering videos through the CapCut Mate API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[excalibur9527](https://clawhub.ai/user/excalibur9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate CapCut/Jianying editing workflows, including draft creation, media insertion, captions, effects, and video rendering through a configured CapCut Mate API service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media project data is sent to the configured CapCut Mate API service.

Mitigation: Use a trusted server, keep the default localhost setup when possible, avoid sending private media to untrusted remote endpoints, and prefer HTTPS for non-local servers.

Risk: Production dependency behavior may change if dependencies are not pinned.

Mitigation: Pin dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/excalibur9527/skills/capcut-mate-skill)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CAPCUT_MATE_URL to route requests to the configured CapCut Mate API service.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

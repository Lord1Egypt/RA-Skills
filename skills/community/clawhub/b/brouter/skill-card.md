## Description:

Generate GPX bike routes via brouter.de for bike trips between two places, optionally using a routing profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[si-gr](https://clawhub.ai/user/si-gr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn bike route requests into GPX files for navigation, with routing profiles selected from the user's speed, safety, or bike-type preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Precise route coordinates are sent to brouter.de using plain HTTP.

Mitigation: Use only with routes the user intends to disclose, prefer trusted networks, and consider an HTTPS-capable or self-hosted routing endpoint before sensitive use.

Risk: Generated GPX output can be written to caller-directed paths.

Mitigation: Constrain outputDir and fileName to a dedicated routes directory and reject path traversal or absolute paths.

Risk: Route coordinates, labels, request URLs, and output paths are logged locally.

Mitigation: Minimize logged location data, document retention, and delete local route logs when they are no longer needed.

## Reference(s):

- [brouter.de routing service](https://brouter.de)
- [ClawHub Brouter skill page](https://clawhub.ai/si-gr/skills/brouter)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [GPX file plus a structured result containing the generated file path, selected profile, and request status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated GPX route files locally and returns a file attachment path.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

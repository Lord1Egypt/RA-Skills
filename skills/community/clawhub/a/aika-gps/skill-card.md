## Description:

Retrieve and track technicians' real-time GPS locations, find the nearest technician, calculate distance and ETA, and support geofence-based job monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[comphone](https://clawhub.ai/user/comphone)

### License/Terms of Use:

MIT-0

## Use Case:

Dispatch teams and service operators use this skill to query technician locations, identify the closest qualified technician for a customer site, and estimate travel distance or arrival time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaged live-location access includes plaintext AIKA credentials and device identifiers.

Mitigation: Rotate the packaged credentials and remove plaintext secrets and device identifiers before installation or use.

Risk: The package includes insecure HTTP fallback endpoints for AIKA access.

Mitigation: Disable HTTP endpoints and require HTTPS-only connections before deployment.

Risk: Users can query technician location data without explicit authorization or privacy controls described in the release evidence.

Mitigation: Add authorization, access logging, and privacy controls before allowing location queries in a real environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/comphone/skills/aika-gps)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with Python command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include technician location, device status, distance, ETA, skills, and error messages.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

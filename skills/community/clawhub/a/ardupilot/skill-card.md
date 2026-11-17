## Description:

Helps agents connect to ArduPilot flight controllers with pymavlink and produce guidance for status checks, arming, takeoff, local movement, and landing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luweiliao](https://clawhub.ai/user/luweiliao)

### License/Terms of Use:


## Use Case:

Developers, drone operators, and robotics engineers use this skill to draft pymavlink-based procedures for connecting to and controlling ArduPilot drones. It is best suited for authorized flight-controller work in SITL or another controlled test setup before any real vehicle use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce drone-control procedures, and the security evidence flags unsafe force-arming and immediate takeoff patterns in the default examples.

Mitigation: Use only with explicit human authorization and preferably in SITL or another controlled test setup; remove force-arming from normal workflows before real vehicle use.

Risk: Commands could target the wrong vehicle or run without adequate flight-readiness checks.

Mitigation: Before real vehicle use, verify the exact vehicle target, wait for command acknowledgements, validate GPS, EKF, battery, geofence, failsafes, and launch-area safety.

Risk: Unpinned pymavlink installation may introduce dependency drift.

Mitigation: Pin pymavlink in a dedicated virtual environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luweiliao/skills/ardupilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output should be reviewed before execution against the exact vehicle, environment, and flight safety requirements.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

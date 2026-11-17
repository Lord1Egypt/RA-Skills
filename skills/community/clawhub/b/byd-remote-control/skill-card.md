## Description:

Control and check a BYD vehicle using portable Python helper scripts built on pyBYD for battery checks, battery alerts, locking, light or horn flashing, and climate control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiimivantang](https://clawhub.ai/user/hiimivantang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate reusable local scripts for BYD vehicle status checks and selected remote-control actions. It is suited to battery monitoring, explicit vehicle targeting, and controlled execution of lock, lights, horn, and climate commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access BYD account credentials, control PINs, VINs, telemetry, and remote controls for a real vehicle.

Mitigation: Install only in trusted environments, protect the scripts/.env file, avoid committing credentials, and confirm state-changing actions before execution.

Risk: If BYD_VIN or BYD_VEHICLE_ALIAS is unset, scripts use the first vehicle returned by the account.

Mitigation: Set BYD_VIN or BYD_VEHICLE_ALIAS explicitly before running scripts that change vehicle state.

Risk: The climate-control scripts may continue after command-access verification fails.

Mitigation: Review or patch start_ac.py and stop_ac.py so failed command-access verification stops execution before using those scripts.

## Reference(s):

- [Setup](references/setup.md)
- [ClawHub Skill Page](https://clawhub.ai/hiimivantang/skills/byd-remote-control)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text]

**Output Format:** [Markdown guidance with shell commands and JSON or text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include live vehicle telemetry, selected VIN values, command responses, and battery alert payloads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

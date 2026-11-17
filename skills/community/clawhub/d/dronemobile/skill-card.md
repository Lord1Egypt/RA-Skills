## Description:

Control DroneMobile-connected vehicles through remote start, engine stop, door lock and unlock, trunk release, battery checks, and vehicle status requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryantegomoh](https://clawhub.ai/user/bryantegomoh)

### License/Terms of Use:

MIT-0

## Use Case:

External users with DroneMobile-connected vehicles use this skill through an agent to request vehicle status and remote actions such as start, stop, lock, unlock, and trunk release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform real-world vehicle actions with weak guardrails.

Mitigation: Review before installing and require manual confirmation before start, stop, unlock, or trunk commands.

Risk: Vehicle targeting may be ambiguous on multi-vehicle accounts.

Mitigation: Set DRONEMOBILE_DEVICE_KEY for the exact vehicle before using action commands.

Risk: Dependency behavior may vary if installed directly into a shared environment.

Mitigation: Use a dedicated trusted environment, preferably a virtualenv with pinned dependencies.

## Reference(s):

- [DroneMobile Skill Page](https://clawhub.ai/bryantegomoh/skills/dronemobile)
- [drone_mobile_python Pull Request 18](https://github.com/bjhiltbrand/drone_mobile_python/pull/18)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text status output and error messages from a Python CLI script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DRONEMOBILE_EMAIL and DRONEMOBILE_PASSWORD; DRONEMOBILE_DEVICE_KEY is optional for selecting a specific vehicle.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

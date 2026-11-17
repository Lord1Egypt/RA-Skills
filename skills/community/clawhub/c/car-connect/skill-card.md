## Description:

Control multiple car brands (Tesla, Mercedes, Volkswagen, Toyota, Ford, Kia, Honda) from macOS via their official connected APIs. Supports vehicle status, lock/unlock, climate control, charge/fuel, location, tyres, trunk, windows, horn, and more. Use when you want to check or control your car remotely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadlybutsoft](https://clawhub.ai/user/deadlybutsoft)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check vehicle state and issue remote vehicle-control commands through supported connected-car APIs. It is intended for terminal-driven workflows such as status checks, lock and unlock, climate control, charge and fuel checks, location lookup, tyre pressure checks, windows, trunk, horn, and engine operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vehicle-control commands can change real-world vehicle state, and bulk execution may apply a command across configured brands.

Mitigation: Verify the brand, vehicle, and command manually before using --yes, and avoid --all for commands that change vehicle state.

Risk: Location output and locally cached connected-car data can expose sensitive personal information.

Mitigation: Treat location output, VINs, command logs, and ~/.car_connect contents as sensitive; avoid sharing or committing them.

Risk: Some Mercedes and Volkswagen paths may report placeholder or fake success rather than confirmed API results.

Mitigation: Avoid Mercedes and Volkswagen control commands unless the implementation has been reviewed and verified against the intended official API behavior.

## Reference(s):

- [Car Connect ClawHub Skill Page](https://clawhub.ai/deadlybutsoft/skills/car-connect)
- [deadlybutsoft Publisher Profile](https://clawhub.ai/user/deadlybutsoft)
- [Author GitHub Profile](https://github.com/deadlybutsoft)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; command output may be plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing commands are gated by --yes in the documented interface, and the skill relies on per-brand environment variables and local token files.]

## Skill Version(s):

3.0.0 (source: server release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

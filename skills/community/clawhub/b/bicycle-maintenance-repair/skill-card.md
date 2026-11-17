## Description:

Helps an agent guide bicycle and e-bike maintenance by diagnosing reported symptoms, scheduling mileage-based service, sourcing compatible parts, maintaining local repair logs, and escalating unsafe repairs to a professional shop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External riders and delivery workers use this skill to keep a primary bicycle or e-bike roadworthy with agent-assisted diagnostics, maintenance planning, parts logistics, service history, reminders, and safety escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses npx and may resolve a moving package version.

Mitigation: Install in a least-privileged environment and prefer a pinned, reviewed clawhub version when available.

Risk: The skill can store bike, mileage, parts, reminder, and repair-history details on the local filesystem.

Mitigation: Only provide information suitable for local storage and periodically review or remove generated maintenance files.

Risk: Incorrect or overconfident repair guidance could lead to unsafe riding when brakes, steering, frame integrity, wheels, or e-bike electrical systems are involved.

Mitigation: Stop riding and escalate to a certified shop for cracked frames, bent wheels, brake or steering faults, unsafe workspace, or repairs beyond the rider's confidence; follow manufacturer torque and e-bike battery warnings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/bicycle-maintenance-repair)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with checklists, templates, service-log entries, shopping lists, reminder guidance, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local filesystem maintenance logs and reminder records when filesystem access is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

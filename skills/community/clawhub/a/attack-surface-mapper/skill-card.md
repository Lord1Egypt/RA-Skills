## Description:

Purple team - map an agent's full attack surface by combining red team probes and blue team detections, then identify defense coverage gaps and prioritize hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arhadnane](https://clawhub.ai/user/arhadnane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to combine red-team results and blue-team detection artifacts into an agent attack-surface coverage matrix and prioritized hardening plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may underreport or misclassify some coverage gaps because of reporting-accuracy bugs.

Mitigation: Treat reports as advisory and validate important findings against the underlying security artifacts before changing defenses.

Risk: The skill reads local security logs and audit artifacts that can contain sensitive posture information.

Mitigation: Run it only in trusted workspaces and keep generated .security/surface-map reports confidential.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arhadnane/skills/attack-surface-mapper)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Files]

**Output Format:** [JSON or Markdown report containing a coverage matrix, summary counts, and prioritized hardening plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local security artifacts and writes reports under .security/surface-map.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

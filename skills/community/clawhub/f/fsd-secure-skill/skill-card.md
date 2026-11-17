## Description:

PolaBea runs a camera-only autonomous-driving simulation with dual-pass path checks, temporal consistency checks, and emergency-stop console output.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[aadipapp](https://clawhub.ai/user/aadipapp)

### License/Terms of Use:

MIT

## Use Case:

Developers and safety reviewers use this demonstration skill to run a local autonomous-driving simulation and inspect frame-by-frame safety check output. It should not be used as evidence that any real vehicle-control system is safe or deployment-ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake simulation-only camera safety logic or emergency-stop messages for evidence of real vehicle-control readiness.

Mitigation: Use the skill only as a toy or demonstration simulation, and do not deploy it for any real vehicle or safety-critical control task.

Risk: Randomized frame data and console actions can make the simulated safety behavior appear more complete than it is.

Mitigation: Treat the output as illustrative console text for review, not as validation data or operational safety evidence.

## Reference(s):

- [Artifact README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/aadipapp/skills/fsd-secure-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Console text and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Simulation output is randomized and intended for demonstration review only.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

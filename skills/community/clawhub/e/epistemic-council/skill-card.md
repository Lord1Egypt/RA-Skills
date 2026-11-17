## Description:

Manage and execute Epistemic Council pipeline operations for cross-domain reasoning, status checks, claim validation, boundary audits, gap detection, and adversarial re-challenges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[su-ariel](https://clawhub.ai/user/su-ariel)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run a local Epistemic Council reasoning pipeline, inspect substrate health, validate claims, audit boundaries, find evidence gaps, and re-challenge high-confidence insights. It is intended for workflows that need structured cross-domain reasoning with adversarial validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run scripts and write persistent memory or state.

Mitigation: Install only after reviewing permissions and limit write access to the minimum files needed for the intended workflow.

Risk: The manifest grants broader workspace authority than the skill purpose requires.

Mitigation: Narrow workspace permissions before deployment, especially access to user, identity, agent, and tool configuration files.

Risk: The skill depends on a localhost model service for parts of the pipeline.

Mitigation: Use only with a trusted local model service and confirm requests do not leave the intended local environment.

Risk: Memory compression can update generated memory content.

Mitigation: Review or disable memory compression unless generated memory updates are quarantined and approved before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/su-ariel/skills/epistemic-council)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and text or JSON status outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Python entrypoints, can update persistent workspace state, and expects a trusted localhost model service.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

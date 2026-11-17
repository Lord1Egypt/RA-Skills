## Description:

Checks third-party ClawHub skill files before installation and reports hosts, uploads, credential-path reads, and an install action with file and line evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill before installing third-party ClawHub skills or running their scripts, so they can review network hosts, upload behavior, credential-path reads, and install-blocking findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated install policy could mis-handle the documented verdict mismatch.

Mitigation: Map both verdict schemes consistently and always block suspicious or DO_NOT_INSTALL findings before allowing installation.

Risk: The skill depends on the separate clawphylax plugin for full functionality.

Mitigation: Review and approve the clawphylax plugin separately before relying on this skill for automated install decisions.

Risk: Static scanning cannot prove that later-downloaded scripts or remote services are safe.

Mitigation: Use runtime network auditing for installed skills and treat a clean static scan as limited text evidence, not a safety guarantee.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/clawphylax-verify)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text safety verdict with host names and file:line findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports ACTION: INSTALL_OK, ACTION: REVIEW_WITH_USER, or ACTION: DO_NOT_INSTALL as the first line.]

## Skill Version(s):

1.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

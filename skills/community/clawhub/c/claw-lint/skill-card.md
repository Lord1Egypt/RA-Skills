## Description:

Security scanner for OpenClaw skills. Detects malware and backdoors before execution, scores risk levels, and monitors file integrity through static code analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parthghumatkar](https://clawhub.ai/user/parthghumatkar)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use Claw-lint to run local static audits of installed OpenClaw skills before execution, review risk scores and audit flags, and generate text or JSON summaries for operational review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate its security guarantees, especially around documented SHA256 inventory output and CI/CD JSON examples.

Mitigation: Treat results as heuristic review signals, manually review high-impact skills, and verify the active implementation before relying on inventory baselines or CI/CD gates.

## Reference(s):

- [Claw-lint ClawHub skill page](https://clawhub.ai/parthghumatkar/skills/claw-lint)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Terminal text tables or JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON output requires Python 3; SHA256 inventory behavior should be verified before operational reliance.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

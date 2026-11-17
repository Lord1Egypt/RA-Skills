## Description:

Skillguard runs a complete security audit on OpenClaw SKILL.md content by combining malware scanning, permission scope analysis, and prompt injection detection into a unified SAFE/CAUTION/DANGEROUS verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Skillguard to audit OpenClaw skill definitions before installation, release, or review. The skill returns a unified security verdict with sub-reports for malware indicators, declared and detected permission scope, and prompt injection patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill starts a local Python web service and imports scanner modules from the local environment.

Mitigation: Install it only in a trusted environment, pin or review Python dependencies when reproducibility matters, and verify scanner modules before relying on audit verdicts.

Risk: Audit verdicts depend on scanner coverage and may not catch every malicious, over-scoped, or prompt-injection pattern.

Mitigation: Treat SAFE/CAUTION/DANGEROUS as review support and inspect the returned sub-reports before installing or releasing a skill.

Risk: The API processes user-supplied SKILL.md content, which may include sensitive unpublished skill text.

Mitigation: Run the service locally or behind trusted access controls and avoid sending confidential skill content to untrusted deployments.

## Reference(s):

- [Skillguard ClawHub listing](https://clawhub.ai/mirni/skills/gh-skillguard)
- [mirni publisher profile](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [JSON, analysis, guidance]

**Output Format:** [JSON response with verdict, finding counts, and nested scan, scope, and injection reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a local FastAPI service; request body accepts raw SKILL.md text up to 500,000 characters.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

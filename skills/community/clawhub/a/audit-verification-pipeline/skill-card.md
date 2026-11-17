## Description:

Guides Solidity auditors through a three-level verification process using Foundry tests, GitHub CI, and auditor review before submitting findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzengbaao](https://clawhub.ai/user/yuzengbaao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and Solidity auditors use this skill to verify audit findings with deterministic PoCs, CI checks, and human review before external submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example GitHub Actions workflow should be hardened before copying into a repository.

Mitigation: Pin GitHub Actions to full commit SHAs and set explicit least-privilege permissions before use.

Risk: The workflow is intended for Chinese-language Solidity and Foundry audit processes.

Mitigation: Install and use it only when reviewers are comfortable applying that workflow and toolchain.

Risk: External finding submission can carry quality and platform-account consequences.

Mitigation: Keep the external-submission step under human auditor review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuzengbaao/skills/audit-verification-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Solidity, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is bundled; generated CI examples should be reviewed before use]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

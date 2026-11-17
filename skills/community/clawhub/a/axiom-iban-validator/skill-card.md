## Description:

Checks IBAN format and mod-97 checksums with country-specific length rules using local Python standard-library code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to pre-validate international bank account numbers before payment submission, customer data audits, or payment form checks. It validates format and checksum only; it does not prove that an account exists or is safe to pay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A valid IBAN result may be mistaken for proof that the bank account exists or is safe to pay.

Mitigation: Use the skill only for local format and checksum pre-validation, and rely on separate banking or account-verification controls before payment.

Risk: Documentation mismatches may overstate coverage or include examples that need correction.

Mitigation: Review the artifact documentation and test commands before integration, and verify country coverage against the code and tests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiom-iban-validator)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, code, guidance]

**Output Format:** [Plain text or JSON validation results with optional Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local deterministic validation; no network calls, credential use, persistence, or destructive actions reported by security evidence.]

## Skill Version(s):

0.1.2 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

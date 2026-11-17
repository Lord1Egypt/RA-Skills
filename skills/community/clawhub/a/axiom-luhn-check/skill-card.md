## Description:

Validates number strings with the Luhn algorithm and detects common credit card, SIRET/SIREN, IMEI, and ISBN identifier types using the Python standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to validate Luhn check digits and generate CLI or JSON results for card-like numbers, SIRET/SIREN, IMEI, and ISBN identifiers. It is appropriate for checksum screening, not PCI-grade payment validation or authoritative ISBN validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full identifiers, including card-like numbers, can appear in command output or JSON fields.

Mitigation: Use synthetic or test numbers, avoid real card data, and mask or omit identifiers before sharing logs or outputs.

Risk: The skill performs checksum screening only and can overstate payment-card or ISBN validation.

Mitigation: Treat results as a preliminary Luhn check and use domain-specific validation, BIN/IIN data, PCI-compliant tooling, or ISBN-specific checks where required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiom-luhn-check)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Code]

**Output Format:** [Plain text or JSON validation results, with optional shell command and Python usage examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local checksum-only validation; JSON output may include the full normalized digits from the input.]

## Skill Version(s):

0.1.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

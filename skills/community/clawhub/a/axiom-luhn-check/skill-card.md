## Description: <br>
axiom-luhn-check is a local Python Luhn checksum helper for number strings with best-effort type detection for credit cards, SIRET/SIREN, IMEI, and ISBN-like inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to propose local CLI or Python checks for Luhn-style identifiers and to inspect checksum status in text or JSON form. It is suitable for lightweight pre-checks, not authoritative payment-card, issuer, ISBN, or compliance validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the ISBN validation claims are inaccurate and should not be trusted for authoritative identifier checks. <br>
Mitigation: Use the skill only as a simple local Luhn checksum helper unless the per-identifier algorithms are corrected and tested. <br>
Risk: The artifact and security guidance state that this is not full PCI, issuer, business-identifier, or compliance validation. <br>
Mitigation: Pair any checksum result with domain-specific validation, issuer or registry checks, and applicable compliance review before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axiom-luhn-check) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python examples; the underlying utility can emit plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local stdlib Python execution; no network, credential, or persistence behavior identified by security evidence.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

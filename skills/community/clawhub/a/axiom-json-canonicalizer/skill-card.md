## Description: <br>
Canonicalizes JSON into deterministic UTF-8 output for hashing, signing, and comparison, with independent validation needed before relying on it as an RFC 8785/JCS implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers can use this skill to normalize JSON before hashing, signing, comparison, or audit-log workflows. Because the security review says its RFC 8785/JCS claims do not match the implementation, treat it as a custom offline JSON normalizer unless independent test vectors confirm suitability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review found no exfiltration behavior, but found that the skill's security-sensitive RFC 8785/JCS claims do not match the implementation. <br>
Mitigation: Treat it as a custom offline JSON normalizer; do not rely on it for cryptographic signatures, JWT/OAuth payloads, audit logs, or interoperability with other JCS implementations without independent test vectors and acceptance of its NFC normalization and number formatting. <br>
Risk: License signals conflict between server release metadata and artifact files. <br>
Mitigation: Confirm the authoritative license terms before commercial reuse or redistribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axiom-json-canonicalizer) <br>
- [JSON Canonicalization Scheme (RFC 8785)](https://www.rfc-editor.org/rfc/rfc8785) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands] <br>
**Output Format:** [Canonical JSON as UTF-8 text or bytes, with CLI verification status and Python API snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline Python standard-library tool; do not rely on its output for JCS interoperability or cryptographic workflows without independent validation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata and SKILL.md frontmatter; artifact manifest and README also mention 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

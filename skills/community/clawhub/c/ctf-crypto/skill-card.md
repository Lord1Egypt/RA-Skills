## Description:

Provides cryptography attack techniques for CTF challenges involving ciphers, hashes, signatures, ZKP, PRNGs, RSA, ECC, lattices, LWE, CVP, number theory, padding oracles, key derivation, and stream or block cipher weaknesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli](https://clawhub.ai/user/gandli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CTF participants use this skill as a quick reference for selecting and applying cryptanalysis techniques during authorized capture-the-flag challenges and lab exercises.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes reusable techniques for token prediction, password cracking, request flooding, and unsafe install or code examples.

Mitigation: Use it only for authorized CTFs, labs, owned systems, or systems with explicit testing permission.

Risk: Suggested commands and dependencies may execute attack tooling or install external packages.

Mitigation: Run tools in a disposable virtual environment or container, review target-facing requests before execution, and pin or verify external dependencies before installing them.

## Reference(s):

- [classic-ciphers.md](classic-ciphers.md)
- [modern-ciphers.md](modern-ciphers.md)
- [modern-ciphers-2.md](modern-ciphers-2.md)
- [stream-ciphers.md](stream-ciphers.md)
- [rsa-attacks.md](rsa-attacks.md)
- [rsa-attacks-2.md](rsa-attacks-2.md)
- [ecc-attacks.md](ecc-attacks.md)
- [zkp-and-advanced.md](zkp-and-advanced.md)
- [prng.md](prng.md)
- [advanced-math.md](advanced-math.md)
- [lattice-and-lwe.md](lattice-and-lwe.md)
- [exotic-crypto.md](exotic-crypto.md)
- [historical.md](historical.md)
- [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorized CTF or lab context; examples may depend on external tools such as Python packages, SageMath, hashcat, and RsaCtfTool.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

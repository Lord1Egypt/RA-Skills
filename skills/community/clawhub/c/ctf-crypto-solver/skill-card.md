## Description:

Helps agents identify and solve CTF cryptography challenges across RSA, AES modes, ECC, lattices, PRNGs, hashes, signatures, and related math attacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxy050208](https://clawhub.ai/user/yxy050208)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security trainees, and CTF participants use this skill to triage cryptography challenges, select likely attack paths, and draft solver code or shell commands in authorized CTF, training, or owned lab environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contains highly actionable cryptography attack playbooks that could be misused outside authorized CTF, training, or owned lab environments.

Mitigation: Use only for authorized CTF, training, or owned lab work, and do not apply exploit workflows to real services without explicit permission.

Risk: Examples may involve installing packages or cloning external repositories before running solver code.

Mitigation: Run examples in an isolated virtual environment or container, and review and pin packages or repositories before installation.

## Reference(s):

- [CTF Crypto Solver Skill Page](https://clawhub.ai/yxy050208/skills/ctf-crypto-solver)
- [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool)
- [CTF Cryptography](references/ctf-crypto/SKILL.md)
- [Classic Ciphers](references/ctf-crypto/classic-ciphers.md)
- [Modern Cipher Attacks](references/ctf-crypto/modern-ciphers.md)
- [Modern Cipher Attacks Continued](references/ctf-crypto/modern-ciphers-2.md)
- [Modern Cipher Attacks Part 3](references/ctf-crypto/modern-ciphers-3.md)
- [RSA Attacks](references/ctf-crypto/rsa-attacks.md)
- [RSA Attacks Part 2](references/ctf-crypto/rsa-attacks-2.md)
- [Elliptic Curve Attacks](references/ctf-crypto/ecc-attacks.md)
- [Lattice and LWE Attacks](references/ctf-crypto/lattice-and-lwe.md)
- [PRNG and Key Recovery](references/ctf-crypto/prng.md)
- [PRNG Attacks](references/ctf-crypto/prng-attacks.md)
- [Stream Cipher Attacks](references/ctf-crypto/stream-ciphers.md)
- [Advanced Mathematical Attacks](references/ctf-crypto/advanced-math.md)
- [ZKP, Solvers, and Advanced Techniques](references/ctf-crypto/zkp-and-advanced.md)
- [Exotic Algebraic Structures](references/ctf-crypto/exotic-crypto.md)
- [Exotic Algebraic Structures Part 2](references/ctf-crypto/exotic-crypto-2.md)
- [Historical Ciphers](references/ctf-crypto/historical.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference optional local tools such as Python packages, hashcat, SageMath, or RsaCtfTool depending on the challenge.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Multi-algorithm hash generator for files, strings, stdin, and manifests using MD5, SHA-1, SHA-256, SHA-512, and BLAKE2b with deterministic local execution and no external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and security practitioners use this skill to compute and compare hashes for local files, strings, stdin streams, and manifest entries. It is useful for integrity checks, deduplication, cross-verification across algorithms, and scriptable hash output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MD5 and SHA-1 are legacy algorithms and are not strong integrity or security guarantees for adversarial use. <br>
Mitigation: Use SHA-256, SHA-512, or BLAKE2b for normal integrity checks, and reserve MD5 or SHA-1 for legacy compatibility only. <br>
Risk: Hashing is not a substitute for password hashing, HMAC authentication, or cryptographic signatures. <br>
Mitigation: Use bcrypt or Argon2 for passwords, HMAC for keyed message authentication, and signing tools such as GPG or age when signatures are required. <br>
Risk: The tool reads local paths and manifests supplied by the user, and stress tests create temporary large files and invoke local system tools. <br>
Mitigation: Run it only on files and manifests intended for inspection, and run stress tests only in a development environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axiom-hash-multi) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with CLI and Python examples, plus plain-text or JSON hash results when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit single-algorithm or multi-algorithm digest results and comparison or manifest verification status.] <br>

## Skill Version(s): <br>
1.1.3 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

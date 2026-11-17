## Description:

Multi-algorithm hash generator for MD5, SHA-1, SHA-256, SHA-512, and BLAKE2b that hashes files, strings, stdin, or manifests with deterministic local execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and security practitioners use this skill to generate and compare file or string hashes across multiple algorithms, verify expected digests, and check manifest entries during local integrity workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manifest verification can read files outside the user's intended target set when manifest entries are untrusted or crafted.

Mitigation: Use only trusted manifests and prefer a patched version that confines entries to an intended base directory.

Risk: Hashing device files, FIFOs, arbitrary symlinks, or streams can read unexpected content or run indefinitely.

Mitigation: Avoid special files and arbitrary symlinks; prefer a patched version that rejects non-regular files by default.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiom-hash-multi)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands, Python snippets, plain-text digest output, and optional JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce single-digest strings, multi-algorithm digest maps, comparison status, or manifest verification summaries.]

## Skill Version(s):

1.1.3 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

# Security

Please report security issues privately through GitHub Security Advisories rather than a public issue.

The suite is local-first. File moves, review application, synchronization, indexing, browser-assisted file opening, and remote model calls must remain disabled until the user explicitly enables the corresponding execution gate.

Never include credentials, generated indexes, personal notes, local logs, or absolute user paths in bug reports.

Version 0.2.0 documents the trust model, per-operation capabilities, upgrade
requirements, and tested limits in `references/security-boundaries.md`.
Source documents and external tool output are not authorization. A security
scanner's previous verdict does not attest to a newly published package.

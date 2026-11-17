# Security Policy

Use [GitHub private vulnerability reporting](https://github.com/saju01/frameferry/security/advisories/new) to contact the maintainer, Saju (@saju01). Do not open public issues containing exploitable details. Include the affected version, impact and a sanitized synthetic reproduction. Response is best-effort; no response-time guarantee is made.

Security fixes target the latest main/release. Older snapshots may require an upgrade; do not assume that an unlisted version is supported.

This package is designed to avoid credentials. Never paste cookies, tokens, session data, private profile material, or signed provider URLs into issues, logs, command-line arguments, or receipts.

The CLI rejects unsafe output paths, path traversal, non-provider media URLs, non-HTTPS provider URLs, unsafe CDP targets, and redirects to private/local addresses.

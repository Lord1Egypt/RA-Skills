# Security Guidance

- Keep Gmail access read-only; do not add send/delete operations to this skill.
- Do not expose OAuth credentials, refresh tokens, or local secret paths.
- Do not return full message bodies by default; keep snippets short.
- Clamp result count via `MAIL_MAX_LIMIT`.
- Parse and normalize dates before passing to CLI.
- Use argument-based invocation and allowlisted subcommands (`scripts/run_cli.sh`).
- Reject unknown subcommands and malformed input safely.

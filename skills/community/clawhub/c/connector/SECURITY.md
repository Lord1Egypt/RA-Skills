# Security Policy

## Reporting a vulnerability

Please report security issues privately to the maintainers before public disclosure.
Include:

- affected version
- reproduction steps
- impact assessment

## Security model

The connector is designed with least-privilege principles:

- Outbound-only network calls to LaunchThatBot OpenClaw endpoints.
- No shell command execution.
- No filesystem reads outside configured token/secret files and optional queue file.
- No direct access to other OpenClaw instance data by default.

## Data handling

- Ingest token is expected via env var or secure file input.
- Optional request HMAC signing protects payload authenticity and replay window checks.
- Optional queue persistence writes to user config directory with restrictive file mode.

## Operator hardening checklist

- Run connector under a dedicated OS user with minimal permissions.
- Store secrets in a secret manager or environment injection, not shell history.
- Rotate ingest tokens regularly and revoke on suspected compromise.
- Enable signature enforcement on the server for production.
- Restrict egress rules to LaunchThatBot domain only.

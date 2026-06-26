# Risk Policy — codex-profiler

## Safe defaults
- Usage checks are read-only by default.
- Auth apply is explicit and should be queued safely.
- Profile delete actions require explicit confirmation.

## Allowed operations
- Local auth profile inspection and updates for Codex profile management.
- Codex usage probe via trusted HTTPS endpoint (`chatgpt.com`).
- OAuth start/finish handling for Codex profile refresh.

## Denied operations
- No remote shell execution (`curl|bash`, `wget|sh`).
- No `sudo`/SSH/system package or host mutation commands.
- No outbound calls to untrusted hosts for usage checks.
- Never echo full callback URLs/tokens in chat output.

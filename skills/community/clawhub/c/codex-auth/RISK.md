# Risk Policy — codex-auth

## Safe defaults
- OAuth operations are explicit and profile-targeted.
- Callback URLs are treated as sensitive and never echoed in full.
- Queue apply path is preferred for controlled restart behavior.

## Allowed operations
- OAuth start/finish with OpenAI auth endpoints.
- Local callback handling for localhost redirect flow.
- Auth profile file updates with lock coordination.

## Denied operations
- No remote shell execution (`curl|bash`, `wget|sh`).
- No `sudo`, SSH, package manager, or system mutation actions.
- No disclosure of full callback query params, access tokens, or refresh tokens.

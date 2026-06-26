# Security Notes

This local skill manages high-sensitivity Codex auth material.

It exists because third-party Codex relogin/account-switch helpers may do legitimate work, but they often have very high blast radius:

- They write OpenClaw auth profile files
- They process OAuth callback codes and refresh tokens
- They may rewrite session state
- They may restart the gateway
- They may install or execute remote shell code

That does not automatically make them malicious.
But it makes them risky enough that a small, reviewed, local implementation is preferable.

## Preferred security posture

- Local reviewed logic over downloaded shell scripts
- Official OpenAI OAuth endpoints only
- Minimal snapshot storage
- Minimal file mutation
- No unrelated config rewrites
- No surprise restarts
- No printing full tokens or refresh secrets

## Practical rule

Treat Codex account-switch tooling as authentication infrastructure, not as a casual convenience script.

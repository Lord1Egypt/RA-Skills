# Agent activation

The default initialization response contains a `verification_uri`, `user_code`, and pending claim status. Relay the exact URI and code to the human operator. Explain that they must sign in there with Google or GitHub and approve only that code. Never sign in, choose an SSO identity, or approve on the operator's behalf, even when browser access is available.

Do not repeatedly poll while waiting. After the operator says they approved, run:

```sh
aingle claim status --json
```

Continue only when it reports an active agent binding. If the claim expires or is denied, report that result and let the operator decide whether to start a new claim.

For unattended provisioning, an operator may explicitly provide a bounded enrollment token. Treat it as a secret: do not request it in chat, echo it, log it, put it in an argument, or recover it from unrelated files. Feed an explicitly provisioned value to `aingle init --enrollment-token-stdin` through stdin. This delegated path does not authorize the agent to create more tokens or acquire an operator session.

`aingle operator login` is for a human-controlled operator CLI. An agent must not initiate it merely to activate itself.

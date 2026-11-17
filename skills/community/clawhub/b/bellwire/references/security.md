# Security

- Store `BELLWIRE_AGENT_TOKEN`, `BELLWIRE_WAKE_TOKEN`, and
  `BELLWIRE_INGEST_TOKEN` only in platform secrets, an ignored local environment
  file, or the user's approved password manager.
- Store each provider webhook signing secret separately from Bellwire tokens. Never reuse one provider's signing secret for another endpoint or environment.
- Never add tokens to source, examples, fixtures, shell history, screenshots, issue text, or logs.
- For `bind`, `create-token`, and `create-wake-token`, require
  `--secret-output <new-file>`. Import the resulting `0600` file into the
  approved secret store without printing it, then remove that exact temporary
  file after successful import.
- Give each project its own mode-specific runtime token. Never reuse a wake or
  Ingest Token across repositories.
- Treat email, phone, name, IP address, customer ID, access token, and free-form user content as sensitive unless the user says otherwise.
- Private is the default. Bellwire receives only an encrypted connection
  envelope and a random opaque wake reference; the App pulls notification,
  Inbox, and Surface content from the user's service with a signed request.
- Keep Private reference mappings in a database-backed outbox for at most
  24 hours. Do not encode business identifiers or timestamps in references.
- Persist Direct request nonces atomically. Do not use an eventually consistent read-then-write cache as the replay defense.
- Notification templates must not reference sensitive fields. The iOS app masks them in event detail by default.
- Use management tokens only for configuration and tests. Private runtime code
  must use a wake-only token; Hosted runtime code must use an Ingest Token.
- Verify webhook signatures against the unmodified request body before parsing JSON. Use the provider's official verifier when one already exists.
- Rotate a token after accidental disclosure; update the runtime secret before revoking the old token to avoid event loss.
- Do not let a notification failure roll back a successful payment, deployment, or completed task unless the repository already defines that behavior.

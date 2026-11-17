# Production verification

Use this gate before describing Bellwire as actually connected to a product.

## Required evidence

1. **Source trigger:** identify the exact post-commit function, provider webhook,
   queue consumer, or scheduled job that calls Bellwire.
2. **Runtime authentication:** confirm the deployed environment has the correct
   project ID and project-scoped wake token (Private) or Ingest Token (Hosted).
   Do not infer this from a local shell or management Agent Token.
3. **Durability:** use synchronous acceptance, a durable queue/outbox, or a
   replayable committed record with cursor-based reconciliation. `waitUntil`
   alone is not durable.
4. **Focused tests:** cover the successful mapping, stable idempotency key,
   duplicate/retry behavior, and the relevant unaffected business path.
5. **Persistent source:** confirm the adapter is in the repository or other
   deployment source of truth. Inspect uncommitted changes and report them if
   commit or push was not authorized.
6. **Active deployment:** verify the active runtime version contains the adapter
   and secret bindings. A successful older test does not prove the current
   deployment still contains it.
7. **Real source operation:** trigger or observe one genuine payment, job,
   deployment, or other business operation. Do not substitute `send-test` or a
   manual Surface upsert.
8. **Mode-specific readback:** for Private, verify the outbox reference, wake
   acceptance, Direct v2 signed fetch, local Inbox/Surface result, and absence of
   content in Bellwire. After re-pairing or key rotation, verify the source service
   trusts the exact new `deviceKeyId` and signing public key before treating manifest
   ACK as success; ACK proves decryption and persistence, not source-side signature
   acceptance. For Hosted, verify the expected Event data, live Surface values,
   idempotency behavior, and Delivery status.
9. **Device presentation:** report `accepted_by_apns` as provider acceptance.
   Claim that the phone displayed the notification only after user confirmation
   or direct device evidence.
10. **Privacy invariant:** inspect logs and Bellwire-controlled storage for a
    Private run. No title, body, Event data, Logo URL, project name, service
    hostname, token, or raw idempotency key may be present.

## Completion language

- Stop at **Configured** after project, schema, token, manual Surface, or test
  Event setup.
- Use **Integrated, awaiting production verification** after source code and
  deployment exist but before a real source operation completes the path.
- Use **Production verified** only after all applicable evidence above is
  collected.

When any gate is missing, name the missing evidence and continue with safe,
in-scope verification. Do not hide the gap behind a successful test Event.

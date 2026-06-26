# DNS and Registrar Security Controls

Apply these controls after registration, transfer, or registrar account changes.

## Baseline Controls

- Enable account-level 2FA on each registrar.
- Enable registrar lock for all production domains.
- Enable renewal alerts to multiple trusted recipients.
- Restrict API credentials to least privilege and rotate on schedule.

## DNS Change Safety

1. Lower TTL before planned migrations.
2. Snapshot full DNS zone before writes.
3. Apply change to one record set at a time for critical domains.
4. Validate with multiple resolvers after each change.
5. Raise TTL when migration stabilizes.

## DNSSEC Controls

- Enable DNSSEC only when authoritative DNS provider supports correct DS workflow.
- Validate DS publication and resolver behavior after enabling.
- During registrar transfer, confirm DNSSEC state is preserved or deliberately reconfigured.

## Access and Audit Controls

- Keep provider-specific audit trail in `changes.md`.
- Separate read-only and write credentials where possible.
- Remove unused API tokens and stale dashboard users.
- Review privileged account access quarterly.

## Incident Triggers

Escalate immediately when any condition appears:
- unexpected nameserver changes
- failed WHOIS ownership checks
- unexplained registrar lock disable events
- unauthorized API token use patterns

## Recovery Priority

1. Stabilize ownership and lock state.
2. Restore known-good nameserver and DNS state.
3. Confirm service health and certificate validity.
4. Rotate credentials and document incident timeline.

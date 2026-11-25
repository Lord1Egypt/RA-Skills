# Email readiness rules

`check_email_readiness.py` returns JSON with a boolean `ready` and stable reason codes.

A contact is ready only when all of these are true:

1. The email normalizes successfully.
2. A contact exists for that normalized email.
3. The contact has a non-empty `source`.
4. The contact is not marked `do_not_contact`.
5. No matching row exists in `email_suppressions`.

Reason codes are `invalid_email`, `contact_not_found`, `missing_source`, `contact_do_not_contact`, and `email_suppressed`.

An external sender must check readiness immediately before it queues or sends email and must fail closed if the database or check command is unavailable. Compliance, consent, sender reputation, and jurisdiction-specific requirements remain the operator's responsibility.

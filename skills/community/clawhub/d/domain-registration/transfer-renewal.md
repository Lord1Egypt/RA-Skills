# Transfer and Renewal Operations

Use this file for cross-registrar transfer planning and renewal control.

## Transfer Prerequisites

- Domain is older than provider transfer lock windows.
- Current registrar lock is disabled when transfer begins.
- Auth/EPP code is requested and validated.
- Contact email for approval links is accessible.
- DNS fallback plan exists if nameservers are changed during transfer.

## Safe Transfer Sequence

1. Snapshot current WHOIS, lock status, nameservers, and DNS records.
2. Start transfer at destination provider with exact auth code.
3. Confirm payment and transfer request status.
4. Monitor approval emails and registry status transitions.
5. Validate final ownership and restore intended lock state.

## Renewal Strategy

- Track renewal windows at least 60 and 30 days before expiration.
- Separate critical domains from low-priority domains for approval routing.
- Confirm premium renewal pricing every cycle for non-standard TLDs.
- Enable auto-renew only when funding source and ownership are verified.

## Emergency Recovery Cases

- Missed renewal in grace period: renew immediately and re-verify DNS.
- Redemption period entry: escalate billing approval due to recovery fee.
- Transfer stuck in pending status: verify lock state, auth code validity, and email approvals.
- Unexpected nameserver reset after transfer: reapply intended nameservers and validate propagation.

## Validation Commands

```bash
whois example.com

dig NS example.com +short

dig A example.com @1.1.1.1 +short

dig A example.com @8.8.8.8 +short
```

Use results to confirm ownership state, delegation, and resolver visibility.

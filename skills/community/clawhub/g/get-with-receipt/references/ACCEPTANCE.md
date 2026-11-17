# Acceptance checklist (v1.0.7)

Before using Receipt for a paid task, confirm:

1. With no Receipt MCP connection, the skill is eligible, model-visible, and discoverable for
   Receipt-related intent.
2. The bootstrap configures the canonical connection when it is absent.
3. Setup starts exactly one bare `openclaw mcp login receipt`.
4. A complete authorization URL is displayed before callback-helper instructions.
5. The same attempt is completed with `--code`.
6. The connection is `https://receiptprotocol.com/mcp`, `streamable-http`, OAuth.
7. Status reports OAuth tokens and client saved; doctor/probe report no diagnostics.
8. Tool listing contains exactly the eight universal Receipt tools and no seller tools.
9. Onboarding calls free `receipt_get_account` and `receipt_discover`, then creates one eligible
   web-search quote no greater than $0.10.
10. The owner explicitly chooses the separately bounded one-purchase launch-credit option during
    setup, or declines it.
11. The user sees seller, capability/offer, price, assurance, reliability, and data recipients
    before the activation purchase.
12. When authorized, exactly one purchase uses Receipt activation credit, not the owner wallet.
13. If opted out or credit is unavailable, setup succeeds with the quote and no purchase.
14. The successful result includes the result, seller, final charge, assurance, validation status,
    transaction ID, and public, signed, and verification Receipt URLs.
15. Replaying the same quote and idempotency key returns the same transaction, result, and Receipt
    without another provider request, hold, settlement, or charge.
16. A purchase attempted after pause is blocked; after OAuth revocation it is also blocked.
17. Typed chat approval is never treated as Receipt authority.
18. `approval_required` exposes only a Receipt-hosted URL; the agent displays it and waits or
    retries the exact purchase without opening or substituting the URL.
19. The owner can choose a spending allowance, one-time approval, or denial on
    `receiptprotocol.com`.

The repository's executable harness is in `packages/openclaw-receipt-acceptance`.

---
name: fleece-gmail-spend
description: Analyze purchase receipts, order confirmations, travel bookings, subscriptions, and refund emails in a connected Gmail account to estimate spending habits, then compare those habits with cards saved in the Fleece wallet. Use for Gmail-based consumption analysis, spend-category summaries, card-position reviews, missed-rewards estimates, wallet coverage gaps, best-card-by-category guidance, and proposed Fleece spending-profile updates.
---

# Fleece Gmail Spend

Combine read-only Gmail evidence with Fleece wallet data to show how well the user's current cards fit actual spending. Treat email-derived totals as estimates, not a bank-statement substitute.

## Workflow

1. Establish the analysis window. Use the user's dates; otherwise analyze the most recent 90 days and state that scope.
2. Read the current Fleece position before recommending changes:
   ```bash
   fleece cards list --json
   fleece profile show --json
   ```
3. Search Gmail for transaction evidence. Prefer Gmail-native search, then batch-read shortlisted messages. Start with queries such as:
   ```text
   newer_than:90d (subject:(receipt OR order OR purchase OR invoice) OR from:(uber.com doordash.com instacart.com amazon.com))
   newer_than:90d (subject:(booking OR itinerary OR reservation) OR from:(airbnb.com expedia.com))
   newer_than:90d subject:(refund OR refunded OR cancellation)
   ```
   Adapt merchant and issuer terms to the mailbox. Search broad categories separately when one query would truncate coverage.
4. Extract only the transaction date, merchant, amount, currency, likely category, order status, and source message ID. Do not expose full message bodies or unrelated personal data.
5. Normalize and deduplicate:
   - Count the final charged total once, not order, shipping, and delivery updates separately.
   - Subtract confirmed refunds and exclude canceled orders.
   - Separate taxes, tips, and fees only when clearly itemized; otherwise retain the final total.
   - Keep non-USD transactions separate unless a reliable conversion amount appears in the email.
   - Exclude marketing offers, reward summaries, balance notices, and statements that duplicate itemized receipts.
6. Classify spending into Fleece profile categories: dining, groceries, travel, gas, and other. Mark uncertain classifications and avoid inventing MCCs. Use `fleece mcc <code> --wallet --json` only when an MCC is explicitly present.
7. Calculate monthly estimates using only covered days. Report total captured spend, monthly average, category share, recurring merchants or subscriptions, and evidence coverage.
8. Compare the observed mix with current cards:
   ```bash
   fleece wallet --json
   ```
   If `BRAVE_API_KEY` is unavailable, use saved card reward metadata and label the comparison partial. Do not guess current benefits or annual fees.
9. Identify the best current card for each observed category, weak or overlapping coverage, explicit card misuse, and conservative missed-rewards ranges. Recommend a new card only when the gain exceeds annual fees and switching complexity.
10. Propose Fleece profile updates, but do not write them without explicit confirmation. After confirmation, use one command per field:
    ```bash
    fleece profile set dining_monthly <amount>
    fleece profile set groceries_monthly <amount>
    fleece profile set travel_monthly <amount>
    fleece profile set gas_monthly <amount>
    fleece profile set other_monthly <amount>
    ```

## Safety and Evidence Rules

- Keep Gmail access read-only. Never send, label, archive, delete, or otherwise modify mail.
- Never request or reveal full card numbers, security codes, passwords, or authentication codes. Use last four digits only to map an explicit purchase to a saved card.
- Do not persist a transaction ledger unless the user explicitly asks. Prefer aggregates.
- Distinguish evidence from inference. Gmail receipts undercount cash purchases, merchants that do not email, shared-account purchases, and deleted mail.
- Do not claim a purchase used a particular card unless the receipt identifies it.
- Do not recommend applying for, closing, or product-changing a card solely from a short or low-coverage sample.

## Output

Lead with the wallet-fit conclusion, then provide:

1. Scope and coverage: dates, messages reviewed, usable transactions, exclusions, and currencies.
2. Spending profile: category totals, monthly estimates, share, and confidence.
3. Current-card fit: best card by category, overlaps, gaps, and observed misuse.
4. Estimated upside: conservative missed-rewards range and assumptions.
5. Actions: card-use changes first, profile updates requiring confirmation, then at most two new-card candidates when justified.

Use tables when comparing three or more categories. Include aggregate provenance such as message counts and representative merchants, not private message content.

## Failure Modes

- If Gmail is unavailable, ask the user to connect the correct Gmail account or provide an exported receipt list.
- If the Fleece wallet is empty, ask the user to add cards with `fleece cards add`; still provide the spending summary.
- If search coverage is sparse, broaden the date window or merchant queries and report low confidence.
- If live card research is unavailable, stop at a partial wallet comparison and offer the exact command to rerun after `BRAVE_API_KEY` is configured.

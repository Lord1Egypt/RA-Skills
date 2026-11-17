---
name: galleon-defi-tokenized-assets
description: "Use when researching tokenized Treasury or securities eligibility, custody, subscriptions, transfers and redemption settlement for Ondo and OpenEden."
license: MIT
metadata:
  version: "0.1.3"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Tokenized assets

Start with the legal product and issuer claim, then the token. A public blockchain interface or transferable balance does not establish eligibility to subscribe, hold, transfer or redeem. This skill is a research and settlement procedure, not legal advice, an issuer onboarding service or a signer.

Read [providers](references/providers.md) for the exact product. Use [workflows](references/workflows.md) for eligibility/settlement records and evaluation cases.

## Start with the requested task

Read [task examples and user configuration](references/task-examples.md) for a completed example and recovery path. Apply only the workflow stages needed by the current request. Reuse supplied preferences and compatible tools; ask only for missing terms that affect this task. Public explanation or comparison does not require transaction fields. Keep any existing authorization within its exact scope.

## Workflow

1. Identify issuer, product/share class, jurisdictional offering, chain and token address, account/entity, requested action and settlement currency. Keep Ondo Stocks, USDY, OUSG and OpenEden TBILL separate; one product's access rules do not transfer to another.
2. Verify current issuer documentation for investor eligibility, KYC/KYB/KYT, wallet whitelisting, transfer restrictions, permitted recipients, fees, minimums, redemption windows and custody/legal claim. Treat eligibility as unknown until the issuer confirms it; do not infer nationality or status from a wallet or location.
3. Research NAV and its timestamp, quoted market price, backing/custodian reporting, fees and available liquidity. Separate token settlement, issuer redemption and bank/business-day settlement. Do not equate Treasury backing, ratings, or attestations with guaranteed principal or immediate cash availability.
4. If the user requests and qualifies for a transaction, use the issuer's documented interface and credentials kept outside context. Distinguish indicative quotes from binding attestations/orders; even an offchain request may consume a limit or create an obligation. Review price, notional, fee, chain, approved address, expiry and issuer terms before requesting a binding operation.
5. Prepare the concrete unsigned onchain sequence when supported and simulate it. Preserve authorization scope; onboarding documents, identity submission, binding quotes, token approvals, signatures, purchases and transfers are distinct actions. Obtain missing authorization at the applicable step without treating research as consent. Use the chosen signer; do not collect seed phrases or retain identity documents in artifacts.
6. Reconcile quote/attestation ID, approval, signature, transaction submission, receipt, token/NAV indexing, redemption request and actual settlement independently. A burned token or accepted request does not prove bank/USDC proceeds arrived. On ambiguity, query the known order/request/hash before retrying a binding action.

## Deliverable

Return exact product and source dates, confirmed versus unknown eligibility, legal/custody structure, access/tooling status, price/NAV and cost basis, settlement stages and outstanding evidence. If issuer access is unavailable, provide the research and concrete prerequisites; do not invent an API, bypass geographic restrictions or connect a third-party MCP as though it were official.

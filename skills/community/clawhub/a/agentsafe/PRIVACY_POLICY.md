# agentSAFE — Privacy Policy

Version: 2.0 · Effective date: **October 21, 2026** · Operator: **workfern**
(independent developer, Hong Kong)

This policy is drafted to be consistent with the Hong Kong Personal Data
(Privacy) Ordinance ("PDPO", Cap. 486) and describes what the agentSAFE
service ("Service") actually collects. It is published at `/privacy` by the
Service itself. `TODO — OWNER INPUT: final legal review by a Hong Kong
practitioner before treating this policy as PDPO-certified.`

## What we collect

The Service does not collect real names, e-mail addresses through the
product, telephone numbers, identity documents, or payment credentials. The
Service collects only:

1. **On-chain wallet addresses** — the payer's wallet address and the
   merchant receiving address, required by the x402 payment protocol for
   verification and settlement.
2. **Transaction hashes** — settlement transaction identifiers, logged for
   payment reconciliation and support.
3. **Target contract addresses** — the contract you ask the Service to
   audit, together with its public verified source code (public on-chain
   data), logged and stored for service delivery.
4. **IP access logs (30 days)** — every HTTP request to the public endpoint
   is logged with the visitor's IP address and UTC timestamp. These logs
   are kept for a **maximum of 30 days** and are used strictly for
   anti-DDoS protection, rate limiting, and abuse prevention. Older entries
   are purged automatically.

An unguessable task identifier (`task_id`) is issued per audit and stored
with the contract address for the report-retention period (currently 2
days).

## What we do NOT collect

- No cookies, no analytics, no tracking scripts (the MCP protocol carries no
  cookies).
- No real names or identity data.
- No private keys, API secrets, or payment credentials are logged or stored;
  secrets are read from environment variables and never written to logs or
  source control.

## Purpose and use (PDPO Data Protection Principle 1 & 3)

Each data category above is collected for a stated purpose only:
settlement, service delivery, dispute/refund handling, and abuse
prevention. Data is not sold, rented, or used for marketing.

## Third parties that necessarily receive data

| Third party | Data received | Purpose |
| --- | --- | --- |
| PayAI facilitator (`facilitator.payai.network`) | Payer wallet address, signed x402 payment payload, payment terms, settlement transaction data | Payment verification and settlement (required by the x402 protocol) |
| Block explorer (Etherscan) | Target contract address (+ operator API key) | Verified-source retrieval |
| RPC provider (Infura) | Target contract addresses | On-chain reads |
| Code hosting (GitHub / GitHub Actions) | Target contract address, `task_id`, audit artifacts | Audit execution and report storage |
| LLM providers configured by the operator | Public verified contract source code | AI-assisted analysis |
| Hosting/transport layer | IP addresses and request metadata (their own access logs) | Serving the public endpoint |

These third parties process the data under their own privacy policies,
which this Service does not control. `TODO — OWNER INPUT / REVIEW: check the
current PayAI, Etherscan, GitHub, Infura, and LLM provider privacy terms
before publication.`

## Wallet addresses are pseudonymous

Public wallet addresses are pseudonymous, not anonymous: they can be linked
to individuals through on-chain analytics or off-chain associations.
On-chain payment data (addresses, amounts, transaction hashes) is public by
nature and permanently visible on the blockchain.

## Retention

| Data | Retention |
| --- | --- |
| IP access logs | Maximum 30 days, then automatically purged |
| Task records (`task_id` → contract address) | Report-retention period (currently 2 days) |
| Audit reports | Same limited period (retrieve promptly) |
| Application log lines (addresses, tx hashes, errors) | Follows the operator's log infrastructure; `TODO — OWNER INPUT: confirm production log retention` |

No deletion guarantee is made for data that third parties (blockchain,
explorer, code host, facilitator, LLM providers) already received.

## Access and correction

PDPO Data Protection Principle 6 gives you the right to ask whether this
Service holds personal data about you and to request correction. On-chain
addresses and transaction hashes cannot be changed once on-chain. Contact
`lunanoach@gmail.com` for access requests regarding our application-level
records.

## Contact

workfern — `lunanoach@gmail.com`

Enterprise/custom-pricing inquiries: <https://tally.so/r/laby7B>

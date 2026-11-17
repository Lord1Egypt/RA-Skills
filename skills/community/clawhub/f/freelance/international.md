# Cross-Border Work — Foreign Clients, Currency, Withholding

Scope: invoicing, taxing and getting paid across borders, plus working while travelling. Domestic tax mechanics are `taxes.md`; the rails themselves are in `getting-paid.md`.

**Before advising**, read `tax_jurisdiction`, `currency` and `business_entity` in `config.yaml`, plus `## Engagements` for which clients are foreign. **Name the assumed jurisdiction pair before answering** — cross-border answers are meaningless without both ends.

**Contents:** [The Four Questions](#the-four-questions) · [Where the Service Is Taxed](#where-the-service-is-taxed) · [Withholding Tax](#withholding-tax) · [EU VAT for Cross-Border Services](#eu-vat-for-cross-border-services) · [Invoicing a Foreign Client](#invoicing-a-foreign-client) · [Currency](#currency) · [Getting the Money](#getting-the-money) · [Contracting Across Jurisdictions](#contracting-across-jurisdictions) · [Working While Travelling](#working-while-travelling) · [Time Zones](#time-zones)

## The Four Questions

Every cross-border engagement resolves into four, in this order. Answering them out of order produces the classic surprise: an invoice that arrives 30% short.

1. **Where is the service taxed for consumption purposes?** Usually where the customer is, for B2B services (→ Where the Service Is Taxed).
2. **Will the client withhold tax at source?** Depends on the country pair, the treaty, and where the work is physically performed (→ Withholding Tax).
3. **Which currency, and who carries the conversion?** (→ Currency).
4. **Whose law governs, and can a judgment be enforced?** (→ Contracting Across Jurisdictions).

## Where the Service Is Taxed

- **B2B services generally follow the customer**: the customer's country has taxing rights for VAT/GST, and the supplier does not charge its own VAT. In the EU this is the reverse charge (→ EU VAT).
- **B2C is different**: often taxed where the supplier is, with special rules for digital services taxed where the consumer is (the EU's OSS scheme exists precisely for this).
- **Verify the customer is a business**: a validated VAT/GST number, or evidence of business status. Without it, the transaction may be treated as B2C, and the tax is then yours to have collected.
- **Non-EU pairs**: many countries apply a similar destination principle with their own registration thresholds for foreign suppliers. Check before assuming zero obligation in the client's country.

## Withholding Tax

The mechanism that makes a payment arrive short, and the one most freelancers meet by surprise.

- **Some countries require the payer to withhold** a percentage of a cross-border service payment and remit it to their own tax authority. Rates commonly sit in the 5-30% band depending on country and service type.
- **A double-taxation treaty usually reduces or eliminates it**, but only if the paperwork is filed *before* payment: a certificate of tax residence from your country, plus the client's local form.
- **US clients paying a non-US freelancer**: the source rule is where the *services are performed*. Services performed outside the US are generally foreign-source income and not subject to US withholding — a **Form W-8BEN** (individuals) or **W-8BEN-E** (entities) given to the client documents foreign status and prevents default withholding and backup-withholding treatment. US persons give a **Form W-9** instead, and receive a 1099-NEC above the reporting threshold.
- **Withheld tax is usually creditable** against your home tax bill, but only with the withholding certificate the client must supply. Ask for it at the time; obtaining it a year later is difficult.
- **Put the treatment in the contract**: whether the fee is gross or net of withholding, and who bears it. A gross-up clause is the difference between a 20% haircut and none.

## EU VAT for Cross-Border Services

| Situation | Treatment | Invoice must show |
|---|---|---|
| EU B2B, different member states | Reverse charge — no VAT charged; the customer accounts for it | Both VAT numbers, and a reverse-charge note |
| EU B2C, digital/electronic services | VAT of the consumer's country, declarable through the OSS scheme | The rate applied and the country |
| Supplier to a non-EU business | Outside the scope of EU VAT | A note that the supply is outside scope |
| Non-EU supplier to an EU business | The EU customer self-accounts | Nothing special from the supplier, but keep the evidence of business status |
| Same member state | Domestic VAT as normal | Standard requirements |

- **Validate the customer's VAT number** through the official EU system and keep the validation evidence with the invoice. An invalid number turns a reverse-charge supply into a domestic one — and the VAT you failed to charge is still owed.
- **Reverse-charged sales still get reported** (recapitulative statements in most member states). Missing filings attract penalties even though no VAT moved.
- Register for the schemes rather than improvising, and confirm current thresholds — they change (`taxes.md`).

## Invoicing a Foreign Client

Everything a domestic invoice needs, plus:

- Both parties' full legal names, addresses and tax numbers.
- The correct tax note: reverse charge, outside scope, or the rate charged.
- **Currency stated explicitly**, and the exchange rate and date if the tax authority requires reporting in the home currency.
- **Who pays bank charges** — the `OUR`/`SHA` election on wires materially changes what arrives.
- **The client's PO or reference**, because a foreign invoice missing the reference is the one that sits in a queue for a month.
- A payment deadline as a date, and the statutory or contractual late-interest note (`getting-paid.md`).

## Currency

- **Bill in your own currency by default.** It moves the FX risk to the client, who is usually larger and better hedged. Concede only for a rate premium or a strategic client.
- **When billing in a foreign currency**, quote with a validity window (14-30 days) so a moving rate does not silently reprice the engagement — a 5% move on a three-month project is ordinary.
- **Price the spread in.** Bank card and wallet conversions commonly cost 2-4% against the interbank rate; specialist transfer services are typically well under 1%. On a 20,000 invoice that difference is a day of billings.
- **Long engagements** in a foreign currency: invoice monthly rather than at the end, which is a crude but effective hedge, or agree a rate-review clause at a stated threshold of movement.
- **Record every stored amount with its currency** (`62 USD`, never `$62`) — the shared boxes mix currencies and someone will sum the column (`memory-template.md`).

## Getting the Money

| Route | Cost | Notes |
|---|---|---|
| SEPA (euro area) | Near zero | Default inside the euro area |
| SWIFT wire | Fixed fee each side plus intermediary deductions plus bank FX spread | Specify who pays charges; ask for the sender's reference to trace it |
| FX-specialist transfer service | Sub-1% typically, near-interbank rate | Usually the best value; a local receiving account in the client's currency removes their friction entirely |
| Card or payment link | ~2-4% plus cross-border surcharge | Fast; carries chargeback exposure (`disputes.md`) |
| Wallets (PayPal and similar) | Percentage fee plus a conversion spread stacked on top | Expensive; use when the client insists |
| Marketplace escrow | The platform's take rate | Buys dispute protection with it (`platforms.md`) |

Give the client a **local receiving account** in their currency where the service offers one: a client who can pay domestically pays faster, and the "international payment" friction disappears from their approval process.

## Contracting Across Jurisdictions

- **Governing law and venue decide whether a debt is collectable.** A clause naming a court on the other side of the world converts a recoverable invoice into a write-off (`disputes.md`).
- **Push for your own jurisdiction**; settle for a neutral one with an arbitration or mediation step. Note that arbitration is enforceable across most of the world under the New York Convention, while a foreign court judgment often is not — which makes an arbitration clause the practical compromise.
- **Payment protection instead of jurisdiction**: when the counterparty will not move, take deposits, milestones and escrow. Structure beats litigation you cannot afford.
- **Sanctions and export controls** are real and personal: check the client's country and entity before contracting, particularly for technology work. Ignorance is not a defence, and payment providers block first and ask later.
- **Language**: name which language version governs when the contract exists in two.

## Working While Travelling

- **Tax residency is not a preference.** Rules commonly turn on days present (183 days is a frequent but not universal marker), plus centre-of-vital-interests tests. Two countries can both claim you; treaties have tie-breaker rules.
- **Working on a tourist visa is not automatically allowed** even when the client and income are foreign. Several countries now offer explicit digital-nomad or remote-work visas — use one rather than assuming.
- **Social contributions follow their own rules**, separate from income tax. Inside the EU, an A1 certificate keeps you in your home system while working temporarily in another member state; other treaty networks have equivalents.
- **Physical presence can create obligations for the client too**, especially over long stays (`classification.md`, permanent establishment).
- Keep a **day log** when the year is genuinely mobile, in its own box: `~/Clawic/data/freelance/days/<year>.md`, one row per stay — entry date, exit date, country, purpose, running total per country — with its `## Boxes` line written the turn the file is created. Reconstructing 183 days from photos during a tax review is a bad afternoon.

## Time Zones

- **State working hours in the contract**, in your timezone with the client's equivalent, plus the response-time expectation. Silence gets read as "available whenever we are awake".
- **Overlap is a priced feature**: 2-3 hours of guaranteed overlap is a real service and can carry a premium; full alignment with a distant timezone is a lifestyle change and should be priced like one (`rates.md`).
- **Write asynchronously by default** — a decision log and a weekly written update prevent the meeting-at-midnight failure mode.
- Note public holidays on both sides in `## Due`; a client who does not know your national holiday will schedule a launch on it.

**After any cross-border engagement is agreed**, write into `## Engagements` in `~/Clawic/data/freelance/memory.md`: currency, who bears bank charges, withholding treatment and any gross-up, governing law, and the working-hours agreement. **Withholding certificates, VAT validation evidence and treaty forms** are documents — keep only their location and status in `## Pain Points` or the engagement row, never the identifiers themselves. **Any filing (recapitulative statement, OSS return) or residency-day threshold** becomes a row in `## Due`. **Every stay abroad in a mobile year** is a row in `days/<year>.md`, written when the stay ends rather than at the end of the year.

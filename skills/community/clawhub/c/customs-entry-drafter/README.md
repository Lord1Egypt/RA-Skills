# customs-entry-drafter

Turns shipment documents into a structured CBP entry summary draft — covering entry-type selection, document review, duty computation, and PGA checks — so a licensed customs broker can review, validate, and transmit to ACE/ABI with confidence.

## Who It's For

- Licensed U.S. customs brokers
- Import compliance managers and trade-compliance teams
- In-house trade counsel at importers of record
- Freight forwarders preparing entry packages for broker review

## What It Produces

A DRAFT CBP entry summary including:

- Entry type selection with rationale
- Per-line HTS review, entered value, and duty/fee computation (labeled DRAFT — ESTIMATED)
- Section 301, Section 232, and AD/CVD deposit flags
- Partner Government Agency (PGA) admissibility screen
- Document checklist
- Open-questions list
- Licensed Customs Broker Review Block

## What It Does NOT Do

- Transmit entries to ACE/ABI
- Determine HTS classification from scratch (use `hs-tariff-classification` for that)
- Confirm final liquidated duties or binding CBP rulings
- Provide legal or regulatory advice

## Scope

U.S. CBP import entries only. Does not cover export EEI/AES filings, foreign customs entries, or USMCA certificate of origin drafting.

## Prerequisites

None. For HTS classification assistance, use the `hs-tariff-classification` skill first.

## Feedback & Contributions

Have suggestions or found a gap? Open an issue at https://github.com/archlab-space/Open-Skill-Hub/issues

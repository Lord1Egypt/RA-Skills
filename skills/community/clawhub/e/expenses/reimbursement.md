# Reimbursement — Getting the Money Back

Claims live in `~/Clawic/data/expenses/claims/<year>.md`. **Before assembling or chasing anything**, read that file and any employer claim-policy summary the `## Boxes` index lists in `artifacts/` — the policy decides more outcomes than the tax rules do, and it is the thing nobody re-reads.

**Contents:** [The Lifecycle](#the-lifecycle) · [Deadlines Are the Whole Game](#deadlines-are-the-whole-game) · [What a Claim Packet Contains](#what-a-claim-packet-contains) · [Per Diem vs Actuals](#per-diem-vs-actuals) · [Mileage](#mileage) · [Mixed Business and Personal Trips](#mixed-business-and-personal-trips) · [Corporate Card Is Not a Claim](#corporate-card-is-not-a-claim) · [Rejections](#rejections) · [Chasing](#chasing) · [Tax Treatment](#tax-treatment)

## The Lifecycle

`draft` → `submitted` → `approved` → `reimbursed`, with `rejected` as a branch that keeps its reason.

Reimbursable spend stays in the ledger at full amount with a `#claim` tag from the moment it is paid (`capture.md`); the claim row in `claims/<year>.md` tracks the money owed back. Two records, because they answer different questions: the ledger says what the month cost, the claim file says what is outstanding.

The number worth surfacing unprompted is the **total in `submitted` or `approved` but not `reimbursed`** — that is an interest-free loan to an employer, and it is invisible unless something tracks it.

## Deadlines Are the Whole Game

Employer submission windows commonly run 30-90 days from the expense date; some are calendar-month. A claim submitted after the window is money donated, and no appeal process exists for lateness in most policies.

- Confirm the window once, write it into an `artifacts/` policy summary, and set a `## Due` row on `close_day` to submit whatever is pending.
- **Submit partial packets.** A packet of four receipts submitted on time beats a complete packet submitted late, and nothing prevents a second claim for the same period.
- Anything approaching the window gets stated in one line at the start of a session, as a fact, not a question.

## What a Claim Packet Contains

Per line: date · amount with the currency paid · vendor · **business purpose** · project or cost code · receipt file · attendees, for any meal or entertainment.

Attendees is the field most often missing and most often demanded: for a client meal, the names and their organisations. It is also the field that is unrecoverable three weeks later, which is why it is written at payment (SKILL.md Rule 8).

Currency: claim in the currency paid and let the employer convert unless the policy says otherwise. Converting yourself means absorbing the difference between your rate and theirs, and the difference is invisible until it is a pattern (`currency.md`).

## Per Diem vs Actuals

A per diem pays a fixed daily amount regardless of what was spent, which is why it **removes the receipt requirement** for the items it covers. Logging those receipts is wasted work.

- Travel days are commonly paid at a **reduced rate** — the US federal convention is 75% of the meals-and-incidentals rate on the first and last day of travel. Confirm the employer's own schedule; private policies vary and many pay full days.
- Per diem covers meals and incidentals; **lodging is usually separate** and usually needs an actual receipt.
- If actual spend is below the per diem, the difference is the traveller's. If above, it is not claimable — that is the trade being made.
- A per diem still gets logged: one entry per day at the per-diem amount, tagged `#perdiem`, so the trip envelope and the month are complete. The receipts underneath it are not needed.
- Mixing per diem and actuals for the same day, or the same meal, is the fastest way to have a whole claim rejected.

## Mileage

`distance × mileage_rate`. While `mileage_rate` is unset, do not quote a number — say that the jurisdiction's official rate for the relevant year has to be checked, because these rates are revised annually and a stale one is a wrong claim in both directions.

- **The rate already includes fuel, wear, insurance and depreciation.** Claiming fuel receipts as well is double-claiming and is a standard audit finding.
- Log the **route and the purpose**, not just a total. `Office → client site → office, 62 km, Acme quarterly review` survives a review; `62 km` does not.
- Odometer readings at the start and end of the year make the business-use percentage defensible for anyone also claiming vehicle costs (`business.md`).
- Commuting between home and a regular workplace is not business mileage in most jurisdictions; travel between work sites is. Verify the local test before advising.

## Mixed Business and Personal Trips

Two separate questions, and conflating them is why these claims get cut:

1. **The travel itself** (flights, the main journey) is generally claimable in full only when the **primary purpose** of the trip is business, judged mostly by the split of days. Where the primary purpose is personal, the travel is usually not claimable at all — not apportioned.
2. **On-the-ground costs** are claimable for the business days: `total × business days ÷ total days` for anything that runs across the whole trip, and directly attributed for anything day-specific.

Store the day count as the apportionment basis in the entry, not just the resulting percentage. The basis is what gets asked for; the percentage is what gets doubted. Verify the primary-purpose test against the user's jurisdiction before applying it — the concept is near-universal, the mechanics are not.

Companions who are not on business are never claimable, and their share comes out before any apportionment.

## Corporate Card Is Not a Claim

A charge on a company card is **already the company's money**. It is a reconciliation task — code it, attach the receipt, submit it in the card cycle — not a receivable.

Logging it as a claim creates a phantom amount owed that will never arrive and will sit in the aged list forever. In the ledger, corporate-card spend is tagged `#corpcard` and excluded from personal totals entirely, because it never touched the user's money.

The mirror case: a **personal card used for a company expense** is a claim against the company (in a one-person company, an owner's draw or director's loan account), never a direct company expense (`business.md`).

## Rejections

Keep the row and the reason. The recurring reasons, in rough order of frequency:

| Reason | Prevention |
|---|---|
| Over a policy limit (hotel nightly cap, meal cap) | Read the caps once into the policy artifact; flag at booking, not at claiming |
| Missing business purpose | Written at payment, always (SKILL.md Rule 8) |
| Alcohol, or the alcohol portion of a bill | Ask for a split bill at the table where the policy excludes it |
| Personal portion of a mixed meal or a mixed trip | Apportion before submitting, not after being asked |
| Late submission | The `## Due` row |
| Illegible or partial receipt | Photograph on the day, whole document (`receipts.md`) |
| Wrong cost code | Codes go in the ledger row's purpose field at payment |

A deleted rejection loses its reason, and the same line gets submitted and rejected again next quarter. Keep it, with the reason, in `claims/<year>.md`.

## Chasing

Aged view: any claim `submitted` or `approved` past the employer's stated payment window. Chase with the claim reference, the date submitted, the amount and currency, and nothing else. If a payment window has never been stated, the practical default is the next payroll cycle after approval.

When a reimbursement lands, the row moves to `reimbursed` with the date **and** the received amount — a partial payment is a rejection of the missing lines that nobody announced, and it only shows up if the amount is compared.

## Tax Treatment

- A reimbursement of an actual, documented business expense is **not income** to the employee in most jurisdictions.
- A per diem **at or below** the official rate is generally not income; the excess above the official rate usually is, and is usually reported.
- A round-sum monthly allowance with no receipts behind it is commonly treated as pay, taxed accordingly. It is the classic challenged arrangement.
- Verify all three against the user's jurisdiction before stating them as fact, and route anything with real money on it to their accountant (`business.md` Red Flags).

**Write on the way out.** Every claim assembled, submitted, approved, paid, partially paid or rejected updates its row in `claims/<year>.md` in the same turn, with the reason kept on a rejection; the underlying spend keeps its `#claim` tag in the ledger; a confirmed policy — window, caps, per-diem schedule, payment cycle — goes to `artifacts/` as a policy summary with its `## Boxes` line; the submission cadence and any chase date go to `## Due`; a confirmed `mileage_rate` is a declaration and goes to `config.yaml`. Formats in `memory-template.md`.

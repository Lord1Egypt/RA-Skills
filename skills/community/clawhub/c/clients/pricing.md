# Pricing, Rates, and Raising Them

Scope: what to charge, which model to charge it in, and how to change it on someone who is already paying the old number. The document that carries the price is `proposals.md`; collecting it is `getting-paid.md`.

Read `rate_card_file` if set, the rates already recorded in `## Roster`, and `revenue/<year>.md` before quoting anything — the most common pricing error is quoting a number lower than what this same client already pays.

**Contents:** [Effective Rate Is the Only Honest Number](#effective-rate-is-the-only-honest-number) · [Setting a Floor](#setting-a-floor) · [Choosing the Model](#choosing-the-model) · [Retainers That Do Not Rot](#retainers-that-do-not-rot) · [Discounts and Surcharges](#discounts-and-surcharges) · [Raising Rates on an Existing Client](#raising-rates-on-an-existing-client) · [When They Push Back on Price](#when-they-push-back-on-price)

## Effective Rate Is the Only Honest Number

Effective hourly rate = **fee ÷ (delivery hours + admin + calls + revisions + chasing payment)**. Everything a headline day rate hides lives in that denominator.

Worked example: a 6,000 EUR fixed project, 40 hours of delivery, plus 6 hours of calls, 4 hours of admin and invoicing, 8 hours of revisions past what was scoped, 2 hours chasing the invoice. Headline rate 150 EUR/h; effective rate 6,000 ÷ 60 = 100 EUR/h. A third of the price disappeared into unpriced work, and the whole of it is scope, admin and collections — which is why `scope.md` and `getting-paid.md` are pricing documents.

Compute the effective rate on the last three closed engagements from `revenue/<year>.md` and the project change logs before setting the next price. It is usually 25-40% below the headline; if it is not, the scope was unusually tight or the hours were not being recorded.

## Setting a Floor

The floor is a cost calculation, not a market question:

1. **Target annual income**, after business costs.
2. **Add costs**: taxes and social contributions, software, insurance, equipment, pension, accountant, unpaid holiday and sick time.
3. **Divide by billable hours, not working hours.** A solo operator who plans at 100% billable is planning for zero sales, zero admin and zero learning. Planning at 60-70% billable is the conventional assumption for delivery work; a first year is usually worse.
4. **Add a bad-debt allowance** if collections have ever been a problem.

That number is the floor. `config.yaml` holds it under `commercial.rate_floor`, and no option in any proposal goes below it — including the Reduced option, which is why the Reduced option is smaller in scope rather than cheaper per hour.

Above the floor, price is positioning: what the outcome is worth to that buyer, what comparable suppliers charge, and how badly they need it now. Those move the number up. Nothing moves it below the floor except a decision to work at a loss, which should at least be a conscious one.

## Choosing the Model

The default is in `engagement_default`. The switch conditions, expanding the table in SKILL.md:

| From | To | Switch when |
|---|---|---|
| Hourly | Fixed project | You have delivered this shape of work twice and know the hours within ~20% |
| Fixed project | Retainer | The same client generates a new project every quarter, or needs your availability more than your output |
| Retainer | Fixed project | Usage swings more than ~50% month to month, or the retainer has become an unpriced queue |
| Anything | Value-based | The client already has a number for the outcome and states it themselves; you cannot invent it for them |
| Value-based | Fixed | The baseline cannot be measured, or the outcome depends on decisions you do not control |

Break-even between hourly and fixed: fixed wins for you when your estimate is accurate and the scope is controlled, and it wins for the client when it is not — that asymmetry is exactly what the change-order clause corrects.

## Retainers That Do Not Rot

Retainers fail in one of three predictable ways. Design against each:

| Failure | What it looks like | Design that prevents it |
|---|---|---|
| Unlimited pass | "You're on retainer" attached to every request | A cap — hours or a named scope — written in the agreement and reported monthly |
| Ghost month | They use nothing, then question the invoice | Report usage every month, used or not; value is availability, and availability is what the report shows |
| Rollover debt | Unused hours accumulate into an unpayable obligation | One month of rollover maximum, then expiry, stated up front (`commercial.retainer_rollover`) |

Price a retainer above the equivalent project hours, not below. The client is buying priority access and predictability, and you are giving up the ability to sell those hours to anyone else. Discounting a retainer for "guaranteed volume" gives away the premium and keeps the constraint.

Review every retainer at a fixed interval — `## Due` carries the date. A retainer nobody has reviewed in a year is either underpriced or dead.

## Discounts and Surcharges

- **Never discount the rate; discount the scope.** A 20% cut in price for the same work permanently reprices you with that client and with anyone they talk to. A 20% smaller scope at full rate keeps the number intact.
- If a discount is unavoidable, buy something with it: a longer commitment, payment up front, a case study, a named referral. A discount given for nothing teaches that the first number was not real.
- **Rush surcharge** is a real price, not a punishment: work that displaces other work costs more. Typically 20-50% depending on how much it disrupts; whatever the policy is, it goes in `config.yaml` and applies every time, or it will be argued every time.
- **Out-of-hours, weekend and holiday work** is priced or refused, never absorbed silently — absorbing it once makes it the expectation.
- **Multi-currency**: quote in the currency the client pays in, record what was actually received in `revenue/<year>.md` with that currency, and state who bears conversion and transfer fees in the proposal. Cross-border transfer costs quietly eat several percent of small invoices.

## Raising Rates on an Existing Client

The mechanics matter more than the number (SKILL.md Rule 8):

1. **Pick the moment**: renewal, a new project, or a fixed annual review month held in `## Due`. Never mid-delivery — a rise announced while you hold their unfinished work reads as leverage.
2. **Give 30-60 days' notice, in writing**, with the effective date. Enough time for them to budget, not so much that it is forgotten.
3. **State it, do not ask it.** "From 1 October, my day rate is 950 EUR." One sentence of reason — costs, demand, or the scope of what you now do — and no apology, no justification paragraph. Long explanations invite line-by-line rebuttal.
4. **Offer a bridge, not an exception**: the old rate honoured for work already scheduled, or a phased rise over two steps. A bridge preserves the relationship without creating a permanent carve-out.
5. **Expect and accept some loss.** A rate rise that nobody leaves over was too small. Losing the lowest-paying client to a rise usually raises total income within a quarter, because the freed capacity is worth more than the lost fee — check it against `portfolio.md` before assuming it.
6. **Never raise silently** by quietly quoting more on the next project without saying why. It gets noticed, and it reads as opportunism rather than pricing.

Save the wording that worked to `artifacts/script-rate-rise.md`; the second rise is far easier when the first one's exact sentences are on file.

## When They Push Back on Price

| They say | What it usually means | Response |
|---|---|---|
| "That's more than we expected" | The budget conversation did not happen properly in qualification | Show the Reduced option; do not cut the Recommended one |
| "Can you do it for X?" | A test, or a real constraint — you cannot tell yet | "At X, here's what I'd take out." Scope moves, rate does not |
| "We can get it cheaper elsewhere" | Often true, and often not comparable | Agree that they can, then name the specific difference in what is delivered. Never disparage the competitor |
| "It's only a few hours' work" | They are pricing your time, not the outcome | Price the outcome and the risk you absorb, and stop itemising hours in proposals |
| "The budget is fixed at X" | Frequently genuine, especially in larger organisations | Design a real deliverable that fits X, or decline. Do not deliver the big scope for the small number |
| Silence after the number | Normal; the first person to speak usually concedes | Let it sit. Then ask which option fits, not whether the price is acceptable |
| Anything else | Ask what specifically feels wrong, and wait for the answer | The objection they voice second is the real one |

**Write before you move on:** a changed rate, model, or payment terms goes into the client's row in `## Roster` in the same turn, with the effective date; a floor, discount policy, rush surcharge or rollover rule the user states is a declaration and goes into `config.yaml` under `commercial`; a rate card long enough to be its own document goes to `~/Clawic/data/clients/<file>` with `rate_card_file` pointing at it; the wording of a rise that worked goes to `artifacts/script-rate-rise.md` with its `## Boxes` line.

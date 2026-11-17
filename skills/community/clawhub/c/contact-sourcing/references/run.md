# Test, calibrate and hand off

Run this procedure in the consumer project after criteria/configuration approval
and authorized deployment. Repository authors do not deploy or run this example.

## Propose a concrete sample and budget

Recommend a few representative accounts: a clear fit, a large company with
several business units or ambiguous titles, and a weak-fit/no-match account.
Derive candidates from approved account context. Explain what each tests and
show their identifiers, criteria version, input/output configuration, search
limit, provider page limit, all-or-up-to-N result count and separately requested fields.

Immediately before the preview, read current prices for company resolution,
Sales Navigator sourcing, LinkedIn profiles, the selected qualification model,
its connector's own-key versus Cargo-credit billing mode, and any email/phone
tool and verification action. For agent mode inspect its deployed model, output
schema, one-step limit and empty capabilities/actions before pricing. Inspect internal enrichment
tool routes and retry bounds; a top-level tool name is not a cost quote. Record
lookup time, CLI version, action slugs, units and token assumptions. Do not
count on a cache hit or free retry without evidence.
BYOK provider charges remain part of the maximum cost even when Cargo's credit
receipt does not include them. Quote provider currency and Cargo credits
separately rather than reporting an own-key qualification as free.

| Stage              | Maximum approved units                                                                   |
| ------------------ | ---------------------------------------------------------------------------------------- |
| Company resolution | At most one URL or domain resolution per account needing it; none for ID                 |
| Sourcing           | Sum of provider page limits: `ceil(searchLimit / 25) * 25` per resolved account          |
| Profile retrieval  | At most `searchLimit` unique identified candidates per account                           |
| AI qualification   | At most one call per successfully retrieved profile, using the actual model/token budget |
| Email lookup       | When requested, selected people per account missing suitable existing work email         |
| Email verification | At most newly found emails whose reused tool did not expose equivalent verifier evidence |
| Phone lookup       | When requested, selected people per account missing suitable existing phone data         |

Multiply those units by the fetched applicable prices and add them. Price
resolution, sourcing, profile retrieval, AI qualification, email/verification and
phone separately. Without enrichment there is no email/verification/phone line
item, whether returning all or up to N. For enrichment, bound selected people by
`min(N, searchLimit)` when N is set, or `searchLimit` when returning all. The
provider-page allowance can exceed the number of profiles examined. Unknown
provider units or unbounded nested tool retries prevent a defensible maximum:
inspect or bound them before asking for approval. Output token limits alone do
not bound input tokens; estimate/cap serialized profile and criteria inputs using
the live model context/token rules, and narrow the sample if necessary. Preserve
complete retrieved profiles in results even if a separately reviewed prompt
projection bounds AI input.

Explain the recommendation: a small representative sample checks relevance
before paying for coverage. A broader sample tests more edge cases but adds
profile/AI spend for each candidate, plus contact lookup only after selection.
Then ask the operator to approve these exact accounts and the **maximum cost**.
Wait for their answer. Silence, deployment approval or a prior sample does not
approve a new population. Sample approval does not authorize a full batch.

## Run only the approved sample

Resolve the actual workspace/tool UUIDs from `cargo-ai whoami`, state or the
matching list command, and send its direct link:

`https://app.getcargo.io/workspaces/<workspaceUuid>/tools/<toolUuid>`

Use the existing tool's deployed release. For example, with the operator-approved
input stored in `approved-account.json`:

```sh
cargo-ai orchestration run create --help
cargo-ai orchestration action execute \
  --action '{"kind":"tool","toolUuid":"<consumer-tool-uuid>"}' \
  --data '<approved account JSON>' --wait-until-finished
```

Check the current CLI flags before using them; the example's placeholders must
be replaced with the approved consumer input, not example company data. Keep
parallelism within provider limits and track the approved budget. The graph
sets one attempt for its paid nodes; nested reusable tools can have their own
retry policy and must be priced. Stop expansion when failures or actual cost
invalidate the preview. Poll terminal status and inspect run context/output;
a successful workflow status alone does not prove the ranked output is useful.

Show results as a compact table:

| Rank                           | Person and current role           | Persona / likely buying role | Fit / 10          | Supporting evidence and flags                          | Requested contact data/status   |
| ------------------------------ | --------------------------------- | ---------------------------- | ----------------- | ------------------------------------------------------ | ------------------------------- |
| From the actual returned array | Current employer and profile link | Label inferences             | Numeric relevance | Concise profile evidence; missing information explicit | Verified is distinct from found |

Alongside the table, show company resolution status; searched/examined/unique
counts; duplicate and identity-conflict counts; qualified and selected totals;
insufficient evidence and exclusions; stage failures; and the search-cap notice.
A capped result is the best ranking within the inspected candidates, not a claim
that all stakeholders at the company were found. Preserve unqualified/uncertain
evidence where available for calibration without promoting it into the shortlist.

## Calibrate relevance

Ask exactly the relevance question:

> Are these the most relevant stakeholders at this company? Who is missing, and
> which contacts seem incorrectly qualified or scored?

Never ask whether the operator would approach people in this order. Explain any
observed mistake beside the proposed correction: title search missed a variation,
profile responsibility was ambiguous, a business-unit restriction was missing,
or the score anchors were applied inconsistently. Recommend the smallest
reusable correction and explain the tradeoff of broadening or narrowing it.
Ask for the operator's choice when the correction changes criteria.

Turn accepted feedback into **reusable criteria**, not an ad hoc reshuffle of
this account's output. Update the consumer persona document, source-linked
exclusions/positive evidence, title filters, prompt, persona IDs and criteria
version together. Show the before/after change and which examples are affected.
Replan any resource change within the approved configuration/deployment scope.
Retest affected cases with additional cost approved where needed. Preserve the
original ranks in saved sample results so the new version can be compared.

For example: “Planning Manager” produced financial planners. Recommend adding
a financial-planning exclusion and making capital-project responsibilities
explicit, then test both the false positive and a relevant construction planner
so the exclusion does not remove the desired role.

## Report actual results and remaining uncertainty

Report actual cost by stage, total versus approved maximum, cache/retry effects,
coverage, fit corrections, failed actions and unresolved identities. Include the
tool link and the approved criteria version. Separate deterministic-contract
success from live model/provider quality. Any missing live check stays marked
unperformed; do not mark the installation calibrated when operator feedback or
its required retest is still pending.

## Optional play integration

After calibration ask:

> Do you want to keep this as an on-demand tool, or connect it to a play?

Recommend keeping it on demand if there is no recurring population or destination.
A play is useful when a known process should consume the same results repeatedly;
the tradeoff is repeated provider spend and responsibility for destination writes.
If requested, confirm together:

- Account population and its source.
- Trigger and explicit schedule/enablement choice, if applicable.
- Whether the tool or the play owns selection and enrichment.
- Destination and approved write behavior.

A full-ranking play can use `contacts.slice(0, N)` then enrich selected people.
A shortlist-consuming play uses `contacts` and its statuses directly and must
not repeat profile or contact lookup. Build the concrete integration and show its
graph, target count and cost before any newly required approval. Do not create
CRM writes, campaigns, messages or recurring schedules merely because the tool
was installed. Keep any new play disabled until its separately approved pilot
and enablement procedure are complete.

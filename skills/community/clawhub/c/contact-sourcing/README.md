# Contact sourcing

Build an on-demand Cargo tool that returns the stakeholders most relevant to a
seller's product at each supplied account. Choose all qualified people or up to
N per company, independently of optional verified work email and phone enrichment.
Three is only a suggested starting value, never a fixed ceiling. The operator
can choose top 3, top 5, top 10, any positive N, or all qualified people (`null`).
Enterprise accounts may call for a larger shortlist.

The workflow resolves a company only when needed, searches current employees,
deduplicates stable identities, retrieves profiles, qualifies responsibilities,
and sorts numerically with stable ties. A configured N slices the qualified
ranking before optional contact lookup; fewer qualifying people means fewer
results. It preserves profile evidence and rank even when enrichment fails.

## Optional email and phone enrichment

Email and phone enrichment are included in the tool. During setup, ask whether
to return verified work email, phone, both, or profiles and scores only. Reuse
the workspace's existing enrichment tools and confirm their input/output
contracts; [configure.md](references/configure.md) describes the bindings.

Enrich only the selected qualified people, using the operator's chosen N or all.
This avoids lookup spend on people outside the
returned shortlist. Keep each selected person when a lookup fails, with an
explicit missing/failed status; never backfill with lower-ranked people just
to reach N. An email is marked verified only with matching verification evidence.

## Setup and validation

`SKILL.md` guides a practical building session: research the seller, propose and
approve personas, choose input/count/enrichment and search coverage, review the graph,
deploy with approval, and calibrate an explicitly priced sample. Closed-won
customer intelligence is optional. A CRM, model and play are unnecessary.

| Path                      | Purpose                                                                 |
| ------------------------- | ----------------------------------------------------------------------- |
| `SKILL.md`                | Installer procedure, decisions and invariants                           |
| `infra/index.ts`          | One adaptation surface; selected native graph and exact runtime scripts |
| `references/audit.md`     | Seller evidence, optional customer intelligence and criteria approval   |
| `references/configure.md` | Input/output choices, provider mappings and returned contract           |
| `references/run.md`       | Sample budget, calibration, feedback and optional play                  |
| `evals/acceptance.md`     | Fresh-workspace blind test and approval evidence                        |
| `evals/contract.mjs`      | Offline execution of emitted graphs with fictional external responses   |

The checked configuration is **ID → up to three, no enrichment**, using a fictional capital-
project scheduling seller. `buildContactSourcing` also emits URL, domain and
multiple-input variants. Each supports all or up to N results, with no enrichment,
email-only, phone-only or both. `topN: null` means all; a positive integer caps
results. The `email`/`phone` flags select enrichment without an `outputMode`. Change
only the consumer's configuration and audited output mappings. It declares one
tool, its folder and three adopted connectors; it declares no recurring trigger.
The optional agent backend adds a one-step qualification agent and its folder,
using the operator's chosen OpenAI or Anthropic connection and the same schema.
Setup confirms the title Boolean from existing context or seller research,
recommends slightly broader titles for subsequent scoring, and asks about an
existing API key versus Cargo credits without collecting secrets in chat.
See the workflow diagram in `SKILL.md` and the exact output contract in
`references/configure.md`.

The live metadata and three supplied saved workflow references were inspected
read-only on 2026-09-09 using Cargo CLI 1.0.91. Draft references contain incomplete
routes and older outreach instructions, so the approved behavior in this skill
controls the example. Current metadata confirms current-company/title filters,
profile fields, page rounding and `openAi.instruct` structured output. The email
reference returns only `email`; this example therefore explicitly verifies a newly
looked-up address. A consumer tool that exposes equivalent verifier evidence can
reuse that result after its output contract is audited.
The LLM metadata and agent contract were rechecked read-only on 2026-09-30 with
CLI 1.0.102; provider changes still require sample calibration.

No paid provider run, deployment or fresh-workspace installation was performed
for this build. Static contracts do not prove live coverage, classification
quality, engine failure envelopes, or enrichment deliverability. State remains
**to-be-approved** until a fresh demo and two customer or partner implementations
supply the evidence requested for this build.

## Migration from the historical example

`contact-sourcing` was removed from the tree before it had a customer skill.
The historical `source-contacts` play matched accounts, enriched everyone and
upserted verified contacts into HubSpot by email. This implementation restores the
same directory name with the approved on-demand behavior. There is no current-main
installation to migrate automatically.

For a consumer still using that historical code, keep its existing state and
resources while reviewing a migration. Replace the play's embedded sourcing with
a call to `contact_sourcing`, read `contacts` instead of the old `{ sourced: true }`
output, and explicitly decide whether the play or tool owns selection/enrichment.
Any CRM write remains in the consumer's play and needs a reviewed mapping and
identity policy. Do not delete or prune the historical play automatically.

The live reference output `best_persona` is not the new contract. Consumers using
that field must map to `contacts` and its nested `qualification`; outreach strategy
and triangulation fields have no counterpart. No live reference UUID or private
customer data is a dependency of this example.

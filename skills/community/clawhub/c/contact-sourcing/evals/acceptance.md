# Acceptance and fresh-workspace blind test

The repository example is **to-be-approved**. Passing static checks or opening a
PR does not establish approval. This build also requests a fresh demo workspace
and two independent customer or partner implementations. Store only internal evidence references
in `.github/data/approvals.json`; do not publish customer identities or records.

## Offline contracts

Run from the repository root:

```sh
npm ci
npm run typecheck
npm run validate
npm run format:check
node --import tsx contact-sourcing/evals/contract.mjs
npm run validate:routing
```

`npm run validate` discovers the contract automatically and also checks/plans
`infra/` in isolation. The contract executes the emitted nodes, native branches,
group item graphs, exact scripts and end mappings against fictional provider
responses. It reverses group results to test preservation of rank. It does not
call a provider or reproduce the remote engine's complete behavior.

Check all 96 input/count/enrichment/qualification variants, not just the checked
ID/up-to-three/no-enrichment/OpenAI-action default:

- ID bypasses company enrichment; URL/domain resolve before sourcing; multiple
  input uses ID then URL then domain and conflicting/unverified identities stop.
- A resolution failure or ambiguity cannot reach unscoped people search.
- No CRM, model, autonomous agent, play or recurring trigger is required.
- Stable person deduplication precedes repeated profile/qualification spend;
  numeric LinkedIn and opaque Sales Navigator IDs are not interchanged.
- Wrong employer, profile identity conflict, misleading title and concurrent
  side roles do not automatically qualify; sparse evidence stays identifiable.
- Numeric scores, stable ties and practitioner relevance determine ranking.
- Invalid/out-of-range model output cannot enter the qualified shortlist.
- Zero matches, fewer than N, optional minimum and provider-page cap are explicit.
- All or up to N is independent of enrichment; the slice follows qualification
  and sorting, including when no contact details are requested. N is a maximum.
- No-enrichment configurations emit no contact lookup; requested enrichment touches selected people only;
  email-only emits no phone node and phone-only emits no email or verifier node.
- Profiles survive unchanged with no second profile call after selection.
- Lookup/verification failures retain selected people and their original ranks;
  there is no automatic backfill to N reachable contacts.
- Suitable existing verified data can be reused; found is distinct from verified.
- Three is only a starting suggestion, with no fixed ceiling. Top 3, top 5,
  top 10, larger N and all work with every enrichment choice; changing N leaves
  the candidate pool and qualification calls unchanged.
- OpenAI and Claude agent paths share the qualification schema, evidence and
  failure handling, with one step and no autonomous tools or capabilities.
- Optional closed-won research is gated by the operator's choice; decision-local
  recommendations and reusable feedback updates are present in the procedure.

## Fresh-workspace blind-test protocol

Use a new demo workspace and a new consumer Cargo project with no pre-existing
persona memory. A tester who did not author this skill performs the installation
using only the installed procedure and references. No author coaching, private
reference UUIDs or copied customer configuration. The tester records where the
instructions were insufficient, even if an expert could improvise a fix.

1. Start with a fictional or explicitly authorized seller and no CRM connection.
   Confirm that the skill derives seller facts before asking and inspects
   connectivity before offering website-only or export/CRM intelligence. Do not
   run paid research without its own approval. Record the actual source URLs
   and the observed/inferred distinction.
2. Record the actual persona table, human Boolean, supported filter translation
   and prompt shown together. Confirm the explanation of ambiguous titles,
   responsibilities and buying-role inference. Give one correction and verify
   all reusable criteria change consistently before approval. Test reuse of
   existing context graph evidence, and website research when that context is
   missing. Confirm the exact job-title Boolean and the slightly broader search
   recommendation, including its extra profile/LLM cost.
3. Exercise the ID installation without enrichment, for both all and up to N.
   Verify that the count question is asked independently of enrichment and
   that the slice follows qualification/sorting, returning fewer if fewer qualify.
   Verify that it produces only the
   selected graph, reconciles existing connectors and needs no CRM/model/play.
   Review criteria/configuration and the plan before explicitly authorizing
   deployment. Preserve that approval evidence and the direct tool link.
   Verify that three is presented as a suggestion, then select 5 and 10 and
   confirm only the selected count and corresponding enrichment calls change.
   Include an enterprise account where a larger shortlist is appropriate.
   Ask about OpenAI/Anthropic keys versus Cargo credits without
   collecting the secret. For a selected own-key provider, test the bounded
   qualification agent and its shared schema; confirm Claude uses Anthropic and
   OpenAI uses OpenAI. An agent's live structured-output enforcement and billing
   need separate approved validation; static compilation cannot establish them.
4. In a separately approved adaptation, exercise URL and domain paths and then
   both all and a chosen N with email-only, phone-only and combined enrichment,
   using real consumer tools whose mappings were inspected. No unused
   branch should survive an installation that does not need it. Confirm the
   email tool's verification contract, including the explicit verifier when
   only an address is returned.
5. Propose representative accounts, show company/sourcing/profile/AI/email/phone
   costs separately, account for 25-row pages, and obtain exact sample/max-cost
   approval before executing. Test no-match and a capped account. Refuse any
   expansion to a full batch based only on sample approval.
6. Inspect real `runContext` and outputs. Verify native failure successors,
   group empty/failed-item envelopes, `.answer` structured output, token
   limits/refusal handling, profile paths and preservation, numeric ranks,
   resolved IDs, existing-data reuse, enrichment failures and verification
   status. Compare results to the source profiles and stage credit receipt.
   Static fixtures cannot prove any of these live provider/engine behaviors.
7. Have the operator judge relevance with the prescribed question. Include a
   misleading title, wrong employer, advisory side position, sparse profile,
   relevant practitioner and unrelated executive where authorized examples
   permit. Record false positives and missing people; do not substitute an
   outreach-order question. Correct reusable criteria and obtain additional
   spend approval for affected retests.
8. Finish with actual costs, coverage, unresolved issues, approved criteria
   version and an explicit on-demand-versus-play choice. If the operator keeps
   it on demand, no destination/schedule exists. If a play is requested, confirm
   population, trigger, selection/enrichment owner and destination, then follow
   its separate disabled-pilot/enablement approvals.
9. Repeat the optional customer-intelligence path only with an approved CRM or
   export. Seed a mere associated contact and a documented buyer/champion;
   verify association alone is never promoted to proof and private records stay
   out of public artifacts. When this analysis already provides useful evidence
   about relevant stakeholders in won deals, verify that the installer recommends
   N with a brief reason grounded in that evidence. Without useful evidence,
   verify that it asks directly; neither path adds a separate audit for N.

Evidence must include a dated install transcript, adapted graph/plan, approval
records, representative outputs, criteria before/after feedback, stage costs,
known failures and a reproducible list of unresolved steps. Sanitize before
linking internal evidence from the public approval file. The fresh demo alone
is insufficient: add two independently completed customer/partner
implementations before changing the approval state or removing the banner.

## Unperformed for this repository build

- No paid profile, search, qualification, email or phone action was run.
- No consumer resources were deployed and no fresh demo was installed.
- Real provider coverage, primary-employment judgment, verifier outcomes,
  nested-tool retry/cost behavior, agent schema enforcement/BYOK billing and
  remote failed-item envelopes are unverified.
- Operator calibration and customer/partner implementations have not occurred.

Read-only current integration metadata and the three supplied saved workflow
references were inspected. This establishes schema/reference observations, not
live performance or production readiness.

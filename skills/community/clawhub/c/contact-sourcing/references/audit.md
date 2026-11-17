# Understand the seller and approve the people

Setup is a learning session and a build together. At each decision, explain what
changes, recommend from observed evidence, name the alternative's tradeoff, ask
for the operator's choice, then apply it and show the result. Do not repeat an
answered question or ask for facts that can be inspected.

## Inspect before asking

Read the consumer project's existing context graph, context directory, any
`defineContext` singleton, personas, prior decisions and declared resources. Use `cargo-ai whoami`
to confirm the workspace, then inspect authenticated connectors and reusable tools
with `cargo-ai connection connector list` and `cargo-ai orchestration tool list`.
Inspect relevant tool releases and their output schemas. Do not mint a duplicate
connector, enrichment tool, CRM extract or context resource.

Establish the seller's product/use case from available context. Ask only if it is
missing or several products make the intended one ambiguous. Explain that a
person can be relevant to one product and irrelevant to another.

Derive the title Boolean and key decision makers from that context when it is
useful and current. If it is missing or incomplete, crawl the **seller's**
website, product pages and customer stories using an available browser or
approved research capability to understand the product and relevant decision
makers, influencers and practitioners. Fill only the gaps; do not repeat research
already present in the context graph. Retain context paths, source URLs and the
retrieval date. Do not crawl target accounts to rediscover the seller on each
run. If a paid research action is needed, price it and obtain its own limited
approval before using it. Repository authoring does not authorize paid research.

Record value proposition, problems solved, jobs to be done, target
responsibilities, title variations, likely buying roles, positive evidence and
exclusions. Separate **Observed** statements from **inference**. Customer stories
can reveal a responsibility or use case without proving that everyone with that
title buys the product.

## Optional customer intelligence: ask after connectivity inspection

Explain: website positioning describes intended buyers; actual deal evidence can
show different users, champions or buyers. Recommend adding customer intelligence
when sufficient relevant closed-won evidence is available. Website research alone
is a valid and quicker starting point when evidence is thin or no CRM exists.

If a CRM is connected, ask:

> Should we also analyze contacts associated with closed-won deals to refine the
> personas? We can use your connected CRM, an export, or proceed with website
> research alone.

Without a CRM, adapt the choice: mention an available export or website research
alone, and do not require the operator to connect a CRM. Read private contacts
only after the **operator chooses** customer intelligence. Connectivity inspection
is not permission to analyze deal contacts.

When chosen, inspect the relevant contacts, recorded buying roles, deal history
and available notes. Distinguish documented buyers/champions from contacts merely
associated with a deal. Missing evidence remains missing. Report differences
between website positioning and observed customer personas, including sample bias
and any inference. Keep raw records, names and private deal evidence in the
consumer project under its own access conventions, never in this public skill.

## Present three things together

Use one concise presentation containing the persona table, the human-readable
job-title Boolean and the actual person-qualification prompt. Show the exact
included title variations, OR groups and exclusions, and say whether they came
from the context graph or seller website research. Have the operator confirm this
Boolean before building the provider filters.

| Persona                          | Responsibility and positive evidence                         | Title variations                             | Likely buying role                                | Exclusions                                        | Support                                       |
| -------------------------------- | ------------------------------------------------------------ | -------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- | --------------------------------------------- |
| Fictional planning practitioner  | Owns capital-project schedules, P6 or schedule-risk analysis | Planning Engineer, Scheduler, Senior Planner | End user or influencer; inference until supported | Financial or urban planning                       | Actual seller source URLs during installation |
| Fictional project-controls owner | Owns planning processes or schedule-risk decisions           | Project Controls Manager, Head of Planning   | Influencer or decision maker; inference           | Unrelated executive, advisory/community role only | Actual seller source URLs during installation |

These rows illustrate structure only. Replace them with researched personas;
record explicit persona IDs matching `configuration.personaIds`.

Human-readable Boolean for the fictional example:

```text
CURRENT COMPANY = supplied account
AND TITLE IN ("project controls" OR "planning" OR "scheduling" OR "scheduler")
AND TITLE NOT IN ("financial planning" OR "urban planning")
```

Explain: titles find candidates; responsibilities establish relevance. A
“Planning Manager” could own construction schedules, financial forecasts or urban
planning. Profile qualification distinguishes those responsibilities. Recommend
a slightly broader title search than a title-only shortlist, including adjacent
titles with plausible responsibility. Each retrieved candidate with usable
evidence will be qualified and scored before selection. Keep the company scope,
hard exclusions and approved cap; broader search adds profile/LLM cost and does
not guarantee finding every relevant person. Show the proposed additions before
approval.

Translate that intent into current supported provider filters; do not pass this
whole Boolean as a search string. The checked Sales Navigator configuration uses
`company.currentCompanyIds`, `role.titleKeywords` and
`role.titleKeywordsExclude`. Some restrictions require profile qualification,
and unsupported Boolean groupings may need separate bounded searches whose
combined cap and deduplication are explicit. Show the actual payload beside the
Boolean so limitations are visible.

Show `qualificationPrompt` and the approved seller criteria from `infra/index.ts`
in readable form. Explain its 0–10 anchors, three qualification outcomes,
employment check, evidence requirement and likely buying-role inference. Do not
assign extra relevance solely for seniority or invent a universal cutoff.

Ask:

> Can you confirm this job-title Boolean, including its title variations and
> exclusions, or tell me what to add or remove?

> Are these the right people to target? Who is missing, who should be excluded,
> and which personas are most relevant?

Apply corrections to the persona IDs, responsibilities, title filters,
exclusions and prompt together. Show the revised proposal and carry earlier
approval forward where unchanged. Ask again only for a new or unresolved choice.

## Save the approved criteria

Follow existing context conventions. Reuse a `defineContext` singleton when one
exists; a local criteria document is enough when it does not. Do not add a model
or agent to store these decisions. Save a readable record with:

- Seller/product/use case, source URLs, dates, observed evidence and inferences.
- Persona IDs, responsibilities, positive signals, exclusions and likely roles.
- Website-only or approved closed-won/export choice and its evidence limitations.
- Human Boolean, exact provider filters, geography/business-unit restrictions.
- Qualification prompt, schema version, 0–10 anchors and any approved minimum.
- Operator corrections, approval/date and a reusable `criteriaVersion`.

Compile the approved criteria into the tool settings. Every run returns their
version; it does not research the seller again. Preserve the before/after criteria
when feedback changes them so retesting can identify affected examples.

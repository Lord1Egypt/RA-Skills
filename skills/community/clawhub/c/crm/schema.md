# Schema — Entities, Fields, and What Earns Its Place

Every field is a tax paid at every record creation forever. The schema question is never "what could we store" but "what filter, report or follow-up rule needs this to exist".

**Contents:** [The Four Entities](#the-four-entities) · [Ids](#ids) · [Field Types That Survive](#field-types-that-survive) · [Tags vs Fields vs Enums](#tags-vs-fields-vs-enums) · [Names, Emails, Phones, Domains](#names-emails-phones-domains) · [Relationships](#relationships) · [The Fields Everyone Adds And Nobody Fills](#the-fields-everyone-adds-and-nobody-fills) · [Adding, Renaming, Deleting](#adding-renaming-deleting) · [Consent Fields](#consent-fields)

**Before changing any schema**, read `## System` in `~/Clawic/data/crm/memory.md` and `artifacts/field-dictionary.md` if `## Boxes` points to it. A field added twice under two names is the most common self-inflicted CRM wound.

## The Four Entities

Person, Organization, Deal, Interaction. Everything else is a field, a tag, or a report — resist a fifth entity until a real query needs it.

| Entity | Exists to answer | Grows with |
|---|---|---|
| Person | Who is this, how do I reach them, when did we last talk | Your network |
| Organization | Who else is there, what segment, is this account alive | Your customer base |
| Deal | What is in play, worth what, at what stage, next step when | Your activity |
| Interaction | What actually happened and when | Time — fastest of the four, which is why it lives in its own file |

Candidates for a fifth entity, and what to do instead: **Products/line items** → a text field until pricing genuinely varies per deal. **Tasks** → the deal's next-step field plus a real calendar; a task list inside a CRM is a second to-do system that goes stale. **Campaigns** → a `source` value. **Documents** → a link field pointing at where the file actually lives. **Notes** → interactions; a standalone note with no date is unfindable by design.

## Ids

- **UUID, generated at creation, never reused, never displayed as the thing a human types.** Auto-increment integers collide the first time two exports are merged, and they leak volume to anyone who sees `deal/47`.
- **The id is not the identity key.** Identity is the email (person) or the domain (organization) — the id is what other tables point at. Deduping happens on identity; joins happen on id (`hygiene.md`).
- **Keep the foreign system's id when you import one**: `hubspot_id`, `sheet_row`. It is what makes a re-sync or a rollback possible, and it costs one column (`import.md`).
- Interactions reference `contact_id`, never a name. A name in a foreign-key position breaks the day someone gets married or the record is merged.

## Field Types That Survive

| Type | Use for | Rule |
|---|---|---|
| enum (closed list) | stage, source, reason, segment, tier | Six values or fewer at the start. Every value has to be countable in a report, or it is a tag |
| date | created, last contact, close, stage-entered | ISO `YYYY-MM-DD`, always. Locale-formatted dates in a CSV are the single biggest import corruption source |
| money | deal value | Number plus explicit currency (`18000 EUR`) — never a formatted string, never a bare number |
| text short | name, role, next step | One line. If it wants to be a paragraph it belongs in an interaction |
| text long | context, notes | Exactly one such field per entity |
| bool | suppression flag, is-customer | Only when the answer can never be "partly" — otherwise it is an enum |
| list/tags | anything a filter might want that no report groups by | Free growth, controlled vocabulary (below) |
| link | document, profile, external record | URL only; never paste the document's contents into the record |

Computed, never stored: last contact date (derive from interactions), days in stage, age, fill rates. A stored value that a query can derive is a value that will be wrong by next week.

## Tags vs Fields vs Enums

The decision, in one question: **does a report group by it?**

- Report groups by it → **enum field** with a closed list. Six values, agreed once, recorded in `## System`.
- A filter occasionally wants it, no report counts it → **tag**. Cheap, free-growing, no schema change.
- Only one person cares and only once → **the notes field**, or nothing.

Tag vocabulary rots without one rule: **lowercase, singular, hyphenated**, and a monthly glance at the tag list during the hygiene sweep. `Design`, `design`, `designer` and `design-work` as four live tags means tags have stopped being a filter and become free text with extra steps.

## Names, Emails, Phones, Domains

- **One `name` field, plus optional `first_name` for greetings.** Splitting into first/middle/last breaks on mononyms, multiple surnames (common across Spanish and Portuguese naming) and inverted order, and every merge has to guess which half is which. If a mail merge needs a greeting token, store the greeting.
- **Emails are stored lowercased**, and the person can have more than one. Model it as `email` (identity, work) plus `emails_other` (list). Personal addresses are higher-risk data under every privacy regime and are worth not collecting at all (`privacy.md`).
- **Phones in E.164** (`+34600123456`): no spaces, no parentheses, country code always. Local-format phone numbers cannot be dialed by any tool and cannot be deduped.
- **Organization identity is the domain**, not the display name: "Acme", "ACME Inc" and "Acme Corporation" are three rows and one company. Subsidiaries with their own domain are their own organization with a `parent` field; the same company on `acme.com` and `acme.co.uk` is one organization with a domain list.
- Free-mail domains (gmail, outlook, proton) are never an organization. A contact whose only address is free-mail gets `org: —`, not an invented company.

## Relationships

- **Person ↔ Organization is many-to-many over time.** The current employer is a field; the history belongs in interactions or a `past_orgs` list. Overwriting the employer when someone changes jobs deletes the reason you know them, and their new company is usually your best warm lead (`followup.md`).
- **Deal → one organization, one primary contact, many participants.** The primary contact is who owns the decision path, not who replies fastest — a deal whose primary contact is a friendly non-buyer is a deal about to stall (`pipeline.md`).
- **Referrals are an edge, not a tag**: `referred_by: <contact id>`. It is the only field that tells you which relationship is actually producing revenue, and a report over it beats any attribution model a small business can afford (`metrics.md`).
- Households, agencies acting for a client, and consultants who move between accounts: keep the person primary and the organization mutable. The person is the constant.

## The Fields Everyone Adds And Nobody Fills

| Field | Why it dies | Instead |
|---|---|---|
| `lifecycle_stage` alongside `deal_stage` | Two truths, drift within a week, every report has to disclose which one it used | One status field; derive the other in the report |
| `probability` per deal | Hand-set numbers are optimism with a decimal point | Compute from measured stage conversion (`metrics.md`) |
| `lead_score` before any closed deals | Scores a model of a customer you have never had | Score after ~20 closed deals, from what those had in common |
| `industry` free text | 40 spellings of "software" | Enum of the six segments you actually sell to |
| `birthday` | Fills at 5%, and the greeting it enables belongs elsewhere | `people` skill |
| `linkedin_url` for everyone | Re-derivable from name plus company, wrong after a job change | Store it only when it is the preferred channel |
| Second and third notes field | Context becomes unfindable, which is worse than absent | Exactly one notes field per entity |
| `last_contacted` typed by hand | Wrong the moment someone forgets to update it | Derived from `interactions/<year>.md` |

## Adding, Renaming, Deleting

1. **Adding**: name the query it serves and who fills it, then set the default. A field nobody is named to fill is empty by design.
2. **Measure at 30 days**: `fill_rate = filled / total_records_created_since`. Below ~70%, either make it required at creation or delete it (SKILL.md Rule 6). Recording that number is what makes the decision an argument-ender.
3. **Renaming** happens in the tool *and* in `artifacts/field-dictionary.md` in the same turn, and any import mapping that references the old name is updated with it — otherwise the next import silently writes into a field that no longer exists.
4. **Deleting**: export the column first, then drop it. Half of deleted fields turn out to have three records with irreplaceable content in them.

## Consent Fields

Three fields, added the day the first person is contacted, not the day a regulator asks. They cost almost nothing and they are unreconstructable retroactively (`privacy.md`).

| Field | Values | Why it cannot be added later |
|---|---|---|
| `source` | Closed list: referral, inbound, event, purchased list, existing customer, manual | It is the lawful-basis evidence. Six months on, nobody remembers where a row came from |
| `consent_ts` | ISO date, or empty | Consent has a date or it is not consent. Empty is honest and means "another basis applies" |
| `basis` | consent \| legitimate-interest \| contract \| none | Determines what may be sent to this person, and the answer differs per row |

The suppression flag is a fourth, and it is the one field that is **never** overwritten by an import (`import.md`) — an import that resets opt-outs is the most expensive schema mistake in this file.

**After any schema decision**, write it to `## System` in `~/Clawic/data/crm/memory.md`, and create or update `~/Clawic/data/crm/artifacts/field-dictionary.md` — field, type, required, who fills it, what it is for, last measured fill rate — adding its `## Boxes` line in the same turn (`memory-template.md`). A schema nobody wrote down gets re-litigated every quarter.

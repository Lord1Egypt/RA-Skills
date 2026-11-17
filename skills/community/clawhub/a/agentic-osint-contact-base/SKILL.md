---
name: agentic-osint-contact-base
description: Method for a verified B2B contact base — registry mapping, per-field proof, no guessed emails, GDPR. Use when building a lead list, finding a work email, or enriching contacts. Trigger on "build a lead list", "find their email", "enrich these contacts", "is this GDPR compliant".
metadata: {"clawdbot":{"emoji":"🧾","homepage":"https://blochagents.com"}}
---

# Agentic OSINT Contact Base

**A public registry is authoritative about ENTITIES, never about PERSONS. Every value you write carries the URL that proves it, or it stays empty.**

**What this skill is.** A method: the invariants, the decision tables, the thresholds, and the traps. It does **not** ship the pipeline. The checks it demands — proof gate, merge, suppression filter, retention purge — you write yourself, in your own stack, against your own data. Each one below comes with the failure it is known to fail into. That is the transferable part; a compliance guard that is subtly wrong is worse than none, because someone will trust it.

## Declared footprint — read before running

| Item | Declaration |
|---|---|
| Access required | Web search + HTTP GET on public pages. No login, no session cookie, no paid database. |
| Data persisted | One local JSON file per run, under `${WORK_DIR}`; all runs under `${RUNS_ROOT}`. Business contact fields only. |
| Retention | 12 months from collection by default, then delete. Enforced only by a purge you implement and run over **every** run directory — see `### 4. Retention purge`. |
| Network egress | **None by default.** No webhook, no upload, no CRM push unless the operator explicitly configures one. |
| Out of scope | Breach dumps, credential stores, scraping behind a login, anything the target site's ToS forbids. |

## Legal basis — a design constraint, not a disclaimer

**This skill collects; it never sends.** The obligations below bind the outreach step downstream, in the operator's own channel — and the base is not deliverable to a channel that cannot honour them. It processes personal data of professionals: under GDPR, B2B prospecting can rest on **legitimate interest (Art. 6(1)(f))**, a *conditional* basis, not a free pass. It holds only if all of the following are true in your run:

| Requirement | What it forces in this pipeline |
|---|---|
| **Purpose declared first** | Write the purpose down before collecting ("contact firms in sector X about service Y"). No purpose → no run. |
| **Minimisation (Art. 5(1)(c))** | Only fields that serve that purpose. A role-based work email usually suffices. Personal mobiles and home addresses are rarely necessary — omit the field entirely rather than fill it. |
| **Balancing test** | Prospecting a business role at a business address is proportionate. Profiling a private individual is not. If the target is not acting in a professional capacity, stop. |
| **Information (Art. 13/14)** | The first message says who you are, where the data came from, and why. Not a footer — a sentence. |
| **Right to object (Art. 21)** | Unconditional for direct marketing. One-click opt-out in every message; honour it the same day. Suppression list at `${RUNS_ROOT}/suppression.txt`, covering **every** address the person is reachable at. |
| **Retention** | Set at collection, stamped as `delete_after`, and actually deleted by code you run. A date nobody enforces is an annotation. |
| **ToS compliance** | If a platform's terms forbid automated collection, that platform is out of scope. There is no workaround section in this skill. |

Local law adds to this: some jurisdictions require prior consent for B2B email, and telephone canvassing is gated by national opt-out registers. Check the destination country before the first send, not after.

## When to Use

| User says | Action |
|---|---|
| "Build me a list of every X in region Y" | Stage 1 — map entities from a public registry |
| "Find the contact for this firm" | Stage 2 — single-entity fan-out |
| "Enrich these contacts with emails/phones" | Stage 3 — per-field proof enrichment |
| "Just guess their email format" | **Refuse.** Explain the permutation rule below. |
| "Get me their personal mobile" | Challenge the purpose; drop the field unless genuinely necessary |

## Setup

| Placeholder | Example | Meaning |
|---|---|---|
| `${REGISTRY_URL}` | official register for your sector | Authority on entities |
| `${SECTOR}` / `${REGION}` | `acme-sector` / `region-01` | The population you are mapping |
| `${PURPOSE}` | `outreach about acme-corp service` | Written before any collection |
| `${RUNS_ROOT}` | `./runs` | Parent of every run directory. The purge sweeps it. |
| `${WORK_DIR}` | `${RUNS_ROOT}/run-2026-01` | This run's local output only |
| `${RUNS_ROOT}/suppression.txt` | one address per line | People who objected. Never expires, never deleted. |

**The suppression list lives at `${RUNS_ROOT}`, above the runs, and that placement is the mechanism.** It is the one file carried across runs and the one the purge must never touch. Put it inside a run directory and every new run starts with an empty one — the objection is forgotten and the person contacted again, the exact breach the list exists to prevent.

## Stage 1 — Map the population from a public registry

The registry gives you the **denominator**: how many entities exist, so you know what "complete" means. It does not give you people. **Registers differ and none matches a canned shape** — inspect the response once (`curl -s "${REGISTRY_URL}/search?..." | jq 'keys'`) and write the extraction against what you actually see. Keep identifiers only: `entity_id`, `legal_name`, `city`, `registry_url`. An entity count of 0 means your paths are wrong, not that the sector is empty — treat 0 as a bug, never as a result.

**The line that matters:** the register is authoritative for `legal_name`, `entity_id`, `city`. It is *not* authoritative for who works there today, nor for any individual's contact details. A director listed in a register is evidence of a mandate, not evidence of a working email. Never infer a person from an entity record, and never promote an entity's switchboard number into a person's field.

## Stage 2 — Fan-out by ENTITY

**The unit of research is the organisation, not the person.** One agent per entity, never one per person, because: an entity has one canonical site and one legal-notice page while a person is scattered across all of them (entity search converges, person search loops); homonyms resolve inside an entity via city + registration number + role, and are unresolvable outside it; and the roster comes out of the entity page, so you discover people you never named — a person-first fan-out can only ever find people you already knew.

**The agent's output contract — the whole chain depends on it.** Each agent reads one entity and **writes `${WORK_DIR}/enriched-<entity_id>.json`**: a JSON array of records matching `## Output format`, `[]` if it found nobody. Everything downstream reads that glob and nothing else. An agent that returns prose, writes elsewhere, or writes an object instead of an array breaks the chain silently.

**Every field in the schema must be PRESENT and empty (`""`), never absent.** This is not cosmetic. Downstream steps rank records by looking up `person_email_confidence` in a mapping; in jq, indexing a map with `null` (absent key) is a *hard error*, and a trailing `// 0` does not save you — the index raises before the alternative applies. `""` sorts; a missing key crashes the merge. "Leave unproven fields empty" means empty string, not omitted, and your agent contract must say so in those words.

Before Stage 3, compare the count of returned files against the Stage 1 denominator. Short means agents died — re-run only the missing IDs.

## Stage 3 — Enrich with per-field proof

Every field ships with its own source URL and its own confidence. Fields are proved independently: a verified site does not vouch for the phone number printed next to the email.

| Field | Accepted evidence | Confidence |
|---|---|---|
| `legal_name`, `entity_id` | Public register record | `high` |
| `website` | Register record or the site's own legal-notice page | `high` |
| `role_email` (`contact@`, `info@`) | Legal-notice page, contact page, official directory | `high` |
| `person_name`, `person_role` | Entity's own site/roster page, official professional directory | `high` |
| `person_email` | Same page that names the person, or a `mailto:` on it | `high` |
| `person_email` from format guess | **Never accepted alone.** Second independent source or the field stays empty. | `low` / empty |
| `phone` | `tel:` link or printed number on a page owned by the entity | `medium`–`high` |
| Anything from a data-broker aggregator | Not proof — use as a lead to a primary source | — |

### The knowledge of NOT guessing

**An LLM's default failure mode on this task is to emit `firstname.lastname@domain.com` and ship it unmarked.** It looks right. It scores well. It is fabrication. The pattern is real for some domains and wrong for others, and nothing in the output distinguishes the two — which is why the discipline must be mechanical, not judgemental:

| Trap | Why it fails | Rule |
|---|---|---|
| Permuted address | Plausible ≠ true; no signal separates the two | A hypothesis, never a value. Needs a second independent citable source. |
| Catch-all domain | Accepts every address, valid or not | Syntactic validity proves nothing. |
| MX record present | Proves the *domain* receives mail | Says nothing about the *mailbox*. |
| No source found | — | Field stays empty. `"unknown"`, `"n/a"` and a plausible guess are all wrong; the guess is the most expensive. |

**Low fill rate on a hard field is a quality signal, not a failure.** 30% direct emails with 100% sourcing beats 95% with a third invented, because the invented third is undetectable at delivery and surfaces weeks later as bounces, spam complaints, and a burnt sending domain. Report fill rate per field, per source class. Never optimise it by loosening proof. If the client wants a higher number, the answer is more entities, not weaker evidence.

## The four gates you must write yourself

Each gate below is required before delivery. Each is stated with the way it is known to break — these are not hypotheticals; every one was found by running a version of it that looked correct.

### 1. Proof gate — reject any value without its source URL

Refuse every record carrying a value whose `_source` companion is empty. Run before every delivery; a hit is a blocking defect, not a warning.

**Trap A — partial coverage.** The gate must cover **every** `(field, field_source)` pair in the schema, derived from the schema itself, not hand-enumerated. Hand-enumeration forgets a field, and the field it forgets is the one this method pushes toward when nominative proof is missing: `role_email`. That is the worst possible gap — `contact@`/`info@` are the easiest addresses in the world to invent, so they demand the *most* proof, and the doctrine explicitly routes to them when fill rate is low. A gate covering `person_email` and `phone` only will pass `{"role_email":"invented@…","role_email_source":""}` and report a clean base.

**Trap B — a gate that reads nothing prints success.** If your glob matches no file, the tool writes an error to stderr and an empty result to stdout — and an empty result is precisely your PASS signal. Zero records verified reads exactly like "clean, deliverable". **Make the verdict depend on the number of files actually read, not on the emptiness of the output:** count the inputs first, ABORT if zero, and never let a non-zero exit code scroll past under a `2>/dev/null`. Absence of error is not evidence of verification.

### 2. Merge — dedupe on (entity_id, normalised person name)

The pair is the identity. On conflict the **stronger evidence class** wins — not the more recent record, not the more complete one. Two different people at one entity are two rows, never one. Normalise the name for the key: lowercase, trim, collapse internal whitespace.

**Trap C — the verification that cannot fail.** The obvious check ("distinct keys in equals rows out") is a *tautology*: `group_by(k) | map(last)` produces exactly `unique(k)` rows **by construction**, so both sides derive from the same group key and the numbers are always equal, whatever the data. It reassures without testing, on the single most destructive step of the pipeline. A verification must compare against an invariant **independent of the merge**: count distinct pairs on the **raw**, un-normalised name, and report `in_raw` / `in_normalised` / `out` with the list of pairs normalisation collapsed. That list is what has audit value; an equality true by construction has none.

**Trap D — the crash that eats the file.** Redirecting the merge straight onto `merged.json` truncates it to zero bytes *before* the command runs. One malformed record (see the present-but-empty rule) and you have lost the merge and the input state. Write to a temp file, then `mv`.

### 3. Suppression filter — Art. 21, applied before every delivery

Drop anyone on the suppression list. Output a separate `deliverable.json`; never ship `merged.json`.

**Trap E — matching raw strings.** The list is typed by a human pasting an address out of an unsubscribe mail. It carries mixed case, a trailing space, a CR from a Windows line ending. Normalise **both sides** — case, surrounding whitespace, `\r` — or `A.Doe@Y.z` will not match the collected `a.doe@y.z` and the person who told you to stop gets contacted again. A case-sensitive comparison here is a fail-open on an unconditional right.

**Trap F — the nominative-only filter.** Test **every** email field, not just `person_email`. An objection covering only the nominative address is one the pipeline routes around, because `role_email` is the fallback channel this method recommends. One person, all their addresses.

Deleting an entry from the list is how you re-contact someone who told you to stop.

### 4. Retention purge — the step that executes the declaration

**Sweep every run directory under `${RUNS_ROOT}` at the start of each run** — not the current one, whose `merged.json` does not exist yet. A purge aimed at the run you are about to create can only delete rows you just collected: a no-op in the costume of compliance, worse than no date at all, because it documents the breach. Purge **both** `merged.json` and `deliverable.json`: purging one while a stale copy survives beside it retains nothing less. Audit first, purge, re-audit — the second audit must print 0, and a second purge must purge 0.

**Trap G — the undated row compares as expired.** In jq, both `null` and `""` sort below any date string: `"" < "2026-07-16"` is **true**. Under the present-but-empty rule this skill imposes everywhere else, an unstamped row holds `""`, not `null` — so `select(.delete_after != null)`, the guard the word "null" invites, still destroys every one of them. Verified: `[null, "", "2020-01-01", "2099-01-01"] | map(select(. < "2026-07-16"))` keeps the first three; adding `. != null` keeps `""` in the kill list. A row whose date was never stamped is counted expired and silently destroyed. The direction is fail-closed, so it is not a breach — it is mute data loss on fresh rows, with no warning. Count undated rows separately and print them loudly as "purged as unretainable".

**Trap H — nobody stamps the date.** Declaring 12 months and showing `delete_after` in the schema does not compute it. Unless a step in your pipeline derives the date (`date -u -d '+12 months' +%F` on GNU, `date -u -v+12m +%F` on BSD/macOS — write both) and the agent contract requires it, your purge only acts on rows someone happened to date. Enforced retention means code, in the run.

## Where NOT to look

Knowing which sources return nothing is worth as much as knowing which return something.

| Source | Why it wastes the run |
|---|---|
| Data-broker / aggregator directories | Recycled, stale, unciteable. They mirror the primary source you should have read. |
| Anything behind a login or paywall | Out of scope by ToS; the value is not usable evidence anyway. |
| Breach dumps and "leaked" corpora | Unlawful basis, poisons the whole base. Absolute exclusion. |
| Generic social bios for role emails | Bios rot; the legal-notice page is canonical and dated. |
| Sector registers, for phone numbers | Authoritative for identity and licence status, near-zero yield for direct lines. Use to *confirm* identity, not to fill contact fields. |
| Search-engine snippets, as final evidence | Cached and truncated. Open the page or don't cite it. |
| Deep archive crawling (>3 years old) | Contact data decays fast; old pages generate confident wrong values. |

## Output format

Every key present on every record. Unproven → `""`, never omitted.

```json
{
  "entity_id": "", "legal_name": "", "city": "", "registry_url": "", "website": "",
  "role_email": "", "role_email_source": "", "role_email_confidence": "high|medium|low",
  "person_name": "", "person_role": "",
  "person_email": "", "person_email_source": "", "person_email_confidence": "high|medium|low",
  "phone": "", "phone_source": "", "phone_confidence": "high|medium|low",
  "collected_at": "", "delete_after": "", "notes": ""
}
```

Filled instance — note the empty `person_email` on a record that has everything else:

```json
{
  "entity_id": "ACME-0042", "legal_name": "Acme Widgets SARL", "city": "Region-01",
  "registry_url": "https://register.example.gov/entity/ACME-0042",
  "website": "https://acme-widgets.example",
  "role_email": "contact@acme-widgets.example", "role_email_source": "https://acme-widgets.example/legal-notice", "role_email_confidence": "high",
  "person_name": "A. Doe", "person_role": "Operations Director",
  "person_email": "", "person_email_source": "", "person_email_confidence": "",
  "phone": "+00 0 00 00 00 00", "phone_source": "https://acme-widgets.example/contact", "phone_confidence": "high",
  "collected_at": "2026-01-15", "delete_after": "2027-01-15",
  "notes": "Name from roster page; no nominative address published. Role email is the reachable channel."
}
```

Ship `deliverable.json` (purged and suppression-filtered), never `merged.json`, and alongside it a one-page method sheet: purpose, sources consulted, fill rate per field, retention date, opt-out channel. The base without the method sheet is not a deliverable.

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| Fill rate on `person_email` looks "too low" | The sector genuinely does not publish nominative addresses | Report it. Pivot to `role_email` — and prove it like any other field. Do not permute. |
| Two people, same name, same sector | Homonym crossing entity boundaries | Resolve inside the entity: registration number + city + role. Unresolved → drop both. |
| Every guessed address on a domain "validates" | Catch-all MX accepts everything | Treat validation as no signal; require a citable page. |
| Numbers found but wrong format/type | Switchboard promoted into a personal field | Keep line types in separate fields. Never merge them. |
| Registry entity count ≫ enriched rows | Fan-out silently dropped entities | Diff the entity list against the returned files; re-run only the missing IDs. |
| Proof gate passes on an empty run | Glob matched nothing; empty output = your PASS signal | Gate on the count of files read. Zero read → ABORT. |
| Merge check always passes | It compares two values derived from the same group key | Compare against the raw-name count. See Trap C. |
| Merge crashes and `merged.json` is 0 bytes | A record omitted a schema key; the shell truncated on redirect | Require present-but-empty fields; write to a temp file, then `mv`. |
| Someone who opted out got contacted again | Raw-string match, nominative-only filter, or list inside a run directory | All three are fail-open. Normalise both sides, test every email field, keep the list at `${RUNS_ROOT}`. |
| `purged 0` on every run | Purge pointed at the current `${WORK_DIR}` | It can only see rows you just collected. Iterate `${RUNS_ROOT}/*/`. |
| A page blocks automated access | The site does not consent to collection | Out of scope. Drop the entity, log the reason, move on. |

## Scope

**This skill ONLY:** ships a method — invariants, decision tables, thresholds, and the traps the gates fall into; you implement and test the gates. It reads publicly published pages and official registers; maps entities before people; attaches a source URL and a confidence to every value; leaves unproven fields empty; collects only what the declared purpose needs; stamps a deletion date and purges past it across every run directory; filters the suppression list before every delivery; writes to a local file and nothing else.

**This skill NEVER:** guesses or permutes an address into a deliverable; infers a person from an entity record; touches breach dumps, paywalled or logged-in content; collects without a written purpose and a legal basis; keeps data past its retention date; **sends, uploads, or pushes anything to a network destination** — the outbound channel is the operator's, and it must carry sender identity and a working opt-out before this base reaches it; evades a ToS restriction, a rate limit, or any anti-automation control — when a source declines automated access, it is out of scope, and the run continues without it.

---
name: developer-talent-discovery
description: Find developers through Crawlora public GitHub user datasets and verify relevant repository and contribution evidence. Use for role-specific technical shortlists or open-source collaborator discovery with public profile freshness and capability limits preserved; excludes outreach.
---

# Developer talent discovery

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound requests by the requested scope and credit budget. Preserve
source IDs, URLs, source dates, and retrieval/crawl times separately.

Produce a role-specific shortlist supported by public technical work. Start
with required technologies, work examples, domain, optional geography, and
explicit availability criteria. A public GitHub profile is a sample of work,
not a complete CV or a verified measure of professional capability.

## Discover identities and validate work evidence

1. Discover dataset facet values before domain/company/location filters, then
   collect a bounded candidate set. `q` searches profile fields, not the full
   source code or a verified skill taxonomy. `active_90d`, location, company,
   and `hireable` are stored/profile-derived observations that may be stale.
2. Keep individuals, organizations, bots, and suspected automation separate.
   A suspected-automation flag is a dataset signal, not proof of misconduct.
   Followers, influence tiers, and rank scores are discovery signals, not skill
   or hiring scores. Avoid requiring popularity when the role needs technical fit.
3. Resolve returned `login` before stored item/live user routes. Inspect selected
   pinned/public repositories, repository details, languages, contributors, and
   public events as needed. Use exact owner/repo names rather than profile-name
   guesses. Forks, generated code, and a pinned project do not prove authorship.
4. Tie each criterion to visible contribution or repository evidence and dates.
   Repository language composition is not the developer's personal mastery;
   contributor totals and event volume do not establish code quality, role,
   seniority, or hours worked. A bounded events feed cannot prove inactivity.
5. Preserve dataset crawl time versus live observation time and profile-declared
   location/company. Dataset geocoding does not verify residence, timezone,
   work authorisation, or willingness to relocate. Public contact presence does
   not establish consent to outreach or current job availability.

```sh
scripts/crawlora.sh /datasets/github-users/facets facet=domains
scripts/crawlora.sh /datasets/github-users/search q="distributed systems" is_org=false is_bot=false page=1 page_size=10
scripts/crawlora.sh /github/search/repositories q="language:go distributed systems"
# Inspect returned candidate login and relevant owner/repo:
# scripts/crawlora.sh "/github/user/$LOGIN/pinned"
# scripts/crawlora.sh "/github/repo/$OWNER/$REPO/contributors"
```

## Deliver a qualified evidence shortlist

Return login/profile URL, requested-role criterion, repository/contribution
links, relevant observable work, dates, declared availability fields, and
unknowns needing a conversation or work assessment. Deduplicate logins while
keeping distinct people with similar names separate. Separate source statements,
your technical interpretation, and unverified fit assumptions. Do not infer
protected characteristics or personal circumstances from names, photos, or
locations, or treat absent public work as evidence of low ability.

Use the user's job-related criteria rather than an opaque popularity ranking.
Keep contact details to returned public professional channels relevant to the
request. Do not contact candidates, send recruiting messages, enrich private
information, or apply on their behalf without an explicit user request.

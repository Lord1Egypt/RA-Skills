---
name: chrome-extension-research
description: Compare Chrome extensions using Crawlora's live store listings and stored adoption, publisher, permission, and privacy history. Use for extension shortlists, market comparisons, or investigating observed changes; store disclosures alone do not establish runtime safety.
---

# Chrome extension research

Compare extensions against the requested features, adoption evidence, maintenance,
and access requirements. Separate observed store fields from developer claims and
conclusions that would require inspecting code or runtime behavior.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for
selected live Chrome Web Store and stored extension tools.

## Compare current listings and observed changes

1. Establish the user's feature requirements and comparison purpose. Discover
   candidates with `/datasets/chrome-extensions/search`, using
   `item_type=extension` and `status=active` for current extensions. The dataset
   also includes themes, legacy apps, and unknown types; do not mix them silently.
   Discover category/filter values through dataset facets or live
   `/chromewebstore/categories`, keeping their taxonomies distinct.
2. Resolve the exact 32-character store ID, developer identity, and canonical URL.
   Refresh selected candidates through `/chromewebstore/item?id=...`; search and
   similar-item results aid discovery but do not establish equivalent functionality.
3. Retrieve `/datasets/chrome-extensions/items/{id}` and `/history/{id}` under
   the same dataset prefix. History is chronological and **change-only**, with
   optional `from`/`to` dates and `limit` up to 1000. Missing calendar days are
   not zero users or evidence that the extension was checked and unchanged.
4. Inspect recent change observations with `/datasets/chrome-extensions/changes`
   and optional `change_type`. Attribute a change to its observation time, not
   an exact transfer or release date. A changed developer label is not by itself
   proof of ownership transfer; compare identity and website evidence.
5. For access/privacy comparisons, use `/chromewebstore/permissions` and
   `/chromewebstore/privacy` with the same ID. Distinguish required from optional
   API permissions and required from optional host permissions. A declaration
   is not proof that every permission is currently granted or used; a privacy
   statement is a developer disclosure, not an independent audit.
6. Read a bounded live review sample, preserving dates, reviewed versions, and
   collection filters. Tie claimed feature gaps to specific evidence. Separate
   a sampled complaint from population prevalence and distinguish publisher
   identity fields from a verified business relationship.

```sh
scripts/crawlora.sh /datasets/chrome-extensions/search \
  q="tab manager" item_type=extension status=active page_size=5
# Resolve a returned ID before reading its live item, permissions, or history.
```

## Output and interpretation

Return a comparison with store ID/link, verified feature evidence, dated user and
rating counts, current version, observed changes, access requirements, disclosures,
review themes, and missing evidence. Use [Chrome's permission definitions](https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions)
when explaining the access fields.

- Store user counts are adoption indicators, not revenue, active usage, or exact
  install/uninstall flows. Dataset trending measures observed movement over its
  available interval; compare matching observation windows.
- Broad permissions, removal, or publisher changes can justify investigation;
  they do not independently prove malware. Low permissions or high ratings do
  not independently prove safety. Do not install an extension merely to research it.
- Dataset pages max at 100 with a 10,000-result window. Bound enrichments to the
  shortlist and stop at no progress or source end. Back off on `429`, retry a
  transient `5xx` once, stop on `401`/`403`, and
  check application `code`. Keep failed refreshes labeled as stored observations.

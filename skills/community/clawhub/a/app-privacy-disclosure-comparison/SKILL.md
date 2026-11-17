---
name: app-privacy-disclosure-comparison
description: Compare public App Store privacy labels, Google Play data-safety declarations, and listed Android permissions through Crawlora. Use for an app shortlist or disclosure matrix with publisher/app identity, taxonomy, market, missing data, and runtime-verification limits preserved.
---

# App privacy disclosure comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Compare what selected mobile apps publicly disclose, for the user's requested
data categories or access concerns. Establish platforms, app set, storefronts,
language, use case, and any specific requirements before interpreting fields.

## Resolve apps and collect comparable declarations

1. Resolve iOS numeric track IDs and Android package IDs through their own search
   and detail routes. Match publisher, official domain, title, and app purpose
   before treating two platforms as one product. Same-name apps, clones, and
   separate business/consumer editions remain separate identities.
2. Fetch App Store privacy cards for the selected numeric ID and storefront/lang.
   Fetch Google Play data safety and permissions for the package ID using only
   their documented parameters. Data safety exposes `lang` but no `country`
   parameter: do not pretend a country set on another route scopes that disclosure.
3. Keep declaration categories/purposes and permission names/groupings in their
   original taxonomies. Apple tracking/linked/not-linked labels and Android
   collected/shared labels are not equivalent definitions. Maintain an explicit
   mapping with uncertain or unmapped fields rather than a single count score.
4. Record platform, app/publisher ID, available version/date, storefront/language,
   source URL, and retrieval time for each surface. These responses are current
   listings, not a guaranteed historical disclosure version. Missing or empty
   content is unknown/unavailable unless the source explicitly states none.

```sh
scripts/crawlora.sh /appstore/search term="note taking" country=us
scripts/crawlora.sh /googleplay/search term="note taking" country=us lang=en
# Use returned platform-specific IDs before requesting disclosures:
# scripts/crawlora.sh "/appstore/privacy/$TRACK_ID" country=us
# scripts/crawlora.sh /googleplay/datasafety app_id="$PACKAGE_ID" lang=en
# scripts/crawlora.sh /googleplay/permissions app_id="$PACKAGE_ID" country=us lang=en
```

## Compare evidence and state what remains unverified

Return an app-by-category/purpose/access matrix with declared, explicitly-not-
declared, and unknown states, plus the original field and source/time behind
any mapping. Separate developer declarations, store-presented fields, and your
interpretation. Optional collection, purpose, linking, and sharing context matter;
a category count alone does not establish the amount or sensitivity of actual data.

Listed permissions do not prove those permissions are granted, exercised, or
abused on the user's device. A data-safety label is not runtime traffic analysis,
an independent audit, a compliance determination, or a malware finding. Do not
claim low permissions prove safety or high ratings validate privacy. Resolve
conflicts through attributed evidence and questions for further testing.
A comparison does not authorise installing apps, submitting packages, changing
permissions, accessing accounts, or sending user/device data to an app.

# JSON-LD Templates

Structured data templates for checklist items 2 and 4 in `SKILL.md`. All templates use
`schema.org` vocabulary and are meant to be injected as a single `<script
type="application/ld+json">` block via Ghost code injection (see
`ghost-deployment.md`). Replace every placeholder value before use — none of these are
meant to ship with placeholder content still in them.

## Person schema

The primary template for a personal or single-owner brand site. Covers checklist item
2, and folds in checklist item 4 (organization completeness) via the `sameAs` array
rather than a separate `Organization` block.

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Full Name",
  "url": "https://yourdomain.com",
  "description": "One or two sentences describing who this person is and what they do.",
  "image": "https://yourdomain.com/path-to-headshot.jpg",
  "jobTitle": "Role or title, if relevant",
  "sameAs": [
    "https://twitter.com/yourhandle",
    "https://www.linkedin.com/in/yourprofile",
    "https://github.com/yourusername",
    "https://another-publication.com/author/yourname"
  ]
}
```

Field notes:

- `name`, `url`, `description`, and `sameAs` are the required fields per the checklist
  — treat `image` and `jobTitle` as optional enrichment, not blockers.
- `sameAs` should only list URLs that independently confirm the identity — profile
  pages, bylines, verified accounts. A link to a page that doesn't mention the person
  by name doesn't strengthen this and shouldn't be included.
- Do not add `contactPoint` or `address` to a Person schema for a personal site —
  those are Organization-type fields; see checklist item 4 in `SKILL.md`. Adding them
  without real, current data produces bad structured data, which actively hurts more
  than omitting the field.

## Organization schema

Use only when the site represents an actual business entity with its own identity
separate from an individual owner — a company, an agency, a product with its own brand.
For a personal or single-owner brand site, do not use this template; extend the Person
schema's `sameAs` array instead, per checklist item 4.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Organization Name",
  "url": "https://yourdomain.com",
  "logo": "https://yourdomain.com/path-to-logo.png",
  "description": "One or two sentences describing what this organization does.",
  "sameAs": [
    "https://twitter.com/yourorg",
    "https://www.linkedin.com/company/yourorg",
    "https://github.com/yourorg"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "contact@yourdomain.com",
    "contactType": "customer support"
  }
}
```

Field notes:

- `contactPoint` and `address` are appropriate here — this is the case they're meant
  for, unlike the Person schema.
- Only include `contactPoint` if the email or channel listed is actually monitored.
  A structured-data contact point that goes nowhere is worse for trust than omitting
  it.

## SoftwareApplication schema

For a product or tool site — use in addition to (not instead of) a Person or
Organization schema identifying who built it.

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Product Name",
  "url": "https://yourdomain.com",
  "applicationCategory": "e.g., DeveloperApplication, BusinessApplication",
  "operatingSystem": "e.g., Web, iOS, Cross-platform",
  "description": "One or two sentences describing what the product does.",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
```

Field notes:

- `applicationCategory` and `operatingSystem` should use schema.org's recognized
  values rather than free text where possible — check the validator (below) for
  warnings if unsure.
- Only include `offers` if the product has a fixed, statable price (including free —
  `"price": "0"` is valid). Omit the block entirely for variable or quote-based
  pricing rather than guessing a number.

## Validation

Before treating any of these as done, validate the rendered output — not the template,
the actual live page:

- **Google Rich Results Test** — `https://search.google.com/test/rich-results` — paste
  the live URL. Confirms both that the structured data parses and that Google
  recognizes the type.
- **Schema.org Validator** — `https://validator.schema.org/` — paste the live URL or
  the raw JSON-LD. Broader vocabulary coverage than the Rich Results Test; use this one
  for types the Rich Results Test doesn't specifically support (e.g., SoftwareApplication
  in some configurations).

Run both against the live URL after injection (not against the template in isolation)
as part of Gate 4's verification step — a template that's syntactically valid can still
fail once it's actually embedded in the page if the surrounding injection breaks the
script tag or produces duplicate `@context` blocks.

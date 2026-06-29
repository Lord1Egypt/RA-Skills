---
name: add-json-ld
description: Add JSON-LD structured data to a website to improve SEO, qualify pages for richer search result previews, and help LLM crawlers correctly identify and cite the site. Use this skill whenever the user mentions JSON-LD, schema.org, structured data, rich snippets, SEO metadata, knowledge graph, or wants to make a personal site, blog, or portfolio more discoverable. Also trigger when the user wants metadata on specific page types — blog posts, profile/about pages, software or project showcases, collection or index pages — even if they don't say "JSON-LD" explicitly. Covers WebSite, WebPage, Person, ProfilePage, CollectionPage, SoftwareApplication, BreadcrumbList, Blog, and BlogPosting nodes.
---

# Add JSON-LD to a Site

JSON-LD (JSON Linked Data) is structured data that lives in a `<script type="application/ld+json">` tag in the page's `<head>`. Browsers ignore it; crawlers like Googlebot and LLM scrapers parse it to understand the page. Good JSON-LD earns richer link previews, helps search engines label the site correctly, and increasingly determines whether LLMs cite the site as a source.

This skill walks through adding JSON-LD to a personal site, blog, or portfolio. Most of the value comes from picking the right *combination* of nodes per page and linking them correctly with `@id` — copying templates blindly without understanding the linking model produces JSON-LD that crawlers can't fully use.

## How JSON-LD is structured

Every page's JSON-LD block has the same outer shape:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "...", "@id": "...", ... },
    { "@type": "...", "@id": "...", ... }
  ]
}
</script>
```

- `@context: "https://schema.org"` tells crawlers which vocabulary is in use. Schema.org defines every valid `@type` and property.
- `@graph` is an array of nodes describing the page and its entities.
- Each node has an `@type` (what it is), an `@id` (unique identifier), and properties.

**The `@id` convention is load-bearing.** IDs are URLs with a hash fragment that uniquely identifies the node — e.g. `https://example.com/#website`, `https://example.com/#person`, `https://example.com/blog/post-slug/#blogposting`. Two things rely on this:

1. **Within a page**, nodes reference each other by `@id` to build relationships: a `BlogPosting` says `"author": { "@id": "https://example.com/#person" }`, and the `Person` node with that `@id` is in the same `@graph`.
2. **Across pages**, crawlers (Googlebot and friends) merge properties of nodes that share an `@id`. So the `Person` node only needs full detail on one canonical page — other pages can reference `https://example.com/#person` and the crawler will stitch the data together.

LLM scrapers usually read one page at a time and don't merge, so important nodes (especially `Person`) should be fully described on every page where they matter, not just the canonical one. The slim/full distinction below addresses this.

## Workflow

When the user asks for JSON-LD help, work through these steps:

### 1. Figure out what kind of site and what pages exist

Ask (or infer from context) what type of site it is — personal site, blog, portfolio, business site — and what pages need JSON-LD. Common page types:

- **Root / home page** — usually doubles as an "about me" page on personal sites
- **About page** — if separate from root
- **Blog index** — lists all posts
- **Blog post** — individual article
- **Project / software showcase** — page describing one or more apps, libraries, games
- **Collection page** — any page that is primarily a list (e.g. `/links/`, `/elsewhere/`, `/projects/`)

Also confirm the site's canonical domain and whether the user has profiles elsewhere (GitHub, LinkedIn, Mastodon, etc.) — those go in `Person.sameAs` and meaningfully help disambiguation.

### 2. Decide which nodes each page needs

Use this matrix as a starting point.

| Page type        | Nodes to include                                                              |
|------------------|-------------------------------------------------------------------------------|
| Root (about-me)  | `WebSite` (full), `Person`, `ProfilePage`                                     |
| About (separate) | `WebSite` (slim), `Person`, `ProfilePage`, `BreadcrumbList`                   |
| Blog index       | `WebSite` (slim), `Person`, `WebPage`, `Blog`, `BreadcrumbList`               |
| Blog post        | `WebSite` (slim), `Person`, `WebPage`, `BlogPosting`, `BreadcrumbList`        |
| Project showcase | `WebSite` (slim), `Person`, `WebPage`, `SoftwareApplication`(s), `BreadcrumbList` |
| Collection page  | `WebSite` (slim), `Person`, `CollectionPage`, `BreadcrumbList`                |

Two rules underlie this matrix:

- **`Person` goes on every page.** Google uses it as a content quality signal, and LLM crawlers use it to decide who to cite. Since LLM scrapers don't merge nodes across pages, include the full `Person` on every page, not just the root.
- **`WebSite` goes on every page too, but slim on non-root pages.** The root page should have the full version (description, image, publisher, alternateName). Other pages just need the slim version so single-page crawlers correctly identify the site's name and domain.

`BreadcrumbList` is optional but useful — it controls how the page's path is displayed in search results. Skip it on the root page; include it elsewhere unless the site already has very short URLs.

### 3. Generate the JSON-LD

For each node:

1. Use the correct schema.org type and properties.
2. Replace placeholder URLs, names, and IDs with the user's actual values.
3. Wire up the `@id` references between nodes — e.g. a `BlogPosting`'s `author` should point at the `@id` of the `Person` node in the same `@graph`.
4. Assemble all nodes for the page into a single `@graph` array inside one `<script type="application/ld+json">` block.

If the user provides a real example page (URL, content, dates, image paths), use their real values rather than placeholders. Concrete output is much more useful than a fill-in-the-blank template.

### 4. Where to place it in the HTML

The script tag goes inside the `<head>` element. Order within `<head>` doesn't matter for crawlers. If the site has a build step or a templating system, put the JSON-LD in the shared layout/template so each page type gets the right nodes automatically.

For static sites without a build step, even just adding `WebSite` + `Person` + `ProfilePage` to the root `index.html` is a meaningful improvement — start there if the user is overwhelmed.

## Important details and best practices

**Use the same `@id` for `Person` and `WebSite` across the entire site.** This is what lets Googlebot merge them into a single knowledge-graph entity. Pick the canonical form once (`https://example.com/#person`, `https://example.com/#website`) and reuse it verbatim on every page.

**Fill out `Person.sameAs` thoroughly.** Each link to another profile (GitHub, LinkedIn, Mastodon, Twitter/X, ORCID, Google Scholar, Wikipedia, etc.) helps crawlers disambiguate, especially if the user has a common name. If the user has a Google Knowledge Graph ID, include it as `https://www.google.com/search?kgmid=/g/...`.

**For `BlogPosting`, mirror the OG image.** The `image` property should point at the same image used for OpenGraph previews — that way social shares, search results, and structured data all match. Use dimensions 1200×630 unless the site has chosen otherwise.

**`publisher` can be a `Person` on a personal site.** Older Google docs required `Organization` for `publisher` on `Blog` and `BlogPosting`. That's been relaxed — `Person` is now valid and is more accurate for personal sites. Don't invent a fake organization just to fill the field.

**Always include `offers` on `SoftwareApplication`, even for FOSS.** Set `price: 0` and pick a `priceCurrency`. Google requires this field to render rich results for software.

**`dateCreated` / `dateModified` are freshness signals.** Include them when the site already tracks these dates. Don't fabricate them — outdated or wrong dates hurt more than missing ones.

**Pick the most specific `@type` available.** `SoftwareApplication` has subtypes `MobileApplication`, `WebApplication`, and `VideoGame` — use them when they fit. Similarly, `WebPage` has subtypes like `ProfilePage`, `CollectionPage`, `ContactPage`, `FAQPage`, `AboutPage`. More specific types give crawlers more to work with.

**Watch out for `BreadcrumbList` on the current page.** The `breadcrumb` property on `WebPage` (or its subtypes) should reference the `BreadcrumbList` `@id` for *that same page* — not a generic one. Each page needs its own `BreadcrumbList` with its own `@id`.

## Validating the output

After generating the JSON-LD, recommend the user validate it:

- **Google's Rich Results Test**: `https://search.google.com/test/rich-results` — checks for errors and shows which rich-result features the page qualifies for.
- **Schema.org Validator**: `https://validator.schema.org/` — strictly validates against the schema.org vocabulary without Google's opinionated requirements.

Both accept either a URL or pasted code. Run the output through at least one before considering the job done.

## What's out of scope

Schema.org defines many more types than this skill covers (`Recipe`, `Event`, `Product`, `LocalBusiness`, `Course`, `JobPosting`, `Review`, and so on). This skill focuses on the nodes that matter for personal sites, blogs, and portfolios. If the user needs JSON-LD for e-commerce, events, or other specialized contexts, point them at `https://schema.org` and `https://developers.google.com/search/docs/appearance/structured-data/search-gallery` for the relevant type-specific guidance.

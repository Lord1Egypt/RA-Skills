# Technical SEO Audit Checklist

## 1. Keyword Placement Audit

For every page on the site, verify the target keyword appears in:
- [ ] URL slug
- [ ] Title tag (within first 60 characters)
- [ ] H1 heading (only one H1 per page)
- [ ] Meta description (within 155 characters)
- [ ] First paragraph of body content
- [ ] At least one H2 subheading
- [ ] Image alt text (at least one image)

**How to audit:** Fetch sitemap.xml, then crawl each page checking for keyword presence in each element. Flag any page missing the keyword in 2+ locations.

## 2. Schema Markup Audit

Check each page type for appropriate JSON-LD schema:

| Page Type | Required Schema |
|---|---|
| Homepage | LocalBusiness (with address, phone, email, socialProfiles, geo, openingHours) |
| Service pages | Service schema + BreadcrumbList |
| Location/area pages | LocalBusiness with areaServed + BreadcrumbList |
| Blog posts | Article schema with author, datePublished, dateModified |
| About page | Organization or Person schema |
| Contact page | LocalBusiness with contactPoint |
| FAQ sections | FAQPage schema (on any page with Q&A content) |
| Reviews page | AggregateRating schema |

**How to audit:** Fetch each page, check for `<script type="application/ld+json">` blocks. Validate at https://validator.schema.org/ or https://search.google.com/test/rich-results.

## 3. Core Web Vitals

Check mobile performance scores:
- **LCP (Largest Contentful Paint):** Target < 2.5 seconds
- **INP (Interaction to Next Paint):** Target < 200 milliseconds
- **CLS (Cumulative Layout Shift):** Target < 0.1

**Fix stack for WordPress:** Cloudflare CDN + WP Rocket + ShortPixel image compression
**Fix stack for other CMS:** Cloudflare CDN + lazy loading + image optimization + minimize JS

## 4. Mobile Interstitials

Check for pop-ups that block content on mobile devices. Google has penalized these since 2016. Common offenders:
- Email signup modals that cover the full screen
- Cookie consent banners that are oversized
- Chat widgets that expand over content
- "Download our app" interstitials

**Fix:** Replace with small slide-in banners or bottom bars that don't block content.

## 5. Trust Signals Audit

Check for presence of:
- [ ] Business name, address, phone in website footer
- [ ] Detailed About page with owner bio, team photos, company history
- [ ] Contact page with physical address, phone, email, map embed
- [ ] Real team/staff photos (not stock)
- [ ] Client testimonials or reviews on-site
- [ ] "Featured in" or certification badges
- [ ] Privacy policy and terms of service pages
- [ ] SSL certificate (HTTPS)

## 6. Sitemap & Indexation Audit

1. Fetch sitemap.xml — count total URLs
2. Compare to Google Search Console submitted page count
3. Compare to GSC indexed page count
4. If submitted > sitemap: Google is finding extra URLs (parameter pages, tags, pagination)
5. If indexed << submitted: quality or crawl budget problem

**Indexation ratio targets:**
- Healthy site: 80-95% of submitted pages indexed
- Needs work: 50-80% indexed
- Serious problem: < 50% indexed

## 7. Internal Linking Audit

### Entity Mapping
For each page, identify what entities it relates to:
- **People** (owner, technicians, staff)
- **Services** (AC repair, furnace install, etc.)
- **Locations** (cities, neighborhoods)
- **Topics** (energy efficiency, maintenance tips, etc.)

### Link Rules
- Every blog post should link to 2-3 relevant service pages
- Every service page should link to 1-2 related blog posts
- Every location page should link to all relevant service pages
- Use descriptive anchor text with keywords (not "click here")
- Surrounding paragraph context should be relevant to the linked page
- Don't link everything to the homepage or money page

### What NOT to Do
- Don't use plugins that auto-generate hundreds of random links
- Don't stuff footer with links to every city page
- Don't use generic anchor text ("learn more", "click here")
- Don't link from irrelevant context

## 8. Thin Content Identification

For each page, evaluate:
- **Word count:** Service pages need 600-800+ words; blog posts need 800-1,500+
- **Uniqueness:** Are location pages just template with city name swapped?
- **Overlap:** Do multiple blog posts cover the same topic?
- **Value:** Does the page answer a real question or serve a real need?

### Action per page:
1. **Improve** — add depth, unique local content, better optimization
2. **Noindex** — keep for users but remove from search
3. **Delete & 301 redirect** — merge into a better page
4. **Leave as-is** — page is strong enough

### Common Thin Content Patterns in Local Service Sites
- 15+ city pages with identical content except city name
- Blog posts under 300 words
- Multiple blog posts about the same topic from different angles
- Auto-generated tag/category archive pages
- Empty or near-empty pages (placeholders, coming soon)

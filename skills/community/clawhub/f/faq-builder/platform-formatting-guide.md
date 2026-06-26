# Platform Formatting Guide for FAQ Sections

## Amazon

### A+ Content FAQ Module
- Maximum answers per FAQ module: 6–8 (recommended)
- Character limit per answer: ~1,000 characters
- Questions should include high-search keywords naturally
- Images can accompany answers in premium A+ Content
- FAQs display in an accordion format — question first, answer on expand

### Amazon Customer Q&A (Separate from A+ Content)
- Sellers can answer any customer question in the Q&A section
- Responses show as "Seller" answer — respond to all questions within 24 hours
- High-volume Q&As surface to top of listing (Amazon ranks by helpfulness votes)
- Best practice: answer competitor questions in your category to build authority

### Keyword Strategy for Amazon FAQ
- Include your primary ASIN keyword in 2–3 answers
- Include backend search terms that don't fit naturally in bullet points
- Avoid keyword stuffing — Amazon's algorithm reads FAQs for relevance signals

---

## Shopify

### FAQ Placement Options
1. **Product page FAQ section** — highest-converting placement for pre-purchase questions
2. **Dedicated /faq page** — for brand-level questions (returns, shipping, company info)
3. **Modal / popup** — triggered on exit intent or add-to-cart click (advanced)

### Recommended Apps
- **HelpCenter** — Native Shopify FAQ with accordion UI, no coding required
- **Acecart FAQ** — Lightweight, fast-loading
- **Yotpo** — Integrates FAQ with reviews for social proof combination
- **Custom Liquid section** — Full control; use `<details>` HTML for native accordion

### Schema Markup for Shopify (FAQPage)
Add to your product page or FAQ page template:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Does this product come with a warranty?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, all products include a 1-year manufacturer warranty covering defects in materials and workmanship."
      }
    }
  ]
}
```

Schema markup enables Google to show FAQ accordion directly in search results (rich results), expanding your SERP presence without additional ranking effort.

### Character Guidance
- No hard limit, but answers longer than 200 words lose readability
- Aim for 50–150 words per answer on product pages
- Break long answers into bullet points rather than paragraphs

---

## TikTok Shop

### FAQ Behavior on TikTok Shop
- Product page FAQs appear in the "Details" tab below the listing
- Buyers on TikTok skim — prioritize short, direct answers
- Return policy and shipping time are the top 2 buyer concerns on TikTok Shop

### Style Guide for TikTok Shop
- Maximum 3 sentences per answer
- Use casual, direct language matching TikTok's tone
- Lead with the direct answer, then add brief context
- Avoid corporate-speak or legal language

### Priority FAQ Order for TikTok Shop
1. Shipping time and carrier
2. Return / refund policy
3. Size / fit (if apparel)
4. Authenticity / brand verification
5. Bundle contents / what's in the package

---

## WooCommerce

### FAQ Implementation Options
- **WPForms FAQ Block** — Gutenberg block, schema enabled
- **Accordion FAQ plugin** — Multiple free options; ensure FAQPage schema output
- **Custom post type** — For stores with large FAQ libraries needing search

### WooCommerce SEO Notes
- Install RankMath or Yoast and use their FAQ block — both output FAQPage schema automatically
- Check Google Search Console after adding schema to confirm rich result eligibility
- FAQ rich results appear within 1–4 weeks of Google recrawling the page

---

## General Formatting Best Practices

| Principle | Do | Don't |
|---|---|---|
| Lead with the answer | "Yes, it is compatible with iOS 16+" | "That's a great question. This product is designed with..." |
| Use specific numbers | "Ships in 3–5 business days" | "Ships quickly" |
| Name the concern | "If you're worried about sizing..." | Ignore the underlying anxiety |
| Action when needed | "Contact us at [email] for custom orders" | Leave the buyer stuck |
| Consistent tone | Match brand voice across all answers | Mix formal and casual randomly |

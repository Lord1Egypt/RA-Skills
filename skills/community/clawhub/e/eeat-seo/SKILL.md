---
name: eeat-seo
version: 1.0.0
description: |
  E-E-A-T SEO Optimization Guide — How to build Experience, Expertise, Authoritativeness, and Trustworthiness signals for AI search engines and Google. Covers E-E-A-T signals for ChatGPT, Perplexity, and Google, author schema optimization, content credibility, internal/external citations, and E-E-A-T audit framework.

  Keywords: e-e-a-t, eeate seo, eeat, experience expertise authoritativeness trustworthiness, google e-e-a-t, ai search e-e-a-t, content credibility, author authority, trust signals seo, seo trust, expertise seo, chatbot seo eeat, perplexity eeat, chatgpt eeat
---

# E-E-A-T SEO Optimization Guide

> Build unshakeable authority signals for AI and Google search
> by Iris (@gingiris) — AFFiNE former COO, 30+ PH #1 launches

---

## TL;DR

- **E-E-A-T** = Experience + Expertise + Authoritativeness + Trustworthiness
- AI engines (ChatGPT, Perplexity) use E-E-A-T to decide what to cite
- **Named authors** with credentials are the #1 E-E-A-T signal
- **Specific, verifiable claims** beat vague statements
- **External citations** from authoritative sources = your authority
- First-hand experience content gets cited 3x more than generic content

---

## The E-E-A-T Framework

### E — Experience
**Did the author actually do this?**

Signals:
- First-person narrative: "When I launched X..."
- Specific dates and places: "August 2022, in Berlin..."
- Actionable lessons from doing: "I tried X. Here's what happened."
- Screenshots, photos, data from your own work

Content style:
```markdown
We ran this campaign in Q3 2025 with a $5,000 budget.
Our conversion rate dropped from 4.2% to 2.8% in week 2
after Google updated their core algorithm. Here's exactly 
what we did to recover — and the specific A/B test data.
```

### E — Expertise
**Does the author know this topic deeply?**

Signals:
- Author bio with relevant credentials
- Consistent coverage of the topic over time
- Technical depth when needed
- Certifications or formal training (where relevant)

```markdown
About the author: Sarah has managed $2M+ in ad spend 
across 50+ SaaS launches. She's certified in Google Ads 
and has been writing about growth since 2019.
```

### A — Authoritativeness
**Is the author recognized as a leader in this space?**

Signals:
- External sites citing your content
- Guest posts on authoritative publications
- LinkedIn endorsements or testimonials
- GitHub stars, open source contributions
- Podcast appearances, interviews

```markdown
This method was also covered in [TechCrunch](link),
[HackerNews](link), and recommended by [famous person](link).
```

### T — Trustworthiness
**Is the information accurate and safe to act on?**

Signals:
- Contact page, about page, clear identity
- Privacy policy, terms of service
- Verifiable claims with data sources
- Corrections or updates to old content
- Secure (HTTPS) site

---

## E-E-A-T Schema Markup

### Person Schema (Author)
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Author Name",
  "url": "https://author-website.com/about",
  "image": "https://author-website.com/photo.jpg",
  "sameAs": [
    "https://twitter.com/authorhandle",
    "https://linkedin.com/in/authorprofile",
    "https://github.com/authorhandle"
  ],
  "jobTitle": "Founder / Growth Consultant",
  "worksFor": {
    "@type": "Organization",
    "name": "Brand Name"
  }
}
```

### Organization Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Your Brand",
  "url": "https://yourbrand.com",
  "logo": "https://yourbrand.com/logo.png",
  "sameAs": [
    "https://twitter.com/brandhandle",
    "https://linkedin.com/company/brand"
  ]
}
```

### Article Schema (Complete)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://author-website.com/about"
  },
  "datePublished": "2026-04-10",
  "dateModified": "2026-04-10",
  "publisher": {
    "@type": "Organization",
    "name": "Your Brand",
    "logo": {
      "@type": "ImageObject",
      "url": "https://yourbrand.com/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://article-url.com"
  }
}
```

---

## E-E-A-T Audit Framework

### Audit Checklist

**Experience (E)**
- [ ] First-person experience mentioned in article?
- [ ] Specific dates, places, numbers used?
- [ ] Original data/screenshots from own work?
- [ ] Lessons from failures included?

**Expertise (E)**
- [ ] Author named and credentialed?
- [ ] Author bio page exists with topic expertise?
- [ ] Consistent topic coverage?
- [ ] Technical depth appropriate for topic?

**Authoritativeness (A)**
- [ ] Cited by external authoritative sites?
- [ ] LinkedIn profile optimized?
- [ ] GitHub profile (if dev topic)?
- [ ] Guest posts or interviews?

**Trustworthiness (T)**
- [ ] Contact page exists?
- [ ] HTTPS enabled?
- [ ] Privacy policy present?
- [ ] dateModified kept current?
- [ ] Claims are verifiable?

### E-E-A-T Score Calculation

| Dimension | Weight | Score (1-5) |
|-----------|--------|------------|
| Experience | 30% | × 0.30 |
| Expertise | 25% | × 0.25 |
| Authoritativeness | 25% | × 0.25 |
| Trustworthiness | 20% | × 0.20 |
| **Total** | 100% | **/5.0** |

Score ≥ 4.0: Strong E-E-A-T, likely cited by AI
Score 3.0-4.0: Average, improve weakest dimension
Score < 3.0: Critical gaps, AI unlikely to cite

---

## Prompt Templates

### Prompt: E-E-A-T Article Writer
```
Write an E-E-A-T-optimized article targeting: [keyword]

Experience layer:
- Open with first-person experience: "[When/Where] I [did X]..."
- Include specific numbers, dates, places from your experience
- Add "I tried this and here's what happened" sections

Expertise layer:
- Name the author with specific credentials in [topic]
- Show depth: don't just say "it's important", explain WHY
- Reference formal knowledge (courses, books, certifications)

Authoritativeness layer:
- Cite 3 authoritative external sources
- Link to your own related content (internal authority)
- Include social proof (mentions, testimonials)

Trustworthiness layer:
- Add datePublished AND dateModified to Article Schema
- Make every claim specific and verifiable
- Include About page link in author section

Output: Full article with complete schema markup (Person, Organization, Article).
```

### Prompt: E-E-A-T Audit
```
Audit [URL] for E-E-A-T optimization:

For each dimension (E-E-A-T), rate 1-5 and give:
- Current score
- 2 specific examples from the page
- 1 prioritized fix

Also output:
- Overall E-E-A-T score
- Weakest dimension
- Top 3 actions to improve in next sprint
```

---

## E-E-A-T for AI Search (ChatGPT, Perplexity)

AI engines weight E-E-A-T differently than Google:

| Signal | Google Weight | AI Search Weight |
|--------|--------------|-----------------|
| Backlinks | Very High | Medium |
| Named Author | Medium | **Very High** |
| Specific Numbers | Low | **Very High** |
| External Citations | Medium | **Very High** |
| Freshness | High | Medium-High |
| Founder Voice | Low | **Very High** |

**AI SEO = E-E-A-T × Specificity**

Generic content with strong backlinks won't get cited by AI.
Specific, experience-rich content with moderate backlinks will.

---

## Real Case Study

**From 0 to 50 AI citations in 60 days:**

1. Added author bio to every article (named, credentialed)
2. Restructured articles: direct answer first + key stats table
3. Added 3 external authoritative citations per article
4. Updated dateModified on all existing articles
5. Added FAQPage Schema to 20 key pages

Result: 
- ChatGPT started citing content for "[keyword]" queries
- Perplexity cited 23 times in first month
- Organic traffic increased 40% from AI search referrals

---

## Related Resources

**Free Playbooks (GitHub):**
- SEO & GEO Playbook: https://github.com/Gingiris/seo-geo-playbook
- Perplexity SEO: https://github.com/Gingiris/perplexity-seo
- ChatGPT SEO: https://github.com/Gingiris/chatgpt-seo
- Gingiris Launch: https://github.com/Gingiris/gingiris-launch
- Growth Tools: https://gingiris.github.io/growth-tools/

**Author**: Iris (@gingiris) — AFFiNE former COO, open source growth consultant

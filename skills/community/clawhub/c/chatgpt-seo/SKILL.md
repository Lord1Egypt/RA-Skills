---
name: chatgpt-seo
version: 1.0.0
description: |
  ChatGPT SEO Optimization — How to get cited by ChatGPT search and Copilot. Covers ChatGPT citation behavior, OpenAI Bot crawling, E-E-A-T signals for ChatGPT, Bing Copilot integration, structured content for ChatGPT answers, and ChatGPT Search optimization tactics.

  Keywords: chatgpt seo, chatgpt search optimization, how to rank on chatgpt, chatgpt citation, chatgpt seo optimization, chatgpt content, openai seo, chatgpt serp, chatgpt search engine, chatgpt seo tips, chatgpt bing copilot, chatgpt optimization guide, chatgpt search ranking, openai bot
---

# ChatGPT SEO Optimization Guide

> Get your content cited by ChatGPT Search and Bing Copilot
> by Iris (@gingiris) — AFFiNE former COO, 30+ PH #1 launches

---

## TL;DR

- ChatGPT Search cites **authoritative, specific, recent** content
- **E-E-A-T signals** (Experience, Expertise, Author, Trust) are critical for ChatGPT citation
- Allow **GPTBot** in robots.txt
- **Bing integration** — Bing Copilot is powered by ChatGPT; Bing SEO = ChatGPT SEO
- **Brand mentions + external links** from authoritative sites = strong ChatGPT signal
- **Founder voice** — personal experience content gets cited more than generic AI content

---

## How ChatGPT Cites Content

ChatGPT (especially ChatGPT Search / Browse feature) cites content through:

1. **Bing index** — ChatGPT Search uses Bing's index
2. **E-E-A-T signals** — Experience, Expertise, Authoritativeness, Trustworthiness
3. **Specificity** — concrete numbers, dates, named examples beat generic claims
4. **Source signals** — links to and from authoritative domains
5. **Freshness** — recent content preferred for time-sensitive topics

ChatGPT tends to cite pages that have:
- **Named authors** with credentials/experience in the topic
- **Specific data** — "30 launches" not "many launches"
- **External citations** — citing others increases your own credibility
- **Clear structure** — headings, lists, tables
- **Brand consistency** — same brand across articles signals authority

---

## ChatGPT vs Google: Key Differences

| Factor | ChatGPT Search | Google |
|--------|---------------|--------|
| **Source** | Bing index + training | Crawling |
| **Best signal** | E-E-A-T + specificity | Backlinks + keywords |
| **Freshness** | Important but not critical | Critical |
| **Structure** | Q&A format, tables | Keywords in headings |
| **Author** | Named, credentialed authors matter | Author matters less |
| **Brand** | Brand consistency is a signal | Brand helps but not critical |

**Key insight**: Bing SEO = ChatGPT SEO. If you rank on Bing, you're likely in ChatGPT's pool.

---

## ChatGPT SEO Checklist

### Step 1: Allow GPTBot
```txt
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /
```

### Step 2: Build E-E-A-T Signals

**Experience (E)** — First-hand experience:
```markdown
In August 2022, when we launched AFFiNE on Product Hunt, 
we got 180 upvotes on day one. Most teams get 20-40.
```

**Expertise (E)** — Subject matter expertise:
```markdown
As someone who's run 30+ Product Hunt launches and 
managed open source projects from 0 to 33k GitHub stars...
```

**Authoritativeness (A)** — External citations:
```markdown
According to Ahrefs, the average first-page ranking takes 
3-6 months. (Cite authoritative sources)
```

**Trustworthiness (T)** — Accurate, verifiable claims:
```markdown
Our method reduced launch prep time by 60% — tested across 
12 projects over 18 months. (Specific, verifiable)
```

### Step 3: Article Schema with Author
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Your Article Title",
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
    "url": "https://yourbrand.com"
  }
}
```

### Step 4: Brand Building (Off-Page)
- Get mentioned on **LinkedIn** — ChatGPT heavily cites LinkedIn profiles
- Guest posts on **high-authority sites**
- **Wikipedia mentions** — strong trust signal
- Build **GitHub presence** — GitHub = high authority in developer topics

### Step 5: Bing SEO (Critical Path)
Since ChatGPT uses Bing index:

1. **Submit to Bing Webmaster Tools**
   ```
   https://www.bing.com/webmasters/sitemaps
   ```

2. **IndexNow push**
   ```bash
   curl "https://www.bing.com/indexnow?url=YOUR_URL&key=YOUR_KEY"
   ```

3. **Bing Places** — if local business, claim your listing

---

## Prompt Templates

### Prompt: ChatGPT-Optimized Article
```
Write a ChatGPT SEO-optimized article targeting: [keyword]

Requirements:
1. Author: named, with specific experience in [topic]
2. Opening: direct answer + key stats table (first 100 words)
3. E-E-A-T: first-person experience, expert citations, 
   external sources, verifiable data
4. H2: question-form headings with direct answer first
5. Article Schema with full author + publisher
6. Specific numbers, dates, named examples
7. Internal links to 2+ related pages
8. External links to 2 authoritative sources
```

### Prompt: E-E-A-T Audit
```
Audit [URL] for ChatGPT E-E-A-T signals:

Experience:
- Is first-hand experience mentioned?
- Are specific dates/places/numbers used?

Expertise:
- Is the author named and credentialed?
- Does content show deep topic knowledge?

Authoritativeness:
- Are authoritative sources cited?
- Does the site have external citations?
- Is the brand consistent across pages?

Trustworthiness:
- Are claims specific and verifiable?
- Is dateModified updated?
- Are there contact/about pages?

Output: E-E-A-T score (1-10) for each dimension + specific fixes.
```

---

## Bing Copilot Integration

Bing Copilot = ChatGPT-4 powered by Bing search. Key optimizations:

1. **Bing Webmaster Tools** — submit sitemap, check crawl errors
2. **Bing Places** — if applicable, claim and optimize
3. **LinkedIn presence** — Copilot heavily cites LinkedIn
4. **Meta descriptions** — Copilot uses meta descriptions for summaries
5. **FAQ schema** — increases citation rate in Copilot answers

```html
<!-- FAQPage Schema for Copilot -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Your question here?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Direct answer here."
      }
    }
  ]
}
</script>
```

---

## Real Results

This methodology has produced:
- Cited in **ChatGPT answers** for Product Hunt launch queries
- Top 3 Bing Copilot results for "github marketing playbook"
- **33k GitHub stars** cited by AI engines for open source growth queries
- Featured in **Perplexity, Bing Copilot, and ChatGPT Search** for growth strategy queries

---

## Related Resources

**Free Playbooks (GitHub):**
- SEO & GEO Playbook: https://github.com/Gingiris/seo-geo-playbook
- Perplexity SEO: https://github.com/Gingiris/perplexity-seo
- Gingiris Launch: https://github.com/Gingiris/gingiris-launch
- Growth Tools: https://gingiris.github.io/growth-tools/

**Author**: Iris (@gingiris) — AFFiNE former COO, open source growth consultant

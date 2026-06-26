# Lead Sources by Industry

When a user picks their industry during onboarding, suggest these sources. Multiple industries can be combined.

## Funding / Startup News (works for most industries)
| Source | URL | Notes |
|--------|-----|-------|
| finsmes | finsmes.com | Daily funding announcements, global |
| Crunchbase News | news.crunchbase.com | Funding rounds, acquisitions |
| TechCrunch | techcrunch.com/category/startups | US-heavy, Series A+ |
| PR Newswire | prnewswire.com | Press releases, funding announcements |
| EU-Startups | eu-startups.com | European funding rounds |
| Tech in Asia | techinasia.com | APAC startup funding |
| UKTN | uktech.news | UK tech funding |
| Startup Daily | startupdaily.net | Australia/NZ startups |

## By Vertical

### SaaS / Software
- ProductHunt (new launches needing dev help)
- BetaList (pre-launch startups)
- Y Combinator company directory (ycombinator.com/companies)
- AngelList / Wellfound (wellfound.com)

### Fintech
- Fintech Global (fintechglobal.com)
- The Fintech Times (thefintechtimes.com)
- Finovate (finovate.com)

### Healthtech / Biotech
- MobiHealthNews (mobihealthnews.com)
- Fierce Healthcare (fiercehealthcare.com)
- Digital Health (digitalhealth.net)

### E-commerce / Retail
- Retail Dive (retaildive.com)
- Modern Retail (modernretail.co)
- eCommerce Magazine (ecommercemagazine.com)

### AI / ML
- AI News (artificialintelligence-news.com)
- VentureBeat AI (venturebeat.com/ai)
- The AI Journal (aijourn.com)

### Recruiting / HR Tech
- HR Tech Feed (hrtechfeed.com)
- Recruiting Daily (recruitingdaily.com)
- HR Dive (hrdive.com)

### Real Estate / Proptech
- Propmodo (propmodo.com)
- The Real Deal (therealdeal.com)
- CREtech (cretech.com)

### Climate / Clean Tech
- CleanTechnica (cleantechnica.com)
- GreenBiz (greenbiz.com)
- Climate Tech VC newsletter

### Education / EdTech
- EdSurge (edsurge.com)
- EdTech Magazine (edtechmagazine.com)

### Legal Tech
- Artificial Lawyer (artificiallawyer.com)
- Legaltech News (legaltechnews.com)

## Custom Sources

Users can add any URL as a source. The skill will attempt to:
1. Fetch the page and extract funding/company announcements
2. If blocked, use search fallback: `site:<domain>` with freshness filter
3. If the site has an RSS feed, prefer that (more reliable, rarely blocked)

## RSS Detection

For any source URL, try appending `/feed`, `/rss`, `/atom.xml`, or checking `<link rel="alternate" type="application/rss+xml">` in the HTML. RSS feeds bypass Cloudflare and are more structured.

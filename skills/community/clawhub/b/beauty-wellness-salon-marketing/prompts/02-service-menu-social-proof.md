# Prompt 2: Service Menu & Social Proof System

## Purpose
Generate website service page copy, membership/package copy, and an FTC-compliant social proof system — testimonial request emails, before/after captions, and FAQ with schema markup.

## Why FTC Compliance Matters
The FTC issued enforcement guidance in 2023 specifically targeting beauty businesses for non-compliant endorsements and before/after photos. Required disclosures include: "Results vary," material connections, and "typical results" language. Generic AI tools don't know this. This prompt does.

---

## The Prompt

```
You are a beauty industry copywriter and FTC compliance specialist. Generate complete service page copy and a social proof system for the business below.

BUSINESS DETAILS:
- Business name: [NAME]
- Business type: [hair salon / nail studio / med spa / massage / esthetician / day spa]
- Location: [CITY, STATE]
- Top 3 services with prices: [e.g., "Hydrafacial $175, Laser Hair Removal (legs) $299, Lash Extensions $185"]
- Full service list: [ALL SERVICES WITH PRICES]
- Target client: [DESCRIPTION]
- Differentiators: [e.g., "only med spa in Henderson using Hydrafacial Syndeo machine," "15 years experience," "all-organic products"]
- Owner name and credentials: [e.g., "Dr. Sarah Kim, board-certified NP"]

GENERATE THE FOLLOWING:

1. SERVICE PAGE COPY — TOP 3 SERVICES
   For each service, generate:
   a) Page headline (H1, 6-10 words, includes location keyword)
   b) Service description (200-250 words): what it is, how it works, what client feels during, expected results, who it's for, who it's NOT for
   c) Benefits list (5 bullets, outcome-focused, not feature-focused)
   d) "What to expect" section (3-step process: before → during → after)
   e) FAQ (3 questions specific to this service with answers)
   f) Primary target keyword and 3 secondary keywords (for meta description)
   g) Meta description (under 155 characters, includes location + service + benefit)

2. MEMBERSHIP / PACKAGE PAGE COPY
   - Page headline
   - 3-tier membership table:
     * Bronze tier: name + price + 3-4 perks
     * Silver tier: name + price + 5-6 perks (decoy tier — makes Gold look better)
     * Gold tier: name + price + 7-8 perks + best value badge
   - "Why Membership?" section (5 bullets)
   - FAQ section (4 questions: cancellation, pausing, guest privileges, value comparison)
   - CTA: "Book a Membership Consultation" or equivalent

3. FTC-COMPLIANT TESTIMONIAL REQUEST EMAILS
   Three templates — send at different milestones:

   Template A — Day 7 (after first visit):
   - Subject line
   - 150-word email: gratitude → specific service mentioned → ask for Google review → direct link placeholder
   - FTC note: "Genuine experiences only — please share what actually happened"

   Template B — Day 30 (rebooking milestone):
   - Subject line
   - 175-word email: check-in → mention of rebooking → ask for before/after photo testimonial
   - FTC disclosure language: "Results vary based on individual factors including skin type, age, and treatment frequency"

   Template C — 6-Month Transformation:
   - Subject line  
   - 200-word email: celebrate progress → transformation story ask → social media tag request
   - FTC required language: "Individual results may vary. [Name]'s experience reflects their specific treatment plan."

4. BEFORE / AFTER CAPTION TEMPLATES (5 templates)
   For each:
   - Caption (100-150 words): service, timeline, process, client experience
   - Required FTC disclosures embedded naturally (not as fine-print add-on):
     * "Results vary"
     * Treatment frequency and timeline
     * "Not a guarantee of results"
   - Hashtag line (10 targeted tags)
   - Note: Do NOT use "guaranteed results," "permanent results," or "eliminates" language

5. "WHY CHOOSE US" PAGE SECTION
   - H2 headline
   - 4-6 differentiator blocks (icon placeholder + headline + 2 sentences each)
   - Trust signals section: credentials, certifications, years in business, number of clients served
   - Closing paragraph + CTA

6. FAQ SECTION WITH JSON-LD SCHEMA MARKUP
   Generate 8 frequently asked questions specific to this business type, then output both:
   a) The readable FAQ (question + 2-3 sentence answer each)
   b) The complete JSON-LD structured data block ready to paste into <head>:
      {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [...]
      }
   Questions must include: pricing, pain/discomfort, results timeline, cancellation, qualifications, parking/location, first visit process, and contraindications (what disqualifies someone)
```

---

## Tips for Best Results

- Provide real prices — "affordable" and "competitive" produce weak copy
- Include credentials — "NP with 12 years dermatology experience" produces more authoritative copy than "experienced provider"
- The more specific the differentiator, the stronger the "Why Choose Us" section

## FTC Quick Reference

Required for beauty testimonials and before/after content:
- "Results may vary" or "Individual results may vary"
- Timeline disclosure ("after 3 treatments over 6 weeks")
- Material connection disclosure if client received free/discounted service ("Complimentary service provided in exchange for honest review")
- No superlatives without substantiation ("best," "most effective," "proven to eliminate")

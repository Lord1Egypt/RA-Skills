# GEO + Conversion Optimization Playbook

This playbook supports the `geo-conversion-optimizer` skill. It
provides patterns and checklists for creating and refining content
that both:

- Performs well for GEO and AI citations.
- Drives meaningful business conversions (sign-ups, leads, purchases,
  bookings, etc.).

Use these patterns as defaults and adapt them to the specific product,
audience, and constraints of the user.

---

## 1. Core principles

1. **Start from the business outcome.**  
   GEO and AI visibility are a means, not an end. Clarify the primary
   and secondary conversion goals before touching structure or copy.

2. **Serve humans and AIs simultaneously.**  
   Good structure, clarity, and explicit answers help both human
   decision-making and AI understanding. Avoid writing “for bots”
   at the expense of human trust and clarity.

3. **Make trade-offs explicit.**  
   When a change risks harming conversion to improve GEO, or vice versa,
   call it out and suggest mitigations or experiments instead of hiding
   the tension.

4. **Design for journeys, not just pages.**  
   GEO may bring users into the site at many entry points. Clarify
   where each page sits in the funnel and which next steps it should
   drive.

---

## 2. Common page types and patterns

### 2.1 SaaS / product landing pages

**Goal:** Drive sign-ups, trials, demos, or qualified leads.

**Typical sections:**
- Hero (value proposition + primary CTA).
- Problem / pain section.
- Solution overview and key benefits.
- Social proof (logos, testimonials, metrics).
- Feature or capability breakdown.
- Pricing or plan overview (if appropriate).
- FAQs and objection handling.
- Supporting resources (case studies, guides).

**GEO considerations:**
- Use clear, descriptive headings that include the product category
  or job to be done.
- Make entities and relationships explicit: who it is for, what it does,
  which problems it solves.
- Include a focused FAQ block aligned with real queries and objections.

**Conversion considerations:**
- Ensure the primary CTA is visible and compelling above the fold.
- Use plain language that reflects how customers describe their problems.
- Provide enough proof (logos, quotes, numbers) for credibility without
  overwhelming the page.

### 2.2 Product detail pages (PDPs)

**Goal:** Drive add-to-cart and purchases.

**Typical sections:**
- Hero (product name, key benefit, price, primary CTA).
- Gallery or imagery.
- Core benefits and use cases.
- Detailed specs and technical details.
- Social proof (reviews, ratings, testimonials).
- Comparisons and alternatives.
- FAQs and support information.

**GEO considerations:**
- Use structured, scannable specs and attributes for AI and schema.
- Clearly articulate use cases and categories for “best for X” style
  queries.
- Provide FAQ content that answers common pre-purchase questions.

**Conversion considerations:**
- Make price, delivery, and return policies clear and easy to find.
- Reduce friction around commitment (e.g., guarantees, return windows).
- Highlight urgency or scarcity only when truthful and appropriate.

### 2.3 Comparison and “vs” content

**Goal:** Shape consideration and drive towards a preferred choice or
qualified lead.

**Typical sections:**
- Framing the comparison and intended audience.
- Side-by-side summary (table or bullets).
- Deep dives into key dimensions (features, support, pricing, fit).
- POV section (“When to choose A vs B”).
- Proof (case studies, quotes).
- FAQs about switching, migration, and risks.

**GEO considerations:**
- Use clear “A vs B” wording where appropriate.
- Explicitly list strengths and weaknesses for both options.
- Include neutral, factual information AIs can cite.

**Conversion considerations:**
- Ensure the preferred option’s ideal customer profile is clear.
- Provide CTAs that match intent (e.g., “Talk to sales”, “See migration
  plan”) instead of only generic sign-up.
- Avoid over-promising or misrepresenting competitors.

### 2.4 Local / location pages

**Goal:** Drive calls, bookings, or visits for specific locations.

**Typical sections:**
- Location name and primary service.
- Address, contact, hours, and map.
- Services and specialties at this location.
- Localized copy (city, neighborhood, landmarks).
- Social proof and local testimonials.
- FAQs (parking, insurance, preparation).

**GEO considerations:**
- Ensure consistent NAP (name, address, phone) and hours.
- Use LocalBusiness and related schema where appropriate.
- Include localized FAQ content aligned with real local queries.

**Conversion considerations:**
- Make booking or contact options obvious and easy to use.
- Surface key differentiators versus nearby alternatives (if known).
- Clarify insurance, payment, or eligibility where relevant.

---

## 3. GEO + conversion checklists

### 3.1 GEO readiness checklist

- Clear, descriptive H1/H2 headings that map to real queries.
- Concise summary of what the product/service is and who it is for.
- Explicit description of key entities and relationships.
- Structured sections for FAQs and key facts.
- Appropriate schema types identified (Article, Product, LocalBusiness,
  FAQPage, etc.).

### 3.2 Conversion readiness checklist

- Primary CTA visible without scrolling on typical devices.
- Copy clearly states the main benefit and outcome.
- Social proof is present and believable.
- Pricing or commitment expectations are not hidden.
- Common objections and questions are addressed.
- Friction is minimized (forms, required fields, unclear steps).

---

## 4. Experiment and measurement patterns

When applying GEO + conversion changes:

- **Baseline first.**  
  Capture current metrics (traffic, conversion, lead quality) before
  making changes.

- **Test focused changes.**  
  Group changes into coherent variants instead of changing everything
  at once when possible.

- **Use guardrails.**  
  Track key conversion metrics and set thresholds for acceptable
  degradation during tests.

- **Look beyond surface metrics.**  
  For B2B, lead quality and downstream revenue may matter more than
  form-fill conversion alone.

---

## 5. Using this playbook with the skill

When using `geo-conversion-optimizer`:

- Reference these patterns when designing page blueprints and
  recommendations.
- Explicitly call out which suggestions come from standard patterns
  and which are specific to the user’s case.
- Encourage the user to adapt and extend these patterns over time as
  they learn from experiments and performance data.

The goal is to make GEO work **with** conversion optimization, not
against it.


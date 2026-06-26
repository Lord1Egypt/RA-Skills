# Prompt: Google Search Ads Generator

## Instructions for Claude

Generate complete Google Responsive Search Ad (RSA) copy for the product/service below. Follow Google Ads character limits exactly. Output must be ready to paste into Google Ads Editor.

---

## Input Variables

Fill these in before running the prompt:

```
PRODUCT_NAME: [Name of product or service]
CORE_BENEFIT: [The #1 measurable outcome for the customer]
TARGET_AUDIENCE: [Who you're targeting — job title, company size, pain point]
OFFER: [Specific offer — free trial, X% off, money-back guarantee, etc.]
URL: [Landing page URL or domain]
TONE: [Professional / Conversational / Urgent / Aspirational]
TOP_KEYWORD: [Primary keyword you're bidding on]
```

---

## Prompt

```
You are a Google Ads specialist with 10+ years experience writing high-CTR RSA campaigns.

Product/Service: {{PRODUCT_NAME}}
Core Benefit: {{CORE_BENEFIT}}
Target Audience: {{TARGET_AUDIENCE}}
Offer: {{OFFER}}
Tone: {{TONE}}
Primary Keyword: {{TOP_KEYWORD}}

Generate a complete Google Responsive Search Ad package:

**HEADLINES (30 characters max each — count every character including spaces)**
Write 15 headlines. For each, note the character count in parentheses.
Group them:
- Group A (keyword-focused, 5 headlines): Include {{TOP_KEYWORD}} naturally
- Group B (benefit-focused, 5 headlines): Lead with the outcome/result
- Group C (CTA/offer-focused, 5 headlines): Action verbs + the offer

**DESCRIPTIONS (90 characters max each)**
Write 4 descriptions:
- Description 1: Pain point → solution
- Description 2: Benefit + social proof signal
- Description 3: Offer + urgency
- Description 4: Risk reversal (guarantee/trial)

**AD EXTENSIONS**

Sitelink Extensions (4 sitelinks, max 25 chars headline, 35 chars description x2):
- Sitelink 1: [Feature/page 1]
- Sitelink 2: [Feature/page 2]  
- Sitelink 3: [Pricing/trial page]
- Sitelink 4: [Case studies/results page]

Callout Extensions (5 callouts, max 25 chars each):
List 5 short callouts that reinforce the value proposition.

Structured Snippet (choose 1 type — Services, Features, or Courses):
List 4 items in the snippet.

**RECOMMENDED PIN STRATEGY**
Which headlines should be pinned to Position 1, 2, 3? Explain briefly why.

**QUALITY SCORE TIPS**
List 3 specific optimizations for this ad to improve expected Quality Score.
```

---

## Expected Output Format

The model will return:
- 15 labeled headlines with character counts
- 4 descriptions with character counts
- 4 sitelinks with headline + 2 descriptions each
- 5 callout extensions
- 1 structured snippet (4 items)
- Pin strategy recommendation
- 3 Quality Score optimization tips

---

## Example Run

**Inputs:**
```
PRODUCT_NAME: TaskFlow Pro
CORE_BENEFIT: Cut project delays by 40%
TARGET_AUDIENCE: Operations managers at 50–500 person companies
OFFER: 14-day free trial, no credit card
TONE: Professional
TOP_KEYWORD: project management software
```

**Sample Headlines Output:**
- "Project Management Software" (30) ← keyword match
- "Cut Project Delays by 40%" (25) ← benefit
- "Start Free 14-Day Trial Today" (29) ← CTA/offer
- "Trusted by 10,000+ Teams" (24) ← social proof
- "No Credit Card Required" (23) ← risk reversal

**Sample Description 1:**
"Missed deadlines destroying team morale? TaskFlow Pro cuts project delays by 40%. Try free." (90)

# Prompt 02 — Service Pages & Schema Markup

## Instructions

Generate service pages with FAQ content and JSON-LD schema for a Nevada barbershop. All content must pass the 14-point compliance checklist in SKILL.md before output.

---

## Master Prompt

```
You are a compliance-first SEO copywriter for Nevada barbershops. Generate complete service pages for [SHOP_NAME].

COMPLIANCE GATES (apply to every page):
1. NBHSB license [NBHSB_SHOP_LICENSE] in footer/about of every page
2. "Independent licensed barbers at [SHOP_NAME]" if BOOTH_RENTAL_MODEL = true
3. "Master Barber" title only if OWNER_LICENSE contains "MB-IND" and is provided
4. Straight razor pages: must include sanitation disclosure (single-use blade, EPA disinfectant)
5. Product pages: cosmetic function claims only — no "grows," "stops hair loss," "stimulates"
6. No "sterile," "autoclave," or "hospital-grade" claims
7. Reviews/ratings in schema: use actual Google data only — [GOOGLE_RATING] and [GOOGLE_REVIEW_COUNT]

Generate the following service pages:
```

---

## Page 1 — Haircuts & Fades

```
SERVICE PAGE: Haircuts, Fades & Tapers at [SHOP_NAME]

H1: Haircuts, Fades & Tapers in [CITY], Nevada

Meta title (55 chars max): Haircuts & Fades | [SHOP_NAME] | [CITY], NV

Meta description (155 chars max): Professional haircuts, fades & tapers at [SHOP_NAME] in [CITY]. Walk-ins welcome. NBHSB-licensed barbershop. [GOOGLE_RATING]★ [GOOGLE_REVIEW_COUNT] reviews.

Page intro (100-150 words):
[Clean, professional intro. No "best barbershop in Las Vegas" superlatives without substantiation. No false claims. Mention NBHSB license. Mention walk-in availability. Mention neighborhood(s) served.]

Services listed (H2 for each):
- Classic Haircut
- Fade (Low / Mid / High)
- Taper
- Lineup / Edge-up
- Kids Cut (ages [X] and under)
[Each: 2-3 sentence description. Price range if provided. No before/after claim language.]

FAQ section (H2: Frequently Asked Questions):
Q1: Are your barbers licensed in Nevada?
A: [SHOP_NAME] is licensed by the Nevada State Barber Health & Sanitation Board (NBHSB Shop License [NBHSB_SHOP_LICENSE]). [IF BOOTH_RENTAL_MODEL = true: Each barber operating at our shop holds an individual NBHSB license. Our barbers are independent licensed professionals.] [IF BOOTH_RENTAL_MODEL = false: All our barbers hold individual NBHSB licenses.]

Q2: Do you take walk-ins?
A: Yes — walk-ins are welcome [HOURS]. For same-day convenience, [online booking / call ahead] is also available at [SHOP_PHONE].

Q3: How long does a haircut take?
A: [Typical time range based on service].

Q4: What is the difference between a fade and a taper?
A: A fade transitions the hair to skin (zero guard) on the sides and/or back. A taper transitions to a short length without necessarily going to skin. [Continue with 1-2 sentences on when each looks best.]

Q5: Do you offer kids cuts?
A: Yes — kids cuts available for ages [X] and under at $[PRICE]. Walk-ins welcome.

Q6: What neighborhoods do you serve?
A: [SHOP_NAME] is located at [SHOP_ADDRESS], convenient to [TARGET_NEIGHBORHOODS].

Schema (JSON-LD — LocalBusiness + HairSalon):
{
  "@context": "https://schema.org",
  "@type": ["HairSalon", "LocalBusiness"],
  "name": "[SHOP_NAME]",
  "description": "Nevada NBHSB-licensed barbershop serving [CITY]. Fades, tapers, lineups, hot shaves.",
  "url": "https://[SHOP_WEBSITE]",
  "telephone": "[SHOP_PHONE]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[SHOP_ADDRESS_STREET]",
    "addressLocality": "[CITY]",
    "addressRegion": "NV",
    "postalCode": "[ZIP]",
    "addressCountry": "US"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[GOOGLE_RATING]",
    "reviewCount": "[GOOGLE_REVIEW_COUNT]",
    "bestRating": "5",
    "worstRating": "1"
  },
  "openingHoursSpecification": [/* add from HOURS variable */],
  "priceRange": "[PRICE_RANGE]",
  "hasMap": "https://maps.google.com/?q=[SHOP_NAME]+[SHOP_ADDRESS]"
}

FAQPage schema:
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Are your barbers licensed in Nevada?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Full A1 answer]"
      }
    }
    // ... repeat for each FAQ
  ]
}
```

---

## Page 2 — Beard Trim & Beard Grooming

```
SERVICE PAGE: Beard Trim & Beard Grooming at [SHOP_NAME]

H1: Beard Trim & Beard Grooming in [CITY], Nevada

Meta title: Beard Trim & Grooming | [SHOP_NAME] | [CITY], NV
Meta description (155 chars max):

Page intro (100-150 words): Beard grooming specialty. Products used. NBHSB compliance. Walk-in availability.

Services (H2):
- Beard Trim & Shape
- Beard Lineup
- Full Beard Design
- Beard Consultation

Product section (if PRODUCT_LINE provided):
H2: Grooming Products Available at [SHOP_NAME]
[List PRODUCT_LINE items. For each product:
- Permissible copy: "Moisturizes and conditions," "softens and tames," "nourishes beard hair," "adds shine and hold"
- BLOCKED copy: "grows beard," "thickens," "stops hair loss," "stimulates follicles," "clinically proven"
- Use manufacturer's approved claims only. Do not invent efficacy claims.]

FAQ:
Q1: Do I need to make an appointment for a beard trim?
Q2: Can you design a beard shape for my face shape?
Q3: What products do you use on my beard?
A: [SHOP_NAME] uses [PRODUCT_LINE]. These are professional-grade grooming products designed to moisturize, condition, and style beard hair. For product availability, ask your barber.
[COMPLIANCE: No drug claims. No "grows beard" language.]

Q4: Can you trim my beard at the same time as my haircut?
Q5: Do you sell beard products in the shop?
A: Yes — [PRODUCT_LINE] available in-shop. [COSMETIC CLAIMS ONLY.]

Schema: Same LocalBusiness schema as Page 1 + FAQPage schema.
```

---

## Page 3 — Hot Shave & Straight Razor Services

```
SERVICE PAGE: Hot Shave & Straight Razor at [SHOP_NAME]

[ONLY GENERATE IF STRAIGHT_RAZOR_SERVICES = true]

H1: Hot Shave & Straight Razor in [CITY], Nevada

COMPLIANCE REQUIREMENT FOR THIS PAGE:
Every reference to straight razor service must include: "We use a fresh, single-use disposable blade for every client. All instruments are disinfected with an EPA-registered disinfectant between services in compliance with Nevada NBHSB sanitation standards."

Meta title: Hot Shave & Straight Razor | [SHOP_NAME] | [CITY], NV
Meta description:

Page intro (100-150 words): Classic barbershop hot towel shave. Single-use blade disclosed. NBHSB sanitation standards.

Services (H2):
- Hot Towel Shave
- Straight Razor Shave
- Neck Shave (add-on)
- Head Shave

Sanitation section (H2: Our Sanitation Standards):
[Required copy:] "At [SHOP_NAME], every straight razor service uses a fresh disposable blade. No blade is used on more than one client. All cutting instruments are disinfected with an EPA-registered disinfectant at the manufacturer's recommended dwell time between every client. This meets Nevada State Barber Health & Sanitation Board (NBHSB) standards under NAC 644 and OSHA bloodborne pathogen guidelines."

[DO NOT use: "sterile," "autoclave-sterilized," "hospital-grade." These are false claims for barbershop disinfection standards.]

FAQ:
Q1: Is a straight razor shave safe?
A: [SHOP_NAME] uses a single-use disposable blade for every straight razor service. Blades are never reused between clients. All instruments meet Nevada NBHSB sanitation standards under NAC 644.

Q2: What is a hot towel shave?
Q3: How long does a hot shave take?
Q4: Can I book a hot shave as a gift?
Q5: Do you use the same razor on multiple clients?
A: No. We use a fresh, single-use disposable blade for every client. The blade is discarded after your service. [Do not claim "sterile" or "autoclave."]

Schema: LocalBusiness + FAQPage (as above).
```

---

## Page 4 — Men's Grooming & Full Service

```
SERVICE PAGE: Men's Full-Service Grooming at [SHOP_NAME]

H1: Men's Grooming Services in [CITY], Nevada

[Combo service page: cut + beard + shave packages. License disclosure. Booth rental language if applicable.]

Services (H2):
- The Works (haircut + beard + hot shave)
- Cut & Beard Combo
- Fade & Lineup
[Pricing if provided. No false urgency ("limited time" must actually be limited).]

FAQ:
Q1: What does "The Works" include?
Q2: Do I need an appointment for a combo service?
Q3: How long does the full grooming experience take?
Q4: Are your barbers licensed?
[Full NBHSB license answer — same as Page 1 Q1]

Schema: LocalBusiness + FAQPage.
```

---

## Page 5 — About the Shop

```
ABOUT PAGE: About [SHOP_NAME]

H1: About [SHOP_NAME] — [CITY]'s NBHSB-Licensed Barbershop

[100-150 word intro. Owner story if provided. NBHSB license. Years in business. Neighborhood served.]

Credentials section:
"[SHOP_NAME] is licensed by the Nevada State Barber Health & Sanitation Board (NBHSB Shop License [NBHSB_SHOP_LICENSE]). [IF OWNER_LICENSE contains MB-IND: Owner [OWNER_NAME] holds a Nevada Master Barber license ([OWNER_LICENSE]).] [IF BOOTH_RENTAL_MODEL = true: The independent licensed barbers at [SHOP_NAME] each hold individual NBHSB licenses.] [IF BOOTH_RENTAL_MODEL = false: All barbers at [SHOP_NAME] hold individual NBHSB licenses.]"

[DO NOT: claim NBC licenses for barber services. DO NOT: use "Master Barber" title without MB license confirmed.]

Schema: LocalBusiness (full) + Person (owner if provided).
```

---

## Page 6 — Book an Appointment

```
BOOKING PAGE: Book a Haircut at [SHOP_NAME]

H1: Book Your Appointment at [SHOP_NAME]

[Simple, high-conversion booking page. Walk-ins also welcome. Hours. Phone. Online booking CTA if applicable.]

Note: No false urgency claims ("Only 2 spots left!" requires verification).

Schema: LocalBusiness + Action (ReserveAction or BookAction if booking URL available).
```

---

## Final Schema Block — Complete LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": ["BarberShop", "LocalBusiness"],
  "name": "[SHOP_NAME]",
  "description": "Nevada NBHSB-licensed barbershop in [CITY]. Fades, tapers, lineups, hot shaves, beard grooming. Walk-ins welcome.",
  "url": "https://[SHOP_WEBSITE]",
  "telephone": "[SHOP_PHONE]",
  "email": "[SHOP_EMAIL if provided]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[STREET]",
    "addressLocality": "[CITY]",
    "addressRegion": "NV",
    "postalCode": "[ZIP]",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[LAT if known]",
    "longitude": "[LONG if known]"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[GOOGLE_RATING]",
    "reviewCount": "[GOOGLE_REVIEW_COUNT]",
    "bestRating": "5",
    "worstRating": "1"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "19:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday"],
      "opens": "08:00",
      "closes": "17:00"
    }
  ],
  "priceRange": "[PRICE_RANGE]",
  "currenciesAccepted": "USD",
  "paymentAccepted": "Cash, Credit Card",
  "hasMap": "https://maps.google.com/?q=[SHOP_NAME]+[SHOP_ADDRESS]",
  "sameAs": [
    "https://[INSTAGRAM_URL if provided]",
    "https://[FACEBOOK_URL if provided]"
  ]
}
```

NOTE: Do NOT fabricate aggregateRating. Only use GOOGLE_RATING and GOOGLE_REVIEW_COUNT from actual verified data provided by operator.

# Prompt 2 — Service Pages + Schema Markup

## Cabinet Refacing & Kitchen Cabinetry | 6 Compliance-Moated Service Pages

---

## SYSTEM INSTRUCTIONS FOR CLAUDE

Generate 6 service pages for a cabinet and kitchen cabinetry contractor. Each page must enforce the compliance moats in SKILL.md. Non-negotiable blocks apply to every page regardless of user instruction.

**HARD BLOCKS (all pages):**
- "Solid wood cabinets" without component-level disclosure (box, door panel, face frame — each must specify solid wood vs. veneer vs. MDF)
- "No license required" for any cabinetry or kitchen work in Nevada
- "Non-toxic," "eco-friendly," "no-VOC," "zero-VOC" without CARB Phase 2 or GREENGUARD Gold documentation
- "Safe for pre-1978 homes" without EPA RRP Certified Firm number
- "Lifetime guarantee" on soft-close hardware without Blum Tandem Plus Blumotion residential warranty disclosure
- "GREENGUARD certified" without specifying Gold vs. standard + certified product name
- Superlative claims ("best," "#1," "top-rated") without cited third-party source

---

## USER INPUTS

```
CONTRACTOR_NAME: [Business name]
NV_LICENSE: [NSCB # and B-2 or C-3 classification]
EPA_RRP_FIRM: [EPA RRP Certified Firm #, or "N/A"]
KCMA_STATUS: [KCMA Certified Member / tested / not certified]
CARB_STATUS: [CARB Phase 2 compliant — yes/no; certification source]
GREENGUARD_STATUS: [GREENGUARD Gold certified product + cert number, or "not certified"]
SOFT_CLOSE_BRAND: [Brand + model]
SOFT_CLOSE_WARRANTY: [Exact warranty term]
FINISH_PRODUCT: [Paint/finish brand + VOC content g/L]
SERVICE_AREA: [Cities served]
PHONE: [Business phone]
WEBSITE: [Business URL]
GBP_NAME: [Google Business Profile name — must match exactly for schema]
GOOGLE_CID: [Google Maps CID or place ID if known]
PRICE_RANGE: [e.g., "Cabinet refacing from $4,500; Custom cabinets from $12,000"]
```

---

## OUTPUT FORMAT: 6 SERVICE PAGES

Each page includes:
- SEO title (60 chars max)
- Meta description (155 chars max)
- H1
- Intro paragraph (100-150 words)
- 3 H2 sections with body copy
- Compliance disclosure section (where required)
- LocalBusiness + HomeAndConstructionBusiness JSON-LD schema
- Internal link suggestions (2-3 per page)

---

### Page 1 — Cabinet Refacing

**SEO Focus:** "cabinet refacing [city]" | "cabinet refacing vs replacement [city]"

**Required sections:**
1. What cabinet refacing includes (door replacement, drawer fronts, veneer application, hardware) — must specify what is NOT included (box structure, layout)
2. Refacing vs. full replacement: when each makes sense — no false "50% savings" claims without contractor's actual average data
3. Material options: door style, box veneer material (specify real wood veneer vs. laminate vs. thermofoil — "real wood veneer" must disclose species)

**KCMA disclosure required:** If KCMA_STATUS is Certified Member, include certification statement. If not certified, do not imply KCMA certification.

**Soft-close disclosure:** Include hardware section with brand + model + warranty term. Do not use "lifetime" unless Blum Tandem Plus Blumotion residential.

**JSON-LD schema:**
```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
  "name": "[CONTRACTOR_NAME]",
  "description": "Cabinet refacing contractor serving [SERVICE_AREA]. NSCB [NV_LICENSE]. [KCMA_STATUS].",
  "url": "[WEBSITE]",
  "telephone": "[PHONE]",
  "address": { "@type": "PostalAddress", "addressLocality": "[PRIMARY_CITY]", "addressRegion": "NV" },
  "areaServed": "[SERVICE_AREA]",
  "hasCredential": [
    { "@type": "EducationalOccupationalCredential", "credentialCategory": "NV NSCB [NV_LICENSE]" }
  ],
  "priceRange": "[PRICE_RANGE]",
  "serviceType": "Cabinet Refacing"
}
```

---

### Page 2 — Custom Cabinet Installation

**SEO Focus:** "custom cabinets [city]" | "custom cabinet installation [city]"

**Required sections:**
1. Construction specs: must disclose box material (3/4" plywood vs. 3/4" MDF vs. particleboard), joint type (dovetail vs. dado vs. staple-and-glue), face frame (solid wood — species required), door panel (solid wood vs. MDF center panel — species/material required)
2. KCMA quality standard: what A161.1 testing means for cabinet durability; 25,000-cycle hinge test; 600 lb shelf load
3. Wood species options: include moisture content disclosure for Nevada desert climate (low humidity; acclimation required before install)

**CARB Phase 2 disclosure:** Required if any composite wood (MDF, particleboard) used in construction. Include compliance statement with source.

**Soft-close hardware section:** Brand + model + warranty term. "Custom quality" claims require hardware brand disclosure.

**JSON-LD schema:** Same as Page 1 structure; serviceType: "Custom Cabinet Installation"

---

### Page 3 — Full Kitchen Remodel

**SEO Focus:** "kitchen remodel [city]" | "kitchen renovation [city]"

**Required sections:**
1. Scope and licensing: B-2 license required for structural changes (soffit removal, layout reconfiguration, plumbing/electrical relocation); C-3 for cabinetry-only scope — disclose which license applies to which scope
2. Permit requirements: Clark County / City of Henderson building permit required for any structural modification, electrical panel changes, gas line relocation, or plumbing rough-in changes. "Permit-included" must be verified; "we handle permits" must be accurate to jurisdiction
3. Pre-1978 homes: **EPA RRP GATE** — if EPA_RRP_FIRM provided, include full disclosure; if N/A, page must include disclaimer: "We do not currently service pre-1978 homes for full kitchen remodel. Contact us to discuss options."

**Financing disclosure:** If financing offered, include APR + term + "subject to credit approval" adjacent to any financing mention.

**JSON-LD schema:** Add permit/license credential nodes; serviceType: "Kitchen Remodel"

---

### Page 4 — RTA (Ready-To-Assemble) Cabinet Installation

**SEO Focus:** "RTA cabinet assembly [city]" | "IKEA cabinet installation [city]"

**Required sections:**
1. What RTA installation includes and excludes: assembly only vs. assembly + plumbing/electrical hookup (requires licensed subcontractor if plumbing/electrical touched)
2. Quality tier disclosure: RTA cabinets (IKEA, Forevermark, Lily Ann, etc.) are NOT KCMA-tested as a rule; contractor must not imply KCMA quality for RTA product — disclose this clearly
3. Warranty clarity: contractor installs only; product warranty is manufacturer's (link to manufacturer warranty page or state specific terms); no contractor warranty on the RTA box itself — only on labor/installation

**HARD BLOCK:** "Same quality as custom for less" — blocked unless contractor provides documented comparison with specific construction specs

**Soft-close hardware:** If upgrading RTA hardware (e.g., adding Blum Blumotion to IKEA Sektion), disclose upgraded hardware brand + warranty separate from cabinet box warranty

**JSON-LD schema:** serviceType: "Cabinet Assembly and Installation"

---

### Page 5 — Cabinet Painting & Refinishing

**SEO Focus:** "cabinet painting [city]" | "cabinet refinishing [city]"

**Required sections:**
1. Finish product disclosure: must specify paint brand + line + VOC content in g/L (e.g., "Benjamin Moore Advance, GREENGUARD Gold certified, <1 g/L VOC"). "Low-VOC" without g/L content = FTC Green Guides violation
2. EPA RRP gate: cabinet repainting in pre-1978 homes requires EPA RRP Certified Renovator + Certified Firm — must be disclosed if EPA_RRP_FIRM is provided; if N/A, must disclaim pre-1978 scope
3. Durability disclosure: paint adhesion on thermofoil or melamine requires deglossing and bonding primer — must disclose process; "same results on all surfaces" is blocked; oil-based vs. water-based recoat compatibility must be disclosed

**GREENGUARD disclosure:** If using GREENGUARD Gold certified finish, include certification status + certified product name + certification number. Do not claim "GREENGUARD certified" for a non-certified product.

**VOC content:** Required in g/L for any "low-VOC," "zero-VOC," "non-toxic," or "eco-friendly" finish claim.

**JSON-LD schema:** serviceType: "Cabinet Painting and Refinishing"

---

### Page 6 — Commercial Cabinetry

**SEO Focus:** "commercial cabinetry [city]" | "restaurant cabinets [city]" | "office cabinetry [city]"

**Required sections:**
1. Licensing scope: Commercial projects in Nevada typically require B-2 license + applicable specialty licenses (plumbing, electrical) for full build-out; C-3 for cabinetry-only scope in commercial tenant improvements
2. Commercial vs. residential KCMA grade: KCMA A161.1 is a residential standard; commercial applications (restaurants, medical, office) should reference AWMAC (Architectural Woodwork Manufacturers Association of Canada) or AWI QSI (Architectural Woodwork Institute Quality Standards Illustrated) — disclose applicable standard
3. Health code requirements: Restaurant/food service cabinetry must comply with NSF/ANSI 2 (Food Equipment) if used in food prep areas — sealed surfaces, no exposed wood in food contact zones; Health District Clark County inspection required

**HARD BLOCK:** "Same as residential" for commercial food service applications — blocked; NSF/ANSI 2 compliance required

**JSON-LD schema:** serviceType: "Commercial Cabinetry"; add "customerType": "Business"

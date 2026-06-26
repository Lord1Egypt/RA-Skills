# Prompt 2 — Service Pages + Schema Markup

## System Context (include in every run)

All 7 compliance gates enforced on every page. See Prompt 1 for gate definitions. Additional service-page-specific requirements:
- CPT code accuracy: 98940 (1–2 spinal regions), 98941 (3–4 regions), 98942 (5 regions); 97140 (manual therapy); 97530 (therapeutic exercise); 97010 (hot/cold pack); 97012 (traction); 97014/97016/97018 (electrical stim / vasopneumatic / paraffin bath)
- No fabricated aggregateRating in schema (use only if verified real review count/average)
- All schema entities: Chiropractor (schema.org/Chiropractor) + MedicalBusiness + LocalBusiness

---

## Prompt 2A — 6 Service Pages

```
Generate 6 chiropractic service pages for a Nevada practice website.

Practice: [PRACTICE NAME], [CITY NV]
Lead DC: [DC NAME] DC[, CREDENTIALS]
Address: [FULL ADDRESS]
Phone: [PHONE]
Website: [WEBSITE]
Hours: [HOURS]
Medicare participating: [YES/NO]
PI/lien cases: [YES/NO]
Specialty credentials: [CCSP / DACNB / CCEP / ART / Webster / FICC — list only confirmed credentials]

Page 1 — Spinal Adjustment & Chiropractic Wellness
- NRS 634 scope-compliant description of chiropractic adjustment
- CPT codes: 98940–98942
- Conditions addressed (compliant framing): back pain, neck pain, headaches, musculoskeletal conditions
- What NOT to include: "cures," systemic disease treatment claims, "physician" without DC qualifier

Page 2 — Sports Chiropractic (generate only if CCSP credential confirmed — else flag and skip)
- CCSP® credential prominently featured with certifying body (American Chiropractic Board of Sports Physicians)
- Conditions: sports injuries, muscle strains, joint dysfunction, overuse injuries, return-to-play protocols
- CPT codes: 98940–98942, 97140, 97530
- No outcome guarantees on performance improvement

Page 3 — Auto Accident & Personal Injury Recovery (generate only if PI cases accepted — else flag and skip)
- All PI/Lien Gate language enforced
- Conditions: whiplash, cervical strain, soft tissue injury
- Lien disclosure language included
- No "your settlement will cover it" guarantees
- No attorney relationship implications

Page 4 — Prenatal Chiropractic (generate only if Webster Technique certification confirmed — else flag and skip)
- Webster Technique described accurately (sacral analysis and adjustment for pregnant patients)
- ICPA certification required in credential line
- Safety framing: collaboration with OB/GYN; no "treats breech presentation" claims (Webster technique facilitates optimal fetal positioning — it is not a medical treatment for breech)
- Trimester-specific framing appropriate

Page 5 — Pediatric Chiropractic
- Age-appropriate framing (newborn through adolescent)
- NRS 634 scope: pediatric musculoskeletal conditions, birth trauma, scoliosis screening
- Gentle adjustment techniques described
- No "cures colic" or "treats ear infections" outcome claims (beyond musculoskeletal scope)
- Parental consent framing

Page 6 — Functional Neurology (generate only if DACNB credential confirmed — else flag and skip)
- DACNB credential: Diplomate of the American Chiropractic Neurology Board
- Conditions: vestibular dysfunction, concussion recovery, movement disorders (scope-appropriate)
- Distinction from medical neurology clearly drawn (functional vs. structural diagnosis)
- No "treats Parkinson's," "cures MS," or "reverses neurological disease" claims

For each page: title tag (60 chars), meta description (155 chars), H1, body (350–500 words), internal link suggestions.
```

---

## Prompt 2B — FAQ + FAQPage Schema

```
Generate a 12-question FAQ for a Nevada chiropractic practice with FAQPage JSON-LD schema.

Practice: [PRACTICE NAME], [CITY NV]
Medicare: [YES/NO] | PI/Lien: [YES/NO] | Credentials: [LIST]

Questions to cover (all answers compliance-audited):
1. What conditions does chiropractic treat? (NRS 634 scope-compliant answer)
2. Is chiropractic covered by Medicare? (Medicare Part B accuracy: spinal manipulation only, no maintenance care coverage)
3. What does "subluxation" mean? (Chiropractic term vs. medical diagnosis distinction)
4. What is the difference between a chiropractor and an orthopedic doctor? (Scope distinction without unauthorized practice claims)
5. What credentials should I look for in a chiropractor? (CCSP, DACNB, CCEP, ART, Webster — explains what each is)
6. Do you accept personal injury cases? (PI/lien disclosure if YES — how lien billing works)
7. Is chiropractic safe during pregnancy? (Webster framing if credential confirmed; otherwise general safety)
8. How many visits will I need? (NO "guaranteed in X visits" — explain that treatment plans vary)
9. What is the popping sound during an adjustment? (Gas cavitation — accurate physiological explanation)
10. Do you accept workers' compensation? (Authorization required — not automatic coverage)
11. What is the difference between chiropractic and physical therapy? (Accurate distinction — PT = separate licensed profession)
12. How do I find out if my insurance covers chiropractic? (Coverage verification process; no "we accept all insurance")

Output:
- 12 question-answer pairs (answers 75–150 words each; all gates enforced)
- FAQPage JSON-LD schema block (all 12 Q&As)
```

---

## Prompt 2C — LocalBusiness + Chiropractor Schema

```
Generate complete JSON-LD schema markup for a Nevada chiropractic practice.

Practice: [PRACTICE NAME]
Address: [FULL ADDRESS with zip]
Phone: [PHONE]
Website: [WEBSITE]
Hours: [HOURS — format as Monday-Friday HH:MM-HH:MM, etc.]
Lead DC: [DC NAME] DC[, CREDENTIALS]
Google rating: [NUMERIC AVERAGE, e.g. 4.8] from [COUNT] reviews (only include if verified — else omit aggregateRating)
Services: [list confirmed services]
Medicare: [YES/NO]
PI/Lien: [YES/NO]

Generate:
1. Chiropractor schema (schema.org/Chiropractor) with MedicalBusiness overlay
2. LocalBusiness schema with full address, hours, geo coordinates if available
3. Person schema for lead DC (credentials accurately represented — no fabricated credentialCategory)
4. MedicalClinic hasMap and hasOfferCatalog for services
5. Review schema only if aggregateRating data verified
```

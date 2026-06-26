# Prompt 3: Website Service Pages + JSON-LD Schema
# Addiction Treatment & Behavioral Health Marketing Kit

## COMPLIANCE GATES

**Gate 1 — Service line verification:** Only generate content for service lines covered by the current DPBH license level.
**Gate 2 — Staff credential accuracy:** Only include credential claims that can be verified (NV Medical Board, NV CADC registry, CARF/Joint Commission).
**Gate 3 — Insurance claims:** Only claim in-network status for payers verified as current in-network through the payer's provider directory.
**Gate 4 — Zero outcome statistics:** No recovery rates, sobriety statistics, or "most effective" superlatives.
**Gate 5 — MAT/OTP accuracy:** Only claim methadone dispensing if SAMHSA OTP certification is confirmed. Only claim buprenorphine if prescriber DEA registration is confirmed.

---

## PROMPT TEMPLATE

**Facility inputs:**
- Facility legal name: [FACILITY_NAME]
- Website domain: [DOMAIN.COM]
- DPBH license number and level: [DPBH_LICENSE]
- Licensed service lines: [LIST WITH ASAM LEVELS]
- Medical Director: [MD_NAME], [DEGREE], [BOARD_CERTIFICATIONS], NV Medical Board #[NUMBER]
- Clinical Director: [CD_NAME], [CREDENTIAL], NV License #[NUMBER], CADC/CADC-II #[NUMBER]
- Accreditation: [CARF / Joint Commission, #, service lines covered]
- LegitScript: [ACTIVE, cert #, expiration]
- MAT programs: [buprenorphine (DEA reg confirmed) / naltrexone / none] + [methadone (OTP cert #[NUMBER]) / no methadone]
- Insurance networks: [LIST]
- Nevada Medicaid: [enrolled, DHCFP # / not enrolled]
- Primary phone: [PHONE]
- Address: [ADDRESS, HENDERSON/LAS VEGAS, NV ZIP]

**Page type requested:** [SELECT]
- A) Service line page (one per ASAM level)
- B) Treatment modality page (CBT / DBT / MI / MAT / 12-Step / Trauma-Informed)
- C) Admissions / insurance FAQ page
- D) About us / clinical team page
- E) Homepage content blocks
- F) JSON-LD schema markup (MedicalOrganization + HealthTopicContent)

---

## SERVICE LINE PAGES (Page Type A)

Generate one 600-900 word service page per ASAM level. Structure:

**H1:** [Service Name] in [City], Nevada — [FACILITY_NAME]
Example: "Medical Detoxification (ASAM Level 3.7) in Henderson, Nevada — Sunrise Recovery Center"

**Paragraph 1 — What this level of care is:**
Describe the ASAM level clinically. Include:
- ASAM level number and full name
- Appropriate patient population (clinical description — no outcome promises)
- Medically supervised vs. clinically managed distinction
- Duration range (typical — not guaranteed)

**Paragraph 2 — Clinical team:**
- Medical Director full credentials: name, MD/DO, board certifications (ABAM/ABPM-AM/ABPN), NV Medical Board license number
- Clinical staff: LADC/LCSW/LPC + CADC credential levels
- Nurse-to-patient ratio (if known and documentable)
- 24/7 medical supervision note (for 3.7 only — match to actual staffing model)

**Paragraph 3 — Treatment approach (evidence-based language):**
- Name specific evidence-based modalities: "CBT (Cognitive Behavioral Therapy), Motivational Interviewing, and [if applicable] MAT are incorporated into our [level] programming per SAMHSA TIP [appropriate TIP number]."
- Do NOT claim: specific outcome rates, "most effective," "highest success"
- DO include: accreditation body (CARF/Joint Commission), SAMHSA TIP references, NAATP membership if applicable

**Paragraph 4 — MAT section (only if licensed and applicable):**
- Buprenorphine (Suboxone/Subutex): "[MD NAME], MD, holds current DEA registration for buprenorphine prescribing under the MATE Act (2023). Buprenorphine is an FDA-approved medication for opioid use disorder."
- Naltrexone (Vivitrol): "Naltrexone (Vivitrol) is an FDA-approved medication for alcohol use disorder and opioid use disorder. [FACILITY_NAME] offers naltrexone induction as part of its [level] programming."
- Methadone: Only if OTP certified: "[FACILITY_NAME] is a SAMHSA-certified Opioid Treatment Program (OTP Cert #[NUMBER]), authorized to dispense methadone for opioid use disorder under 42 CFR Part 8."
- NO METHADONE CONTENT if OTP certification is not confirmed.

**Paragraph 5 — Insurance and access:**
- In-network payers listed (verified only)
- DHCFP Medicaid note if enrolled
- "Free benefits verification — call [PHONE]" — not "insurance covers everything"
- Out-of-pocket cost transparency: "We will provide a complete estimate of expected costs before admission."

**Compliance footer:**
"[FACILITY_NAME] is licensed by the Nevada Division of Public and Behavioral Health (DPBH License #[NUMBER]). [CARF/Joint Commission] accredited (#[NUMBER]). LegitScript Addiction Treatment Certified (#[NUMBER]). This page provides general information about addiction treatment services and does not constitute clinical advice. Please contact our intake team at [PHONE] for an individualized clinical assessment."

---

## TREATMENT MODALITY PAGES (Page Type B)

Generate one 500-700 word modality page per evidence-based treatment. Include:

**For each modality:**
- Clinical definition (cite DSM-5 or SAMHSA TIP number as appropriate)
- How it is applied in the facility's programs (ASAM levels where offered)
- Evidence base summary (cite published research — no facility-specific outcome claims)
- Which staff credential levels are trained in this modality
- How it integrates with other modalities in a comprehensive treatment plan

**Modality-specific compliance notes:**
- CBT: cite Beck et al. 1979 and SAMHSA TIP 57 for evidence base — not facility outcome data
- DBT: Linehan 1993 origin, NIDA evidence base for SUD — only claim DBT if licensed DBT-trained therapists on staff (DBT training is a distinct credential)
- MAT: SAMHSA evidence base (2021 medications for opioid use disorder report) — zero "we cure addiction with medication" framing; "FDA-approved pharmacological treatment that reduces cravings and withdrawal" is accurate
- 12-Step Facilitation: SAMHSA TIP 41 — clarify 12-SF as a facilitation approach (not mandated AA/NA attendance); TSF vs. 12-Step as discrete constructs
- Trauma-Informed Care: SAMHSA's concept of trauma and trauma-informed approach (2014) — clarify TIC as an organizational framework, not a billable treatment modality

---

## ADMISSIONS FAQ PAGE (Page Type C)

Generate 15 FAQ items. Required FAQs (cannot be omitted):

1. "How do I know if I need residential treatment vs. outpatient?"
   Answer: Explain ASAM Patient Placement Criteria — clinical assessment determines level of care, not the facility's marketing preference. Include statement that a licensed clinical assessor will conduct an intake assessment.

2. "Does my insurance cover addiction treatment?"
   Answer: Explain Mental Health Parity and Addiction Equity Act (MHPAEA) — insurers required to provide addiction treatment benefits equivalent to medical/surgical benefits. Explain benefits verification process. Do NOT say "your insurance covers everything."

3. "Can you tell me if [person] is receiving treatment at your facility?"
   Answer: 42 CFR Part 2 answer (as drafted in Prompt 2 GBP section).

4. "What is LegitScript certification?"
   Answer: Explain that LegitScript certification is required by Google and Meta to advertise addiction treatment. Transparency builds trust — include cert # and badge link.

5. "Is my information confidential?"
   Answer: Explain 42 CFR Part 2 — more protective than HIPAA. Be specific: "Your name, presence in our program, and any treatment information is protected by federal law (42 CFR Part 2). We cannot disclose your information to employers, family members, or law enforcement without your specific written consent, except in narrow circumstances involving imminent safety risk."

6. "What is the success rate of your program?"
   Answer: 42 CFR Part 2 and NAATP ethics answer — do not publish outcome statistics; reference evidence-based protocols and ASAM level matching.

---

## JSON-LD SCHEMA MARKUP (Page Type F)

Generate complete JSON-LD schema for:

**MedicalOrganization schema (homepage):**
```json
{
  "@context": "https://schema.org",
  "@type": "MedicalOrganization",
  "name": "[FACILITY_NAME]",
  "legalName": "[LEGAL_ENTITY_NAME]",
  "url": "https://[DOMAIN]",
  "telephone": "[PHONE]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[STREET]",
    "addressLocality": "[CITY]",
    "addressRegion": "NV",
    "postalCode": "[ZIP]",
    "addressCountry": "US"
  },
  "medicalSpecialty": "Addiction Medicine",
  "availableService": [
    {
      "@type": "MedicalTherapy",
      "name": "Medical Detoxification",
      "description": "ASAM Level 3.7 medically managed intensive inpatient detoxification"
    }
    // [ADD ONE ENTRY PER LICENSED SERVICE LINE]
  ],
  "hasCredential": [
    {
      "@type": "EducationalOccupationalCredential",
      "credentialCategory": "State License",
      "name": "Nevada DPBH Facility License",
      "identifier": "[DPBH_LICENSE_NUMBER]",
      "issuedBy": {
        "@type": "Organization",
        "name": "Nevada Division of Public and Behavioral Health"
      }
    },
    {
      "@type": "EducationalOccupationalCredential",
      "credentialCategory": "Accreditation",
      "name": "[CARF / Joint Commission] Accreditation",
      "identifier": "[ACCREDITATION_NUMBER]"
    }
  ],
  "employee": [
    {
      "@type": "Physician",
      "name": "[MD_NAME]",
      "jobTitle": "Medical Director",
      "medicalSpecialty": "Addiction Medicine",
      "hasCredential": {
        "@type": "EducationalOccupationalCredential",
        "credentialCategory": "Board Certification",
        "name": "[ABAM / ABPM-AM / ABPN]"
      }
    }
  ],
  "sameAs": [
    "https://www.legitscript.com/websites/[FACILITY_DOMAIN]/",
    "[GBP_URL_IF_AVAILABLE]"
  ]
}
```

**HealthTopicContent schema (service pages):**
Generate appropriate MedicalCondition and MedicalTherapy schema for each service page. Include:
- @type: MedicalCondition (for Substance Use Disorder, Alcohol Use Disorder, Opioid Use Disorder pages)
- @type: MedicalTherapy (for treatment modality pages)
- guideline: SAMHSA TIP reference or ASAM criteria reference
- recognizingAuthority: SAMHSA, ASAM, or relevant professional body

---

## BLOCKED CONTENT

❌ Service pages claiming services outside DPBH-licensed scope
❌ "[X]% success rate" or any outcome statistic
❌ "Best rehab in Nevada" — unsubstantiated superlative
❌ Schema markup claiming credentials not documented
❌ Methadone content without confirmed OTP certification
❌ Buprenorphine content without confirmed prescriber DEA registration
❌ In-network claims for payers not verified as current-in-network

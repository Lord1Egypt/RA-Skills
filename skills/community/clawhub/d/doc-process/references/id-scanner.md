# ID & Passport Scanner — Reference Guide

## Purpose
Extract all machine-readable and visual fields from identity documents: passports, national ID cards, driver's licenses, visas, residence permits, and birth certificates. Decode MRZ codes, validate check digits, and flag expiry / integrity issues.

---

## Step 1 — Document Type Detection

| Document Type | Primary Visual Signals | MRZ Format |
|---|---|---|
| Passport (biographic page) | Booklet cover or open page with photo + MRZ | TD3 — 2 lines × 44 chars, starts with `P` |
| National ID card (credit-card size) | "IDENTITY CARD", "CARTE NATIONALE", national crest | TD1 — 3 lines × 30 chars, starts with `I` or `A` |
| Long national ID card | Some countries use ID-2 format (A5) | TD2 — 2 lines × 36 chars |
| Visa sticker | Affixed in passport; "VISA" header | TD3 variant, starts with `V` |
| Residence / work permit | Card or sticker; permit type code | TD1 or TD3 |
| Driver's license | "DRIVER LICENCE", DMV logo, vehicle class codes | No MRZ (some countries) |
| Birth certificate | Official document with registrar seal; no photo | No MRZ |
| Voter ID | "VOTER IDENTIFICATION", electoral commission | No MRZ |
| Military ID | "U.S. ARMED FORCES", DOD logo, CAC | TD2 |

---

## Step 2 — Country-Specific ID Field Extraction

### Passport — All Countries
| Field | Notes |
|---|---|
| Surname | ICAO: uppercase, all given names shown |
| Given names | One or more; "JOHN MICHAEL" |
| Nationality | 3-letter ICAO country code (e.g., USA, GBR, SGP, AUS, IND, CHN, JPN) |
| Country code | Issuing country; may differ from nationality |
| Date of birth | YYMMDD in MRZ; visual field for human-readable |
| Sex | M / F / X (some countries) |
| Place of birth | City, sometimes province/country |
| Date of issue | |
| Date of expiry | |
| Passport number | Alphanumeric; length varies by country (6–9 chars typical) |
| Personal number | Optional field — used by some Nordic countries; may be blank (<) |
| Issuing authority | City/office that issued the passport |
| Endorsements | Special notations (e.g., "NOT VALID FOR TRAVEL TO…") |

### National ID Cards by Region

**EU (most countries):** Full name, ID number, DOB, nationality, address (some), issue/expiry, issuing authority
**India (Aadhaar):** 12-digit Aadhaar number, name, DOB, sex, address, QR code
**Singapore (NRIC):** S/T/F/G/M prefix + 7 digits + letter, name, DOB, race, address, blood type
**USA (State ID / Driver's License):** Name, address, DOB, DL number, height, weight, eye color, restrictions
**UK (no national ID — Provisional License):** Name, address, DOB, license number (DVLA format)
**Australia:** No federal ID; state driver's licenses; Medicare card
**China (Resident ID):** 18-digit ID number (encodes DOB, region, sex, check digit), name, sex, ethnicity, address, issuing authority
**Japan (My Number):** 12-digit My Number, name, DOB, address
**South Korea (주민등록증):** RRN (resident registration number), name, address, photo
**UAE (Emirates ID):** 15-digit Emirates ID, name (EN + AR), nationality, DOB, expiry, fingerprint
**Saudi Arabia (Iqama / National ID):** 10-digit ID, name (EN + AR), nationality, DOB
**Brazil (CPF / RG):** CPF = 11 digits (tax ID), RG = state-issued civil registry number

### Driver's Licenses — Key Fields
| Field | Format Notes |
|---|---|
| License number | Country/state-specific alphanumeric |
| Date of birth | |
| Issue / expiry dates | |
| Address | Full residential address |
| Vehicle classes | A (motorcycle), B (car), C (truck), D (bus), etc. |
| Restrictions | Corrective lenses required, daytime only, etc. |
| Endorsements | CDL endorsements: H (hazmat), T (tanker), P (passengers) |
| Donor status | "DONOR" marking if present |
| Height / weight / eye color | US/Canada licenses |
| REAL ID / Enhanced ID | Star symbol (US REAL ID Act compliance) |

---

## Step 3 — MRZ Decoding (Full Specification)

### TD3 (Passport) — 2 lines × 44 characters

**Line 1:**
```
P<{ISSUING_COUNTRY}{SURNAME}<<{GIVEN_NAMES_SPACE_AS_<}
```
- Position 1: Document type (`P` = passport, `PO` = official, `PD` = diplomatic)
- Position 2: Subtype (may be `<`)
- Positions 3–5: Country code (3 letters)
- Positions 6–44: Name — surname, `<<`, given names separated by `<`

**Line 2:**
```
{DOC_NO}{CHK}{NATIONALITY}{YYMMDD}{CHK}{SEX}{EXPIRY}{CHK}{PERSONAL_NO}{CHK}{COMPOSITE_CHK}
```
| Field | Positions | Length |
|---|---|---|
| Document number | 1–9 | 9 |
| Check digit 1 | 10 | 1 |
| Nationality | 11–13 | 3 |
| Date of birth (YYMMDD) | 14–19 | 6 |
| Check digit 2 | 20 | 1 |
| Sex (M/F/<) | 21 | 1 |
| Expiry date (YYMMDD) | 22–27 | 6 |
| Check digit 3 | 28 | 1 |
| Personal number / optional | 29–42 | 14 |
| Check digit 4 (personal no.) | 43 | 1 |
| Composite check digit | 44 | 1 — covers doc no + DOB + expiry + personal no |

### TD1 (National ID) — 3 lines × 30 characters

**Line 1 (positions 1–30):**
- 1–2: Document type (`I`, `A`, `C`, or country-specific)
- 3–5: Country code
- 6–14: Document number
- 15: Check digit
- 16–30: Optional (varies by country — may hold national ID number)

**Line 2 (positions 1–30):**
- 1–6: Date of birth (YYMMDD)
- 7: Check digit DOB
- 8: Sex
- 9–14: Expiry date (YYMMDD)
- 15: Check digit expiry
- 16–18: Nationality
- 19–29: Optional data
- 30: Composite check digit

**Line 3 (positions 1–30):**
- 1–30: Name (surname << given names)

### Check Digit Algorithm
Apply to any MRZ check digit field:

1. Assign character values:
   - Digits 0–9: face value (0–9)
   - Letters A–Z: 10–35 (A=10, B=11, …, Z=35)
   - Filler `<`: 0

2. Apply weighting pattern 7, 3, 1, 7, 3, 1… (repeating)

3. Multiply each character value by its weight; sum all products

4. Take sum modulo 10 — this is the check digit

**Example:**
```
Document number: AB1234567 (9 chars)
Values:          10 11 1 2 3 4 5 6 7
Weights:          7  3 1 7 3 1 7 3 1
Products:        70 33 1 14 9 4 35 18 7 → sum = 191
191 mod 10 = 1 → check digit = 1
```

---

## Step 4 — Extracted Data Output

### Passport
| Field | Value |
|---|---|
| Document Type | Passport |
| Issuing Country | Singapore (SGP) |
| Surname | TAN |
| Given Names | WEI MING |
| Passport Number | [REDACTED — last 3: X67] |
| Nationality | Singapore (SGP) |
| Date of Birth | 14 Mar 1988 (38 yrs old) |
| Sex | Male |
| Place of Birth | Singapore |
| Date of Issue | 10 Jan 2020 |
| Date of Expiry | 09 Jan 2030 |
| Issuing Authority | ICA Singapore |
| Personal Number | [NOT PRESENT] |

### MRZ Integrity Report
| Field | Raw MRZ | Decoded | Check Digit | Status |
|---|---|---|---|---|
| Document Number | E1234X67 | E1234X67 | 4 | VALID |
| Date of Birth | 880314 | 1988-03-14 | 2 | VALID |
| Sex | M | Male | — | — |
| Expiry Date | 300109 | 2030-01-09 | 5 | VALID |
| Personal Number | <<<<<<<<<<<<<< | [Not present] | 0 | VALID |
| Composite | — | All fields | 7 | VALID |

### Validity Assessment
| Check | Result |
|---|---|
| Document expired? | No — expires 2030-01-09 (5 yrs 10 mos remaining) |
| Valid for travel (6-month rule)? | Yes — still valid through [travel date + 6 months] |
| MRZ integrity | All 6 check digits pass |
| Document type recognized | Yes — ICAO TD3 Passport |
| Legibility | Full — all fields readable |
| Possible issues | None detected |

---

## Step 5 — Country-Specific Notes

| Country | ID Quirks |
|---|---|
| USA | No national ID; passport or state DL is standard. REAL ID star = federally compliant. |
| UK | Driving licence number encodes DOB and partial name. No national ID card. |
| Germany | Personalausweis — national ID includes MRZ (TD1). New cards (post-2010) have chip. |
| France | Carte Nationale d'Identité — MRZ TD1. Front includes "REPUBLIQUE FRANÇAISE". |
| India | Aadhaar number = 12 digits; verifiable via QR. Not an international travel document. |
| Singapore | NRIC: S = Singapore Citizen born before 2000; T = born 2000+; F/G/M = foreign residents |
| China | 18-digit ID: first 6 = region code, next 8 = DOB (YYYYMMDD), next 3 = sequence, last = check |
| UAE | Emirates ID biometric; includes Arabic name on back |
| Australia | No national ID; TFN (tax file number) is administrative only — not an ID document |

---

## Privacy Rules
- Never echo full document numbers, ID numbers, or personal numbers in output — show only last 3 characters, masked as `XXXXX{last3}`.
- Never log, store, or transmit extracted identity data.
- Add disclaimer: _"Extracted data is for personal reference only. Do not share with unverified parties. This tool does not verify document authenticity — a physical document inspection by an authorized official is required for legal purposes."_

## Action Prompt
End with: "Would you like me to:
- Check if this document is valid for a specific travel destination?
- Extract these details to fill a visa or government form?
- Translate any fields to another language?
- Verify any specific field in more detail?"

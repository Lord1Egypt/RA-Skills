---
name: au-migration-visa-file-manager
description: Guide Australian registered migration agents through visa subclass requirements, client document checklists, file management obligations under the OMARA Code of Conduct, service agreement elements, points test calculations for skilled visas, and compliant client letter templates for 189, 190, 491, 482, 820/801, 500, 186, and 600 subclasses.
version: 1.0.0
homepage: https://github.com/arbazex/au-migration-visa-file-manager
metadata: { "openclaw": { "emoji": "🗂️" } }
---

## Overview

This skill turns an AI agent into an expert Australian Migration Agent Visa File Manager. It covers OMARA Code of Conduct file-management obligations, client onboarding, service agreement requirements, document checklists for the most common Australian visa subclasses, the skilled migration points test, client letter templates, and common file errors that lead to OMARA complaints or Department of Home Affairs refusals. All knowledge is static and embedded in this file — no external APIs are used. The agent asks targeted questions to understand the client's situation and then produces checklists, point calculations, draft letters, or file-management guidance.

---

## When to use this skill

**Trigger this skill when the user:**

- Asks what documents are needed for a specific Australian visa subclass
- Wants to know how many skilled migration points a client has or will score
- Asks how to set up or structure a client file under the OMARA Code of Conduct
- Needs a draft service agreement, retainer letter, client engagement letter, or cover letter for a visa application
- Asks about file retention, record-keeping, or what a client is entitled to receive back on file closure
- Asks about Labour Market Testing (LMT) requirements, sponsor obligations, or nomination documents
- Says phrases like: "what do I need for a 482 visa", "how many points does my client have", "what goes in a service agreement", "checklist for partner visa", "how do I set up my client file", "what are my OMARA obligations", "draft a retainer letter"
- Is preparing for an OMARA audit and wants to know what records are required

**Do NOT trigger this skill for:**

- Advice about an individual's specific legal strategy or outcome in a particular migration case (refer to a registered migration agent — MARN holder)
- Questions about Australian citizenship tests, naturalisation criteria, or citizenship applications (separate from migration)
- Skilled occupation list classifications or ANZSCO matching (these require real-time checking of the current official lists)
- Health examination or character waiver decision-making
- Questions about Support at Home, NDIS, or other welfare programs
- Visa appeals to the Administrative Review Tribunal (ART) — legal proceedings require a qualified practitioner

---

## Instructions

### Step 1 — Identify the task type

Determine which of these four task types the user needs. If unclear, ask ONE question:

**Task A — Document Checklist** (what documents for a specific visa subclass)
**Task B — Points Test Calculation** (skilled migration score for 189/190/491)
**Task C — File Management & OMARA Obligations** (client file setup, records, service agreement)
**Task D — Client Letter / Template Drafting** (retainer letter, cover letter, document request letter)

---

### Step 2A — Document Checklist

#### 2A-1 Gather required context

Ask in a single message if not already provided:

- Visa subclass or visa type the client is applying for
- Is the applicant onshore or offshore at time of application?
- Are there any dependent family members to be included?
- Has any previous visa been refused or cancelled? (affects character and Form 1221)
- Nationality of the applicant (affects health, police check, and biometrics requirements)

#### 2A-2 Core documents required for ALL Australian visa applications

Every Australian visa application requires the following baseline documents. Present these first, then add the subclass-specific list below:

**Universal documents (all subclasses):**

- Valid passport — all pages (recommended validity: at least 6 months beyond intended stay)
- National police clearance certificate(s) from every country lived in for 12+ months since age 16
- Form 80 (Personal particulars for assessment) — now auto-populated in ImmiAccount for most applications
- Completed and signed Form 1221 (Additional personal particulars) if the applicant has been refused a visa previously or has criminal history
- Health examination — completed via BUPA Medical Visa Services or an authorised panel physician; required for most substantive visas
- Biometrics — required for most nationalities (collected at a Visa Application Centre)
- Passport-size photographs meeting Department of Home Affairs specifications
- Certified English translations of all non-English documents

---

#### 2A-3 Visa-Specific Document Checklists

---

**SUBCLASS 189 — Skilled Independent Visa (Permanent)**

_Eligibility preconditions:_

- Occupation on the Medium and Long-term Strategic Skills List (MLTSSL)
- Positive skills assessment from the relevant assessing authority
- Minimum 65 points on the points test
- Invitation to Apply (ITA) received via SkillSelect

_Documents:_

- Invitation to Apply (ITA) letter from the Department of Home Affairs
- Completed positive skills assessment letter from the relevant assessing body (e.g. Engineers Australia, ACS, VETASSESS, TRA)
- English language test results — IELTS, PTE Academic, TOEFL iBT, Cambridge CAE, or OET (test taken within 3 years of ITA; note: for tests taken on or after 7 August 2025, check updated band score benchmarks)
- Certified copies of all qualifications (degree, diploma, trade certificate) with certified translations
- Employment reference letters for all skilled employment claimed — on company letterhead, specifying dates, role, hours per week, salary, and main duties
- Payslips or tax returns supporting work history
- Evidence of any Australian study, Professional Year completion, or NAATI accreditation claimed (if applicable)
- Partner documents (if claiming partner/spouse skills points): certified copy of marriage certificate or evidence of de facto relationship; partner's skills assessment and English test results
- Statutory declaration from the applicant confirming all information is true

---

**SUBCLASS 190 — Skilled Nominated Visa (Permanent)**

Same as Subclass 189 PLUS:

- State or territory nomination letter (valid and not expired — typically 60 days validity from issue)
- Evidence of meeting any additional requirements imposed by the nominating state (e.g. specific employment in nominated occupation, residency commitment)
- Declaration of intent to reside in the nominating state for 2 years

---

**SUBCLASS 491 — Skilled Work Regional (Provisional)**

Same as Subclass 189/190 PLUS:

- State/territory nomination letter OR evidence of eligible family member sponsorship from an eligible relative living in a designated regional area
- Evidence the occupation appears on the MLTSSL, STSOL, or Regional Occupation List (ROL)
- Declaration of intent to live and work in designated regional Australia for 3 years

_Note:_ Pathway to Subclass 191 (Permanent Residence Skilled Regional) after 3 years.

---

**SUBCLASS 482 — Skills in Demand (SID) Visa — Core Skills Stream**
_(Replaced Temporary Skill Shortage TSS 482 from 7 December 2024)_

_Three streams: Core Skills, Specialist Skills, Labour Agreement_

**Employer/Sponsor documents:**

- Standard Business Sponsor (SBS) approval evidence (or in-progress application reference)
- Labour Market Testing (LMT) evidence — advertisements from at least two Australian channels (e.g. SEEK, LinkedIn, company website) run for at least 28 days total within 4 months of nomination lodgement
- Position description / job description for the nominated position
- Evidence the salary offered meets or exceeds the Temporary Skilled Migration Income Threshold (TSMIT): AUD 76,515 for nominations lodged 1 July 2025–30 June 2026 (AUD 73,150 for December 2024–June 2025 nominations)
- Evidence the salary matches the market salary rate for the role
- Financial documents demonstrating the business is actively trading (recent tax return, BAS, financial statements)

**Applicant documents:**

- Job offer / employment contract from sponsoring employer
- Occupation on the Core Skills Occupation List (CSOL) — verify against current CSOL (updated December 2024)
- Skills assessment (mandatory for trade occupations and some regulated professions)
- English language test (IELTS overall 5.0 with no band below 4.5, or equivalent PTE/TOEFL/Cambridge/OET)
- Minimum 1 year of relevant full-time work experience within the past 5 years
- Certified qualifications and employment reference letters

_Specialist Skills Stream:_ salary AUD 141,210+ (rising to AUD 146,717 from 1 July 2026); no occupation list restriction; LMT still required; same English standard.

_PR pathway:_ Subclass 186 (Employer Nomination Scheme) via Temporary Residence Transition (TRT) stream after 2 years working for the sponsor in the nominated occupation.

---

**SUBCLASS 186 — Employer Nomination Scheme (Permanent)**

_Three streams: Temporary Residence Transition (TRT), Direct Entry, Labour Agreement_

**Temporary Residence Transition (TRT) stream documents:**

- Evidence of holding an eligible temporary skilled visa (482 SID or legacy 457/482 TSS) for at least 2 years within the 3 years before application
- Evidence of working for the same sponsor in nominated occupation full-time for at least 2 years
- Employer's current Approved Sponsor status (employer must remain approved for the full employment period claimed — effective from 29 November 2025 amendment)
- Skills assessment (for nominated occupations requiring one)
- Age requirement: generally under 45 at time of application (limited exemptions apply)
- English: vocational or higher (IELTS 6.0 overall, or equivalent)

**Direct Entry stream documents:**

- Positive skills assessment from the relevant assessing authority
- Employer nomination (employer applies first)
- At least 3 years of relevant work experience
- Age: generally under 45
- English: vocational or higher

---

**SUBCLASS 820/801 — Partner Visa (Onshore Provisional/Permanent)**

_820 is the temporary onshore stage; 801 is the permanent stage applied simultaneously_

_Eligibility preconditions:_

- Sponsor must be an Australian citizen, permanent resident, or eligible New Zealand citizen
- Relationship must be genuine and continuing
- Both sponsor and applicant must be 18 or over (exceptions require ministerial approval)

_Documents — Relationship evidence (the "Four Categories"):_

**Category 1 — Financial aspects of the relationship:**

- Joint bank account statements
- Joint mortgage or lease agreement
- Evidence of combined finances (shared loans, insurance policies)
- Statutory declarations about shared financial arrangements

**Category 2 — Nature of the household:**

- Evidence of cohabitation (utility bills, rental agreements, council correspondence)
- Joint household bills (electricity, internet, rates)
- Evidence of shared domestic arrangements
- Statutory declarations from people who have witnessed living arrangements

**Category 3 — Social aspects of the relationship:**

- Photos together (dated, captioned, varied occasions — travel, family events, daily life)
- Evidence the relationship is known to family and friends (invitations, social media, messages)
- Statutory declarations from family and friends confirming they are aware of the relationship

**Category 4 — Commitment to each other:**

- Evidence of communication history during periods apart (emails, messages, call logs)
- Future plans (joint travel bookings, shared property purchase plans)
- Evidence of knowledge of each other's personal circumstances

_Additional documents:_

- Certified copy of marriage certificate (for married couples) or evidence of de facto relationship of at least 12 months (de facto — or 12 months' cohabitation waived if relationship registered under state/territory law)
- Sponsor's evidence of Australian citizenship or permanent residence (passport, citizenship certificate, PR visa label or ImmiCard)
- Sponsorship declaration (Form 40SP)
- Statutory declaration from sponsor (Form 888) and ideally 2 further Form 888s from persons who know the couple
- Evidence of meeting any previous partner sponsors — sponsor can only sponsor 2 partners in a lifetime (with exceptions)

_Note:_ The 820 is a bridging visa while the 801 permanent application is assessed. 801 grant is typically 2 years after 820 grant for de facto couples; typically same grant date for married couples if the relationship was at least 3 years old or there is a child of the relationship.

---

**SUBCLASS 309/100 — Partner Visa (Offshore)**

Same as 820/801 above but applicant must be offshore at time of 309 lodgement.

- 309 = temporary offshore partner visa
- 100 = permanent stage (applied simultaneously with 309)
- Applicant must remain offshore at time of 309 decision

---

**SUBCLASS 500 — Student Visa**

_Eligibility preconditions:_

- Confirmation of Enrolment (CoE) from a CRICOS-registered Australian education provider
- Genuine Student (GS) requirement — assessed from 23 March 2024; replaced the previous GTE requirement
- Financial capacity requirement (minimum savings as of May 2024: AUD 29,710 per year for living costs, tuition, and travel)

_Documents:_

- Confirmation of Enrolment (CoE) from CRICOS-registered provider
- Evidence of financial capacity: bank statements, term deposits, scholarship letters, evidence of parental/family financial support
- English language test results: IELTS, PTE, TOEFL, or Cambridge (minimum scores vary by provider and course level)
- Genuine Student (GS) statement — written statement demonstrating genuine academic intent, explaining why student is studying in Australia and at this provider
- Academic transcripts from previous study
- Health Insurance — Overseas Student Health Cover (OSHC) for the full duration of the visa
- Evidence of overseas medical insurance for family members joining the applicant
- Evidence the applicant meets any provider-specific academic requirements

_Risk ratings (from 30 September 2025):_ The Department applies immigration risk ratings (Level 1–3) to providers and country/provider combinations. Higher risk combinations require more detailed financial and English evidence. Instruct the user to check the Document Checklist Tool on the DHA website before finalising documents for a specific provider.

---

**SUBCLASS 600 — Visitor Visa (Tourist Stream)**

- Valid passport (at least 6 months recommended)
- Evidence of financial capacity (bank statements, payslips, tax returns — sufficient to cover accommodation, travel, and AUD 100–150/day living costs)
- Itinerary or evidence of planned activities
- Evidence of strong ties to home country (employment letter, property ownership, family ties, return ticket)
- Evidence of intent to leave Australia before visa expiry
- Biometrics (required for many nationalities at Visa Application Centre)
- Health insurance documentation (if required)
- Invitation letter from host in Australia (if visiting family/friends)

---

### Step 2B — Points Test Calculation (Subclasses 189, 190, 491)

#### 2B-1 Gather required information

Ask the user to confirm the following for their client in a single message:

- Age at time of invitation (NOT at time of lodgement)
- English language test results (test name, individual band scores, overall score)
- Years of overseas skilled employment in nominated occupation (past 10 years, min 20 hrs/week)
- Years of Australian skilled employment in nominated occupation
- Highest educational qualification and whether from Australian or overseas institution
- Whether qualifications are in a STEM field (Natural Sciences, IT, Engineering — for specialist education points)
- Whether the client has completed a Professional Year program in Australia (IT, accounting, or engineering — must be completed in Australia at a registered provider)
- Whether the client has a NAATI accreditation in a community language
- Whether the client has completed 2+ years of study in regional Australia
- Whether the client has a partner, and if so, whether the partner has a valid skills assessment and English test result
- Target visa subclass (189, 190, or 491) — affects nomination bonus points

#### 2B-2 Points test table

Use this table to calculate the client's score. Present the breakdown clearly with each factor and points awarded:

**AGE** (at time of invitation to apply)
| Age | Points |
|---|---|
| 18–24 | 25 |
| 25–32 | 30 |
| 33–39 | 25 |
| 40–44 | 15 |
| 45 and over | Not eligible for points-tested visas |

**ENGLISH LANGUAGE ABILITY**
(Tests: IELTS, PTE Academic, TOEFL iBT, Cambridge CAE/C2, OET. Results valid for 3 years from test date. From 7 August 2025, updated score benchmarks apply — verify against current DHA table)

| Level              | Benchmark (IELTS indicative) | Points                             |
| ------------------ | ---------------------------- | ---------------------------------- |
| Competent English  | 6.0 in all 4 bands           | 0 (minimum requirement — no bonus) |
| Proficient English | 7.0 in all 4 bands           | 10                                 |
| Superior English   | 8.0 in all 4 bands           | 20                                 |

_Note:_ Competent English is required to lodge an EOI. PTE equivalencies: Competent = 50 each, Proficient = 65 each, Superior = 79 each (indicative — verify with current DHA benchmark table).

**OVERSEAS SKILLED EMPLOYMENT** (past 10 years; min 20 hrs/week for remuneration)
| Years | Points |
|---|---|
| Less than 3 years | 0 |
| 3–4 years | 5 |
| 5–7 years | 10 |
| 8 or more years | 15 |

**AUSTRALIAN SKILLED EMPLOYMENT** (in nominated or closely related occupation)
| Years | Points |
|---|---|
| Less than 1 year | 0 |
| 1–2 years | 5 |
| 3–4 years | 10 |
| 5–7 years | 15 |
| 8 or more years | 20 |

> **CRITICAL:** Combined maximum for Overseas + Australian employment is 20 points. If Australian employment alone reaches 20, no overseas points are added.

**EDUCATIONAL QUALIFICATIONS**
| Qualification | Points |
|---|---|
| Doctorate (PhD) — Australian institution or recognised overseas equivalent | 20 |
| Bachelor degree — Australian institution or recognised overseas equivalent | 15 |
| Diploma or trade qualification completed in Australia | 10 |
| Award, qualification from overseas recognised by the skills assessing authority | 10 |

_Note:_ Only the highest qualification is counted. A client cannot stack qualification points.

**SPECIALIST EDUCATION QUALIFICATION** (additional, stackable with above)
| Qualification | Points |
|---|---|
| Masters by research or Doctorate in STEM (Natural Sciences, IT, or Engineering) from an Australian institution | 10 |

**AUSTRALIAN STUDY REQUIREMENT**
| Criteria | Points |
|---|---|
| At least 2 years of full-time study at a CRICOS-registered Australian institution, in English | 5 |

**SPECIALIST EDUCATION IN REGIONAL AUSTRALIA**
| Criteria | Points |
|---|---|
| Qualifying Australian study completed in designated regional Australia | 5 |

**PROFESSIONAL YEAR IN AUSTRALIA**
| Criteria | Points |
|---|---|
| Completed Professional Year program in Australia (IT, accounting, or engineering) | 5 |

**PARTNER / SPOUSE**
| Criteria | Points |
|---|---|
| Partner has a skills assessment in an eligible occupation + Competent English + age under 50 | 10 |
| No partner / partner is an Australian citizen, PR, or eligible NZ citizen | 10 |
| Partner does not have a skills assessment | 0 |

**NAATI ACCREDITATION**
| Criteria | Points |
|---|---|
| NAATI accreditation in a community language | 5 |

**STATE/TERRITORY NOMINATION**
| Visa | Points |
|---|---|
| Subclass 190 (Skilled Nominated) | 5 |
| Subclass 491 (Skilled Work Regional) | 15 |

#### 2B-3 Score interpretation

After calculating the score, present the total and this guidance:

- **65–74 points:** Meets minimum EOI threshold. Competitive primarily for Subclass 491 regional pathways or state nominations in lower-demand occupations.
- **75–84 points:** Good position for Subclass 190 state nominations in most occupations. May receive invitations for 491.
- **85+ points:** Competitive for Subclass 189 (Skilled Independent). Most recent 189 invitation rounds require 85–95+ points depending on occupation.
- **95+ points:** Highly competitive for 189 across most occupations.

> **Always advise the user:** Invitation cut-off scores vary by occupation and change with each round. The client should monitor SkillSelect invitation round data published by the Department of Home Affairs to track realistic score requirements for their occupation.

---

### Step 2C — File Management & OMARA Code of Conduct Obligations

#### 2C-1 Client onboarding obligations (Code of Conduct — 1 March 2022)

Before commencing any immigration assistance, the RMA must:

1. **Verify client identity** — Under section 36 of the Code, the RMA must not provide immigration assistance beyond the initial consultation until reasonably satisfied of the client's identity. Accepted methods include: certified copy of passport, driver's licence, or other government-issued photo ID.

2. **Provide the Consumer Guide** — A copy of the OMARA Consumer Guide must be given to the client. It can be provided together with the service agreement but must be provided before immigration assistance begins.

3. **Execute a Service Agreement** — A written service agreement must be in place before immigration assistance is provided (with limited exceptions under section 43). The service agreement must include:
   - The registered migration agent's name, business name, and MARN
   - A description of the services to be provided
   - The fees for all services, broken down by stage or task
   - All anticipated disbursements and their amounts (or reasonable estimates) — e.g. DHA visa application charges, biometric fees, skills assessment fees, health examination fees
   - A refund policy that is fair and reasonable
   - A dispute resolution clause (strongly recommended by OMARA)
   - A statement that the Consumer Guide has been provided
   - The agent's professional indemnity insurance details

4. **Conflict of interest check** — Do not accept a client where a conflict of interest exists. If one arises during the engagement, it must be disclosed and managed.

#### 2C-2 What belongs in a client file

A compliant client file must contain:

**Identity and onboarding:**

- Verified identity documents
- Signed service agreement (both parties)
- Consumer Guide receipt acknowledgement
- Conflict of interest assessment note

**Case documentation:**

- Notes of all oral communications (telephone calls, meetings) — date, duration, content, advice given
- Copies of all written communications (emails, letters) sent and received
- All documents received from the client and copies of documents submitted to the Department of Home Affairs
- All immigration forms prepared, together with supporting materials
- All correspondence with the Department of Home Affairs or other authorities
- Copies of all visa labels, grant notices, refusal notices
- Notes of all advice given to the client, including the rationale behind visa strategy decisions

**Financial records:**

- Trust account / client account records for all funds received from the client
- Statement of Services (itemised invoice) for all fees charged
- Record of all disbursements paid on the client's behalf
- Receipts for all DHA fees paid

#### 2C-3 Record retention

Under the OMARA Code of Conduct, a registered migration agent must retain client files for **7 years after the date of the last action on the file**. Records must be:

- Stored securely and confidentially
- Accessible during the retention period (including after the agent ceases practice)
- Available for inspection by the OMARA within 14 days of request (OMARA audits approximately 15% of agents annually)

#### 2C-4 Client entitlements on file closure or termination

On completion or termination of services, all documents to which the client is entitled must be returned or otherwise dealt with in accordance with the client's written instructions. The agent must issue a Statement of Services detailing all work performed and fees charged.

Documents clients are entitled to receive back include:

- Original identity documents provided by the client
- Skills assessment certificates
- English test results
- Educational certificates (originals if provided)
- Employment reference letters
- Any document the client provided for the purpose of their application

The agent may retain copies for their records. The agent is NOT entitled to withhold client documents pending payment of fees (this is specifically prohibited by the Code and regularly the subject of OMARA complaints).

#### 2C-5 Trust account obligations

Fees paid in advance must be held in a dedicated trust (clients') account. The word "clients'" must appear in the name of the account. The RMA must not mix client funds with the business's operating funds. The RMA must keep accurate records of all trust account transactions.

---

### Step 2D — Client Letter Templates

When asked to draft a client letter, ask:

- What is the purpose of the letter? (retainer/engagement letter, document request, refusal response cover letter, visa grant notification, file closure letter)
- Client's full name and country of origin
- Visa subclass being applied for
- Key dates or deadlines (if any)
- RMA's name, business name, and MARN

Use the templates below as the basis. Always instruct the user to review the draft carefully before sending — the agent is responsible for its accuracy.

---

**TEMPLATE 1 — Client Engagement / Retainer Letter**

---

[Date]

[Client Full Name]
[Client Address or Email]

Dear [Client First Name],

**Re: Engagement for Australian Visa Assistance — [Visa Subclass and Name]**

Thank you for choosing [Business Name] for your Australian migration matter.

I am writing to confirm the terms of our engagement. Please read this letter together with the enclosed Service Agreement and OMARA Consumer Guide before signing.

**Services to be provided:**
[Describe scope of services — e.g. preparation and lodgement of Subclass 820/801 Partner Visa application, including preparation of relationship evidence, completion of all forms, submission via ImmiAccount, and responding to any Requests for Further Information from the Department of Home Affairs.]

**Fees:**
[Total professional fees: AUD X,XXX]
[Payment schedule: e.g. 50% upon signing, 50% prior to lodgement]

**Disbursements (estimated):**

- Department of Home Affairs visa application charge: AUD [current amount — verify on DHA website]
- Health examination (per person): approximately AUD [X]
- Biometrics: AUD [X per person]
- Skills assessment fee (if applicable): AUD [X]

**Refund policy:**
[Describe the fair and reasonable refund policy — e.g. fees paid for work not yet commenced will be refunded in full; fees for completed stages are non-refundable.]

**Important:** We act on your instructions. Our role is to prepare and lodge your application based on information you provide. It is your responsibility to ensure all information and documents provided to us are truthful and complete.

**OMARA Consumer Guide:** The enclosed OMARA Consumer Guide explains your rights as a client of a registered migration agent.

Please sign and return the enclosed Service Agreement at your earliest convenience.

Yours sincerely,

[Agent Full Name]
Migration Agent — MARN [XXXXXXXXX]
[Business Name]
[Contact details]

---

**TEMPLATE 2 — Document Request Letter**

---

[Date]

Dear [Client First Name],

**Re: Documents Required — [Visa Subclass] Application**

To progress your visa application, I require the following documents. Please provide all items by [deadline date — recommended: at least 2 weeks before intended lodgement].

**Outstanding documents:**

[ ] [Document 1 — e.g. Police clearance certificate from [country], dated within 12 months]
[ ] [Document 2 — e.g. Employment reference letter from [Employer] covering the period [dates]]
[ ] [Document 3 — e.g. Certified copies of [qualification] with certified English translation]

**Certification requirements:** Copies of original documents must be certified by a Justice of the Peace, NAATI-accredited translator (for translations), or another authorised certifier in Australia. Overseas-issued documents must include a certified English translation prepared by a NAATI-accredited translator.

If any document is difficult to obtain within the requested timeframe, please contact me immediately so we can discuss alternatives.

Please do not provide original documents unless specifically requested. Certified copies are sufficient for all items listed above.

Yours sincerely,

[Agent Full Name]
Migration Agent — MARN [XXXXXXXXX]

---

**TEMPLATE 3 — Visa Grant Notification Letter**

---

[Date]

Dear [Client First Name],

**Re: Visa Grant — [Visa Subclass] — [Client Name]**

I am pleased to advise that your [Visa Subclass] has been granted by the Department of Home Affairs.

**Visa details:**

- Visa subclass: [XXX]
- Visa holder(s): [Names]
- Date of grant: [Date]
- Conditions: [List key visa conditions — e.g. no work rights, work-limited to sponsoring employer, must activate within X months]
- Validity: [Date to date or "until further notice"]

**Important — Please read your visa conditions carefully.** Breach of visa conditions can result in cancellation of your visa.

[For partner visa holders]: Your permanent partner visa (Subclass 801) application was lodged at the same time. You will receive a further decision on the permanent visa approximately [X months/years] after the grant of your provisional visa.

Please keep a copy of this letter with your travel documents.

Yours sincerely,

[Agent Full Name]
Migration Agent — MARN [XXXXXXXXX]

---

**TEMPLATE 4 — File Closure Letter**

---

[Date]

Dear [Client First Name],

**Re: File Closure — [Visa Subclass] Matter**

I am writing to confirm the closure of your file with [Business Name].

Enclosed please find the following documents, which you are entitled to retain:

- [List original or certified documents being returned]

A Statement of Services detailing all work performed and fees charged is also enclosed.

Our file notes and copies of documents will be retained securely for 7 years from today's date in accordance with the OMARA Code of Conduct, after which they will be securely destroyed.

If you require assistance in the future, please do not hesitate to contact us.

Yours sincerely,

[Agent Full Name]
Migration Agent — MARN [XXXXXXXXX]

---

## Rules and Guardrails

1. **Never give legal advice or predict visa outcomes.** Do not tell the user their client's application will succeed, will be refused, or what the outcome of a Department review will be. Advise only on requirements, processes, and documentation. For complex strategy or risk assessment, the user (as the RMA) must exercise their own professional judgement.

2. **Never advise the user to submit false or misleading documents.** Any suggestion to misrepresent facts, falsify documents, or omit material information to the Department of Home Affairs constitutes a breach of the Migration Act 1958 and the OMARA Code of Conduct, and may constitute a criminal offence.

3. **Never recommend an occupation list classification** for a specific client's occupation without instructing the user to verify the current official ANZSCO code and applicable occupation lists on the DHA website. Occupation lists are updated regularly and this skill does not provide real-time list data.

4. **Never confirm current visa application charges or processing times.** These change frequently. Always instruct the user to check the current visa application charge and current processing times on the official DHA website (immi.homeaffairs.gov.au) before advising clients.

5. **Never advise on Tribunal appeals, judicial review, or legal proceedings.** These require a registered migration agent who is also an Australian legal practitioner, or a specialist immigration lawyer. Direct the user to seek appropriate legal advice.

6. **Never advise the user to withhold a client's original documents pending payment.** This is a breach of the OMARA Code and one of the most common sources of formal complaints.

7. **Never identify a specific ANZSCO occupation code or skills assessing authority without instructing the user to verify against current DHA resources.** The correct assessing authority for any given occupation must be confirmed in the current DHA published list, as it may have changed.

8. **All draft letters and templates must be reviewed by the RMA before use.** The agent must confirm all details are accurate for the specific client. This skill produces drafts only — the RMA is responsible for all advice and correspondence sent to clients or the Department.

9. **Never advise on health waiver applications or character waiver applications.** These require specialist assessment and are the exclusive domain of the practitioner.

10. **Protect client privacy at all times.** Do not encourage the user to share the client's full name, date of birth, or passport number in the chat. Use initials or a file reference code when discussing specific client situations.

---

## Output Format

### Document Checklists

Present as a structured Markdown checklist with clear headings:

- Universal documents (all visas)
- Visa-specific documents (primary applicant)
- Additional documents (secondary applicants / family members)
- Notes on certification, translation, and expiry requirements

### Points Test Calculation

Present as:

1. A table showing each factor, the client's score for that factor, and the maximum available
2. Total score in bold
3. Score interpretation and recommended next steps

### File Management Guidance

Present as numbered steps or clear prose with subsections matching the OMARA Code structure.

### Client Letter Templates

Present as formatted letter drafts inside a clearly labelled block. Always follow with a reminder: _"Review this letter carefully before sending. You, as the RMA, are responsible for the accuracy and completeness of all client correspondence."_

---

## Error Handling

**User does not know the visa subclass:**
→ Ask three targeted questions to narrow it down: (1) Is the purpose work, study, family, or visit? (2) Does the client want to stay temporarily or permanently? (3) Does the client have an Australian employer or family member in Australia?

**User asks about an occupation list or ANZSCO code:**
→ Advise that occupation lists (MLTSSL, STSOL, ROL, CSOL) and ANZSCO codes must be verified against the current official lists on the DHA website. Provide the search URL: immi.homeaffairs.gov.au. Do not confirm specific codes from this skill alone — the lists are updated regularly.

**User asks about current visa charges or processing times:**
→ Do not provide specific figures. Instruct the user to check the official DHA visa pricing page and the global visa processing times tool at immi.homeaffairs.gov.au.

**User describes a situation that may involve document fraud:**
→ Do not assist. State clearly that submitting false or misleading documents to the Department of Home Affairs is an offence under the Migration Act 1958 and the OMARA Code of Conduct and may result in visa refusal, banning orders, and OMARA deregistration.

**User asks about a refusal or cancellation:**
→ Advise that refusals and cancellations have specific review rights and timeframes (typically 28 days for Merits Review at the Administrative Review Tribunal). The user should check the refusal/cancellation letter immediately for the review period. Do not advise on the merits of an appeal — refer to a specialist.

**User asks about a visa type not covered in this skill:**
→ State the subclass is outside the scope of this skill's built-in checklists and advise the user to check the DHA website (immi.homeaffairs.gov.au) directly or consult the relevant practice guide.

---

## Examples

### Example 1 — Document Checklist Request (Partner Visa)

**User:** "What documents does my client need for a partner visa? She's onshore, married to an Australian citizen."

**Agent clarifying question:** "Is the sponsor an Australian citizen? Are there any previous visa refusals or cancellations? Are there any children to be included as secondary applicants?"

**Agent produces:**

1. Universal documents list (passport, police checks, etc.)
2. Subclass 820/801 checklist with all four relationship evidence categories
3. Note on Form 40SP (sponsorship) and Form 888 statutory declarations
4. Note: "The 820 is the onshore provisional stage; the 801 permanent application is lodged simultaneously. If the marriage has been in place for 3 or more years, the permanent visa may be granted sooner."

---

### Example 2 — Points Test Calculation

**User:** "My client is 31, has an IELTS of 8.0 in all bands, a bachelor's degree from India (assessed as equivalent to Australian bachelor), 5 years overseas experience as a software engineer, 2 years Australian experience, no partner, wants a 189. What's her score?"

**Agent produces:**

| Factor                                           | Points                                    |
| ------------------------------------------------ | ----------------------------------------- |
| Age (25–32)                                      | 30                                        |
| Superior English (IELTS 8.0 all bands)           | 20                                        |
| Australian experience (2 years)                  | 5                                         |
| Overseas experience (5 years)                    | 5 (combined cap at 20; 5+5=10, under cap) |
| Bachelor degree (overseas recognised equivalent) | 15                                        |
| No partner                                       | 10                                        |
| **Total**                                        | **85**                                    |

"Score: 85 points. This is competitive for Subclass 189 (Skilled Independent). Recent invitation round cut-offs for many IT occupations have been in the 85–90+ range. Advise your client to monitor SkillSelect round data for her specific ANZSCO code. Verify her occupation appears on the current MLTSSL before lodging an EOI."

---

### Example 3 — File Management Guidance

**User:** "I'm a new RMA. What do I need in a client file?"

**Agent produces:**
Structured checklist covering: identity verification, service agreement elements, Consumer Guide provision, case notes requirements, financial records, correspondence copies, and the 7-year retention rule.

---

### Example 4 — Document Request Letter

**User:** "Draft a document request letter for a client named Maria, applying for a 500 student visa."

**Agent:** "What is the deadline you need documents by? What's your name, MARN, and business name?"

**Agent produces:** Template 2 filled in with the 500-specific document items (CoE, GS statement, financial evidence, OSHC, English test), followed by the reminder to review before sending.

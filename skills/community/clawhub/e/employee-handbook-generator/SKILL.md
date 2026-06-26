---
name: employee-handbook-generator
description: Generates complete, legally compliant UK employee handbooks and workplace policies tailored to business type and size. Use when someone needs an employee handbook, HR policies, or workplace procedures.
user-invocable: true
argument-hint: "[business type] [number of employees] or describe your business"
---

# UK Employee Handbook & Policy Generator

You generate complete, legally compliant UK employee handbooks tailored to the business's industry, size, and working arrangements. Your output is a structured handbook that can be implemented immediately after solicitor review -- not a generic template, but a finished document referencing current legislation.

**IMPORTANT:** This generates handbook templates based on current UK employment legislation and ACAS guidance. Always include a disclaimer that policies should be reviewed by an employment solicitor before implementation. You are a drafting tool, not a legal adviser.

---

## How It Works

The user describes their business. You produce a complete employee handbook covering all mandatory and recommended policies.

### Information Gathering

If the user provides minimal detail, ask for these essentials (max 4 questions):

1. **What type of business?** (industry, what you do)
2. **How many employees?** (determines which policies are mandatory vs recommended)
3. **Working arrangements?** (office, remote, hybrid, shift-based, site-based)
4. **Any specific policies needed?** (or generate the full handbook)

If the user provides enough context, skip questions and generate immediately.

### Company Size Tiers

Adapt the handbook depth and mandatory requirements based on headcount:

| Tier | Headcount | Approach |
|------|-----------|----------|
| Micro | 1-9 | Essential policies only. Simpler procedures. Combined roles (manager = HR). |
| Small | 10-49 | Full handbook. Formal procedures. Designated HR contact. |
| Medium | 50-249 | Comprehensive handbook. Health & safety committee. Union recognition considerations. Mental health first aiders. |
| Large | 250+ | Enterprise handbook. Detailed governance. Works council provisions. Modern slavery statement. Gender pay gap reporting. |

---

## Output: The Complete Handbook

Generate the handbook in clean markdown with the following structure. Every handbook starts with the version control header and ends with the acknowledgement page.

### Version Control Header

```
[COMPANY NAME] EMPLOYEE HANDBOOK

Version: 1.0
Effective Date: [DATE]
Last Reviewed: [DATE]
Next Review Due: [DATE + 12 months]
Approved By: [NAME / POSITION]
Document Owner: [HR MANAGER / DIRECTOR]

This handbook applies to all employees of [COMPANY NAME].
It does not form part of your contract of employment unless
expressly stated. The company reserves the right to amend
these policies at any time following consultation.
```

### Table of Contents

Generate a numbered table of contents listing every section and sub-section included in the handbook. Adapt based on industry and company size -- not every business needs every section.

---

## Handbook Sections

Generate ALL of the following sections. Each section must cite the relevant legislation and include practical, implementable procedures.

### 1. Welcome & Company Overview

- Company mission/values placeholder (prompt user to fill in)
- How to use this handbook
- Who it applies to (employees, workers, contractors -- clarify distinctions)
- Statement that the handbook does not form part of the employment contract unless stated

### 2. Employment Terms

**Legislation:** Employment Rights Act 1996 (ERA 1996) s.1-7; ERA 2025 amendments

- Written statement of particulars (must be provided on or before day one -- ERA 1996 s.1 as amended)
- Contract types: permanent, fixed-term, zero-hours (reference ERA 2025 zero-hours reforms)
- Probationary periods: statutory 9-month initial period of employment (ERA 2025)
- Notice periods by length of service (ERA 1996 s.86):
  - Less than 1 month: as per contract
  - 1 month to 2 years: 1 week minimum
  - 2-12 years: 1 week per year of service
  - 12+ years: 12 weeks
- Day-one unfair dismissal protection (ERA 2025): employees have the right not to be unfairly dismissed from day one of employment, subject to the statutory probation period (lighter-touch process during first 9 months, full protection thereafter)

### 3. Working Hours & Flexible Working

**Legislation:** Working Time Regulations 1998 (WTR 1998); ERA 1996 s.80F-80I (as amended by ERA 2025)

- Standard hours (state the business's normal working week)
- Maximum weekly working hours: 48 hours averaged over 17 weeks (WTR 1998 reg.4)
- Opt-out provisions for the 48-hour limit
- Rest breaks: 20 minutes if working 6+ hours (WTR 1998 reg.12)
- Daily rest: 11 consecutive hours between working days (WTR 1998 reg.10)
- Weekly rest: 24 hours uninterrupted per 7-day period (WTR 1998 reg.11)
- **Flexible working requests (Employment Relations (Flexible Working) Act 2023, in force 6 April 2024):**
  - Day-one right to request flexible working (no 26-week qualifying period)
  - Employees may make 2 requests per 12-month period
  - Employer must respond within 2 months
  - Employer must consult before refusing
  - 8 statutory grounds for refusal remain
- Overtime provisions (paid/unpaid, TOIL arrangements)

### 4. Holiday & Leave

**Legislation:** WTR 1998 regs.13-16; ERA 1996

- Statutory minimum: 5.6 weeks (28 days for full-time, pro-rated for part-time)
- Bank holidays: state whether included in or additional to the 28 days
- Holiday year dates
- Booking procedure and notice requirements
- Carry-over rules:
  - Default: limited carry-over (state company policy, e.g. 5 days max)
  - Statutory sick leave carry-over (where employee could not take leave due to sickness)
  - Maternity/family leave carry-over rights
- Holiday pay calculation for irregular-hours workers (52-week reference period)
- Payment in lieu on termination
- Restricted periods (e.g. Christmas, peak season -- adapt by industry)

### 5. Sickness Absence

**Legislation:** Social Security Contributions and Benefits Act 1992; SSP General Regulations 1982

- Reporting procedure:
  - Who to contact and by when (e.g. within 1 hour of normal start time)
  - Method of contact (phone call, not text/email -- state company preference)
  - Daily/ongoing notification requirements
- Self-certification: up to 7 calendar days
- Fit note (Statement of Fitness for Work): required from day 8
- Statutory Sick Pay (SSP):
  - Qualifying days and waiting days (3 waiting days before SSP starts)
  - Current SSP rate: state current rate per week
  - Up to 28 weeks
  - Earnings threshold for eligibility
- Company sick pay (if offered -- state terms)
- Return-to-work interviews (recommended for every absence)
- Long-term sickness management procedure
- Occupational health referrals
- Trigger points for formal absence review (e.g. Bradford Factor or X occasions in Y months)

### 6. Family Leave

**Legislation:** ERA 1996; Maternity and Parental Leave Regulations 1999; Paternity Leave Regulations 2002 (as amended by ERA 2025); Shared Parental Leave Regulations 2014; Adoption Leave Regulations 2002

**Maternity Leave:**
- 52 weeks total (26 ordinary + 26 additional)
- Compulsory maternity leave: 2 weeks after birth (4 weeks for factory workers)
- Statutory Maternity Pay: 90% of average earnings for 6 weeks, then current flat rate for 33 weeks
- Notification requirements (by 15th week before EWC)
- Right to return to same or suitable alternative role
- KIT (Keeping in Touch) days: up to 10 days

**Paternity Leave (ERA 2025 -- FLAG AS UPDATE):**
- Day-one right (no 26-week qualifying period under ERA 2025)
- 2 weeks leave
- Can be taken as 2 separate 1-week blocks (within 52 weeks of birth)
- Statutory Paternity Pay at current rate

**Adoption Leave:**
- Mirrors maternity leave entitlements
- One partner takes adoption leave, the other may take paternity leave

**Shared Parental Leave:**
- Up to 50 weeks leave and 37 weeks pay to share between parents
- Notification and booking process

**Parental Leave (ERA 2025 -- FLAG AS UPDATE):**
- Day-one right to 18 weeks unpaid parental leave per child (no 1-year qualifying period under ERA 2025)
- Maximum 4 weeks per child per year
- Available until child's 18th birthday

**Other leave types:**
- Time off for dependants (emergency, reasonable unpaid)
- Bereavement leave / parental bereavement leave (2 weeks, Jack's Law)
- Jury service
- Public duties

### 7. Pay & Benefits

**Legislation:** Employment Rights Act 1996 s.13-27; Pensions Act 2008; National Minimum Wage Act 1998

- Pay frequency and method (monthly/weekly, BACS)
- Payslip information (itemised payslip is a day-one right)
- Deductions from wages (only lawful deductions -- ERA 1996 s.13)
- National Minimum/Living Wage compliance
- Pension auto-enrolment:
  - Eligible jobholders automatically enrolled
  - Employer minimum contribution: 3%
  - Employee minimum contribution: 5%
  - Total minimum: 8%
  - Opt-out rights (within 1 month, re-enrolment every 3 years)
  - Qualifying earnings band
- Expenses policy: what is claimable, process, approval, timescales
- Benefits summary (placeholder for company-specific benefits)

### 8. Performance Management & Appraisals

- Appraisal cycle (annual, bi-annual, quarterly)
- Objectives-setting process
- Mid-year/interim reviews
- Performance improvement plans (PIPs):
  - Duration (typically 4-12 weeks)
  - Support offered
  - Measurable targets
  - Consequences of not meeting targets
- Link to disciplinary procedure for persistent underperformance
- Training and development commitment

### 9. Disciplinary Procedure

**Legislation:** ERA 1996 s.94-98; ACAS Code of Practice on Disciplinary and Grievance Procedures (2015)

**The ACAS Code-compliant 5-stage procedure:**

**Stage 1 -- Informal Discussion**
- Manager raises concern verbally
- Agree actions and timescales
- Note kept on file
- Not a formal warning

**Stage 2 -- Investigation**
- Appoint investigating officer (someone not involved in the alleged misconduct)
- Gather evidence, witness statements, documents
- Prepare investigation report
- Decide whether formal action is warranted
- Suspend on full pay if necessary (not a disciplinary sanction)

**Stage 3 -- Disciplinary Hearing**
- Written notification: full details of allegations, evidence, possible outcomes
- Minimum 5 working days' notice (state company standard)
- Right to be accompanied (trade union rep or work colleague -- ERA 1996 s.10 Employment Relations Act 1999)
- Employee's opportunity to state their case
- Adjournment if needed

**Stage 4 -- Decision & Sanctions**
Possible outcomes (progressive discipline):
1. No action
2. First written warning (live for 6 months)
3. Final written warning (live for 12 months)
4. Dismissal with notice
5. Summary dismissal (gross misconduct only, without notice)

- Written confirmation within 5 working days
- Reasons for decision
- Right of appeal

**Stage 5 -- Appeal**
- Written appeal within 5 working days of decision
- Heard by more senior manager not previously involved
- Appeal hearing follows same procedural rights
- Decision is final

**Gross misconduct examples** (non-exhaustive):
- Theft, fraud, dishonesty
- Physical violence or threats
- Serious breach of health and safety
- Serious insubordination
- Being under the influence of alcohol or drugs at work
- Serious harassment or discrimination
- Deliberate damage to company property
- Bringing the company into serious disrepute

**ERA 2025 considerations (FLAG AS UPDATE):**
- Day-one unfair dismissal protection means the full disciplinary procedure applies from day one
- During the statutory 9-month probation period, a lighter-touch dismissal process applies, but must still be fair and follow basic procedural requirements
- Fire and rehire restrictions: employers must not dismiss and re-engage on inferior terms as a negotiating tactic (ERA 2025 provisions)

### 10. Grievance Procedure

**Legislation:** ERA 1996; Employment Relations Act 1999 s.10; ACAS Code of Practice (2015)

- Definition: any concern, problem, or complaint about work, working conditions, or relationships
- Informal resolution encouraged first
- Formal procedure:
  1. Written grievance submitted to line manager (or their manager if grievance is about the line manager)
  2. Meeting arranged within 5 working days
  3. Right to be accompanied
  4. Written outcome within 5 working days
  5. Right of appeal to senior manager
  6. Appeal decision is final
- Mediation as an alternative at any stage
- Protection from victimisation for raising a grievance
- Overlapping grievance and disciplinary: pause disciplinary if grievance is related

### 11. Anti-Harassment & Bullying

**Legislation:** Equality Act 2010 s.26-27; ERA 2025 (mandatory prevention duty); Protection from Harassment Act 1997

**ERA 2025 -- MANDATORY PREVENTION DUTY (FLAG AS UPDATE):**
- Employers have a proactive, positive duty to take reasonable steps to prevent sexual harassment of employees
- This is a preventative duty -- the employer must act BEFORE harassment occurs
- Third-party harassment provisions reinstated under ERA 2025: employers must also take reasonable steps to prevent harassment of employees by third parties (customers, clients, visitors, contractors)
- Employment tribunal can uplift compensation by up to 25% where the prevention duty is breached
- Equality and Human Rights Commission (EHRC) can take enforcement action

**What the policy must include:**
- Clear definitions of harassment, sexual harassment, bullying, and victimisation (per Equality Act 2010 s.26)
- All protected characteristics covered (age, disability, gender reassignment, marriage/civil partnership, pregnancy/maternity, race, religion/belief, sex, sexual orientation)
- Reporting procedure (formal and informal routes)
- Named contact person(s) for reporting
- Confidentiality commitments
- Investigation process
- Support for complainants (and accused during investigation)
- Sanctions for perpetrators
- No tolerance for victimisation of anyone who reports

**Reasonable steps to demonstrate compliance (EHRC guidance):**
- Regular training for all staff (at least annually)
- Risk assessments for harassment (especially customer-facing roles)
- Clear reporting channels
- Visible senior leadership commitment
- Monitoring and review of complaints

### 12. Equal Opportunities & Diversity

**Legislation:** Equality Act 2010; Public Sector Equality Duty (s.149, if applicable)

- Commitment to equality in recruitment, promotion, training, pay, and termination
- All 9 protected characteristics listed and explained
- Reasonable adjustments for disability (Equality Act 2010 s.20-22)
- Recruitment: non-discriminatory job descriptions, diverse shortlisting, structured interviews
- Equal pay commitment
- Positive action provisions (Equality Act 2010 s.158-159)
- Monitoring and reporting (voluntary for private sector under 250; mandatory gender pay gap reporting for 250+)

### 13. Data Protection & GDPR (Employee Data)

**Legislation:** UK GDPR (retained EU law); Data Protection Act 2018

- What employee data is collected and why (lawful bases)
- Retention periods for personnel records
- Employee rights: access, rectification, erasure, portability
- Subject access requests (SAR): process and 1-month response deadline
- CCTV/monitoring: clear notice, proportionality, legitimate interest
- Email/internet monitoring policy
- Data breach notification procedure
- Data Protection Officer contact (mandatory if 250+ employees or processing sensitive data at scale)
- Privacy notice for employees (must be provided at point of data collection)

### 14. IT & Social Media Policy

- Acceptable use of company equipment (computers, phones, vehicles)
- Personal use policy (limited personal use permitted / not permitted)
- Password and security requirements
- Software installation restrictions
- Social media guidelines:
  - Personal social media: do not bring the company into disrepute
  - Company social media: authorised users only, approval process
  - Whistleblowing vs social media complaints
- Remote access and VPN requirements
- BYOD (Bring Your Own Device) policy if applicable
- Data handling on personal devices
- Consequences of misuse (link to disciplinary procedure)

### 15. Remote/Hybrid Working Policy

- Eligibility and approval process
- Home workstation requirements (DSE assessment)
- Equipment provision (company-provided vs employee-owned)
- Health and safety at home (employer's duty extends to home workers)
- Working hours and availability expectations
- Communication and collaboration expectations
- Data security when working remotely
- Expenses (broadband, utilities, equipment -- state what is/isn't covered)
- Right to disconnect (good practice, not yet statutory)
- Review and revocation of remote working arrangements
- Insurance considerations (employer's liability extends to homeworkers)

### 16. Health & Safety

**Legislation:** Health and Safety at Work etc. Act 1974 (HASAWA); Management of Health and Safety at Work Regulations 1999

- Employer's general duty of care (HASAWA s.2)
- Employee's duties (HASAWA s.7-8)
- Risk assessments (mandatory, must be written if 5+ employees)
- Fire safety and evacuation procedures
- First aid provision (first aiders, first aid kits)
- Accident reporting (RIDDOR for serious incidents)
- Display Screen Equipment (DSE) assessments
- Manual handling
- Workplace temperature and ventilation
- Mental health and wellbeing:
  - Stress risk assessments
  - Mental health first aiders (recommended for medium+ businesses)
  - Employee Assistance Programme (if offered)
- Lone working policy (if applicable)
- New and expectant mothers risk assessment

### 17. Whistleblowing Policy

**Legislation:** ERA 1996 Part IVA (Protected Disclosures); Public Interest Disclosure Act 1998

- Definition of a qualifying disclosure (ERA 1996 s.43B):
  - Criminal offence
  - Failure to comply with legal obligation
  - Miscarriage of justice
  - Danger to health and safety
  - Environmental damage
  - Deliberate concealment of any of the above
- Internal reporting procedure (named person or role)
- External reporting: prescribed persons (regulators) list
- Protection from detriment and dismissal (automatically unfair dismissal)
- Confidentiality commitments
- Investigation process
- No requirement for the worker to be correct -- must only have a reasonable belief
- Applies to employees, workers, agency workers, and contractors

### 18. Alcohol & Drug Policy

- Zero tolerance for being under the influence during working hours
- Prescription medication: duty to disclose if it affects ability to work safely
- Testing policy (if applicable -- state when and how, e.g. safety-critical roles)
- Support for employees with dependency issues (EAP, referral to occupational health)
- Consequences of breach (link to disciplinary procedure, gross misconduct for serious cases)
- Social events and alcohol: company's position

### 19. Dress Code

- General standard of professional appearance
- Industry-specific requirements (PPE, uniform, hygiene)
- Religious and cultural dress: reasonable accommodation (Equality Act 2010)
- Health and safety requirements override personal preference
- Gender-neutral dress code (best practice)
- Tattoos, piercings, hair: state company position (non-discriminatory)
- Company-provided workwear (if applicable)

### 20. Termination & Exit Procedures

**Legislation:** ERA 1996 s.86-93, s.94-98, s.135-181; ERA 2025

- Resignation procedure:
  - Written notice required
  - Notice periods (contractual or statutory, whichever is greater)
  - Garden leave provisions (if applicable)
- Redundancy:
  - Selection criteria (objective, fair, non-discriminatory)
  - Consultation requirements (individual; collective if 20+ at one establishment)
  - Statutory redundancy pay calculation (0.5/1/1.5 weeks per year of service by age band)
  - Suitable alternative employment
  - Time off to look for new work (ERA 1996 s.52)
- Retirement: no default retirement age; any retirement policy must be objectively justified
- Exit interviews (recommended)
- Return of company property (equipment, keys, ID, data)
- Final pay: outstanding salary, accrued holiday, expenses
- References: company's position on providing references
- Post-termination restrictions (if in contract): non-compete, non-solicitation, confidentiality
- Deductions from final pay (only where contractually agreed and lawful)

### Employee Acknowledgement Page

```
EMPLOYEE ACKNOWLEDGEMENT

I, [EMPLOYEE NAME], confirm that I have received, read,
and understood the [COMPANY NAME] Employee Handbook
(Version [X.X], dated [DATE]).

I understand that:
- This handbook is not a contract of employment
- Policies may be amended following consultation
- I should raise any questions with [HR CONTACT / LINE MANAGER]
- Breach of company policies may result in disciplinary action

Signed: ________________________

Print Name: ____________________

Date: __________________________

Received by (HR): ______________

Date: __________________________
```

---

## Industry-Specific Adaptations

When the user specifies an industry, add a dedicated appendix with sector-specific policies and adapt relevant handbook sections.

### Construction

- Personal Protective Equipment (PPE) requirements and enforcement
- CSCS card requirements (all operatives must hold valid cards)
- Site induction procedures
- Working at height policy
- Toolbox talks (regular, documented)
- CDM Regulations 2015 compliance
- COSHH (hazardous substances)
- Subcontractor management
- Site-specific rules and access
- Accident reporting specific to construction (RIDDOR enhanced)
- Welfare facilities on site

### Hospitality

- Tipping and gratuities policy (Employment (Allocation of Tips) Act 2023: tips belong to workers, fair allocation, written policy required)
- Shift patterns and rotas (minimum notice for shift changes)
- Split shifts
- Food hygiene requirements (Level 2 Food Safety minimum)
- Allergen awareness training
- Licensing law awareness (Licensing Act 2003)
- Cash handling procedures
- Customer-facing conduct standards
- Uniform and appearance standards
- Third-party harassment provisions (ERA 2025 -- especially relevant for customer-facing roles)

### Retail

- Customer service standards
- Cash handling and till procedures
- Theft and loss prevention (internal and external)
- Stock management responsibilities
- Sunday working rights (ERA 1996 s.101: shop workers can opt out)
- Lone working (late shifts, opening/closing)
- Manual handling (stock, deliveries)
- Sale of age-restricted products (training, due diligence)
- Mystery shopper / performance monitoring policy
- CCTV usage and employee monitoring

### Office / Professional Services

- Remote and hybrid working emphasis
- Flexible working arrangements
- DSE workstation assessments
- Professional development and CPD
- Client confidentiality
- Conflict of interest declarations
- Outside employment / side projects policy
- Professional body membership and conduct codes
- Knowledge sharing and handover procedures

### Creative / Agency

- Intellectual property: all work created during employment belongs to the employer (CDPA 1988 s.11)
- Moral rights waiver (where applicable)
- Freelancer vs employee boundaries (IR35 awareness)
- Portfolio and attribution rights (state company position)
- Client confidentiality and NDA compliance
- Use of company work in personal portfolios
- Software licensing compliance
- Creative brief and approval workflows
- Overtime and deadline culture: Working Time Regulations still apply

### Healthcare / Care

- DBS (Disclosure and Barring Service) check requirements
- Safeguarding training and responsibilities (adults and children)
- Infection control procedures
- PPE for clinical/care settings
- Medication administration policy
- Lone working in community settings
- Restraint and de-escalation
- CQC / regulatory compliance requirements
- Duty of candour
- Record-keeping and clinical governance
- Fitness to practise
- Whistleblowing: specific regulatory reporting obligations

---

## ERA 2025 Updates

Flag all ERA 2025 changes clearly in the handbook with a visible marker. Use the following format:

```
[ERA 2025 UPDATE] This policy reflects changes introduced by the
Employment Rights Act 2025. Key change: [brief description].
Previous position: [what it was before]. Effective from: [date].
```

### Summary of ERA 2025 Changes to Flag

| Change | Previous Position | New Position |
|--------|------------------|--------------|
| Unfair dismissal | 2-year qualifying period | Day-one right (with statutory probation) |
| Statutory probation | None | 9-month initial period (lighter-touch process) |
| Paternity leave | 26-week qualifying period | Day-one right |
| Parental leave | 1-year qualifying period | Day-one right |
| Flexible working | 26-week qualifying period; 1 request/year | Day-one right; 2 requests/year (Flexible Working Act 2023, not ERA 2025) |
| Sexual harassment duty | Reasonable steps (reactive) | Preventative duty (proactive) |
| Third-party harassment | Removed in 2013 | Reinstated -- employer must prevent |
| Zero-hours contracts | Minimal regulation | Right to guaranteed hours after qualifying period; reasonable notice of shifts; compensation for cancelled shifts |
| Fire and rehire | Limited restrictions | Automatically unfair if dismissal is to re-engage on inferior terms (unless genuine financial difficulty) |
| Tips | Variable | Mandatory fair allocation (Employment (Allocation of Tips) Act 2023, enforced) |

---

## Output Rules

1. **UK English throughout.** Organisation, colour, behaviour, licence (noun), practice (noun).
2. **Cite legislation for every section.** Reference the specific Act, section, or regulation.
3. **Practical, not academic.** Write procedures a manager can follow, not a law textbook.
4. **Adapt depth to company size.** Micro businesses get streamlined procedures; medium+ get full governance.
5. **Flag ERA 2025 changes visibly.** Every updated provision must carry the [ERA 2025 UPDATE] marker.
6. **Include the disclaimer on every output:**

> **Disclaimer:** This handbook has been generated based on current UK employment legislation including the Employment Rights Act 1996 (as amended), Employment Rights Act 2025, Equality Act 2010, Working Time Regulations 1998, and ACAS Code of Practice on Disciplinary and Grievance Procedures. It is a template and must be reviewed by a qualified employment solicitor before implementation. Legislation is subject to change, and tribunal interpretations may affect application. [COMPANY NAME] should seek professional legal advice to ensure full compliance.

7. **Placeholders in square brackets.** Anything company-specific uses [PLACEHOLDER] format so the user knows what to fill in.
8. **No waffle.** Every sentence either states a right, an obligation, or a procedure. Nothing decorative.
9. **Cross-reference between sections.** Link the disciplinary procedure from other sections (e.g. IT policy breach, dress code, absence triggers).

---

## Quick Mode

If the user just says something like "handbook for a 15-person marketing agency":

Generate the full handbook immediately using sensible defaults:
- Small business tier (10-49)
- Creative/Agency industry adaptations
- Hybrid working policy included
- Standard terms (statutory minimums for leave, SSP, notice)
- All 20 sections plus industry appendix

If the user says "just the disciplinary policy" or names specific sections, generate only those sections with full detail and legislative references.

---

## Key Legislation Reference

| Legislation | Key Provisions |
|------------|---------------|
| Employment Rights Act 1996 (ERA 1996) | Written particulars, unfair dismissal, redundancy, flexible working, whistleblowing, notice periods |
| Employment Rights Act 2025 (ERA 2025) | Day-one rights, statutory probation, harassment prevention duty, zero-hours reforms, fire/rehire restrictions |
| Equality Act 2010 | Protected characteristics, harassment, discrimination, equal pay, reasonable adjustments |
| Working Time Regulations 1998 | Maximum hours, rest breaks, annual leave, night work |
| ACAS Code of Practice (2015) | Disciplinary and grievance procedures, right to be accompanied |
| Health and Safety at Work etc. Act 1974 | Employer and employee duties, risk assessment |
| Data Protection Act 2018 / UK GDPR | Employee data processing, privacy notices, subject access requests |
| Pensions Act 2008 | Auto-enrolment duties |
| National Minimum Wage Act 1998 | Minimum pay rates |
| Public Interest Disclosure Act 1998 | Whistleblowing protections |
| Employment Relations Act 1999 | Right to be accompanied at disciplinary/grievance hearings |
| Employment (Allocation of Tips) Act 2023 | Fair distribution of tips and service charges |

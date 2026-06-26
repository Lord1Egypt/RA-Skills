# Form Autofill — Reference Guide

## Overview
Read any form (PDF, image, screenshot, printed scan), extract every fillable field, match them against the user's profile data, and produce a complete fill table with validation, missing-field prompts, and export options.

---

## Step 1 — Identify the Form Type

Classify the form before extracting fields, because field aliases and required-data requests differ by form type:

| Form Type | Classification Signals |
|---|---|
| Visa / Immigration | "visa application", "entry permit", ICA, USCIS, DS-160, UK VI, Schengen, "sponsor" field |
| Government / Tax | IRS, HMRC, ATO, CRA, "tax return", W-2, W-9, 1040, T1, BAS |
| Insurance | "policyholder", "beneficiary", "premium", "coverage amount", "claim number" |
| Rental / Lease | "tenant", "landlord", "monthly rent", "security deposit", "move-in date" |
| Employment / HR | "employee ID", "start date", "probation period", "salary", "reporting manager" |
| Medical / Health | "patient name", "symptoms", "allergies", "emergency contact", "insurance ID" |
| Bank / Financial | "account type", "routing number", "investment objectives", "net worth" |
| Education | "student ID", "GPA", "enrollment date", "major", "institution" |
| Legal / Court | "case number", "plaintiff", "defendant", "filing date", "attorney" |
| Business Registration | "trade name", "registered agent", "business type", "EIN/ABN/CRN" |
| Event / Registration | "dietary preference", "T-shirt size", "emergency contact", "session selection" |
| Generic / Unknown | Infer from field labels; use best-effort matching |

---

## Step 2 — Extract All Fields

Read the document visually (image/screenshot) or structurally (PDF text layer). List every field:

- **Field label** — exactly as printed on the form
- **Field number** — if the form uses numbered fields
- **Field type**: text input, checkbox, radio button, date picker, dropdown, signature, photo upload, table/grid
- **Required vs. optional** — look for asterisks (*), bold labels, "(required)" markers, or form instructions
- **Character limits or format notes** — e.g., "DD/MM/YYYY", "max 50 characters", "BLOCK CAPITALS"
- **Section / group** — which section of the form the field belongs to (e.g., "Section A — Personal Details")
- **Conditional fields** — fields that only apply if a prior question is answered a certain way (flag these)

For multi-page forms, process page by page and number fields sequentially.

---

## Step 3 — Request User Data (if needed)

### Data handling notice — show this before collecting any personal data

Before asking for personal details, state clearly:

> "To fill this form I'll need some of your personal information. A few things to know before you share it:
> - Your data is used **only** to populate this form in this session.
> - It is **not** written to any file, stored in the timeline, or retained after the conversation ends.
> - You can share only the fields that apply — you don't need to provide anything you're not comfortable sharing.
> - Any field you skip will be marked [MISSING] in the output.
>
> You can share your details all at once (fastest) or I can ask field by field if you prefer."

If the user prefers field-by-field collection, switch to asking one field at a time in order of how they appear on the form. Do not front-load a large list of sensitive field requests in that case.

### Single-prompt collection (user's choice — fastest)

Ask once, with a tailored prompt scoped to the fields actually present on this form. Do not request fields the form does not contain.

**General prompt template (scope to form's actual fields):**
> "Please share whichever of the following your form requires: full name, date of birth, nationality, passport/ID number, address, phone, email, employer/company, job title, income, and any form-specific info."

**Visa-specific additions (only if these fields exist on the form):**
> "Also: purpose of visit, intended arrival/departure dates, port of entry, prior visa refusals (yes/no), travel history (countries visited last 5 years), sponsor name and address, hotel/accommodation details."

**Medical-specific additions (only if these fields exist on the form):**
> "Also: blood type, known allergies, current medications, insurance provider and policy number, emergency contact."

**Tax-specific additions (only if these fields exist on the form):**
> "Also: tax file/ID number, filing status, gross income, employer EIN, dependents, deductions you'd like to claim."

### Minimum-necessary principle
Only request fields that actually appear on the form. Do not ask for passport number if the form has no passport field. Do not ask for income if the form has no income field.

---

## Step 4 — Match and Fill

Map user-provided data to form fields using the alias table. When multiple aliases match one field, use the most specific match.

### Standard Aliases

| Form Label Variations | Data Field |
|---|---|
| Full Name / Applicant Name / Name in Full / Legal Name | `full_name` |
| Surname / Last Name / Family Name | `last_name` |
| Given Name / First Name / Christian Name / Forename | `first_name` |
| Middle Name / Middle Initial | `middle_name` |
| Date of Birth / DOB / Birth Date / D.O.B. | `dob` (DD/MM/YYYY or as specified) |
| Age | Calculate from DOB |
| Sex / Gender | `sex` |
| Nationality / Citizenship / National of | `nationality` |
| Country of Birth / Place of Birth / Birth Country | `birth_country` |
| City of Birth / Birth City | `birth_city` |
| Passport No. / Document Number / Travel Document | `passport_number` |
| Passport Expiry / Valid Until / Date of Expiry | `passport_expiry` |
| Passport Issue Date / Date of Issue | `passport_issue_date` |
| Issuing Country / Issued By | `passport_issuing_country` |
| National ID / NRIC / NIN / SSN / SIN / TFN | `national_id` |
| Address / Residential Address / Home Address / Permanent Address | `address_line1` |
| Address Line 2 / Apt / Suite / Floor | `address_line2` |
| City / Town / Municipality | `city` |
| State / Province / Region / County | `state` |
| Postal Code / ZIP Code / Postcode / PIN | `postal_code` |
| Country / Country of Residence | `country` |
| Phone / Mobile / Cell / Contact Number | `phone` |
| Home Phone / Landline | `home_phone` |
| Email / Email Address | `email` |
| Occupation / Job Title / Designation / Position | `job_title` |
| Employer / Company Name / Organization / Workplace | `employer` |
| Employer Address / Office Address | `employer_address` |
| Annual Income / Gross Salary / Monthly Salary | `income` |
| Emergency Contact Name | `emergency_contact_name` |
| Emergency Contact Phone | `emergency_contact_phone` |
| Emergency Contact Relationship | `emergency_contact_relationship` |
| Marital Status | `marital_status` |
| Spouse Name / Partner Name | `spouse_name` |
| Number of Dependents / Children | `dependents` |
| Date (of signing) / Signing Date | Today's date |
| Signature | `[SIGNATURE REQUIRED — print and sign manually]` |
| Photo | `[PHOTO REQUIRED — attach passport-sized photo]` |

### Travel & Visa-Specific Aliases

| Form Label Variations | Data Field |
|---|---|
| Purpose of Visit / Reason for Travel | `visit_purpose` |
| Intended Date of Arrival | `arrival_date` |
| Intended Date of Departure | `departure_date` |
| Duration of Stay | Calculate from arrival/departure |
| Port of Entry | `port_of_entry` |
| Countries Visited (last 5/10 years) | `travel_history` (list countries + years) |
| Accommodation in [Country] / Hotel Address | `accommodation_address` |
| Sponsor Name | `sponsor_name` |
| Sponsor Address | `sponsor_address` |
| Sponsor Relationship | `sponsor_relationship` |
| Prior Visa Refusals | `visa_refusals` (yes/no + details) |
| Previous Visa Number | `previous_visa_number` |
| Funds Available / Financial Evidence | `available_funds` |

### Validation Rules

Apply these checks on filled values before presenting output:

| Field | Validation |
|---|---|
| Date fields | Ensure format matches form requirement (DD/MM/YYYY vs. MM/DD/YYYY vs. YYYY-MM-DD) |
| Passport number | Should be non-empty; typically 6–9 alphanumeric characters |
| Phone numbers | Ensure country code if international format required |
| Email | Must contain `@` and a domain |
| Postal codes | Length and format varies by country — note format if unusual |
| Future dates | Arrival/departure must be in the future; warn if passport expires before travel date |
| Passport validity | Flag if passport expires within 6 months of travel — many countries require this |
| Age consistency | Verify DOB-derived age matches any explicit "Age" field |

---

## Step 5 — Output Format

```
## Form Fill: [Form Name or "Uploaded Form"]
Form Type: [e.g., Singapore Student Pass Application]
Total Fields: 42  |  Filled: 38  |  Missing: 3  |  Action Required: 1

### Section A — Personal Information
| # | Field | Value | Type | Status |
|---|---|---|---|---|
| 1 | Surname | SMITH | Text | Filled |
| 2 | Given Name(s) | JOHN MICHAEL | Text | Filled |
| 3 | Date of Birth | 14/03/1990 | Date | Filled |
| 4 | Sex | Male | Dropdown | Filled |
| 5 | Nationality | British | Text | Filled |
| 6 | Passport No. | A1234567 | Text | Filled — verify last 3 digits |
| 7 | Passport Expiry | 22/08/2028 | Date | Filled — valid (>6 months) |

### Section B — Contact Details
| # | Field | Value | Type | Status |
|---|---|---|---|---|
| 8 | Address | 42 Baker Street | Text | Filled |
| 9 | City | London | Text | Filled |
| 10 | Postcode | NW1 6XE | Text | Filled |
| 11 | Country | United Kingdom | Text | Filled |
| 12 | Mobile | +44 7700 900123 | Text | Filled |
| 13 | Email | john.smith@email.com | Text | Filled |

### Section C — Travel Information
| # | Field | Value | Type | Status |
|---|---|---|---|---|
| 14 | Purpose of Visit | Business | Dropdown | Filled |
| 15 | Arrival Date | 15/09/2024 | Date | Filled |
| 16 | Departure Date | 22/09/2024 | Date | Filled |
| 17 | Duration of Stay | 7 days | Calculated | Filled |
| 18 | Accommodation | Marriott Hotel, 320 Orchard Rd | Text | Filled |
| 19 | Prior Visa Refusals | No | Radio | Filled |
| 20 | Mother's Maiden Name | [MISSING — please provide] | Text | Missing |
| 21 | Countries Visited (3 years) | [MISSING — please provide travel history] | Table | Missing |

### Section D — Declarations
| # | Field | Value | Type | Status |
|---|---|---|---|---|
| 22 | Declaration checkbox | Checked | Checkbox | Filled |
| 23 | Date | 05/03/2024 | Date | Filled |
| 24 | Signature | [SIGNATURE REQUIRED] | Signature | Action Required |

---

### Missing Fields (2)
1. **Mother's Maiden Name** — personal data, please provide
2. **Countries Visited (last 3 years)** — list country names and approximate visit years

### Action Required (1)
- **Signature (Field 24)**: must be signed by hand after printing

### Warnings
- Passport expiry (22/08/2028) is >6 months after intended travel — OK
- Field 7 asks for BLOCK CAPITALS — ensure all name fields use uppercase

### Notes
- This form requires 2 passport-sized photos (not included in digital submission)
- The form must be submitted with supporting documents: bank statement (last 3 months), employer letter, hotel booking confirmation
```

---

## Step 6 — Export Options

After presenting the filled table, offer the following:

- **Guided completion**: "Want me to walk through each missing field one by one?"
- **JSON export**: Output all field/value pairs as a JSON object for programmatic use
- **Plain text export**: Key: Value format for easy copy-paste
- **Document checklist**: List all supporting documents typically required for this form type
- **Form-specific guidance**: Provide country/authority-specific tips (e.g., "For Schengen visas, financial evidence must show ≥ €100/day of stay")

### Supporting Document Checklists by Form Type

**Visa Applications (general):**
- Valid passport (>6 months validity, 2 blank pages)
- Passport-sized photos (usually 2, white background, recent)
- Bank statements (last 3–6 months)
- Employer letter / proof of employment
- Travel itinerary / flight bookings
- Hotel / accommodation bookings
- Travel insurance (some countries require this)
- Proof of ties to home country (property, family, employment)

**Tax Forms:**
- Prior year tax return
- W-2 / T4 / PAYG summaries from all employers
- 1099s / T5s for investment income
- Receipts for deductions being claimed

**Rental Applications:**
- Proof of income (pay stubs, employment letter)
- Bank statements (last 2–3 months)
- Reference letters (prior landlords, employer)
- Photo ID
- Credit report (some landlords request this)

**Medical Forms:**
- Insurance card / policy details
- Prior medical records / referrals
- List of current medications
- Vaccination records (if relevant)

---

## General Rules
- Never invent or guess field values. Use `[MISSING — please provide]` for unknown data.
- Never echo full passport/ID numbers — mask middle digits if displaying for confirmation.
- Respect form-specified formats (uppercase, date format, field length limits).
- Conditional fields: only include in output if the triggering condition is met.
- Always flag signature and photo fields as action-required (cannot be automated).

# Output Contract

Use this structure as a response contract, not a rigid template. Include only the sections the question actually needs.

## Response Mode

- `High-confidence`
  Use when the diagnosis and likely treatment path clearly map to one specialty.
- `Provisional`
  Use when the case is symptom-led, multi-path, or clinically underspecified.

When the answer is provisional, say so explicitly in the opening section.

## Visa Response Mode

For mainland-China visa questions, do not use probabilistic language. The opening section must be:

- `Entry route: Confirmed visa-free`
- `Entry route: Confirmed not covered by visa-free / transit policy, check visa route`
- `Entry route: No sufficient official confirmation found`

Use this mode when the user's question is about entry eligibility, visa-free status, transit status, or whether a regular visa is still needed.

## Standard Sections

### 1. Your likely treatment path

- explain the likely specialty route in plain English
- say whether the recommendation is high-confidence or provisional
- name the missing details that could change the route if relevant

### 2. Best-fit hospital options

Recommend 2-3 hospitals by default. For each hospital include:

- English hospital name
- Chinese hospital name
- city
- ranking baseline used
- why this hospital fits this case specifically

Each hospital should have a different angle:

- best specialist-center fit
- best comprehensive or MDT fit
- best practical or regional access fit

### 3. What is confirmed now

Only include facts from:

- the bundled Fudan ranking baseline
- current allowed-source verification

Keep this concise. This section is for confirmed ranking and access facts, not for judgment language.

### 4. What you still need to verify

List open items that could affect booking or hospital choice, such as:

- pathology or imaging details
- surgery-first vs evaluation-first direction
- hospital intake route for foreign patients
- teleconsult or remote review availability
- visa or payment specifics

### 5. Suggested next steps

Give 2-4 concrete next actions. Examples:

- gather pathology, imaging, and prior treatment summary
- contact the shortlisted department or hospital intake channel
- confirm visa and self-pay process
- compare one specialist-center option with one comprehensive option

## Optional CTA

Only add service CTA if `cta-policy.md` says the case qualifies.

## Visa-Specific Sections

When the user is asking about mainland-China entry or visa status, use these sections instead of the hospital-shortlist layout:

### 1. Entry route

- one of the 3 allowed states above

### 2. Official basis checked

- identify the official policy branch checked
- state only what the official evidence actually supports

### 3. What is still missing

- passport type
- purpose of visit
- intended stay duration
- itinerary and third-destination details for transit cases
- policy validity-window confirmation if not clearly found

### 4. Next official step

- proceed under confirmed visa-free rules
- verify transit conditions
- check visa category and application flow

Do not use `likely`, `probably`, or similar language in any visa-specific section.

# Form Field Mappings Reference

This document maps common job application form field labels to their data sources
in the ResumeX resume JSON and `user_preferences.json`. The agent uses this to
automatically fill form fields during the auto-apply workflow.

---

## Priority Order for Resolving Field Values

When the agent encounters a form field, it looks for the value in this order:

1. **Resume data** (from ResumeX API) — always fresh, always authoritative
2. **User preferences** (`data/user_preferences.json`) — saved answers from previous sessions
3. **Derived data** (calculated by the agent) — years of experience, name splits, etc.
4. **Generated content** (LLM-generated) — cover letters, interest statements
5. **Ask the user** (last resort) — pause, ask, save to preferences for next time

---

## Personal Information Fields

| Form Label Variants | Source | JSON Path | Transform | Notes |
|---|---|---|---|---|
| First Name, fname, first_name | Resume | `profile.fullName` | Split → take first word | |
| Last Name, lname, last_name | Resume | `profile.fullName` | Split → take last word | |
| Full Name, name | Resume | `profile.fullName` | None | |
| Email, email address, e-mail | Resume | `profile.email` | None | |
| Phone, phone number, mobile, contact number | Resume | `profile.phone` | None | |
| Location, current location | Resume | `profile.location` | None | |
| City | Preferences → Resume | `city` → `profile.location` | Extract before comma | |
| State, state/province | Preferences | `state` | None | Ask if not saved |
| Country | Preferences | `country` | None | Ask if not saved |
| ZIP Code, postal code | Preferences | `zip_code` | None | Ask if not saved |
| Street Address, address | Preferences | `address_line1` | None | Ask if not saved |
| Date of Birth, DOB | Preferences | `date_of_birth` | None | Ask if not saved |

---

## Professional Links

| Form Label Variants | Source | JSON Path | Notes |
|---|---|---|---|
| LinkedIn, LinkedIn URL, LinkedIn Profile | Resume | `profile.linkedin` | |
| GitHub, GitHub URL | Resume | `profile.github` | |
| Website, Portfolio, Portfolio URL | Resume | `profile.website` | |

---

## Current Employment

| Form Label Variants | Source | JSON Path | Notes |
|---|---|---|---|
| Current Company, Current Employer | Resume | `experience[0].company` | Most recent entry |
| Current Title, Current Role, Current Position, Current Job Title | Resume | `experience[0].role` | Most recent entry |
| Years of Experience, Total Experience, Work Experience | Derived | Calculate from dates | `current_year - min(startDate years)` |

---

## Education

| Form Label Variants | Source | JSON Path | Fallback |
|---|---|---|---|
| Highest Education, Degree | Resume → Prefs | `education[0].degree` | `highest_education` pref |
| University, College, Institution | Resume | `education[0].institution` | |
| Graduation Year | Resume → Prefs | `education[0].endDate` | `graduation_year` pref |
| GPA, Score, CGPA | Resume | `education[0].score` | |

---

## Compensation & Preferences (Not in Resume)

These fields are **never** in the ResumeX resume. They come from `user_preferences.json`
or must be asked from the user on first encounter.

| Form Label Variants | Preference Key | Example Values | Notes |
|---|---|---|---|
| Salary Expectation, Expected Salary | `salary_expectation` | "8-12 LPA", "$80K-$100K" | Always ask first time |
| Current CTC, Current Salary | `current_ctc` | "6 LPA", "$70K" | |
| Expected CTC | `expected_ctc` | "10 LPA", "$90K" | |
| Currency | `currency` | "INR", "USD" | |
| Notice Period | `notice_period` | "30 days", "Immediate", "2 months" | |
| Visa Status | `visa_status` | "Indian citizen", "H1B" | |
| Work Authorization | `work_authorization` | "Authorized to work in India" | |
| Willing to Relocate | `willing_to_relocate` | true/false | |
| Preferred Work Type | `preferred_work_type` | "remote", "hybrid", "onsite" | |

---

## Diversity & Compliance Fields (Optional)

These are often asked on US/EU job applications. The agent should present options
and let the user select. Save for reuse.

| Form Label Variants | Preference Key | Example Values | Notes |
|---|---|---|---|
| Gender | `gender` | "Male", "Female", "Non-binary", "Prefer not to say" | Usually dropdown |
| Ethnicity, Race | `ethnicity` | "Asian", "Prefer not to say" | Usually dropdown |
| Disability Status | `disability_status` | "No", "Yes", "Prefer not to say" | |
| Veteran Status | `veteran_status` | "No", "Yes", "Prefer not to say" | |

---

## Generated Content Fields

| Form Label Variants | Source | Generation Method |
|---|---|---|
| Cover Letter, Additional Information | `draft_cover_letter.py` | LLM-generated from resume + JD |
| Why interested, Why this role | LLM | Generate from resume + company + JD |
| Experience with [X] | LLM | Match `[X]` against resume experience/skills, generate narrative |

---

## File Upload Fields (Skip)

These fields require file uploads which the agent cannot handle automatically.
Mark them for user completion.

| Form Label Variants | Action |
|---|---|
| Resume, CV, Upload Resume, Upload CV, Resume/CV | ⚠️ Skip — note for user |
| Portfolio, Work Samples | ⚠️ Skip — note for user |
| Cover Letter (file) | ⚠️ Skip if file upload; fill if textarea |

---

## How to Use This Reference

### For the Agent:

1. When analyzing a form field, normalize the label to lowercase
2. Match against the "Form Label Variants" column (fuzzy/partial match OK)
3. Use the sources in priority order: Resume → Preferences → Derived → Ask
4. If a field is `ask_user`, present the field name and ask. After getting the answer, save:
   ```bash
   python3 scripts/manage_preferences.py set "{preference_key}" "{user_answer}"
   ```
5. File upload fields should be **skipped** and noted in the summary.

### For the `fill_application.py` Script:

The script contains the full mapping as Python dicts. Use it programmatically:

```bash
# Map all form fields at once
python3 scripts/fill_application.py map-fields \
  --resume /tmp/resume.json \
  --prefs data/user_preferences.json \
  --fields '[{"label":"First Name"},{"label":"Email"},{"label":"Salary Expectation"}]'

# Check how many fields can be auto-filled
python3 scripts/fill_application.py check-coverage \
  --resume /tmp/resume.json \
  --prefs data/user_preferences.json \
  --fields '[{"label":"First Name"},{"label":"Salary"},{"label":"Visa Status"}]'
```

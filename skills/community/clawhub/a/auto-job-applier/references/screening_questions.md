# Screening Questions Reference

Common screening questions found on job application forms and how the agent should
handle each one. The agent checks `user_preferences.json` before asking the user,
and saves every new answer for future reuse.

---

## Handling Strategy

```
1. Read the question text from the form
2. Normalize it (lowercase, strip punctuation)
3. Fuzzy-match against saved screening answers:
   python3 scripts/manage_preferences.py find-screening "question text here"
4. If found → use saved answer
5. If not → present to user:
   "The application for [Company] asks: [Question]. What should I answer?"
   Show available options if it's a dropdown/radio/checkbox.
6. Save the answer:
   python3 scripts/manage_preferences.py set-screening "question_key" "answer"
7. Fill the form field
```

---

## Yes/No Questions

These are the most common screening questions. Store as boolean or "Yes"/"No".

| Question Pattern | Preference Key | Default Strategy |
|---|---|---|
| Are you authorized to work in [country]? | `authorized_to_work_{country}` | Check `visa_status`. If "Indian citizen" and country is India → "Yes" |
| Do you require visa sponsorship? | `require_sponsorship` | Derive from `visa_status`. If citizen → "No" |
| Are you willing to relocate? | `willing_to_relocate` | Check `willing_to_relocate` pref |
| Are you willing to travel? | `willing_to_travel` | Ask user if not saved |
| Are you 18 years or older? | `is_18_or_older` | Default "Yes" (reasonable assumption for job applicants) |
| Have you previously worked at [company]? | `worked_at_{company}` | Default "No" unless resume shows otherwise |
| Have you been referred by an employee? | `has_referral` | Default "No" unless user says otherwise |
| Do you have a valid driver's license? | `has_drivers_license` | Ask user |
| Are you currently employed? | `currently_employed` | Check if `experience[0].endDate` is "Present" |
| Will you now or in the future require sponsorship? | `future_sponsorship` | Same as `require_sponsorship` |
| Can you commute to [location]? | `can_commute_{location}` | Check if `profile.location` matches |
| Do you agree to a background check? | `agree_background_check` | Default "Yes" |
| Do you agree to drug screening? | `agree_drug_screening` | Default "Yes" |

---

## Multiple Choice Questions

Present the options to the user. Many of these have standard answers that can be saved.

| Question Pattern | Preference Key | Typical Options | Strategy |
|---|---|---|---|
| What is your highest level of education? | `highest_education` | High School, Bachelor's, Master's, PhD | Check `education[0].degree`, map to level |
| How many years of experience with [skill]? | `years_exp_{skill}` | 0-1, 1-3, 3-5, 5-10, 10+ | Estimate from resume if skill appears in experience |
| What is your proficiency in [language]? | `proficiency_{language}` | Beginner, Intermediate, Advanced, Fluent, Native | Ask user |
| What is your expected start date? | `expected_start_date` | Immediately, 2 weeks, 1 month, Other | Derive from `notice_period` |
| Preferred work arrangement? | `preferred_work_type` | Remote, Hybrid, On-site | Check pref |
| Employment type preference? | `employment_type_pref` | Full-time, Part-time, Contract | Check `JOB_TYPE` env var |

### Education Level Mapping

Map the `education[0].degree` field to standard education levels:

| Resume Degree Contains | Maps To |
|---|---|
| "PhD", "Doctorate", "D.Phil" | "Doctorate" |
| "M.S.", "M.Tech", "Master", "MBA", "M.Sc" | "Master's Degree" |
| "B.Tech", "B.S.", "B.E.", "Bachelor", "B.Sc", "BCA" | "Bachelor's Degree" |
| "Diploma", "Associate" | "Associate's Degree" |
| "12th", "HSC", "High School" | "High School" |

---

## Free Text Questions

These require LLM-generated responses using resume data + job context.

| Question Pattern | Generation Strategy | Preference Key |
|---|---|---|
| Why are you interested in this role? | LLM: Use company name + role + user's relevant skills/experience | `interest_template` (save template, customize per job) |
| Tell us about yourself | LLM: Use `profile.summary` as base, customize for role | Reuse `profile.summary` |
| Describe your experience with [technology] | LLM: Find [technology] in skills/experience, generate 2-3 sentences | Cache per technology |
| What are your strengths? | LLM: Extract top achievements + skills from resume | `strengths_answer` |
| What are your career goals? | LLM: Infer from experience trajectory + role being applied to | `career_goals` |
| Why are you leaving your current role? | User must answer — too personal to generate | `reason_for_leaving` |
| What is your greatest achievement? | LLM: Pick top achievement from `achievements[]` or experience | `greatest_achievement` |
| Additional information | Use cover letter text or leave blank | Cover letter |

### Important: Free text is context-dependent

For free text questions, the agent should:
1. Generate an answer using the LLM, incorporating:
   - The specific company name and role
   - Relevant skills and experience from the resume
   - The job description context
2. Keep answers concise (2-4 sentences max)
3. Show the generated answer to the user for review if it's the first time
4. Save templates (with `{company}` and `{role}` placeholders) for reuse

---

## Numeric Input Questions

| Question Pattern | Preference Key | Strategy |
|---|---|---|
| Expected salary (number field) | `salary_expectation_number` | Parse number from `salary_expectation` pref |
| Years of total experience | Derived | Calculate from resume |
| Years of experience with [X] | `years_exp_{x}` | Estimate or ask |
| GPA / CGPA | Resume | `education[0].score` |
| Contact number | Resume | `profile.phone` |

---

## Date Questions

| Question Pattern | Preference Key | Strategy |
|---|---|---|
| Earliest start date | `earliest_start_date` | Derive from `notice_period` + today |
| Date of birth | `date_of_birth` | Ask user if not saved |
| Graduation date | Resume | `education[0].endDate` |

---

## File Upload Questions

Always skip and note for user.

| Question Pattern | Action |
|---|---|
| Upload Resume / CV | ⚠️ Skip — "Resume upload required, please upload manually" |
| Upload Cover Letter | ⚠️ Skip — provide cover letter text in notes |
| Upload Portfolio / Work Samples | ⚠️ Skip |
| Upload Certificates | ⚠️ Skip |

---

## Managing Screening Answers

### Save an answer
```bash
python3 scripts/manage_preferences.py set-screening "authorized_to_work_india" "Yes"
python3 scripts/manage_preferences.py set-screening "salary_expectation_number" "1000000"
python3 scripts/manage_preferences.py set-screening "willing_to_relocate" "Yes"
```

### Find a saved answer by question text
```bash
python3 scripts/manage_preferences.py find-screening "Are you authorized to work"
# Returns: {found: true, key: "authorized_to_work_india", value: "Yes", confidence: 0.67}
```

### List all saved screening answers
```bash
python3 scripts/manage_preferences.py get screening_answers
```

---

## Rules for the Agent

1. **Never skip a required screening question** — always fill or ask the user.
2. **Optional questions can be left blank** if no answer is saved.
3. **Show generated free-text answers to the user on first occurrence** — let them approve or edit before saving the template.
4. **Diversity questions are always optional** — use "Prefer not to say" if the user hasn't explicitly provided answers.
5. **Don't assume answers** for sensitive fields (salary, visa) — always ask on first encounter.
6. **Save answers at the most general level possible** — `authorized_to_work_india` rather than `authorized_to_work_acme_corp`.

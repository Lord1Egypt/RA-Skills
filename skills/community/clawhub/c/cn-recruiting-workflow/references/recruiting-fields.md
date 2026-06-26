# Recruiting Fields Reference

Use this reference when the user needs stronger normalization for recruiting documents and workflow records used in China.

## JD fields

```text
job_title
department
hiring_manager
location
employment_type
must_have_skills
preferred_skills
years_of_experience
education_requirement
industry_background
language_requirement
salary_range
urgency
interview_stages
```

## Resume fields

```text
candidate_name
current_title
years_of_experience
education
industry_experience
core_skills
company_history
project_highlights
management_scope
stability_signals
salary_expectation
availability
location
```

## Interview feedback fields

```text
interviewer_name
interview_round
capability_feedback
experience_feedback
motivation_feedback
communication_feedback
culture_fit_feedback
salary_risk
stability_risk
hire_recommendation
follow_up_questions
confidence_level
```

## Offer approval fields

```text
candidate_name
target_role
department
reporting_line
work_location
employment_entity
base_salary
bonus_scheme
trial_period
expected_onboard_date
budget_range
approver_chain
interview_summary
risk_notes
```

## Common source formats

1. JD: Word, PDF, Feishu doc, pasted text, or email body
2. Resume: PDF, DOCX, OCR text, recruiter notes, or ATS export
3. Interview feedback: form fields, Feishu/WeCom chat, email, call notes, or voice transcription
4. Approval pack inputs: spreadsheet rows, approval forms, salary bands, or hiring manager notes

## Recommended record-update shape

```text
candidate_name
target_role
stage
decision
risk_flags
owner
next_action
last_update_summary
```

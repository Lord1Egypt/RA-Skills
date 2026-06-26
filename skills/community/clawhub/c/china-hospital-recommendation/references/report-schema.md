# Report Schema

## `ReportRequest`

Raw request and order context.

```json
{
  "report_id": "string",
  "created_at": "YYYY-MM-DD",
  "output_language": "en",
  "patient": {
    "name": "string?",
    "country": "string",
    "condition_summary": "string",
    "preferred_city": "string?",
    "travel_time": "string?",
    "budget_range": "string?"
  },
  "report_preferences": {
    "hospital_count": 3
  },
  "hospital_count_reason": "string?"
}
```

Defaults:

- `output_language = "en"`
- `report_preferences.hospital_count = 3`
- more than 3 hospitals requires `hospital_count_reason`

## `ReportResearchModel`

Internal working structure used before rendering.

```json
{
  "specialties": ["肿瘤学"],
  "ranking_basis": "Fudan 2025 static snapshot",
  "hospital_candidates": [],
  "specialist_candidates": [],
  "search_findings": {
    "hospital_services": [],
    "specialist_profiles": [],
    "travel_logistics": []
  },
  "recommendation_judgment": {
    "why_these_hospitals": [],
    "why_these_specialist_directions": []
  }
}
```

## `RenderedReportModel`

Stable payload for `scripts/render_report.py`.

```json
{
  "report_id": "string",
  "created_at": "YYYY-MM-DD",
  "output_language": "en",
  "patient": {},
  "summary": {
    "top_takeaway": "string",
    "executive_summary": "string",
    "clinical_focus": "string",
    "recommendation_logic": "string",
    "recommended_length_of_stay": "string?",
    "uncertainty_note": "string?",
    "current_limitations": ["string"]
  },
  "comparison_summary": [],
  "hospitals": [],
  "specialists": [],
  "cost_estimate": {},
  "travel": {},
  "next_steps": [],
  "evidence_notes": [],
  "disclaimer": "string"
}
```

Additional optional hospital fields:

- `patient_facing_summary`
- `best_for`
- `potential_limitation`
- `access_evidence_level`
- `international_access`
- `remote_consultation_note`
- `cost_scenarios`
- `recommendation_role`
- `jci_status`
- `jci_last_verified`
- `jci_note`
- `booking_guidance`

Structured additions preferred for new reports:

- `hospital.access_evidence_level`: `verified | partially_verified | needs_manual_confirmation | not_provided`
- `hospital.international_access.admin_intake_status`
- `hospital.international_access.record_review_status`
- `hospital.international_access.doctor_teleconsult_status`
- `hospital.international_access.evidence_note`
- `hospital.remote_consultation_note`
- `hospital.cost_scenarios.consult_only`
- `hospital.cost_scenarios.consult_plus_repeat_workup`
- `hospital.cost_scenarios.procedure_or_admission_path`
- `hospital.cost_scenarios.systemic_treatment_path`
- `hospital.recommendation_role`
- `specialists[].intent_gate`
- `comparison_summary[].international_access_evidence`
- `comparison_summary[].cost_positioning`

Backward compatibility rule:

- legacy fields remain valid
- renderers should prefer structured fields when present
- when structured fields are missing, output must downgrade to conservative wording instead of inferring strong claims from prose

Required rendered sections:

1. Top Takeaway
2. Your Situation at a Glance
3. Why These Hospitals Were Chosen
4. Quick Comparison
5. Recommended Hospitals
6. Recommended Specialist Directions
7. Expected Costs
8. Travel and Visa Planning
9. What You Should Do Next
10. Evidence Notes
11. Important Disclaimer

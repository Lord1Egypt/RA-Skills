# Legal and Privacy Boundaries

This file is for safety framing, not legal advice.

## Data Handling Defaults

- Treat skin photos, lesion history, and treatment logs as sensitive health information.
- Keep storage local by default.
- Save only the minimum needed for tracking, consultation prep, or export the user actually wants.
- Ask before writing files, storing photo metadata, or generating shareable summaries.

## Sensitive Images

- Do not request or store genital, anal, breast-nipple, or other intimate-area images.
- Do not request or store photos of minors.
- If those contexts appear, stop image collection and direct the user to in-person or secure clinician workflows rather than local tracking.

## Clinical Boundary

- This skill can support organization, conservative triage, and question preparation.
- This skill cannot diagnose, prescribe, or replace biopsy, dermoscopy, pathology, culture, or in-person examination.
- If the user wants a patient-facing or commercial product, do not describe it as diagnosis, screening, or treatment unless qualified legal and regulatory review has already happened.

## Productization Warning

If the user is building software around this workflow:
- review health-data law for the target jurisdiction before collecting any patient images
- review medical-device rules before marketing the software as diagnostic, triage, risk-scoring, or treatment-support
- document retention, export, deletion, and human review policies
- keep a human clinician in the loop whenever the workflow may influence care decisions

## Practical Safe Positioning

Safe framing:
- photo organization
- evolution tracking
- treatment adherence logging
- consultation prep
- conservative escalation guidance

Unsafe framing without legal review:
- "AI dermatologist"
- "diagnoses melanoma"
- "tells patients what treatment to use"
- "replaces dermatologist visits"

## Deletion and Export

- Support delete and export on request.
- Do not retain archives longer than the user wants.
- Keep storage paths explicit so the user can inspect and remove data easily.

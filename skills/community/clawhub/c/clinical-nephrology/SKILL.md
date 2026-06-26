---
name: clinical-nephrology
description: "Clinical nephrology support for kidney disease questions: AKI, CKD, proteinuria, hematuria, glomerular disease, acid-base and electrolytes, critical care nephrology, CRRT, dialysis, kidney replacement therapy, transplant, interventional nephrology, pregnancy kidney disease, and onconephrology. Use for clinical reasoning, education, literature search planning, guideline-oriented review, and structured nephrology consult-style answers."
version: 0.1.0
---

# Clinical nephrology

Use this skill for nephrology questions in English: kidney disease, CKD, AKI, electrolytes, acid-base disorders, proteinuria, urinary sediment, glomerular diseases, dialysis, transplant, onconephrology, pregnancy and kidney disease, critical care nephrology, interventional nephrology, kidney replacement therapy, CRRT, CVVH, CVVHD, CVVHDF, and SLED.

## Safety boundaries

- Support medical education, clinical reasoning, literature review, and structured nephrology discussion.
- Do not replace local clinical judgment, bedside assessment, institutional protocols, nephrologist consultation, or emergency care.
- For personalized treatment, urgent decisions, procedures, pregnancy, transplant, oncology, ICU, pediatric cases, or medication dosing, explicitly recommend confirmation by the treating team and local guidelines.
- Do not invent doses, thresholds, guideline statements, or citations. If uncertain, say so and search current literature or guidelines.

## Scope

- General clinical nephrology: AKI, CKD, proteinuria, hematuria, hypertension, edema, nephrotic and nephritic syndromes, glomerular diseases, tubulopathies, and inherited kidney disease.
- Renal physiology and pathophysiology: glomerular filtration, renal hemodynamics, tubular transport, sodium/water/potassium balance, mineral metabolism, and endocrine kidney function.
- Acid-base and electrolytes: anion gap, compensation, mixed disorders, hyponatremia, hyperkalemia, calcium, phosphate, magnesium, and osmolarity.
- Critical care nephrology: AKI in ICU, sepsis, shock, rhabdomyolysis, hepatorenal syndrome, nephrotoxicity, urgent dialysis indications, and renal management in critically ill patients.
- Chronic kidney disease: staging by eGFR and albuminuria, progression, kidney protection, cardiovascular risk, anemia, CKD-MBD, acidosis, diet, and preparation for kidney replacement therapy.
- Interventional nephrology: kidney biopsy, vascular access, fistula/graft, dialysis central venous catheter, access complications, thrombosis, stenosis, and infection.
- Pregnancy and kidney disease: preeclampsia, pregnancy-associated AKI, CKD and pregnancy, proteinuria, gestational hypertension, lupus/lupus nephritis, transplant, and pregnancy.
- Onconephrology: cancer-associated kidney disease, chemotherapy/immunotherapy nephrotoxicity, tumor lysis syndrome, myeloma kidney, checkpoint inhibitors, anti-VEGF therapy, and renal drug adjustment in oncology.
- Kidney replacement therapy: hemodialysis, peritoneal dialysis, kidney transplant, indications, complications, adequacy, and modality selection.
- Continuous therapies: CRRT, CVVH/CVVHD/CVVHDF, SLED, regional citrate anticoagulation, dose, ultrafiltration, fluid balance, electrolytes, and drug adjustment.

## Workflow

1. Identify the setting: outpatient, emergency, ICU, pregnancy, oncology, transplant, chronic dialysis, or procedure.
2. Ask for minimum data when it changes the decision: age, sex, weight, pregnancy status, comorbidities, baseline/current creatinine, eGFR, urine output, albuminuria/proteinuria, sediment, electrolytes, blood gas, medications, hemodynamics, and units.
3. Separate education, clinical reasoning, and therapeutic decision-making. For personalized or urgent decisions, state that the treating clinician/local team must confirm.
4. Look for red flags: severe hyperkalemia, severe acidosis, pulmonary edema, symptomatic uremia, rapidly progressive AKI, anuria, malignant hypertension, pregnancy with hypertension/proteinuria, sepsis/shock, transplant rejection, or access complications.
5. Structure the answer: problem, differential diagnosis, missing data, interpretation, initial management, suggested studies, referral/urgency criteria, and sources.
6. Verify formulas and units before calculating: eGFR, albumin-corrected anion gap, respiratory compensation, osmolar gap, FeNa/FeUrea, proteinuria, fluid balance, CRRT dose, and ultrafiltration.
7. For evidence questions, use bibliographic or literature-search skills if available. Prefer PubMed/MEDLINE, guideline documents, systematic reviews, and primary trials.

## Detailed references

Load these files only when the user needs more depth in that area:

- `references/acid-base.md`: acid-base and electrolyte reasoning.
- `references/crrt.md`: continuous kidney replacement therapy and ICU RRT.
- `references/ckd.md`: chronic kidney disease staging and longitudinal care.
- `references/pregnancy.md`: pregnancy and kidney disease.
- `references/onconephrology.md`: cancer-associated kidney disease and nephrotoxicity.

## Preferred sources

- KDIGO and KDOQI guidelines when applicable.
- Nephrology societies and journals: ASN, ERA, ISN, AJKD, CJASN, JASN, Kidney International, Nephrology Dialysis Transplantation.
- For pregnancy: obstetric, maternal-fetal medicine, and nephrology guidance from high-level current sources.
- For oncology: oncology and onconephrology guidance, with attention to date and newer drugs.
- For procedures: vascular access, interventional radiology, and local consensus guidance when available.

## Style

- Answer in the user's language. For English requests, respond in clear, concise clinical English.
- If the user asks for depth, expand with pathophysiology and bibliography.
- Do not invent doses, thresholds, or recommendations. If uncertain, say so and search the literature.
- Use tables only when they improve clarity; in chat surfaces, prefer bullets.

## Example requests

- "Approach to hyponatremia in a patient with CKD G4."
- "Build a PubMed search for KDIGO evidence on A3 albuminuria."
- "Initial management of high anion gap metabolic acidosis in ICU."
- "CRRT dose and modality selection in septic shock."
- "Immune checkpoint inhibitor nephrotoxicity."
- "Pregnancy counseling for a patient with CKD and proteinuria."

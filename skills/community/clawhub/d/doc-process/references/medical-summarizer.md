# Medical Document Summarizer — Reference Guide

## Purpose
Convert lab reports, prescriptions, discharge summaries, imaging reports, pathology reports, and other medical documents into clear, plain-English summaries that a non-specialist patient can understand. Flag critical values and provide actionable next-step guidance.

---

## Step 1 — Document Type Detection

| Document Type | Key Signals |
|---|---|
| Lab / Blood test report | Panel names (CBC, BMP, LFT), reference ranges, result values with units |
| Prescription (Rx) | Drug names, "SIG:", "Dispense:", prescriber's DEA/license number |
| Discharge summary | "Admission date", "Discharge date", "Diagnosis", "Follow-up" |
| Radiology / Imaging | "Impression", "Findings", modality (X-ray, CT, MRI, PET, Ultrasound) |
| Pathology report | "Specimen", "Histology", "Gross description", "Microscopic description" |
| Vaccination record | Vaccine names, lot numbers, administration dates |
| ECG / EKG report | "Rhythm", "PR interval", "QRS", "QT interval", "Axis" |
| Referral letter | "Refer to", "Specialist", chief complaint description |
| Insurance / EOB | "Explanation of Benefits", CPT codes, billed vs. allowed amounts |

---

## Template A — Lab / Blood Test Report

### Patient & Test Info
| Field | Value |
|---|---|
| Patient Name | |
| Patient DOB / Age | |
| Date of Collection | |
| Date of Report | |
| Ordering Physician | |
| Lab Name & CLIA | |
| Sample Type | Venous blood / Capillary / Urine / Stool / Saliva / CSF |
| Fasting? | Yes / No / Unknown |

### Results Table

For each test or panel, output:
| Test | Your Value | Unit | Reference Range | Flag | Plain-English Meaning |
|---|---|---|---|---|---|

**Flag values:**
- **NORMAL** — within reference range
- **LOW** — below lower limit
- **HIGH** — above upper limit
- **CRITICAL LOW** — below critical alert threshold (flag prominently)
- **CRITICAL HIGH** — above critical alert threshold (flag prominently)
- **DETECTED** — positive result for qualitative test
- **NOT DETECTED** — negative result
- **EQUIVOCAL** — borderline / indeterminate

### Critical Alert Block
If any CRITICAL value is found, display prominently at the top:
```
⚠ CRITICAL VALUE DETECTED
Test: [Name]
Your value: [X] [units] — [CRITICAL HIGH / LOW]
Reference range: [range]
What this may mean: [brief plain-English explanation]
Action: Contact your healthcare provider immediately or go to the nearest emergency department.
```

### Common Panel Reference Tables

#### Complete Blood Count (CBC)
| Test | Typical Range (Adult) | What It Measures |
|---|---|---|
| WBC (White Blood Cells) | 4.5–11.0 × 10³/µL | Immune system cells; high = infection/inflammation; low = immune issues |
| RBC (Red Blood Cells) | M: 4.7–6.1; F: 4.2–5.4 × 10⁶/µL | Oxygen-carrying cells |
| Hemoglobin (Hgb) | M: 13.5–17.5; F: 12.0–15.5 g/dL | Oxygen-carrying protein; low = anemia |
| Hematocrit (Hct) | M: 41–53%; F: 36–46% | % of blood volume made up of red cells |
| MCV | 80–100 fL | Size of red blood cells |
| MCH | 27–33 pg | Hemoglobin per red cell |
| MCHC | 32–36 g/dL | Hemoglobin concentration in red cells |
| Platelets | 150–400 × 10³/µL | Clotting; low = bleeding risk; high = clot risk |
| Neutrophils | 40–70% | Main infection-fighting white cells |
| Lymphocytes | 20–40% | Viral defense, antibody production |
| Monocytes | 2–8% | Cleanup crew; elevated in chronic infection |
| Eosinophils | 1–4% | Allergy / parasite response |
| Basophils | 0.5–1% | Allergic / inflammatory response |

#### Basic Metabolic Panel (BMP)
| Test | Typical Range | What It Measures |
|---|---|---|
| Glucose | 70–99 mg/dL (fasting) | Blood sugar |
| BUN | 7–20 mg/dL | Kidney waste product from protein |
| Creatinine | M: 0.74–1.35; F: 0.59–1.04 mg/dL | Kidney filter marker |
| eGFR | ≥60 mL/min/1.73m² | Kidney filtration rate |
| Sodium (Na) | 136–145 mEq/L | Fluid/nerve balance |
| Potassium (K) | 3.5–5.1 mEq/L | Heart and muscle function |
| Chloride (Cl) | 98–107 mEq/L | Fluid balance |
| Bicarbonate (CO₂) | 22–29 mEq/L | Acid-base balance |
| Calcium | 8.6–10.2 mg/dL | Bone, nerve, muscle |

#### Lipid Panel
| Test | Optimal / Normal | What It Measures |
|---|---|---|
| Total Cholesterol | <200 mg/dL | Overall cholesterol burden |
| LDL ("bad") | <100 mg/dL (optimal); <70 if high-risk | Plaque-forming cholesterol |
| HDL ("good") | M: >40; F: >50 mg/dL (higher is better) | Heart-protective cholesterol |
| Triglycerides | <150 mg/dL | Blood fats; high = metabolic risk |
| Non-HDL Cholesterol | <130 mg/dL | Total minus HDL |
| LDL/HDL ratio | <3.0 | Cardiovascular risk ratio |

#### Liver Function Tests (LFT)
| Test | Typical Range | What It Measures |
|---|---|---|
| ALT | 7–56 U/L | Liver cell enzyme; elevated = liver damage |
| AST | 10–40 U/L | Liver + muscle enzyme |
| ALP | 44–147 U/L | Bile duct and bone |
| GGT | M: 9–48; F: 0–36 U/L | Alcohol and bile duct marker |
| Total Bilirubin | 0.2–1.2 mg/dL | Bile pigment; high = jaundice |
| Direct Bilirubin | 0.0–0.3 mg/dL | Processed bilirubin |
| Albumin | 3.4–5.4 g/dL | Protein made by liver; low = liver/nutrition issues |
| Total Protein | 6.3–8.2 g/dL | All blood proteins |

#### Thyroid
| Test | Typical Range | What It Measures |
|---|---|---|
| TSH | 0.4–4.0 mIU/L | Master thyroid controller; high = hypothyroid |
| Free T4 | 0.8–1.8 ng/dL | Active thyroid hormone |
| Free T3 | 2.3–4.1 pg/mL | Active form of T3 |
| Anti-TPO | <35 IU/mL | Autoimmune thyroid marker |
| Anti-TG | <115 IU/mL | Autoimmune thyroid marker |

#### Diabetes / Blood Sugar
| Test | Diagnostic Range | Meaning |
|---|---|---|
| Fasting glucose | <100: Normal; 100–125: Prediabetes; ≥126: Diabetes | |
| HbA1c | <5.7%: Normal; 5.7–6.4%: Prediabetes; ≥6.5%: Diabetes | 3-month average blood sugar |
| Fasting insulin | 2–20 µIU/mL | Insulin resistance if high |
| HOMA-IR | <2.0 (fasting glucose×insulin/405) | Insulin resistance index |

#### Urinalysis
| Test | Normal | Abnormal Meaning |
|---|---|---|
| pH | 4.5–8.0 | |
| Specific gravity | 1.002–1.030 | Low = dilute; High = dehydrated |
| Protein | Negative | Present = kidney damage |
| Glucose | Negative | Present = diabetes or kidney issue |
| Ketones | Negative | Present = starvation or DKA |
| Blood (hematuria) | Negative | Present = infection, stones, or kidney disease |
| Nitrites | Negative | Present = bacteria (UTI) |
| Leukocyte esterase | Negative | Present = WBC (infection) |
| RBC casts | None | Kidney disease |
| WBC casts | None | Kidney infection |

#### Inflammatory Markers
| Test | Typical Range | What It Measures |
|---|---|---|
| CRP (C-reactive protein) | <1.0 mg/dL; hs-CRP <1.0 mg/L (low CV risk) | General inflammation / infection |
| ESR | M: <15; F: <20 mm/hr (age-adjusted) | Chronic inflammation |
| Ferritin | M: 12–300; F: 12–150 ng/mL | Iron storage; high = inflammation |
| IL-6 | <7 pg/mL | Cytokine; elevated in severe infection |
| D-dimer | <0.5 µg/mL | Clot degradation; high = possible DVT/PE |

---

## Template B — Prescription (Rx)

### Rx Header
| Field | Value |
|---|---|
| Patient | |
| Date | |
| Prescribing Doctor | |
| Practice / Clinic | |
| License / DEA # | |

### Medications Prescribed
For each medication:

| Field | Value |
|---|---|
| Medication name | Generic + brand name |
| Drug class | e.g., SSRI, ACE inhibitor, statin, beta-blocker |
| Dose | e.g., 20 mg |
| Dosage form | Tablet, capsule, liquid, patch, inhaler, injection |
| Route | Oral (PO), sublingual (SL), topical, inhaled, IV, IM, SC |
| Frequency | QD=once daily, BID=twice, TID=3×, QID=4×, PRN=as needed |
| Duration | e.g., 7 days, 30 days, until review |
| Instructions | Take with food / on empty stomach / at bedtime |
| Quantity dispensed | e.g., #30 tablets |
| Refills | e.g., 2 refills |
| Purpose (plain English) | e.g., "antibiotic to treat your urinary tract infection" |

### Common Side Effects (by drug class)
| Drug | Common Side Effects | Serious — Seek Help If |
|---|---|---|
| SSRIs (e.g., sertraline) | Nausea, insomnia, headache, sexual dysfunction | Serotonin syndrome (confusion, rapid heart rate, tremor) |
| ACE inhibitors | Dry cough, dizziness, elevated potassium | Angioedema (face/throat swelling) — emergency |
| Statins (e.g., atorvastatin) | Muscle aches, elevated liver enzymes | Rhabdomyolysis (severe muscle breakdown) — rare |
| Beta-blockers | Fatigue, cold hands, sexual dysfunction | Bradycardia (slow heart rate), bronchospasm in asthma |
| Metformin | Nausea, diarrhea, metal taste | Lactic acidosis (rare; stop if severe) |
| Antibiotics (general) | Diarrhea, nausea | C. diff infection (severe bloody diarrhea) |

### Drug Interaction Check
If 2+ medications prescribed, flag known interactions:
| Drug A | Drug B | Interaction | Severity |
|---|---|---|---|

Common serious interactions to flag:
- Warfarin + NSAIDs → bleeding risk
- MAOIs + SSRIs / SNRIs → serotonin syndrome
- Methotrexate + NSAIDs → methotrexate toxicity
- Digoxin + amiodarone → digoxin toxicity
- Statins + gemfibrozil → rhabdomyolysis risk

### Special Instructions
- **Grapefruit warning**: Flag drugs affected (statins, calcium channel blockers, some immunosuppressants)
- **Alcohol warning**: Metronidazole, tinidazole, CNS depressants
- **Pregnancy**: Flag Category D or X drugs if patient may be pregnant
- **Driving**: Flag sedating medications (benzodiazepines, antihistamines, opioids)
- **Sun sensitivity**: Tetracyclines, fluoroquinolones, thiazide diuretics

---

## Template C — Discharge Summary

### Admission Episode
| Field | Value |
|---|---|
| Hospital / Facility | |
| Ward / Unit | e.g., ICU, Cardiology, General Medicine |
| Admission Date | |
| Discharge Date | |
| Length of Stay | |
| Admitting Complaint | In patient's own words |
| Admitting Diagnosis | Medical terminology → plain English |
| Discharge Diagnosis | (may differ from admitting) |
| Attending Physician | |
| Consulting Specialists | |

### What Happened (Narrative)
2–5 sentence plain-English narrative: why the patient was admitted, what was found, what was done, and what the outcome was.

### Procedures & Interventions
| Procedure | Date | Performed By | Outcome |
|---|---|---|---|

### Investigations During Admission
| Test | Date | Key Findings |
|---|---|---|

### Discharge Medications
Compare to admission medications:
| Medication | Dose | Frequency | Status |
|---|---|---|---|
| Lisinopril 10mg | 10 mg | Once daily | Continued |
| Metformin 500mg | 500 mg | Twice daily | Dose increased to 1000mg |
| Furosemide 40mg | 40 mg | Once daily | NEW — added during admission |
| Aspirin 81mg | 81 mg | Once daily | STOPPED — replaced by clopidogrel |

### Follow-up Plan
| Action | Provider | Due Date |
|---|---|---|
| Cardiology review | Dr. [Name] | 2 weeks |
| Repeat ECG | GP / cardiologist | 4 weeks |
| Blood tests (BMP) | GP | 1 week |
| Wound check | GP / nurse | 3 days |

### Return to ER / Call Doctor If:
List every red-flag symptom mentioned in the discharge instructions.

### Lifestyle Instructions
Diet, activity restrictions, wound care, smoking cessation, alcohol limits.

---

## Template D — Imaging / Radiology Report

### Study Details
| Field | Value |
|---|---|
| Modality | X-ray / CT / MRI / PET / PET-CT / Ultrasound / Fluoroscopy / DEXA |
| Body region | e.g., Chest, Abdomen & Pelvis, Head, Right Knee, Whole Body |
| Contrast used | Yes (IV / oral / rectal) / No / N/A |
| Study date | |
| Radiologist | |
| Referring physician | |
| Clinical indication | Why the scan was ordered (plain English) |
| Comparison | Prior study used for comparison (if any) |

### Findings (Section by Section)
For each anatomical region described:
1. Quote or paraphrase the finding
2. Provide plain-English translation
3. Flag any abnormal findings with `[ABNORMAL]`
4. Flag incidental findings (unexpected findings unrelated to the indication) with `[INCIDENTAL]`

### Impression
The radiologist's conclusions in plain language. This is the most important section.

### Imaging Terminology Glossary
Define every technical term found in the report:
| Term | Plain English |
|---|---|
| Consolidation | Fluid/pus filling air spaces in the lung (may indicate pneumonia) |
| Effusion | Fluid collection (pleural effusion = fluid around the lung) |
| Atelectasis | Collapsed area of lung (may be mild/expected or significant) |
| Nodule | Small round mass (size determines significance; lung nodules <6mm usually benign) |
| Lytic lesion | Area where bone has been destroyed (may indicate cancer or other disease) |
| Enhancement | Area brightens with contrast (suggests active blood supply — can indicate tumor) |
| Herniation | Organ/tissue pushing through a gap it shouldn't be in |
| Stenosis | Narrowing (e.g., of a vessel or a spinal canal) |
| Heterogeneous | Non-uniform appearance — mixed density (may indicate complex pathology) |
| Incidental finding | Unexpected finding unrelated to the reason for the scan |

---

## Template E — ECG / EKG Report

### Measurements
| Parameter | Your Value | Normal Range | Flag |
|---|---|---|---|
| Heart rate | bpm | 60–100 bpm | |
| Rhythm | | Regular sinus | |
| PR interval | ms | 120–200 ms | |
| QRS duration | ms | 60–100 ms | |
| QT interval | ms | <440 ms (M); <460 ms (F) | |
| QTc (corrected) | ms | <450 ms | |
| Axis | degrees | -30° to +90° | |

### Plain-English Interpretation
Translate each abnormal finding (e.g., "Q waves in leads II, III, aVF" → "signs of possible old inferior heart attack — may need cardiology review").

---

## General Rules
- **Never diagnose.** Use language like "may indicate", "consistent with", "your doctor will interpret".
- **Always append**: _"This summary is for informational purposes only and does not replace medical advice. Please consult your healthcare provider to discuss these results."_
- **Flag CRITICAL values prominently** with the ⚠ alert block above.
- Spell out all abbreviations on first use.
- Use age- and sex-adjusted reference ranges when patient demographics are known.
- If the document is in another language, translate to English before summarizing.
- Preserve all original values exactly — do not round or modify reported numbers.

## Action Prompt
End with: "Would you like me to:
- Explain any specific result in more detail?
- Compare these results with a previous report you share?
- Prepare a list of questions to ask your doctor?
- Check for drug interactions in this prescription?
- Translate this report to another language?"

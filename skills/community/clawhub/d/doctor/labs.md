# Labs And Results — Reading What They Were Handed

A result is a number, a unit, a reference range, and a person. Missing any of the four makes it uninterpretable, and the flag in the margin is the least informative part of it.

**Before interpreting**, read `~/Clawic/data/health/profile.md` for conditions, medicines and previous values, and open any `~/Clawic/data/health/<metric>.md` that `## Boxes` indexes. **A single result without a prior value is a data point, not a trend** — the previous number changes the meaning of the current one more often than the reference range does.

## Four Rules Before Any Interpretation

1. **The reference range is a statistical interval, not a health target.** It is typically set so that 95% of a reference population falls inside it — which means 5% of perfectly healthy people fall outside by construction.
2. **Panels multiply that.** On 20 independent tests, the chance of at least one abnormal flag in a healthy person is 1 − 0.95²⁰ ≈ 64%. A single mildly out-of-range value on a broad panel is the expected result, not a finding.
3. **Ranges differ by laboratory, assay, age and sex.** Never compare a value against a range from a different lab; compare against the range printed on that report.
4. **Repeat before acting** on any borderline or first-time abnormality, unless it is in the act-now list below. Biological variation, a recent meal, a hard workout, dehydration and the time of day all move common analytes.

## Act Now, Do Not Wait For A Repeat

Potassium above ~6.0 or below ~2.5 mmol/L · sodium below ~125 mmol/L or a rapid change · glucose below 3.0 mmol/L (54 mg/dL) or above ~20 mmol/L (360 mg/dL) with symptoms · haemoglobin far below baseline with symptoms · neutrophils below 0.5 ×10⁹/L, especially on chemotherapy · platelets below ~20 ×10⁹/L · calcium above ~3.0 mmol/L · a new troponin rise · a positive blood culture. These are contacted-the-same-day results; if the lab or practice has not called, the person calls them.

## The Common Panels

| Panel | What it answers | The parts people misread |
|---|---|---|
| Full blood count | Anaemia, infection, platelet problems | MCV directs the anaemia work-up: low → iron deficiency or thalassaemia, high → B12/folate, alcohol, thyroid, some drugs. A normal haemoglobin does not exclude iron deficiency |
| Iron studies | Whether anaemia is iron deficiency | Ferritin below 30 µg/L means iron deficiency even with normal haemoglobin; below 15 is definitive. Ferritin rises with any inflammation, so read it beside CRP before calling it normal |
| Kidney function | Dosing, chronic kidney disease | eGFR is estimated from creatinine and depends on muscle mass — high in bodybuilders, misleadingly reassuring in frail people. CKD requires the change to persist ≥3 months |
| Liver function | Injury pattern, not "liver damage" | ALT-dominant = hepatocellular; ALP/GGT-dominant = cholestatic or alcohol. Isolated raised bilirubin with everything else normal is often Gilbert's syndrome and harmless |
| Lipids | Cardiovascular risk input | LDL is the target of treatment; a single value is not the decision — total risk over 10 years is. Non-fasting samples are acceptable for screening in most guidelines now |
| HbA1c | Average glucose over ~3 months | ≥6.5% (48 mmol/mol) diagnoses diabetes on two occasions; 5.7-6.4% (39-46) is prediabetes by ADA criteria. Falsely low in anaemia, recent blood loss, pregnancy and haemoglobin variants |
| Thyroid | Thyroid function | TSH moves first and moves opposite to the hormone. Subclinical hypothyroidism (raised TSH, normal T4) is usually watched, not treated, unless TSH is above 10 or there are symptoms with positive antibodies |
| Inflammatory markers | Something is inflamed | CRP rises and falls within days; ESR lags by weeks. Neither names the cause, and a normal CRP does not exclude serious disease |
| Vitamin D | Deficiency | Below 30 nmol/L (12 ng/mL) is deficiency; 30-50 is insufficiency. Routine screening in healthy people is not recommended by most bodies |
| Urinalysis | Infection, blood, protein | A positive dipstick in an older person with no urinary symptoms usually means asymptomatic bacteriuria and does not explain confusion (`older-adults.md`) |
| PSA | Prostate risk input | Raised by recent ejaculation, cycling, examination and infection; repeat before acting (Where Experts Disagree in SKILL.md) |

## Units, Because The Same Number Means Different Things

`glucose_units` and `lipid_units` govern every figure. Conversions worth having exact:

- Glucose: mg/dL ÷ 18 = mmol/L. 126 mg/dL = 7.0 mmol/L (the fasting diabetes threshold).
- Cholesterol: mg/dL ÷ 38.67 = mmol/L. LDL 100 mg/dL ≈ 2.6 mmol/L; 70 mg/dL ≈ 1.8 mmol/L.
- HbA1c: mmol/mol = (DCCT% − 2.15) × 10.929. 6.5% = 48 mmol/mol; 7.0% = 53 mmol/mol.
- Creatinine: mg/dL × 88.4 = µmol/L.

Always restate the value in the unit their report uses, with the report's own reference range beside it.

## Imaging And Incidental Findings

- An incidental finding is something unrelated to the reason for the scan. They are common — CT of the abdomen finds one in a substantial minority of scans — and most never cause harm.
- The useful question is not "is it there" but "what is the follow-up protocol for a lesion of this size in this organ, and what would change management?" Most have published surveillance intervals.
- Radiology reports hedge by design. "Cannot exclude" is not a diagnosis; the clinician who ordered it interprets it against the clinical question.
- Radiation dose is a real cost of repeat CT, particularly in young people — one more reason a scan should have a question it can answer.

## Getting The Result Explained

If the result arrives without an explanation, the three questions that get one: **what does this number mean for me specifically**, **does it change what we do**, and **when is it repeated**. A result marked abnormal with no plan and no repeat date is an unfinished job, and asking for the repeat date is the way to finish it.

## Where This Goes

**Write in the same turn** (`memory-template.md`):

- A value the person will compare again — blood pressure, weight, HbA1c, LDL, TSH, ferritin, eGFR, peak flow, resting heart rate — goes to the shared health box: `## Measurements` in `~/Clawic/data/health/profile.md` with date, value **and unit**, and the reference range from the report. Once a single metric passes ~15 entries, it moves to `~/Clawic/data/health/<metric>.md` in the same turn, `profile.md` keeps one index line, and the copy is deleted there.
- The repeat date the clinician gave becomes a row in `## Due` of `~/Clawic/data/doctor/memory.md`.
- A whole-panel scan the user wants kept as a document, or a written interpretation they will re-read, is an artifact: `~/Clawic/data/doctor/artifacts/<kebab-name>.md` with its `## Boxes` line the same turn.
- Nothing that authenticates goes anywhere: portal logins and health-record numbers used as credentials are pointers only (`memory-template.md`, Secrets).

# Barefoot Doctor — Robustness & Safety Checklists (02)

## How to Use

Before generating any medical recommendation, run through the relevant checklists below. These are quality gates to ensure safety, accuracy, and compliance. Mark each item as PASS / FAIL / NA, and if any FAIL, escalate appropriately.

---

## Checklist A: Emergency Triage Gate

Apply this FIRST before any other processing.

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| A1 | Does the symptom text contain any EMERGENCY keyword (chest pain >15min, unconsciousness, severe bleeding, etc.)? | [] | [] | Immediately output EMERGENCY protocol + "Call 120" |
| A2 | Is the patient a pregnant woman with ANY potentially harmful symptom? | [] | [] | Flag pregnancy warning + recommend obstetrician |
| A3 | Is this a child under 2 years with fever or respiratory symptoms? | [] | [] | Recommend immediate pediatric evaluation |
| A4 | Is there any mention of poisoning, overdose, or snake bite? | [] | [] | Invoke specific poisoning/snake bite protocol |
| A5 | Has a disclaimer been included in the output? | [] | [] | Add mandatory disclaimer before delivering |

**Gate Result**: Any FAIL in A1-A4 → STOP normal flow, invoke emergency protocol. ALL PASS → Continue.

---

## Checklist B: TCM Pattern Quality Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| B1 | Were at least 3 of 4 TCM examination methods considered? | [] | [] | Expand inquiry to cover missing methods |
| B2 | Was the tongue description consistent with the stated pattern? | [] | [] | Re-evaluate pattern or note inconsistency |
| B3 | Was the pulse quality consistent with the stated pattern? | [] | [] | Re-evaluate or note insufficient pulse data |
| B4 | Was the Eight Principles (Yin/Yang, Ext/Int, Cold/Heat, Def/Exc) addressed? | [] | [] | Add Eight Principles analysis |
| B5 | Was an organ system (Zang-Fu) identified? | [] | [] | Add organ system differentiation |

---

## Checklist C: Herb/Drug Interaction Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| C1 | Were the patient's current medications reviewed? | [] | [] | Ask patient to list medications |
| C2 | Were any blood-activating herbs (Tao Ren, Hong Hua, Dan Shen) recommended to a pregnant patient? | [] | [] | REMOVE those herbs immediately |
| C3 | Was Gan Cao (licorice) recommended to a cardiac patient on digoxin? | [] | [] | WARN about hypokalemia risk |
| C4 | Was Dan Shen recommended with warfarin/anticoagulants? | [] | [] | WARN about increased bleeding risk |
| C5 | Were any toxic or unprocessed herbs recommended? | [] | [] | Replace with processed versions |
| C6 | Was the herb recommended at a safe dose for the patient's age? | [] | [] | Adjust dose per age-based pediatric/adult table |

---

## Checklist D: Acupuncture Safety Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| D1 | Were any contraindicated points recommended for pregnancy? (SP6, LR3, GB21, DU20 for some practitioners) | [] | [] | Remove contraindicated points for pregnant patients |
| D2 | Was needling depth appropriate for the anatomical location? | [] | [] | Adjust depth or use acupressure instead |
| D3 | Were sharp instruments (three-edged needle, prismatic needle) recommended for home use? | [] | [] | Replace with safer alternatives |
| D4 | Was moxibustion recommended near flammable materials or on sensitive areas? | [] | [] | Add safety distance instructions |
| D5 | Were acupoints recommended that are anatomically dangerous without training? | [] | [] | Replace with safer surface points |

---

## Checklist E: Pediatric Safety Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| E1 | Was the dose calculated using the pediatric age-based table? | [] | [] | Recalculate dose |
| E2 | Were any toxic or strong purgative herbs recommended? | [] | [] | Replace with gentler alternatives |
| E3 | Were all medications checked against pediatric contraindications? | [] | [] | Remove contraindicated medications |
| E4 | Were dehydration signs properly assessed in a pediatric case? | [] | [] | Add ORS and rehydration guidance |
| E5 | Was the fever temperature and duration assessed for danger? | [] | [] | Add fever danger threshold guidance |

---

## Checklist F: Output Format Compliance

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| F1 | Does the response include severity rating (EMERGENCY / MODERATE / MILD)? | [] | [] | Add severity rating |
| F2 | Does it include TCM pattern diagnosis when applicable? | [] | [] | Add TCM analysis |
| F3 | Does it include Western differential diagnosis? | [] | [] | Add differential diagnosis |
| F4 | Does it include actionable recommendations (specific, not vague)? | [] | [] | Make recommendations concrete |
| F5 | Does it include a clear medical disclaimer? | [] | [] | Add disclaimer |
| F6 | Is the language clear and non-technical for general audiences? | [] | [] | Simplify language |
| F7 | Are follow-up criteria and warning signs included? | [] | [] | Add follow-up section |

---

## Checklist G: Content Accuracy Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| G1 | Are all acupoint locations described with anatomical landmarks? | [] | [] | Add location description |
| G2 | Are all herb dosages within the standard reference range? | [] | [] | Correct dosage |
| G3 | Are all cited disease names consistent with Western medical classification? | [] | [] | Align terminology |
| G4 | Are TCM pattern names consistent with standard nomenclature? | [] | [] | Use standard pattern names |
| G5 | Is the emergency protocol consistent with current standard guidelines? | [] | [] | Update to standard protocol |

---

## Error Handling Table

| Error Code | Trigger | Response |
|-----------|---------|---------|
| E001 | No symptoms provided | "Please describe your symptoms in more detail." |
| E002 | Emergency keyword detected | Stop normal flow, invoke emergency protocol immediately |
| E003 | Conflicting diagnosis data | Present both possibilities, recommend professional evaluation |
| E004 | Pregnancy + harmful substance | STOP: "This is not safe during pregnancy. Please consult your obstetrician." |
| E005 | Pediatric + severe symptoms | Recommend immediate pediatric specialist |
| E006 | TCM pattern unclear | Default to broader category + lifestyle guidance |
| E007 | Herb-drug interaction detected | Remove interacting herb, warn patient |
| E008 | Chronic + acute symptoms | Both assessments + urgent referral recommendation |
| E009 | Age unknown | Ask for age before proceeding with dosage |
| E010 | Non-OTC medication requested | "I can only recommend OTC medications. For prescription drugs, please consult your doctor." |

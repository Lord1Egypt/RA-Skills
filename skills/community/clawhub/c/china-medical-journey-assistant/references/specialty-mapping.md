# Specialty Mapping

Use this map before selecting hospitals from the bundled Fudan ranking snapshot. Choose one primary specialty. Add a secondary specialty only when the case could reasonably branch.

## Core Routing Table

| Patient Need | Primary Specialty Key | Secondary Keys | Notes |
|---|---|---|---|
| solid tumor, cancer, chemotherapy, radiotherapy | 肿瘤学 | 胸外科, 放疗相关方向按 access notes 补充 | Use for most solid-organ cancers unless the user clearly needs hematology. |
| lymphoma, leukemia, myeloma, bone marrow transplant, CAR-T for blood cancer | 血液科 | 肿瘤学 | Prefer hematology over general oncology for blood cancers and CAR-T routing. |
| chest pain, coronary disease, heart failure, arrhythmia, angiography, interventional cardiology | 心血管病 | 心血管外科 | Use when the likely path is evaluation, medical management, or catheter-based intervention. |
| bypass surgery, valve surgery, aortic surgery, congenital cardiac surgery | 心血管外科 | 心血管病 | Use when the user is already describing a surgery-led cardiac path. |
| brain tumor surgery, skull base surgery, spine surgery, epilepsy surgery | 神经外科 | 神经内科 | Use for surgery-led neurological cases. |
| stroke follow-up, epilepsy medication, Parkinson's disease, headache workup | 神经内科 | 神经外科 | Use for evaluation-first or medication-led neurological cases. |
| respiratory disease, lung infection, chronic lung disease | 呼吸科 | 胸外科 | Use thoracic surgery only if the user is already on a surgery path. |
| digestive disease, liver disease, colon disease, GI bleeding | 消化病 | 普外科 | |
| kidney disease, renal failure, dialysis | 肾脏病 | 泌尿外科 | |
| diabetes, thyroid disease, endocrine disease | 内分泌 | 普外科 | For thyroid cancer, route to oncology instead. |
| orthopedics, spine, joint replacement, fractures | 骨科 | 康复医学 | |
| fertility, gynecology, obstetrics, IVF | 妇产科 | 生殖方向按 hospital fit 补充 | |
| pediatric disease, pediatric cancer, rare pediatric illness | 小儿内科 | 小儿外科 | |
| dermatology, severe autoimmune skin disease | 皮肤科 | 风湿免疫科 | |
| infectious disease, liver infection | 传染感染科 | 消化病 | |
| psychiatry, severe depression, anxiety, psychosis | 精神医学 | 无 | |
| rheumatology, autoimmune disease, lupus, vasculitis | 风湿免疫科 | 肾脏病 | |
| eye disease, ophthalmology | 眼科 | 无 | |

## Provisional-Routing Triggers

Mark the answer as provisional when:

- the user describes only symptoms, not a diagnosis
- the case could reasonably fit two specialties
- the likely path could be surgery-first or evaluation-first depending on missing records
- staging, pathology, receptor status, imaging, or prior treatment history would materially change the shortlist

## Unsupported Or Weakly Covered Cases

If the condition does not map cleanly to the bundled specialty baseline:

1. say the routing is not fully covered by the bundled ranking map
2. recommend comprehensive hospitals from the static ranking baseline
3. explain what specialist direction the patient should verify next

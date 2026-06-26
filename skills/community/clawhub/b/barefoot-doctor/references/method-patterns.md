# Barefoot Doctor — Method Patterns & Code Templates

## Overview

Detailed implementation templates, diagnostic decision trees, herb/point selection logic, and protocol specifications for the Barefoot Doctor AI skill.

---

## 1. Diagnostic Flow Patterns

### 1.1 Standard Diagnostic Procedure

```
START
  + Step 1: Triage Check (EMERGENCY? -> 120 + stop)
  + Step 2: Chief Complaint Clarification
  + Step 3: Symptom Duration & Progression
  + Step 4: Accompanying Symptoms
  + Step 5: Patient Profile (age, gender, chronic conditions, medications)
  + Step 6: TCM Four Examinations
  |    + Inquiry (Ten Questions - Shi Wen Ge)
  |    + Observation (Wang Zhen - Tongue, complexion, spirit)
  |    + Listening/Smelling (Wen Zhen - voice, breath, odor)
  |    + Palpation (Qie Zhen - pulse, local palpation)
  + Step 7: TCM Pattern Differentiation (Ba Gang Bian Zheng)
  |    + Yin vs Yang
  |    + Exterior vs Interior
  |    + Cold vs Heat
  |    + Deficiency vs Excess
  + Step 8: Western Differential Diagnosis
  + Step 9: Severity Assessment (EMERGENCY / MODERATE / MILD)
  + Step 10: Recommendation Generation
```

### 1.2 Symptom -> System Mapping

| Symptom Cluster | Western System | TCM Organ | Priority Differential |
|-----------------|---------------|-----------|----------------------|
| Fever + cough + sputum | Respiratory | Lung | Common cold, flu, pneumonia, bronchitis |
| Fever + headache + stiff neck | Neurological | Liver | Meningitis (EMERGENCY), common cold |
| Epigastric pain + acid reflux | GI | Spleen/Stomach | Gastritis, ulcer, GERD |
| Chest pain + dyspnea + palpitations | Cardiovascular | Heart | Angina (EMERGENCY), anxiety |
| Urinary frequency + dysuria | GU | Kidney/Bladder | UTI, cystitis, prostatitis |
| Diarrhea + vomiting | GI | Spleen/Stomach | Gastroenteritis, food poisoning |
| Skin rash + itching | Dermatological | Lung/Spleen | Allergy, eczema, infection |
| Joint pain + swelling | Musculoskeletal | Liver/Kidney | Arthritis, gout |

### 1.3 TCM Pattern Decision Matrix

| Primary Manifestation | Pattern | Key Signs | Common Causes |
|---------------------|---------|-----------|---------------|
| Fever + aversion to cold | Exterior Cold | No sweat, stiff neck, thin white tongue | Wind-cold invasion |
| Fever + aversion to heat | Exterior Heat | Sweat, sore throat, yellow tongue | Wind-heat invasion |
| Fever + heavy body | Internal Heat | Thirst, constipation, red tongue | Heat excess |
| Cold limbs + no fever | Yang Deficiency | Pale face, fatigue, deep weak pulse | Cold deficiency |
| Night fever + night sweating | Yin Deficiency | Thirst, red tongue, thin pulse | Heat from deficiency |
| Fullness + pain worse pressure | Excess | Rigid abdomen, tense pulse | Blockage/stagnation |
| Emptiness + pain better pressure | Deficiency | Chronic onset, weak pulse | Weakness |

---

## 2. Emergency Protocols

### 2.1 Emergency Triage Algorithm

```python
EMERGENCY_KEYWORDS = [
    "unconscious", "coma", "cardiac arrest", "respiratory arrest",
    "severe bleeding", "hematemesis", "hemoptysis", "black stool",
    "chest pain > 15min", "crushing chest pain",
    "sudden severe headache", "meningeal signs",
    "high fever > 39.5C > 3 days", "fever with rash",
    "poisoning", "overdose", "snake bite", "drowning",
    "electric shock", "burns > 10%", "fracture with deformity",
    "acute abdomen", "eclampsia", "shock"
]

MODERATE_KEYWORDS = [
    "persistent vomiting", "high fever", "severe pain",
    "hematuria", "vaginal bleeding", "dyspnea"
]

def triage(symptoms, patient_info):
    for kw in EMERGENCY_KEYWORDS:
        if kw.lower() in symptoms.lower():
            return {"severity": "EMERGENCY", "action": "CALL_120"}
    for kw in MODERATE_KEYWORDS:
        if kw.lower() in symptoms.lower():
            return {"severity": "MODERATE", "action": "SEEK_CARE"}
    return {"severity": "MILD", "action": "HOME_CARE"}
```

### 2.2 First Aid Protocols

#### Cardiac Arrest / Unconsciousness
1. Check responsiveness (tap shoulders, call loudly)
2. Call 120 immediately
3. Begin CPR if no breathing/pulse:
   - Compressions: 100-120/min, depth 5-6cm
   - Ratio: 30 compressions : 2 breaths
   - Continue until EMS arrives
4. Use AED if available

#### Choking (Heimlich Maneuver)
- Stand behind victim
- Locate navel, place fist above
- Deliver 6-10 upward thrusts
- Repeat until object expelled or victim unconscious
- If unconscious: begin CPR

#### Poisoning
1. Call 120
2. Identify substance + estimated amount
3. DO NOT induce vomiting if:
   - Corrosive substance (acids, alkalis)
   - Petroleum product
   - Patient unconscious
   - Pregnancy
4. Collect vomitus/sample for identification

#### Snake Bite
1. Keep victim calm, immobilize affected limb
2. DO NOT: cut wound, suck venom, apply tourniquet, ice
3. Remove jewelry before swelling
4. Transport to hospital (ideally within 1 hour)

#### Heat Stroke
1. Move to cool area immediately
2. Cool rapidly: ice packs to neck, armpits, groin
3. Fan victim + mist skin with water
4. Monitor temperature - stop cooling when below 38.5C
5. Give fluids if conscious
6. Transport to hospital

#### Drowning
1. Remove from water ASAP
2. Check breathing/pulse
3. If no breathing: rescue breathing first (2 breaths), then CPR
4. Keep victim horizontal
5. Remove wet clothes, warm patient
6. Transport to hospital (secondary drowning risk)

#### Electric Shock
1. Disconnect power source (DO NOT touch victim until)
2. Check breathing/pulse
3. CPR if needed
4. Treat burns with clean dressing
5. Monitor for cardiac arrhythmias

---

## 3. Acupuncture Point Patterns

### 3.1 Common Point Formulas by Condition

| Condition | Primary Points | Adjunctive Points | Notes |
|-----------|--------------|------------------|-------|
| Headache (general) | GB20, Taiyang | LI4, GB8 | Front: DU20+Yintang; Back: GB20+DU20 |
| Fever (wind-heat) | DU14, LI11, LI4 | GB20, Quchi | Heavy cupping on DU14 effective |
| Cough | LU7, LU1, RN22 | RN12, LU5, BL13 | Dry needling; moxibustion on LU7 |
| Nausea/vomiting | PC6, RN12 | SP4, RN6 | PC6 most important point |
| Abdominal pain | RN12, RN6, ST36 | PC6, SP6 | Cold: moxibustion; Heat: needling |
| Diarrhea | RN12, ST25, ST36 | SP6, DU20 | Chronic: moxibustion |
| Insomnia | HT7, SP6, RN24 | Anmian (EX-HN14), PC6 | Combine HT7 + SP6 |
| Back pain | DU26, BL40, BL23 | Ashi points | Acute: bloodletting |
| Knee pain | ST35, Xiyan, SP9 | BL40, GB34 | Ashi + local points |
| Toothache | LI4, Xiaguan, ST6 | ST44, SI18 | ST44 for lower; SI18 for upper |
| Sore throat | LI4, LU11 | SJ5, RN23 | LU11 bloodletting effective |
| Asthma | RN22, BL13, Dingchuan | LU7, RN6 | Moxibustion on RN4+RN6 preventive |
| Menstrual pain | SP6, RN4, RN6 | ST36, SP8 | Moxibustion on RN4+RN6 |
| Dysmenorrhea | SP6, LR3, RN4 | ST36, SP10 | LR3 important for emotional pain |

### 3.2 Acupoint Location Quick Reference

| Point | Anatomical Landmark | Cun Measurement |
|-------|--------------------|-----------------|
| Hegu (LI4) | web space of thumb-index, 2nd MCP | 50% of metacarpal |
| Zusanli (ST36) | 3 cun below knee (ST35), 1 finger lateral tibia | lateral tibia |
| Neiguan (PC6) | 2 cun from wrist crease, between tendons | flexor carpi |
| Huantiao (GB30) | junction of lateral 1/3 + medial 2/3 of distance SI-AS | buttocks |
| Fengfu (DU16) | 1 cun below occipital protuberance, in depression | midline |
| Renzhong (DU26) | upper 1/3 of philtrum | midline |
| Weizhong (BL40) | midpoint of popliteal crease | midpoint |
| Sanyinjiao (SP6) | 3 cun above ankle (malleolus), posterior tibia | posterior border |

### 3.3 Moxibustion Indication Rules

| Type | Application | Duration | Caution |
|------|------------|---------|---------|
| Mild warming | Chronic deficiency-cold | 10-15 min per point | None |
| Moderate | Arthritis, pain | 15-20 min | Check for burns |
| Strong (scarring) | Chronic severe | Until blister | Painful, scarring - professional only |
| Moxa stick | General use | 20-30 min | Keep 3-5 cm from skin |
| Indirect | Sensitive patients | Variable | Use salt/ginger/salt barrier |

---

## 4. Herbal Medicine Patterns

### 4.1 Common Formula Templates

| Formula Name | Indications | Core Herbs | Modifications |
|-------------|------------|-----------|-------------|
| Yin Qiao San | Wind-heat (early stage) | Jin Yinhua + Lian Qiao + Bo He | + Ban Lan Gen if sore throat |
| Ma Xing Gan Shi Tang | Heat lung, asthma | Ma Huang + Xing Ren + Gan Cao + Shi Gao | Severe: + Gua Lou |
| Ping Wei San | Damp-spleen | Cang Zhu + Hou Po + Chen Pi + Gan Cao | + Fu Ling if edema |
| Si Jun Zi Tang | Qi deficiency | Ren Shen + Bai Zhu + Fu Ling + Gan Cao | + Ban Xia for phlegm |
| Si Wu Tang | Blood deficiency | Shu Di Huang + Bai Shao + Dang Gui + Chuan Xiong | + Tao Ren for stasis |
| Liu Wei Di Huang Tang | Yin deficiency | Shu Di + Shan Zhu Yu + Shan Yao + Fu Ling + Mu Dan Pi + Ze Xie | Specific organ yin |
| Xiao Yao San | Liver qi depression | Chai Hu + Bai Shao + Dang Gui + Bai Zhu + Fu Ling + Bo He | + Dan Zhi for heat |
| Chai Hu Shu Gan San | Liver stagnation | Chai Hu + Bai Shao + Xiang Fu + Chen Pi + Chuan Xiong + Zhi Ke | Pain dominant |
| Bao He Wan | Food stagnation | Shan Zha + Shen Qu + Lai Fu Zi + Ban Xia + Chen Pi + Fu Ling | Heavy accumulation |
| Zhen Wu Tang | Yang deficiency water | Fu Zi + Bai Zhu + Fu Ling + Sheng Jiang + Bai Shao | Severe edema |

### 4.2 Herb Interaction Safety Matrix

| Herb Category | Common Herbs | Contraindicated With | Notes |
|--------------|-------------|----------------------|-------|
| Warming | Fu Zi, Rou Gui, Gan Jiang | Yin deficiency heat, pregnancy | Monitor for overheating |
| Heat-clearing | Shi Gao, Huang Qin, Huang Lian | Cold-deficient spleen | Can damage qi |
| Blood-activating | Tao Ren, Hong Hua, Dan Shen | Pregnancy, bleeding disorders | Careful with anticoagulants |
| Toxic herbs | Ban Xia (processed) | Raw use, overdose | Must be properly processed |
| Purgative | Da Huang, Mang Xiao | Pregnancy, elderly weak | Not for chronic use |

### 4.3 Common Herb-Drug Interactions

| Herbal Substance | Pharmaceutical Drug | Interaction | Severity |
|------------------|-------------------|------------|---------|
| Dan Shen (Salvia) | Warfarin | Increased bleeding risk | HIGH |
| Gou Teng (Uncaria) | Antihypertensives | Potentiated effect | MODERATE |
| Gan Cao (Licorice) | Digoxin | Hypokalemia toxicity | HIGH |
| Huang Qin (Scutellaria) | Multiple drugs | CYP450 inhibition | MODERATE |
| Ren Shen (Ginseng) | Warfarin | Decreased INR | MODERATE |
| Ginkgo biloba | Aspirin/NSAIDs | Increased bleeding | HIGH |

---

## 5. Disease Classification Index

### 5.1 By Body System

```
INTERNAL MEDICINE
+-- Respiratory: Common cold, Flu, Pneumonia, Bronchitis, Asthma, COPD, Pleurisy, Lung abscess
+-- Cardiovascular: Angina, MI, Arrhythmia, Heart failure, Hypertension, Hypotension, Phlebitis
+-- Digestive: Gastritis, Peptic ulcer, Enteritis, Dysentery, Constipation, Hemorrhoids, Jaundice, Cirrhosis
+-- Neurological: Headache, Migraine, Vertigo, Neurasthenia, Facial paralysis, Hemiplegia
+-- Endocrine: Diabetes, Hyper/hypothyroidism, Obesity
+-- Urinary: Nephritis, Cystitis, UTI, Prostatitis, Urinary stones, Hematuria
+-- Hematological: Anemia, Leukopenia, Thrombocytopenia
+-- Infectious: Tuberculosis, Hepatitis, Dysentery, Malaria, Rabies, Tetanus

PEDIATRICS
+-- Neonatal: Asphyxia neonatorum, Neonatal sepsis, Neonatal jaundice
+-- Nutritional: Protein-energy malnutrition, Rickets, Vitamin deficiency
+-- Respiratory: Pediatric pneumonia, Croup, Bronchiolitis
+-- Digestive: Pediatric diarrhea, Dysentery, Ascariasis, Enterobiasis
+-- Infectious: Measles, Rubella, Chickenpox, Mumps, Scarlet fever, Whooping cough, Diphtheria

GYNECOLOGY
+-- Menstrual: Menorrhagia, Dysmenorrhea, Amenorrhea, PCOS, PMS
+-- Inflammatory: Pelvic inflammatory disease, Cervicitis, Vaginitis
+-- Pregnancy: Morning sickness, Threatened abortion, Postpartum care, Mastitis
+-- Menopausal: Perimenopausal syndrome, Osteoporosis

SURGERY
+-- Trauma: Fracture, Dislocation, Sprain, Contusion, Laceration
+-- Acute Abdomen: Appendicitis, Cholecystitis, Intestinal obstruction, Perforation
+-- Burns and Scalds
+-- Dog Bite, Snake Bite
+-- Hemorrhoids, Hernia

DERMATOLOGY
+-- Bacterial: Impetigo, Furuncle, Cellulitis, Erysipelas
+-- Viral: Herpes simplex, Herpes zoster, Warts, Molluscum
+-- Fungal: Tinea (ringworm), Candidiasis
+-- Allergic: Urticaria, Eczema, Contact dermatitis, Drug eruption
+-- Parasitic: Scabies, Pediculosis

EMERGENCY MEDICINE
+-- Shock (hypovolemic, septic, cardiogenic)
+-- Poisoning (food, chemical, drug overdose)
+-- Heat Stroke / Heat Exhaustion
+-- Hypothermia
+-- Drowning
+-- Electric Shock
+-- Acute Allergic Reaction / Anaphylaxis
```

---

## 6. Dosage Reference Tables

### 6.1 Common Western OTC Medications

| Drug | Indication | Adult Dose | Frequency | Max Daily | Contraindication |
|------|-----------|-----------|-----------|-----------|-----------------|
| Paracetamol | Fever, pain | 500mg-1g | q6h | 4g | Alcoholic liver disease |
| Ibuprofen | Pain, fever, inflammation | 200-400mg | q6-8h | 1.2g | Peptic ulcer, renal impairment |
| Aspirin | Fever, pain, antiplatelet | 300-600mg | q4-6h | 4g | Peptic ulcer, children under 16 |
| ORS salts | Diarrhea dehydration | 1 packet per liter | ad libitum | as needed | Severe dehydration (IV needed) |
| Loperamide | Diarrhea | 4mg first, then 2mg | after each loose stool | 8mg | Dysentery with fever |
| Ranitidine | Acid reflux, gastritis | 150mg | bid | 300mg | Hepatic impairment |
| Domperidone | Nausea, vomiting | 10mg | tid | 30mg | Cardiac disease, breastfeeding |
| Metoclopramide | Nausea, vomiting | 10mg | tid | 30mg | Parkinson disease, epilepsy |
| Ambroxol | Cough (wet) | 30mg | tid | 90mg | Gastric ulcer |
| Dextromethorphan | Cough (dry) | 10-20mg | q4h | 120mg | Asthma, children under 2 |
| Cetirizine | Allergy, itching | 10mg | qd | 10mg | Renal impairment |
| Chlorpheniramine | Allergy, itching | 4mg | q6h | 24mg | BPH, glaucoma |
| Vitamin C | Scurvy, supplementation | 100-500mg | qd | 2g | Oxalate kidney stones |

### 6.2 Common Chinese Patent Medicines

| Patent Medicine | TCM Pattern | Indications | Dosage | Caution |
|----------------|------------|-------------|--------|---------|
| Yin Qiao Jie Du Pian | Wind-heat | Common cold, sore throat | 4-6 tabs tid | Wind-cold: do not use |
| Gan Mao Qing Re Ke Li | Wind-heat | Flu with fever | 1 bag tid | None specific |
| Banlangen Granules | Heat toxin | Sore throat, fever | 1 bag tid | Spleen-deficient diarrhea: use with caution |
| Huo Xiang Zhengqi Shui | Summer-damp | Nausea, vomiting, diarrhea (damp) | 5-10ml bid | Heat disease: do not use |
| Huoxiang Zhengqi San | Damp-spleen | Diarrhea, nausea (damp) | 1 bag bid | Yin deficiency: use with caution |
| Jia Wei Xiao Yao San | Liver-blood deficiency + heat | PMS, irritability, bloating | 6g bid | None specific |
| Liuwei Dihuang Wan | Yin deficiency | Tinnitus, lumbar pain, dizziness | 8-10 pills tid | Spleen-deficient diarrhea: use with caution |
| Guizhi Fuling Wan | Blood stasis + deficiency | Menstrual disorders, masses | 6g bid | Pregnancy: contraindicated |
| Tong Bei San | Food accumulation | Abdominal distension, belching | 1 bag bid | Spleen deficiency: use with caution |
| Xiao Chaihu Tang | Shaoyang disorder | Alternating fever/chill, bitter taste | 1 bag bid | Heat from yin deficiency: not suitable |

---

## 7. TCM Pattern Differentiation Code

### 7.1 Eight Principles Decision Tree

```
PATIENT ASSESSMENT

+ STEP 1: Yin or Yang?
|    + Yin: Pale, cold limbs, quiet, prefers warmth
|    + Yang: Red face, fever, restless, prefers cold
|
+ STEP 2: Exterior or Interior?
|    + Exterior: Acute onset, fever + chills, floating pulse
|    + Interior: Chronic/secondary, no chills, deep pulse
|
+ STEP 3: Cold or Heat?
|    + Cold: Cold limbs, clear discharge, pale tongue, slow pulse
|    + Heat: Fever, red face, thirst, yellow tongue, rapid pulse
|
+ STEP 4: Deficiency or Excess?
     + Deficiency: Chronic, weak voice, pain better pressure, weak pulse
     + Excess: Acute, strong voice, pain worse pressure, forceful pulse
```

### 7.2 Organ System Pattern Matching

| Organ | Primary Functions | Common Patterns | Key Signs |
|-------|-----------------|-----------------|-----------|
| Lung | Breath, skin, water distribution | Wind-cold, Wind-heat, Phlegm-damp, Lung qi deficiency, Lung yin deficiency | Cough, sputum, dyspnea, asthma |
| Spleen | Transport, digestion, blood containment | Spleen qi deficiency, Spleen yang deficiency, Damp encumbrance, Spleen-blood deficiency | Fatigue, poor appetite, loose stool, bloating |
| Heart | Spirit, blood vessels, sweating | Heart qi deficiency, Heart blood deficiency, Heart yin deficiency, Heart yang deficiency, Heart fire excess | Palpitation, insomnia, anxiety, chest pain |
| Liver | Planning, tendons, emotions, blood storage | Liver qi stagnation, Liver fire, Liver yang rising, Liver blood deficiency, Damp-heat liver | Irritability, headache, hypochondriac pain, tinnitus |
| Kidney | Reproduction, bones, water, reception of qi | Kidney yang deficiency, Kidney yin deficiency, Kidney qi insecurity | Lumbar pain, tinnitus, frequent urination, infertility |
| Stomach | Receiving, rotting, descending | Stomach qi deficiency, Stomach yin deficiency, Cold invading stomach, Stomach fire | Epigastric pain, bloating, hunger changes |
| Large Intestine | Conduction, forming stool | Large intestine heat, Large intestine damp-heat, Large intestine dryness | Constipation, diarrhea, bloody stool |

---

## 8. Special Population Guidelines

### 8.1 Pediatric Dosing (TCM)

| Age | Adult Dose Equivalent |
|-----|----------------------|
| 1 month | 1/18 |
| 6 months | 1/10 |
| 1 year | 1/5 |
| 3 years | 1/3 |
| 7 years | 1/2 |
| 12 years | 2/3 |
| Adult | 1 |

### 8.2 Pregnancy Safety Categories (Simplified)

| Category | Status | Action |
|----------|--------|--------|
| SAFE | Prenatal vitamins, iron, calcium, ORS | Safe to recommend |
| CAUTION | Paracetamol, certain antibiotics | Recommend professional consultation |
| AVOID | Most TCM herbs (especially blood-activating, toxic, strong herbs) | STRONGLY DISCOURAGE |
| ABSOLUTE | Fu Zi, Tao Ren, Hong Hua, Da Huang, Mang Xiao | NEVER recommend |

### 8.3 Elderly Considerations

- Start with lower doses, titrate up
- Monitor kidney/liver function
- Prefer gentle methods (moxibustion > acupuncture)
- Watch for polypharmacy interactions
- Increase attention to cardiovascular symptoms

---

## 9. Error Codes

| Code | Description | Handling |
|------|-------------|---------|
| E001 | No symptoms provided | Ask patient to describe symptoms |
| E002 | Emergency detected | Immediately advise 120 + provide first aid |
| E003 | Conflicting symptoms | Present differential diagnoses, recommend professional |
| E004 | Pregnancy + harmful substance | STRICT: warn against harmful substance |
| E005 | Pediatric severe symptoms | Refer to pediatric specialist |
| E006 | TCM pattern unclear | Apply broader pattern category |
| E007 | Herb-drug interaction detected | Warn + recommend professional consultation |
| E008 | Chronic condition + acute symptoms | Recommend professional evaluation |

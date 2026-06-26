# Diagnostic Medicine-PMPH-10edition
<div align="center">

> *「21st Century Medical Student Diagnostic Skills Guide」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> A clinical skills handbook based on *Diagnostics* (PMPH, 10th Edition) — **183 core diagnostic skills**
<br>
<br>
<img src="/assets/Diagnostics.png" width="260px">
<br>

Why struggle through a whole textbook?<br>
Just ask a question, and get solutions directly from the textbook.

<br>

**Other Languages:**

[中文](README.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## About

This project systematically integrates core clinical diagnostic competencies derived from *Diagnostics*, 10th Edition (People's Medical Publishing House), covering **183 essential diagnostic skills** across 14 major categories.

**Audience**: Clinicians, medical students, residents in standardized training, laboratory and imaging technicians, nursing and public health professionals

**Reference Textbook**: *Diagnostics* 10th Edition, People's Medical Publishing House (ISBN: 978-7-117-35276-8)

**⚠️ Disclaimer ⚠️**
- This project is intended for **educational reference** and **clinical training only** and should not replace professional medical judgment.
- All diagnostic decisions must be made by qualified clinicians based on individual patient circumstances.
- Source content may not reflect the latest clinical guidelines; always cross-verify with current official guidelines, local protocols, and specialist advice.
- Deploy system-level medical safety policies requiring escalation of diagnosis, prescription, and emergency care decisions to qualified physicians.

## Project Structure

```
Diagnostic-Medicine-PMPH-10edition/
├── SKILL.md              # Core config — 183-skill registry
├── README.md             # This documentation
├── <skill-name>/         # Individual skill definitions
│   └── SKILL.md          #   Skill details (usage, steps, references)
├── scripts/              # Executable tool scripts
├── config/               # Configuration files
└── tests/                # Validation and testing
```

## Skill Categories Overview

| Category | Skills | Description |
|----------|--------|-------------|
| 📋 History Taking & Communication | 8 | Structured interviewing, focused H&P, doctor-patient communication, medical record writing |
| 🩺 Physical Examination | 22 | Comprehensive exam, basic methods, special populations adaptation, system-specific exams |
| ❤️ Cardiovascular Diagnostics | 16 | ECG staging and localization, heart sounds, arrhythmias, exercise stress testing, biomarkers |
| 🫁 Respiratory Diagnostics | 7 | Abnormal breath sounds, percussion interpretation, bronchoscopy prep, PFTs and blood gas |
| 🫃 Digestive System & Abdominal | 10 | Abdominal masses, pain mechanisms, vomitus analysis, Murphy sign, venous patterns |
| 🩸 Hematology & Coagulation | 21 | Anemia classification, bone marrow iron stain, coagulation factors, hemolysis screening, PNH flow |
| ⚖️ Endocrine & Metabolism | 11 | Edema differentials, nutrition assessment, glucose/OGTT, thyroid function, congenital jaundice |
| 🫘 Hepato-Pancreato-Renal & Urinary | 15 | Jaundice differentiation, liver enzyme patterns, blood ammonia, urine RBC morphology, RTA testing |
| 🦠 Infection & Immunology | 14 | Susceptibility testing, resistance mechanisms, syphilis serology, PPD, complement & autoantibodies |
| 🧠 Neurology & Psychiatry | 4 | Vertigo classification, depression screening, papilledema, retinal signs of systemic disease |
| 🔬 Lab Testing & Quality Control | 10 | Specimen collection, reference intervals, QC systems, stool/semen analysis, vaginal cleanliness |
| 🏥 Specialty Procedures & Punctures | 10 | Paracentesis, thoracentesis, lumbar puncture, liver biopsy, lymph node aspiration, catheterization |
| 🧩 Clinical Reasoning & Diagnostics | 11 | Four-step diagnosis, hypothetico-deductive reasoning, diagnostic principles, symptom differentials |
| 📚 Textbook & Resource Use | 5 | Edition verification, revision guidelines, digital resource access, core framework |

> **Total: 183 skills** covering a complete diagnostic competency spectrum from fundamentals to advanced practice.

## Quick Start

### Installation

CLI:
```bash
openclaw skills install diagnostics-pmph-10edition
```

Prompt (for AI assistants):
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Diagnostic-Medicine-PMPH-10edition" (xllgreen/diagnostics-pmph-10edition) from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/xllgreen/diagnostics-pmph-10edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### Usage

Each skill includes four sections:
1. **When to Use** — appropriate triggering scenarios
2. **How to Execute** — standardized operating procedures
3. **Precautions** — contraindications and warnings
4. **Reference** — supplementary materials

### Query Examples

#### 1. **Concept Query**
```text
What is a gallop rhythm? What types are there?
```

#### 2. **Clinical Case Analysis**
```text
A 65-year-old male presents with retrosternal crushing chest pain radiating to the left shoulder for 2 hours, accompanied by diaphoresis and nausea. ECG shows ST-segment elevation (0.3-0.5mV) in leads V₁-V₄, cTnI elevated. What is the most likely diagnosis?
```

#### 3. **Differential Diagnosis**
```text
A 28-year-old female with generalized edema and frothy urine for 1 week. Urinalysis: protein (+++), 24h urine protein 4.5g, serum albumin 25g/L. What is the most likely diagnosis and what conditions should be differentiated?
```

**More Examples:**
- "Use the **acute-myocardial-infarction-ecg-staging** skill to analyze this patient's ECG."
- "Apply **mcv-rdw-anemia-classification** to classify this anemia case."
- "Use **clinical-diagnostic-four-step-method** to reason through this fever patient's possible diagnoses."
- "Use **bilirubin-metabolism-and-jaundice-classification** to analyze the cause of jaundice."

## About the Author

**xllgreen** ([xllgreen.github.io](https://xllgreen.github.io)) — Medical student at Jiujiang University · Tech geek

## Technical Support

<br>
PDF2App: https://pdf2app.cn
<br>
Microsoft Visual Studio Code: https://code.visualstudio.com/
<br>
Claude Code for VS Code: https://claude.com/
<br>
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API: https://platform.deepseek.com/
<br>
© 2026 Hangzhou DeepSeek Artificial Intelligence Basic Technology Research Co., Ltd.
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API: https://platform.xiaomimimo.com/
<br>
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## License

This project is organized based on *Diagnostics*, 10th Edition (PMPH) for educational purposes only.

## Star History

<a href="https://www.star-history.com/#xllgreen%2FDiagnostic-Medicine-PMPH-10edition&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xllgreen/Diagnostic-Medicine-PMPH-10edition&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xllgreen/Diagnostic-Medicine-PMPH-10edition&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xllgreen/Diagnostic-Medicine-PMPH-10edition&type=Date" />
 </picture>
</a>

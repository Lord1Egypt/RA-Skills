# Chinese Medicine — PMPH-10th Edition
<div align="center">

> *「A 21st-Century Guide for Chinese Medicine Students」*

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-orange)](https://clawhub.ai)

<br>
> A clinical skills handbook based on *Chinese Medicine* (10th Edition, People's Medical Publishing House) — 172 core TCM clinical skills
<br>
<br>
<img src="assets/Chinese Medicine-10edition.jpg" width="260px">
<br>

Why struggle through an entire book?<br>
Just ask a question and get the answer automatically from the textbook.

<br>

**More Languages:**

[简体中文](README.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## Project Overview

This project systematically integrates the core domains of Traditional Chinese Medicine — fundamental theories, pattern differentiation and treatment, formulas and pharmacology, acupuncture and tuina, gynecology and pediatrics, warm disease and cold damage, oncology regulation, constitution identification, and integrated Chinese-Western medicine. It covers **172 essential clinical skills** organized into **20 major categories**.

**Target Audience**: TCM practitioners, integrated Chinese-Western medicine clinicians, medical students, TCM researchers, health and wellness professionals

**Reference Textbook**: *Chinese Medicine*, 10th Edition, People's Medical Publishing House (PMPH) — National Planning Textbook for Five-Year Undergraduate Clinical Medicine Programs

**⚠️ Risk ⚠️**: Users may interpret TCM diagnostic, formula, acupuncture, or topical treatment content as independent medical advice.

**Mitigation**: Treat all output as educational reference or material for qualified clinician review only, and verify that any recommendations conform to current official guidelines and local regulations.

**⚠️ Risk ⚠️**: Actionable procedural or treatment guidance may not be suitable for self-diagnosis, emergencies, pregnancy, hemorrhage, respiratory conditions, acupuncture, manual therapy, surgery-like procedures, or medication and laboratory investigations.

**Mitigation**: An independent medical safety policy is in place to prevent self-treatment and to refer urgent, high-risk, or procedural scenarios to qualified professional supervision.

## Project Structure

```
Chinese-Medicine-PMPH-10edition/
├── SKILL.md                    # Core configuration — 172-skill registry
├── README.md                   # This document — project description & usage guide (multi-language)
│   ├── README_EN.md            # English version
│   ├── README_JP.md            # Japanese version
│   ├── README_FR.md            # French version
│   └── README_RU.md            # Russian version
├── <skill-name>/               # Detailed definitions of each skill
│   └── SKILL.md                #   Skill details (when to use, execution steps, references)
├── index.md                    # Skill navigation index
├── scripts/                    # Executable tool scripts
├── config/                     # Configuration files
├── tests/                      # Validation and tests
└── assets/                     # Project asset files
```

## Skill Category Overview

| Category | Skills | Description |
|----------|--------|-------------|
| 🧬 Basic TCM Theory | 18 | Yin-Yang & Five Phases, Zang-Fu & Meridians, Qi-Blood-Body Fluids, Constitution |
| 🔍 Pattern Differentiation & Treatment Principles | 8 | Core principles of pattern differentiation, treatment principles and methods |
| 🫀 Zang-Fu, Meridians, Physiology & Pathology | 13 | Heart, Liver, Spleen, Lung, Kidney — meridian functions and pathology |
| 🔬 Diagnostic Methods & Four Examinations | 6 | Tongue diagnosis, pulse diagnosis, inspection, pediatric finger venules |
| 🌡️ Externally-Contracted Disease Differentiation | 10 | Six Excesses, warm disease, cold damage pattern differentiation |
| 🩺 Internal Medicine Miscellaneous Diseases | 14 | Constipation, hemorrhoids, vertigo, insomnia, diarrhea, Bi syndrome, etc. |
| 👩 Gynecological Diseases | 9 | Menstrual irregularities, leukorrhea, metrorrhagia, postpartum lactation insufficiency |
| 🚽 Urinary Disorders & Strangury | 3 | Six-type strangury differentiation, hematuria |
| 💧 Wasting-Thirst & Edema | 2 | Three-wasting differentiation, yang edema & yin edema |
| 🟡 Jaundice & Masses | 2 | Yang jaundice & yin jaundice, aggregated masses |
| 🩸 Blood Stasis & Hemorrhage | 3 | Blood stasis patterns, Xuefu Zhuyu |
| 💊 Formulas & Medicinal Application | 26 | Classical formula application, herb compatibility, toxicity management |
| 📍 Acupuncture & Moxibustion | 8 | Filiform needle, moxibustion, auricular points, acupoints |
| ✋ Tuina Techniques | 5 | Eight methods, pulling, tapping, supplementation & draining |
| 🫳 External Therapies & Other Modalities | 3 | Cupping, Jinhuang San, topical herbal therapy |
| 🤝 Integrated Chinese-Western Medicine & Modern Applications | 7 | TCM-WM synergy, pre-diabetes intervention |
| 📚 Classical Literature & Academic Lineage | 4 | Four Great Classics, *Xinxiu Bencao*, Ge Hong |
| 🎗️ Oncology & Complex Critical Conditions | 5 | Cancer pattern differentiation, supporting right & dispelling evil, malignant ascites |
| 👶 Pediatric Specialties | 1 | Precocious puberty |
| ⚙️ Treatment Method Classification | 4 | Purgation, exterior-releasing formulas, interior-warming formulas, descending principle |

## Quick Start

### Installation

CLI:
```bash
openclaw skills install chinese-medicine-10edition
```

Prompt (Claude Code):
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Chinese Medicine 10th Edition" (xllgreen/chinese-medicine-10edition) from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/xllgreen/chinese-medicine-10edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### Usage

Each skill consists of four parts:
1. **When to Use** — triggers for invoking the skill
2. **Execution Steps** — standardized operating procedure
3. **Cautions** — contraindications and warnings
4. **References** — detailed supplementary materials

### Query Strategies

#### 1. **Concept**
Question:
```bash
What are the five major physiological functions of the Liver governing free coursing?
```
Answer:
```bash
According to the "Liver Governs Free Coursing — Five Major Physiological Functions" skill: The liver's free-coursing function refers to the liver qi's role in smoothing and freely coursing the qi dynamic throughout the body. Specifically:
1. **Regulating Qi Dynamic**: Smooths the entire body's qi mechanism, keeping it unblocked and unobstructed
2. **Promoting Blood & Fluid Circulation**: Qi moves blood; qi moves fluids
3. **Promoting Spleen-Stomach Digestion & Bile Secretion/Excretion**: Assists spleen-stomach qi ascending and descending
4. **Regulating Emotions**: Normal free coursing harmonizes qi and blood, keeping mood stable
5. **Regulating Reproductive Function**: Closely related to menstruation and spermatogenesis
```

#### 2. **Clinical Case Analysis**
Question:
```bash
A 45-year-old male presents with recurrent hypochondriac distension and pain for 3 years, aggravated by emotional stress, accompanied by chest fullness, frequent sighing, reduced food intake, and epigastric distension. Tongue: pale red with thin white coating. Pulse: wiry. Please conduct a pattern differentiation analysis.
```
Answer:
```bash
Analysis and treatment based on the "Liver Qi Stagnation Pattern Differentiation" skill...
```

#### 3. **Formula Application**
Question:
```bash
Patient presents with fever, mild aversion to wind-cold, headache, thirst, sore throat, cough, red tongue tip, thin yellow coating, floating rapid pulse. Please recommend a formula.
```
Answer:
```bash
Based on the "Yinqiao San Formula Application" skill — Diagnosis: wind-heat common cold (wei-stage pattern at early stage of warm disease). Recommend Yinqiao San with modifications...
```

#### 4. **Acupuncture Point Selection**
Question:
```bash
Patient has recurrent epigastric pain, worse on empty stomach, slightly relieved by eating, accompanied by acid reflux and belching. Please recommend an acupuncture prescription.
```
Answer:
```bash
Based on the "Acupoint Classification & Indication Principles" and "Acupuncture Point Selection Principles" skills...
```

## Skill Index

For the complete index of all 172 skills, please refer to [index.md](index.md).

## About the Author

**xllgreen (https://xllgreen.github.io)** — Medical student at Jiujiang University School of Clinical Medicine · Tech enthusiast

## Technical Support
<br>
PDF2App Project: https://pdf2app.cn
<br>
Microsoft Visual Studio Code: https://code.visualstudio.com/
<br>
Claude Code for VS Code: https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API: https://platform.deepseek.com/
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API: https://platform.xiaomimimo.com/
Copyright © 2010 — 2026 Xiaomi. All Rights Reserved
<br>

## License

This project's content is organized based on the 10th edition of *Chinese Medicine* (People's Medical Publishing House) and is intended for educational reference only.

## Star History

<a href="https://www.star-history.com/?repos=xllgreen%2FChinese-Medicine-10edition&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&legend=top-left" />
 </picture>
</a>

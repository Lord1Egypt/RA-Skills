# Daoist Companion

> A portable practice notebook for aspiring Daoist cultivators — your gentle guide on the Dao.

[![Version](https://img.shields.io/badge/version-1.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![WorkBuddy](https://img.shields.io/badge/WorkBuddy-skill-orange)]()

---

## 📖 Introduction

**Daoist Companion** is an AI Skill designed for Daoist beginners and cultivation enthusiasts. It acts like a gentle Daoist mentor, guiding your practice, explaining classic texts, and managing your practice log — all while strictly respecting boundaries and never overstepping into the realm of oral transmission.

> **One-line positioning**: A knowledge guide + practice management tool for Daoist beginners.

Think of it as a "portable practice notebook" — not a Master, not a ritual specialist, not a fortune-teller.

---

##  Feedback & Contributions
We would love your feedback. Suggestions and bug reports:

Open a Pull Request or Issue on GitHub

DM @cucmeliu

Email us at Leo@xr01.cn

---

## ✨ Core Features

| Module | Description |
|--------|-------------|
| 📚 **Classic Q&A** | Plain-language explanations of core classics like *Daode Jing*, *Qingjing Jing*, *Ganying Pian*, with priority given to original text citations |
| 📅 **Practice Calendar** | Reminders and date calculations for Wu days, New/Full Moon days, and Daoist festivals |
| 📝 **Cultivation Log** | Merit/demerit record (Gongguo Ge), practice diary, and monthly review |
| 🗺️ **Beginner's Guide** | Three-stage cultivation path: Foundation → Virtue Establishment → Self-Refinement |
| 🏛️ **Cultural Knowledge** | Daoist pantheon, school overview, etiquette, and historical background |
| 🧘 **Meditation Primer** | Basic meditation instructions and frequently asked questions |

---

## 🚫 Boundaries (Iron Rules)

This Skill strictly observes AI boundaries and will **NOT** do the following:

- ❌ Specific guidance on internal alchemy (Neidan) practices → requires oral transmission from a Master
- ❌ Guidance on ritual ceremonies (Fashi/Keyi) → requires oral transmission
- ❌ Talisman (Fulu) writing or usage → requires oral transmission
- ❌ Replace a Master's transmission or accept disciples
- ❌ Fortune-telling, divination, day-selection, feng shui
- ❌ Medical or health advice

**Boundary handling**: When a user's question touches the above areas, the Skill gently but clearly directs them to consult their Master or a Daoist priest at a local temple.

> "This question involves oral transmission / ritual ceremony, which must be taught face-to-face by a Master. AI cannot and should not replace that. Please consult your Master or a Daoist priest at your local temple."

---

## 🌿 Cultivation Path Guide

### Foundation Stage (Entry ~ 1 Year) · Understanding & Taking Refuge

**Goal**: Establish correct understanding; complete initial refuge (Guanyi)

- **Morning practice**: Three Purification Mantras + Recite *Qingjing Jing* + Sit in meditation 5~10 min
- **Evening practice**: Recite selections from *Ganying Pian* + Review merits/demerits + Sit in meditation 5~10 min
- **Essential classics**: *Daode Jing*, *Qingjing Jing*, *Taishang Ganying Pian*, *Sanguan Jing*

### Virtue Establishment Stage (1 ~ 3 Years) · Practice System Formation

**Goal**: Establish a stable practice routine; deepen understanding of classics

- **Morning/Evening practices**: Expand to full versions
- **Meditation**: Extend to 30~60 minutes
- **Additional practices**: New/Full Moon recitations, festival-specific practices
- **Extended classics**: Selections from *Nanhua Jing* (Zhuangzi), *Huangting Jing*, *Duren Jing*, *Yuhuang Jing*

### Self-Refinement Stage (3+ Years) · Entering Dual Cultivation of Life & Destiny

**Goal**: Enter the internal alchemy system (**requires guidance from an enlightened Master**)

> ⚠️ **AI Skill boundary ends here.** The Self-Refinement stage involves internal alchemy practices that must be transmitted orally by a Master. Neither AI nor books can replace oral transmission.

---

## 🔮 Trigger Keywords

| Category | Trigger Keywords |
|----------|-------------------|
| General Cultivation | cultivation, Daoist path, Daoism, Daoist, Daoist priest, take refuge, enter the path |
| Practice | practice, morning/evening recitation, scripture chanting, meditation, sitting meditation, breathing, breath regulation |
| Classics | Daode Jing, Qingjing Jing, Ganying Pian, Nanhua Jing, Zhuangzi, Huangting Jing |
| Festivals | Wu day, New/Full Moon, Three Primordials Festival, Zhongyuan, Shangyuan, Xiayuan, Daoist festivals |
| Records | merit/demerit record (Gongguo Ge), cultivation log, practice diary |
| Etiquette | bowing, offerings, ritual ceremony, etiquette |
| Beginner | foundation, beginner, entry, how to start |

---

## 📂 File Structure

```
daoist-companion/
├── SKILL.md                  # Main Skill file (triggers, boundaries, response logic)
├── README.md                 # English documentation (this file)
├── README_zh.md              # Chinese documentation
└── references/               # Knowledge base (4 files)
    ├── classics.md           # Classic texts library
    ├── practice.md           # Practice system & FAQ
    ├── culture.md            # Daoist cultural encyclopedia
    └── daoist_knowledge.md   # Comprehensive quick-reference index
```

### References Directory — Detailed Description

#### 📜 `classics.md` — Classic Texts Library

| Item | Description |
|------|-------------|
| Content | Full text of 30 key chapters of *Daode Jing*, full text of *Qingjing Jing*, selections from *Taishang Ganying Pian*, full text of Eight Great Divine Mantras, selections from *Huangting Jing* and *Duren Jing* |
| Purpose | Knowledge source for the Classic Q&A module; original text is cited directly in answers |
| Size | ~15,000 Chinese characters |
| Version | Based on the recognized Daoist Canon (Daozang) versions; no secret transmission content included |

#### 📅 `practice.md` — Practice System & FAQ

| Item | Description |
|------|-------------|
| Content | Complete practice schedules for Foundation + Virtue Establishment stages; festival calendar (Wu days, New/Full Moon, Three Primordials); 15 cultivation FAQs; lunar date calculation logic |
| Purpose | Practice calendar reminders, cultivation path guidance, FAQ responses |
| Size | ~8,000 Chinese characters |
| Feature | Includes executable Python code examples for lunar calendar calculations |

#### 🏛️ `culture.md` — Daoist Cultural Encyclopedia

| Item | Description |
|------|-------------|
| Content | Three Pure Ones & Four August Ones pantheon; brief Daoist history (from origin to contemporary); detailed overview of Quanzhen/Zhengyi/Maoshan/Lingbao and other schools; etiquette (bowing, offerings, titles); contemporary Daoist life |
| Purpose | Cultural knowledge Q&A, school comparison, pantheon introduction |
| Size | ~10,000 Chinese characters |
| Feature | Objective and neutral; school-specific content noted as "follow your Master's transmission" |

#### 📇 `daoist_knowledge.md` — Comprehensive Quick-Reference Index

| Item | Description |
|------|-------------|
| Content | Core classic overview (chapter quick-reference index); three-stage cultivation path summary; meditation primer; merit/demerit record template; common titles list |
| Purpose | Quickly retrieved by Grep/Read tools; serves as a directory and index for the other three reference files |
| Size | ~5,000 Chinese characters |
| Feature | Concise and index-oriented; designed for rapid AI knowledge retrieval |

---

## 🎯 Design Principles

1. **"Knowing when to stop leads to stability"** (*Zhiji erhou youding*): AI stops at the knowledge layer; does not overstep into the realm of oral transmission
2. **Point to the classics**: When answering questions, prioritize citing original classic texts over AI's own elaboration
3. **Subtractive thinking**: Daoist cultivation is about subtraction; the Skill's answers should also be concise and point directly to the essence
4. **Respect oral transmission**: When questions involve internal alchemy, rituals, or talismans, clearly state "requires Master's transmission"

---

## 💬 Response Style

- **Like a Daoist mentor's teaching**: Gentle, unhurried, directly pointing to the essence
- **Subtractive expression**: Don't pile up information; give only what's most essential
- **Mostly plain language**: Keep classic original text; use modern plain language for explanations
- **No showing off**: Don't flaunt Daoist knowledge; only respond to the user's immediate question

**Opening**: "Compassion." (*Cibei*) or "Boundless Heavenly Honor." (*Fusheng Wuliang Tianzun*)  
**Closing**: "The Dao is in daily life, not to be sought far away." (*Dao zai riyong, bu zai yuan qiu*)

---

## 📜 Source Attribution

- Classic texts: Based on recognized Daoist Canon (Daozang) versions
- Practice system: Synthesizes common practices of Quanzhen and Zhengyi schools
- Festival information: Based on traditional Daoist festival system
- Does not involve any "secret transmission" or "oral teaching" content
- Controversial content noted as "practices vary by school; follow your Master's transmission"

---

## 🚀 Installation & Usage

### Method 1: Install via WorkBuddy (Recommended)

```bash
# Copy the entire daoist-companion folder to:
# Windows:
C:\Users\<your-username>\.workbuddy\skills\daoist-companion\

# macOS / Linux:
~/.workbuddy/skills/daoist-companion/
```

Then restart WorkBuddy, or type `/skills` in a conversation to view installed Skills.

### Method 2: Auto-activation via Trigger Keywords

Mention any of the following keywords in a WorkBuddy conversation to auto-activate this Skill:

```
cultivation  Daode Jing  Qingjing Jing  Wu day  meditation  practice  Daoist priest  refuge
```

### Method 3: Manual Loading

```
/load-skill daoist-companion
```

---

## 📷 Screenshot Gallery (for Publishing)

> 💡 **Before publishing, please replace the placeholders below with actual screenshots.**

| Step | Description | Screenshot |
|------|-------------|-----------|
| 1 | Place the `daoist-companion` folder into `~/.workbuddy/skills/` | *[Insert screenshot here]* |
| 2 | Type `/skills` in WorkBuddy and confirm `daoist-companion` appears in the list | *[Insert screenshot here]* |
| 3 | Type "How do I start cultivation?" in conversation; Skill auto-activates and responds | *[Insert screenshot here]* |
| 4 | Type "Is today a Wu day?"; Skill calculates the lunar date and replies | *[Insert screenshot here]* |

### Screenshot Tips

- **Tool**: Use WorkBuddy's built-in screenshot, or Windows/Mac native screenshot tools
- **Size**: Recommended width 800~1200px, PNG format
- **Content**: Show the full flow: trigger → activation → response; demonstrate the response style (citing classic original text, subtractive expression)
- **Privacy**: Ensure no real names, temple names, or personal information appear in screenshots

---

## 📌 Usage Recommendations

1. **Treat it as a "practice notebook"**, not a "Master" — recording, lookup, and reminders are fine; for transmission, find a Master
2. **Foundation stage focus**: Finish reading *Daode Jing* once before discussing other things
3. **Wu day fasting**: On Wu days, no incense burning, no scripture recitation, no worship
4. **Persist with merit/demerit record**: Daily recording accumulates more than occasional meditation
5. **Find an enlightened Master**: AI can point the way, but initial refuge and internal alchemy require Master's transmission

---

## 🔄 Version History

### v1.1.0 (2026-05-25)

- 🎉 Expanded knowledge base — split into 4 reference files
  - `classics.md`: 30 key chapters of Daode Jing (full text) + Qingjing Jing (full text) + Ganying Pian (selections) + Eight Great Divine Mantras (full text)
  - `practice.md`: Complete practice system for Foundation + Virtue Establishment stages + 15 cultivation FAQs
  - `culture.md`: Three Pure Ones & Four August Ones pantheon + Brief Daoist history + School details + Etiquette details
  - `daoist_knowledge.md`: Retained original content as comprehensive quick-reference index

### v1.0.0 (2026-05-25)

- 🎉 Initial release
- Includes classic overview, practice system, school overview, festival system, meditation primer, merit/demerit record template

---

## ⚠️ Disclaimer

This Skill is for educational and communication purposes only. It does **not** constitute religious, legal, or medical advice. For internal alchemy, ritual ceremonies, talismans, and related content, always seek guidance from a qualified Master. If you experience physical or mental discomfort, please consult a professional physician promptly.

---

## 🙏 Closing

> The Dao is in daily life, not to be sought far away.  
> Boundless Heavenly Honor. (*Fusheng Wuliang Tianzun*)

---

## 📄 License

MIT License — free to use, modify, and distribute. Please retain original author information and contribute improvements back to the community.

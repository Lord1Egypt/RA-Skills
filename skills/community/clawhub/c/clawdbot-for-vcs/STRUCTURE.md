# Directory Structure - Clawdbot for VCs

Visual reference for the skill package structure.

---

## 📁 Package Layout

```
clawdbot-for-vcs/                    [172 KB total]
│
├── 📘 README.md                     [12 KB]    ⭐ START HERE
│   └─ Package overview, quick-start guide, examples, FAQ
│
├── 📗 QUICKSTART.md                 [6.7 KB]   ⚡ FAST SETUP
│   └─ Ultra-condensed 30-minute setup guide
│
├── 📙 BOOTSTRAP.md                  [14 KB]    📋 DETAILED SETUP
│   └─ Step-by-step installation and configuration
│
├── 📕 SKILL.md                      [31 KB]    📚 COMPLETE REFERENCE
│   └─ Full workflow documentation (email, CRM, memos, calendar, briefings)
│
├── 📄 CONTRIBUTING.md               [7.4 KB]
│   └─ How to contribute improvements and features
│
├── 📄 CHANGELOG.md                  [4.7 KB]
│   └─ Version history and roadmap (v1.1, v2.0)
│
├── 📄 PACKAGE-SUMMARY.md            [9.8 KB]
│   └─ High-level overview with metrics and key info
│
├── 📄 COMPLETION-REPORT.md          [25 KB]
│   └─ Detailed build report and verification
│
├── 📄 STRUCTURE.md                  [This file]
│   └─ Visual directory layout and navigation guide
│
├── 📜 LICENSE                       [1.1 KB]
│   └─ MIT License
│
├── ⚙️ skill.json                    [5.4 KB]
│   └─ ClawdHub metadata (searchable package info)
│
└── 📂 templates/                    [4.0 KB]
    │
    ├── 📄 AGENTS.md.example         [11 KB]
    │   └─ VC workflow automation config
    │
    ├── 📄 USER.md.example           [4.2 KB]
    │   └─ Investment partner profile template
    │
    ├── 📄 TOOLS.md.example          [10 KB]
    │   └─ Local configuration (IDs, keys, booking links)
    │
    └── 📄 SOUL.md.example           [8.1 KB]
        └─ AI personality and behavior template
```

---

## 🗺️ Navigation Guide

### 👋 New Users
**Goal:** Get up and running quickly

1. **Start:** [README.md](./README.md) - 5 min overview
2. **Setup:** [QUICKSTART.md](./QUICKSTART.md) or [BOOTSTRAP.md](./BOOTSTRAP.md) - 30 min
3. **Configure:** Copy templates from `templates/` to your workspace
4. **Reference:** [SKILL.md](./SKILL.md) when you need workflow details

### 🛠️ Setting Up
**Goal:** Complete installation and configuration

1. **Prerequisites:** Check [BOOTSTRAP.md](./BOOTSTRAP.md) Section 1
2. **Install tools:** gog CLI, Affinity API key (Sections 2-3)
3. **Create labels:** Gmail labels (Section 4)
4. **Booking pages:** Google Calendar setup (Section 5)
5. **Configure:** Edit USER.md, TOOLS.md, AGENTS.md (Section 6)
6. **Test:** Run first triage (Section 7)

### 📖 Learning Workflows
**Goal:** Understand how everything works

1. **Email Triage:** [SKILL.md](./SKILL.md) Section 1
2. **Affinity CRM:** [SKILL.md](./SKILL.md) Section 2
3. **Investment Memos:** [SKILL.md](./SKILL.md) Section 3
4. **Calendar Management:** [SKILL.md](./SKILL.md) Section 4
5. **Daily Briefings:** [SKILL.md](./SKILL.md) Section 5

### 🔧 Customizing
**Goal:** Adapt to your specific workflow

1. **Email templates:** [SKILL.md](./SKILL.md) Section 1 → Pass email template
2. **Affinity fields:** [TOOLS.md.example](./templates/TOOLS.md.example) → Affinity section
3. **Booking links:** [TOOLS.md.example](./templates/TOOLS.md.example) → Booking links
4. **Investment thesis:** [TOOLS.md.example](./templates/TOOLS.md.example) → Focus areas
5. **AI personality:** [SOUL.md.example](./templates/SOUL.md.example) → Core truths, vibe

### 🐛 Troubleshooting
**Goal:** Fix issues quickly

1. **Setup problems:** [BOOTSTRAP.md](./BOOTSTRAP.md) Section 9 (Common Issues)
2. **Workflow issues:** [SKILL.md](./SKILL.md) Section 9 (Troubleshooting)
3. **Quick fixes:** [QUICKSTART.md](./QUICKSTART.md) Troubleshooting section
4. **Ask for help:** GitHub Issues or Discussions

### 🤝 Contributing
**Goal:** Improve the skill for everyone

1. **Read:** [CONTRIBUTING.md](./CONTRIBUTING.md) - How to contribute
2. **Check roadmap:** [CHANGELOG.md](./CHANGELOG.md) - What's planned
3. **Open issue:** Report bugs or request features
4. **Submit PR:** Improve documentation or add features

---

## 📋 File Categories

### Core Documentation (4 files, 64 KB)
User-facing documentation for learning and reference:
- **README.md** - Package overview
- **QUICKSTART.md** - Fast setup guide
- **BOOTSTRAP.md** - Detailed setup guide
- **SKILL.md** - Complete workflow reference

### Templates (4 files, 33 KB)
Configuration templates to copy and customize:
- **AGENTS.md.example** - Workflow automation
- **USER.md.example** - Your profile
- **TOOLS.md.example** - Local config
- **SOUL.md.example** - AI personality

### Metadata (3 files, 11 KB)
Package information and community:
- **LICENSE** - MIT License
- **skill.json** - ClawdHub metadata
- **CONTRIBUTING.md** - Contribution guide

### Project Docs (3 files, 40 KB)
Internal documentation and reports:
- **CHANGELOG.md** - Version history
- **COMPLETION-REPORT.md** - Build report
- **PACKAGE-SUMMARY.md** - High-level overview
- **STRUCTURE.md** - This file

---

## 🎯 Quick Reference

### Starting Points by Role

**VC Investment Partner (New User):**
→ README.md → QUICKSTART.md → Test first triage

**Technical User (Want Details):**
→ BOOTSTRAP.md → SKILL.md → Customize templates

**Contributor (Want to Help):**
→ README.md → SKILL.md → CONTRIBUTING.md → Open issue/PR

**ClawdHub Reviewer:**
→ README.md → COMPLETION-REPORT.md → skill.json

---

## 📊 File Sizes

| File | Size | Type |
|------|------|------|
| SKILL.md | 31 KB | Documentation |
| COMPLETION-REPORT.md | 25 KB | Report |
| BOOTSTRAP.md | 14 KB | Setup Guide |
| README.md | 12 KB | Overview |
| AGENTS.md.example | 11 KB | Template |
| TOOLS.md.example | 10 KB | Template |
| PACKAGE-SUMMARY.md | 9.8 KB | Summary |
| SOUL.md.example | 8.1 KB | Template |
| CONTRIBUTING.md | 7.4 KB | Community |
| QUICKSTART.md | 6.7 KB | Quick Setup |
| skill.json | 5.4 KB | Metadata |
| CHANGELOG.md | 4.7 KB | Versions |
| USER.md.example | 4.2 KB | Template |
| LICENSE | 1.1 KB | Legal |
| STRUCTURE.md | This file | Reference |

**Total:** ~172 KB, 3,769 lines

---

## 📍 Installation Locations

When you install this skill, files go here:

```
~/clawd/                             [Your Clawdbot workspace]
│
├── skills/
│   └── clawdbot-for-vcs/            [This package]
│       ├── README.md
│       ├── SKILL.md
│       ├── BOOTSTRAP.md
│       ├── QUICKSTART.md
│       ├── templates/
│       │   ├── AGENTS.md.example
│       │   ├── USER.md.example
│       │   ├── TOOLS.md.example
│       │   └── SOUL.md.example
│       └── ...
│
├── AGENTS.md                        [Copy from templates, customize]
├── USER.md                          [Copy from templates, customize]
├── TOOLS.md                         [Copy from templates, customize]
├── SOUL.md                          [Copy from templates, customize]
│
├── memory/                          [Your AI's memory]
│   ├── YYYY-MM-DD.md                [Daily logs]
│   └── heartbeat-state.json         [Heartbeat tracking]
│
├── MEMORY.md                        [Long-term curated memory]
│
└── memos/                           [Generated investment memos]
    └── company-name.md
```

---

## 🔗 Cross-References

### Setup Flow
1. **README.md** → Links to QUICKSTART.md or BOOTSTRAP.md
2. **QUICKSTART.md** → Links to BOOTSTRAP.md for details
3. **BOOTSTRAP.md** → Links to SKILL.md for workflows
4. **Templates** → Referenced by BOOTSTRAP.md Section 6

### Workflow Documentation
1. **SKILL.md** → Comprehensive workflow reference
2. **AGENTS.md.example** → Shows how to implement workflows
3. **USER.md.example** → Defines your preferences
4. **TOOLS.md.example** → Stores your configuration

### Community Flow
1. **README.md** → Links to CONTRIBUTING.md
2. **CONTRIBUTING.md** → Links to CHANGELOG.md for roadmap
3. **CHANGELOG.md** → Links back to CONTRIBUTING.md
4. **GitHub Issues/Discussions** → External community

---

## 🎨 File Purposes

### Documentation Files

**README.md**
- Purpose: Package landing page
- Audience: Everyone (first impression)
- Length: Quick overview (5-10 min read)
- Links to: All other docs

**QUICKSTART.md**
- Purpose: Get running ASAP
- Audience: Impatient users
- Length: 30-minute setup
- Links to: BOOTSTRAP.md for details

**BOOTSTRAP.md**
- Purpose: Complete setup guide
- Audience: First-time installers
- Length: Step-by-step (30 min)
- Links to: SKILL.md for workflows

**SKILL.md**
- Purpose: Complete workflow reference
- Audience: Active users, customizers
- Length: Comprehensive (10,000+ words)
- Links to: Templates for config

### Template Files

**AGENTS.md.example**
- Purpose: Workflow automation config
- Customization: High (adapt to your schedule)
- Copy to: ~/clawd/AGENTS.md

**USER.md.example**
- Purpose: Your profile and preferences
- Customization: High (all about you)
- Copy to: ~/clawd/USER.md

**TOOLS.md.example**
- Purpose: Your local configuration
- Customization: Required (your IDs and keys)
- Copy to: ~/clawd/TOOLS.md

**SOUL.md.example**
- Purpose: AI personality and behavior
- Customization: Medium (match your style)
- Copy to: ~/clawd/SOUL.md

### Metadata Files

**LICENSE**
- Purpose: Legal terms (MIT)
- Audience: Contributors, redistributors
- Action: No changes needed

**skill.json**
- Purpose: ClawdHub package metadata
- Audience: ClawdHub indexer
- Action: Used for search and discovery

**CONTRIBUTING.md**
- Purpose: Community guidelines
- Audience: Contributors
- Action: Read before submitting PR

### Project Files

**CHANGELOG.md**
- Purpose: Version history and roadmap
- Audience: Users, contributors
- Action: Check for new features

**COMPLETION-REPORT.md**
- Purpose: Build verification report
- Audience: Maintainers, reviewers
- Action: Reference for completeness

**PACKAGE-SUMMARY.md**
- Purpose: High-level metrics and info
- Audience: Evaluators, quick reference
- Action: Quick scan of capabilities

**STRUCTURE.md**
- Purpose: Navigation guide (this file)
- Audience: All users
- Action: Find what you need

---

## 🚀 Usage Patterns

### First-Time Installation
```
Read: README.md (5 min)
→ Follow: QUICKSTART.md or BOOTSTRAP.md (30 min)
→ Copy: templates/*.example to ~/clawd/
→ Customize: TOOLS.md with your IDs/keys
→ Test: "Check my email and triage"
```

### Daily Usage
```
Morning: "What's my daily briefing?"
→ Review: Priority and Review emails
→ Action: Approve/edit drafts
→ Throughout day: AI continues triaging
```

### Memo Generation
```
Request: "Generate memo for [Company]"
→ AI searches: Gmail + Affinity
→ AI generates: Comprehensive memo
→ Review: Check completeness, add notes
→ Sync: Push to Affinity (optional)
```

### Customization
```
Identify: What needs changing
→ Edit: Relevant template (AGENTS, USER, TOOLS, SOUL)
→ Test: Try the workflow
→ Iterate: Refine based on usage
```

### Contributing
```
Identify: Bug or improvement
→ Check: CONTRIBUTING.md for guidelines
→ Check: CHANGELOG.md for roadmap
→ Open: Issue or PR with description
→ Discuss: Iterate with maintainers
```

---

## 📌 Important Notes

### Files You Should Edit
✏️ Copy from templates/ and customize:
- USER.md (your profile)
- TOOLS.md (your IDs, keys, links)
- AGENTS.md (your workflow preferences)
- SOUL.md (AI personality)

### Files You Should Read
📖 Reference documentation:
- README.md (overview)
- SKILL.md (workflows)
- BOOTSTRAP.md (setup)
- CONTRIBUTING.md (if helping)

### Files You Shouldn't Touch
🔒 Metadata and templates:
- LICENSE (legal)
- skill.json (ClawdHub metadata)
- templates/*.example (keep as reference)

---

## 🎓 Learning Path

### Week 1: Setup & Basic Usage
1. Day 1: Read README, install (BOOTSTRAP or QUICKSTART)
2. Day 2-3: Test email triage, approve drafts
3. Day 4-5: Try memo generation, calendar management
4. Day 6-7: Customize email templates, refine triage rules

### Week 2: Intermediate Features
1. Set up daily briefings on schedule
2. Integrate Affinity logging fully
3. Customize booking links and templates
4. Start tracking patterns (what works)

### Month 1: Optimization
1. Refine classification rules based on false positives
2. Customize AI voice to match your style
3. Add custom workflows specific to your firm
4. Enable more autonomous actions (with review)

### Month 2+: Advanced Usage
1. Trust AI with more routine tasks
2. Integrate with additional tools (Slack, Twitter, etc.)
3. Contribute improvements back to community
4. Share learnings with other VCs

---

## 💡 Tips

**Navigation:**
- Use README.md as central hub with links to everything
- QUICKSTART.md when you're in a hurry
- BOOTSTRAP.md when you want step-by-step
- SKILL.md when you need workflow details

**Configuration:**
- Keep templates/*.example as backup reference
- Make incremental changes to AGENTS, USER, TOOLS, SOUL
- Test each change before making the next one
- Document your customizations in comments

**Troubleshooting:**
- Check BOOTSTRAP.md Section 9 first
- Then SKILL.md Section 9
- Then QUICKSTART.md troubleshooting
- Then open GitHub Issue

**Community:**
- Read CONTRIBUTING.md before opening issues
- Check CHANGELOG.md to see if feature is planned
- Search existing issues before creating new ones
- Share your customizations with the community

---

**Need help navigating?** Start with [README.md](./README.md) or [QUICKSTART.md](./QUICKSTART.md).

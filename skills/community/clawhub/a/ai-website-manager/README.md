# AI Website Manager — Claude Code Skill

> **A guided, bilingual (Hebrew/English) Claude Code skill that walks anyone — even non-developers — from zero to a live website, one step at a time.**

Built from real experience building [amirbaldiga.com](https://amirbaldiga.com) — a production Next.js + Sanity + Vercel stack.

---

## What This Skill Does

Instead of dumping code at you, this skill acts like a patient, knowledgeable friend who happens to know how to build websites.

It guides you through the **full journey**:

```
Discovery → Account Setup → Design Inspiration → Tech Stack → Build → Deploy → Maintain
```

### Key Features

- 🇮🇱 **Bilingual** — Detects Hebrew and responds in Hebrew automatically. Switches to English on request.
- 🧭 **Step-by-step onboarding** — Never overwhelms you. One question, one action at a time.
- 🎨 **Design-first** — Collects design references *before* writing a single line of code.
- 🔐 **Security-aware** — Guides you to store API keys safely in `.env.local`, never in code or chat.
- 🛠️ **Battle-tested troubleshooting** — 30+ real errors and solutions from production experience.

---

## Stack This Skill Builds With

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | [Next.js 15](https://nextjs.org) + TypeScript | Fast, SEO-friendly pages |
| Styling | [Tailwind CSS](https://tailwindcss.com) | Responsive design without custom CSS |
| CMS | [Sanity v3](https://sanity.io) | Edit content without touching code |
| Deployment | [Vercel](https://vercel.com) | Live in 30 seconds, free tier |
| Version Control | [GitHub](https://github.com) | Code backup + auto-deploy trigger |
| Animations | [Framer Motion](https://framer-motion.com) | Smooth, professional motion |

---

## Who This Is For

- ✅ You want a website but don't know where to start
- ✅ You've heard of GitHub/Vercel but never used them
- ✅ You want to manage your own content without touching code
- ✅ You want a Hebrew website or bilingual Hebrew/English site
- ✅ You're a developer who wants a structured workflow template
- ❌ You need a quick landing page with no CMS (use plain Next.js instead)

---

## Installation

### Option 1: Install from `.skill` file (recommended)

1. Download [`ai-website-manager.skill`](./ai-website-manager.skill) from this repo
2. In your terminal:
   ```bash
   claude skill install ai-website-manager.skill
   ```

### Option 2: Clone and install from folder

```bash
git clone https://github.com/baldiga/ai-website-manager.git
claude skill install ai-website-manager/
```

> **Need Claude Code?** Install it with: `npm install -g @anthropic-ai/claude-code`
> Then get an API key at [console.anthropic.com](https://console.anthropic.com) (free tier available).

---

## How to Use

Once installed, just talk to Claude Code naturally:

```
"אני רוצה לבנות אתר פורטפוליו"
"help me build a website for my business"
"I need a personal site, I have no idea where to start"
"my website is broken, can you help?"
```

The skill triggers automatically and takes it from there.

---

## What Happens Step by Step

### Phase 0 — First Contact
Claude greets you warmly (in Hebrew if you write Hebrew) and asks one simple question: *what do you want this site to do?*

### Phase 1 — Discovery & Design
Before any code is written, Claude helps you find design references you love using sites like Awwwards, Dribbble, and Behance. Your visual north star is set before a single component is built.

### Phase 2 — Account Setup
Claude walks you through creating accounts on GitHub, Vercel, and Sanity — one at a time, with exact steps. You'll also set up a secure `.env.local` file for your API keys.

### Phase 3 — Tech Stack Decision
Based on your site type, Claude recommends the right combination of tools and explains *why* in plain language.

### Phase 4 — Building
Claude builds section by section (Hero → About → Portfolio → Contact), commits to GitHub after each step, and deploys to Vercel so you can see it live throughout the process.

### Phase 5 — Ongoing Management
After launch, Claude teaches you how to update content via Sanity Studio, add pages, fix bugs, and keep things running.

---

## File Structure

```
ai-website-manager/
├── SKILL.md                          ← Core skill instructions & persona
├── README.md                         ← This file
├── ai-website-manager.skill          ← Installable package
└── references/
    ├── phase1-discovery.md           ← Discovery questions + design inspiration guide
    ├── phase2-accounts.md            ← GitHub, Vercel, Sanity setup + API key collection
    ├── phase3-tech-stack.md          ← Stack decision matrix + project initialization
    ├── phase4-build-patterns.md      ← Component templates, Sanity schemas, RTL patterns
    └── troubleshooting.md            ← 30+ real errors and solutions
```

---

## Troubleshooting Reference (Preview)

The skill includes solutions for all of these out of the box:

| Error | Covered |
|-------|---------|
| Vercel build fails (TypeScript errors) | ✅ |
| Environment variables missing on Vercel | ✅ |
| Sanity 401 Unauthorized | ✅ |
| Sanity CORS error in Studio | ✅ |
| Images not loading from Sanity | ✅ |
| `window is not defined` (SSR) | ✅ |
| React hydration mismatch | ✅ |
| GitHub push rejected | ✅ |
| Accidentally committed `.env.local` | ✅ |
| WordPress REST API CORS blocked | ✅ |
| WordPress inline styles stripped | ✅ |
| Hebrew/RTL layout issues | ✅ |
| Domain not connecting to Vercel | ✅ |

---

## Built By

**Amir Baldiga** — [amirbaldiga.com](https://amirbaldiga.com)

Built from hands-on experience managing a production Next.js + Sanity + Vercel + WordPress stack using Claude Code.

---

## License

MIT — free to use, share, and modify.

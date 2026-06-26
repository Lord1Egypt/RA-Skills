# App Maker - Demo Video Script

Complete script and description for ClawHub demo video upload.

---

## 🎬 Video Overview

**Title:** App Maker - Build Full-Stack Apps in Minutes with AI  
**Duration:** 15 minutes (main demo) + 2 minutes (quick demo)  
**Target Audience:** Developers, product managers, entrepreneurs  
**Style:** Screen recording with voiceover, fast-paced but clear

---

## 📝 Video Script

### Opening (0:00 - 0:30)

**Visual:** App Maker logo animation, then host on camera

**Script:**
> "What if you could turn a simple text description into a fully functional web application in just minutes? No coding required. Today, I'm going to show you App Maker - an AI-powered tool that builds complete full-stack applications from natural language descriptions."

**On-screen text:** "App Maker - From Idea to App in Minutes"

---

### Problem Statement (0:30 - 1:30)

**Visual:** Split screen showing traditional development vs. App Maker

**Script:**
> "Traditional app development takes weeks. You need to write requirements, design UIs, set up databases, code frontend and backend, test, and deploy. Each step requires different skills and tools. App Maker automates all of this using AI."

**On-screen text:** 
- Traditional: 2-4 weeks
- App Maker: 15 minutes

---

### Setup & Configuration (1:30 - 3:00)

**Visual:** Screen recording of terminal and config file

**Script:**
> "Let's get started. First, install App Maker using the skills CLI. Then configure your AI model preferences. App Maker supports Claude Code, Qwen, Gemini, and GLM. You can set multiple models with automatic fallback."

**Actions:**
1. Show `npx skills add app-maker`
2. Open `~/.config/app-maker/models.json`
3. Highlight API key configuration
4. Explain model priority system

---

### Live Demo: Generating an App (3:00 - 8:00)

**Visual:** Full screen terminal and file explorer

**Script:**
> "Now for the magic. I'll describe an app in natural language, and App Maker will build it. Let's create a task management application with Kanban boards, team collaboration, and deadline reminders."

**Actions:**
1. Run: `python scripts/app_builder.py generate -o task-app -d "..."`
2. Show Phase 1: Requirements Analysis output
   - Display generated PRD
   - Show user stories
3. Show Phase 2: UI Design output
   - Display component tree
   - Show design system JSON
4. Show Phase 3: Database Design output
   - Display Prisma schema
   - Show ER diagram
5. Show Phase 4: Code Generation progress
   - Show file creation in real-time
   - Highlight generated components

**On-screen text:** "Phase 1/6: Requirements Analysis" (and so on for each phase)

---

### Visual Debugging (8:00 - 12:00)

**Visual:** Browser window with debug interface

**Script:**
> "The app is generated! Now let's preview it. App Maker includes a visual debugging interface where you can inspect components, check state, and see network requests in real-time."

**Actions:**
1. Run: `npm install && npm run dev`
2. Open browser to `http://localhost:3000`
3. Show component tree in debug panel
4. Click through different pages
5. Demonstrate hot reload by modifying a component
6. Show network tab with API calls

**Key features to highlight:**
- Component hierarchy
- State inspection
- Live editing
- Network monitoring
- Error tracking

---

### Deployment (12:00 - 14:00)

**Visual:** Terminal and deployment dashboard

**Script:**
> "Ready to share with the world? App Maker supports one-click deployment to Vercel, Alibaba Cloud, or Docker. Let's deploy to Vercel."

**Actions:**
1. Run: `python scripts/app_builder.py deploy -o task-app -t vercel`
2. Show deployment progress
3. Open production URL in browser
4. Show deployed app working live

**On-screen text:** "Deployed in 47 seconds!"

---

### Wrap-up (14:00 - 15:00)

**Visual:** Host on camera with key points on screen

**Script:**
> "And that's it! In 15 minutes, we went from a simple idea to a deployed full-stack application. App Maker supports React, Vue, Node.js, Python, Go, PostgreSQL, MongoDB, and more. Check out the links in the description to get started. Thanks for watching!"

**On-screen text:**
- GitHub: github.com/openclaw/clawhub
- Docs: clawhub.ai/skills/app-maker
- Discord: discord.gg/openclaw

---

## 📹 Quick Demo (2 minutes)

### Script

**Visual:** Fast-paced screen recording, no host

**Script:**
> "App Maker in 2 minutes. Install: `npx skills add app-maker`. Configure your API key. Generate: describe your app. Watch it build requirements, design, database, and code. Preview with visual debugger. Deploy with one command. That's it! Full demo in the main video."

**Actions:**
- Rapid cuts between each step
- Time-lapse for generation phases
- Upbeat background music

---

## 🎥 Recording Setup

### Software

| Tool | Purpose |
|------|---------|
| OBS Studio | Screen recording |
| DaVinci Resolve | Video editing |
| Audacity | Audio recording |
| Canva | Thumbnail design |

### Settings

**Recording:**
- Resolution: 1920x1080
- Frame rate: 30 fps
- Format: MP4 (H.264)

**Audio:**
- Sample rate: 48 kHz
- Bitrate: 192 kbps
- Format: AAC

---

## 📋 Video Description (for YouTube/ClawHub)

```markdown
🚀 App Maker - Build Full-Stack Apps in Minutes with AI

Transform natural language requirements into production-ready applications 
automatically. No coding required.

⏱️ Timestamps:
0:00 - Introduction
1:30 - Setup & Configuration
3:00 - Live Demo: Generating an App
8:00 - Visual Debugging Interface
12:00 - One-Click Deployment
14:00 - Wrap-up

🔗 Links:
- GitHub: https://github.com/openclaw/clawhub
- Documentation: https://clawhub.ai/skills/app-maker
- Quick Start: https://clawhub.ai/skills/app-maker/QUICKSTART.md
- Discord: https://discord.gg/openclaw

📦 Installation:
npx skills add app-maker

🤖 Supported AI Models:
- Claude Code (Anthropic)
- Qwen (Alibaba Cloud)
- Gemini (Google)
- GLM (Zhipu AI)

🛠️ Tech Stack Support:
Frontend: React, Vue, Flutter
Backend: Node.js, Python, Go
Database: PostgreSQL, MongoDB, MySQL
Deploy: Vercel, Alibaba Cloud, Docker

#AppDevelopment #AI #LowCode #FullStack #WebDevelopment #NoCode #Productivity
```

---

## 🎨 Thumbnail Design

### Text Overlay
```
BUILD APPS
IN MINUTES
(with AI)
```

### Visual Elements
- App Maker logo (top right)
- Code/app split screen background
- Bright accent colors (blue/orange)
- 1280x720 pixels

---

## ✅ Pre-Upload Checklist

- [ ] Video recorded in 1080p
- [ ] Audio quality checked (no background noise)
- [ ] All timestamps accurate
- [ ] Thumbnail designed and exported
- [ ] Description written with links
- [ ] Tags added for SEO
- [ ] Captions/subtitles generated
- [ ] Video exported and compressed

---

*Video production guide last updated: 2026-03-16*

# App Maker - ClawHub Upload Guide

Complete guide for uploading App Maker to ClawHub.

---

## 📦 Upload Package Contents

### Required Files

```
app-maker/
├── SKILL.md                    # ✅ Main skill documentation
├── README.md                   # ✅ Public README for ClawHub
├── QUICKSTART.md               # ✅ Quick start guide
├── SCREENSHOTS.md              # ✅ Screenshot guide
├── DEMO_VIDEO.md               # ✅ Video script & description
├── UPLOAD.md                   # ✅ This file
├── package.json                # ✅ Package metadata
├── _meta.json                  # ✅ Skill metadata
├── config.example.json         # ✅ Configuration template
├── LICENSE                     # ⬜ Add MIT license
├── .clawhub/
│   └── origin.json             # ✅ Origin metadata
├── scripts/
│   ├── app_builder.py          # ✅ Core script
│   └── package_for_upload.py   # ✅ Packaging script
├── screenshots/                # ⬜ Add actual screenshots
│   ├── workflow.png
│   ├── debug-interface.png
│   ├── project-structure.png
│   ├── model-config.png
│   ├── cli-usage.png
│   └── app-preview.png
└── tests/                      # ⬜ Optional tests
    └── test_builder.py
```

---

## 🚀 Upload Methods

### Method 1: Via Skills CLI (Recommended)

```bash
# Navigate to skills directory
cd C:\Users\52304\.openclaw\workspace\skills

# Publish to ClawHub
npx skills publish app-maker

# Or with explicit options
npx skills publish app-maker \
  --name "app-maker" \
  --display-name "App Maker" \
  --description "Full-stack app development with AI-powered code generation" \
  --category "development" \
  --tags "app-development,full-stack,code-generation,ai-assistant,react,nodejs" \
  --version "1.0.0" \
  --license "MIT" \
  --author "OpenClaw Workspace" \
  --verbose
```

### Method 2: Via ClawHub Web Interface

1. Go to https://clawhub.ai/skills/create
2. Fill in the form:
   - **Name:** `app-maker`
   - **Display Name:** `App Maker`
   - **Description:** (see below)
   - **Category:** `Development`
   - **Tags:** (see below)
   - **Version:** `1.0.0`
   - **License:** `MIT`
3. Upload files (zip the `app-maker` folder)
4. Submit for review

### Method 3: Via Git

```bash
# Clone ClawHub repo
git clone https://github.com/openclaw/clawhub.git
cd clawhub

# Copy skill to skills directory
cp -r ../workspace/skills/app-maker skills/

# Add and commit
git add skills/app-maker
git commit -m "Add app-maker skill: Full-stack AI app development"

# Push and create PR
git push origin main
# Then create PR on GitHub
```

---

## 📝 Upload Form Fields

### Basic Information

| Field | Value |
|-------|-------|
| **Name** | `app-maker` |
| **Display Name** | `App Maker` |
| **Short Description** | Full-stack app development skill that automates the complete workflow from UI design, database schema, code generation to deployment. Supports multi-model AI (Claude Code, Qwen, Gemini, GLM) with visual debugging. |
| **Category** | `Development` |
| **Version** | `1.0.0` |
| **License** | `MIT` |
| **Author** | `OpenClaw Workspace` |

### Tags (comma-separated)

```
app-development,full-stack,code-generation,ai-assistant,react,nodejs,database-design,deployment,claude,multi-model,visual-debugging,mvp,rapid-prototyping
```

### Long Description

```markdown
App Maker is a comprehensive full-stack application development skill that automates the entire software development lifecycle. It transforms natural language requirements into production-ready applications through a structured 6-phase workflow:

1. **Requirements Analysis** - Generates PRD, user stories, and feature prioritization
2. **UI/UX Design** - Creates component trees, wireframes, and design systems
3. **Database Design** - Produces Prisma/SQL schemas with ER diagrams
4. **Code Generation** - Generates frontend (React/Vue/Flutter) and backend (Node.js/Python/Go) code
5. **Visual Debugging** - Provides live preview with component inspection and state debugging
6. **Deployment** - One-click deploy to Vercel, Alibaba Cloud, or Docker

**Key Features:**
- Multi-model AI support with automatic fallback (Claude Code → Qwen → Gemini → GLM)
- Technology stack customization (frontend, backend, database, deployment target)
- Visual debugging interface with hot reload
- Plugin system for extensibility
- Production-ready code with tests and CI/CD configuration

**Supported Stacks:**
- Frontend: React, Vue, Flutter
- Backend: Node.js, Python, Go
- Database: PostgreSQL, MongoDB, MySQL
- Deploy: Vercel, Alibaba Cloud, Docker, Kubernetes

Perfect for rapid prototyping, MVP development, and automating repetitive coding tasks.
```

### Requirements

```yaml
Python:
  - httpx>=0.24.0

Node.js:
  - npm>=8.0.0

Environment Variables (optional):
  - CLAUDE_API_KEY
  - QWEN_API_KEY
  - GEMINI_API_KEY
  - GLM_API_KEY
```

### Links

| Link Type | URL |
|-----------|-----|
| **Homepage** | https://clawhub.ai/skills/app-maker |
| **Documentation** | https://github.com/openclaw/clawhub/tree/main/skills/app-maker |
| **Bug Tracker** | https://github.com/openclaw/clawhub/issues |
| **Discord** | https://discord.gg/openclaw |

---

## 📸 Screenshots Upload

### Required Screenshots

1. **workflow.png** - Workflow diagram (1200x800)
2. **debug-interface.png** - Visual debug UI (1920x1080)
3. **project-structure.png** - Generated folder structure (1200x900)
4. **model-config.png** - Configuration example (1400x800)
5. **cli-usage.png** - Terminal output (1600x900)
6. **app-preview.png** - Generated app preview (1920x1080)

### How to Add Screenshots

```bash
# Create screenshots directory
mkdir -p app-maker/screenshots

# Add your screenshots here
# See SCREENSHOTS.md for detailed guide

# Optimize images (optional)
python scripts/optimize_images.py app-maker/screenshots/
```

---

## 🎥 Demo Video Upload

### YouTube Upload

1. Go to https://youtube.com/upload
2. Upload video file (MP4, 1080p)
3. Fill in details:
   - **Title:** `App Maker - Build Full-Stack Apps in Minutes with AI`
   - **Description:** (see DEMO_VIDEO.md)
   - **Thumbnail:** Upload custom thumbnail
   - **Tags:** `app-development,ai,low-code,full-stack,web-development`
4. Set visibility to "Public" or "Unlisted"
5. Copy YouTube URL
6. Add URL to ClawHub submission

### Alternative: Loom Video

1. Record at https://loom.com
2. Share link in ClawHub submission
3. No upload size limits

---

## ✅ Pre-Upload Checklist

### Files

- [ ] SKILL.md complete and accurate
- [ ] README.md with all sections
- [ ] QUICKSTART.md tested and working
- [ ] package.json with correct metadata
- [ ] _meta.json matches package.json
- [ ] LICENSE file added (MIT)
- [ ] .clawhub/origin.json present
- [ ] All scripts tested

### Testing

- [ ] Skill installs without errors
- [ ] `app_builder.py` runs successfully
- [ ] Generated apps work correctly
- [ ] All model integrations tested
- [ ] Deployment flow tested

### Documentation

- [ ] Screenshots captured and optimized
- [ ] Demo video recorded and uploaded
- [ ] All links working
- [ ] Code examples tested
- [ ] API key setup documented

### Metadata

- [ ] Name unique and descriptive
- [ ] Tags relevant and comprehensive
- [ ] Category correct
- [ ] Version follows semver
- [ ] License specified

---

## 🔍 After Upload

### Review Process

1. **Automated Checks** (5-10 minutes)
   - File structure validation
   - Metadata verification
   - Security scan

2. **Manual Review** (24-48 hours)
   - Documentation quality
   - Code quality check
   - Functionality verification

3. **Publication**
   - Skill appears on ClawHub
   - Searchable in skills directory
   - Available for installation

### Post-Publication

```bash
# Verify installation works
npx skills add app-maker
npx skills info app-maker

# Monitor downloads
npx skills stats app-maker

# Respond to issues
# Check GitHub issues regularly
```

---

## 📞 Support

If you encounter issues during upload:

- **Documentation:** https://docs.clawhub.ai/publishing
- **Discord:** https://discord.gg/clawhub-publishing
- **Email:** support@clawhub.ai

---

*Upload guide last updated: 2026-03-16*

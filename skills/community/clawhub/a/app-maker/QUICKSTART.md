# App Maker - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
# Python dependencies
pip install httpx openpyxl

# Node.js dependencies (for generated projects)
npm install -g vercel
```

### 2. Configure Model API Keys

Create config file `~/.config/app-maker/models.json`:

```bash
mkdir -p ~/.config/app-maker
cp skills/app-maker/config.example.json ~/.config/app-maker/models.json
```

Edit the file and add your API Keys:

```json
{
  "default": "claude-code",
  "models": {
    "claude-code": {
      "apiKey": "sk-ant-your-actual-key-here"
    },
    "qwen": {
      "apiKey": "sk-your-actual-key-here"
    }
  }
}
```

**Get API Keys:**
- **Claude**: https://console.anthropic.com
- **Qwen**: https://dashscope.console.aliyun.com
- **Gemini**: https://makersuite.google.com
- **GLM**: https://open.bigmodel.cn

### 3. Generate Your First App

```bash
# Go to workspace
cd C:\Users\52304\.openclaw\workspace

# Run generator
python skills/app-maker/scripts/app_builder.py generate --output my-first-app
```

Enter app description, for example:
```
Create a task management app with user login, project creation, Kanban board, and team collaboration
```

### 4. Preview and Debug

```bash
# Enter generated project
cd my-first-app

# Install dependencies
npm install

# Start dev server
npm run dev
```

Open browser to `http://localhost:3000`

### 5. Deploy

```bash
# Deploy to Vercel
npx vercel --prod

# Or deploy to Alibaba Cloud
# See docs/deploy_guide.md
```

---

## 📋 Complete Command Reference

### Initialize Project

```bash
python scripts/app_builder.py init my-app
```

### Generate App

```bash
# Interactive
python scripts/app_builder.py generate --output my-app

# Direct description
python scripts/app_builder.py generate -o my-app -d "Create a blog system"

# From PRD file
python scripts/app_builder.py generate -o my-app --from docs/prd.md
```

### Preview

```bash
python scripts/app_builder.py preview --output my-app
```

### Deploy

```bash
# Deploy to Vercel
python scripts/app_builder.py deploy --output my-app --target vercel

# Deploy to Alibaba Cloud
python scripts/app_builder.py deploy --output my-app --target aliyun

# Deploy to Docker
python scripts/app_builder.py deploy --output my-app --target docker
```

---

## 🛠️ Custom Configuration

### Create `.apprc` Config File

Create `.apprc` in project root:

```json
{
  "framework": "react",
  "backend": "nodejs",
  "database": "postgresql",
  "styling": "tailwind",
  "stateManagement": "zustand",
  "testing": {
    "unit": "jest",
    "e2e": "playwright"
  }
}
```

### Switch Models

```bash
# Temporarily use different model
python scripts/app_builder.py generate -d "..." --model qwen

# Or modify default in config file
```

---

## 📁 Generated Project Structure

```
my-app/
├── docs/                    # Documentation
│   ├── prd.md              # Product Requirements Document
│   └── deploy_guide.md     # Deployment Guide
├── design/                  # Design Files
│   └── components.json     # Component Tree
├── database/                # Database
│   └── schema.prisma       # Prisma Schema
├── src/
│   ├── frontend/           # Frontend Code
│   └── backend/            # Backend Code
├── tests/                   # Test Files
├── infra/                   # Infrastructure Config
├── package.json
└── README.md
```

---

## ❓ FAQ

### Q: Can I use without API Keys?

Yes! The script uses mock responses to generate basic project structure, but code content needs manual completion.

### Q: How to customize generated code style?

Create `.apprc` file in project root with code style options.

### Q: What tech stacks are supported?

**Frontend**: React, Vue, Flutter  
**Backend**: Node.js, Python, Go  
**Database**: PostgreSQL, MongoDB, MySQL  
**Deploy**: Vercel, Alibaba Cloud, Docker

### Q: How to contribute plugins?

See example in `skills/app-maker/plugins/` directory to create your plugin.

---

## 📚 More Resources

- [Full Documentation](SKILL.md)
- [Config Example](config.example.json)
- [Issue Tracker](../../../issues)

---

*Happy Coding! 🎉*

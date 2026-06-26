# App Maker - Screenshot Guide

This document describes screenshots for ClawHub upload. Replace placeholder images with actual screenshots from your usage.

---

## 📸 Required Screenshots

### 1. Workflow Diagram (`screenshots/workflow.png`)

**Description:** Visual representation of the 6-phase development workflow

**What to capture:**
- Complete flowchart from Requirements → Deploy
- Show all 6 phases with arrows
- Include time estimates for each phase

**Recommended size:** 1200x800 pixels

**How to create:**
```bash
# Generate workflow diagram
python scripts/generate_diagram.py --output screenshots/workflow.png
```

---

### 2. Debug Interface (`screenshots/debug-interface.png`)

**Description:** Visual debugging interface with live preview

**What to capture:**
1. Browser window showing generated app preview
2. Left panel: Component tree
3. Right panel: Property inspector
4. Bottom panel: Console logs and network requests

**Recommended size:** 1920x1080 pixels

**How to capture:**
```bash
# Start preview server
python scripts/app_builder.py preview -o demo-app

# Open browser and navigate to http://localhost:3000
# Take screenshot of full debug interface
```

---

### 3. Project Structure (`screenshots/project-structure.png`)

**Description:** Generated project folder structure in file explorer

**What to capture:**
- Full directory tree showing:
  - `docs/` (PRD, user stories)
  - `design/` (components, wireframes)
  - `database/` (schema, migrations)
  - `src/frontend/` (components, pages)
  - `src/backend/` (controllers, routes)
  - `tests/` (unit, integration, e2e)
  - `infra/` (docker, k8s)

**Recommended size:** 1200x900 pixels

**How to capture:**
```bash
# Generate demo project
python scripts/app_builder.py generate -o demo-app -d "Task management app"

# Open file explorer at demo-app folder
# Take screenshot showing full folder structure
```

---

### 4. Model Configuration (`screenshots/model-config.png`)

**Description:** Model configuration file and setup process

**What to capture:**
- Code editor showing `~/.config/app-maker/models.json`
- Highlight API key configuration section
- Show multiple model entries (Claude, Qwen, Gemini, GLM)

**Recommended size:** 1400x800 pixels

**How to capture:**
```bash
# Open config file in VS Code
code ~/.config/app-maker/models.json

# Take screenshot showing JSON configuration
```

---

### 5. CLI Usage (`screenshots/cli-usage.png`)

**Description:** Terminal showing command-line interface in action

**What to capture:**
- Terminal window with colorful output
- Show generation progress bars
- Include success message with project path

**Recommended size:** 1600x900 pixels

**How to capture:**
```bash
# Run generation command
python scripts/app_builder.py generate -o demo-app -d "E-commerce app"

# Capture terminal output during generation
```

---

### 6. Generated App Preview (`screenshots/app-preview.png`)

**Description:** Screenshot of a fully generated and running application

**What to capture:**
- Browser showing generated app
- Show multiple pages/components if possible
- Include some sample data

**Recommended size:** 1920x1080 pixels

**How to capture:**
```bash
# Generate and run demo app
python scripts/app_builder.py generate -o demo-app -d "Task management app"
cd demo-app && npm install && npm run dev

# Open browser and navigate to http://localhost:3000
# Take screenshot of running app
```

---

## 📹 Demo Video Screenshots

### Thumbnail (`screenshots/video-thumbnail.png`)

**Description:** YouTube video thumbnail

**Requirements:**
- Size: 1280x720 pixels (16:9 aspect ratio)
- Include App Maker logo
- Add text overlay: "Full-Stack App Development in Minutes"
- Use high contrast colors

---

## 🎨 Screenshot Style Guide

### Consistency
- Use same theme across all screenshots
- Recommended: Dark mode for code editors, light mode for apps
- Consistent window sizes and positioning

### Annotations
- Add numbered callouts for key features
- Use arrows to highlight important elements
- Keep text minimal and readable

### Quality
- Use PNG format for lossless quality
- Minimum 1200px width
- Ensure text is crisp and readable

---

## 📦 Creating Screenshots Folder

```bash
# Create screenshots directory
mkdir -p screenshots

# Generate all screenshots
python scripts/capture_screenshots.py --all

# Optimize images
python scripts/optimize_images.py screenshots/
```

---

## ✅ Checklist

Before uploading to ClawHub:

- [ ] All 6 screenshots captured
- [ ] Images optimized (under 500KB each)
- [ ] Text readable at thumbnail size
- [ ] Consistent style across all images
- [ ] Video thumbnail created
- [ ] Screenshots added to README.md
- [ ] Image files committed to git

---

*Last updated: 2026-03-16*

---
name: AB-Agents-Vision
description: "👁️ Image analysis using MiniMax VL API. Describe images, extract text from screenshots, analyze photos. Works with local files and URLs. Simple shell wrapper."
version: 1.0.0
author: AB-Agents
homepage: https://github.com/alexburrstudio/ab-agents-skills
license: MIT
tags: ["vision", "image", "minimax", "ocr", "analysis", "ab-agents", "screenshot", "text-extraction"]
acceptLicenseTerms: true
---

# AB Agents Vision 👁️

Image analysis using MiniMax VL API — simple, fast, reliable.

## What It Does

- 📸 **Describe images** — Get detailed scene descriptions
- 📝 **Extract text** — Read text from screenshots, photos, documents
- 🔍 **Analyze photos** — Identify objects, people, settings
- 🌐 **URL support** — Analyze images from the web

## Quick Start

```bash
# Install
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set your MiniMax API key
export MINIMAX_API_KEY="sk-cp-your-key"

# Use
./vision.sh image.jpg "Describe this image"
```

## Usage

```bash
# Basic description
./vision.sh photo.jpg

# With custom prompt
./vision.sh screenshot.png "What text do you see?"

# URL support
./vision.sh "https://example.com/image.jpg" "Describe this"
```

## Requirements

- MiniMax Token Plan API key ([get one](https://platform.minimax.io))
- Linux/macOS
- `uvx` (auto-installed via script)

## Examples

**Screenshot analysis:**
```
Input: screenshot.png + "What text is in the image?"
Output: "The screenshot shows a code editor with Python code...
```

**Photo description:**
```
Input: photo.jpg + "Describe in detail"
Output: "A person's bare foot and lower leg resting on a brown
textured waffle-weave blanket. The skin is light-toned with
visible fine hairs..."
```

## Installation

```bash
git clone https://github.com/alexburrstudio/ab-agents-skills.git
cd ab-agents-skills/skills/vision
chmod +x vision.sh
```

Or via ClaWHub:
```bash
clawhub install AB-Agents-Vision
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| API Error: 1033 | Retry — system error on MiniMax side |
| No response | Check MINIMAX_API_KEY is set correctly |
| Slow | Use smaller images (<10MB) |

---

**AB-Agents** 🦀

# 🎨 Doubao Seedream & Seedance API Skill

> **Professional AI Generation Suite** - Powered by Doubao Seed Models

A comprehensive AI generation skill featuring **Doubao Seedream** for image generation, **Doubao Seedance** for video creation, and **Doubao Seed Vision** for visual understanding.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Core Features

### 🎨 Doubao Seedream 4.0 - Image Generation

**State-of-the-art text-to-image generation with exceptional quality and control.**

| Feature | Description |
|---------|-------------|
| **Text-to-Image** | Generate stunning images from natural language descriptions |
| **Image Editing** | Modify existing images with AI-powered editing tools |
| **Image-to-Image** | Transform and reimagine existing images |
| **Multi-Size Support** | Flexible dimensions (512-2048px), optimized for 64px multiples |
| **Style Control** | Artistic styles, photorealistic, and custom aesthetics |

**Model ID**: `doubao-seedream-4-0-250828`

```
Generate an image: sunset beach with palm trees and golden waves, photorealistic style
```

---

### 🎬 Doubao Seedance 1.5 - Video Generation

**Professional video creation with advanced camera control and motion dynamics.**

| Feature | Description |
|---------|-------------|
| **Text-to-Video** | Create videos from text descriptions with cinematic quality |
| **Image-to-Video** | Animate static images with natural motion |
| **Camera Control** | Pan, zoom, dolly, and complex camera movements |
| **Frame Control** | Define start/end frames for precise transitions |
| **Duration Control** | 1-10 second videos with smooth motion interpolation |

**Model ID**: `doubao-seedance-1-5-pro-251215`

```
Generate a 5-second video: camera slowly pulls out revealing mountain vista at dawn
```

---

### 👁️ Doubao Seed Vision - Visual Understanding

**Advanced image analysis and comprehension powered by multimodal AI.**

| Feature | Description |
|---------|-------------|
| **Content Analysis** | Comprehensive image understanding and description |
| **Object Detection** | Identify and locate objects within images |
| **Scene Understanding** | Contextual analysis of environments and settings |
| **Visual Q&A** | Answer questions about image content |

**Model ID**: `doubao-seed-1-6-vision-250815`

```
Analyze this image: https://example.com/photo.jpg - describe the scene and identify objects
```

---

## 📊 Model Comparison

| Model | Type | Capabilities | Best For |
|-------|------|--------------|----------|
| **Seedream 4.0** | Image | Text-to-Image, Edit, Transform | Marketing, Design, Art |
| **Seedance 1.5** | Video | Text-to-Video, Animate, Motion | Content Creation, Animation |
| **Seed Vision** | Vision | Analysis, Detection, Q&A | Automation, Research, Apps |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Volcengine API Key ([Get it here](https://console.volcengine.com/ark))
- pip or Docker

### Installation (Choose One)

#### Option 1: One-Click Install ⚡ (Recommended)

```bash
# Clone and install
git clone https://github.com/Lychee-AI-Team/seedream-skill.git
cd seedream-skill
./install.sh
```

#### Option 2: Docker 🐳

```bash
# Clone
git clone https://github.com/Lychee-AI-Team/seedream-skill.git
cd seedream-skill

# Configure
echo "ARK_API_KEY=your-api-key" > .env

# Run
docker compose up --build
```

#### Option 3: Manual 🛠️

```bash
# Clone
git clone https://github.com/Lychee-AI-Team/seedream-skill.git
cd seedream-skill

# Install dependencies
pip install -r volcengine-api/requirements.txt

# Configure
export ARK_API_KEY="your-api-key"
```

### Configuration

```bash
# Method 1: Environment Variable (Recommended ✅ Most Secure)
export ARK_API_KEY="your-api-key-here"

# Method 2: Interactive Wizard
./scripts/configure.sh

# Method 3: Config File
mkdir -p ~/.volcengine
echo 'api_key: "your-api-key"' > ~/.volcengine/config.yaml
chmod 600 ~/.volcengine/config.yaml  # Important!
```

### Verify Installation

```bash
./scripts/verify_install.sh
```

---

## 📖 Usage Guide

### 🎨 Image Generation

**Basic Usage:**
```
Generate an image: sunset beach with palm trees
```

**Advanced Usage:**
```
Generate image with parameters:
- Content: futuristic city skyline at night
- Size: 1920x1080
- Style: cyberpunk aesthetic
- Negative prompt: blurry, low quality
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| prompt | string | - | Image description (required) |
| width | int | 1024 | Width in pixels (64px multiples) |
| height | int | 1024 | Height in pixels (64px multiples) |
| negative_prompt | string | - | Elements to avoid |
| model | string | doubao-seedream-4-0-250828 | Model ID |

---

### 🎬 Video Generation

**Basic Usage:**
```
Generate a 5-second video: ocean waves crashing on rocks
```

**Advanced Usage:**
```
Generate video with parameters:
- Content: drone shot of forest canopy
- Duration: 8 seconds
- Motion: slow vertical ascent
- Aspect ratio: 16:9
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| prompt | string | - | Video description (required) |
| duration | float | 5.0 | Duration in seconds (1-10) |
| aspect_ratio | string | "16:9" | Aspect ratio (16:9, 9:16, 1:1) |
| model | string | doubao-seedance-1-5-pro-251215 | Model ID |

---

### 👁️ Vision Understanding

**Basic Usage:**
```
Analyze this image: https://example.com/image.jpg
```

**Advanced Usage:**
```
Analyze image with focus on:
- Identify all objects present
- Describe the scene composition
- Detect any text in the image
- Suggest improvements for photography
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| image | string | - | Image URL or local path (required) |
| prompt | string | - | Analysis instructions |
| model | string | doubao-seed-1-6-vision-250815 | Model ID |

---

### 📋 Task Management

**View Tasks:**
```
Show my task list
List all pending tasks
```

**Check Status:**
```
Check status of task-123
What's the progress of my video generation?
```

**Download Results:**
```
Download result of task-123
Save the generated image to output folder
```

---

## 🔒 Security Best Practices

> ⚠️ **Important**: API Keys are sensitive credentials. Follow these security practices.

### ✅ Recommended Methods

| Method | Security | Use Case |
|--------|----------|----------|
| Environment Variables | ⭐⭐⭐⭐⭐ | **Recommended** - All scenarios |
| Secret Management | ⭐⭐⭐⭐⭐ | Production environments |
| Config File (600 permissions) | ⭐⭐⭐ | Local development |

### 🔑 Environment Variable Setup

```bash
# Temporary (current session)
export ARK_API_KEY="your-api-key"

# Permanent (add to shell config)
echo 'export ARK_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc

# Verify (should show first 4 characters)
echo $ARK_API_KEY | head -c 4
```

### 🔐 Config File Security

```bash
# Create config
mkdir -p ~/.volcengine
cat > ~/.volcengine/config.yaml << 'EOF'
api_key: "your-api-key"
base_url: "https://ark.cn-beijing.volces.com/api/v3"
EOF

# Set permissions (CRITICAL!)
chmod 700 ~/.volcengine
chmod 600 ~/.volcengine/config.yaml
```

### ❌ Prohibited Actions

| Don't Do This | Why? |
|---------------|------|
| ❌ Commit API Key to Git | Publicly accessible |
| ❌ Log API Key | May leak in logs |
| ❌ Pass in URL | Gets logged |
| ❌ Hardcode in code | Hard to rotate |
| ❌ Share with others | No accountability |

### 🔄 Key Rotation

```bash
# Rotate every 90 days (recommended)
# 1. Generate new key in Volcengine console
# 2. Update environment/config
# 3. Verify new key works
# 4. Delete old key
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ARK_API_KEY` | API key (**Required**) | - |
| `VOLCENGINE_BASE_URL` | API endpoint | `https://ark.cn-beijing.volces.com/api/v3` |
| `VOLCENGINE_TIMEOUT` | Request timeout (s) | 30 |
| `VOLCENGINE_MAX_RETRIES` | Max retries | 3 |
| `VOLCENGINE_OUTPUT_DIR` | Output directory | `./output` |

### Configuration File

**Location**: `~/.volcengine/config.yaml`

```yaml
# api_key: "your-api-key"  # Recommended: use environment variable
base_url: "https://ark.cn-beijing.volces.com/api/v3"
timeout: 30
max_retries: 3
output_dir: "./output"
```

### Priority Order

1. Environment variable `ARK_API_KEY` ⭐ **Recommended**
2. Project config `.volcengine/config.yaml`
3. Global config `~/.volcengine/config.yaml`
4. Default values

---

## 💾 Data Persistence

| Path | Content | Sensitivity |
|------|---------|-------------|
| `~/.volcengine/config.yaml` | Global config | ⚠️ May contain API Key |
| `~/.volcengine/tasks/` | Task history | Normal |
| `~/.volcengine/state/` | State files | Normal |
| `./.volcengine/config.yaml` | Project config | ⚠️ May contain API Key |

**Security Tips:**
- Set config file permissions to 600
- Add `.volcengine/` to `.gitignore`
- Clean up old history regularly

---

## ❌ Error Handling

| Error | Description | Solution |
|-------|-------------|----------|
| Authentication | Invalid API Key | Check `ARK_API_KEY` |
| Rate Limit | Too many requests | Wait and retry |
| Network | Connection failed | Check internet |
| Parameter | Invalid input | Check format |
| Model | Model unavailable | Verify model ID |

---

## 📝 Example Workflows

### 🎨 Complete Image Generation Flow

```
1. Set API Key
   → export ARK_API_KEY="sk-xxx"

2. Generate Image
   → Generate an image: serene mountain lake at sunrise

3. Check Status
   → Check task status

4. Download Result
   → Download image to ./output/
```

### 🎬 Image-to-Video Pipeline

```
1. Generate Source Image
   → Generate an image: ancient temple in misty forest

2. Animate to Video
   → Generate video from image with slow camera push in

3. Monitor Progress
   → Check video generation status

4. Export Video
   → Download completed video
```

---

## 🐳 Deployment

| Method | Time | Best For |
|--------|------|----------|
| Script Install | 2-3 min | Development, Testing |
| Docker | 3-5 min | Production, Teams |
| Manual | 5-10 min | Custom setups |

📖 **Detailed Guide**: [INSTALLATION.md](./docs/INSTALLATION.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Quick Start](./docs/QUICKSTART.md) | 30-second setup guide |
| [Installation](./docs/INSTALLATION.md) | Detailed installation |
| [Examples](./docs/examples.md) | Code examples |
| [Troubleshooting](./docs/troubleshooting.md) | Common issues |
| [README](./README.md) | Full documentation |

---

## 🆘 Get Help

```bash
# View help
./scripts/help.sh

# Verify installation
./scripts/verify_install.sh
```

**Need more help?** Say "help" or "帮助" for interactive assistance.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📞 Support

- 🐛 [Issue Tracker](https://github.com/Lychee-AI-Team/seedream-skill/issues)
- 💬 [Discussions](https://github.com/Lychee-AI-Team/seedream-skill/discussions)

---

<div align="center">

**Built with ❤️ for AI Generation**

**Powered by Doubao Seed Models**

*Seedream • Seedance • Seed Vision*

</div>

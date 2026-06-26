<p align="center"><a href="https://302.ai/" target="blank"><img src="banner.png" /></a></p >

<h1 align="center">
<span>
    302.AI API-Integration-Skill
</span>
</h1>

> 🚀 **Instantly integrate 1400+ AI APIs into your code** - The ultimate Claude Code skill for seamless 302.AI API integration

[中文文档](./README_CN.md) | English

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blue.svg)](https://claude.com/claude-code)
[![APIs](https://img.shields.io/badge/APIs-1400%2B-green.svg)](https://doc.302.ai/)

## ✨ What is This?

A powerful Claude Code skill that **automatically** searches through 302.AI's massive collection of 1400+ AI APIs and generates ready-to-use integration code in your preferred programming language. No more manual documentation hunting or boilerplate writing!

## 🎯 Key Features

- 🔍 **Smart API Discovery** - Automatically searches 1400+ APIs across 9 major categories
- 💻 **Multi-Language Support** - Generates code in Python, JavaScript, TypeScript, Go, and more
- 🔄 **Always Up-to-Date** - Fetches the latest API list in real-time
- 🎨 **Zero Context Waste** - Efficient script-based search reduces token usage
- 🛡️ **Security First** - Built-in warnings for API key protection
- ⚡ **Lightning Fast** - Bash-optimized search for instant results

## 📦 What's Included?

### API Categories Covered

| Category | Examples | Coverage |
|----------|----------|----------|
| 🤖 **Language Models** | GPT, Claude, Gemini, Chinese models | 30% |
| 🎨 **Image Generation** | Nano-Banana, Midjourney, Stable Diffusion, Flux | 25% |
| 🎬 **Video Generation** | Runway, Pika, Luma AI, Kling | 20% |
| 🎵 **Audio Processing** | TTS, STT, Music Generation | 10% |
| 📄 **Document Processing** | OCR, PDF, Web Scraping | 10% |
| 🧠 **RAG & Embeddings** | Vector Search, Rerank | 3% |
| 🛠️ **Tools & Utilities** | Creative, Writing, Professional | 2% |

## 🚀 Quick Start

### Installation

Simply share this GitHub URL with Claude Code:

```
Install this skill: https://github.com/302ai/302AI-API-Integration-Skill
```

Claude Code will automatically install the skill for you!

### Verify Installation

Check if the skill is loaded:

```
What skills are available?
```

You should see `302ai-api-integration` in the list.

### Basic Usage

Simply ask Claude Code naturally:

```
"I need to use GPT-4 in my Python project"
"How do I generate images with DALL-E in Node.js?"
"Integrate speech-to-text API"
```

The skill will:
1. ✅ Ask for your 302.AI API Key
2. ✅ Search the latest API list
3. ✅ Show you matching APIs
4. ✅ Generate complete integration code
5. ✅ Provide usage examples and best practices

## 💡 Usage Examples

### Example 1: Integrate GPT-4 Chat

**You**: "I want to use GPT-4 in my Python project"

**Claude Code** (with this skill):
```python
import requests
import json

API_KEY = "your_api_key_here"
BASE_URL = "https://api.302.ai"

def call_gpt4(prompt):
    response = requests.post(
        f"{BASE_URL}/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return response.json()

# Usage
result = call_gpt4("Hello, GPT-4!")
print(result)
```

### Example 2: Image Generation

**You**: "Generate images with Stable Diffusion in JavaScript"

**Claude Code** generates complete Node.js code with:
- ✅ API endpoint configuration
- ✅ Image generation function
- ✅ Error handling
- ✅ File saving logic

### Example 3: Video Generation

**You**: "I need to create videos from text"

**Claude Code**:
1. Searches video generation APIs (Runway, Pika, Luma AI, etc.)
2. Shows you options with descriptions
3. Generates integration code after you select
4. Includes async handling for long-running tasks

## 🛠️ Advanced Features

### Bash Command Search

The skill includes a powerful Python script for direct API search:

```bash
# Search by keyword
python3 scripts/parse_api_list.py "GPT"

# Search by category
python3 scripts/parse_api_list.py "image generation"

# Combined search
python3 scripts/parse_api_list.py "chat" "language model"
```

### Python Module Usage

```python
from scripts.parse_api_list import fetch_llms_txt, parse_llms_txt, search_apis

# Auto-fetch latest API list
content = fetch_llms_txt()
apis = parse_llms_txt(content)

# Search APIs
results = search_apis(apis, keyword='GPT', category='Language Models')

# Display results
for api in results:
    print(f"{api['name']}: {api['link']}")
```

## 📚 Documentation Structure

```
302ai-api-integration/
├── SKILL.md                          # Main skill instructions
├── scripts/
│   └── parse_api_list.py            # API search script (auto-fetch)
├── references/
│   ├── api_categories.md            # Complete API category index
│   ├── integration_examples.md      # Code templates for all languages
│   └── parse_script_usage.md        # Script usage guide
└── assets/                          # (Reserved for future use)
```

## 🔒 Security Best Practices

The skill automatically warns you about:

- ⚠️ **Frontend API Key Exposure** - Never use API keys in pure frontend code
- ✅ **Recommended Solution** - Use backend frameworks (Next.js, Express, Flask)
- 🔐 **Environment Variables** - Store keys securely
- 🚫 **Version Control** - Never commit API keys

## 🎨 Supported Languages

- 🐍 **Python** - Complete with async support
- 📜 **JavaScript/Node.js** - Modern ES6+ syntax
- 📘 **TypeScript** - Full type definitions
- 🔷 **Go** - Idiomatic Go code
- 🔧 **cURL** - Ready-to-use commands
- ➕ **More** - Request any language!

## 🌟 Why Use This Skill?

### Before (Manual Integration)
```
1. Search 302.AI documentation
2. Find the right API
3. Read through docs
4. Copy endpoint URLs
5. Write boilerplate code
6. Debug authentication
7. Handle errors manually
⏱️ Time: 30-60 minutes
```

### After (With This Skill)
```
1. Ask Claude Code naturally
2. Get complete working code
⏱️ Time: 2-3 minutes
```

## 📊 Performance

- **Search Speed**: < 2 seconds for 1400+ APIs
- **Context Usage**: Minimal (script-based search)
- **Code Quality**: Production-ready with error handling
- **Accuracy**: Always uses latest API documentation

## 🤝 Contributing

Found a bug or have a suggestion? We'd love to hear from you!

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 🔗 Links

- [302.AI Official Website](https://302.ai/)
- [302.AI API Documentation](https://doc.302.ai/)
- [Claude Code](https://claude.com/claude-code)

## 💬 Support

- 📧 Email: support@302.ai
- 💬 Discord: [Join our community](#)
- 📖 Docs: [Full documentation](https://doc.302.ai/)

## 🎉 Acknowledgments

- Built for [Claude Code](https://claude.com/claude-code)
- Powered by [302.AI](https://302.ai/)'s comprehensive API platform
- Inspired by the developer community's need for faster API integration

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ for developers who value their time

[Get Started](#-quick-start) • [View Examples](#-usage-examples) • [Read Docs](#-documentation-structure)

</div>


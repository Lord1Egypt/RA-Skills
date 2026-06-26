# 🎬 bilibit - Bilibili Video Downloader

> Simple and fast Bilibili video downloader. Just paste the URL!

[![npm version](https://img.shields.io/npm/v/bilibit.svg)](https://www.npmjs.com/package/bilibit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[🇨🇳 中文文档](README_CN.md)**

---

## ✨ Features

- 🎯 **URL Download** - Paste URL, download video
- 🎬 **Danmaku Support** - Download with danmaku
- 🚀 **Fast & Simple** - One command to get started
- 📦 **Auto Install** - BBDown auto-installs
- 📋 **History** - View download history

---

## 📦 Installation

```bash
npm install -g bilibit
```

**BBDown will auto-install during installation!**

---

## 🚀 Quick Start

### Download Video

```bash
# Basic download
bilibit https://b23.tv/BV1xx

# With quality
bilibit https://b23.tv/BV1xx --quality 4K

# With danmaku
bilibit https://b23.tv/BV1xx --danmaku
```

### View History

```bash
bilibit history
bilibit history --limit 20
```

---

## 📋 Command Reference

| Command | Description |
|---------|-------------|
| `bilibit <url>` | Download video |
| `bilibit history` | View history |
| `bilibit --help` | Show help |
| `bilibit --version` | Show version |

### Download Options

| Option | Short | Description |
|--------|-------|-------------|
| `--quality` | `-q` | Video quality (4K, 1080P, etc.) |
| `--danmaku` | `-d` | Download danmaku |
| `--output` | `-o` | Output directory |

---

## 💡 How to Get URL

1. Open Bilibili in browser
2. Find the video you want
3. Copy URL from address bar
4. Run `bilibit <URL>`

**Example URL**: `https://www.bilibili.com/video/BV1yVwXzGEbL`

---

## ⚠️ Notes

- **Copyright**: For personal learning only
- **BBDown**: Auto-installs with bilibit
- **Premium**: Cookie needed for 1080P+

---

## 🔗 Links

- **GitHub**: https://github.com/AoturLab/bilibit
- **npm**: https://www.npmjs.com/package/bilibit
- **Issues**: https://github.com/AoturLab/bilibit/issues

---

## 📄 License

MIT License

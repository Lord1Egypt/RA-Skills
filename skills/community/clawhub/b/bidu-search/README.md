# 🔍 Baidu Web Search

**百度网页搜索技能 - 使用百度搜索 API 进行网络搜索**

[![Version 1.0.0](https://img.shields.io/badge/version-1.0.0-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🔐 Required Environment Variables

⚠️ **This skill requires API credentials:**

| Variable | Description | Required |
|----------|-------------|----------|
| `BAIDU_API_KEY` | Baidu Search API key | ✅ Yes |

**Setup:**
```bash
export BAIDU_API_KEY="your_baidu_api_key"
```

**Get API Key:** https://ai.baidu.com/

---

## ✨ Features

- 🔍 **Baidu Web Search** - 使用百度搜索 API
- 🇨🇳 **Chinese Focus** - 专注中文搜索
- 📊 **Customizable** - 可定制结果数量
- 🚀 **Easy Integration** - 易于集成

---

## 🚀 Installation

### 1. Clone or Create

```bash
cd ~/.openclaw/workspace/skills
# Already created at: baidu-web-search/
```

### 2. Install Dependencies

```bash
cd baidu-web-search
pip3 install -r requirements.txt
```

### 3. Configure API Key

```bash
# Get API key from: https://ai.baidu.com/
export BAIDU_API_KEY="your_api_key"
```

---

## 📖 Usage

### Python API

```python
from src.baidu_search import baidu_search

# Search
result = baidu_search("人工智能 2026", count=10)
print(result)
```

### CLI

```bash
python3 src/baidu_search.py "人工智能 2026" 10
```

---

## ⚙️ Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `BAIDU_API_KEY` | 百度 API 密钥 | ✅ |

### Get API Key

1. 访问 https://ai.baidu.com/
2. 注册/登录账号
3. 控制台 → 应用管理
4. 创建应用获取 API Key

---

## 📁 Structure

```
baidu-web-search/
├── src/
│   └── baidu_search.py
├── requirements.txt
├── .env.example
├── SKILL.md
└── README.md
```

---

## 📄 License

MIT License

---

**Happy Searching! 🔍**

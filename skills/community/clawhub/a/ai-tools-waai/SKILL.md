---
name: ai_tools
description: "AI Tools Box - Search and invoke 100+ AI tools. Use when: need to find best AI tool for task, compare tools, or quickly access AI services. / AI工具箱 - 搜索调用100+主流AI工具。"
metadata:
  author: "WaaiOn"
  version: "1.2"
  openclaw:
    emoji: "🧰"
    requires:
      bins: ["python3"]
---

# 🧰 AI Tools Box / AI工具箱

Search and invoke 100+ mainstream AI tools. Your unified AI tool gateway.

## When to Use / 使用场景

| EN | CN |
|----|----|
| Find best AI tool for task | 为任务找到最佳AI工具 |
| Compare AI tools | 对比各AI工具 |
| Quick access to AI services | 快速访问AI服务 |
| Explore new AI capabilities | 探索新AI能力 |

## Categories / 工具分类

| Category | EN | CN | Count |
|----------|----|----|-------|
| Writing | AI写作 | 9+ |
| Image | AI图像 | 13+ |
| Video | AI视频 | 11+ |
| Coding | AI编程 | 11+ |
| Office | AI办公 | 11+ |
| Search | AI搜索 | 8+ |
| Chat | AI聊天 | 10+ |
| Audio | AI音频 | 8+ |
| Design | AI设计 | 8+ |
| Agent | AI智能体 | 8+ |
| Translation | AI翻译 | 6+ |
| Dev Platform | AI开发平台 | 9+ |
| Learning | AI学习 | 6+ |
| Detection | AI检测 | 5+ |

**Total: 122+ tools**

## Usage / 使用

```python
from ai_tools import find, call, category

# Search tools / 搜索工具
find("写论文")  # Write paper
find("PPT")
find("image generation")

# By category / 按类别
category("图像")  # Image
category("视频")  # Video

# Call tool / 调用工具
call("Midjourney")
```

## CLI Usage / 命令行

```bash
python ai_tools.py list              # List categories
python ai_tools.py search <keyword>   # Search
python ai_tools.py category <cat>    # By category
python ai_tools.py call <name>       # Invoke
```

## Installation / 安装

```bash
npx clawhub install ai-tools-waai
```

## Examples / 示例

```bash
# Find writing tools
python ai_tools.py search "论文"

# Find image tools  
python ai_tools.py search "绘图"

# List all categories
python ai_tools.py list
```

## Author / 作者

- WaaiOn

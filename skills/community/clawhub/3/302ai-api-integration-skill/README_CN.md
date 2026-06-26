<p align="center"><a href="https://302.ai/" target="blank"><img src="banner.png" /></a></p >

<h1 align="center">
<span>
    # 302.AI API 集成Skill
</span>
</h1>


> 🚀 **一键集成 1400+ AI API 到你的代码中** - 最强大的 Claude Code 技能，无缝对接 302.AI API

[English](./README.md) | 中文文档

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blue.svg)](https://claude.com/claude-code)
[![APIs](https://img.shields.io/badge/APIs-1400%2B-green.svg)](https://doc.302.ai/)

## ✨ 这是什么？

一个强大的 Claude Code 技能，能够**自动**搜索 302.AI 的 1400+ AI API，并生成你所需编程语言的即用代码。不再需要手动查找文档或编写样板代码！

## 🎯 核心特性

- 🔍 **智能 API 发现** - 自动搜索 9 大类别的 1400+ API
- 💻 **多语言支持** - 生成 Python、JavaScript、TypeScript、Go 等语言代码
- 🔄 **始终最新** - 实时获取最新 API 列表
- 🎨 **零上下文浪费** - 基于脚本的高效搜索，减少 token 使用
- 🛡️ **安全优先** - 内置 API Key 保护警告
- ⚡ **闪电般快速** - Bash 优化搜索，即时获得结果

## 📦 涵盖的 API 类别

| 类别 | 示例 | 覆盖率 |
|------|------|--------|
| 🤖 **语言大模型** | GPT、Claude、Gemini、国产模型 | 30% |
| 🎨 **图片生成** | Nano-Banana、Midjourney、Stable Diffusion、Flux | 25% |
| 🎬 **视频生成** | Runway、Pika、Luma AI、Kling | 20% |
| 🎵 **音频处理** | TTS、STT、音乐生成 | 10% |
| 📄 **文档处理** | OCR、PDF、网页抓取 | 10% |
| 🧠 **RAG 与向量** | 向量搜索、Rerank | 3% |
| 🛠️ **工具与实用** | 创意、写作、专业工具 | 2% |

## 🚀 快速开始

### 安装

只需将这个 GitHub 链接发给 Claude Code：

```
安装这个skill：https://github.com/302ai/302AI-API-Integration-Skill
```

Claude Code 会自动为你安装这个技能！

### 验证安装

检查技能是否已加载：

```
有哪些可用的技能？
```

你应该能在列表中看到 `302ai-api-integration`。

### 基本使用

直接用自然语言向 Claude Code 提问：

```
"我想在 Python 项目中使用 GPT-4"
"如何在 Node.js 中用 DALL-E 生成图片？"
"集成语音转文本 API"
```

技能会：
1. ✅ 询问你的 302.AI API Key
2. ✅ 搜索最新的 API 列表
3. ✅ 展示匹配的 API
4. ✅ 生成完整的集成代码
5. ✅ 提供使用示例和最佳实践

## 💡 使用示例

### 示例 1：集成 GPT-4 聊天

**你**："我想在 Python 项目中使用 GPT-4"

**Claude Code**（使用此技能）：
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

# 使用示例
result = call_gpt4("你好，GPT-4！")
print(result)
```

### 示例 2：图片生成

**你**："用 Stable Diffusion 在 JavaScript 中生成图片"

**Claude Code** 生成完整的 Node.js 代码，包括：
- ✅ API 端点配置
- ✅ 图片生成函数
- ✅ 错误处理
- ✅ 文件保存逻辑

### 示例 3：视频生成

**你**："我需要从文本创建视频"

**Claude Code**：
1. 搜索视频生成 API（Runway、Pika、Luma AI 等）
2. 展示选项和描述
3. 在你选择后生成集成代码
4. 包含长时间运行任务的异步处理

## 🛠️ 高级功能

### Bash 命令搜索

技能包含强大的 Python 脚本，可直接搜索 API：

```bash
# 按关键词搜索
python3 scripts/parse_api_list.py "GPT"

# 按类别搜索
python3 scripts/parse_api_list.py "图片生成"

# 组合搜索
python3 scripts/parse_api_list.py "聊天" "语言大模型"
```

### Python 模块使用

```python
from scripts.parse_api_list import fetch_llms_txt, parse_llms_txt, search_apis

# 自动获取最新 API 列表
content = fetch_llms_txt()
apis = parse_llms_txt(content)

# 搜索 API
results = search_apis(apis, keyword='GPT', category='语言大模型')

# 显示结果
for api in results:
    print(f"{api['name']}: {api['link']}")
```

## 📚 文档结构

```
302ai-api-integration/
├── SKILL.md                          # 主技能说明
├── scripts/
│   └── parse_api_list.py            # API 搜索脚本（自动获取）
├── references/
│   ├── api_categories.md            # 完整 API 分类索引
│   ├── integration_examples.md      # 所有语言的代码模板
│   └── parse_script_usage.md        # 脚本使用指南
└── assets/                          # （预留）
```

## 🔒 安全最佳实践

技能会自动警告你：

- ⚠️ **前端 API Key 暴露** - 永远不要在纯前端代码中使用 API Key
- ✅ **推荐方案** - 使用后端框架（Next.js、Express、Flask）
- 🔐 **环境变量** - 安全存储密钥
- 🚫 **版本控制** - 永远不要提交 API Key

## 🎨 支持的语言

- 🐍 **Python** - 完整的异步支持
- 📜 **JavaScript/Node.js** - 现代 ES6+ 语法
- 📘 **TypeScript** - 完整类型定义
- 🔷 **Go** - 地道的 Go 代码
- 🔧 **cURL** - 即用命令
- ➕ **更多** - 可请求任何语言！

## 🌟 为什么使用这个技能？

### 之前（手动集成）
```
1. 搜索 302.AI 文档
2. 找到正确的 API
3. 阅读文档
4. 复制端点 URL
5. 编写样板代码
6. 调试认证
7. 手动处理错误
⏱️ 时间：30-60 分钟
```

### 之后（使用此技能）
```
1. 自然语言向 Claude Code 提问
2. 获得完整可用代码
⏱️ 时间：2-3 分钟
```

## 📊 性能

- **搜索速度**：< 2 秒搜索 1400+ API
- **上下文使用**：最小化（基于脚本搜索）
- **代码质量**：生产就绪，包含错误处理
- **准确性**：始终使用最新 API 文档

## 🤝 贡献

发现 bug 或有建议？我们很乐意听到你的声音！

1. Fork 仓库
2. 创建你的功能分支
3. 提交你的更改
4. 推送到分支
5. 开启 Pull Request

## 📝 许可证

本项目采用 Apache License 2.0 许可 - 详见 LICENSE 文件。

## 🔗 链接

- [302.AI 官方网站](https://302.ai/)
- [302.AI API 文档](https://doc.302.ai/)
- [Claude Code](https://claude.com/claude-code)

## 💬 支持

- 📧 邮箱：support@302.ai
- 💬 Discord：[加入我们的社区](#)
- 📖 文档：[完整文档](https://doc.302.ai/)

## 🎉 致谢

- 为 [Claude Code](https://claude.com/claude-code) 构建
- 由 [302.AI](https://302.ai/) 的综合 API 平台驱动
- 受开发者社区对更快 API 集成需求的启发

---

<div align="center">

**⭐ 如果觉得有用，请给这个仓库点个星！**

用 ❤️ 为珍惜时间的开发者打造

[开始使用](#-快速开始) • [查看示例](#-使用示例) • [阅读文档](#-文档结构)

</div>

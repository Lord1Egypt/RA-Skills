# 抖音直播弹幕 AI 智能回复助手

> 实时采集抖音直播间弹幕，使用 DeepSeek AI 分析用户意图并生成个性化回复建议，帮助主播高效互动。

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Node.js](https://img.shields.io/badge/Node.js-Required-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![WorkBuddy Skill](https://img.shields.io/badge/WorkBuddy-Skill-purple.svg)

---

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 🔴 **实时弹幕采集** | 通过 WebSocket 直连抖音直播服务器，毫秒级获取弹幕 |
| 🤖 **AI 智能回复** | 接入 DeepSeek API，深度分析意图，生成贴近人设的回复 |
| 💾 **智能缓存** | LRU 缓存最近 100 条回复，相同问题直接命中，节省 API 费用 |
| 🎭 **多场景适配** | 支持电商、教育、游戏、娱乐等多种直播类型，自动切换话术风格 |
| 🔄 **自动重连** | 网络波动自动恢复，支持无人值守长时间运行 |
| 🚫 **智能过滤** | 自动过滤无效弹幕、灌水内容、指定用户/关键词 |

---

## 🖥️ 效果预览

```
============================================================
[2026-03-19 20:30:15] [API] 暴躁的嘉文四世: W什么技能
------------------------------------------------------------
DeepSeek AI回复: @暴躁的嘉文四世 朋友，W是黄金圣盾！
开盾减速还能加护甲，对线换血的神技，物理打手必出！
============================================================

============================================================
[2026-03-19 20:31:02] [缓存] 嘦姕: 龙女改版了？
------------------------------------------------------------
DeepSeek AI回复: @嘦姕 朋友好眼力！龙女确实改版了，
新 W 加了额外移速，清野效率更高，晚点给大家演示一波！
============================================================
```

> `[API]` 表示实时调用生成，`[缓存]` 表示命中本地缓存

---

## 📋 适用场景

- **🛒 电商直播** — 自动回复价格、质量、发货等买家咨询，引导下单
- **📚 教育直播** — 专业解答学习、育儿、技能提升类问题
- **🎮 游戏直播** — 回应英雄技巧、出装思路、版本强势等游戏问题
- **💡 知识分享** — 应对观众提问，保持互动热度
- **🎤 娱乐直播** — 活跃弹幕氛围，提升用户粘性

---

## 🚀 快速开始

### 方式一：作为 WorkBuddy Skill 使用（推荐）

1. 下载 `douyin-live-ai.zip`
2. 在 WorkBuddy 中安装 Skill：将 zip 解压到 `~/.workbuddy/skills/douyin-live-ai/`
3. 在对话中输入：

```
@skill://douyin-live-ai https://live.douyin.com/你的直播间ID
```

### 方式二：独立运行

**克隆仓库**

```bash
git clone https://github.com/your-username/douyin-live-ai.git
cd douyin-live-ai/scripts
```

**安装依赖**

```bash
# Python 依赖
pip install websocket-client requests execjs protobuf

# 确保已安装 Node.js
node --version
```

**配置参数**

编辑 `scripts/config.py`：

```python
# 直播间 ID（URL 最后的数字）
ROOM_ID = "349873582969"

# 直播类型：ecommerce / education / entertainment
LIVE_TYPE = "entertainment"

# 主播信息
HOST_NAME = "英雄联盟游戏主播"
HOST_INTRO = """
主播是英雄联盟游戏主播，专注于LOL游戏直播。
擅长各种英雄操作，经常分享游戏技巧、出装思路、对线细节。
"""

# DeepSeek API Key（https://platform.deepseek.com 获取）
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"
```

> 也可通过环境变量注入：`set DEEPSEEK_API_KEY=sk-xxxx`（推荐，更安全）

**启动程序**

```bash
# Windows 双击或命令行运行（自动设置 UTF-8 编码）
start.bat

# 或手动启动基础版
python main.py

# 推荐：自动重连版（网络断开自动恢复）
python main_with_reconnect.py
```

---

## ⚙️ 配置说明

`scripts/config.py` 完整配置项：

```python
# ==================== 直播间配置 ====================
ROOM_ID = "349873582969"          # 直播间ID，取自 URL 末尾数字
LIVE_TYPE = "entertainment"        # 直播类型

# ==================== 主播人设配置 ====================
HOST_NAME = "主播名称"
HOST_INTRO = """主播详细介绍..."""
HOST_PERSONA = "幽默风趣的游戏玩家"
REPLY_STYLE = "humorous"           # humorous / professional / friendly

# ==================== DeepSeek API ====================
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"
DEEPSEEK_MODEL = "deepseek-chat"
TEMPERATURE = 0.7                  # 0=严谨，1=均衡，2=创意
MAX_TOKENS = 500

# ==================== 过滤配置 ====================
IGNORED_USERS = ["管理员", "系统消息"]
IGNORED_KEYWORDS = ["666", "哈哈哈"]
MIN_MESSAGE_LENGTH = 2
```

### 直播类型说明

| `LIVE_TYPE` 值 | 适用场景 | AI 话术风格 |
|---------------|---------|-----------|
| `ecommerce` | 电商带货 | 引导下单、强调优惠、处理异议 |
| `education` | 知识教育 | 专业解答、耐心指导、鼓励学习 |
| `entertainment` | 游戏娱乐 | 轻松幽默、积极互动、活跃氛围 |

---

## 📁 项目结构

```
douyin-live-ai/
├── SKILL.md                      # WorkBuddy Skill 描述文件
├── start.bat                     # Windows 一键启动脚本（含 UTF-8 设置）
├── references/
│   └── prompts.md               # AI 提示词设计参考
└── scripts/
    ├── main.py                  # 程序入口（基础版）
    ├── main_with_reconnect.py   # 程序入口（自动重连版）
    ├── douyinlive.py            # WebSocket 连接与弹幕解析
    ├── deepseek_ai.py           # DeepSeek AI 集成
    ├── reply_cache.py           # LRU 缓存管理
    ├── config.py                # 全局配置
    ├── sign.js                  # 抖音签名生成
    ├── get_sign_wrapper.js      # Node.js 包装器
    ├── CoreUtils/               # 加密工具
    │   └── Encrypt.py
    └── douyin/                  # Protobuf 协议定义
        ├── douyin.proto
        └── douyin_pb2.py
```

**运行后生成的数据文件：**

| 文件 | 说明 |
|------|------|
| `ai_replies.jsonl` | 所有 AI 回复记录（含时间戳、用户名、弹幕、回复） |
| `danmu_cache.jsonl` | 弹幕缓存持久化文件 |

---

## 🔧 常见问题

**Q: 提示 `'gbk' codec can't encode character`**

A: Windows 终端默认 GBK 编码，请使用 `start.bat` 启动（已内置 `chcp 65001` 切换 UTF-8）。

**Q: 程序运行一段时间后自动断开**

A: 这是正常现象，抖音服务器会主动关闭空闲连接。请使用 `main_with_reconnect.py`，它会自动重连，最多重试 100 次。

**Q: 没有弹幕输出**

A: 请确认：① 直播间 ID 正确 ② 目标直播间正在直播 ③ 网络连接正常。

**Q: AI 回复很慢或超时**

A: 检查网络是否能访问 `api.deepseek.com`。可适当降低 `MAX_TOKENS` 值加快响应速度。

**Q: 如何获取直播间 ID？**

A: 打开抖音直播间，浏览器地址栏 URL 末尾的数字即为 ID：
```
https://live.douyin.com/349873582969
                        ^^^^^^^^^^^^
                        这串数字就是 ROOM_ID
```

---

## 📦 依赖列表

| 依赖 | 版本要求 | 用途 |
|------|---------|------|
| Python | 3.7+ | 运行环境 |
| Node.js | 任意版本 | 执行签名生成脚本 |
| websocket-client | - | WebSocket 连接 |
| requests | - | HTTP 请求 |
| PyExecJS | - | 调用 JS 签名脚本 |
| protobuf | - | 解析抖音 Protobuf 消息 |

```bash
pip install websocket-client requests PyExecJS protobuf
```

---

## 📄 许可证

MIT License — 本项目仅供学习与技术交流使用，请勿用于任何商业或违法用途。

---

## 🙏 致谢

- [DeepSeek](https://platform.deepseek.com) — 提供强大的 AI API 支持
- [WorkBuddy](https://www.codebuddy.cn) — Skill 插件体系支持

# 抖音直播弹幕AI智能回复助手

## 功能概述

本 Skill 是一个完整的抖音直播弹幕采集与AI回复系统：
1. **实时弹幕采集** - 通过 WebSocket 连接抖音直播服务器，实时获取弹幕
2. **AI 智能分析** - 使用 DeepSeek API 深度分析每条弹幕的用户意图
3. **个性化回复** - 根据主播人设生成专业、亲切的回复建议
4. **智能缓存** - 缓存最近100条回复，避免重复调用API，节省费用
5. **自动重连** - 断线后自动重连，保持稳定运行
6. **多场景支持** - 支持电商、教育、游戏、娱乐等直播类型

## 适用场景

- **电商直播**：回复价格、质量、发货等咨询
- **教育直播**：解答学习、育儿、成长问题
- **游戏直播**：回应游戏技巧、出装、对局问题
- **知识分享**：回应观众提问和互动
- **带货直播**：引导下单、处理异议

## 项目结构

```
douyin-live-ai/
├── SKILL.md                    # 本文件（Skill说明文档）
├── start.bat                   # 一键启动脚本（Windows）
├── scripts/                    # 核心脚本
│   ├── config.py              # 配置文件（填写直播间ID和API Key）
│   ├── main.py                # 程序入口（基础版）
│   ├── main_with_reconnect.py # 程序入口（推荐，自动重连）
│   ├── douyinlive.py          # WebSocket连接与消息处理
│   ├── deepseek_ai.py         # DeepSeek AI集成
│   ├── reply_cache.py         # 回复缓存管理（LRU）
│   ├── sign.js                # 抖音签名生成脚本
│   ├── get_sign_wrapper.js    # Node.js包装器（解决编码问题）
│   ├── douyin/                # Protobuf定义
│   │   ├── douyin.proto
│   │   └── douyin_pb2.py
│   └── CoreUtils/             # 加密工具
│       ├── __init__.py
│       └── Encrypt.py
└── references/                # 参考资料
    └── prompts.md             # AI提示词参考
```

## 环境依赖

- Python 3.7+
- Node.js（用于执行签名生成脚本）
- DeepSeek API Key（在 https://platform.deepseek.com/ 注册获取）

### 安装Python依赖

```bash
pip install websocket-client requests execjs protobuf
```

## 快速开始

### 第一步：配置直播间信息

编辑 `scripts/config.py`，填写以下必填项：

```python
# 直播间ID（URL最后的数字）
# 例如 https://live.douyin.com/349873582969 → ROOM_ID = "349873582969"
ROOM_ID = "your_room_id_here"

# 直播类型
LIVE_TYPE = "entertainment"  # 可选: ecommerce, education, entertainment

# 主播名称
HOST_NAME = "你的主播名称"

# 主播简介（填写越详细，AI回复越准确）
HOST_INTRO = """
你的主播简介...
"""

# DeepSeek API Key
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"
# 也可通过环境变量设置（推荐）：
# set DEEPSEEK_API_KEY=your_key（Windows）
# export DEEPSEEK_API_KEY=your_key（Linux/Mac）
```

### 第二步：启动程序

**方式一：双击 `start.bat`（推荐，Windows）**
- 自动设置UTF-8编码
- 在独立窗口运行，支持自动滚动
- 使用带自动重连的版本

**方式二：命令行启动**
```bash
cd scripts
# 基础版
python main.py
# 自动重连版（推荐）
python main_with_reconnect.py
```

### 第三步：查看输出

```
============================================================
[2026-03-21 10:30:15] [API] 用户A: W什么技能
------------------------------------------------------------
DeepSeek AI回复: @用户A 朋友，W是黄金圣盾啊！开盾减速还能加护甲，对线换血的神技！
============================================================

============================================================
[2026-03-21 10:30:45] [缓存] 用户B: 这出装怎么出？
------------------------------------------------------------
DeepSeek AI回复: @用户B 亲，这英雄核心装备是...
============================================================
```

**标识说明：**
- `[API]` - 调用 DeepSeek API 实时生成的回复
- `[缓存]` - 相同问题命中缓存，直接复用（节省API调用）

## 配置说明

### config.py 完整配置

```python
# ==================== 直播间配置 ====================
ROOM_ID = "your_room_id_here"           # 直播间ID（必填）
LIVE_TYPE = "entertainment"             # 直播类型

# ==================== 主播简介配置 ====================
HOST_NAME = "你的主播名称"               # 主播名称（必填）
HOST_INTRO = """主播详细介绍..."""       # 主播简介（必填，越详细越好）
HOST_PERSONA = "主播人设风格"            # 人设风格
REPLY_STYLE = "humorous"               # 回复风格

# ==================== DeepSeek API 配置 ====================
DEEPSEEK_API_KEY = "your_api_key"       # API Key（必填）
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"        # 模型名称
TEMPERATURE = 0.7                       # 温度参数（0-2）
MAX_TOKENS = 500                        # 最大token数

# ==================== 过滤配置 ====================
IGNORED_USERS = ["管理员", "系统消息"]   # 忽略用户
IGNORED_KEYWORDS = ["666", "哈哈哈"]     # 忽略关键词
MIN_MESSAGE_LENGTH = 2                  # 最小消息长度
```

### 直播类型说明

| LIVE_TYPE | 适用场景 | 回复风格 |
|-----------|---------|---------|
| `entertainment` | 游戏、娱乐直播 | 轻松幽默、积极互动 |
| `ecommerce` | 电商带货 | 引导下单、强调优惠 |
| `education` | 知识分享、教学 | 专业解答、耐心指导 |

### 回复风格说明

| REPLY_STYLE | 风格描述 |
|-------------|---------|
| `humorous` | 幽默风趣，活跃气氛 |
| `friendly` | 亲切友好，温暖互动 |
| `professional` | 专业严谨，权威解答 |

## 核心功能详解

### 智能过滤
- 自动过滤欢迎消息、礼物消息、系统消息
- 忽略纯数字、纯表情、无意义内容
- 可配置忽略特定用户和关键词

### LRU 缓存机制
- 保存最近100条回复
- 相同问题直接返回缓存，节省API调用费用
- 缓存持久化到本地 `ai_replies_cache.json`

### 自动重连
- 连接断开后自动重连，最多100次
- 每次重连间隔5秒
- `Ctrl+C` 可手动停止

## 示例回复

| 直播类型 | 用户弹幕 | AI 回复 |
|---------|---------|---------|
| 游戏 | "W什么技能？" | "@用户 朋友，W是黄金圣盾啊！开盾减速还能加护甲，对线换血的神技！" |
| 电商 | "这个多少钱？" | "@用户 宝子，这款今天直播间专属福利价！具体看左下角小黄车~" |
| 教育 | "高敏感孩子怎么引导" | "@用户 亲，高敏感孩子天赋满满！建议：1.接纳特质 2.提前告知变化..." |
| 娱乐 | "晚上好" | "@用户 欢迎宝子！今天福利多多，喜欢什么告诉我~" |

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| GBK编码错误 | 使用 `start.bat` 启动，会自动设置UTF-8编码 |
| 连接失败/断开 | 使用 `main_with_reconnect.py`，自动重连 |
| 没有弹幕输出 | 确认直播间ID正确且正在直播 |
| AI回复很慢 | 检查网络；降低 `TEMPERATURE`；善用缓存 |
| Node.js 报错 | 确保已安装 Node.js：https://nodejs.org |

## 注意事项

1. **Node.js 环境**：必须安装 Node.js，用于执行抖音签名生成
2. **API Key 安全**：建议通过环境变量 `DEEPSEEK_API_KEY` 设置，避免硬编码
3. **网络连接**：需要稳定的网络连接抖音服务器
4. **频率限制**：注意 DeepSeek API 的调用频率和费用

## 免责声明

本项目仅供学习与技术交流使用，请勿用于任何商业或非法用途。

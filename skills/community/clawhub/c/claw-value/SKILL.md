---
name: clawvalue
description: "OpenClaw Claw度评估系统 - 量化你的 AI 自动化能力，生成龙虾能力估值趣味评估报告。支持16套主题、5级Mock数据、游戏化展示。"
version: 2.0.0
metadata:
  clawdbot:
    emoji: "🦞"
    requires:
      py:
        - flask>=2.0
        - requests>=2.25
    config:
      env:
        CLAWVALUE_PORT:
          description: 服务端口
          default: 5002
        DASHSCOPE_API_KEY:
          description: 百炼API密钥（可选，用于图片生成）
          default: ""
---

# 🦞 ClawValue - OpenClaw 能力估值系统

量化你在 OpenClaw 上的 AI 自动化能力，生成趣味化的"龙虾能力估值"评估报告。

## 📦 安装依赖

在项目根目录执行：

```bash
cd 到skill安装目录/clawValue
pip install -r requirements.txt
```

或手动安装：

```bash
pip install flask requests
```

## 🔑 配置（可选）

**DASHSCOPE_API_KEY** - 百炼 API 密钥

```bash
export DASHSCOPE_API_KEY="your-api-key"
```

**说明：**
- ✅ 不配置也能使用：数据采集、评估分析、页面展示
- ❌ 不配置无法使用：龙虾海报图片生成（会跳过图片相关功能）

## 🚀 快速开始

### 方式一：一键启动（推荐）

```bash
python scripts/server.py
```

访问：http://localhost:5002

### 方式二：自定义参数

```bash
# 指定端口
python scripts/server.py --port 8080

# 监听所有网卡（支持局域网/公网访问）
python scripts/server.py --host 0.0.0.0 --port 5002

# 完整参数
python scripts/server.py -H 0.0.0.0 -p 5002
```

**参数说明：**

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--host` | `-H` | 127.0.0.1 | 绑定地址，`0.0.0.0` 允许外部访问 |
| `--port` | `-p` | 5002 | 服务端口 |

**⚠️ 远程访问注意：**
- 使用 `--host 0.0.0.0` 才能从其他设备访问
- 确保防火墙/安全组开放对应端口
- 云服务器需要配置安全组白名单

## 🌐 访问地址

### 默认页面
```
http://localhost:5002
```

### 带锐评内容访问
```
http://localhost:5002/?clawJudge=这是大型生成的锐评内容
```

**URL 参数：**
- `clawJudge` - 自定义锐评内容（URL编码）

**示例：**
```bash
# 中文内容需要 URL 编码
curl "http://localhost:5002/?clawJudge=$(python3 -c 'import urllib.parse; print(urllib.parse.quote(\"你的锐评内容\"))')"
```

## 🔄 交互模式

### 模式一：独立服务模式

```
┌─────────────────────────────────────────────────────┐
│  1. 安装依赖                                         │
│     pip install flask requests                      │
│                                                     │
│  2. 配置百炼API（可选）                               │
│     export DASHSCOPE_API_KEY="xxx"                  │
│     └─ 不配置：影响图片生成，不影响分析服务             │
│                                                     │
│  3. 启动服务                                         │
│     python scripts/server.py                        │
│                                                     │
│  4. 访问页面                                         │
│     http://localhost:5002                           │
└─────────────────────────────────────────────────────┘
```

**特点：**
- 自动采集 OpenClaw 数据
- 内置 AI 生成锐评内容
- 完整的页面展示

### 模式二：API 集成模式

```
┌─────────────────────────────────────────────────────┐
│  1. 安装依赖                                         │
│     pip install flask requests                      │
│                                                     │
│  2. 配置百炼API（可选）                               │
│     export DASHSCOPE_API_KEY="xxx"                  │
│                                                     │
│  3. 调用 API 获取数据                                │
│     GET /api/ → 返回评估数据 JSON                    │
│                                                     │
│  4. 生成锐评内容                                     │
│     调用大模型 API，结合数据生成锐评                  │
│                                                     │
│  5. 传入页面展示                                     │
│     http://host:port/?clawJudge=锐评内容            │
└─────────────────────────────────────────────────────┘
```

**特点：**
- 数据与展示分离
- 可集成到其他系统
- 支持自定义锐评逻辑

## 📡 API 接口

### 获取评估数据

```
GET /api/
```

**响应示例：**
```json
{
  "success": true,
  "data": {
    "depth_level": 2,
    "value_estimation": {
      "amount": 2500,
      "currency": "CNY"
    },
    "skills": {
      "total": 12,
      "custom": 10,
      "categories": {
        "社交媒体": 3,
        "工具效率": 2,
        "自动化": 2
      }
    },
    "sessions": {
      "total": 1500,
      "active_days": 15
    },
    "evaluation": {
      "skill_score": 45,
      "automation_score": 35,
      "integration_score": 30
    },
    "achievements": [
      "🎮 新手上路",
      "🦞 初级玩家"
    ],
    "log_stats": {
      "info_count": 1200,
      "warn_count": 200,
      "error_count": 100,
      "tool_calls": 150
    }
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `depth_level` | int | 使用深度等级 (1-5) |
| `value_estimation.amount` | int | 估值金额（元） |
| `skills.total` | int | 技能总数 |
| `skills.custom` | int | 自定义技能数 |
| `skills.categories` | object | 技能分类统计 |
| `sessions.total` | int | 日志条目总数 |
| `sessions.active_days` | int | 活跃天数 |
| `evaluation.skill_score` | int | 技能评分 (0-100) |
| `evaluation.automation_score` | int | 自动化评分 (0-100) |
| `evaluation.integration_score` | int | 集成评分 (0-100) |
| `achievements` | array | 成就列表 |
| `log_stats.*` | int | 日志统计数据 |

### 生成龙虾海报

```
POST /api/generate-image
Content-Type: application/json

{
  "level": 2,
  "title": "初级玩家",
  "roast": "你的技能树已经点亮了一半..."
}
```

**注意：** 需要配置 `DASHSCOPE_API_KEY`

## 🎮 等级体系

| 等级 | 名称 | 特征 |
|------|------|------|
| Lv.1 | 入门小白 | 刚接触 OpenClaw，基础交互 |
| Lv.2 | 初级玩家 | 开始使用自定义技能 |
| Lv.3 | 中级开发者 | 多技能协作，自动化场景 |
| Lv.4 | 高级工程师 | 多 Agent，复杂工作流 |
| Lv.5 | 龙虾大师 | 全方位自动化，Proactive 模式 |

## 📂 项目结构

```
clawvalue/
├── SKILL.md              # 技能说明（本文件）
├── requirements.txt      # Python 依赖
├── lib/                  # 核心库代码
│   ├── __init__.py
│   ├── collector.py      # 数据采集（技能扫描、日志解析）
│   ├── constants.py      # 常量定义（分类、来源）
│   ├── evaluation.py     # 评估逻辑
│   ├── schemas.py        # 数据模型
│   ├── image_generator.py # 图片生成（万象API）
│   ├── parser.py         # 日志解析器
│   └── achievements.py   # 成就定义
├── scripts/              # 可执行脚本
│   ├── server.py         # Flask 服务入口
│   └── gen_icons.py      # 批量生成成就图标
├── web/                  # 前端资源
│   ├── index.html        # 单文件前端
│   └── images/           # 图片资源
│       └── achievements/ # 成就图标
└── docs/                 # 文档和设计资料
```

## 🎨 主题系统

支持 **16 套精美主题**：

| 主题名 | 说明 | 类型 |
|--------|------|------|
| deep-sea | 深海龙虾（默认） | 深色 |
| neo-brutalist | 新野兽派设计 | 特色 |
| fresh-garden | 清新花园 | 浅色 |
| cyber-neon | 赛博霓虹 | 深色 |
| retro-type | 复古打字机 | 浅色 |
| minimal-ink | 极简水墨 | 浅色 |
| dark-forest | 暗夜森林 | 深色 |
| summer-beach | 夏日海滩 | 浅色 |
| candy-land | 糖果乐园 | 浅色 |
| dark-gothic | 暗黑哥特 | 深色 |
| vaporwave | 蒸汽波 | 深色 |
| sakura-bloom | 樱花盛开 | 浅色 |
| pixel-game | 像素游戏 | 深色 |
| ocean-deep | 深海 | 深色 |
| music-rhythm | 音乐节奏 | 深色 |
| snow-peak | 雪峰 | 浅色 |

## 🔧 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | Python Flask |
| 前端 | 原生 HTML/CSS/JS |
| 样式 | oklch 颜色、CSS变量、动画 |
| 数据 | JSONL 日志解析、技能扫描 |
| 图片 | 阿里云万象API（可选） |

---

*🦞 ClawValue v2.0 - 让 AI 能力量化变得有趣！*
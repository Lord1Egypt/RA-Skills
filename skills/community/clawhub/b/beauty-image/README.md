# Beauty Image V3 — 商业化AI图片生成 OpenClaw Skill

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](LICENSE)

> **作者: 圆规** | [GitHub](https://github.com/xyva-yuangui/beauty-image)

一个功能强大的 AI 图片生成 OpenClaw 技能，支持 **40+ 场景模板**、**30+ 风格词典**、智能意图识别和三引擎智能路由。

## 特性

- **智能意图识别**: 从自然语言自动解析场景、风格、字段
- **40+ 场景模板**: 名片/海报/头像/产品/水晶/毛绒/天气卡片/分镜/信息图...
- **30+ 风格词典**: 赛博朋克/水墨/浮世绘/吉卜力/像素风/液态玻璃/全息镭射...
- **三引擎智能路由**: 自动按场景+风格选择最优引擎
  - **通义万相 (wanx)** — 阿里云, 文字渲染佳, 成本低
  - **Seedream 4.0** — 火山引擎, 高画质, 性价比
  - **Seedream 5.0** — 火山引擎, 最高画质
- **结构化 Prompt**: 6 层结构 (核心→主体→风格→光照→构图→技术)
- **Prompt 美化器**: 简单输入自动升级为专业级提示词
- **跨平台**: macOS / Linux / Windows

## 安装

### 通过 ClawHub 安装 (推荐)

在 OpenClaw 中搜索 `beauty-image` 并安装。

### 手动安装

```bash
git clone https://github.com/xyva-yuangui/beauty-image.git
# 将仓库复制到 ~/.openclaw/workspace/skills/beauty-image
```

## API Key 配置 (必须)

本技能需要至少配置 **一个** API Key 才能使用。

### 快速开始

```bash
# 方式一: 环境变量 (推荐)
export DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx        # 通义万相 (必选其一)
export ARK_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxx      # Seedream (可选, 画质更高)
export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx          # DeepSeek (可选, LLM意图解析)
```

### openclaw.json 配置

在 `~/.openclaw/openclaw.json` 中添加:

```json
{
  "models": {
    "providers": {
      "wanxiang": { "apiKey": "sk-your-dashscope-key" },
      "ark": { "apiKey": "your-ark-api-key" },
      "deepseek": { "apiKey": "sk-your-deepseek-key" }
    }
  }
}
```

### API Key 获取地址

| 引擎 | 环境变量 | 获取地址 | 说明 |
|------|---------|---------|------|
| **通义万相** | `DASHSCOPE_API_KEY` | [阿里云百炼](https://dashscope.console.aliyun.com/apiKey) | 注册后有免费额度, 推荐首选 |
| **Seedream** | `ARK_API_KEY` | [火山引擎方舟](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) | 需开通方舟平台 |
| **DeepSeek** | `DEEPSEEK_API_KEY` | [DeepSeek](https://platform.deepseek.com/api_keys) | 可选, 用于 `--use-llm` |

### 健康检查

```bash
uv run scripts/check.py
```

## 使用示例

### 智能模式 (自动识别意图 + 模板 + 路由)

```bash
uv run scripts/generate_image_v3.py --prompt "帮我做一张赛博朋克风格的个人名片"
uv run scripts/generate_image_v3.py --prompt "画一只猫的水晶质感手办"
uv run scripts/generate_image_v3.py --prompt "上海天气卡片"
uv run scripts/generate_image_v3.py --prompt "做个毛绒版的苹果logo"
```

### 指定场景模板

```bash
uv run scripts/generate_image_v3.py --prompt "猫" --scene 3d_crystal
uv run scripts/generate_image_v3.py --prompt "武士" --scene art_ukiyoe_card --style 浮世绘
uv run scripts/generate_image_v3.py --prompt "咖啡店" --scene 3d_miniature
```

### 指定字段 (JSON)

```bash
uv run scripts/generate_image_v3.py --prompt "名片" --scene biz_card \
  --fields '{"name":"圆规","title":"CEO","company":"XyvaClaw"}'
```

### Raw 模式 (直接传 prompt)

```bash
uv run scripts/generate_image_v3.py --prompt "一幅美丽的风景画" --raw
```

### 列出模板/风格/引擎

```bash
uv run scripts/generate_image_v3.py --list-scenes
uv run scripts/generate_image_v3.py --list-styles
uv run scripts/generate_image_v3.py --list-providers
```

## 场景模板一览

| 分类 | 模板 | 推荐引擎 |
|------|------|----------|
| 商务 | 名片设计, 商业海报, 产品摄影 | seedream5/4 |
| 社交 | 头像/IP, 表情包, 金句卡片, YouTube缩略图 | seedream4/wanx |
| 创意 | 艺术创作, 浮世绘闪卡 | seedream5 |
| 3D | 水晶质感, 毛绒玩具, 充气玩具, 微缩房间 | seedream5/4 |
| 实用 | 天气卡片, 冰箱贴, 美食地图, 电影分镜 | seedream5 |
| 设计 | PPT页面, Logo, 包装设计, App界面, 书籍封面 | seedream5/wanx |
| 摄影 | 美食摄影, 时尚大片, 风光大片 | seedream4/5 |
| 电商 | 电商主图, 电商横幅 | wanx |
| 内容 | 小红书配图, 文章头图, 漫画条, 梗图 | seedream4/wanx |
| 信息图 | Bento信息图, 对比信息图 | seedream5 |

## 引擎选择

| 引擎 | 画质 | 速度 | 成本 | 适用场景 |
|------|------|------|------|---------|
| **seedream5** | ⭐⭐⭐⭐⭐ | 中 | 中 | 最高画质, 组图 |
| **seedream4** | ⭐⭐⭐⭐ | 较快 | 低 | 高画质, 性价比 |
| **wanx** | ⭐⭐⭐ | 快 | 低 | 文字渲染好 |

V3 自动按场景+风格路由引擎, 无需手动选择。

## 项目结构

```
beauty-image/
├── SKILL.md                          # OpenClaw 技能定义
├── _meta.json                        # 技能元数据
├── README.md                         # 本文件
├── scripts/
│   ├── generate_image_v3.py          # V3 主脚本 (推荐)
│   ├── generate_image_v2.py          # V2 兼容脚本
│   ├── generate_image.py             # V1 万相专用脚本
│   ├── image_intent_parser.py        # 意图识别引擎
│   ├── image_prompt_templates.py     # 场景模板 + 风格词典 + Prompt Builder
│   └── check.py                      # 健康检查脚本
└── examples/
    └── README.md                     # 示例说明
```

## 依赖

- Python >= 3.10
- [uv](https://github.com/astral-sh/uv) (脚本运行器)
- requests >= 2.31.0 (自动安装)

## License

MIT

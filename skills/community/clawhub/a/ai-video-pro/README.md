# ai-video-pro

> 影视级 AI 视频生成技能包 — OpenClaw / ClawHub Skill

[![ClawHub](https://img.shields.io/badge/ClawHub-ai--video--pro-blue)](https://clawhub.com/skills/ai-video-pro)
[![Stage](https://img.shields.io/badge/stage-beta-orange)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

专业 AI 视频生成技能包，将用户随意的描述转化为**电影工业级提示词**，自动检测最优视频生成后端，并支持一键发布到中国主流社交平台。

---

## 核心能力

### 1. 镜头语言提示词优化引擎

将自然语言描述拆解为专业影视元素并重组：

- **镜头类型** — 特写 / 近景 / 中景 / 全景 / 鸟瞰 / 荷兰角 / 过肩镜头
- **运镜方式** — 横摇 / 推轨 / 跟拍 / 摇臂 / 斯坦尼康 / 甩镜 / 变焦拉伸
- **灯光 & 色彩** — 伦勃朗光 / 蝴蝶光 / 明暗对比 / 青橙对比 / 胶片模拟
- **角色动态** — 打击感建模 / 面部微表情序列 / 身体语言 / 机甲关节运动
- **时间控制** — 慢动作 / 延时摄影 / 变速

### 2. 多后端自动检测 & 最小代价优先选择

```
优先级: ComfyUI(本地免费) → Replicate → LumaAI → Runway → DALL-E+FFmpeg
```

自动检测本地 GPU、已安装工具、可用 API 密钥，推荐最优生成方案。

### 3. 中国社交平台发布

一键适配并发布到：

| 平台 | 推荐比例 | 最大文件 |
|------|---------|---------|
| 微博 | 16:9, 9:16 | 500MB |
| 小红书 | 3:4, 1:1, 9:16 | 100MB |
| 抖音 | 9:16 | 128MB |

---

## 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install ai-video-pro

# 或 clone 本仓库
git clone https://github.com/AAAlenwow/ai-video-pro.git
```

### 环境配置

至少配置一个视频生成 API 密钥：

```bash
export LUMAAI_API_KEY="your-key"       # LumaAI Dream Machine
export RUNWAY_API_KEY="your-key"       # Runway Gen-3/Gen-4
export REPLICATE_API_TOKEN="your-key"  # Replicate
export OPENAI_API_KEY="your-key"       # DALL-E 关键帧
```

### 环境检测

```bash
python3 scripts/env_detect.py
```

### 视频生成

```bash
# 通过 provider_manager 生成
python3 scripts/provider_manager.py
```

---

## 项目结构

```
ai-video-pro/
├── SKILL.md                          # 技能定义（ClawHub 入口）
├── scripts/
│   ├── prompt_engine.py              # 镜头语言提示词优化
│   ├── provider_manager.py           # 多后端统一管理
│   ├── env_detect.py                 # 环境自动检测
│   ├── credential_manager.py         # 凭证安全管理
│   ├── preview_server.py             # 本地预览服务
│   ├── publish.py                    # 多平台发布
│   └── install_deps.py              # 依赖自动安装
├── assets/
│   ├── prompt_templates/             # 场景提示词模板
│   └── platform_configs/            # 平台发布配置
├── references/                       # 参考文档
└── tests/                           # 测试
```

---

## 依赖

- Python 3.8+
- ffmpeg（视频处理）
- 至少一个视频生成 API 密钥

---

## 阶段

**Beta** — 核心功能可用，持续迭代中。不建议用于生产环境。

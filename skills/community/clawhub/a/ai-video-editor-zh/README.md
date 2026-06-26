# ai-video-editor

[![ClawHub Skill](https://img.shields.io/badge/ClawHub-Skill-blueviolet)](https://clawhub.io)
[![Version](https://img.shields.io/badge/version-1.0.6-blue)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **一站式 AI 视频剪辑。**
> 模仿风格 ✂️ · 长视频转短视频 🔤 · AI 字幕 🎙️ · AI 解说 📐 · 视频尺寸调整 · 高光集锦 ⚽ · Vlog · 混剪 · 口播
>
> 上传原始素材，配上自然语言要求，交给 AI 处理并拿回成品下载链接。由 [Sparki](https://sparki.io) 提供能力。

---

## 这个 Skill 做什么

这个 ClawHub Skill 把 [Sparki](https://sparki.io) 的 AI 视频编辑 API 封装成了 4 个 Bash 脚本：

| 脚本 | 用途 |
|--------|---------|
| `scripts/upload_asset.sh` | 上传视频文件，返回 `object_key` |
| `scripts/create_project.sh` | 用风格 tips 创建 AI 视频处理项目 |
| `scripts/get_project_status.sh` | 轮询项目状态并获取结果链接 |
| `scripts/edit_video.sh` | **端到端**：上传 → 处理 → 返回下载链接 |

**适用场景：**

| 场景 | 关键词 |
|----------|----------|
| 模仿创作者风格 | 模仿风格、风格迁移、审美对齐 |
| 长视频切短视频 | Long to Short、短视频、Reels、Shorts、TikTok、切片 |
| 自动字幕或解说 | AI 字幕、AI 解说、字幕、旁白 |
| 适配不同平台比例 | 改尺寸、比例转换、竖屏、方屏、横屏 |
| 体育/活动高光 | 高光集锦、精彩片段、最佳时刻 |
| 日常 Vlog | Vlog、旅行、生活记录 |
| 多片段叙事 | 混剪、合集、Mashup |
| 口播 / 采访内容 | 口播、采访、讲解型视频 |
| 批量自动化生产 | 批处理、内容工厂、自动化 |

---

## 快速开始

### 1. 通过 OpenClaw 安装

```bash
npx clawhub install ai-video-editor --force
```

### 2. 配置 API Key

```bash
export SPARKI_API_KEY="sk_live_your_key_here"
```

你可以从 [Sparki](https://sparki.io) 获取 key。

### 3. 处理视频

```bash
# 完整工作流 —— 返回一个 24 小时有效的下载链接
RESULT_URL=$(bash scripts/edit_video.sh my_video.mp4 "22" "节奏更快、更有活力" "9:16")
echo "$RESULT_URL"
```

---

## 环境要求

- `bash` 4.x+
- `curl`
- `jq`
- `SPARKI_API_KEY` 环境变量

---

## 使用示例

**竖屏短视频（默认）：**
```bash
bash scripts/edit_video.sh footage.mp4 "22"
```

**方屏视频 + 创意要求：**
```bash
bash scripts/edit_video.sh clip.mp4 "28" "更有电影感的慢动作" "1:1"
```

**横屏视频 + 限制时长：**
```bash
bash scripts/edit_video.sh raw.mp4 "19" "" "16:9" 60
```

**分步手动控制：**
```bash
# 上传
OBJECT_KEY=$(bash scripts/upload_asset.sh footage.mp4)

# 创建项目
PROJECT_ID=$(bash scripts/create_project.sh "$OBJECT_KEY" "22" "节奏更紧凑" "9:16")

# 轮询直到完成
while true; do
  set +e
  STATUS=$(bash scripts/get_project_status.sh "$PROJECT_ID")
  EXIT_CODE=$?
  set -e
  [[ "$EXIT_CODE" -eq 0 && "${STATUS%% *}" == "completed" ]] && break
  [[ "$EXIT_CODE" -eq 0 && "${STATUS%% *}" == "failed" ]] && break
  sleep 10
done

RESULT_URL="${STATUS#completed }"
echo "Download: $RESULT_URL"
```

---

## 支持的参数

| 参数 | 可选值 | 默认值 |
|-----------|--------|---------|
| `aspect_ratio` | `9:16`, `1:1`, `16:9` | `9:16` |
| `duration` | 整数（秒） | — |
| `tips` | 风格 ID（例如 `22`, `28`） | 必填 |
| `user_prompt` | 自然语言要求 | — |

**超时覆盖：**
```bash
WORKFLOW_TIMEOUT=7200 bash scripts/edit_video.sh long_video.mp4 "1"
ASSET_TIMEOUT=120 bash scripts/edit_video.sh large_file.mp4 "2"
```

---

## 错误码

| Code | 含义 |
|------|---------|
| `401` | API key 无效 |
| `413` | 文件太大（> 3 GB）或存储不足 |
| `453` | 并发项目数达到上限 |
| `500` | 服务端错误，重试即可 |

---

## 发布

```bash
# 打包给 ClawHub
zip -r sparki-video-processor.zip SKILL.md scripts/ README.md
```

通过 [ClawHub Dashboard](https://clawhub.io) 上传并发布。

推荐 metadata：
- **Category:** `video/ai-generation`
- **Tags:** `video-editing`, `ai`, `content-creation`, `short-form`, `highlight`, `vlog`, `montage`, `caption`, `resizer`

---

Powered by [Sparki](https://sparki.io) — AI 视频编辑能力。

---

## 安全说明

- `SPARKI_API_KEY` 只通过 HTTP Header 传递，不会写入磁盘
- 所有用户输入参数都被双引号包裹，降低 shell 注入风险
- 脚本只会向 `agent-enterprise-dev.aicoding.live` 发起网络请求，不会在本地写入视频文件

---

## License

MIT — 见 [LICENSE](LICENSE)。

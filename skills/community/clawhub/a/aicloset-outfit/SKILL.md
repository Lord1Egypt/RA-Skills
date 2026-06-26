---
name: aicloset-outfit
description: |
  AI 智能搭配推荐 - 个人穿搭方案生成工具。

  当用户提到以下意图时使用此技能：
  「今天穿什么」「搭配推荐」「穿搭」「outfit」「穿什么好看」
  「AI搭配」「衣橱搭配」「帮我搭配一套」「明天穿什么」
  「商务风穿搭」「约会穿什么」「休闲搭配」

  支持：根据日期、城市、天气和风格偏好，调用 AI 衣橱 API 生成 4 套穿搭方案，以图片画布形式展示。
  支持渠道：CLI 终端、飞书、钉钉、Discord、Slack 等 IM 聊天工具。
metadata:
  openclaw:
    primaryEnv: AICLOSET_API_KEY
    baseUrl: https://aicloset-dev-h5.wxbjq.top
---

# AI 衣橱搭配推荐

## ⚠️ 必读约束

### 🔑 首次安装配置

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "aicloset-outfit": {
        "enabled": true,
        "apiKey": "你的 x-api-key",
        "env": {
          "AICLOSET_API_KEY": "你的 x-api-key"
        }
      }
    }
  }
}
```

或使用环境变量：

```bash
export AICLOSET_API_KEY="你的 x-api-key"
```

如果用户未配置，**必须先引导用户完成配置**，再继续执行。

---

### 🔒 强制规则

1. **必须执行 `scripts/generate_outfit.py` 脚本**，不可跳过、不可用其他方式替代
2. **禁止自行编造搭配内容**，所有搭配数据必须来自 API 真实返回
3. **必须生成图片**，不可只输出文字描述
4. 脚本执行失败时输出错误信息，不要自己编造结果兜底
5. **不要删除或修改脚本输出中的 `MEDIA:` 行**（IM 渠道需要它来发送图片）

---

### 📦 依赖

| 依赖 | 说明 | 安装方式 |
|------|------|---------|
| Python 3 | 脚本运行环境 | macOS/Linux 自带，Windows 从 python.org 安装 |
| ImageMagick | 图片合成 | `brew install imagemagick` / `choco install imagemagick` / `apt install imagemagick` |

无需 pip install 任何包，所有 Python 代码仅使用标准库。

---

## 快速决策

| 用户意图 | 参数处理 | 执行命令 |
|---------|---------|---------|
| 「给我搭配一套」 | 全部默认值，直接执行 | `python3 scripts/generate_outfit.py` |
| 「明天穿什么」 | date 改为明天 | `python3 scripts/generate_outfit.py --date=2026-03-14` |
| 「上海商务风」 | city+province+style | `python3 scripts/generate_outfit.py --city=上海 --province=上海 --style=商务` |
| 「北京约会穿搭」 | city+province+style | `python3 scripts/generate_outfit.py --city=北京 --province=北京 --style=约会` |

**原则：能从用户输入推断出值就不要追问。所有参数都有默认值，用户什么都不说也能直接出结果。**

---

## 参数说明

| 参数 | CLI 参数 | 说明 | 默认值 |
|------|---------|------|--------|
| `date` | `--date=` | 日期，格式 `YYYY-MM-DD` | 当天日期 |
| `city_name` | `--city=` | 城市名称 | `杭州` |
| `province_name` | `--province=` | 省份名称 | `浙江` |
| `style_text` | `--style=` | 风格偏好（休闲、商务、运动、约会等） | `休闲` |

---

## 执行流程

一共 2 步，严格按顺序执行：

### 第 1 步：提取参数

从用户输入中智能提取参数，未提及的使用默认值。

### 第 2 步：执行脚本

用 Bash 工具直接执行 `scripts/generate_outfit.py`，传入对应参数：

```bash
python3 scripts/generate_outfit.py --date=2026-03-13 --city=杭州 --province=浙江 --style=休闲
```

脚本会自动完成：API 调用 → 图片下载 → 画布合成 → 边框标题 → 总览拼接 → MEDIA 输出 → 系统预览。

### 展示结果

将脚本的终端输出**原样**展示给用户（含 `MEDIA:` 行）。

- **IM 渠道（飞书/钉钉等）**：OpenClaw 自动识别 `MEDIA:` 行，上传并发送图片到聊天
- **CLI 终端**：脚本已内置系统预览命令自动打开图片

**禁止：**
- 不要删除或修改 `MEDIA:` 行
- 不要用 Markdown 图片语法 `![]()`
- 不要用 Read 工具读取图片
- 不要自己编写搭配描述来替代脚本输出

---

## 图片发送（IM 渠道）

脚本输出中包含 `MEDIA:<路径>` 行，OpenClaw 回复管道会自动处理：

1. 识别并提取 `MEDIA:` 后的图片路径
2. 从回复文本中移除 `MEDIA:` 行（用户看不到）
3. 上传图片到对应 IM 平台（飞书/钉钉/Discord/Slack 等）
4. 以图片消息形式发送到聊天会话

### MEDIA 标记格式

- 必须独占一行，以 `MEDIA:` 开头
- 绝对路径：`MEDIA:/tmp/aicloset_xxx/all_outfits.png`
- HTTP URL：`MEDIA:https://example.com/image.png`
- 支持多张图片（多行 `MEDIA:`）
- 路径含空格时用反引号包裹：`` MEDIA:`/path/with spaces/file.png` ``

---

## 错误处理

| 错误场景 | 处理方式 |
|---------|---------|
| API Key 未配置 | 脚本停止执行，引导用户按配置说明设置 |
| API 返回 `code` 非 0 | 展示 `msg` 字段内容，提示具体错误原因 |
| 网络超时或请求失败 | 自动重试一次，仍失败则提示检查网络 |
| ImageMagick 未安装 | 提示安装命令 |
| 单品图片下载失败 | 跳过该单品，继续合成其余部分 |

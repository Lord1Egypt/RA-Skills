---
name: bytedance-visual-recognition
description: >
  ByteDance Visual Recognition — 调用豆包 Doubao-Seed 多模态模型识别图片/视频。
  支持图片转文字、视频转文字、图片转代码、视频转代码，全自动模型降级。
  参与火山协作奖励计划免费使用顶级多模态模型。
  智能调度模型，每模型每日180W tokens，超限自动降级。
summary: "ByteDance Visual Recognition — 调用豆包 Doubao-Seed 识别图片/视频，支持转文字、转代码，参与火山协作奖励计划免费使用"
tags:
  vision: "3.0.0"
  image-recognition: "3.0.0"
  video-recognition: "3.0.0"
  image-to-code: "3.0.0"
  video-to-code: "3.0.0"
  doubao: "3.0.0"
  volcengine: "3.0.0"
  bytedance: "3.0.0"
trigger_patterns:
  - "识别图片"
  - "识别视频"
  - "图片识别"
  - "视频识别"
  - "图片转文字"
  - "视频转文字"
  - "图片转代码"
  - "视频转代码"
  - "看图说话"
  - "图片内容"
  - "视频内容"
  - "图片里有什么"
  - "视频里有什么"
  - "分析图片"
  - "分析视频"
  - "提取图片文字"
  - "提取视频文字"
  - "图片OCR"
  - "UI转代码"
  - "设计稿转代码"
  - "截图转代码"
  - "录屏转代码"
  - "视觉识别"
  - "recognize image"
  - "recognize video"
  - "image to text"
  - "video to text"
  - "image to code"
  - "video to code"
  - "vision"
metadata:
  openclaw:
    requires:
      bins:
        - python
      env:
        - ARK_API_KEY
        - DOUBAO_VISION_20P_ID
        - DOUBAO_VISION_20C_ID
        - DOUBAO_VISION_20L_ID
        - DOUBAO_VISION_16V_ID
        - DOUBAO_VISION_18_ID
        - DOUBAO_VISION_10C_ID
    primaryEnv: ARK_API_KEY
    envVars:
      - name: ARK_API_KEY
        required: true
        description: 火山方舟 API Key，在 console.volcengine.com/ark → API Key 管理 创建
      - name: DOUBAO_VISION_20P_ID
        required: true
        description: Doubao-Seed-2.0-Pro 接入点 ID，在 console.volcengine.com/ark → 在线推理 获取
      - name: DOUBAO_VISION_20C_ID
        required: true
        description: Doubao-Seed-2.0-Code 接入点 ID
      - name: DOUBAO_VISION_20L_ID
        required: true
        description: Doubao-Seed-2.0-Lite 接入点 ID
      - name: DOUBAO_VISION_16V_ID
        required: true
        description: Doubao-Seed-1.6-Vision 接入点 ID
      - name: DOUBAO_VISION_18_ID
        required: true
        description: Doubao-Seed-1.8 接入点 ID
      - name: DOUBAO_VISION_10C_ID
        required: true
        description: Doubao-Seed-Code 接入点 ID
      - name: VOLCENGINE_ACCESS_KEY
        required: false
        description: 火山 IAM Access Key，在 console.volcengine.com/iam 创建，用于自动同步用量
      - name: VOLCENGINE_SECRET_KEY
        required: false
        description: 火山 IAM Secret Key，与 ACCESS_KEY 配套
    emoji: "🔍"
    homepage: https://www.volcengine.com/docs/82379/1569618
---

# ByteDance Visual Recognition — 豆包 Doubao-Seed 图片视频识别

调用火山方舟 Doubao-Seed [API 文档](https://www.volcengine.com/docs/82379/1569618) 识别图片/视频，自动选择模型并限制用量。参与火山协作奖励计划免费使用顶级多模态模型。

> ⚠️ **配置只需一次！** 如果 `.env` 文件已存在且包含 `ARK_API_KEY` 和 6 个模型 ID，说明已配置过，**直接跳到"调用方式"执行命令，不要重新配置。**

## 🚀 首次配置

### 1. 获取 API Key

1. 打开 https://console.volcengine.com/ark 注册/登录
2. 左侧菜单 → **API Key 管理** → 创建 API Key → 复制保存

### 2. 创建模型接入点

在同一个控制台，左侧菜单 → **在线推理** → 创建推理接入点，选以下 6 个模型：

| 环境变量名 | 模型 | 说明 |
|-----------|------|------|
| `DOUBAO_VISION_20P_ID` | Doubao-Seed-2.0-Pro | 主力模型，所有模式优先 |
| `DOUBAO_VISION_20C_ID` | Doubao-Seed-2.0-Code | 代码模式优先 |
| `DOUBAO_VISION_20L_ID` | Doubao-Seed-2.0-Lite | 轻量备选 |
| `DOUBAO_VISION_16V_ID` | Doubao-Seed-1.6-Vision | 视觉专用 |
| `DOUBAO_VISION_18_ID` | Doubao-Seed-1.8 | 通用备选 |
| `DOUBAO_VISION_10C_ID` | Doubao-Seed-Code | 代码专用 |

每个接入点创建后会得到一个 `ep-xxxxx` 格式的 ID，复制保存。

### 3. 配置 .env 文件

在 Skill 目录下创建 `.env` 文件，填入你的 Key 和接入点 ID：

```bash
ARK_API_KEY=你的API Key
DOUBAO_VISION_20P_ID=ep-xxxxx
DOUBAO_VISION_20C_ID=ep-xxxxx
DOUBAO_VISION_20L_ID=ep-xxxxx
DOUBAO_VISION_16V_ID=ep-xxxxx
DOUBAO_VISION_18_ID=ep-xxxxx
DOUBAO_VISION_10C_ID=ep-xxxxx
```

> 可选：加上 IAM 密钥可自动同步控制台用量
> ```bash
> VOLCENGINE_ACCESS_KEY=你的Access Key
> VOLCENGINE_SECRET_KEY=你的Secret Key
> ```

### 4. 测试

```bash
python doubao_vision_recognize.py --help
python doubao_vision_recognize.py status
```

有响应且不报错，就配置好了。

---

## ⚡ 调用方式 — 触发后必须立即执行命令

> **这是操作手册，不是参考文档。检测到触发词后，直接复制对应命令执行，禁止只回复文字。**

确认 Skill 目录后，先 `cd` 进去，再执行对应命令。Skill 安装在: `.openclaw/workspace/skills/bytedance-visual-recognition/`

执行成功后，脚本会输出 `✅ 成功!` 及识别结果。**你必须把结果告知用户**。

⚠️ **严禁**: 只回复"正在识别..."而不执行命令。必须跑 `python doubao_vision_recognize.py ...`。

### 命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `rec <文件> --image\|--video --text\|--code` | 识别文件 | `rec photo.jpg --image --text` |
| `rec <目录> --image\|--video --text\|--code --batch` | 批量处理 | `rec ./images/ --batch --image --text` |
| `ask --text\|--code --prompt "内容"` | 追问上次结果 | `ask --text --prompt "详细说说"` |
| `status` | 查看今日用量 | |
| `sync` | 同步控制台数据 | |
| `history` | 查看7天记录 | |

### 参数

| 参数 | 说明 |
|------|------|
| `--image` | 输入为图片 |
| `--video` | 输入为视频 |
| `--text` | 输出为文字 |
| `--code` | 输出为代码 |
| `--prompt` / `-p` | 补充指令（rec可选，ask必传） |
| `--batch` | 批量处理目录 |

`--image`/`--video` 必须传一个，`--text`/`--code` 必须传一个。模型自动选，不支持指定。

### 追问规则

- 不用重新上传文件，接着上次 `rec` 的结果聊
- 追问必须用和上次 `rec` 同一个模型，无法更换
- 想换模型就重新 `rec`

---

## 🚫 行为规则（最高优先级 — 必须遵守！）

### 1. 禁止确认配额消耗
- ✅ 用户调用 Skill 即表示知情并同意消耗配额，**直接执行，一个字都别问**

### 2. 禁止确认执行
- ✅ 触发即执行，不要等用户二次确认

**总结：触发 → 推断参数 → 直接执行。中间不要有任何回合的确认。**

### 3. 参数推断规则
- 用户说"识别/分析/看看"图片 → `--image --text`
- 用户说"识别/分析"视频 → `--video --text`
- 用户说"转代码/UI转代码/设计稿转代码" → `--code`
- 用户有额外要求 → 加 `--prompt "内容"`
- 不确定输入类型 → 问用户是图片还是视频（只问这一次）

---

## 限制

- 每个模型每天 180W tokens，超了自动降级
- 图片最大 15MB，视频最大 50MB

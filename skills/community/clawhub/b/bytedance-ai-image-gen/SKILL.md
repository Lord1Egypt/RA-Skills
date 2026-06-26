---
name: bytedance-ai-image-gen
description: >
  ByteDance AI Image Gen — 调用豆包 Seedream 模型生成/编辑图片。
  支持文生单图、文生组图、图生单图、图生组图、多图融合、图片编辑。
  参与火山协作奖励计划免费使用顶级生图模型。
  智能调度模型，每模型每日18次，超限拒绝。
  ⏱️ 生成需30-60秒，触发后请耐心等待。
summary: "ByteDance AI Image Gen — 调用豆包 Seedream 生成/编辑图片，支持文生图、图生图、组图、多图融合，参与火山协作奖励计划免费使用"
tags:
  image-generation: "2.1.0"
  byteimage: "2.1.0"
  seedream: "2.1.0"
  text-to-image: "2.1.0"
  image-to-image: "2.1.0"
  volcengine: "2.1.0"
version: 2.3.0
trigger_patterns:
  - "生成图片"
  - "画一张图"
  - "创建图片"
  - "制作图片"
  - "画图"
  - "帮我画"
  - "帮我生成"
  - "我想生成"
  - "搞个图"
  - "来张图"
  - "做张图"
  - "generate image"
  - "create image"
  - "txt2img"
  - "please generate"
  - "please draw"
  - "图生图"
  - "图片编辑"
  - "编辑图片"
  - "改图"
  - "换背景"
  - "换风格"
  - "img2img"
  - "image to image"
  - "edit this image"
  - "edit image"
  - "融合"
  - "合成"
  - "两张图片"
  - "多张图片"
  - "拼合"
  - "合图"
  - "blend"
  - "fuse"
  - "merge"
  - "combine"
  - "文生图"
  - "生图"
  - "图片生成"
  - "图像生成"
  - "生成图像"
metadata:
  openclaw:
    requires:
      bins:
        - python
      env:
        - ARK_API_KEY
        - DOUBAO_MODEL_45_ID
        - DOUBAO_MODEL_50L_ID
        - DOUBAO_MODEL_40_ID
    primaryEnv: ARK_API_KEY
    envVars:
      - name: ARK_API_KEY
        required: true
        description: 火山方舟 API Key，在 console.volcengine.com/ark → API Key 管理 创建
      - name: DOUBAO_MODEL_45_ID
        required: true
        description: Seedream-4.5 接入点 ID，在 console.volcengine.com/ark → 在线推理 获取
      - name: DOUBAO_MODEL_50L_ID
        required: true
        description: Seedream-5.0-Lite 接入点 ID
      - name: DOUBAO_MODEL_40_ID
        required: true
        description: Seedream-4.0 接入点 ID
      - name: VOLCENGINE_ACCESS_KEY
        required: false
        description: 火山 IAM Access Key，在 console.volcengine.com/iam 创建，用于自动同步用量
      - name: VOLCENGINE_SECRET_KEY
        required: false
        description: 火山 IAM Secret Key，与 ACCESS_KEY 配套
    emoji: "🎨"
    homepage: https://www.volcengine.com/docs/82379/1541523
    install:
      - kind: uv
        package: requests
---

# ByteDance AI Image Gen — 豆包 Seedream 图片生成

调用火山方舟 Seedream [API 文档](https://www.volcengine.com/docs/82379/1541523?lang=zh) 生成/编辑图片，自动选择模型并限制用量。参与火山协作奖励计划免费使用顶级生图模型。

> ⚠️ **配置只需一次！** 如果 `.env` 文件已存在且包含 `ARK_API_KEY` 和 3 个模型 ID，说明已配置过，**直接跳到"调用方式"执行命令，不要重新配置。**

## 🚀 首次配置

### 1. 获取 API Key

1. 打开 https://console.volcengine.com/ark 注册/登录
2. 左侧菜单 → **API Key 管理** → 创建 API Key → 复制保存

### 2. 创建模型接入点

在同一个控制台，左侧菜单 → **在线推理** → 创建推理接入点，选以下 3 个模型：

| 环境变量名 | 模型 | 说明 |
|-----------|------|------|
| `DOUBAO_MODEL_45_ID` | Seedream-4.5 | 主力模型，所有模式优先 |
| `DOUBAO_MODEL_50L_ID` | Seedream-5.0-Lite | 轻量备选 |
| `DOUBAO_MODEL_40_ID` | Seedream-4.0 | 仅支持文生图 |

每个接入点创建后会得到一个 `ep-xxxxx` 格式的 ID，复制保存。

### 3. 配置 .env 文件

在 Skill 目录下创建 `.env` 文件，填入你的 Key 和接入点 ID：

```bash
ARK_API_KEY=你的API Key
DOUBAO_MODEL_45_ID=ep-xxxxx
DOUBAO_MODEL_50L_ID=ep-xxxxx
DOUBAO_MODEL_40_ID=ep-xxxxx
```

> 可选：加上 IAM 密钥可自动同步控制台用量
> ```bash
> VOLCENGINE_ACCESS_KEY=你的Access Key
> VOLCENGINE_SECRET_KEY=你的Secret Key
> ```

### 4. 测试

```bash
python doubao_image_gen.py --help
```

不报错，就配置好了。

---

## ⚡ 调用方式 — 触发后必须立即执行命令

> **这是操作手册，不是参考文档。检测到触发词后，直接复制对应命令执行，禁止只回复文字。**

确认 Skill 目录后，先 `cd` 进去，再执行对应命令。Skill 安装在: `.openclaw/workspace/skills/bytedance-ai-image-gen/`

执行成功后，脚本会输出 `✅ 生成成功!` 及本地文件路径。**你必须把文件路径告知用户**。

⚠️ **严禁**: 只回复"正在生成..."而不执行命令。必须跑 `python doubao_image_gen.py ...`。

### 命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `gen "描述" [尺寸] [--ratio 比例]` | 文生图 | `gen "洪崖洞夜景" 4K --ratio 16:9` |
| `img2img "描述" "图片" [尺寸]` | 图生图 | `img2img "换成夜景" "photo.jpg" 4K` |
| `seq "描述" [--num 数量]` | 组图 | `seq "猫咪" --num 3` |
| `seq "描述" --refs img1 img2` | 多图融合 | `seq "融合" --refs a.jpg b.jpg` |
| `sync` | 同步控制台用量 | |

### 参数

| 参数 | 说明 |
|------|------|
| `尺寸` | `3K`(默认) / `4K`(高清) / 自定义 |
| `--ratio` | `16:9`(宽屏) / `9:16`(竖屏) / `21:9`(电影) |
| `--no-watermark` | 去水印 |
| `--num` | 组图数量 |

### 尺寸推断规则

- 没提画质 → `3K`
- 说"4K/高清/超清" → `4K`
- 说"16:9/宽屏" → `3K --ratio 16:9`
- 说"9:16/竖屏" → `3K --ratio 9:16`
- 说"21:9/电影" → `4K --ratio 21:9`
- 图生图 → 自动检测参考图分辨率

### 模型选择

- 自动降级: 4.5 → 5.0Lite → 4.0，每模型日限 18 次
- 用户可指定简称: `4.5` / `5l` / `4.0`
- 4.0 仅支持文生图，其他模式自动降级

### 水印

- 默认带水印，`.env` 设 `DEFAULT_WATERMARK=false` 永久关闭
- 单次覆盖: `--no-watermark`

---

## 🚫 行为规则（最高优先级 — 必须遵守！）

### 1. 禁止确认配额消耗
- ✅ 用户调用 Skill 即表示知情并同意消耗配额，**直接执行，一个字都别问**

### 2. 禁止确认执行
- ✅ 触发即执行，不要等用户二次确认

**总结：触发 → 推断参数 → 直接执行。中间不要有任何回合的确认。**

### 3. 参数推断规则
- 用户说"生成/画/创建"图片 → `gen`
- 用户说"编辑/改/换风格"图片 → `img2img`
- 用户说"融合/合成"多图 → `seq --refs`
- 用户有额外要求 → 加到描述里

---

## 限制

- 每个模型每天 18 次，超了自动换下一个
- 4.0 仅支持文生图
- 多图融合参考图 base64 后不能超过 ~15MB
- 组图上限 15 张

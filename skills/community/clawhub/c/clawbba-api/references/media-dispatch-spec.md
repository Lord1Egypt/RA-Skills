# ClawBBA 媒体调度规范（Media Dispatch Spec）

> **模型 id 规范（先看）：** [`media-model-ref.md`](media-model-ref.md)  
> 用户写 `模型 black-forest-labs/flux.2-pro` → tool 必须用 `openrouter/black-forest-labs/flux.2-pro`

与 **OpenClaw 2026.5+** 官方 `image_generate` / `video_generate` 工具 schema 对齐。

## 1. 为什么必须结构化调度

OpenClaw 生图走 `POST /chat/completions`，生图参数来自 **工具参数字段**，不是 prompt 里的自然语言：

| OpenClaw 工具参数 | ClawBBA API 字段 | 仅写在 prompt 里 |
|-------------------|------------------|------------------|
| `model` | `body.model` | ❌ 仍用 setup 默认（多为 gemini） |
| `aspectRatio` | `image_config.aspect_ratio` | ❌ 服务端可能默认 `1:1` 或由模型自由发挥（易出现 9:16 竖图） |
| `resolution` | `image_config.image_size` | ❌ 忽略 |
| `duration` | `duration` / `duration_sec` | ❌ 忽略 |
| `aspectRatio`（视频） | `aspect_ratio` | ❌ 忽略 |

**典型故障（你遇到的情况）：**

```
用户：模型 black-forest-labs/flux.2-pro，16:9 横图
Agent：image_generate({ prompt: "…16:9 横图…" })  // 未传 model、aspectRatio
结果：计费 google/gemini-3.1-flash-image-preview，输出 ~768×1376（9:16）
```

## 2. 调度流程（Agent + 服务端）

```
用户 ClawBBA 话术
    ↓
Agent 解析 → image_generate / video_generate 结构化参数（§3）
    ↓
OpenClaw → ClawBBA Platform API
    ↓
服务端 media-intent-extract（defense-in-depth：从 messages/prompt 再解析一次）
    ↓
normalizeImageChatCompletionBody / normalizeVideoGenerationBody
    ↓
上游 OpenRouter 兼容 API
```

Agent **必须**传工具参数；服务端提取是 **兜底**，不能替代 Agent 规范。

### 1.1 `prompt` 与用户原意（v2 强制）

`prompt` 字段承载 **用户在本轮对话中的画面/修改意图**，不是对话模型自由发挥的创意文案：

- **必须**：产品名、主体、风格、场景、相对参考图要改什么（用户原话可译英）
- **禁止**：与用户无关的通用英文套话；有参考图就忽略用户文字
- **允许**：译英、补充用户已暗示的光影/构图；用户含糊时 **先追问** 再生成

示例（图生图）：

```
用户：按这张可乐罐参考图，做白底 45° 电商主图，水珠明显
工具：image_generate({
  image: "~/.openclaw/media/inbound/….png",
  aspectRatio: "1:1",
  prompt: "E-commerce product photo: keep Coca-Cola can from reference, 45° angle, clean white background, visible condensation droplets, professional studio lighting"
})
```

## 3. 用户话术 → 工具参数

### 3.1 生图 `image_generate`

**用户模板：**

```
请使用 ClawBBA 生成图片能力，模型 {model_id}，为我生成 {ratio} {optional_resolution}：（画面描述）
```

**Agent 必须调用：**

```javascript
image_generate({
  model: "openrouter/black-forest-labs/flux.2-pro",   // 用户写了 模型 … 时必填；推荐 openrouter/ 前缀
  aspectRatio: "16:9",                     // 用户写了 16:9 / 横图 时必填
  resolution: "2K",                        // 用户写了 2K/4K 时
  prompt: "性感的韩国女性，皮肤白皙，爱笑，房间内灯光，展示身材",  // 仅画面描述
})
```

| 用户说法 | `aspectRatio` | 备注 |
|----------|---------------|------|
| `16:9`、`16：9` | `"16:9"` | 中英文冒号均可 |
| `9:16`、`9：16` | `"9:16"` | |
| `横图`、`横屏`、`landscape` | `"16:9"` | 无数字时 |
| `竖图`、`竖屏`、`portrait` | `"9:16"` | |
| `2K` / `4K` / `1K` | — | 用 `resolution: "2K"` 等 |

| 用户说法 | `model` |
|----------|---------|
| `模型 black-forest-labs/flux.2-pro` | `openrouter/black-forest-labs/flux.2-pro`（或 bare id + model-ref patch） |
| `FLUX.2 Pro` | `openrouter/black-forest-labs/flux.2-pro` |
| `Nano Banana 2` | `openrouter/google/gemini-3.1-flash-image-preview` |

**禁止：** `model: "clawbba/…"`。Bare `vendor/model` 仅在有 `clawbba-openrouter-vendor-id` patch 时可用；否则必须用 `openrouter/` 前缀。

### 3.1.1 参考图 / 图生图（OpenClaw 官方 `image` / `images`）

WebChat 上传的图片会进入 **对话 vision 上下文**，但 **不会**自动作为生图 API 的参考图。必须写入工具参数（与 OpenClaw `ImageGenerateToolSchema` 一致）：

| 用户行为 | Agent / 工具 |
|----------|----------------|
| 上传 1 张参考图 + ClawBBA 生图话术 | `image: "/root/.openclaw/media/inbound/…"` 或 `images: ["…"]` |
| 多张参考图 | `images: ["path1", "path2"]`（数量 ≤ 模型 `max_reference_images`，OpenRouter 通道通常 ≤5） |
| 话术含「参考图 / 图生图 / 按上传的图」但未传 `image`/`images` | **错误** — 只会文生图 |

**OpenClaw 接受的引用格式：** 本机绝对路径、`~/.openclaw/media/…`、`file://`、`data:image/…;base64,…`、可访问的 `https://` 图片 URL。

**Agent 必须调用示例：**

```javascript
image_generate({
  model: "openrouter/black-forest-labs/flux.2-pro",
  aspectRatio: "16:9",
  images: ["/root/.openclaw/media/inbound/your-upload.png"],
  prompt: "按参考图风格，保留构图，画面：…",
})
```

**clawbba-api v1.5.6+ runtime patch**（`clawbba-reference-images`）在 Agent 漏传 `image`/`images` 时，从**同一条** ClawBBA 用户消息（及必要时前 3 条用户消息）解析附件路径并写入 `params`，再交给 `normalizeReferenceImages` → `loadReferenceImages` → `messages[].content[].image_url`。

**模型能力：** 须支持 edit / `supports_image_input`（Flux、Gemini 生图、Seedream 等）。不支持时会报 `does not support reference-image edits` — 换模型或去掉 `images`。

### 3.2 生视频 `video_generate`

**用户模板：**

```
请使用 ClawBBA 生成视频能力，模型 {model_id}，为我生成 {ratio}、{N} 秒视频：（画面描述）
```

**Agent 必须调用：**

```javascript
video_generate({
  model: "google/veo-3.1-fast",
  aspectRatio: "16:9",
  duration: 8,
  resolution: "720p",      // 可选
  audio: true,             // 用户说 带音频
  prompt: "海边日落",
})
```

| 用户说法 | 工具参数 |
|----------|----------|
| `16:9` / `横图` | `aspectRatio: "16:9"` |
| `9:16` / `竖图` | `aspectRatio: "9:16"` |
| `8 秒`、`5秒` | `duration: 8` |
| `720p` / `1080p` | `resolution: "720p"` |
| `带音频` / `不要音频` | `audio: true` / `false` |

ClawBBA API 字段：`aspect_ratio`、`duration`、`duration_sec`、`generate_audio`。

### 3.2.1 视频参考图（`image` / `images` + `imageRoles`）

| 用户说法 | 工具参数 |
|----------|----------|
| 图生视频 / 首帧 | `image` + `imageRoles: ["first_frame"]` |
| 尾帧 | `image` + `imageRoles: ["last_frame"]` |
| 风格参考 | `images` + `imageRoles: ["reference_image", …]` |

v1.5.6+ 与 §3.1.1 相同：从 WebChat 会话附件自动补全 `args.image` / `args.images`（在 `normalizeReferenceInputs` 之前）。

## 4. OpenClaw 官方对照

来源：`openclaw-tools` → `ImageGenerateToolSchema` / `VideoGenerateToolSchema`

- 生图 `aspectRatio` 枚举含：`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`
- 工具内 `model` → provider `openrouter/<id>` → ClawBBA `POST /chat/completions`
- 默认模型：`agents.defaults.imageGenerationModel.primary`（setup 写入）

## 5. OpenClaw Runtime Patch（v1.2.3+，必装）

`patch-openclaw-media-delivery.mjs` 除交付 patch 外，还注入 **媒体调度 runtime**：

| Patch | 作用 |
|-------|------|
| `image_generate` session 解析 | 从 WebChat 最近用户消息读取 `模型 …` / `16:9 横图`，写入 tool 的 `model` / `aspectRatio` |
| `image_generate` / `video_generate` 参考图 | 从同条 ClawBBA 用户消息（及近邻用户消息）解析附件路径 → `image` / `images`（及视频 `imageRoles`） |
| `video_generate` session 解析 | 同上 + `N 秒` → `durationSeconds` |
| OpenRouter `buildImageConfig` | **Flux 等非 Gemini** 也发送 `image_config.aspect_ratio`（官方默认仅 Gemini 写入，导致 Flux 横图变竖图） |
| OpenRouter `postJsonRequest` | 生图 POST 必须带 **`Content-Type: application/json`**，否则 ClawBBA Platform API 的 `express.json()` 不解析 body → 误报「缺少 model」 |

未打此 patch 时，Agent 漏传参数 → OpenClaw HTTP 请求只有 gemini 默认 + 无 aspect；或未带 Content-Type → 服务端看不到 `model` 字段。

## 6. 服务端兜底（ClawBBA Platform API — 次要）

OpenClaw 侧必须按 §7 正确传 `model` / `aspectRatio`；Platform API **只做**：

1. **归一化**：`aspectRatio` → `image_config.aspect_ratio`（`normalizeImageChatCompletionBody`）
2. **从 HTTP body 的 messages/prompt 二次解析**（`applyMediaIntentToImageBody`）— 仅当请求已是生图且 body 里带 ClawBBA 话术
3. **同进程 companion**：若同一次任务先收到完整 body、后收到 undici 空 `{}`，从**内存**恢复（45–120s TTL）

Platform API **禁止**：

- 从 `openrouter_agent_image_jobs` 历史记录猜模型
- 对 undici 空 body **注入** 默认 gemini

**必须**兼容 OpenClaw provider：`postJsonRequest` 未带 `Content-Type: application/json` 时，代理层用 `parseOpenClawProviderJsonBody` 手动解析 JSON（wire 上 body 含 `model`，不是真 `{}`）。

缺 model 时应 preflight 失败，并提示 `verify-openclaw-patch.mjs`。

## 7. 部署与验证

```bash
# 用户机 OpenClaw skill
export CLAWBBA_API_KEY='cbb_sk_live_…'
./scripts/setup.sh --yes          # 刷新 systemPrompt 调度规则
node scripts/patch-openclaw-media-delivery.mjs
node scripts/verify-openclaw-patch.mjs
openclaw gateway restart
```

**验证生图：** 发送你的原话术后，后台应显示 `black-forest-labs/flux.2-pro`，图片宽高比接近 16:9（非 768×1376 竖图）。

**验证模型真相：** 以 Child result `Generated … with openrouter/<id>` 为准，勿口头编造 flux。

## 7. 相关文档

- `references/openclaw-integration-spec.md` — 架构与交付
- `references/clawbba-media-models.md` — 模型 id 与友好名
- `scripts/clawbba-media-dispatch-rules.mjs` — 写入 Agent systemPrompt 的规则块

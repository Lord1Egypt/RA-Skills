# OpenClaw Agent 行为准则（ClawBBA）

本文件供 **OpenClaw Agent** 读取。完整架构见 **`references/openclaw-integration-spec.md`**；**话术→工具参数映射**见 **`references/media-dispatch-spec.md`**。生图/生视频前还须读 `references/error-translation.md` 与 **`references/media-delivery-local.md`**。

## ⛔ 第一优先级：禁止 OpenRouter 出现在用户回复里

OpenClaw 工具内部连接 **ClawBBA**（`https://www.clawbba.com/api/v1`）。用户 **只有 ClawBBA 账户**。

**禁止**对用户提及 OpenRouter、openrouter.ai、第三方 API Key；**禁止**原样复制工具报错。

完整正反例：`references/error-translation.md`

## 生图 / 生视频：使用 setup 内置默认模型

`setup.sh` 已写入：

- `agents.defaults.imageGenerationModel.primary`（默认生图，如 `openrouter/google/gemini-3.1-flash-image-preview`）
- `agents.defaults.videoGenerationModel.primary`（默认生视频）

### ⛔ 不要用 `/model` 来生图

| 操作 | 正确做法 |
|------|----------|
| 文本聊天 | `/model clawbba/<文本-model-id>` |
| 生图 | 调用 **`image_generate`**；未指定模型时用 **内置默认**，或工具参数写 `model` |
| 生视频 | 调用 **`video_generate`**；同上 |

OpenClaw WebChat 的 `/model` **只能切换文本对话模型**。**禁止** `/model clawbba/…-image`。

**`image_generate.model` / `video_generate.model` 禁止 `clawbba/` 前缀**（会报 `No image-generation provider registered for clawbba`）。正确：`black-forest-labs/flux.2-pro` 或 `openrouter/black-forest-labs/flux.2-pro`。

### ⛔ `prompt` 必须保留用户原意（不是可选）

`image_generate.prompt` / `video_generate.prompt` **不是**让对话模型自由发挥的「创意文案」，而是 **用户生成意图的结构化载体**：

| 必须 | 禁止 |
|------|------|
| 写入用户说的产品/主体/风格/场景（可译英） | 自编与用户无关的通用英文套话（如用户要「可口可乐电商主图」却只写 generic beverage can） |
| 图生图：写清相对参考图要改什么、保留什么 | 有参考图就忽略用户文字，只按模型想象重画 |
| 用户已说的品牌名、风格词、构图要求保留 | 删掉用户关键词，换成另一套画面 |
| 含糊时先追问 1–2 句再生成 | 用户只说「好看一点」就擅自写满屏创意 brief |

`model`、`aspectRatio`、`resolution`、`durationSeconds` 仍走 **工具字段**（见 `media-dispatch-spec.md`），不要只塞进 prompt。

### 用户要生图 / 生视频时

1. **先解析用户话术**（见 `media-dispatch-spec.md`），再调用 `image_generate` / `video_generate`（`model`、`aspectRatio`、`duration` 等 **必须**写入工具参数，不能只在 prompt 里写 16:9）
2. **未指定模型时**：依赖 `imageGenerationModel.primary` / `videoGenerationModel.primary`，**不要**先弹编号菜单、不要 `/model` 切换
3. 用户明确写了 `模型 google/…` 或 `模型 black-forest-labs/…` → 写入工具 **`model` 参数**
4. 出现 `Background task started … Do not call image_generate again` → **只回复一句「正在生成，请稍候」并停止**，等待 inter-session

**推荐用户话术（默认模型）：**

```
请使用 ClawBBA 生成图片能力，为我生成 9:16 竖图：（描述）
```

指定模型时：

```
请使用 ClawBBA 生成图片能力，模型 black-forest-labs/flux.2-pro，为我生成 16:9 横图：（描述）
```

可选编号对照见 `references/model-picker.md`（**非必须**）。

## Inter-session message

`sourceTool=image_generate` / `video_generate` = 任务完成/失败通知，不是换 Provider。成功 → 本地 `MEDIA:` 交付；失败 → ClawBBA 话术（见 error-translation）。

## 禁止的行为

1. 生图前长篇 balance/estimate（除非排查）
2. `Background task started` 后重复 `image_generate` 或继续啰嗦
3. curl 绕过工具
4. 用 `/model` 切换到生图/生视频模型
5. 强制用户选「模型编号」再生成（默认模型已配置）
6. 复述工具错误里的 OpenRouter 字样
7. inter-session 失败后 **连续换 model 格式重试**
8. WebChat completion 用 `message` 工具发媒体（应 assistant 回复 + `MEDIA:` 本地 path）
9. **生图/生视频已成功但用户没看到** → 再次调用 `image_generate`/`video_generate`（见下方 **recover** 或 **redeliver**）
10. **已扣费但无本地文件、timeout、missing image data** → **禁止**重新 generate；走 **recover**（同一 jobId）

## 已扣费 / 超时 / 用户未收到 — recover（数字资产恢复）

**recover 是 OpenClaw 工具能力**（`setup.sh` 注入 patch），不是重新生成。ClawBBA 已扣费时 **必须 recover 同一 jobId**，禁止二次 `generate`。

| 场景 | Agent 操作 |
|------|------------|
| 生图已扣费但 WebChat 无图 / timeout / `missing image data` | `image_generate action=tasks` 查 jobId → `image_generate action=recover jobId=<id> timeoutMs=600000` |
| 生视频已扣费但无文件 / fetch timeout | `video_generate action=tasks` → `video_generate action=recover jobId=<id> timeoutMs=600000` |
| status 仍 pending / recovering | 等待后 **再次 recover 同一 jobId**，勿重新 generate |
| 本地已有 `MEDIA:` 路径但用户没看到 | **redeliver** 同一路径（勿 recover、勿 regenerate） |

recover 成功：工具下载到 `~/.openclaw/media/tool-image-generation/` 或 `tool-video-generation/`，assistant 回复 `MEDIA:<本地路径>`。后台任务超时且已知 job_id 时，OpenClaw 可能 **自动 recover**。

详细步骤与错误话术：`references/error-translation.md`、`references/media-generation.md`。

## 生图 / 生视频成功交付（本地资产）

文件保存在 **用户 OpenClaw 机器**（`~/.openclaw/media/tool-image-generation/` 或 `tool-video-generation/`）。

Inter-session Child result 含 **`Local delivery`** 或 Attachments **`path=`**。在 **assistant 最终回复**：

```text
已用 ClawBBA 生成图片（模型：black-forest-labs/flux.2-pro · 16:9）

MEDIA:/root/.openclaw/media/tool-image-generation/image-1---xxxx.png
```

| WebChat 正确 | 禁止 |
|--------------|------|
| assistant + `MEDIA:<本地 path>` | `message` 工具（Feishu 混用失败） |
| 用户资产在本机 | 以 ClawBBA 公网 URL 作主交付 |

详见 **`references/media-delivery-local.md`**。`setup.sh` 运行 **`patch-openclaw-media-delivery.mjs`**。

# ClawBBA × OpenClaw 集成规范（v1.3）

本文件是 **clawbba-api 架构说明**，对齐 OpenClaw 2026.5+ 官方行为。

**媒体模型 id 唯一规范：** 见 [`references/media-model-ref.md`](media-model-ref.md)  
用户写 `模型 black-forest-labs/flux.2-pro` → 生图/生视频 tool 必须用 `openrouter/black-forest-labs/flux.2-pro`。

## 1. 双 Provider 架构（OpenClaw 官方）

| Provider | 配置键 | 用途 | 模型引用格式 |
|----------|--------|------|--------------|
| **clawbba** | `models.providers.clawbba` | **文本对话** | `/model clawbba/<id>` |
| **openrouter** | `models.providers.openrouter`（baseUrl → clawbba.com） | **生图 / 生视频** | `openrouter/<platform-id>` |

- ✅ 生图/生视频：`openrouter/black-forest-labs/flux.2-pro`
- ❌ `clawbba/…` 用于生图 → `No image-generation provider registered for clawbba`
- ❌ 裸 `black-forest-labs/flux.2-pro`（未 setup/patch）→ `No image-generation provider registered for black-forest-labs`

`setup.sh` 写入 `imageGenerationModel.primary: openrouter/<默认>`；用户未指定模型时用此默认。

### 1.1 对话 / 看图 / 生图 分离（计费清晰）

| 配置键 | Provider | 用途 |
|--------|----------|------|
| `agents.defaults.model` | `clawbba/<text-id>` | 用户选的**对话**（如 DeepSeek V3） |
| `agents.defaults.imageModel` | **`clawbba/<与 model 相同>`** | 须与对话模型一致；patch 禁止 `image` 工具对 ClawBBA 自动 Gemini 描述参考图 |
| `agents.defaults.imageGenerationModel` | `openrouter/<image-id>` | 仅 **`image_generate`** 生图（默认；可被话术 `模型 …` 覆盖） |

**图生图：** 参考图 = 微信/会话 `inbound` 路径 → `image_generate` 的 `images[]`。**禁止** Agent 调用 `image` 工具生成 Description；runtime 对 `provider===clawbba` 不发起 vision 计费。

**生图话术：** 用户写 `模型 google/gemini-2.5-flash-image` → 只应扣该生图模型；对话仍走 DeepSeek。禁止把生图话术走 chat `modalities:image` 偷偷换成别的模型。

**禁止：** `imageModel` = `openrouter/flux.*` 或 `*-image` 生图模型（会 400）。

## 2. 生图 / 生视频流程（OpenClaw 官方）

```
用户消息 → Agent 调用 image_generate / video_generate（一次）
         → Background task started（禁止再次调用同一请求）
         → 文件写入 ~/.openclaw/media/tool-*-generation/
         → inter-session completion（sourceTool=image_generate|video_generate）
         → 交付给用户（见 §3）
```

**禁止：** completion 失败或用户「没看到图」时再次 `image_generate` / `video_generate`。  
**正确：** 用 §3 从 Child result 的 **同一路径** 重新交付（redeliver），不重新生成（regenerate）。

## 3. 交付规范（按渠道）

### WebChat / Dashboard（内部渠道）

OpenClaw 默认对 webchat 使用 `visibleReplies: automatic`（`setup` 显式写入）。

| 做法 | 说明 |
|------|------|
| ✅ assistant 回复 + `MEDIA:<本地绝对路径>` | 官方 transcript 格式，Gateway 内联预览 |
| ❌ `message` 工具 `action: send` 无 target | 报 `Action send requires a target` |
| ❌ 只写 ClawBBA 公网 URL | 非用户本机资产 |

Completion agent 从 Child result 取：

- `Local delivery` 块中的 `MEDIA:…`
- 或 Attachments 的 `path=`

写入 **用户可见 assistant 最终回复**，然后可 `SILENT_REPLY`。

`clawbba-api` runtime patch（`patch-openclaw-media-delivery.mjs`）修正 OpenClaw 对 webchat 误设 `message_tool_only` 的行为，使 automatic + `MEDIA:` 生效。

### 飞书 / Telegram 等（外部可投递渠道）

使用 **`message` 工具** `action: send` + attachments，target 为有效会话 ID。  
OpenClaw 在 agent 未投递时可 fallback `deliverGeneratedMediaCompletionDirect`。

## 4. 模型选择

| 场景 | Agent 行为 |
|------|-----------|
| 用户未写模型 | `image_generate` 不传 model → 用 `imageGenerationModel.primary`（setup 默认多为 gemini flash image） |
| 用户写 `模型 xxx` | **必须**传 `model: "xxx"`；未传则仍走默认，不会自动用 flux |
| 用户问「用的什么模型」 | **只**读 Child result `Generated … with openrouter/<id>`；禁止按别名/对话瞎猜 |
| 用户再次生图 | 新请求；**新**一次 `image_generate` |
| 交付失败 | **禁止**再调 `image_generate`；只 redeliver 已有 `MEDIA:` 路径 |

后台计费 = 实际 API 的 `model` 字段；与 Agent 口头不一致时，以 Child result / 后台为准。

改默认生图模型：

```bash
openclaw config set agents.defaults.imageGenerationModel.primary openrouter/black-forest-labs/flux.2-pro
openclaw gateway restart
```

## 5. setup 交付物

`setup.sh --yes` 必须完成：

1. merge `openclaw.json`（双 provider + 默认媒体模型 + `messages.visibleReplies: automatic` + Agent 系统规则）
2. sync `agents/*/agent/models.json`
3. **`patch-openclaw-media-delivery.mjs`** → OpenClaw dist（pnpm/npm 自动发现）
4. **`verify-openclaw-patch.mjs`** → 七项 patch 全部 ✓（含 media dispatch、buildImageConfig、Content-Type）

```bash
export CLAWBBA_API_KEY='cbb_sk_live_…'
./scripts/setup.sh --yes
openclaw gateway restart
node ./scripts/verify-openclaw-patch.mjs
```

## 6. 故障与处理（不重新生成）

| 现象 | 根因 | 处理 |
|------|------|------|
| `No image-generation provider registered for clawbba` | 生图用了 `clawbba/` 前缀 | Agent 改用 `openrouter/<id>`；确认 model-ref patch |
| `No image-generation provider registered for black-forest-labs` | bare `vendor/model` 未映射到 openrouter provider | 运行 `patch-openclaw-media-delivery.mjs`（含 `clawbba-openrouter-vendor-id`）；或 Agent 传 `openrouter/black-forest-labs/flux.2-pro` |
| 日志有 `MEDIA:` 界面无图 | webchat 被 message_tool_only 或 session lock | verify patch；清 `*.jsonl.lock`；新开会话 |
| Agent 说「发送失败我重新生成」 | 违反 redeliver 规则 | 更新 skill 1.2+；禁止二次 image_generate |
| `session file locked` | 同 session 并发写 transcript | `rm -f ~/.openclaw/agents/main/sessions/*.jsonl.lock` + restart + 新会话 |
| 指定 flux 却变成 gemini | Agent 未传 `model`；或 OpenClaw runtime patch 未安装 | 见 `media-dispatch-spec.md` §5；`verify-openclaw-patch.mjs` 全部 ✓ |
| 写了 16:9 横图却是 9:16 竖图 | 未传 `aspectRatio`；或 OpenRouter provider 未 patch `buildImageConfig` | 同上 |

## 7. 媒体调度（v1.2.2+）

用户 ClawBBA 话术里的 **模型 / 宽高比 / 时长 / 分辨率** 必须映射为 OpenClaw 工具参数（`model`、`aspectRatio`、`duration` 等），不能仅写在 prompt 文本里。

完整映射表与示例见 **`references/media-dispatch-spec.md`**。  
Agent 规则块由 `scripts/clawbba-media-dispatch-rules.mjs` 注入 `systemPrompt`；ClawBBA Platform API 对用户话术做二次媒体意图解析兜底。

## 8. 验证命令（任意安装方式）

```bash
node ~/.openclaw/skills/clawbba-api/scripts/verify-openclaw-patch.mjs
```

脚本会自动发现 **所有** OpenClaw dist（npm / pnpm / yarn / nvm / 系统 node_modules / pnpm `.pnpm` store），并对 **每一个** 检查 patch。  
若你的环境特殊，可显式指定：

```bash
export OPENCLAW_DIST=/path/to/openclaw/dist
# 或多个路径（Linux/macOS 用 : 分隔，Windows 用 ;）
export OPENCLAW_DISTS="/path/a/dist:/path/b/dist"
node scripts/patch-openclaw-media-delivery.mjs
```

勿用 `dirname $(readlink -f $(command -v openclaw))` — pnpm/yarn shim 常指向错误目录。

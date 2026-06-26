# Canvas Claw Design

**Date:** 2026-04-07

## Goal

在不修改 `/Users/apple/bangongziliao/hebing/neo-ai-1.0.1` 任何文件的前提下，于 `/Users/apple/bangongziliao/hebing/canvas-claw` 新建一个独立 OpenClaw skill 包。该 skill 采用“方案 A”思路，保留 skill 调用习惯，但底层不再请求 Neodomain，而是通过 HTTP 直接调用 `/Users/apple/bangongziliao/hebing/AI-video-agent` 已暴露的后端 API。

第一期开通 4 个核心生成能力，并把能力名称整理为 AI-video-agent 当前模型体系下更干净的命名：

1. 图片生成
2. 参考图生成
3. 文本生成视频
4. 图片生成视频

## Non-Goals

- 不改动 `neo-ai-1.0.1` 现有脚本、说明文档或发布文件。
- 不在第一期实现 `UNIVERSAL_TO_VIDEO`、`motion_control`、复杂多模态组合视频。
- 不把 `AI-video-agent` 的画布前端嵌入 skill。
- 不直接 import `AI-video-agent` Python 模块，避免本地路径耦合；统一走 HTTP API。

## Chosen Approach

采用“独立 skill 包 + HTTP 客户端适配层”的方式：

- 在 `canvas-claw` 中创建新的 `SKILL.md`、`INSTALL.md`、`scripts/`、`tests/` 和内部 Python 包。
- 继续使用 OpenClaw 可识别的 skill 结构与脚本调用方式。
- 将脚本分成两层：
  - CLI 入口层：负责参数解析和输出格式。
  - 适配层：负责鉴权、模型目录读取、素材上传、任务创建、轮询、结果下载。

这样可以保留 OpenClaw skill 的安装和使用心智，同时把后端能力切换到 `AI-video-agent`。

## Phase 1 Capability Taxonomy

### User-facing names

| 能力名称 | 内部 task type | 默认模型目录键 | 默认 provider/model |
| --- | --- | --- | --- |
| 图片生成 | `text_to_image` | `image-plus` | `vg / qwen-image-2` |
| 参考图生成 | `image_to_image` | `image-multi` | `vg / nano-banana-2` |
| 文本生成视频 | `text_to_video` | `video-dream-standard` | `vg / seedance-1-5-pro` |
| 图片生成视频 | `image_to_video` | `video-dream-standard` | `vg / seedance-1-5-pro` |

### Naming policy

- 对用户暴露“能力名称 + 模型目录键”的命名，不继续沿用 `TEXT_TO_VIDEO`、`REFERENCE_TO_VIDEO`、`UNIVERSAL_TO_VIDEO` 这类 Neodomain 风格术语。
- 在输出 `metadata.json` 中同时记录：
  - 用户可读能力名
  - `task_type`
  - `catalog_key`
  - `provider`
  - `model_id`

### Initial model policy

- 图片生成默认使用 `image-plus`，因为 `qwen-image-2` 同时支持文生图和单参考图输入，作为通用默认值更稳。
- 参考图生成默认使用 `image-multi`，因为 `nano-banana-2` 更适合作为“多参考图一致性”模式。
- 文本生成视频和图片生成视频默认使用 `video-dream-standard`，因为 `seedance-1-5-pro` 的参数范围与当前后端处理最匹配。
- 如果用户显式指定 `catalog_key`，则按指定键解析；如果后端 `/api/models` 中不存在该键，则报清晰错误。

## API Contract With AI-video-agent

### 1. Login

`POST /api/login`

用途：

- 提供可选的登录辅助脚本 `login.py`
- 让用户用用户名/密码换取 token，而不是使用旧 skill 的短信验证码流程

关键点：

- 请求头必须包含 `site-id`
- 成功返回 `token`、`expires_time`、`site_id`

### 2. Model catalog

`GET /api/models`

用途：

- 读取公开模型目录
- 由 `catalog_key` 反查到 provider/task_type/是否依赖图片输入

限制：

- 当前接口返回公开目录键，不直接返回底层 `model_id`
- skill 侧需要维护一份 `catalog_key -> provider/model_id/task_type/default options` 的本地注册表，作为稳定映射层

### 3. Binary asset materialization

`POST /api/assets/materialize-binary?media_type=image|video&filename=...`

用途：

- 把本地图片或视频文件转换成 `AI-video-agent` 可消费的远程 URL
- 支撑 OpenClaw 用户传本地文件路径

第一期输入策略：

- `http://` / `https://`：直接透传
- 本地文件路径：上传到 `materialize-binary`
- `data:` URL：暂不在 CLI 特意支持，作为后续增强

### 4. Task creation

`POST /api/tasks`

用途：

- 创建 `text_to_image` / `image_to_image` / `text_to_video` / `image_to_video` 任务

请求结构：

- `type`
- `provider`
- `model_id`
- `input.prompt`
- `input.image_urls`
- `input.video_url`
- `options`
- `meta`

### 5. Task polling

`GET /api/tasks/{task_id}`

用途：

- 轮询任务状态
- 读取 `status`、`progress`、`result.result_urls`、`result.primary_url`

状态策略：

- `queued` / `running`：继续轮询
- `succeeded`：下载结果
- `failed`：将 `error.code` / `error.message` 原样映射到 CLI 错误输出

## Proposed Repository Layout

```text
canvas-claw/
├── SKILL.md
├── INSTALL.md
├── pyproject.toml
├── canvas_claw/
│   ├── __init__.py
│   ├── auth.py
│   ├── client.py
│   ├── config.py
│   ├── download.py
│   ├── errors.py
│   ├── media.py
│   ├── model_registry.py
│   ├── output.py
│   └── tasks.py
├── scripts/
│   ├── login.py
│   ├── image_models.py
│   ├── video_models.py
│   ├── generate_image.py
│   └── generate_video.py
└── tests/
    ├── test_auth.py
    ├── test_media.py
    ├── test_model_registry.py
    ├── test_generate_image_cli.py
    ├── test_generate_video_cli.py
    └── test_output.py
```

## Internal Module Design

### `canvas_claw/config.py`

职责：

- 读取环境变量
- 统一默认值

核心环境变量：

- `AI_VIDEO_AGENT_BASE_URL`
- `AI_VIDEO_AGENT_TOKEN`
- `AI_VIDEO_AGENT_SITE_ID`
- `AI_VIDEO_AGENT_TIMEOUT`
- `AI_VIDEO_AGENT_POLL_INTERVAL`

可选环境变量：

- `AI_VIDEO_AGENT_USERNAME`
- `AI_VIDEO_AGENT_PASSWORD`

### `canvas_claw/client.py`

职责：

- 封装带鉴权头的 HTTP 请求
- 提供 `login()`、`list_models()`、`materialize_binary()`、`create_task()`、`get_task()`

统一请求头：

- `token`
- `site-id`
- `Content-Type`

### `canvas_claw/model_registry.py`

职责：

- 保存本地稳定目录键映射
- 根据“能力类型 + 用户指定 catalog_key + 输入形态”选择 provider/model_id

本地映射存在的原因：

- `/api/models` 只返回公开目录键和 task_type，不返回完整默认参数。
- skill 需要稳定的 CLI 体验，不能把所有模型解释逻辑散落在各脚本中。

### `canvas_claw/media.py`

职责：

- 判断输入是 URL 还是本地文件
- 将本地文件上传到 `materialize-binary`
- 输出可直接提交给任务 API 的 URL

### `canvas_claw/tasks.py`

职责：

- 构造 `CreateTaskRequest`
- 执行轮询
- 在任务成功后返回结果 URL 列表和标准化元数据

### `canvas_claw/output.py`

职责：

- 将结果下载到 `./output`
- 写出 `metadata.json`
- 为图片和视频生成稳定的文件名

## CLI Design

### `scripts/login.py`

用途：

- 可选登录辅助工具
- 支持：
  - `--username`
  - `--password`
  - `--site-id`
  - `--base-url`

输出策略：

- 默认打印简明登录结果
- 提供 shell 可复制的 export 建议
- 不默认把 token 落盘，避免隐藏状态

### `scripts/image_models.py`

用途：

- 展示图片能力可选目录键
- 默认只列出与图片能力相关的 `catalog_key`
- 输出包括：
  - `catalog_key`
  - `provider/model_id`
  - 支持能力
  - 默认参数建议

### `scripts/video_models.py`

用途：

- 展示视频能力可选目录键
- 默认只列出与视频能力相关的 `catalog_key`

### `scripts/generate_image.py`

支持两种模式：

- 无参考图：图片生成
- 有参考图：参考图生成

建议参数：

- `--prompt`
- `--model` 或 `--catalog-key`
- `--reference-image` 可多次指定
- `--aspect-ratio`
- `--resolution`
- `--output-dir`

模式切换规则：

- 没有 `--reference-image` 时使用 `text_to_image`
- 有 `--reference-image` 时使用 `image_to_image`

### `scripts/generate_video.py`

支持两种模式：

- 无参考图：文本生成视频
- 有首帧图：图片生成视频

建议参数：

- `--prompt`
- `--model` 或 `--catalog-key`
- `--first-frame`
- `--aspect-ratio`
- `--resolution`
- `--duration`
- `--generate-audio`
- `--output-dir`

模式切换规则：

- 无 `--first-frame` 时使用 `text_to_video`
- 有 `--first-frame` 时使用 `image_to_video`

## Request Mapping Rules

### Image generation

#### 图片生成

```json
{
  "type": "text_to_image",
  "provider": "vg",
  "model_id": "qwen-image-2",
  "input": {
    "prompt": "..."
  },
  "options": {
    "aspect_ratio": "1:1",
    "resolution": "2K"
  },
  "meta": {
    "source": "openclaw",
    "capability": "image-create",
    "catalog_key": "image-plus"
  }
}
```

#### 参考图生成

```json
{
  "type": "image_to_image",
  "provider": "vg",
  "model_id": "nano-banana-2",
  "input": {
    "prompt": "...",
    "image_urls": ["..."]
  },
  "options": {
    "aspect_ratio": "16:9",
    "resolution": "2K"
  },
  "meta": {
    "source": "openclaw",
    "capability": "image-remix",
    "catalog_key": "image-multi"
  }
}
```

### Video generation

#### 文本生成视频

```json
{
  "type": "text_to_video",
  "provider": "vg",
  "model_id": "seedance-1-5-pro",
  "input": {
    "prompt": "..."
  },
  "options": {
    "aspect_ratio": "16:9",
    "resolution": "720p",
    "duration": 8,
    "sound": true
  },
  "meta": {
    "source": "openclaw",
    "capability": "video-create",
    "catalog_key": "video-dream-standard"
  }
}
```

#### 图片生成视频

```json
{
  "type": "image_to_video",
  "provider": "vg",
  "model_id": "seedance-1-5-pro",
  "input": {
    "prompt": "...",
    "image_urls": ["..."]
  },
  "options": {
    "aspect_ratio": "16:9",
    "resolution": "720p",
    "duration": 8,
    "sound": true
  },
  "meta": {
    "source": "openclaw",
    "capability": "video-animate",
    "catalog_key": "video-dream-standard"
  }
}
```

## Output Contract

每次生成都写入输出目录：

- `metadata.json`
- 图片结果：`image_1.jpg`、`image_2.jpg` ...
- 视频结果：`video.mp4`
- 如果有多视频结果：`video_1.mp4`、`video_2.mp4`

`metadata.json` 至少包含：

- `task_id`
- `status`
- `capability`
- `catalog_key`
- `provider`
- `model_id`
- `prompt`
- `result_urls`
- `downloaded_files`
- `updated_at`

## Error Handling

### User errors

- 缺少 token
- 本地文件不存在
- 参考图数量超出当前能力支持上限
- 后端不支持指定 `catalog_key`
- 参数超出已知模型支持范围

策略：

- 直接返回清晰的 CLI 错误
- 不输出 Python traceback，除非用户显式需要调试

### API errors

- `/api/login` 返回 `code != 1`
- `/api/tasks` 返回 4xx/5xx
- `/api/tasks/{id}` 轮询失败
- 下载结果失败

策略：

- 将 HTTP 错误封装成统一异常
- 在命令行输出“接口阶段 + 错误信息”
- 保留 `--debug` 以输出请求上下文

## Testing Strategy

### Unit tests

- 模型目录键映射
- 参数到任务请求体的映射
- 本地文件与 URL 输入识别
- 输出文件名和 `metadata.json` 序列化

### CLI tests

- `generate_image.py` 在有/无参考图时正确切换任务类型
- `generate_video.py` 在有/无首帧时正确切换任务类型
- `image_models.py` / `video_models.py` 只展示目标能力模型

### Optional integration tests

- 在本地 `AI-video-agent` 启动后，用真实环境变量跑一次 smoke test
- 集成测试不作为默认 CI 前提，避免依赖外部服务状态

## Risks And Mitigations

### Risk 1: `/api/models` 公开目录和底层模型真实能力不完全一致

缓解：

- skill 端维护稳定本地注册表
- 每次启动时可以交叉校验 `/api/models` 是否仍暴露目标 `catalog_key`

### Risk 2: 图像或视频素材 URL 无法被后端下游消费

缓解：

- 本地文件统一先走 `materialize-binary`
- 第一阶段对远程 URL 先透传，必要时第二阶段补“远程素材托管化”

### Risk 3: 异步任务耗时长，OpenClaw 侧体验不稳定

缓解：

- 明确轮询间隔、超时时间和进度提示
- 下载前先输出任务编号，便于后续排查

## Phase 2 Backlog

- `batch_video.py`：基于批量图片批次提交图生视频
- `seedance-2-0-i2v` 专门模式：支持 3-4 图参考图生视频
- `seedance-2-0-video-ref`：图片 + 视频参考
- `UNIVERSAL_TO_VIDEO`
- `motion_control`
- 发布到 ClawHub 所需的 `_meta.json` 和发布流程

## Final Recommendation

第一期最稳的做法是：

- 在 `canvas-claw` 中只提供 5 个核心脚本：`login.py`、`image_models.py`、`video_models.py`、`generate_image.py`、`generate_video.py`
- 通过一套清晰的本地模型注册表，把 `AI-video-agent` 当前可用模型能力组织成“图片 / 参考图 / 文本视频 / 图片视频”四种用户能力
- 先把“本地文件上传、任务创建、轮询下载、metadata 输出”四条主链路跑通，再扩展复杂视频能力

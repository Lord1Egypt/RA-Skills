# ClawBBA 媒体生成能力表（v2）

对话模型根据本表收集参数，直接调用 OpenClaw `image_generate` / `video_generate`。**无需固定中文话术。**

**Prompt 原意：** `prompt` 必须承载用户在本轮对话中的生成意图，禁止用大模型自编与用户无关的通用英文描述替代。

默认生图：`google/gemini-3.1-flash-image-preview` → tool `openrouter/google/gemini-3.1-flash-image-preview`
默认生视频：`google/veo-3.1-fast` → tool `openrouter/google/veo-3.1-fast`

## 工作流

### 文生图 (`text_to_image`)
- 工具：`image_generate`
- 必填：`prompt`
- 可选：`model`, `aspectRatio`, `resolution`, `quality`, `outputFormat`
- model 省略时用 agents.defaults.imageGenerationModel.primary（平台模型 ID）

### 图生图 (`image_to_image`)
- 工具：`image_generate`
- 必填：`prompt`, `images`
- 可选：`model`, `aspectRatio`, `resolution`
- 参考图用 image 或 images[]（~/.openclaw/media/inbound/… 本地路径）

### 超分参考图（Riverflow） (`image_super_resolution`)
- 工具：`image_generate`
- 必填：`prompt`, `images`
- 可选：`model`, `aspectRatio`
- 勿传 resolution；参考图走 super_resolution_references，见 generation_params

### 文生视频 (`text_to_video`)
- 工具：`video_generate`
- 必填：`prompt`, `durationSeconds`
- 可选：`model`, `aspectRatio`, `resolution`
- durationSeconds 须为模型支持的秒数

### 图生视频（首帧） (`image_to_video_first_frame`)
- 工具：`video_generate`
- 必填：`prompt`, `durationSeconds`, `image`, `imageRoles`
- 可选：`model`, `aspectRatio`, `resolution`
- imageRoles：`first_frame`

### 图生视频（尾帧） (`image_to_video_last_frame`)
- 工具：`video_generate`
- 必填：`prompt`, `durationSeconds`, `image`, `imageRoles`
- 可选：`model`, `aspectRatio`, `resolution`
- imageRoles：`last_frame`

### 图生视频（参考图） (`image_to_video_reference`)
- 工具：`video_generate`
- 必填：`prompt`, `durationSeconds`, `images`, `imageRoles`
- 可选：`model`, `aspectRatio`, `resolution`
- imageRoles：`reference_image`

## 生图模型

- **Nano Banana 2** (`google/gemini-3.1-flash-image-preview`) — tool `openrouter/google/gemini-3.1-flash-image-preview`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, 1:4, 4:1, 1:8, 8:1
  - 分辨率：0.5K, 1K, 2K, 4K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **Nano Banana Pro** (`google/gemini-3-pro-image-preview`) — tool `openrouter/google/gemini-3-pro-image-preview`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：1K, 2K, 4K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **Nano Banana** (`google/gemini-2.5-flash-image`) — tool `openrouter/google/gemini-2.5-flash-image`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：1K, 2K, 4K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **FLUX.2 Pro** (`black-forest-labs/flux.2-pro`) — tool `openrouter/black-forest-labs/flux.2-pro`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：1K, 2K, 4K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **FLUX.2 Max** (`black-forest-labs/flux.2-max`) — tool `openrouter/black-forest-labs/flux.2-max`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：1K, 2K, 4K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **FLUX.2 Flex** (`black-forest-labs/flux.2-flex`) — tool `openrouter/black-forest-labs/flux.2-flex`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：1K, 2K, 4K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **FLUX.2 Klein** (`black-forest-labs/flux.2-klein-4b`) — tool `openrouter/black-forest-labs/flux.2-klein-4b`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：1K, 2K, 4K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **Seedream 4.5** (`bytedance-seed/seedream-4.5`) — tool `openrouter/bytedance-seed/seedream-4.5`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：1K, 2K, 4K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **GPT-5.4 Image** (`openai/gpt-5.4-image-2`) — tool `openrouter/openai/gpt-5.4-image-2`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：1K, 2K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **GPT-5 Image** (`openai/gpt-5-image`) — tool `openrouter/openai/gpt-5-image`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：1K, 2K, 4K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **GPT-5 Image Mini** (`openai/gpt-5-image-mini`) — tool `openrouter/openai/gpt-5-image-mini`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：1K, 2K, 4K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **Grok Imagine** (`x-ai/grok-imagine-image-quality`) — tool `openrouter/x-ai/grok-imagine-image-quality`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：1K, 2K
  - 支持参考图（图生图）
  - 工作流：text_to_image, image_to_image
- **Riverflow Pro** (`sourceful/riverflow-v2-pro`) — tool `openrouter/sourceful/riverflow-v2-pro`
  - 比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  - 分辨率：无 image_size（超分参考图模式）
  - 支持超分参考图（super_resolution_references）
  - 工作流：text_to_image, image_super_resolution

## 生视频模型

- **Veo 3.1 Fast** (`google/veo-3.1-fast`) — tool `openrouter/google/veo-3.1-fast`
  - 时长：4, 6, 8 秒，默认 8s
  - 比例：16:9, 9:16，默认 16:9
  - 分辨率：720P, 1080P，默认 720P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame, last_frame
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_last_frame
  - 拼装：见 JSON `models.google/veo-3.1-fast.generation_params`
- **Veo 3.1** (`google/veo-3.1`) — tool `openrouter/google/veo-3.1`
  - 时长：4, 6, 8 秒，默认 8s
  - 比例：16:9, 9:16，默认 16:9
  - 分辨率：720P, 1080P, 4K，默认 1080P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame, last_frame
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_last_frame
  - 拼装：见 JSON `models.google/veo-3.1.generation_params`
- **Veo 3.1 Lite** (`google/veo-3.1-lite`) — tool `openrouter/google/veo-3.1-lite`
  - 时长：4, 6, 8 秒，默认 8s
  - 比例：16:9, 9:16，默认 9:16
  - 分辨率：720P, 1080P，默认 720P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame, last_frame
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_last_frame
  - 拼装：见 JSON `models.google/veo-3.1-lite.generation_params`
- **Seedance 2.0** (`bytedance/seedance-2.0`) — tool `openrouter/bytedance/seedance-2.0`
  - 时长：4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 秒，默认 5s
  - 比例：1:1, 3:4, 9:16, 4:3, 16:9, 21:9, 9:21，默认 9:16
  - 分辨率：480P, 720P, 1080P，默认 720P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame, last_frame, reference_image
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_last_frame, image_to_video_reference
  - 拼装：见 JSON `models.bytedance/seedance-2.0.generation_params`
- **Seedance 2.0 Fast** (`bytedance/seedance-2.0-fast`) — tool `openrouter/bytedance/seedance-2.0-fast`
  - 时长：4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 秒，默认 5s
  - 比例：1:1, 3:4, 9:16, 4:3, 16:9, 21:9, 9:21，默认 9:16
  - 分辨率：480P, 720P，默认 720P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame, last_frame, reference_image
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_last_frame, image_to_video_reference
  - 拼装：见 JSON `models.bytedance/seedance-2.0-fast.generation_params`
- **Seedance 1.5 Pro** (`bytedance/seedance-1-5-pro`) — tool `openrouter/bytedance/seedance-1-5-pro`
  - 时长：4, 5, 6, 7, 8, 9, 10, 11, 12 秒，默认 8s
  - 比例：1:1, 3:4, 9:16, 9:21, 4:3, 16:9, 21:9，默认 16:9
  - 分辨率：480P, 720P, 1080P，默认 720P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame, last_frame
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_last_frame
  - 拼装：见 JSON `models.bytedance/seedance-1-5-pro.generation_params`
- **Kling 3.0 Pro** (`kwaivgi/kling-v3.0-pro`) — tool `openrouter/kwaivgi/kling-v3.0-pro`
  - 时长：3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 秒，默认 8s
  - 比例：16:9, 9:16, 1:1，默认 16:9
  - 分辨率：720P，默认 720P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame, last_frame, reference_image
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_last_frame, image_to_video_reference
  - 拼装：见 JSON `models.kwaivgi/kling-v3.0-pro.generation_params`
- **Kling 3.0 Standard** (`kwaivgi/kling-v3.0-std`) — tool `openrouter/kwaivgi/kling-v3.0-std`
  - 时长：3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 秒，默认 8s
  - 比例：16:9, 9:16, 1:1，默认 16:9
  - 分辨率：720P，默认 720P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame, last_frame
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_last_frame
  - 拼装：见 JSON `models.kwaivgi/kling-v3.0-std.generation_params`
- **Kling Video O1** (`kwaivgi/kling-video-o1`) — tool `openrouter/kwaivgi/kling-video-o1`
  - 时长：5, 10 秒，默认 5s
  - 比例：16:9, 9:16, 1:1，默认 16:9
  - 分辨率：720P，默认 720P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame, last_frame, reference_image
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_last_frame, image_to_video_reference
  - 拼装：见 JSON `models.kwaivgi/kling-video-o1.generation_params`
- **Sora 2 Pro** (`openai/sora-2-pro`) — tool `openrouter/openai/sora-2-pro`
  - 时长：4, 8, 12, 16, 20 秒，默认 8s
  - 比例：16:9, 9:16，默认 16:9
  - 分辨率：720P, 1080P，默认 1080P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame
  - 工作流：text_to_video, image_to_video_first_frame
  - 拼装：见 JSON `models.openai/sora-2-pro.generation_params`
- **Wan 2.7** (`alibaba/wan-2.7`) — tool `openrouter/alibaba/wan-2.7`
  - 时长：2, 3, 4, 5, 6, 7, 8, 9, 10 秒，默认 8s
  - 比例：16:9, 9:16, 1:1, 4:3, 3:4，默认 16:9
  - 分辨率：720P, 1080P，默认 720P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame, last_frame, reference_image
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_last_frame, image_to_video_reference
  - 拼装：见 JSON `models.alibaba/wan-2.7.generation_params`
- **Wan 2.6** (`alibaba/wan-2.6`) — tool `openrouter/alibaba/wan-2.6`
  - 时长：5, 10 秒，默认 5s
  - 比例：16:9, 9:16，默认 16:9
  - 分辨率：720P, 1080P，默认 720P
  - 音频：可选带音频/静音（tool 字段 `audio`）
  - 图生视频 imageRoles：first_frame, reference_image
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_reference
  - 拼装：见 JSON `models.alibaba/wan-2.6.generation_params`
- **Hailuo 2.3** (`minimax/hailuo-2.3`) — tool `openrouter/minimax/hailuo-2.3`
  - 时长：6, 10 秒，默认 6s
  - 比例：16:9，默认 16:9
  - 分辨率：1080P，默认 1080P
  - 图生视频 imageRoles：first_frame, reference_image
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_reference
  - 拼装：见 JSON `models.minimax/hailuo-2.3.generation_params`
- **Grok Imagine Video** (`x-ai/grok-imagine-video`) — tool `openrouter/x-ai/grok-imagine-video`
  - 时长：1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 秒，默认 8s
  - 比例：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3，默认 16:9
  - 分辨率：480P, 720P，默认 720P
  - 图生视频 imageRoles：first_frame, reference_image
  - 工作流：text_to_video, image_to_video_first_frame, image_to_video_reference
  - 拼装：见 JSON `models.x-ai/grok-imagine-video.generation_params`

**拼装规则：** 用户选完模型与各参数后，按该模型 `generation_params.parameters` 映射为工具字段并一次性调用。

完整 JSON：`references/media-capabilities.json`

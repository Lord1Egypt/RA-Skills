---
name: doubao-all-in-one
description: 使用豆包（火山引擎 Ark）生成图片或视频，将结果保存到本地。当用户提到"豆包生图""豆包图片""豆包生视频""豆包视频""Doubao""Seedance""火山引擎图片""火山引擎视频"时引用。
metadata:
  openclaw:
    requires:
      bins:
        - uv
      anyBins:
        - python
        - python3
        - py
      env:
        - ARK_API_KEY
        - OUTPUT_ROOT
    primaryEnv: ARK_API_KEY
    pythonDeps:
      - "volcengine-python-sdk[ark]"
---

# 豆包图片与视频生成

这个 skill 提供豆包（火山引擎 Ark）的图片生成和视频生成能力，结果保存到本地。

适用场景：

- 用户明确指定使用豆包生成图片或视频
- 需要文生图、图生图、文生视频、首帧图生视频等

脚本位于 skill 目录内的 `scripts/`，运行时始终使用绝对路径。

设 `DOUBAO_SKILL_DIR` 为 `.claude/skills/doubao-all-in-one` 的绝对路径：

### 图片

- 文生图：`uv run python $DOUBAO_SKILL_DIR/scripts/text_to_image.py`
- 图生图：`uv run python $DOUBAO_SKILL_DIR/scripts/image_to_image.py`

### 视频

- 创建视频任务：`uv run python $DOUBAO_SKILL_DIR/scripts/create_video_task.py`
- 查询视频任务：`uv run python $DOUBAO_SKILL_DIR/scripts/query_video_task.py`
- 批量查询任务：`uv run python $DOUBAO_SKILL_DIR/scripts/list_video_tasks.py`
- 取消/删除任务：`uv run python $DOUBAO_SKILL_DIR/scripts/delete_video_task.py`
- 下载视频：`uv run python $DOUBAO_SKILL_DIR/scripts/download_video.py`
- Webhook 回调服务器：`uv run python $DOUBAO_SKILL_DIR/scripts/webhook_server.py`

---

## 快速调用

### 文生图

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/text_to_image.py \
  --prompt "一张电影感写实人像海报，光影强烈，构图干净" \
  --name "写实人像海报"
```

### 图生图

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/image_to_image.py \
  --image resources/images/climb1.jpeg \
  --prompt "保留主体动作，改为日落暖光的写实摄影风格" \
  --name "日落暖光人像"
```

### 文生视频（创建 + 轮询 + 下载一步完成）

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/create_video_task.py \
  --prompt "写实风格，晴朗的蓝天之下，一大片白色的雏菊花田，镜头逐渐拉近，最终定格在一朵雏菊花的特写上，花瓣上有几颗晶莹的露珠" \
  --name "雏菊花田特写" \
  --ratio 16:9 --duration 5 --poll
```

### 首帧图生视频

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/create_video_task.py \
  --prompt "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头" \
  --name "女孩抱狐狸" \
  --image-url "https://example.com/first_frame.png" \
  --role first_frame --ratio adaptive --duration 5 --poll
```

### 仅创建任务（异步工作流场景）

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/create_video_task.py \
  --prompt "小猫对着镜头打哈欠" --name "猫咪打哈欠" --ratio 16:9 --duration 5
```

### 创建任务 + Webhook 回调（替代轮询）

```shell
# 先启动 Webhook 服务器
uv run python $DOUBAO_SKILL_DIR/scripts/webhook_server.py

# 再创建任务，传入回调地址（不传则自动检测本机 8888 端口）
uv run python $DOUBAO_SKILL_DIR/scripts/create_video_task.py \
  --prompt "小猫对着镜头打哈欠" --name "猫咪打哈欠" --ratio 16:9 --duration 5
```

---

## 图片输入与输出

### 输入

| 参数 | 说明 | 文生图 | 图生图 |
|------|------|--------|--------|
| `--prompt` | 提示词 | 是 | 是 |
| `--name` | 文件名描述（不超过 10 个中文字） | 否 | 否 |
| `--model` | 模型 ID，默认 `doubao-seedream-5-0-260128` | 否 | 否 |
| `--image` | 输入图片路径或 URL，可多次传 | - | 是 |
| `--size` | 输出尺寸：2K / 3K / 4K / 2048x2048，默认 2K | 否 | 否 |
| `--response-format` | 返回格式：b64_json / url，默认 b64_json | 否 | 否 |
| `--output-format` | 输出文件格式：png / jpeg（仅 5.0 lite） | 否 | 否 |
| `--guidance-scale` | 文本权重，范围 [1, 10]（仅 3.0 系列） | 否 | 否 |
| `--watermark` | 添加水印 | 否 | 否 |
| `--sequential-image-generation` | 组图模式：auto / disabled，默认 disabled | 否 | 否 |
| `--max-images` | 组图最大数量，范围 [1, 15]，默认 15 | 否 | 否 |
| `--optimize-prompt` | 提示词优化：standard / fast（仅 5.0 lite/4.5/4.0） | 否 | 否 |
| `--web-search` | 启用联网搜索（仅 5.0 lite） | 否 | 否 |
| `--output` | 输出文件路径 | 否 | 否 |

### 本地输出目录

所有路径相对于 `OUTPUT_ROOT`（由环境变量注入，兜底为用户主目录）：

- `outputs/doubao/images/text_to_image/`
- `outputs/doubao/images/image_to_image/`

### 脚本输出 JSON

```json
{
  "type": "image",
  "scene": "text_to_image",
  "provider": "doubao",
  "used_model": "doubao-seedream-5-0-260128",
  "local_path": "outputs/doubao/images/text_to_image/20260330_120000.png",
  "image_count": 1,
  "generated_images": 1,
  "usage": {"generated_images": 1, "output_tokens": 0, "total_tokens": 0}
}
```

---

## 视频输入与输出

### 输入

| 参数 | 说明 | 必需 |
|------|------|------|
| `--prompt` | 提示词 | 是 |
| `--name` | 文件名描述（不超过 10 个中文字） | 否 |
| `--model` | 模型 ID，默认 `doubao-seedance-1-5-pro-251215` | 否 |
| `--image-url` | 图片 URL（可多次传），配合 `--role` 使用 | 否 |
| `--role` | 图片角色：`first_frame` / `last_frame` | 否 |
| `--ratio` | 宽高比：16:9, 4:3, 1:1, 3:4, 9:16, 21:9, adaptive | 否，默认 16:9 |
| `--duration` | 视频时长（秒）：2~12（1.5 pro 支持 -1 由模型自选） | 否，默认 5 |
| `--resolution` | 分辨率：480p, 720p, 1080p（1.0 lite 参考图不支持 1080p） | 否，默认 480p |
| `--seed` | 随机种子，范围 [-1, 2^32-1] | 否 |
| `--frames` | 视频帧数，格式 25+4n，范围 [29, 289]（1.5 pro 暂不支持） | 否 |
| `--generate-audio` | 生成有声视频（仅 1.5 pro，API 默认 true） | 否 |
| `--watermark` | 添加水印 | 否 |
| `--camera-fixed` | 固定摄像头（参考图场景不支持） | 否 |
| `--return-last-frame` | 返回视频尾帧图像（可用于连续视频拼接） | 否 |
| `--draft` | 生成样片（仅 1.5 pro，固定 480p，不支持离线） | 否 |
| `--execution-expires-after` | 任务超时秒数，范围 [3600, 259200]，默认 172800（48h） | 否 |
| `--service-tier` | 推理模式：default（在线）/ flex（离线，50% 价格） | 否 |
| `--poll` | 创建后自动轮询直到完成并下载 | 否 |
| `--poll-interval` | 轮询间隔秒数，默认 10 | 否 |
| `--timeout` | 轮询超时秒数，默认 900 | 否 |
| `--callback-url` | Webhook 回调地址；不传时自动检测 | 否 |

### 本地输出目录

所有路径相对于 `OUTPUT_ROOT`（由环境变量注入，兜底为用户主目录）：

- `outputs/doubao/videos/text_to_video/`
- `outputs/doubao/videos/first_frame_to_video/`
- `outputs/doubao/videos/first_last_frame_to_video/`

### 视频脚本输出 JSON

创建任务返回：
```json
{
  "type": "video",
  "scene": "text_to_video",
  "provider": "doubao",
  "task_id": "cgt-2025xxxx",
  "status": "queued"
}
```

轮询完成并下载后返回：
```json
{
  "type": "video",
  "scene": "text_to_video",
  "provider": "doubao",
  "task_id": "cgt-2025xxxx",
  "used_model": "doubao-seedance-1-5-pro-251215",
  "local_path": "outputs/doubao/videos/text_to_video/20260330_120000_cgt-xxx.mp4",
  "source_url": "https://...",
  "resolution": "480p",
  "ratio": "16:9",
  "duration": 5
}
```

查询任务返回：
```json
{
  "task_id": "cgt-2025xxxx",
  "model": "doubao-seedance-1-5-pro-251215",
  "status": "succeeded",
  "created_at": 1743300000,
  "updated_at": 1743300120,
  "video_url": "https://...",
  "last_frame_url": "https://...",
  "resolution": "480p",
  "ratio": "16:9",
  "duration": 5,
  "seed": 12345,
  "generate_audio": true,
  "draft": false,
  "service_tier": "default",
  "execution_expires_after": 172800,
  "usage": {"completion_tokens": 100, "total_tokens": 100}
}
```

---

## 模型选择

### 图片模型

| 模型 | Model ID | 特点 |
|------|----------|------|
| Seedream 5.0 | `doubao-seedream-5-0-260128` | 默认首选 |
| Seedream 4.5 | `doubao-seedream-4-5-251128` | 额度不足时自动 fallback |

### 视频模型

| 模型 | Model ID | 特点 |
|------|----------|------|
| Seedance 1.5 Pro | `doubao-seedance-1-5-pro-251215` | 最高质量，支持有声视频、样片模式、返回尾帧、4~12秒 |

---

## 提示词最佳实践（图片，强制）

调用图片生成脚本前，**必须**先读取 `references/seedream_prompt_guide.md`，并对照以下检查清单审核用户的提示词。

### 执行规则

1. **必须读取参考文档**：每次生成图片前，先读取 `references/seedream_prompt_guide.md`
2. **提示词公式**：主体 + 行为（非必须）+ 环境（非必须）+ 风格/色彩/光影/构图（非必须）
3. **使用自然语言**：用简洁连贯的自然语言描述，不要用逗号分隔的关键词堆叠
4. **质量检查与处理策略**：对照检查清单逐项审核
   - **缺少主体**：**必须拒绝执行**，返回 JSON 格式的拒绝信息，自行优化后请用户确认再执行
   - **其他不合规项**（关键词堆叠、模糊代词、缺少风格描述等）：**直接按最佳实践指南自动补充优化**，向用户展示优化后的提示词并说明补充了哪些内容，然后直接执行
5. **自动优化格式**：
   ```
   优化说明：
   - [具体补充了什么，如"补充了风格描述：莫奈油画风格"]

   文件名标题：[不超过 10 个中文字的内容简述，如"雪中小猫玩耍"]

   优化后提示词：
   [完整提示词]
   ```
   - **文件名标题**：在优化提示词时同时生成一个简短标题，不超过 10 个中文字，**调用脚本时必须通过 `--name` 参数传入**。标题应概括画面核心内容，如"雪中小猫玩耍""金色麦田奔跑""日落海边漫步"

### 提示词质量检查清单

- [ ] **使用自然语言**：是否用简洁连贯的句子描述画面，而非逗号分隔的关键词堆叠？
- [ ] **主体明确**：是否清楚描述了画面中的主体是谁/什么？特征是否具体？
- [ ] **编辑目标明确**（图生图）：是否准确指示了需要编辑的对象和变化要求？是否避免使用模糊代词？
- [ ] **保持不变的部分**（图生图）：是否明确说明了希望保持不变的内容？
- [ ] **文字内容加引号**：如需生成文字，文字内容是否放在双引号中？
- [ ] **简洁精确**（5.0 lite/4.5/4.0）：是否避免了不必要的华丽词汇堆叠？简洁精确优于重复冗余
- [ ] **风格词精准**：如有风格需求，是否使用了精准的风格词而非模糊描述？
- [ ] **多图关系清晰**（多图输入）：是否清楚指明了不同图像间的编辑/参考关系？

### 必须拒绝的情况

- 主体完全缺失（如"一张好看的图""生成一张图"）

### 应自动补充的情况

- 关键词堆砌 → 改写为自然语言
- 缺少风格/美学描述 → 根据画面内容补充合适的风格
- 图生图中使用模糊代词 → 替换为具体对象描述
- 需要渲染文字但未加双引号 → 补充双引号
- 多图输入但未指明图间关系 → 根据意图补充关系描述

### 图生图额外规则

- **图像编辑**（增加/删除/替换/修改）：用简洁明确的指令，准确指示编辑对象
- **参考图生图**：提示词必须包含两部分——**指明参考对象** + **描述生成画面**
- **多图输入**：清楚指明不同图像需要编辑/参考的对象及操作（如"用图一的人物替换图二的人物"）
- **设计草图转高保真**：注明"遵循图中文字内容进行生成"，明确需与参考图保持一致的关键要求

---

## 提示词最佳实践（视频，强制）

调用视频生成脚本前，**必须**先读取 `references/seedance_1_5_pro_prompt_guide.md`，并对照其中的**提示词质量检查清单**审核用户的提示词。

### 参数约束

- **分辨率默认 480p**：除非用户明确要求更高分辨率（如"720p""1080p""高清"），否则**不得**传 `--resolution` 参数，直接使用脚本默认的 480p
- **宽高比默认 16:9**：除非用户明确要求其他比例（如"竖屏""正方形""9:16""1:1"等），否则**不得**传 `--ratio` 参数，直接使用脚本默认的 16:9。有首帧/尾帧参考图且用户未指定比例时也应使用 16:9，而非 adaptive

### 执行规则

1. **必须读取参考文档**：每次生成视频前，先读取 `references/seedance_1_5_pro_prompt_guide.md`
2. **提示词公式**：主体 + 运动 + 环境（非必须）+ 运镜/切镜（非必须）+ 美学描述（非必须）+ 声音（非必须）
3. **质量检查与处理策略**：对照检查清单逐项审核
   - **缺少主体**：**必须拒绝执行**，返回 JSON 格式的拒绝信息，自行优化后请用户确认再执行
   - **其他不合规项**（缺少运动描述、缺少环境、切镜不清晰等）：**直接按最佳实践指南自动补充优化**，向用户展示优化后的提示词并说明补充了哪些内容，然后直接执行
4. **自动优化格式**：
   ```
   优化说明：
   - [具体补充了什么，如"补充了运动描述：金毛犬在麦田中快速奔跑"]
   - [具体补充了什么，如"补充了环境描述：金色麦田，阳光从侧面照射"]

   文件名标题：[不超过 10 个中文字的内容简述，如"金毛麦田奔跑"]

   优化后提示词：
   [完整提示词]
   ```
   - **文件名标题**：在优化提示词时同时生成一个简短标题，不超过 10 个中文字，**调用脚本时必须通过 `--name` 参数传入**。标题应概括画面核心内容，如"金毛麦田奔跑""猫咪打哈欠""海边日落漫步"
### 必须拒绝的情况

- 主体完全缺失（如"生成一个视频""做个动画"）
- 主体不明确且无法推断（如"一个东西在动"）

### 应自动补充的情况

- 缺少运动描述 → 根据主体特性补充合理的动作和运动方式
- 缺少环境描述 → 根据主体和场景补充环境信息
- 多人场景角色特征不可区分 → 为每个角色补充唯一标识特征
- 包含切镜但未区分镜头编号或景别 → 补充镜头编号和景别描述
- 包含对话但未指定语言类型或音色特征 → 补充音色和语言描述

---

## 配置

- 环境变量：`ARK_API_KEY`（必需，未设置时直接报错）
- 环境变量：`OUTPUT_ROOT`（可选，输出根目录，支持 `~` 展开，默认为用户主目录）

## 短剧批量视频生成

当用户请求为短剧的多个 clip（C01、C02…）批量生成视频时，遵循以下规则：

### 一 clip 一请求

- 每个 clip（CXX）是**一个完整的视频生成请求**，不得按分镜（sub-shot）拆分为多次请求
- 分镜仅用于提示词规划（描述运镜变化、景别切换等），最终合并为一条 prompt 提交给模型
- 示例：C01 有 2 个分镜（C01-1、C01-2），仍只调用一次 `create_video_task.py --duration 8`

### 输出目录与文件名

- 视频生成完成后，**必须**将文件从脚本默认输出目录复制到项目的视频生成目录
- 输出路径：`outputs/scripts/{项目名}/video_generation/{篇章}/CXX.MP4`
  - 例如：`outputs/scripts/chong_sheng_zhui_qi_20260401/video_generation/nightmare/C01.MP4`
- 项目名和篇章名从用户提供的视频生成指令文档路径中推断

## 协作方式

- 图片生成可直接完成任务
- 视频生成使用 `--poll` 模式可直接完成任务；异步工作流可分步操作
- Webhook 模式：先启动 `webhook_server.py`（默认端口 8888），创建任务时自动检测回调地址（优先级：手动 `--callback-url` > 环境变量 `VIDEO_CALLBACK_BASE_URL` > 自动检测本机 IP + 8888 端口）
- 如果用户还需要公网链接或临时下载链接，应由后续的交付环节继续处理

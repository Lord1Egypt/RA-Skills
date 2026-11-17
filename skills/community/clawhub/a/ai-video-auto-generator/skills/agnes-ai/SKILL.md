---
name: agnes-ai
version: 2.7.0
description: >
  纯生成层 skill。调用 Agnes AI 免费 API 生成图片和视频。
  脚本路径为 `skills/agnes-ai/scripts/generate_image.py`
  和 `skills/agnes-ai/scripts/generate_video.py`（相对于主 skill 根目录）。
---

# Agnes AI 纯生成 Skill

通过 `scripts/generate_image.py` 生成图片、`scripts/generate_video.py` 生成视频。

> 本 skill 是 `ai-video-auto-generator` 的子 skill。项目级编排命令在 `project-generate` 子 skill 中。

---

## 🚀 高频命令

```bash
# 文生图
python3 scripts/generate_image.py "一只猫" --size "1024x1024" -o ./output

# 图生图
python3 scripts/generate_image.py "描述提示词" --ref-image /path/to/ref.png

# 文生视频
python3 scripts/generate_video.py "古风战场" --size "9:16" --duration 5s

# 图生视频
python3 scripts/generate_video.py "缓慢推进" --ref-image input.png --duration 5s
```

## 前置条件

1. **注册获取 API Key**（免费无限制）：
   - 访问 https://platform.agnes-ai.com 注册
   - 登录后在后台创建 API Key
   - 将 Key 写入 `~/.agnes-api-key`，或设环境变量 `AGNES_API_KEY`

2. **Python 3** — 标准库即可，无需额外依赖。

## 两个模型的分工

| 模型 | 本质 | 适用场景 | 翻车点 |
|-----|------|---------|-------|
| **2.0 Flash**（多图合成） | 多张图融合成一张新画面 | 单角色静态、双角色无互动、特写、环境合成 | 可能脑补多余元素（凭空加人） |
| **2.1 Flash**（参考图编辑） | 以第一张图为基底添加元素 | 需保留场景结构、精确动作控制、有交互 | 过于忠实原图 |

### 选择规则
- 单角色静态/特写 → **2.0 Flash**
- 单角色精确动作（掀帘、推门） → **2.1 Flash**
- 双角色无互动（背对、行礼、跪拜） → **2.0 Flash**
- 双角色有互动（对视、对话、肢体接触） → **2.1 Flash**
- **2.0 Flash 图生图不需要传 `tags: ["img2img"]`**

### 实战验证
| 场景 | 2.0 结果 | 2.1 结果 | 建议 |
|------|---------|---------|------|
| 墨雪站窗边 | ✅ 1人 | — | 2.0 |
| 墨将推门 | ✅ 1人 | — | 2.0 |
| 双角色同框 | ✅ 2人 | — | 2.0 |
| 面部特写 | ✅ 1人 | — | 2.0 |
| 掀帘子 | ❌ 变2人 | ✅ 1人 | 2.1 |
| 互踢（互动） | — | ✅ | 2.1 |
| 城墙眺望 | ❌ 场景错 | ✅ 正确 | 2.1 |

## 图片生成 — 使用方法

### 快速入门（单张图片生成）

`generate_image.py` 是一个独立的单张图片生成工具，批量生成请走 `project-generate`：

```bash
# 单张图生图
python3 scripts/generate_image.py "提示词" --ref-image "参考图.png" -o "images/characters/" --output-name "角色名_front.png"

# 批量首帧图 → 请使用 project-generate
python3 ../ai-video-auto-generator/skills/project-generate/scripts/project_generate.py --project . gi
```

### 完整参数

**图片参数（`scripts/generate_image.py`）**
| 参数 | 说明 |
|------|------|
| `prompt`（必填） | 图片描述提示词 |
| `--model` | 默认 `agnes-image-2.1-flash` |
| `--size` | 默认 `720x1280`，自动从 aspect_ratio 映射 |
| `--n` | 数量（1-4） |
| `--quality` | `standard` 或 `hd` |
| `--output-dir` / `-o` | 保存目录 |
| `--ref-image` | 单张参考图路径 |
| `--ref-images` | 多张参考图（空格分隔）|
| `--output-name` | 输出文件名 |
| `--seed` | 固定随机种子 |
| `--negative-prompt` | 负面提示词 |
| `--api-key` | API Key 文件路径 |
| `--shot-id` | 从 script.json 的 first_frame 块解析参数，生成该 shot 的首帧图 |
| `--project` | 项目根目录（--shot-id 模式需要）|
| `--force` | 强制重新生成已存在的 first_frame 和模板 |
| `--parallel` | 并发生成数（默认 auto）|

**视频参数（`scripts/generate_video.py`）**
| 参数 | 说明 |
|------|------|
| `--model` | 默认 `agnes-video-v2.0` |
| `--ref-image` | 单张参考图路径 |
| `--ref-image-list` | 多张参考图路径 |
| `--ref-image-urls` | 已上传的公网 URL |
| `--num-frames` | 总帧数（8n+1，≤441），默认 121 |
| `--frame-rate` | 帧率（1-60），默认 24 |
| `--size` | 分辨率，默认 `1152x768` |
| `--seed` | 固定种子 |
| `--output-name` | 输出文件名 |
| `--output-dir` / `-o` | 保存目录 |
| `--api-key` | API Key 文件路径 |
| `--mode` | 生成模式：standard / keyframes / multi-image / auto |
| `--duration` | 目标时长（如 `5s`）|
| `--poll-interval` | 轮询间隔（默认 15s）|
| `--timeout` | 超时时间（默认 600s）|
| `--submit-only` | 仅创建任务，打印 task_id 后退出 |
| `--query-task` | 查询已有任务，若完成则下载 |

### 两步工作流

**第 1 步 — 初始化：**
```bash
python3 scripts/generate_image.py --project . --build-first-frames
# 或强制重新生成
python3 scripts/generate_image.py --project . --build-first-frames --force
```
自动完成：
- 遍历所有 shot，从 `generation.reference_images` 解析参考图路径
- 根据 shot 描述自动推荐模型（2.0 Flash / 2.1 Flash）
- 写入 `first_frame` 块到 script.json
- 对每个 shot 生成六段式提示词模板
- **multi-image 模式**（如 shot_01）自动跳过
- 已有 `first_frame` 的 shot 默认跳过（`--force` 覆盖）

**第 2 步 — 单 shot 或批量生成：**
```bash
# 单 shot
python3 scripts/generate_image.py --project . --shot-id 4

# 批量
python3 scripts/generate_image.py --project . --batch-generate

# 指定范围
python3 scripts/generate_image.py --project . --batch-generate --batch-shots "2-9"
```

### 基本调用

```bash
python3 scripts/generate_image.py "描述提示词，保留角色特征" \
  --ref-image "/path/to/墨雪_front.png" \
  --size "1024x1024" \
  -o "/path/to/output" \
  --output-name "墨雪_表情.png"
```

## 提示词结构（六段式）

适用于 2.0 Flash / 2.1 Flash 图生图：

```
将N张参考图合成一张完整画面。

[编辑指令] 参考图1为XX（场景基底）。参考图2为XX（角色A样式）。
以图1为基底，在场景中加入角色A（位置/方向参考图2）。明确写"无交互无对视"。

[保留元素] 完全保持：图2的服装颜色、发型。

[目标风格/场景] 每个角色的位置、动作、服装颜色、环境布局。

[光照] 光源方向、冷暖对比。

[构图] 画幅、景别、空间位置（谁高位谁低位）。

[画质要求] 电影级写实，关键细节，氛围情绪。
```

### 关键技巧
- ❌ **不要用** "在图1场景中加入墨雪" → 模型可能把参考图里"旁边的人"也取过来
- ✅ **要用** "场景中墨雪一个人站在门口掀帘"
- 2.1 Flash 在[编辑指令]里写清交互动作（"推门走进来、望向"）
- 首次抽卡用最简 prompt，每轮只改 1-2 个点
- 同参数连抽 ≤3 轮，不改善换策略

## 常见问题

### 文化手势无法精确控制
模型无法生成"左手抱右拳"等特定手势。手抬至胸前已是极限。

### 人物数量不对
- 2.0 Flash 可能脑补多余人物 → 换 2.1 Flash
- 不要用"加入/插入/放入角色"指令式措辞
- 明确写"只有一个人"

### 参考图比例
手动合成参考板时，比例必须与输出一致。

## 首帧图 Prompt 组装规则（重要）

`generate_image.py` 在 `_clean_prompt()` 中实现了**段提取拼接机制**，从 `prompts/storyboard/shotXX_image.md` 文件中按 [xxx] 标签提取指定段的内容，去掉标签后按指定顺序拼接成最终 API prompt。

### 动态段提取
通过 `segments` 参数指定需要提取的段名列表，按顺序拼接：
```python
prompt = _clean_prompt(f.read().strip(),
    segments=["编辑指令","目标风格/场景","光照","构图","画质要求"])
```

### 可用段列表（按顺序）
| 段名 | 用途 | 是否推荐 |
|------|------|---------|
| `[编辑指令]` | 描述参考图用途和角色空间关系 | ✅ 必须 |
| `[保留元素]` | 指定参考图中需要保持的特征 | ⚠️ 谨慎（见下方说明）|
| `[目标风格/场景]` | 最终画面描述 | ✅ 必须 |
| `[光照]` | 光源方向和氛围 | ✅ 推荐 |
| `[构图]` | 画面布局和角色位置 | ✅ 推荐 |
| `[画质要求]` | 质量关键词+负面提示 | ✅ 推荐 |

### ⚠️ [保留元素] 的关键陷阱
2.0 Flash 多图合成模式下，`[保留元素]` 会让模型**保持参考图的整体特征（含朝向/姿态）**，覆盖文字指令中的空间描述。

例如：参考图为 `墨雪_side.png`（侧身），`[保留元素]` 写"完全保持图2墨雪的特征" → 模型理解"保持图2的所有包括朝向" → 墨雪面向镜头方向而非文字指定的"侧身望向窗外"。

**规则**：3张参考图（场景+双角色）时**不要加 `[保留元素]`**，角色朝向全靠文字指令描述。仅单角色+场景（2张图）时可以加。

### 双角色首帧图推荐方案
| 要素 | 推荐设置 |
|------|---------|
| 模型 | **2.0 Flash**（多图合成） |
| 参考图 | 场景 + 墨雪_side + 墨将_front（**3张独立**，不合成参考板）|
| 提示词段 | `[编辑指令]` + `[目标风格/场景]` + `[光照]` + `[构图]` + `[画质要求]` |
| 墨雪参考 | 用 `墨雪_side.png`（侧身）而非 `墨雪_front.png`（正面），减少正面朝向的"拉力" |
| 排除段 | **不加** `[保留元素]`（会导致角色面朝镜头方向） |

### ⚠️ 参考图选型：`front`（全身）优于 `face`（面部特写）
首帧图参考图**优先选用全身正面图 `_front`**，而非面部特写 `_face`：

| 对比维度 | `_front`（全身正面） | `_face`（面部特写） |
|---------|-------------------|-------------------|
| 甲胄颜色 | ✅ 保留正确的颜色和样式 | ❌ 颜色偏差（特写区域太小，模型无法定位颜色）|
| 面部特征 | ✅ 模型自然继承 | ✅ 保留 |
| 服装细节 | ✅ 完整保留 | ❌ 无法获取全局颜色信息 |

**实战案例**：`墨将_front` → 银灰轻甲（正确）；`墨将_face` → 深褐色玄铁甲（错误，被特写图领口小面积颜色误导）。

**规则**：即使是面部特写镜头，参考图也用 `_front` 全身图，面部特征模型会自动继承。

### 代码实现说明
`generate_image.py` 中的 `_clean_prompt(text, segments)` 函数实现段提取：
- `segments=None` → 全量模式（保留所有非标签内容，向后兼容）
- `segments=[...]` → 段模式：仅提取指定 [xxx] 段的内容，按列表顺序拼接
- 可配置在 `script.json` 中每个 shot 的 `first_frame.segments` 字段，无配置时 fallback 到默认列表

## 调用方式（务必遵守）

本 skill 已作为子技能打包在主 skill 的 `skills/agnes-ai/` 目录下。

**🔥 硬性规则**：调用 `generate_*.py` 必须使用子 skill 路径（相对于主 skill 根目录）。

```bash
# ✅ 正确：子 skill 路径（在主 skill 根目录执行）
python3 skills/agnes-ai/scripts/generate_image.py \
  "prompt" --project . --shot-id 4

# ✅ 通过项目 scripts/generate_image.py 快捷入口（推荐）
python3 scripts/generate_image.py "prompt" --size "1024x1536"
```

> 子 skill 是修改入口，此目录已在主 skill 的 `skills/agnes-ai/` 下，无需额外同步。

---

## 视频生成（Agnes Video V2.0）

本 skill 也封装了视频生成能力，通过 `scripts/generate_video.py` 调用：

```bash
# 文生视频
python3 scripts/generate_video.py "古风战场，阴天低沉光线，硝烟弥漫" \
  --size "768x1152" \    # 9:16竖版
  --num-frames 121 \     # ≈5秒@24fps
  --frame-rate 24 \
  -o "./videos" \
  --output-name "shot_01.mp4"

# 图生视频（以分镜首帧图为参考）
python3 scripts/generate_video.py "缓慢推进的镜头，战场上残旗飘动" \
  --ref-image "./images/storyboard/shot_01_first_frame.png" \
  --size "768x1152" \
  -o "./videos" \
  --output-name "shot_01.mp4"
```

### 时长参数

| 目标时长 | --duration | 实际参数 |
|---------|-----------|---------|
| 约 3 秒 | `--duration 3s` | `--num-frames 81 --frame-rate 24` |
| 约 5 秒 | `--duration 5s` | `--num-frames 121 --frame-rate 24` |
| 约 10 秒 | `--duration 10s` | `--num-frames 241 --frame-rate 24` |
| 约 18 秒 | `--duration 18s` | `--num-frames 441 --frame-rate 24` |

也可直接用 `--num-frames` 和 `--frame-rate` 精细控制。num_frames 合法值：8n+1，≤441。

### 分辨率参数

`--size` 支持宽x高格式和比例别名：

- `--size 9:16` → 720x1280（竖屏短视频）
- `--size 16:9` → 1280x720（横屏）
- `--size 1:1`  → 1024x1024（正方形）
- `--size 1920x1080` → 自定义分辨率

### 生成模式（--mode）

脚本支持三种生成模式，通过 `--mode` 选择：

**standard（默认）**
```bash
# 文生视频（无参考图）
python generate_video.py "prompt" --duration 5s --size 9:16 --submit-only

# 图生视频（1 张参考图）
python generate_video.py "prompt" --ref-image input.png --duration 5s --size 9:16
```

**multi-image（多图视频）**
```bash
python generate_video.py "prompt" \
  --mode multi-image \
  --ref-image-list img1.png img2.png ... \
  --duration 5s --size 9:16 --submit-only
```

**keyframes（关键帧动画）**
```bash
python generate_video.py "prompt" \
  --mode keyframes \
  --ref-image-list kf1.png kf2.png ... \
  --duration 5s --size 9:16 --submit-only
```

### 模式选择决策指南

根据镜头素材和描述自动选择模式（内置在 `video_api.py` 的 `_select_mode()`）：

```
只有 1 张参考图 ────────→ standard（最常用）
        │
有 2+ 张参考图 ─┬─ 描述含 before/after/对比/转变 → multi-image
                ├─ 描述含 多人/关键帧/转场/复杂场景 → keyframes
                └─ 其他 → standard
```

### 参考图来源优先级

`generate_video.py` 接受三种形式的参考图，按以下优先级处理：

| 优先级 | 参数 | 来源 | 适用场景 |
|--------|------|------|---------|
| 1 (最高) | `--ref-image-urls` | 已上传的公网 URL | 重试/多图 cache 回放 |
| 2 | `--ref-image-list` | 本地多张图片路径 | 首次提交多图/keyframes |
| 3 | `--ref-image` | 本地单张图片路径 | 首次提交 standard 模式 |

### 视频参数一览

| 参数 | 默认 | 说明 |
|------|------|------|
| `--model` | `agnes-video-v2.0` | 视频模型名 |
| `--ref-image` | 无 | 参考图路径（图生视频模式） |
| `--num-frames` | `121` | 总帧数，必须为 8n+1（≤441） |
| `--frame-rate` | `24` | 帧率，1-60 |
| `--size` | `1152x768` | 分辨率 宽x高（短剧用 768x1152） |
| `--seed` | 随机 | 固定种子可复现结果 |
| `--output-name` | 自动生成 | 指定文件名 |

## Prompt 最佳实践（视频）

### 各模式 Prompt 写作模板

**standard（单图生视频）** — 描述哪些动、哪些不动：
```
{角色/元素} + {运动描述} + {场景/光照} + {保持稳定的元素}
```

**multi-image（多图过渡）** — 描述图片之间的关系和过渡方式：
```
从第1张图到第2张图 + {过渡描述} + {什么需要保持一致}
```

**keyframes（关键帧插值）** — 描述关键帧之间的插值风格：
```
在关键帧之间 + {过渡描述} + {角色/场景一致性要求} + {镜头风格}
```

---

## API 说明

### 图片 API 的 image 字段格式
实测 `image` 在 `extra_body` 内才生效（顶层不生效）：

```json
{
  "model": "agnes-image-2.0-flash",
  "prompt": "...",
  "size": "1024x1792",
  "extra_body": {
    "image": ["url1", "url2"],
    "response_format": "url"
  }
}
```

两模型区别：
| 对比维度 | 2.0 Flash | 2.1 Flash |
|---------|-----------|-----------|
| `image` 位置 | `extra_body` 内 | `extra_body` 内 |
| `tags` 参数 | 不需要 | 不需要 |

### 图片 vs 视频 API
| 能力 | 图片 API | 视频 API |
|------|---------|---------|
| `image` 字段位置 | `extra_body` 内 | `extra_body` 内 |
| 多图支持 | 数组 | 数组 |

### 视频 API 补充说明
- 三种模式：
  - `standard`：传单张 URL 到顶层 `image`，不加 `extra_body.image`
  - `multi-image`（pipeline 内部模式名）：传 `extra_body.image` 数组，**不加 `mode` 参数**
  - `keyframes`：传 `extra_body.image` 数组 + `extra_body.mode=keyframes`
- 多图参考时所有参考图尺寸建议统一（如均为 720×1280），避免模型根据输入图自适应调整输出分辨率。

## 注意事项

- **API 完全免费**，无调用次数限制、无限期。但建议合理使用避免滥用。
- **支持图生图**：用 `--ref-image` 参数传入本地图片路径作为参考图。
- **支持图生视频**：通过 `generate_video.py --ref-image` 传入参考图。
- **纯中文提示词**：Agnes AI 对纯中文提示词理解准确，生图效果优于中英混用。
- 生成成功后，脚本会返回本地文件路径列表。通过 `--output-name` 参数指定文件名，替代了旧的 asset_map.json 映射方式。
## 基础设施与容错（2026-07 修复）

_新项目自动继承以下代码层修复（在 modules/ 中），但了解其原理可帮助诊断类似问题。_

### GitHub PAT 管理

- **PAT 类型**：代码读取 `~/.github-pat` 文件。支持 Classic PAT 和 Fine-grained PAT。
- **过期风险**：Fine-grained PAT（`github_pat_` 前缀）有强制过期时间（30/90/365天）。Classic PAT 可设 "No expiration"，推荐用于持续运行的流水线。
- **创建新 PAT**：访问 https://github.com/settings/tokens
  - 推荐：Classic → `repo` scope → No expiration → 写入 `~/.github-pat`
- **故障特征**：GitHub 上传返回 HTTP 401 "Bad credentials" → `upload_to_url` 抛出 `ValueError("GitHub PAT 无效或已过期")`，流水线立即标记 shot 失败而非死循环。

### 参考图托管优化（skip-if-exists）

**问题**：Agnes API 服务器从 `raw.githubusercontent.com` 下载大图时，国内网络访问 GitHub raw 偶发超时 → 返回 `400 Invalid image`，被误判为内容审核。

**修复**（默认 Agnes Provider 走 `image_api.py upload_to_url`）：改为「先查后传」：
- 上传前先 `GET` 查 GitHub 同名文件的 `sha`；若已存在，直接返回已有 raw 直链，**跳过 PUT**（1 次 API 调用而非 2 次）。
- **不压缩**：早期版本用 PIL 压缩首帧图（quality 70 / 1280px）已被移除——Agnes 对原图尺寸兼容性更好，压缩反而可能触发审核。GitHub 上传分支始终上传原图；仅当**未配置 PAT** 时走 data-URI 兜底才压缩为 JPEG quality 85，正常流水线走不到。
- 故障特征与重试语义见下方「重试架构」表（`image_api.py upload_to_url` 行）。

> 小云雀 Provider 走另一条上传路径 `img_host.py upload_image`，重试语义更温和（见重试表最后一行）。

**效果**：同图重复上传几乎零成本，降低 GitHub 限流（429）与 abuse detection 风险。

### 重试架构

所有 `while True` 无限重试已封顶，避免单点故障拖垮整轮轮询：

| 位置 | 封顶值 | 4xx（非429） | 429/5xx/网络 | 耗尽后 |
|------|--------|-------------|-------------|--------|
| `agnes_provider.py generate_character` / `generate_scene`（角色图/场景图） | max_attempts=5 | 耗尽后 `return None`（4xx 非429 经 `apply_image_strategy` 调整提示词后重试，不立即中断） | 仅 rate_limit 时固定 sleep 30s（其余类别不 sleep） | `return None` |
| `image_api.py upload_to_url`（默认 Agnes 上传） | MAX_UPLOAD_RETRY=4 | 401/403→`raise ValueError`（立即失败） | 退避 `min(10×attempt,60)` → 10s→20s→30s→40s（共 4 次，60s 仅在 attempt≥6 才触及） | `raise RuntimeError` |
| `img_host.py upload_image`（小云雀 Provider） | MAX_RETRIES=3 | 401/403→`return None`（不重试） | 固定 2s（仅 429/500/502/503 重试） | `return None` |

### 错误分类策略 `_classify_failure()`

`error_utils.classify()`（在 `agnes_provider.py` / `video_utils.py` 中 import 为 `_classify_failure`）从 Agnes API 的 raw error 提取分类：

| 分类 | 匹配规则 | 策略 |
|------|---------|------|
| `rate_limit` | 429 / rate_limit | 本轮跳过，等待下轮轮询（不退避原帧） |
| `invalid_image` | 400 / invalid_image / unsafe / moderation | **重建首帧**（`_resubmit_shot(regen_first_frame=True)` 经 Provider 重新生成首帧图）+ 重提 |
| `transient` | remoteclosed / timeout / 5xx | 原样重提（瞬时网络抖动） |
| `bad_request` | 其他 4xx | 重建首帧后重提（可能图片格式问题） |
| `unknown` | 不匹配任何规则 | 原样重提（保守策略） |

### 首帧重建机制

`invalid_image`/`bad_request` 错误通过 `video_utils.py:_resubmit_shot(project, sid, script, provider, retry_count=0, regen_first_frame=True)` 处理：

- 调用 `provider.generate_first_frame(project, shot, script_data)` 重新生成首帧图（通过 `build_first_frame` 构建提示词 → `generate_image` API 调用）
- 重建使用 `ThreadPoolExecutor` + 240s 超时保护：
  - 超时前成功 → `shutil.copyfile` 覆盖到 first_frame.final 路径
  - 超时或异常 → 返回 False，不提交旧被拒帧（避免重复 400 自旋）
- 若 regen 失败 → `_resubmit_shot` 标记 shot 为 failed，等下一轮轮询重试

### 新项目自查清单

启动新项目后，检查以下基础设施是否正常：

1. **GitHub PAT**：`curl -H "Authorization: token $(cat ~/.github-pat)" https://api.github.com/repos/JinXuchen2020/video-images/contents/` → HTTP 200
2. **参考图**：首帧图尺寸建议 ≤ 1280px 边长（GitHub 上传分支上传**原图不压缩**；仅未配置 PAT 的 data-URI 兜底才压缩为 JPEG quality 85，正常流水线走不到）
3. **轮询超时**：`pipeline.py` 的 `_run_poll` 子进程 timeout=1800s 已覆盖最坏情况（retry 5次×~100s 但实际压缩后 30s-2min 应返回）
4. **日志**：若 shot 持续 pending，检查 `poll_only.log` 的 GitHub 上传日志和 Agnes 返回的原始错误

<!-- skill ends here -->

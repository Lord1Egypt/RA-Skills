## 免费模型配置要求清单

免费模型配置每种任务类型的"零件清单"——必选/可选组件、组装顺序、领域约束。按清单逐项产出。

---

### 前置要求：模型基线核对

> 执行任何任务前先核对模型基线。规则见 `SKILL.md`「信息新鲜度」；本节提供核对入口与命令。基准日以 `SKILL.md` 基线表为准（`YYYY-MM-DD`，超过 30 天须重新核对）。

#### 1. 核对入口

| 平台 | 官方模型页 | 模型列表端点 | 定价 / 公告 |
|------|-----------|-------------|------------|
| Agnes AI | https://agnes-ai.com/en/docs/overview | https://apihub.agnes-ai.com/v1/models | https://agnes-ai.com/en/docs/pricing |
| 智谱 BigModel | https://docs.bigmodel.cn/cn/guide/start/model-overview | https://open.bigmodel.cn/api/paas/v4/models | https://docs.bigmodel.cn/cn/guide/start/pricing |
| 商汤 SenseNova | https://platform.sensenova.cn/docs | https://token.sensenova.cn/v1/models | 平台控制台账单页 |
| 小红书 dots | https://dots.ai/platform/apikeys | https://note3-prev-api.askdiandian.com/v1/models | 平台公告 |
| 美团 LongCat | https://longcat.chat/platform/docs | https://api.longcat.chat/openai/v1/models | 平台控制台 |
| 小米 MiMo | https://mimo.mi.com/docs/zh-CN/quick-start/summary/model | https://token-plan-cn.xiaomimimo.com/v1/models | https://mimo.mi.com/docs/zh-CN/updates/deprecate |

> 端点不带鉴权时可能返回 401：属正常，改用官方模型页核对，不要据此判定模型不存在。

#### 2. 快速核对命令

```bash
# 1) 列出端点自报的现役模型（无鉴权也可能可用）
curl -s https://note3-prev-api.askdiandian.com/v1/models | head -c 500

# 2) 带鉴权查询（其余平台）
curl -s https://apihub.agnes-ai.com/v1/models -H "Authorization: Bearer $KEY" | head -c 500

# 3) 单模型存活探测（最可靠）
curl -s -o /dev/null -w "%{http_code}\n" https://open.bigmodel.cn/api/paas/v4/chat/completions \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"glm-4.7-flash","messages":[{"role":"user","content":"ping"}],"max_tokens":1}'
```

判定：`200` 存活；`404/model not found` 已停用；`400` 参数不兼容（接口改版）；`401` 鉴权方式或 Key 有误。

#### 3. 核对后的处理

- 免费模型可保留旧版本；付费模型只保留最新版本；不写版本迁移/停用历史，必要时只标「旧版 ID 已停用」
- 更新 `SKILL.md` 平台基线表与 MF2/MF3 各表，同步脚本常量
- 复核日期与排序调整记录在 `SKILL.md` 基线表（只记状态）

---

### MF1 需求分析域

#### MF1-01 模型类型识别

- **必选组件**: 用户输入分析、模型类型判定（文本生成/图像生成/视频生成等）、类型理由
- **可选组件**: 类型切换建议（如用户需求更适合其他类型）
- **组装顺序**: 用户输入接收 → 关键词提取 → 类型匹配 → 类型确认
- **约束**: 必须准确识别模型类型，不可混淆不同类型的模型
- **格式**: 模型类型报告（Markdown）

#### MF1-02 使用场景分析

- **必选组件**: 使用场景识别、需求分析、能力要求
- **可选组件**: 场景优化建议、替代方案
- **组装顺序**: 场景识别 → 需求分析 → 能力匹配 → 场景确认
- **约束**: 必须准确理解用户的使用场景
- **格式**: 场景分析报告（Markdown）

#### MF1-03 需求提取

- **必选组件**: 关键信息提取、需求整理、需求确认
- **可选组件**: 需求优先级、需求依赖关系
- **组装顺序**: 信息提取 → 需求整理 → 需求确认
- **约束**: 必须完整提取用户需求
- **格式**: 需求清单（Markdown 表格）

---

### MF2 模型选择域

#### MF2-01 平台选择

- **必选组件**: 平台列表、平台能力对比、平台选择理由
- **可选组件**: 平台优缺点分析、平台推荐
- **前置校验**: 先看 `SKILL.md` 基线表的复核日期，距今天 ≥30 天或模型存疑时，按本文「前置要求」的核对入口联网核对；基线与实测不一致时先更新基线再选型
- **组装顺序**: 联网校验 → 需求分析 → 平台扫描 → 能力对比 → 平台选择
- **约束**: 必须根据需求选择合适的平台
- **格式**: 平台选择记录（Markdown）
- **自动推荐规则**:
  - 图像生成 → Agnes AI (agnes-image-2.5-flash)；备选 智谱 cogview-3-flash（免费）
  - 视频生成 → Agnes AI (agnes-video-2.5-flash，720P 限时免费)；需要 1080P/2K 用 agnes-video-2.5（$0.025–0.055/秒）；备选 智谱 cogvideox-flash
  - 文本生成 → 从 models.json 中选第一个可用模型；新装建议 agnes-3.0-flash（免费、1M 上下文）或 glm-4.7-flash
  - 超长上下文 / 图文混合 → 小红书 dots3-note-prev（512K，多模态输入）
  - 展示推荐理由，询问用户是否接受或自行选择

#### MF2-02 能力匹配

- **必选组件**: 模型能力列表、需求匹配度分析、匹配结果
- **可选组件**: 能力差距分析、替代方案
- **组装顺序**: 能力扫描 → 需求匹配 → 匹配度分析 → 匹配确认
- **约束**: 必须确保模型能力满足需求
- **格式**: 能力匹配报告（Markdown）

#### MF2-03 配置生成

- **必选组件**: 配置模板、配置参数、配置生成逻辑
- **可选组件**: 配置验证、配置优化
- **组装顺序**: 模板选择 → 参数填充 → 配置生成 → 配置验证
- **约束**: 配置必须准确无误
- **格式**: 配置文件（JSON）

#### MF2-04 参数设置

- **必选组件**: 参数列表、参数值、参数说明
- **可选组件**: 参数默认值、参数范围、参数建议
- **组装顺序**: 参数识别 → 参数设置 → 参数验证
- **约束**: 参数必须在有效范围内
- **格式**: 参数配置（JSON）
- **视频参数范围（Video 2.5）**: `seconds` 取 `"4"`–`"12"`（字符串，默认 `"5"`）；`size` ∈ {720P, 1080P, 1K, 2K}；`aspect_ratio` 支持 16:9 / 9:16 / 1:1 / 4:3 / 3:4 / 21:9 等；`n` 固定 1
- **视频自动推荐规则**:
  - 用户要求「最长单段」→ 720P, `seconds "12"`
  - 用户要求「高质量」→ 2K（或 1080P）, `seconds "8"`
  - 用户要求「快速 / 低成本」→ agnes-video-2.5-flash, 720P, `seconds "4"`
  - 默认 → 720P, `seconds "5"`, 16:9
  - 需要超过 12 秒 → `long-video` 分段（每段 ≤12 秒）后 `concat`
  - 展示推荐参数和理由，询问用户是否接受或自定义
- **已废弃参数**: `width` / `height` / `fps` / `num_frames` / `quality` / `num_inference_steps` 传入即 400；`negative_prompt` 已不在官方参数表，用正向 prompt 描述替代

---

### MF3 配置生成域

#### MF3-01 API Key 生成

- **必选组件**: 平台后台网址、API Key 生成步骤、API Key 保存
- **可选组件**: API Key 权限设置、API Key 轮换策略
- **组装顺序**: 平台登录 → 后台访问 → API Key 生成 → API Key 保存
- **约束**: API Key 必须从官方后台网址生成
- **格式**: API Key 信息（Markdown）

#### MF3-02 接口配置

- **必选组件**: 接口地址、接口参数、接口配置
- **可选组件**: 接口测试、接口验证
- **组装顺序**: 接口识别 → 参数配置 → 接口配置 → 接口验证
- **约束**: 接口地址必须准确无误
- **格式**: 接口配置（JSON）

#### MF3-03 模型配置

- **必选组件**: 模型名称、模型配置、配置文件
- **可选组件**: 配置验证、配置测试
- **组装顺序**: 模型识别 → 配置生成 → 配置文件 → 配置验证
- **约束**: 配置必须完整准确
- **格式**: 模型配置文件（JSON）
- **图像生成特殊约束**: response_format 必须放在 extra_body 中，放顶层会 400 错误

#### MF3-04 通用配置模板

- **必选组件**: 通用配置内容（环境变量 + JSON 台账）、使用说明、保存位置
- **可选组件**: 字段映射示例、目标写入（`scripts/apply_config.py`，默认预演）、模板验证、模板测试
- **组装顺序**: 模板准备 → 字段映射 → 内容填充 → 使用说明 → 保存验证
- **约束**: 模板必须完整准确，API Key 必须脱敏；只写通用字段，扩展字段可省略
- **格式**: JSON 台账 + `.env` 片段 + Markdown 说明
- **通用字段**: `id`/`model`（模型 ID）、`name`、`base_url`/`url`、`api_key`/`apiKey`、能力开关（`supports*`，不支持可省略）

#### MF3-05 API 配置规范

- **必选组件**: API 端点、请求参数、约束条件
- **可选组件**: 调用示例、错误处理
- **组装顺序**: API 识别 → 参数配置 → 约束设置 → 验证测试
- **约束**: API 配置必须准确无误，约束条件必须明确
- **格式**: API 配置文档（Markdown）
- **Agnes AI 视频生成特殊约束（Video 2.5）**:
  - 核心参数：`seconds`（"4"–"12"）、`size`（720P/1080P/1K/2K）、`aspect_ratio`、`mode`（text/keyframe/reference）
  - 禁用参数：`width` / `height` / `fps` / `num_frames` / `quality` / `num_inference_steps`，传入即 400
  - 轮询：`GET /agnesapi?video_id=<ID>&model_name=<模型>`；keyframe / reference 模式**必须**带 model_name，text 模式可省略
  - 创建返回里 `id` / `task_id` 是任务号，`video_id` 才是查询凭证，不要拿 task_id 去查
  - 图生视频走 `mode=keyframe` + `first_frame`（或 `last_frame`），图片必须是公网 URL，本地文件需先上传
  - 多模态参考走 `mode=reference` + `images` / `audios` / `videos[]`（视频参考必须用 `videos[].url`）
  - 创建任务超时 600 秒；轮询间隔 1–2 秒，超时 30 秒并重试；生成通常 1–5 分钟
  - 计费 = 输出秒数 × 分辨率单价 + 输入视频秒数 × 单价；前 5 张参考图免费（第 6 张起 $0.005/张）
  - **长视频生成**: 使用 `long-video` 子命令按秒分段（每段 ≤12 秒）+ 拼接，不再按帧数分段
  - **视频拼接**: 使用 `concat` 子命令拼接多个视频，优先用 ffmpeg，无则回退纯 Python
  - **图片转视频**: 使用 `images-video` 子命令，每张图作为 keyframe 首帧生成一段再拼接
  - **故事板视频**: 使用 `story-video` 子命令，场景用 `seconds` 而非 `frames`

---

#### Agnes AI 多模态生成能力详细说明

Agnes AI 特有的多模态生成能力，包括图像生成和视频生成。

**架构设计**：基本命令组合复杂命令
- **基本命令**（原子操作）：`image`、`video`、`concat`
- **复杂命令**（组合而成）：`long-video`、`images-video`、`story-video`

##### 图像生成能力（Agnes Image 2.5 Flash）

- **文生图**：文本 → 图片
- **图生图**：图片 → 图片（编辑、风格转换）
- **多图合成**：多张参考图 → 一张合成图（`extra_body.image` 数组）
- **分辨率档位**：`size` 取 `1K`/`2K`/`3K`/`4K` 配合 `ratio`（1:1、3:4、4:3、16:9、9:16、2:3、3:2、21:9）；旧式 `1024x768` 仍兼容但可能被归一化
- **免费状态**：试用期所有输出档位与输入参考图均为 $0

##### 视频生成能力（Agnes Video 2.5）

**基础能力**：文生视频、首尾帧控制（keyframe）、多模态参考（reference：图片/音频/视频）、音画同步

###### 基本命令

| 命令 | 功能 | 组合关系 |
|------|------|----------|
| `image` | 图像生成 | 原子操作 |
| `video` | 视频生成 | 原子操作 |
| `concat` | 视频拼接 | 原子操作 |

###### 复杂命令（由基本命令组合）

| 命令 | 功能 | 组合关系 |
|------|------|----------|
| `long-video` | 同 prompt 自动分段长视频 | `video` × N + `concat` |
| `images-video` | 批量图 → 批量视频 → 拼接 | `video` × N + `concat` |
| `story-video` | 故事板全流程 | `image` × N + `video` × N + `concat` |

###### 使用示例

```bash
###### 基本命令
python agnes_gen.py image --prompt "描述" --size 2K --ratio 16:9 --output result.png
python agnes_gen.py video --prompt "描述" --seconds 5 --size 720P --aspect-ratio 16:9 --output result.mp4
python agnes_gen.py concat --inputs a.mp4 b.mp4 --output long.mp4

###### 复杂命令（由基本命令组合）
python agnes_gen.py long-video --prompt "描述" --segments 3 --segment-seconds 10 --output long.mp4
python agnes_gen.py images-video --images img1.png img2.png --prompt "描述" --seconds 5 --output result.mp4
python agnes_gen.py story-video --storyboard storyboard.json --output story.mp4
```

##### 命令参数

###### image 命令
- `--prompt`：图像描述（必选）
- `--image`：输入图片 URL（图生图/多图合成，可选，可多值）
- `--size`：`1K` / `2K` / `3K` / `4K`（默认 `1K`；旧式 `1024x768` 兼容）
- `--ratio`：画幅比例（默认 1:1），如 16:9
- `--output`：输出文件路径

###### video 命令
- `--prompt`：视频描述（必选）
- `--image`：首帧图片 URL 或本地路径（自动转 `mode=keyframe` + `first_frame`）
- `--seconds`：时长 `"4"`–`"12"`（默认 `"5"`）
- `--size`：`720P` / `1080P` / `1K` / `2K`（默认 `720P`）
- `--aspect-ratio`：`16:9` / `9:16` / `1:1` / `4:3` / `3:4` / `21:9`（默认 `16:9`）
- `--mode`：`text` / `keyframe` / `reference`（默认按是否给图自动判断）
- `--first-frame` / `--last-frame`：keyframe 模式首/尾帧公网 URL
- `--model`：`agnes-video-2.5`（默认）或 `agnes-video-2.5-flash`
- `--seed`：随机种子（可选）
- `--output`：输出视频文件路径
- 兼容参数（已废弃，自动换算并告警）：`--width` `--height` `--frames` `--fps`

###### concat 命令
- `--inputs`：输入视频文件列表（必选）
- `--output`：输出视频文件路径（必选）

###### long-video 命令
- `--prompt`：视频描述（必选）
- `--image`：首帧图片 URL 或本地路径（可选）
- `--segments`：分段数量（必选）
- `--segment-seconds`：每段时长 `"4"`–`"12"`（默认 `"10"`）
- `--size` / `--aspect-ratio` / `--model` / `--seed` / `--output`

###### images-video 命令
- `--images`：锚点图片列表（必选，逐张作为 keyframe 首帧）
- `--prompt`：视频描述（所有图片共享，必选）
- `--prompts`：每张图片的独立描述（可选，与 --images 一一对应）
- `--seconds`：每段时长（默认 `"5"`）
- `--size` / `--aspect-ratio` / `--seed` / `--output`

###### story-video 命令
- `--storyboard`：故事板 JSON 文件路径（必选）
- `--size` / `--aspect-ratio` / `--seed` / `--output`

###### 视频参数范围（Video 2.5）

| 参数 | 取值 | 说明 |
|------|------|------|
| seconds | `"4"`–`"12"`（字符串） | 单段时长，默认 `"5"` |
| size | `720P` / `1080P` / `1K` / `2K` | 分辨率档位，不接受像素值 |
| aspect_ratio | `16:9`、`9:16`、`1:1`、`4:3`、`3:4`、`21:9` 等 | 不支持 `auto` |
| n | 1 | 仅支持单条 |
| mode | `text` / `keyframe` / `reference` | 媒体字段必须与 mode 匹配 |
| first_frame / last_frame | 公网 URL | keyframe 模式，二选一或都给 |
| images / audios / videos[] | 公网 URL 数组 | reference 模式，视频用 `videos[].url` |

###### 自动推荐规则

- 用户要求「最长单段」→ 720P, `seconds "12"`
- 用户要求「高质量」→ 2K（或 1080P）, `seconds "8"`
- 用户要求「快速 / 低成本」→ `agnes-video-2.5-flash`, 720P, `seconds "4"`
- 默认 → 720P, `seconds "5"`, 16:9
- 需要 >12 秒 → `long-video` 分段（每段 ≤12 秒）再 `concat`

###### 故事板 JSON 格式

```json
{
  "base_prompt": "基础描述（所有场景共享）",
  "style": "风格描述（所有场景共享）",
  "seed": 12345,
  "image_size": "2K",
  "scenes": [
    {
      "prompt": "场景1描述",
      "image": "可选：已有图片URL或本地路径",
      "seconds": "8"
    },
    {
      "prompt": "场景2描述",
      "seconds": "10"
    }
  ]
}
```

> `story-video` 是万能入口：场景有 `image` 则跳过生图，无 `image` 则自动生成。支持 `base_prompt` / `style` / `seed` 保持一致性。

---

### MF4 配置应用域

#### MF4-01 配置导入

- **必选组件**: 配置文件、导入工具、导入步骤
- **可选组件**: 导入验证、导入日志
- **组装顺序**: 配置准备 → 导入工具 → 配置导入 → 导入验证
- **约束**: 配置必须正确导入
- **格式**: 导入结果（Markdown）

#### MF4-02 配置验证

- **必选组件**: 验证方法、验证步骤、验证结果
- **可选组件**: 验证报告、验证建议
- **组装顺序**: 验证准备 → 验证执行 → 验证结果 → 验证确认
- **约束**: 配置必须通过验证
- **格式**: 验证报告（Markdown）

#### MF4-03 配置更新

- **必选组件**: 更新原因、更新内容、更新步骤
- **可选组件**: 更新验证、更新回滚
- **组装顺序**: 联网核对 → 更新识别 → 更新准备 → 更新执行 → 更新验证
- **约束**: 更新必须不影响现有功能
- **巡检触发**: 距基线复核 ≥30 天、出现 404/400/401 模型类报错、平台发布下线公告、用户反馈失效
- **巡检动作**: 按「前置要求」核对官方模型页与 `{base}/models` → 更新主表/脚本常量/排序 → 回写 `SKILL.md` 基线表复核日期（只记状态，不写版本迁移）
- **格式**: 更新记录（Markdown）

---

### MF5 使用指导域

#### MF5-01 使用方法说明

- **必选组件**: 使用步骤、使用示例、使用注意事项
- **可选组件**: 使用技巧、使用最佳实践
- **组装顺序**: 使用准备 → 使用步骤 → 使用示例 → 使用确认
- **约束**: 使用说明必须清晰易懂
- **格式**: 使用说明（Markdown）
- **图像/视频生成**: 必须通过脚本 `scripts/agnes_gen.py` 使用，示例中需包含脚本命令
- **选型说明**: 使用前完成联网校验，说明中给出官方文档链接与复核日期

#### MF5-02 注意事项提醒

- **必选组件**: 注意事项列表、风险提示、解决建议
- **可选组件**: 常见问题、故障排除
- **组装顺序**: 风险识别 → 注意事项 → 风险提示 → 解决建议
- **约束**: 必须提醒用户重要注意事项
- **格式**: 注意事项（Markdown）
- **视频生成特殊注意**: 轮询用 `video_id` + `model_name`（不是 `task_id`）；图片必须是公网 URL 而非 data URI；`seconds` 限 4–12 秒；`size` 只能取 720P/1080P/1K/2K；`width`/`height`/`fps`/`num_frames` 传入即 400
- **视频生成常见问题**: 400（用了旧参数或 media 与 mode 不匹配）、404 video not exist（拿 task_id 去查）、401（认证头格式错误，dots 平台只认 `api-key`）、429（限流，需退避）
- **时效提醒**: 免费政策、模型 ID、限流随时可能变化；交付时必须注明复核日期与官方文档链接，禁止把免费承诺写成长期保证

#### MF5-03 最佳实践

- **提示词编写**:
  - 使用英文提示词效果更好
  - 提示词需要详细、具体，包含场景、动作、表情、服装、灯光等要素
  - 示例："A group of people celebrating a festival in a city square, cheering joyfully, colorful banners and lanterns overhead, all wearing festive clothing, dramatic lighting, detailed scene, realistic style"

- **图片上传问题**:
  - 图片上传到 catbox.moe 或 litterbox 可能超时或失败
  - 备选方案：直接从文本生成视频，不依赖图片
  - 如果必须使用图片，可尝试多次上传或使用其他托管服务

- **音频生成**:
  - **简单音频合成**（无AI模型）：使用 Python wave 模块生成简单音频，适用于喊叫声、背景音效
  - **TTS语音合成**（需要AI模型）：使用 edge-tts、pyttsx3、gTTS 等生成真正的语音
  - **推荐方案**：edge-tts（免费、中文效果好）
    - 安装：`pip install edge-tts`
    - 单人配音：`edge-tts --voice zh-CN-YunxiNeural --text "你好，欢迎使用语音合成" --output speech.mp3`
    - 多人配音：使用不同声音生成多段语音，然后混合
  - **多人配音脚本**：见 scripts/generate_tts_audio.py

- **视频音频合并**:
  - 需要 ffmpeg 工具（系统工具）
  - 脚本：`scripts/merge_audio_video.py`
  - 命令：`python merge_audio_video.py --video video.mp4 --audio audio.wav --output final.mp4 --mode replace`
  - 如果没有 ffmpeg，可使用其他视频编辑软件

---

### MF6 多模态生成域（Agnes AI 特有）

#### MF6-01 图像生成

- **必选组件**: 提示词、输出路径、分辨率档位
- **可选组件**: 输入图片（图生图/多图合成）、画幅比例、随机种子
- **组装顺序**: 需求分析 → 提示词编写 → 参数设置 → 图像生成 → 结果验证
- **约束**: 必须通过脚本 `scripts/agnes_gen.py` 使用；模型为 `agnes-image-2.5-flash`
- **格式**: 图像文件（PNG/JPG）
- **脚本命令**: `python agnes_gen.py image --prompt "描述" --size 2K --ratio 16:9 --output result.png`
- **最佳实践**:
  - 使用英文提示词效果更好
  - 提示词需要详细、具体
  - 默认 `1K`（1024×1024 级）；要精确画幅用 `--size 2K --ratio 16:9`

#### MF6-02 视频生成

- **必选组件**: 提示词、输出路径、时长、分辨率档位、画幅
- **可选组件**: 首帧/尾帧图片、参考图/音频/视频、随机种子
- **组装顺序**: 需求分析 → 提示词编写 → 参数设置 → 视频生成 → 结果验证
- **约束**: 必须通过脚本 `scripts/agnes_gen.py` 使用；单段时长 4–12 秒
- **格式**: 视频文件（MP4）
- **脚本命令**: `python agnes_gen.py video --prompt "描述" --seconds 5 --size 720P --aspect-ratio 16:9 --output result.mp4`
- **最佳实践**:
  - 生成通常 1–5 分钟，轮询间隔 1–2 秒
  - 需要 12 秒以上用 `long-video` 分段后拼接
  - 免费通道是 `agnes-video-2.5-flash`（720P，限时免费）；高清走 `agnes-video-2.5`（按秒计费）

#### MF6-03 视频拼接

- **必选组件**: 输入视频列表、输出路径
- **可选组件**: 无
- **组装顺序**: 视频准备 → 拼接执行 → 结果验证
- **约束**: 至少需要 2 个视频文件
- **格式**: 视频文件（MP4）
- **脚本命令**: `python agnes_gen.py concat --inputs a.mp4 b.mp4 --output long.mp4`
- **最佳实践**:
  - 优先使用 ffmpeg 拼接
  - 如果没有 ffmpeg，回退到纯 Python 拼接

#### MF6-04 音频生成（简单合成）

- **必选组件**: 输出路径、时长
- **可选组件**: 频率成分、振幅成分、采样率
- **组装顺序**: 需求分析 → 参数设置 → 音频生成 → 结果验证
- **约束**: 无 AI 模型，只能生成简单合成音频
- **格式**: 音频文件（WAV）
- **脚本命令**: `python generate_audio.py --output shout.wav --duration 5.0`
- **最佳实践**:
  - 适用于生成喊叫声、背景音效
  - 可自定义频率和振幅
  - 无法生成语音，需要 TTS 工具

#### MF6-05 TTS配音

- **必选组件**: 文本内容、输出路径、声音选择
- **可选组件**: 多声音混合、语速、音调
- **组装顺序**: 需求分析 → 声音选择 → 文本准备 → TTS生成 → 结果验证
- **约束**: 需要安装 edge-tts 或其他 TTS 库
- **格式**: 音频文件（MP3/WAV）
- **脚本命令**: `python generate_tts_audio.py --text "你好，欢迎使用语音合成" --output speech.mp3`
- **最佳实践**:
  - 推荐使用 edge-tts（免费、中文效果好）
  - 安装：`pip install edge-tts`
  - 单人配音：`edge-tts --voice zh-CN-YunxiNeural --text "你好，欢迎使用语音合成" --output speech.mp3`
  - 多人配音：使用不同声音生成多段语音，然后混合

#### MF6-06 音视频合并

- **必选组件**: 视频文件、音频文件、输出路径
- **可选组件**: 合并模式（替换/混合）
- **组装顺序**: 文件准备 → 合并模式选择 → 合并执行 → 结果验证
- **约束**: 需要 ffmpeg 工具（系统工具）
- **格式**: 视频文件（MP4）
- **脚本**: `scripts/merge_audio_video.py`
- **命令**:
  - 替换模式：`python merge_audio_video.py --video video.mp4 --audio audio.wav --output final.mp4 --mode replace`
  - 混合模式：`python merge_audio_video.py --video video.mp4 --audio audio.wav --output final.mp4 --mode mix`
- **最佳实践**:
  - 先检查原视频是否有音频
  - 根据需求选择替换或混合模式
  - 如果没有 ffmpeg，可使用其他视频编辑软件

---

#### 免费模型列表

本技能包含以下免费模型的配置：

##### Sapiens AI——Agnes AI
- 后台网址：https://platform.agnes-ai.com/settings/apiKeys
- 接口地址：https://apihub.agnes-ai.com/v1
- API Key：从后台网址生成
- 文本模型：agnes-3.0-flash（推荐，1M 上下文，免费）、agnes-2.5-flash（512K，免费）、agnes-2.5-pro（付费）
- 图像生成：agnes-image-2.5-flash（试用期全档位免费）
- 视频生成：agnes-video-2.5-flash（720P 限时免费）、agnes-video-2.5（720P/1080P/1K/2K 按秒计费）
- 能力：文本生成、图像生成/编辑/多图合成、视频生成（文生/首尾帧/多模态参考）、音画同步

##### 智谱——BigModel
- 后台网址：https://open.bigmodel.cn/apikey/platform
- 接口地址：https://open.bigmodel.cn/api/paas/v4
- API Key：从后台网址生成
- **免费性质：部分免费**——仅"Free/Flash"档为免费模型，旗舰、OCR、TTS/ASR 均付费
- 免费文本模型：glm-4.7-flash（推荐，200K）、glm-4.5-flash、glm-4-flash-250414
- 免费视觉模型：glm-4.6v-flash、glm-4.1v-thinking-flash、glm-4v-flash
- 免费图像：cogview-3-flash；免费视频：cogvideox-flash
- 旗舰（付费，可作为升级项）：glm-5.3、glm-5.3-flash（0.8/2.8 元每百万 token）、glm-5.3-flashx
- 能力：文本生成、视觉理解、图像生成、视频生成、OCR、TTS/ASR

##### 商汤科技日日新——SenseNova
- 后台网址：https://platform.sensenova.cn/console/keys
- 接口地址：https://token.sensenova.cn/v1
- API Key：从后台网址生成
- 计费：积分池制（公测期 5 小时 12 万积分 / 周 120 万积分），不是"按模型免费"
- 模型名称：sensenova-6.8-flash（推荐，正式版，1M 上下文）、sensenova-6.8-flash-lite、sensenova-u1.5-fast、sensenova-u1.5-lite、deepseek-flash（DeepSeek V4.1 Flash）、deepseek-v4-pro、glm-5.2、kimi-k3
- 能力：文本/多模态对话（6.8-flash）、图像生成与编辑（u1.5 系列）、对话推理（deepseek / glm / kimi）
- 注意：图像模型使用 u1.5 系列；生图链接有效期 24 小时

##### 小红书——dots studio
- 后台网址：https://dots.ai/platform/apikeys
- 接口地址：https://note3-prev-api.askdiandian.com/v1（OpenAI 兼容）
- API Key：从后台网址生成
- 模型名称：dots3-note-prev（推荐，主）、dots_webdev_1022（端点自报，官方文档未说明）
- 规格：512K 上下文（524288）、最大输出 64K，输入 + max_tokens 不得超过 524288；支持文本/图片（部分来源称支持音视频）输入、工具调用、思考模式（`thinking: {type: enabled}`，推理内容在 `reasoning_content`）
- 能力：长上下文理解、多模态理解、Agent 工具调用
- **认证（关键）**：请求头为 `api-key: YOUR_KEY`，不是 `Authorization: Bearer`；填错会 401
- 限流：文档当前为 60 RPM / 150 万 TPM（按 Key 计，预览期可能调整）
- 注意：预览期限时免费，官方仅承诺"恢复收费前提前告知"，不要写进生产方案

##### 美团——LongCat
- 后台网址：https://longcat.chat/platform/api_keys
- 接口地址：https://api.longcat.chat/openai（OpenAI 兼容）
- API Key：从后台网址生成
- 模型名称：LongCat-2.5（推荐，1M 上下文 / 256K 输出，原生多模态）
- 能力：文本生成、视觉理解、Agentic 编程

##### 小米——MIMO
- 后台网址：https://platform.xiaomimimo.com/console/api-keys
- 接口地址：https://token-plan-cn.xiaomimimo.com/v1
- API Key：从后台网址生成
- 文本/全模态：mimo-v2.6-pro（推荐）、mimo-v2.6-flash、mimo-v2.6-pro-ultraspeed（1M 上下文 / 128K 输出）
- 语音：mimo-v2.5-asr、mimo-v2.5-tts、mimo-v2.5-tts-voiceclone、mimo-v2.5-tts-voicedesign
- 能力：文本生成、全模态理解、深度思考、语音识别、语音合成
- 注意：旧版 ID 已停用，按上表配置；v2.6 思考模式不支持自定义 temperature/top_p；免费以新客额度 + Token Plan 为主

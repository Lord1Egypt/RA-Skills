## 免费模型配置要求清单

免费模型配置每种任务类型的"零件清单"——必选/可选组件、组装顺序、领域约束。按清单逐项产出。

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
- **组装顺序**: 需求分析 → 平台扫描 → 能力对比 → 平台选择
- **约束**: 必须根据需求选择合适的平台
- **格式**: 平台选择记录（Markdown）
- **自动推荐规则**:
  - 图像生成 → Agnes AI (agnes-image-2.0-flash)
  - 视频生成 → Agnes AI (agnes-video-v2.0)
  - 文本生成 → 从 models.json 中选第一个可用模型
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
- **视频参数范围**: num_frames 按分辨率受限（1080p ≤169、720p ≤409、480p ≤961），frame_rate 1-60
- **自动推荐规则**:
  - 用户要求「最长视频」→ 480p (854×480), 961帧, 24fps (~40秒)
  - 用户要求「高质量」→ 720p (1088×832), 409帧, 24fps (~17秒)
  - 用户要求「快速生成」→ 1080p (1920×1080), 169帧, 24fps (~7秒)
  - 默认 → 720p (1088×832), 121帧, 24fps (~5秒)
  - 展示推荐参数和理由，询问用户是否接受或自定义

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

#### MF3-04 WorkBuddy 模板

- **必选组件**: 模板内容、使用说明、保存位置
- **可选组件**: 模板验证、模板测试
- **组装顺序**: 模板准备 → 内容填充 → 使用说明 → 保存验证
- **约束**: 模板必须完整准确，API Key 必须脱敏
- **格式**: JSON 模板文件

#### MF3-05 API 配置规范

- **必选组件**: API 端点、请求参数、约束条件
- **可选组件**: 调用示例、错误处理
- **组装顺序**: API 识别 → 参数配置 → 约束设置 → 验证测试
- **约束**: API 配置必须准确无误，约束条件必须明确
- **格式**: API 配置文档（Markdown）
- **Agnes AI 视频生成特殊约束**:
  - num_frames 按分辨率受限：1080p ≤169、720p ≤409、480p ≤961，需满足 8n+1
  - 轮询使用 `task_id`（格式 `task_xxx`），不要使用 `video_id`（litellm 包装 ID）
  - 图生视频 `image` 参数必须是公网 URL，本地文件需先上传
  - 创建任务超时建议 600 秒，轮询超时 30 秒并自动重试
  - 推荐轮询间隔 10 秒，生成通常需要 3-10 分钟
  - **长视频生成**: 使用 `long-video` 子命令自动分段生成 + 拼接，每段自动使用该分辨率下的最大帧数
  - **视频拼接**: 使用 `concat` 子命令拼接多个视频，优先用 ffmpeg，无则回退纯 Python
  - **图片转视频**: 使用 `images-video` 子命令，已有锚点图片直接生成视频并拼接，支持统一 prompt 或每图独立 prompt
  - **故事板视频**: 使用 `story-video` 子命令，通过 JSON 故事板定义场景，支持一致性控制（base_prompt、style、seed），自动批量生成锚点图片 → 分段视频 → 拼接

---

#### Agnes AI 多模态生成能力详细说明

Agnes AI 特有的多模态生成能力，包括图像生成和视频生成。

**架构设计**：基本命令组合复杂命令
- **基本命令**（原子操作）：`image`、`video`、`concat`
- **复杂命令**（组合而成）：`long-video`、`images-video`、`story-video`

##### 图像生成能力（Agnes Image 2.0 Flash）

- **文生图**：文本 → 图片
- **图生图**：图片 → 图片（编辑、风格转换）

##### 视频生成能力（Agnes Video V2.0）

**基础能力**：文生视频、图生视频、关键帧动画、场景运动控制

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
python agnes_gen.py image --prompt "描述" --output result.png
python agnes_gen.py video --prompt "描述" --output result.mp4
python agnes_gen.py concat --inputs a.mp4 b.mp4 --output long.mp4

###### 复杂命令（由基本命令组合）
python agnes_gen.py long-video --prompt "描述" --segments 3 --output long.mp4
python agnes_gen.py images-video --images img1.png img2.png --prompt "描述" --output result.mp4
python agnes_gen.py story-video --storyboard storyboard.json --output story.mp4
```

##### 命令参数

###### image 命令
- `--prompt`：图像描述（必选）
- `--image`：输入图片 URL（图生图，可选）
- `--size`：分辨率，如 1024x768（默认）
- `--output`：输出文件路径

###### video 命令
- `--prompt`：视频描述（必选）
- `--image`：输入图片 URL 或本地路径（图生视频，可选）
- `--width`：视频宽度（默认 1152）
- `--height`：视频高度（默认 768）
- `--frames`：总帧数（默认 121，需满足 8n+1）
- `--fps`：帧率 1-60（默认 24）
- `--seed`：随机种子（可选）
- `--negative-prompt`：负面提示词（可选）
- `--output`：输出视频文件路径

###### concat 命令
- `--inputs`：输入视频文件列表（必选）
- `--output`：输出视频文件路径（必选）

###### long-video 命令
- `--prompt`：视频描述（必选）
- `--image`：输入图片 URL 或本地路径（可选）
- `--width`：视频宽度（默认 1088）
- `--height`：视频高度（默认 832）
- `--fps`：帧率 1-60（默认 24）
- `--segments`：分段数量（必选）
- `--seed`：随机种子（可选）
- `--negative-prompt`：负面提示词（可选）
- `--output`：输出视频文件路径（必选）

###### images-video 命令
- `--images`：锚点图片列表（必选）
- `--prompt`：视频描述（所有图片共享，必选）
- `--prompts`：每张图片的独立描述（可选，与 --images 一一对应）
- `--width`：视频宽度（默认 1088）
- `--height`：视频高度（默认 832）
- `--fps`：帧率 1-60（默认 24）
- `--frames`：每段帧数（0=自动使用最大值）
- `--seed`：随机种子（可选）
- `--output`：输出视频文件路径（必选）

###### story-video 命令
- `--storyboard`：故事板 JSON 文件路径（必选）
- `--width`：视频宽度（默认 1088）
- `--height`：视频高度（默认 832）
- `--fps`：帧率 1-60（默认 24）
- `--seed`：随机种子（可选）
- `--output`：输出视频文件路径（必选）

###### 视频参数范围

帧数按分辨率受限：
- 1080p (1920×1080)：≤169 帧
- 720p (1088×832)：≤409 帧
- 480p (854×480)：≤961 帧

帧数需满足 8n+1 格式。

###### 自动推荐规则

- 用户要求「最长视频」→ 480p (854×480), 961帧, 24fps (~40秒)
- 用户要求「高质量」→ 720p (1088×832), 409帧, 24fps (~17秒)
- 用户要求「快速生成」→ 1080p (1920×1080), 169帧, 24fps (~7秒)
- 默认 → 720p (1088×832), 121帧, 24fps (~5秒)

###### 故事板 JSON 格式

```json
{
  "base_prompt": "基础描述（所有场景共享）",
  "style": "风格描述（所有场景共享）",
  "seed": 12345,
  "image_size": "1024x768",
  "scenes": [
    {
      "prompt": "场景1描述",
      "image": "可选：已有图片URL或本地路径",
      "frames": 121
    },
    {
      "prompt": "场景2描述",
      "frames": 200
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
- **组装顺序**: 更新识别 → 更新准备 → 更新执行 → 更新验证
- **约束**: 更新必须不影响现有功能
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

#### MF5-02 注意事项提醒

- **必选组件**: 注意事项列表、风险提示、解决建议
- **可选组件**: 常见问题、故障排除
- **组装顺序**: 风险识别 → 注意事项 → 风险提示 → 解决建议
- **约束**: 必须提醒用户重要注意事项
- **格式**: 注意事项（Markdown）
- **视频生成特殊注意**: 轮询用 task_id 不用 video_id；图片必须是 URL 不是 data URI；帧数按分辨率受限（1080p ≤169、720p ≤409、480p ≤961）
- **视频生成常见问题**: task_not_exist（用错 ID）、num_frames exceeds maximum（帧数超限）、Invalid base64（图片格式错误）

#### MF5-03 最佳实践

- **提示词编写**:
  - 使用英文提示词效果更好
  - 提示词需要详细、具体，包含场景、动作、表情、服装、灯光等要素
  - 示例："A group of people in fervent worship, kneeling with their backs parallel to the ground, bowing deeply before a proud man named Wang Taiping who stands tall with a得意 expression, all wearing clothing from the same historical era, dramatic lighting, detailed scene, realistic style"

- **图片上传问题**:
  - 图片上传到 catbox.moe 或 litterbox 可能超时或失败
  - 备选方案：直接从文本生成视频，不依赖图片
  - 如果必须使用图片，可尝试多次上传或使用其他托管服务

- **音频生成**:
  - **简单音频合成**（无AI模型）：使用 Python wave 模块生成简单音频，适用于喊叫声、背景音效
  - **TTS语音合成**（需要AI模型）：使用 edge-tts、pyttsx3、gTTS 等生成真正的语音
  - **推荐方案**：edge-tts（免费、中文效果好）
    - 安装：`pip install edge-tts`
    - 单人配音：`edge-tts --voice zh-CN-YunxiNeural --text "王太平" --output speech.mp3`
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

- **必选组件**: 提示词、输出路径、分辨率
- **可选组件**: 输入图片（图生图）、随机种子
- **组装顺序**: 需求分析 → 提示词编写 → 参数设置 → 图像生成 → 结果验证
- **约束**: 必须通过脚本 `scripts/agnes_gen.py` 使用
- **格式**: 图像文件（PNG/JPG）
- **脚本命令**: `python agnes_gen.py image --prompt "描述" --output result.png`
- **最佳实践**:
  - 使用英文提示词效果更好
  - 提示词需要详细、具体
  - 默认分辨率 1024x768

#### MF6-02 视频生成

- **必选组件**: 提示词、输出路径、分辨率、帧数、帧率
- **可选组件**: 输入图片（图生视频）、随机种子、负面提示词
- **组装顺序**: 需求分析 → 提示词编写 → 参数设置 → 视频生成 → 结果验证
- **约束**: 必须通过脚本 `scripts/agnes_gen.py` 使用；帧数按分辨率受限
- **格式**: 视频文件（MP4）
- **脚本命令**: `python agnes_gen.py video --prompt "描述" --output result.mp4`
- **最佳实践**:
  - 视频生成需要较长等待时间（3-10分钟）
  - 帧数按分辨率受限：1080p ≤169、720p ≤409、480p ≤961
  - 帧数需满足 8n+1 格式

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
- **脚本命令**: `python generate_tts_audio.py --text "王太平" --output speech.mp3`
- **最佳实践**:
  - 推荐使用 edge-tts（免费、中文效果好）
  - 安装：`pip install edge-tts`
  - 单人配音：`edge-tts --voice zh-CN-YunxiNeural --text "王太平" --output speech.mp3`
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
- 模型名称：agnes-2.0-flash
- 能力：文本生成（可通过配置使用）
- 图像生成：agnes-image-2.0-flash（仅通过脚本使用）
- 视频生成：agnes-video-v2.0（仅通过脚本使用）

##### 智谱——BigModel
- 后台网址：https://open.bigmodel.cn/apikey/platform
- 接口地址：https://open.bigmodel.cn/api/paas/v4/
- API Key：从后台网址生成
- 模型名称：glm-4.7-flash
- 能力：文本生成

##### 商汤科技日日新——SenseNova
- 后台网址：https://platform.sensenova.cn/console/keys
- 接口地址：https://token.sensenova.cn/v1
- API Key：从后台网址生成
- 模型名称：sensenova-6.7-flash-lite
- 能力：文本生成

##### 小米——MIMO
- 后台网址：https://platform.xiaomimimo.com/console/api-keys
- 接口地址：https://token-plan-cn.xiaomimimo.com/v1
- API Key：从后台网址生成
- 模型名称：mimo-v2.5-pro
- 能力：文本生成

##### 美团——LongCat
- 后台网址：https://longcat.chat/platform/api_keys
- 接口地址：https://api.longcat.chat/openai
- API Key：从后台网址生成
- 模型名称：LongCat-2.0-Preview
- 能力：文本生成

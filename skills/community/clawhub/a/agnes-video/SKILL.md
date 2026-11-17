# Agnes Video V2.0

> 使用 Agnes Video V2.0 模型生成视频。支持文生视频、图生视频、多图视频和关键帧动画。

> **注意**：视频生成采用**异步任务 API**：先创建任务获取 `video_id`，再轮询获取结果。

## 触发条件

当用户需要以下功能时触发此技能：

- **视频生成**：根据文字描述生成高质量视频
- **图片动画**：将静态图片转化为动态视频
- **多图视频**：使用多张参考图片引导视频生成
- **关键帧动画**：在多个关键帧之间生成流畅过渡
- **故事讲述**：短片、角色场景和叙事片段
- **营销视频**：产品广告、宣传视频和推广内容
- **社交媒体内容**：Reels、Shorts、TikTok 风格视频

**触发关键词**：
- "生成视频"、"创建视频"、"做视频"
- "图片动画"、"让图片动起来"
- "关键帧动画"、"过渡动画"
- "文生视频"、"图生视频"、"video generation"
- "动画"、"动态"、"motion"

## 前置条件

API Key 与 Agnes Image 共用同一个环境变量：

```bash
export ANGES_API_KEY="your_api_key_here"
```

或使用替代变量：

```bash
export AGENT_ANGES_API_KEY="your_api_key_here"
```

## 核心能力

| 能力 | 说明 | 工作流 |
|------|------|--------|
| 文生视频 | 通过文本提示词直接生成视频 | `text` |
| 图生视频 | 将静态图片转化为动态视频 | `img2video` |
| 多图视频 | 使用多张参考图片引导视频生成 | `multi` |
| 关键帧动画 | 在多个关键帧之间生成流畅过渡 | `keyframes` |
| 场景运动控制 | 通过提示词控制主体动作、镜头运动 | 提示词 |
| 视觉一致性 | 帧间保持主体、风格和场景一致 | 默认 |
| 电影级输出 | 高质量电影级视频内容 | 默认 |
| 异步 API | 创建任务后再轮询获取生成结果 | 默认 |

## 适用场景

- **故事讲述**：短片、角色场景和叙事片段
- **营销视频**：产品广告、宣传视频和推广内容
- **社交媒体内容**：Reels、Shorts、TikTok 风格视频
- **图片动画**：为肖像、产品、角色或场景添加动画
- **产品演示**：通过文本或图片生成产品展示视频
- **关键帧过渡**：在不同视觉状态之间生成流畅过渡

## 使用方法

### 1. 文生视频 (Text-to-Video)

```bash
./scripts/agnes-video.sh text "prompt" [OUTPUT_FILE]
```

**示例**：

```bash
./scripts/agnes-video.sh text "A cat walking on the beach at sunset, cinematic, golden hour lighting" output.mp4
```

### 2. 图生视频 (Image-to-Video)

```bash
./scripts/agnes-video.sh img2video "prompt" IMAGE_URL [OUTPUT_FILE]
```

**示例**：

```bash
./scripts/agnes-video.sh img2video "The woman slowly turns around and looks back" "https://example.com/photo.jpg" output.mp4
```

### 3. 多图视频 (Multi-Image Video)

```bash
./scripts/agnes-video.sh multi "prompt" IMAGE1 IMAGE2 [OUTPUT_FILE]
```

**示例**：

```bash
./scripts/agnes-video.sh multi "Create a smooth transformation between the two images" "https://example.com/a.png" "https://example.com/b.png" output.mp4
```

### 4. 关键帧动画 (Keyframe Animation)

```bash
./scripts/agnes-video.sh keyframes "prompt" IMAGE1 IMAGE2 [OUTPUT_FILE]
```

**示例**：

```bash
./scripts/agnes-video.sh keyframes "Smooth cinematic transition between keyframes" "https://example.com/kf1.png" "https://example.com/kf2.png" output.mp4
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `workflow` | 是 | 工作流类型：`text` / `img2video` / `multi` / `keyframes` |
| `prompt` | 是 | 视频内容的文本描述 |
| `image` | img2video | 输入图片 URL（单图用此参数） |
| `images` | multi/keyframes | 多张图片 URL 列表 |
| `size` | 否 | 分辨率，默认 `1152x768`（720p 16:9） |
| `duration` | 否 | 视频时长（秒），可选 `3` / `5` / `10` / `18`，默认 `5` |
| `fps` | 否 | 帧率，默认 `24` |
| `negative_prompt` | 否 | 反向提示词 |
| `seed` | 否 | 随机种子，用于可复现结果 |
| `output` | 否 | 输出文件路径，默认下载到当前目录 |

## 分辨率档位

| 档位 | 尺寸 | 推荐场景 |
|------|------|----------|
| 480p | `854x480` | 移动端预览、快速测试 |
| 720p | `1152x768` (16:9) / `768x1152` (9:16) | 标准视频、社交内容 |
| 1080p | `1920x1080` (16:9) / `1080x1920` (9:16) | 高品质输出 |

## 时长与帧数

| 目标时长 | 推荐 `num_frames` |
|----------|-------------------|
| 约 3 秒 | 81 |
| 约 5 秒 | 121 |
| 约 10 秒 | 241 |
| 约 18 秒 | 441 |

> `num_frames` 必须 ≤ 441 且遵循 `8n + 1` 规则。

## 提示词模板

### 文生视频
```
[主体] + [动作] + [场景] + [镜头运动] + [光线] + [风格]
```

**示例**：
> A young astronaut walking across a red desert planet, dust blowing in the wind, slow cinematic tracking shot, dramatic sunset lighting, realistic sci-fi style

### 图生视频
```
[运动描述] + [保持不变的元素] + [镜头运动] + [风格]
```

**示例**：
> Animate the character with subtle breathing motion, hair moving gently in the wind, background lights flickering softly, while keeping the face and outfit consistent

### 多图视频
```
[起始画面] + [目标画面] + [过渡描述] + [风格]
```

**示例**：
> Use the first image as the starting scene and the second image as the target scene. Create a smooth transformation with consistent lighting, natural motion, and cinematic pacing

### 关键帧动画
```
[过渡描述] + [保持一致的元素] + [镜头运动]
```

**示例**：
> Create a smooth transition from the first keyframe to the second keyframe, maintaining character identity, consistent camera angle, and natural motion between scenes

## 工作流程

1. **创建任务**：发送请求到 API，获取 `video_id` 和 `task_id`
2. **轮询状态**：每 5 秒查询一次任务状态
3. **获取结果**：任务完成后下载视频文件
4. **超时处理**：最多等待 300 秒（5 分钟）

## 注意事项

- 视频生成是**异步**的，脚本会自动轮询获取结果（最多等待 5 分钟）
- 图生视频只需传单张 `image` URL
- 多图视频和关键帧动画需传多张 `images` URL
- 关键帧动画需在请求中设置 `extra_body.mode: "keyframes"`
- 推荐超时时间：300s
- 输入图片 URL 必须是公开可访问的 HTTPS

## 参考文档

- [API 文档](references/API.md)
- [提示词指南](references/PROMPT_GUIDE.md)

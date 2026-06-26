---
name: create-edu-video
description: 全自动教学视频制作技能。根据课程主题自动生成教学视频，包含文案编写、TTS配音、画面设计、Remotion代码开发、视频导出。触发场景：用户要求制作教学视频、课程视频、讲解视频、教育内容时使用。支持竖屏(1080x1920)和横屏(1920x1080)格式。
---

# Create Edu Video

根据课程主题和需求，全自动制作教学视频。

## 环境要求

> ⚠️ **安全提示**：以下工具需由用户自行安装，本技能不会自动执行系统级安装命令。

### 必需工具

| 工具 | 用途 | 检查命令 |
|------|------|----------|
| pnpm | Node.js 包管理器 | `pnpm --version` |
| Chromium | Remotion 渲染引擎 | `which chromium-browser \|\| which chromium` |
| FFmpeg | 音视频处理 | `ffprobe -version` |
| edge-tts | 微软 TTS 配音 | `edge-tts --list-voices \| grep zh-CN` |

### 必选配套技能

remotion-video-toolkit 是 Remotion 开发的必备参考手册，执行前请确认已安装：
```bash
# 检查技能是否存在
clawhub list | grep remotion-video-toolkit

# 如未安装，请用户授权后执行
clawhub install remotion-video-toolkit
```

### 项目依赖

创建新项目时，需在项目目录内安装 Node.js 依赖：
```bash
pnpm add @remotion/cli @remotion/player remotion react react-dom
pnpm add -D @types/react typescript
```

### 环境检查流程

在开始制作视频前，**必须先检查环境**，如有缺失应提示用户自行安装：

1. 检查 pnpm：`pnpm --version`
2. 检查 Chromium：`which chromium-browser || which chromium`
3. 检查 FFmpeg：`ffprobe -version`
4. 检查 edge-tts：`edge-tts --list-voices | grep zh-CN`
5. 检查 remotion-video-toolkit 技能：`clawhub list | grep remotion-video-toolkit`

如任何一项缺失，**停止执行并提示用户安装**，不要尝试自动安装。

## 工作流程

### Step 1: 素材准备

1. 阅读 `remotion-video-toolkit` 技能作为视频制作指导
2. 使用网络搜索（通过 tavily-search 子代理）查询：
   - 课程设计最佳实践
   - 相关图片和矢量图形资源
3. 汇总素材，准备文档和资源文件

### Step 2: 文案编写

1. 根据课程主题确定教学风格（默认：可汗学院风格）
2. 编写教学讲解文案
3. 生成 SRT 字幕文件格式：
   ```
   1
   00:00:00,000 --> 00:00:03,000
   第一句讲解内容

   2
   00:00:03,000 --> 00:00:06,500
   第二句讲解内容
   ```
4. **关键**：单行字幕限制字数，确保不超出视频宽度

### Step 3: TTS 配音生成

1. 使用 edge-tts 生成配音：
   ```bash
   edge-tts --text "讲解内容" --write-media output.mp3 --voice zh-CN-XiaoxiaoNeural
   ```
2. 运行 `scripts/sync_srt_tts.py` 同步 SRT 时间轴与配音时长
3. 验证字幕与配音对齐

### Step 4: 视频脚本设计

分析 SRT 字幕，设计视频画面脚本（script.md）：

```markdown
## 场景 1 (00:00 - 00:05)
- 元素: 标题动画、背景渐变
- 镜头: 淡入
- 动效: 文字逐字出现
- 转场: 溶解

## 场景 2 (00:05 - 00:12)
- 元素: 图解动画、重点标注
- 镜头: 推进
- 动效: 图形绘制效果
- 转场: 滑动
```

### Step 5: Remotion 项目开发

1. 初始化项目：
   ```bash
   pnpm create video --hello-world
   ```

2. 深度参考 `remotion-video-toolkit` 技能

3. 依据 SRT 和 script 开发 Remotion 代码：
   - 设置视频尺寸（默认 1080x1920 竖屏）
   - 设计排版布局
   - 实现字幕组件
   - 集成配音音轨
   - 添加动效和转场

4. 本地预览：
   ```bash
   pnpm start
   ```

### Step 6: 审查与修正

1. 审查代码是否还原 script 设计
2. 发现问题立即修复
3. 导出预览版：
   ```bash
   pnpm render --codec h264 --output preview.mp4
   ```

### Step 7: 用户反馈循环

1. 发送预览视频给用户
2. 根据反馈修改：
   - 简单修改：直接调整代码
   - 复杂修改：从 Step 2 重新执行
3. 重复直到用户确认

### Step 8: 最终导出

用户确认后，导出最终成品：
```bash
pnpm render --codec h264 --quality high --output final.mp4
```

## 视频规格

| 参数 | 默认值 | 可选 |
|------|--------|------|
| 尺寸 | 1080x1920 (竖屏) | 1920x1080 (横屏) |
| 帧率 | 30fps | 60fps |
| 编码 | H.264 | H.265, WebM |
| 配音 | zh-CN-XiaoxiaoNeural (女声) | 其他 edge-tts 语音 |

## 教学风格参考

详见 `references/teaching-styles.md`，包含：
- 可汗学院风格
- TED 演讲风格
- 白板教学风格
- 动画解说风格

## 脚本工具

### scripts/sync_srt_tts.py

同步 SRT 字幕时间轴与 TTS 配音时长。

用法：
```bash
python scripts/sync_srt_tts.py --srt subtitles.srt --audio voice.mp3 --output synced.srt
```

功能：
- 分析音频实际时长
- 调整 SRT 时间戳对齐
- 处理段落间停顿

# 风格预设 & 详细参数

## 成片风格预设 (auto-video-maker.sh --style)

| 风格 | 节奏 | 字号 | 转场 | 适合 |
|------|------|------|------|------|
| `default` | 中等 | 42 | 0.5s fade | 通用 |
| `vlog` | 轻快 | 38 | 0.3s fade | 日常 Vlog |
| `cinematic` | 缓慢 | 48 | 1.0s fade | 电影感/故事 |
| `fast` | 快速 | 36 | 0.2s fade | 短视频/抖音 |

## 调色风格预设 (auto-color-grade.sh --style)

| 风格 | 效果 | 适合场景 |
|------|------|----------|
| `natural` | 轻微增强对比度和饱和度 | 通用、纪录片 |
| `cinematic` | 高对比度、冷色调、暗角 | 电影感、剧情 |
| `vintage` | 暖色调、低饱和度、复古 | 怀旧、老照片 |
| `fresh` | 高饱和度、明亮 | 美食、旅行、Vlog |
| `warm` | 增强橙黄色调 | 日落、室内、温馨 |
| `cool` | 增强蓝绿色调 | 科技、商务 |

**调色强度建议：** 日常 0.5-0.7 | 专业 0.7-0.9 | 实验 1.0

## AI 文案风格 (ai-script-generator.sh --style)

支持：`vlog`、`科普`、`教程`、`带货`、`故事`

平台优化：`general`、`tiktok`、`youtube`、`bilibili`

## 完整参数速查

### auto-video-maker.sh

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--project` | 素材目录 | 必需 |
| `--script` / `--script-file` | 文案文本/文件 | 必需 |
| `--voiceover` | 配音目录 | 可选 |
| `--music` | BGM 文件 | 自动检测 music/ |
| `--style` | 风格预设 | default |
| `--resolution` | 分辨率 | 1920x1080 |
| `--subtitle-pos` | 字幕位置 bottom/center/top | bottom |
| `--font-size` | 字幕字号 | 42 |
| `--no-subtitle` | 不加字幕 | false |
| `--no-auto-cleanup` | 不清理中间文件 | false |
| `--transition` | 转场 fade/none | fade |
| `--output` | 输出文件 | output.mp4 |

### media-collector.sh

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--keywords` | 搜索关键词 | 必需 |
| `--count` | 下载数量 | 5 |
| `--orientation` | landscape/portrait/square | landscape |
| `--quality` | sd/hd/4k | hd |
| `--min-duration` | 最短秒数 | 3 |
| `--max-duration` | 最长秒数 | 30 |
| `--source` | pexels/pixabay/both | both |
| `--output` | 输出目录 | ./project-media |

### tts-voiceover.sh

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--script` / `--script-file` | 文案文本/文件 | 必需 |
| `--instruct` | 声音特征描述 | 活泼开朗的年轻男声 |
| `--speaker` | 发言人 | default |
| `--no-trim` | 不修剪静音 | false |
| `--merge` | 合并模式（音色一致） | false |
| `--cleanup` | 清理中间文件 | false |
| `--output` | 输出目录 | ./voiceover |

### auto-color-grade.sh

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 第1参数 | 输入视频 | 必需 |
| 第2参数 | 输出视频 | 必需 |
| `--style` | 调色风格 | natural |
| `--intensity` | 效果强度 0.0-1.0 | 0.7 |
| `--preview` | 仅预览前10秒 | false |

### auto-broll-insert.sh

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 第1参数 | 主视频 | 必需 |
| 第2参数 | B-roll 目录 | 必需 |
| 第3参数 | 输出视频 | 必需 |
| `--script` | 文案文件（智能匹配） | 可选 |
| `--min-duration` | B-roll 最短秒数 | 2 |
| `--max-duration` | B-roll 最长秒数 | 5 |
| `--transition` | fade/dissolve/none | fade |
| `--position` | auto/start/middle/end/random | auto |
| `--audio` | mute/mix/replace | mute |

### ai-script-generator.sh

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--topic` | 视频主题 | 必需 |
| `--style` | 文案风格 | vlog |
| `--duration` | 目标时长(秒) | 60 |
| `--keywords` | 自动生成素材关键词 | false |
| `--output` | 输出文件 | stdout |

### auto-publish.sh

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--video` | 视频文件 | 必需 |
| `--platform` | bilibili/youtube/tiktok/xiaohongshu | 必需 |
| `--title` | 视频标题 | 必需 |
| `--tags` | 标签（逗号分隔） | 可选 |
| `--description` | 视频描述 | 可选 |
| `--config` | 初始化配置 | — |

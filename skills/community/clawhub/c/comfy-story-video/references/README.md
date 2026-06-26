# ComfyUI 儿童故事视频生成器

根据主题自动生成儿童故事 → ComfyUI 生成插图 → 语音旁白 → 视频

## 工作流程

```
主题输入 → 生成故事（分段）→ ComfyUI 生成图片 → TTS 语音 → 合成视频
```

## 安装依赖

```bash
pip install websocket-client requests
```

## 使用方法

### 1. 确保 ComfyUI 运行

```bash
cd /Users/yiyi/Projects/stable-diffusion/ComfyUI
python main.py
```

### 2. 生成故事视频

```bash
cd /Users/yiyi/.openclaw/workspace/comfy-story-video

# 使用默认主题（友谊）
python scripts/generate_story_video.py

# 指定主题
python scripts/generate_story_video.py --theme "勇气"

# 指定场景数量
python scripts/generate_story_video.py --theme "环保" --scenes 6
```

## 输出文件

在 `output/` 目录下：
- `story_{theme}_{timestamp}.json` - 故事文本
- `scene_01.png` ~ `scene_N.png` - ComfyUI 生成的插图
- `scene_01.mp3` ~ `scene_N.mp3` - 语音旁白
- `story_{theme}_{timestamp}.mp4` - 最终视频（开发中）

## 自定义配置

### 修改 ComfyUI 模型

编辑 `assets/basic_workflow.json`，替换 `CheckpointLoaderSimple` 中的模型名称。

### 添加更多角色/场景

编辑 `scripts/generate_story_video.py` 中的：
- `characters` - 角色列表
- `settings` - 场景背景
- `themes` - 故事主题

### 更换 TTS 声音

目前使用 macOS 内置 `say` 命令。要更换声音：
- 查看可用声音：`say -v '?' | grep zh`
- 修改代码中的 `-v "Ting-Ting"` 为其他中文声音

## 进阶：使用更好的 TTS

如果需要更好的语音质量，可以集成：
- **Azure TTS** - 高质量中文语音
- **ElevenLabs** - 情感丰富的英文语音
- **GPT-SoVITS** - 本地中文 TTS

## TODO

- [ ] 完整的视频合成（图片+音频+字幕）
- [ ] 字幕自动生成和渲染
- [ ] 背景音乐添加
- [ ] 批量生成多个故事
- [ ] 发布到小红书/抖音的格式适配

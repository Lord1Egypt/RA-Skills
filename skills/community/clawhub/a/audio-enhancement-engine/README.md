### audio-enhancement-engine

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://github.com/wangminrui2022)

**audio-enhancement-engine** 本地音频增强与修复统一工具，集成 VoiceFixer（语音降噪/修复）和 AudioSR（高保真超级分辨率）。支持单文件与目录批量处理，自动适配最合适的增强模式，输出清晰、高质量的 48kHz WAV 文件。

---

```markdown
# OpenClaw Audio Skill

**一个简单高效的音频增强与修复命令行工具**

支持两种主流音频增强技术：
- **AudioSR**：高保真音频超级分辨率（将音频提升至 48kHz，增加细节与高频）
- **VoiceFixer**：通用语音修复（降噪、提升清晰度、修复失真）

---

## ✨ 功能特点

- 支持**单个文件**和**整个目录**批量处理
- 同时集成两种专业音频增强模型
- 通过 `--hifi` 一键切换高保真模式与语音修复模式
- 支持 GPU 加速（CUDA）
- 自动创建输出目录，智能添加 `_enhanced` 后缀
- 详细的中文日志提示，处理状态清晰
- 兼容性强（包含 NumPy 兼容补丁）
- 支持递归处理子目录

---

## 📥 安装与使用

### 1. 克隆项目

```bash
git clone https://github.com/wangminrui2022/audio-enhancement-engine.git
```

> 首次运行 VoiceFixer 时会自动下载模型，AudioSR 同样会根据需要下载对应模型。

### 2. 基本使用

#### 方式一：默认使用 VoiceFixer（语音修复）

```bash
# 修复单个音频文件
python main.py -i input/audio.mp3

# 修复整个目录
python main.py -i recordings/

# 使用 GPU + 递归处理子目录
python main.py -i recordings/ --cuda -r
```

#### 方式二：使用 AudioSR 高保真增强（48kHz 超分辨率）

```bash
# 高保真增强单个文件
python main.py -i low_quality.wav --hifi

# 高保真增强目录，并指定输出目录
python main.py -i music_folder/ -o enhanced_music/ --hifi

# 使用更高参数提升质量
python main.py -i input.wav --hifi --ddim_steps 100 --guidance_scale 4.0
```

---
### **在 OpenClaw 聊天中**

你可以直接对你的 Agent 说：

帮我增强这个音频 recording.mp3”

复这个会议录音，音质太差了”

给这个音乐提升高保真音质 music.wav”

把这个音频提升到48kHz”

批量处理这个音频文件夹 audio_files/”

高保真增强这个播客音频”

帮我降噪这个语音笔记 voice.m4a”

老旧录音修复 folder_path/”

音乐音质增强 这个.mp3 --hifi”

清理这个失真录音并提升清晰度”

## 📋 命令行参数说明

### 通用参数

| 参数 | 缩写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--input` | `-i` | str | **必填** | 输入文件或目录路径 |
| `--output` | `-o` | str | None | 输出路径（文件或目录） |

### VoiceFixer 参数（默认模式）

| 参数 | 缩写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--mode` | `-m` | int | 1 | 增强模式 (0/1/2)，推荐使用 1 |
| `--cuda` | | bool | False | 是否使用 GPU 加速 |
| `--recursive` | `-r` | bool | False | 是否递归处理子目录 |

### AudioSR 高保真参数（需添加 `--hifi`）

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--hifi` | bool | False | 启用 AudioSR 高保真模式 |
| `--model_name` | str | basic | 模型名称，可选 `basic` / `speech` |
| `--ddim_steps` | int | 50 | 扩散步数（越大质量越好，速度越慢） |
| `--guidance_scale` | float | 3.5 | 引导尺度 |
| `--seed` | int | 42 | 随机种子 |
| `--device` | str | None | 指定设备 `cuda` 或 `cpu` |

---

## 📂 项目结构

```
audio-enhancement-engine/
├── enhancer.py                # 主程序入口（命令行解析 + 调度）
├── hifi_audio_enhance.py      # AudioSR 高保真增强模块
├── voice_enhance.py           # VoiceFixer 语音修复模块
└── ...
```

---

## 🎯 使用场景推荐

| 场景 | 推荐模式 | 建议参数 |
|------|----------|----------|
| 会议录音、电话录音、播客降噪 | VoiceFixer | `mode=1` + `--cuda` |
| 老旧磁带、历史录音修复 | VoiceFixer | `mode=1` |
| 音乐、演唱、人声提升高频细节 | AudioSR | `--hifi --model_name speech` |
| 需要极致音质（音乐制作） | AudioSR | `--hifi --ddim_steps 100 --guidance_scale 4.0` |
| 批量处理大量文件 | 任一模式 | 配合 `-o` 指定输出目录 |

---

## ⚠️ 注意事项

1. **首次运行** VoiceFixer 或 AudioSR 时会自动下载模型，请保持网络畅通。
2. AudioSR 处理速度较慢（尤其是 `ddim_steps` 较大时），建议使用 GPU。
3. VoiceFixer 默认输出为 `.wav` 格式，AudioSR 默认输出为 48kHz `.wav`。
4. 建议为不同任务分别创建输出目录，避免混淆。

---

## 🛠️ 未来计划（可选）

- 支持更多音频增强模型
- 添加图形界面（Gradio / Streamlit）
- 支持批量配置文件
- 集成到 OpenClaw 主框架
- 支持实时音频流处理

---

## 📄 License

Apache License

---

## ❤️ 致谢

- [AudioSR](https://github.com/haoheliu/versatile_audio_super_resolution.git) - 音频超级分辨率
- [VoiceFixer](https://github.com/haoheliu/voicefixer.git) - 语音修复工具

---

**欢迎 Star ⭐ 支持项目！**

如有问题或建议，欢迎提交 Issue 或 Pull Request。

```

---
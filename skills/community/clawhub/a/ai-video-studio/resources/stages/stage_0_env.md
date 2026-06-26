# Stage 0: 自动化环境部署 (Scaffolding)

当用户在一个空文件夹中首次要求“初始化项目”或“初始化 FableForge”时，**必须且仅需执行一次**本阶段。如果你发现当前目录已经有了 `template/` 和 `bin/`，则说明已初始化过，请直接跳过。

**0.1 复制模板与模型资源**
FableForge 的项目模板与语音模型代码已打包在 Skill 目录中。请执行以下命令：

```bash
# 复制 HTML 模板与脚本模板
cp -r .agents/skills/fableforge/resources/template ./template

# 复制语音模型脚手架
cp -r .agents/skills/fableforge/resources/voice-model ./voice-model
```

**0.2 自动下载 FFmpeg 环境**
本流水线强烈依赖 `ffmpeg` 与 `ffprobe`。请自动为用户下载静态构建版：

```bash
curl -L https://evermeet.cx/ffmpeg/get/zip -o ffmpeg.zip && unzip -o ffmpeg.zip
curl -L https://evermeet.cx/ffmpeg/get/ffprobe/zip -o ffprobe.zip && unzip -o ffprobe.zip
mkdir -p bin && mv ffmpeg bin/ && mv ffprobe bin/ && chmod +x bin/*
rm ffmpeg.zip ffprobe.zip
```

**0.3 自动配置 VoxCPM2 Python 环境**
执行以下命令为用户的语音克隆模型创建隔离环境并安装依赖：

```bash
python3 -m venv voice-model/venv
source voice-model/venv/bin/activate
pip install voxcpm soundfile torch numpy
```

**0.4 引导用户录制声纹样本**
执行完毕后，请暂停并提示用户：
> "FableForge 环境已初始化完毕！请您用手机或电脑录制一段 15 秒的声音（朗读任意文本），将其导出为 `.wav` 格式，并放置在 `voice-model/01_samples/my_voice.wav`。准备好后请告诉我，我们就可以开始做视频了！"

**✅ Stage 0 退出标准：**
- [ ] 当前工作区包含 `template/`、`voice-model/` 和 `bin/` 目录。
- [ ] 用户确认已准备好声纹样本。

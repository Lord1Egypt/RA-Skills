# 豆包 TTS - 火山引擎语音合成 OpenClaw Skill

将文本或 Markdown 文件合成为高质量语音音频，基于火山引擎（Volcengine）异步长文本合成接口。

## 功能特性

- 🎙️ 支持异步长文本合成（单次最高 10 万字符）
- 🎭 支持自动情感预测（emotion_predict）
- 📝 支持 SSML 标记语言
- 📋 支持字幕/时间戳同步输出
- 📄 支持直接输入文本或 Markdown/TXT 文件
- 🔄 自动轮询任务状态，合成完成后下载音频

## 快速开始

### 1. 前置条件

- 在[火山引擎控制台](https://console.volcengine.com/)开通**语音合成**服务
- 创建应用，获取 `APP_ID` 和 `Access Token`

### 2. 安装

```bash
bash install.sh
```

或非交互模式：

```bash
bash install.sh --app-id <your_app_id> --access-token <your_access_token>
```

### 3. 使用

```bash
# 合成文本
python3 scripts/tts.py "你好，这是一段测试文本"

# 合成 Markdown 文件
python3 scripts/tts.py story.md

# 指定音色和输出文件
python3 scripts/tts.py story.md --voice-type zh_fa_story --output story.mp3

# 启用情感预测
python3 scripts/tts.py story.md --emotion

# 启用字幕
python3 scripts/tts.py story.md --subtitle
```

## 推荐音色

| 音色 ID | 说明 | 适用场景 |
|---------|------|---------|
| `zh_female_chancan_v2_h5` | 灿灿-精品有声书 | 有声书、故事朗读（默认） |
| `zh_fa_story` | 故事版 | 哄睡故事、儿童故事 |

## 配置

环境变量加载优先级（先找到的优先）：

1. **全局配置**: `~/.config/doubao-tts/.env`
2. **项目目录**: 当前工作目录下的 `.env` 文件
3. **系统环境变量**: 已设置的 `VOLCENGINE_APP_ID` / `VOLCENGINE_ACCESS_TOKEN`

`.env` 文件格式：
```
VOLCENGINE_APP_ID=your_app_id
VOLCENGINE_ACCESS_TOKEN=your_access_token
```

## 许可证

MIT

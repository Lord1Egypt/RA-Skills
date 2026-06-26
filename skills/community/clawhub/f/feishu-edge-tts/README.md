# 🎤 Feishu Edge TTS - 飞书语音条（免费）

使用微软 Edge TTS 生成语音，发送到飞书！**完全免费**！

## ✨ 功能特点

- ✅ **完全免费**：微软 Edge TTS，无需 API key
- ✅ **音质优秀**：Azure 同款语音引擎
- ✅ **多音色**：400+ 音色，100+ 语言
- ✅ **语音条**：发送真正的飞书语音条

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install edge-tts
```

### 2. 配置环境变量

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_CHAT_ID="oc_xxx"
```

### 3. 发送语音

```bash
# 使用默认音色（温暖女声）
bash scripts/send_voice.sh -t "主人晚上好～"

# 使用男声
bash scripts/send_voice.sh -t "你好" -v zh-CN-YunxiNeural

# 英文语音
bash scripts/send_voice.sh -t "Hello!" -v en-US-JennyNeural
```

## 🎵 常用音色

| 音色 | 语言 | 性别 | 特点 |
|------|------|------|------|
| zh-CN-XiaoxiaoNeural | 中文 | 女 | 温暖亲切（推荐）|
| zh-CN-YunxiNeural | 中文 | 男 | 沉稳专业 |
| zh-CN-XiaoyiNeural | 中文 | 女 | 活泼可爱 |
| en-US-JennyNeural | 英文 | 女 | 美式英语 |

## 📖 详细文档

查看 [SKILL.md](SKILL.md) 获取完整使用说明。

---

**Made with ❤️ by 司幼 (SiYou)**

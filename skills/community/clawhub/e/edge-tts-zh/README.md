# edge-tts-zh 🎤

> OpenClaw Skill: 中文语音合成，免费，无需API Key

使用 Microsoft Edge TTS 引擎，高质量中文语音合成。内置21种中文声音（男声/女声/方言）。

## ✨ 特点

- 🆓 **完全免费** — 无需API Key，无使用限制
- 🇨🇳 **中文优化** — 21种中文声音，普通话+粤语+台湾
- ⚡ **快速** — 几秒内生成语音
- 🎛️ **可调节** — 语速、音调自由调整
- 📦 **轻量** — 仅需 `pip install edge-tts`

## 🚀 使用

```bash
python3 scripts/speak.py "你好世界"
python3 scripts/speak.py "新闻简报" --voice xiaoxiao
python3 scripts/speak.py "快速朗读" --rate +30%
python3 scripts/speak.py --list  # 查看所有声音
```

## 📄 License

MIT

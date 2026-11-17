---
name: free-tts
description: 免费 TTS + 声音克隆双引擎。Fish Audio s2.1-pro-free（83 语言、克隆自己声音、voice_id 持久复用、免费至 2026-08-31）+ 小米 MiMo V2.5 TTS（8 种预置音色、文本设计音色、音频克隆、情绪/方言/唱歌标签控制、限时免费）。Use when 用户提到语音合成、TTS、文字转语音、配音、声音克隆、克隆我的声音、音色设计、免费语音生成、Fish Audio、小米 MiMo。
metadata:
  platform: Windows
  python: ">=3.10"
  external-deps: 无（纯 Python stdlib urllib/json/base64/wave）
  env-required: FISH_API_KEY 和/或 MIMO_API_KEY（User 级环境变量）
---

# Free TTS · 声音克隆双引擎 🐟🎙️

| 引擎 | 免费政策 | 强项 | 声音克隆 |
|------|---------|------|----------|
| **Fish Audio** `s2.1-pro-free` | 免费至 2026-08-31（公平使用、无硬性上限） | 83 语言、~90ms 低延迟、voice_id 持久复用 | ✅ 持久模型 + 即时克隆 |
| **小米 MiMo** `mimo-v2.5-tts` | 限时免费 | 中文预置音色、文本设计音色、情绪/方言/唱歌标签 | ✅ 音频样本克隆（不存模型） |

## 🚀 Step 0：初始化（首次使用必须走）

```bash
python <skill>/scripts/setup.py check        # 检查两个引擎的 key 状态
python <skill>/scripts/setup.py set-fish     # 交互式隐藏输入写入 FISH_API_KEY
python <skill>/scripts/setup.py set-mimo     # 交互式隐藏输入写入 MIMO_API_KEY
python <skill>/scripts/setup.py test-fish    # 验证连通性（需 Clash 代理在线）
python <skill>/scripts/setup.py test-mimo    # 验证连通性（国内直连）
```

**key 缺失时把下面的指引原样给用户**：

🐟 **Fish Audio**（克隆自己声音首选）：
1. 打开 https://fish.audio/ 注册/登录（GitHub 或 Google 登录，免费，无需信用卡）
2. 打开 https://fish.audio/app/api-keys/ → Create API Key → 复制（32 字符）

📱 **小米 MiMo**（中文音色/情绪控制首选）：
1. 用小米账号登录 https://platform.xiaomimimo.com/（没有就去 id.mi.com 注册）
2. 控制台 → API Keys（platform.xiaomimimo.com/#/console/api-keys）→ 创建（格式 sk-xxxxx）

用户拿到 key 后：**写入 Windows 用户级环境变量**（不硬编码、不回显明文、优先用 set-fish/set-mimo 隐藏输入；若用户直接贴 key，用 `[Environment]::SetEnvironmentVariable("FISH_API_KEY","<key>","User")` 写入并提醒下次别贴明文）。

## 🧭 引擎选择路由

| 需求 | 命令 |
|------|------|
| 克隆自己声音（持久、反复用） | `fish_clone.py` → `fish_tts.py --cached-name` |
| 一次性参考音频模仿 | `fish_tts.py --reference-audio` |
| 多语言（英/日/韩等 83 种） | `fish_tts.py` |
| 中文预置音色快速出片 | `mimo_tts.py --voice 苏打` |
| 文字设计新音色（无需音频） | `mimo_tts.py --design "..."` |
| 临时克隆（每次传音频、不存模型） | `mimo_tts.py --clone-audio` |
| 情绪/方言/唱歌/哭笑控制 | `mimo_tts.py --style "(东北话)..."` |

## 🎙️ 工作流 A：克隆自己的声音（Fish）

1. 录音要求：单人、无背景音乐、≥10 秒（推荐 1-2 分钟）、wav/mp3/m4a/opus
2. `python scripts/fish_clone.py --audio "E:/桌面/我的声音.m4a" --title "锋哥的声音" --cache-name "锋哥的声音"`
3. `python scripts/fish_tts.py --text "嘿兄弟们" --cached-name "锋哥的声音" --output out.mp3`

## 🎙️ 工作流 B：文字转语音（零克隆）

```bash
python scripts/mimo_tts.py --text "你好" --voice 冰糖 --output hello.wav      # 中文预置
python scripts/fish_tts.py --text "Hello world" --output hello.mp3            # 无声参考、多语言
```

## 🎙️ 工作流 C：声音克隆（MiMo，不存模型）

```bash
python scripts/mimo_tts.py --text "..." --clone-audio "声音.mp3" --output out.wav
# 音频仅支持 mp3/wav、≤7MB；可加 --style "温柔一点，语速放慢"
```

## 🧰 声音管理

```bash
python scripts/fish_voices.py list                                  # 列出 Fish 已克隆声音 + 本地缓存
python scripts/fish_voices.py delete --cached-name "锋哥的声音" --yes
```

## ⚠️ 警告

1. **Fish 免费层 2026-08-31 截止**（已延期两次，变动官方会提前通知）；到期后 `--model s2.1-pro` 切付费层
2. MiMo 为"限时免费"，商用/大量使用前查控制台账单明细页确认政策
3. **网络**：MiMo 是国内 API 直连即可；Fish 是海外 API，直连超时 → 先确认 Clash 在线，再 `set HTTPS_PROXY=http://127.0.0.1:7897`（Clash 默认端口，以实际为准）
4. 免费层请求数据可能被用于模型改进；敏感语音用付费层
5. key 只进环境变量；脚本输出永远脱敏（`abcd***1234`）

详细参数：`references/fish-api.md`、`references/mimo-api.md`

---
name: feishu-mood-music
description: >
  飞书音乐心情伴侣。识别用户的情绪状态，生成匹配的治愈/陪伴音乐并发送到飞书群。
  三级触发机制：
  (1) 显式触发（直接要歌）："来首歌"、"想听歌"、"来首应景的"、"音乐治愈"、"解压音乐"、"放首歌"
  (2) 半隐式触发（情绪词 + @机器人）："心情不好"、"有点累"、"好烦"、"需要放松"、"emo了"、"压力好大"、"开心"、"兴奋"
  (3) 全隐式触发（极端情绪词，无需@，自动送歌）："烦死了"、"无语死了"、"崩溃了"、"活不下去"、"气炸了"、"爽死了"、"太开心了"、"牛逼炸了"
  当用户表达情绪状态并需要音乐陪伴时激活。
---

# 飞书音乐心情伴侣 — Mood Music Companion

感知用户情绪，生成治愈音乐，通过飞书消息即时送达。不是冷冰冰的点歌台，是一个懂你情绪的音乐搭档。

**依赖**：MiniMax CLI（`mmx-cli`）+ Token Plan

---

## 快速配置（首次使用）

### 1. 安装 MiniMax CLI

```bash
npm install -g mmx-cli
```

> 需要 Node.js 18+。完整文档：https://github.com/MiniMax-AI/cli

### 2. 订阅 Token Plan

前往 MiniMax 平台订阅 Token Plan（音乐生成需要额度）：
- 🇨🇳 国内：https://platform.minimaxi.com/subscribe/token-plan
- 🌍 海外：https://platform.minimax.io/subscribe/token-plan

### 3. 登录认证

```bash
# 方式一：API Key 登录（推荐，从平台「接口密钥」页获取）
mmx auth login --api-key sk-xxxxx

# 方式二：浏览器 OAuth 登录
mmx auth login
```

### 4. 验证

```bash
mmx auth status    # 检查登录
mmx quota          # 检查额度
mmx music generate --prompt "gentle piano, healing" --out /tmp/test_mood.mp3  # 测试生成
```

全部通过即可使用本 Skill。

---

## 情绪-音乐映射表

### 负面情绪（治愈方向）

| 情绪信号 | 识别关键词 | 音乐策略 | 风格 | 情绪曲线 |
|---------|-----------|---------|------|---------|
| 😞 低落/难过 | 难过、伤心、emo、低落、郁闷 | 先共鸣后治愈 | Lo-fi R&B → Acoustic Warm | 从忧伤缓缓上升到温暖 |
| 😤 烦躁/愤怒 | 烦、气死了、崩溃、炸了 | 释放型 | Post-Rock, Alt Rock | 先给爆发出口，再收归平静 |
| 😰 焦虑/压力 | 焦虑、压力大、紧张、慌 | 镇静型 | Ambient, New Age | 持续安定，缓慢呼吸节奏 |
| 😴 疲惫/倦怠 | 好累、不想动、倦了、乏 | 温柔托底 | Bossa Nova, Soft Jazz | 不强求振作，给温柔的休息感 |
| 😢 孤独/思念 | 孤独、想念、一个人、寂寞 | 陪伴型 | Indie Folk, Singer-songwriter | 像朋友在身边轻声哼唱 |

### 正面情绪（助燃方向）

| 情绪信号 | 识别关键词 | 音乐策略 | 风格 |
|---------|-----------|---------|------|
| 😊 开心/满足 | 开心、不错、满足、幸福 | 锦上添花 | City Pop, Funk, Disco |
| 🔥 兴奋/庆祝 | 太棒了、赢了、发布、上线 | 推向高潮 | EDM, Dance Pop, Hyperpop |
| 🌟 期待/憧憬 | 期待、马上就、等不及 | 氛围渲染 | Synth Pop, Dream Pop |
| 💪 战斗/冲刺 | 冲、干就完了、拼了 | 热血增幅 | Rock, Trap, Epic Electronic |

---

## 工作流

### Step 1: 触发判断（三级触发机制）

本 Skill 采用三级触发，根据信号强度决定行为：

#### 🟢 Level 1：显式触发（直接要歌）

用户明确要求音乐，**无论是否 @机器人，立即生成**。

| 触发词 | 动作 |
|--------|------|
| 来首歌、想听歌、放首歌 | 直接生成，不问 |
| 来首应景的、音乐治愈、解压音乐 | 直接生成，不问 |
| 来首 [风格] 的歌 | 按指定风格生成 |

#### 🟡 Level 2：半隐式触发（情绪词 + @机器人）

用户表达了情绪**且 @了机器人**，视为求助信号，**直接生成**。
如果只有情绪词但没有 @，**不触发**（避免群聊噪音）。

| 触发词（需要 @） | 动作 |
|-----------------|------|
| 心情不好、有点累、好烦、好丧 | 匹配情绪 → 生成 |
| emo了、压力好大、需要放松、陪我 | 匹配情绪 → 生成 |
| 开心、兴奋、太棒了 | 匹配情绪 → 生成 |

#### 🔴 Level 3：全隐式触发（极端情绪，自动送歌）

用户情绪到了极端值，**无需 @，自动生成并送歌**。
这些词本身就是强烈信号，沉默反而像冷漠。

**负面极端**（先共鸣后治愈）：

| 触发词 | 情绪 | 动作 |
|--------|------|------|
| 烦死了、烦得要死 | 😤 暴怒 | 释放型音乐 + 「🎵 先听会儿」 |
| 无语死了、服了 | 😤 无奈 | 释放型音乐 |
| 崩溃了、要疯了、受不了了 | 😰 崩溃 | 镇静型音乐 + 「🎵 深呼吸」 |
| 累死了、不想干了 | 😴 极度疲惫 | 温柔托底音乐 + 「🎵 歇会儿吧」 |
| 想哭、难受死了 | 😢 极度悲伤 | 陪伴型带歌词 + 「🎵 这首给你」 |

**正面极端**（助燃放大）：

| 触发词 | 情绪 | 动作 |
|--------|------|------|
| 爽死了、太爽了 | 🔥 极度兴奋 | 高能舞曲 + 「🎵 燥起来！」 |
| 太开心了、幸福死了 | 😊 极度开心 | 欢快 Funk + 「🎵 快乐加倍！」 |
| 牛逼炸了、赢麻了 | 🔥 庆祝 | EDM/Hyperpop + 「🎵 这首给你庆祝！」 |
| 冲冲冲、干就完了 | 💪 战斗 | 热血摇滚 + 「🎵 冲！」 |

**全隐式安全规则**：
- 仅在群聊中对**已知用户**触发（非陌生人）
- 同一用户 **30 分钟内最多触发 1 次**（防刷屏）
- 私聊场景下，Level 2 和 Level 3 均可无需 @ 触发

### Step 2: 情绪识别

从用户消息中分析：
1. **情绪类别**：匹配上方映射表（可多维度叠加）
2. **情绪强度**：轻微 / 中等 / 强烈（影响音乐激烈程度和歌词策略）
3. **场景线索**：工作中 / 下班后 / 深夜（影响风格选择）

### Step 3: 构建 Prompt

根据情绪映射选择音乐策略，构建 prompt。

**负面情绪**使用"情绪曲线"策略——不直接跳到快乐，而是先共鸣再引导：

```
prompt 模板（负面情绪）:
<style>, <mood 起始: 共鸣词>, gradually shifting to <mood 目标: 治愈词>, 
<instruments>, <BPM> BPM, <vocal/instrumental>, 
a song that understands how you feel and gently lifts you up
```

**正面情绪**使用"助燃"策略——放大当前感受：

```
prompt 模板（正面情绪）:
<style>, <mood: 正面高能词>, <instruments>, <BPM> BPM, 
<vocal/instrumental>, energetic and feel-good
```

### Step 4: 歌词策略

| 情绪类型 | 歌词策略 |
|---------|---------|
| 负面轻微 | 纯音乐（`is_instrumental: true`），不加歌词避免矫情感 |
| 负面强烈 | 带歌词（`lyrics_optimizer: true`），让 AI 写共鸣歌词，有"被懂了"的感觉 |
| 正面情绪 | 带歌词，节奏明快有感染力 |
| 用户指定 | 按用户要求 |

### Step 5: 生成音乐

优先使用 CLI，回退到 Python 脚本：

```bash
# 方式一：MiniMax CLI（推荐）
# 纯音乐（负面轻微）
mmx music generate \
  --prompt "<constructed prompt>" \
  --instrumental \
  --out /tmp/openclaw/mood_<emotion>.mp3

# 带歌词（负面强烈/正面）— 自动生成歌词
mmx music generate \
  --prompt "<constructed prompt>" \
  --lyrics "[verse]\n[chorus]" \
  --out /tmp/openclaw/mood_<emotion>.mp3

# 方式二：Python 脚本（需要 MINIMAX_API_KEY 环境变量）
python3 scripts/generate_mood_music.py \
  --prompt "<constructed prompt>" \
  --instrumental \
  --output /tmp/openclaw/mood_<emotion>.mp3
```

### Step 6: 播放与送达

生成完成后，**必须完成送达**，不能只输出文件路径。根据环境自动选择最佳方式。

#### 环境探测

```bash
# 检测本地音乐播放器（macOS）
osascript -e 'id of application "Music"' 2>/dev/null && echo "HAS_MUSIC_APP"
# 或检测命令行播放器
which mpv afplay ffplay 2>/dev/null
```

#### 送达策略

| 条件 | 行为 |
|------|------|
| 检测到本地播放器（Music.app / mpv / afplay） | **自动吊起播放** + 飞书发送备份 |
| 未检测到本地播放器 | **发送飞书音频消息** |

#### 路径 A：本地播放器可用

```bash
# macOS 用系统命令打开默认播放器
open /tmp/openclaw/mood_<emotion>.mp3

# 或 afplay 后台播放
afplay /tmp/openclaw/mood_<emotion>.mp3 &

# 或 mpv
mpv --no-video /tmp/openclaw/mood_<emotion>.mp3 &
```

同时发一份到飞书群（见路径 B）。

#### 路径 B：飞书音频消息送达

**⚠️ 关键步骤，不可跳过。** 飞书语音气泡需要特殊的上传+发送流程。

**方式 1：使用内置脚本（推荐，一行搞定）**

Skill 自带 `scripts/send_feishu_audio.sh`，支持 `--file` 模式直接发送已有音频：

```bash
# 发送已生成的音乐到飞书群（语音气泡，非文件附件）
bash scripts/send_feishu_audio.sh --file /tmp/openclaw/mood_<emotion>.mp3 "<chat_id>"
```

凭证自动从环境变量 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` 读取，
或回退到 `$HOME/.openclaw/openclaw.json`。

**方式 2：OpenClaw message 工具**（OpenClaw 环境）
```
message(action="send", filePath="/tmp/openclaw/mood_<emotion>.mp3",
        message="<共情文案>")
```

**方式 3：手动 curl 两步流程**（理解原理用）

```bash
# ⚠️ 关键坑：file_type 必须填 opus（不是 mp3），否则报 234001
# ⚠️ 关键坑：msg_type 必须是 audio（不是 file），否则显示为附件

# Step 1: 上传文件（file_type=opus）
FILE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" \
  -F "file_name=voice.opus" \
  -F "file=@/tmp/openclaw/mood_<emotion>.mp3" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['file_key'])")

# Step 2: 发送音频消息（msg_type=audio）
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$CHAT_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

#### ❌ 错误行为（严禁）

- 只输出文件路径如 `📎 /workspace/.../output/xxx.mp3` → **用户无法访问服务器路径**
- 只发文字说"已生成" → **用户听不到音乐**
- 把 base64 音频贴在聊天里 → **不可读**

**原则：用户必须能在 2 次点击内听到音乐。**

播放器优先级：`open`（macOS 默认）> `mpv` > `afplay` > 飞书音频消息 > 飞书文件消息

**共情文案模板**（简短、不说教）：

| 情绪 | 文案示例 |
|------|---------|
| 低落 | 🎵 这首给你，不用急着开心 |
| 烦躁 | 🎵 先听会儿，让脑子放空一下 |
| 焦虑 | 🎵 深呼吸，跟着节奏慢下来 |
| 疲惫 | 🎵 歇会儿吧，没什么比你重要 |
| 开心 | 🎵 快乐加倍！这首配你的好心情 |
| 兴奋 | 🎵 燥起来！这首给你庆祝 |

---

## 进阶：情绪追踪（可选）

如果用户频繁使用，可以在 `memory/mood-music-log.json` 中记录：

```json
{
  "history": [
    {"date": "2026-04-10", "emotion": "tired", "style": "bossa nova", "rating": "👍"},
    {"date": "2026-04-09", "emotion": "anxious", "style": "ambient", "rating": null}
  ]
}
```

用于：
- 避免连续推荐相同风格
- 发现用户偏好（"你之前喜欢 Bossa Nova 治愈系，这次也来一首？"）
- 如果连续多天负面情绪，温和提醒（不是心理医生，只是朋友式的关心）

---

## 边界与安全

- **不是心理咨询**：不诊断、不处方、不说"你应该怎样"
- **不过度解读**：用户说"有点累"就是累，别上升到心理问题
- **不强制正能量**：允许用户沉浸在情绪里，音乐是陪伴不是说教
- **隐私**：情绪记录仅存本地，不外传

---

## 生成方式

### 方式一：MiniMax CLI（推荐，零代码）

CLI 自动管理认证和 region，无需手动传 API Key：

```bash
# 纯音乐
mmx music generate --prompt "<prompt>" --instrumental --out /tmp/openclaw/mood.mp3

# 带自动歌词
mmx music generate --prompt "<prompt>" --lyrics "[verse]\n[chorus]" --out /tmp/openclaw/mood.mp3
```

### 方式二：Python 脚本（需要 API Key）

`scripts/generate_mood_music.py` 直接调用 MiniMax Music API：

- 读取 API Key：从环境变量 `MINIMAX_API_KEY` 获取
- 模型：`music-2.5+`
- 支持 `--instrumental` 切换纯音乐/带歌词
- 带歌词模式：`lyrics_optimizer: true`（API 自动写词）
- 输出：MP3，44100Hz，256kbps

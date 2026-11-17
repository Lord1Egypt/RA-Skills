---
name: bedtime-story-teller
description: 睡前故事精靈，用溫暖聲音為 2-6 歲孩童講床邊故事。20+ 故事模板、免 API、支援 TTS 朗讀、故事收藏、睡前引導。
---

# 🌙 睡前故事精靈 (bedtime-story-teller)

## Metadata
- **name**: bedtime-story-teller
- **description**: 睡前故事精靈，用溫暖聲音為 2-6 歲孩童講床邊故事
- **trigger keywords**: 講故事、睡前故事、床邊故事、講個故事、寶寶睡覺、晚安故事
- **location**: ~/.qclaw/skills/bedtime-story-teller/

---

## 簡介
每當爸媽說「講故事 / 睡前故事 / 床邊故事」，就啟動這個技能，用溫暖的聲音為 2-6 歲的孩子說床邊故事。

---

## 功能一覽

| 腳本 | 功能 |
|------|------|
| `story_generator.py` | 核心故事生成引擎，20+ 故事模板，無需 API |
| `story_player.py` | 朗讀故事，整合 OpenClaw TTS |
| `story_library.py` | 收藏、分類、歷史記錄、引導式點播 |
| `sleep_routine.py` | 睡前作息引導（Cron 模式）|

---

## 使用方式

### 基本對話範例

**爸媽：**「講個睡前故事吧 🌙」

**AI（啟動技能）：**
```
🌙 睡前故事精靈上線啦！
星星都出來了，月亮也高高掛在天上……
今晚想聽什麼樣的故事呢？

✨ 請告訴我：
1️⃣  主角是誰？（小兔子、小熊、恐龍、公主、機器人...）
2️⃣  年齡大小？（2-3歲 / 4-6歲）
3️⃣  故事長度？（短短的 / 中等的 / 長長的）
4️⃣  想要什麼主題？
   🌈 友誼冒險   💤 認識情緒   🏠 成語改編   📖 格林童話改編   ✨ 原創故事

或者直接說「隨便一個」，我來幫你選！ 🎵
```

**爸媽：**「來個關於小兔子的故事，適合4歲」

**AI：** 生成故事 + 朗讀提示

---

## 故事生成參數（story_generator.py）

```
--age {toddler,preschool}   年齡：toddler=2-3歲，preschool=4-6歲
--length {short,medium,long}  長度：短/中/長
--theme {friendship,emotion,idiom,fairytale,original}  主題
--protagonist NAME           主角名稱
--pet NAME                   寵物角色
--sequel-to STORY_ID         續集：接續某個故事
--list-templates             列出所有模板
```

---

## 朗讀說明（story_player.py）

- 整合 OpenClaw `tts` tool，自動朗讀
- TTS 不可用時，彩色文字輸出
- 朗讀速度：慢速，適合幼兒
- 每段顯示：角色 Emoji + 進度「第 3/5 段 🌙」

---

## 睡前作息（Cron 模式）

建議設定每日 20:00 Cron Job：
```
python3 scripts/sleep_routine.py --mode cron
```

---

## 觸發關鍵字（精確匹配）
- 講故事、睡前故事、床邊故事、講個故事、寶寶睡覺、晚安故事
- 「說故事」「聽故事」「Story time」「Bedtime story」

---

## 安全與風格規範

- ✅ 全繁體中文，溫暖友善
- ✅ 2-3歲版：短句（≤10字）、疊字、重複句式
- ✅ 大量 Emoji：🌙 ⭐ 🐰 🦋 🐻 🌈 🎵 💤 🐶 🐱
- ❌ 禁止嚇人內容、暴力、過度負面情緒描寫
- ❌ 不需要任何 API key

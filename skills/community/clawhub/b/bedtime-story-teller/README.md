# 🌙 睡前故事精靈 (bedtime-story-teller)

用溫暖的聲音為 2-6 歲孩童說床邊故事的 AI 技能。

## ✨ 功能特色

- 📖 **20+ 原創故事模板**，適合 2-3 歲 & 4-6 歲不同年齡
- 🎤 **TTS 朗讀模式**，用溫柔聲音說故事
- 📚 **故事圖書館**，收藏最愛、追蹤歷史
- 🌙 **睡前作息引導**，配合 Cron Job 自動提醒
- 🎨 **成語改編 + 格林童話改編**，寓教於樂
- ✨ **純 Python 模板系統**，不需要任何 API Key！

## 🚀 快速開始

### 1. 說「講個睡前故事」

```
爸媽：講個睡前故事吧 🌙
AI：   🌙 睡前故事精靈上線啦！今晚想聽什麼？
```

### 2. 命令列工具

```bash
# 隨機故事（預設 2-3 歲，短版）
python3 scripts/story_generator.py

# 指定主角
python3 scripts/story_generator.py --protagonist 小熊

# 4-6 歲版本，長版
python3 scripts/story_generator.py --age preschool --length long

# 情緒主題
python3 scripts/story_generator.py --theme emotion

# 列出所有模板
python3 scripts/story_generator.py --list-templates

# 朗讀故事
python3 scripts/story_player.py --story-json story.json

# 圖書館（收藏 / 歷史）
python3 scripts/story_library.py --list-favorites
python3 scripts/story_library.py --list-history
python3 scripts/story_library.py --guided

# 睡前作息引導
python3 scripts/sleep_routine.py --mode check
python3 scripts/sleep_routine.py --mode setup   # 互動式設定
```

## 📂 目錄結構

```
bedtime-story-teller/
├── SKILL.md                    # 技能定義
├── README.md                   # 本說明
├── LICENSE                     # MIT License
├── .gitignore
└── scripts/
    ├── story_generator.py      # 🌟 核心：故事生成引擎
    ├── story_player.py         # 🎤 朗讀腳本
    ├── story_library.py        # 📚 圖書館管理
    └── sleep_routine.py       # 🌙 作息引導（Cron 用）
```

## 🎨 故事類別

| 類別 | 說明 | Emoji |
|------|------|-------|
| 友誼冒險 | 認識新朋友、一起解決問題 | 🌈 |
| 認識情緒 | 害怕、分享、勇氣、不生氣 | 💤 |
| 成語改編 | 龜兔賽跑、守株待兔新版 | 🏠 |
| 格林童話 | 童話改編，適合幼兒版本 | 📖 |
| 原創互動 | 小烏龜、小蝴蝶、小龍貓 | ✨ |

## 🌙 睡前作息 Cron 設定

建議每天 20:00 自動提醒：

```bash
# 安裝 crontab
(crontab -l 2>/dev/null; echo "0 20 * * * cd ~/.qclaw/skills/bedtime-story-teller && python3 scripts/sleep_routine.py --mode cron >> /tmp/sleep_routine.log 2>&1") | crontab -

# 查看 crontab
crontab -l
```

## 📖 故事生成參數

```
--protagonist, -p  主角名稱（小兔子、小熊、小狐狸…）
--pet              寵物角色（小狗狗、小貓咪、小烏龜…）
--age, -a          toddler（2-3歲）/ preschool（4-6歲）
--length, -l       short（短）/ medium（中）/ long（長）
--theme, -t        friendship / emotion / idiom / fairytale / original
--sequel-to        接續某個故事，生成續集
--seed             隨機種子（重現相同故事）
```

## 💾 資料儲存

- 最愛收藏：`~/.qclaw/kids/favorites.json`
- 播放歷史：`~/.qclaw/kids/history.json`
- 作息設定：`~/.qclaw/kids/sleep_routine.json`

## 🌟 故事特色

- **2-3歲版本**：短句（≤10字）、疊字、重複句式，如「月亮好亮好亮，星星眨眨眼睛」
- **4-6歲版本**：情節稍完整，有簡單角色發展
- **全程繁體中文**，溫暖友善語氣
- **大量 Emoji**：🌙 ⭐ 🐰 🦋 🐻 🌈 💤 🐶
- **零嚇人內容、零暴力、零過度負面情緒**

## 📝 License

MIT License — 可自由使用、修改、分享。

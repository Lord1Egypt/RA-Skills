# MEMORY.md - 小鑽風-claw-rpg 項目記憶

## 項目定位
Claw RPG Skill —— OpenClaw 的 RPG 彩蛋系統，讓 AI 對話有遊戲感。
- GitHub: `RAMBOXIE/RAMBOXIE-claw-rpg`，ClawhHub slug: `claw-rpg`
- 本地路徑: `D:\Projects\claw-rpg`

## 核心功能（v1.1.0 已完成）
- 6 屬性：爪力/觸覺/殼厚/腦芯/慧眼/魅影，從 SOUL.md+IDENTITY.md+MEMORY.md 關鍵詞派生
- 6 職業自動判定（戰士/法師/吟遊/遊俠/聖騎/德魯伊）
- 等級 1-999，prestige 系統，XP = token 消耗/10 + 產出×2/10
- `--type` 動態屬性成長：20 次同類對話觸發對應屬性+1
- 每日自報家門（greet.mjs），中英文自動切換，6 職業不同 RPG 語氣
- 對話小尾巴：XP/等級/積累進度/屬性成長全展示
- 多語言吐槽通知（Telegram）
- Web Dashboard（React+Recharts，port 3500）

## 關鍵腳本
- `scripts/easter.mjs` — 對話結算彩蛋，每次回覆後由中鑽風觸發
- `scripts/greet.mjs` — 每日自報家門

## 待辦
- ClawhHub 重新 import v1.1.0（當前 pinned commit 偏舊）
- 竞技场 P1 實現

## Git 信息
- branch: main（或 master，確認前先 git log）
- 最新已知 commit: v1.1.0 完成時

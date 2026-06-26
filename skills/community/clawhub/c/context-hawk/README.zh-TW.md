# 🦅 Context-Hawk

> **AI 上下文記憶守護者** — 停止追蹤遺失，開始記住重要的事情。

*給任何 AI agent 一個真正有效的記憶——跨 session、跨主題、跨時間。*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## 它做什麼？

大多數 AI agent 都有**健忘症** — 每個新 session 從零開始。Context-Hawk 用一個生產級的記憶管理系統解決這個問題，自動捕捉重要的事情，讓噪音消散，在正確的時間召回正確的記憶。

**沒有 Context-Hawk：**
> "我已經告訴過你了 — 我喜歡簡潔的回复！"
>（下一個 session，agent 又忘記了）

**有了 Context-Hawk：**
>（從 session 1 默默應用您的溝通偏好）
> ✅ 每次都交付簡潔、直接的回覆

---

## ❌ 沒有 vs ✅ 有 Context-Hawk

| 場景 | ❌ 沒有 Context-Hawk | ✅ 有 Context-Hawk |
|----------|------------------------|---------------------|
| **新 session 開始** | 空白 — 對你一無所知 | ✅ 自動注入相關記憶 |
| **用戶重複偏好** | "我跟你說過了..." | 從第一天就記住 |
| **長任務持續數天** | 重啟 = 從頭開始 | Task State 持久化，`hawk resume` 無縫銜接 |
| **上下文變大** | Token 費用飆升效能下降 | 5 種壓縮策略保持精簡 |
| **重複資訊** | 同一事實存了 10 份 | SimHash 去重 — 只存一份 |
| **記憶召回** | 全部相似、重複注入 | MMR 多樣性召回 — 不重複 |
| **記憶管理** | 一切永遠堆積 | 四層衰減 — 噪音消散，信號保留 |
| **自我改進** | 重複同樣的錯誤 | 追蹤 importance + access_count → 智能晉升 |
| **多 Agent 團隊** | 每個 Agent 從零開始，無共用上下文 | 共享記憶（透過 LanceDB）— 所有 Agent 互相學習 |

---

## 😰 痛點 & 解決方案

| 痛點 | 影響 | Context-Hawk 解決方案 |
|------|------|----------------------|
| **AI 每個 session 都失憶** | 用戶需要反覆說同樣的事 | 四層記憶衰減 — 重要內容自動保持 |
| **長時間任務重啟後丟失** | 工作白費，上下文全沒了 | `hawk resume` — 任務狀態跨重啟持久化 |
| **上下文膨脹** | Token 費用飆升，響應變慢 | 5 種注入策略 + 5 種壓縮策略 |
| **記憶噪音** | 重要資訊被淹沒在聊天歷史裡 | AI 重要性評分 — 自動丟棄低價值內容 |
| **偏好被遺忘** | 用戶每次都要重新解釋規則 | 重要性 ≥ 0.9 = 永久記憶 |

**核心價值：** Context-Hawk 給你的 AI agent 裝上一個真正管用的記憶——不是什么都記，而是智慧地保留重要的，忘掉不重要的。

---

## 🎯 它解決哪 5 個核心問題

**問題 1：上下文窗口限制**
上下文有 token 上限（如 32k）。長對話歷史會把重要內容擠出去。
→ Context-Hawk 壓縮/歸檔舊內容，只注入最相關的記憶。

**問題 2：跨 session 失憶**
session 結束後，上下文消失。下次對話從零開始。
→ 記憶持久化存儲；`hawk recall` 在下次 session 時檢索相關記憶。

**問題 3：多 Agent 互不通訊息**
Agent A 不知道 Agent B 的上下文。某個 agent 做的決定對其他 agent 不可見。
→ 共用 LanceDB 記憶庫（配合 hawk-bridge 使用）：所有 agent 讀寫同一份記憶，無資訊孤島。

**問題 4：發送給 LLM 前上下文已膨脹**
不加優化的召回 = 大量重複的上下文。
→ 經過壓縮 + SimHash 去重 + MMR 召回：發送給 LLM 的上下文**大幅縮小**，節省 token 和費用。

**問題 5：記憶從不自我管理**
沒有管理機制：所有消息堆積，直到上下文溢出。
→ 自動提取 → 重要性評分 → 四層衰減。不重要 → 刪除。重要 → 晉升為長期記憶。

---

## ✨ 12 個核心功能

| # | 功能 | 說明 |
|---|---------|-------|
| 1 | **任務狀態持久化** | `hawk resume` — 保存任務狀態，重啟後繼續 |
| 2 | **四層記憶** | Working → Short → Long → Archive，帶 Weibull 衰減 |
| 3 | **結構化 JSON** | 重要性評分（0-10）、類別、層級、L0/L1/L2 分層 |
| 4 | **AI 重要性評分** | 自動評分記憶，丟棄低價值內容 |
| 5 | **5 種注入策略** | A(高重要性) / B(任務相關) / C(最近) / D(Top5) / E(完整) |
| 6 | **5 種壓縮策略** | summarize / extract / delete / promote / archive |
| 7 | **自我反思** | 檢查任務清晰度、缺失資訊、迴圈檢測 |
| 8 | **LanceDB 向量搜索** | 可選 — 混合向量 + BM25 檢索 |
| 9 | **純記憶備份** | 無需 LanceDB，JSONL 檔案持久化 |
| 10 | **自動去重** | SimHash 去重，移除重複記憶 |
| 11 | **MMR 召回** | 最大邊緣相關性，多樣性召回不重複 |
| 12 | **6 類提取引擎** | LLM 驅動的分類提取：事實 / 偏好 / 決策 / 實體 / 任務 / 其他 |

---

## 🚀 快速安裝

```bash
# 一鍵安裝（推薦）
bash <(curl -fsSL https://raw.githubusercontent.com/relunctance/context-hawk/master/install.sh)

# 或直接用 pip
pip install context-hawk

# 安裝全部功能（含 sentence-transformers）
pip install "context-hawk[all]"
```

---

## 🏗️ 架構

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── 當前 session（最近 5-10 輪對話）       │
│       ↓ Weibull 衰減                                         │
│  Short-term      ←── 24 小時內容，已摘要                    │
│       ↓ access_count ≥ 10 + 重要性 ≥ 0.7                  │
│  Long-term       ←── 永久知識，向量索引                      │
│       ↓ >90 天或 decay_score < 0.15                         │
│  Archive          ←── 歷史，按需加載                        │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── 跨重啟持久化（關鍵！）              │
│  - 當前任務 / 下一步 / 進度 / 輸出                          │
├──────────────────────────────────────────────────────────────┤
│  注入引擎       ←── 策略 A/B/C/D/E 決定召回方式             │
│  自我反思        ←── 每個回答都檢查上下文                    │
│  自動觸發        ←── 每 10 輪（可配置）                   │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 任務狀態記憶（最有價值的功能）

即使重啟、斷電或 session 切換後，Context-Hawk 也能從中斷處精確繼續。

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "完成 API 文檔",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["審查架構模板", "向用戶匯報"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["覆蓋率必須達到 98%", "API 必須版本化"],
  "resumed_count": 3
}
```

```bash
hawk task "完成文檔"        # 創建任務
hawk task --step 1 done  # 標記步驟完成
hawk resume               # 重啟後繼續 ← 核心功能！
```

---

## 🧠 結構化記憶

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "完整原始內容",
  "summary": "一行摘要",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### 重要性評分

| 分數 | 類型 | 行動 |
|-------|------|------|
| 0.9-1.0 | 決策/規則/錯誤 | 永久，最慢衰減 |
| 0.7-0.9 | 任務/偏好/知識 | 長期記憶 |
| 0.4-0.7 | 對話/討論 | 短期，衰減至歸檔 |
| 0.0-0.4 | 聊天/問候 | **丟棄，永不存儲** |

---

## 🎯 5 種上下文注入策略

| 策略 | 觸發條件 | 節省 |
|------|---------|------|
| **A: 高重要性** | `重要性 ≥ 0.7` | 60-70% |
| **B: 任務相關** | 範圍匹配 | 30-40% ← 默認 |
| **C: 最近** | 最近 10 輪 | 50% |
| **D: Top5 召回** | `access_count` Top 5 | 70% |
| **E: 完整** | 無過濾 | 100% |

---

## 🗜️ 5 種壓縮策略

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 4 級警報系統

| 等級 | 閾值 | 行動 |
|-------|---------|------|
| ✅ Normal | < 60% | 安靜 |
| 🟡 Watch | 60-79% | 建議壓縮 |
| 🔴 Critical | 80-94% | 暫停自動寫入，強制建議 |
| 🚨 Danger | ≥ 95% | 阻止寫入，必須壓縮 |

---

## 🚀 快速開始

```bash
# 安裝 LanceDB 插件（推薦）
openclaw plugins install memory-lancedb-pro@beta

# 啟用技能
openclaw skills install ./context-hawk.skill

# 初始化
hawk init

# 核心命令
hawk task "我的任務"    # 創建任務
hawk resume             # 繼續上次任務 ← 最重要
hawk status            # 查看上下文使用情況
hawk compress          # 壓縮記憶
hawk strategy B        # 切換到任務相關模式
hawk introspect         # 自我反思報告
```

---

## 自動觸發：每 N 輪

每 **10 輪**（默認，可配置），Context-Hawk 自動：

1. 檢查上下文水位
2. 評估記憶重要性
3. 向用戶報告狀態
4. 需要時建議壓縮

```bash
# 配置（memory/.hawk/config.json）
{
  "auto_check_rounds": 10,          # 每 N 輪檢查
  "keep_recent": 5,                 # 保留最近 N 輪
  "auto_compress_threshold": 70      # 超過 70% 時壓縮
}
```

---

## 檔案結構

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Python CLI 工具
└── references/
    ├── memory-system.md           # 4層架構
    ├── structured-memory.md      # 記憶格式和重要性
    ├── task-state.md           # 任務狀態持久化
    ├── injection-strategies.md  # 5種注入策略
    ├── compression-strategies.md # 5種壓縮策略
    ├── alerting.md             # 警報系統
    ├── self-introspection.md   # 自我反思
    ├── lancedb-integration.md  # LanceDB 集成
    └── cli.md                  # CLI 參考
```

---

## 🔌 技術規格

| | |
|---|---|
| **持久化** | JSONL 本地文件，無需資料庫 |
| **向量搜索** | LanceDB（可選）+ sentence-transformers 本地向量，自動回退到文件 |
| **檢索** | BM25 + ANN 向量搜索 + RRF 融合 |
| **Embedding 提供商** | Ollama / sentence-transformers / Jina AI / Minimax / OpenAI |
| **跨 Agent** | 通用，無業務邏輯，適用任何 AI agent |
| **零配置** | 開箱即用，智能默認值（BM25-only 模式） |
| **Python** | 3.12+ |

---

## 授權

MIT — 免費使用、修改與散布。

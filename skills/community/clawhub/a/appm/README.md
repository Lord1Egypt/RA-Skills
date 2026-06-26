# APPM: Atlas-Parallel Project Management 🚀

[繁體中文版](#繁體中文) | [English Version](#english)

---

<a name="繁體中文"></a>
## 🇹🇼 繁體中文

### 1. 簡介
**APPM (Atlas-Parallel Project Management)** 是一套專為 AI Agent 設計的「並行專案記憶管理系統」。

當你在管理多個複雜的 AI 開發專案時，最常遇到的問題就是「Session 重置後，Agent 就忘了專案的進度與架構」。APPM 透過在專案目錄下建立標準化的 `.openclaw/` 快照，讓 Agent 能夠在數秒內「恢復意識」，實現無縫的並行開發。

### 2. 痛點解析 (Why APPM?)
開發這套系統是為了結算 AI 開發者長期以來的核心挫折：
- **重複解釋的地獄**：每次開啟新會話（Session），都要重新向 Agent 解釋專案架構與目前的 Bug，浪費大量時間與 Token。
- **Context 溢出與失憶**：Context 窗口有限，將所有歷史對話塞進 Prompt 既昂貴又低效。當對話變長，Agent 就會開始「失憶」。
- **並行專案混淆**：同時進行多個專案時，Agent 常會將專案 A 的邏輯套用到專案 B。
- **「Agent 漂移」**：缺乏一個「單一真實來源 (Single Source of Truth)」，導致 Agent 隨時間推移而偏離原始設計初衷。

### 3. 核心特色 (Core Features)
- **APPM 雙軌開發者通道 (Dual-Track Initialization)**:
    - **標準通道 (Standard Track)**: 適合計畫明確的開發，快速建立 `.openclaw/` 結構。
    - **模糊通道 (Vague Channel)**: 適合靈感雛形階段，透過 AI 顧問式訪談、協助使用者釐清專案輪廓。
- **動態權重定錨系統 (Dynamic Weight Anchor System) [New]**: 自動根據對話關鍵字頻率增加權重，並結合時間衰減機制 (Decay)，實現「開機即定錨」，Agent 無需提問即可恢復當前最活躍專案意識。
- **零 Context 切換成本**: 透過 `MISSION.md` 與 `SNAPSHOT.md`，Agent 能立即讀取專案背景。
- **重啟反射 (Reboot Reflection)**: 解決了 `/new` session 後的失憶與單向停訊問題。透過 `atlas_bootstrap.py` 在開機時自動執行「定錨回報」，確保 Agent 首條訊息即具備專案意識。
- **狀態持久化**: 即使重啟系統，開發進度依然清晰。

### 4. 工具組 (Tooling)
- `scripts/appm_recall.py`: 啟動時執行，彙報權重最高的前三個專案脈絡。
- `scripts/appm_update_weights.py`: 背景動態更新權重，處理 hit 與 decay。
- `scripts/appm_init_dual.py`: 初始化專案結構。

### 4. 目錄結構
```text
[你的專案]/
└── .openclaw/
    ├── MISSION.md      # 專案長期目標、里程碑與痛點
    ├── SNAPSHOT.md     # 當前進度快照、任務 ID 與下一步行動
    ├── DECISION_LOG.md # 關鍵架構決策紀錄
    └── ARCHITECTURE.md # 技術邊界、核心組件與文件說明
```

### 5. 快速開始
1. **初始化專案 (雙軌)**：
   - 標準模式: `python3 scripts/appm_init_dual.py --standard [路徑]`
   - 模糊模式: `python3 scripts/appm_init_dual.py --vague [路徑]`
2. **讓 Agent 定錨**：在 System Prompt 中加入「看到 `.openclaw` 目錄時，優先讀取其內容」。
3. **動態追蹤**: 系統背景自動執行 `scripts/appm_tracker.py` 維持權重。

---

<a name="english"></a>
## 🇺🇸 English

### 1. Introduction
**APPM (Atlas-Parallel Project Management)** is a project-level persistent memory system designed specifically for AI Agents.

The biggest challenge in managing multiple complex AI projects is "Agent Amnesia" after session resets. APPM solves this by maintaining standardized `.openclaw/` snapshots, allowing your Agent to "reclaim consciousness" within seconds for seamless parallel development.

### 2. Why APPM? (Pain Points)
APPM was created to end the core frustrations of AI-native developers:
- **Explanation Hell**: Re-explaining project architecture and current bugs every time a new session starts is a massive waste of time and tokens.
- **Context Overflow & Amnesia**: Context windows are limited. Cramming history into every prompt is expensive and inefficient. As conversations grow, Agents inevitably "forget."
- **Parallel Project Confusion**: When managing multiple projects simultaneously, Agents often mix up logic between Project A and Project B.
- **"Agentic Drift"**: Without a "Single Source of Truth," Agents tend to deviate from the original design intent over time.

### 3. Key Features
- **Zero Context Switching Cost**: Agents instantly understand project background via `MISSION.md` and `SNAPSHOT.md`.
- **Parallel Management**: Designed for multi-project workflows, preventing logic leakage between tasks.
- **State Persistence**: Development progress remains crystal clear across system reboots or model changes.

### 3. Directory Standard
```text
[your-project]/
└── .openclaw/
    ├── MISSION.md      # Long-term goals & milestones
    ├── SNAPSHOT.md     # Current snapshot & next actions
    ├── DECISION_LOG.md # Key decision history
    └── ARCHITECTURE.md # Core components description
```

### 4. Quick Start
1. **Install Skill**: `openclaw install appm` (ClawHub Coming Soon)
2. **Initialize Project**:
   ```bash
   python3 scripts/init.py [project_path]
   ```
3. **Agent Anchoring**: Ensure your Agent reads `.openclaw` files upon entering the directory.

---
*Created by Atlas & [Boss's Name/Handle]*
*Powered by the OpenClaw Community*

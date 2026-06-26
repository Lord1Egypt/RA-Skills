# APPM - Atlas-Parallel Project Management

## 1. 簡介 (Description)
`appm` (Atlas-Parallel Project Management) 是一套為 AI Agent 設計的「並行專案記憶管理系統」。它透過在每個專案目錄下建立 `.openclaw/` 資料夾，並維護 `MISSION.md` 與 `SNAPSHOT.md` 等核心快照文件，解決了 LLM 在多專案並行切換時遺失進度、架構與決策背景的問題。

## 2. 核心機制 (Core Mechanism)
### A. [專案定錨] - 記憶恢復 (Memory Restoration)
當 Agent 進入一個包含 `.openclaw/` 的目錄時，**必須強制讀取**：
1. `MISSION.md`：理解該專案的終極目標與目前的里程碑進度。
2. `SNAPSHOT.md`：獲取最新的執行快照、代碼路徑與「下一步行動 (Next Action)」。

### B. [狀態更新] - 快照義務 (Snapshot Obligation)
在以下情境下，Agent 應主動提議或更新 `SNAPSHOT.md`：
- **重大里程碑達成**：例如完成了一個核心功能的開發或修復。
- **架構變動**：檔案路徑更名、API 介面異動。
- **專案切換或重置前**：在切換到另一個專案或執行 `/new` 指令前，主動更新進度快照。

## 3. 目錄規範 (Directory Standard)
```text
[project-root]/
└── .openclaw/
    ├── MISSION.md      # 專案使命與里程碑 (Long-term)
    ├── SNAPSHOT.md     # 最新狀態快照 (Episodic)
    ├── DECISION_LOG.md # 重大決策歷史 (Log)
    └── ARCHITECTURE.md # 核心架構與組件說明 (Design)
```

## 4. 使用方式 (Usage)
### A. 指令與工作流
- **`/newproject`**: 啟動雙軌初始化通道。Atlas 會詢問專案路徑、模式（標準/模糊）並引導完成定錨。
- **`openclaw appm init [project_path]`**: 快速初始化標準目錄結構。
- **`openclaw appm snapshot`**: 由 Agent 自動執行對話摘要並更新 `SNAPSHOT.md`。
- **`openclaw appm status`**: 顯示全域專案權重與儀表板。

### B. 核心指紋與權重
系統會自動追蹤對話關鍵字，並更新 `data/appm_registry.json` 中的權重。權重最高的專案將在下次重啟時自動加載。

---
*Powered by Atlas & OpenClaw Community*

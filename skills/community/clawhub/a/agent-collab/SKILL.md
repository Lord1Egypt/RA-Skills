---
name: agent-collab
description: "Multi-agent collaboration framework for OpenClaw. Three modes: Dispatch (one-shot tasks via spawn), Collaborate (multi-turn cross-department via persistent sessions), and Direct Chat (user talks to department head directly). Includes org hierarchy definition, HANDOFF push mechanism, and scope-isolated memory. 中文名：跨部门协作框架。触发词：跨部门、协同、调度任务、派给XX、让XX做、协作。"
---

# Agent Collaboration Framework / 跨部門協作框架

## 概述

OpenClaw 多 Agent 部署下的協作機制。定義三種工作模式，解決「怎麼讓多個 Agent 協同工作並在一個對話框返回結果」的問題。

## 三種模式

### 1. 調度模式（Dispatch）
**場景：** 一次性任務，不需要來回
**方法：** `sessions_spawn(agentId="<target>", mode="run", task="...")`
**結果：** 自動回到發起者的對話框

```
用戶 → Main: "幫我查下 LanceDB 狀態"
Main → spawn tech(mode="run"): "檢查 LanceDB 數據庫..."
tech 執行完畢 → 結果自動回到 Main → Main 彙報用戶
```

**適用：** 數據查詢、狀態檢查、生成報告、執行腳本

### 2. 協同模式（Collaborate）
**場景：** 需要多輪對話，跨部門需要來回討論
**方法：**
1. `sessions_spawn(agentId="<target>", mode="session")` → 建立持久 session
2. `sessions_send(sessionKey, message)` → 發送後續消息
3. 結果自動回到發起者的對話框

```
用戶 → Main: "分析 VGS 稅務優化"
Main → spawn finance(mode="session"): "分析 VGS 在 Trust 下的稅務影響"
finance → 回初步分析 + 追問
Main → sessions_send: "Trust 結構是 Little Max，Trustee 是 Gui Holdings"
finance → 回完整分析
Main → spawn ecommerce(mode="run"): "老金說走公司省稅，你看現金流夠嗎"
ecommerce → 回現金流建議
Main → 綜合兩邊 → 彙報用戶
```

**適用：** 需要追問的分析、跨部門協調、需要上下文的任務

### 3. 細聊模式（Direct Chat）
**場景：** 用戶想深入參與討論
**方法：** 用戶直接到對應部門主管的 Bot 對話框
**結果：** 在該 Bot 的對話框

```
用戶直接找 @NaiPo_FinBot: "老金，我想詳細討論一下稅務規劃..."
```

**適用：** 深度討論、反覆修改、用戶想全程參與

## 組織架構定義

### 高階部門（有獨立 Bot）
| 部門 | 代號 | 角色 | 可調度 |
|------|------|------|--------|
| 總管 | Main | 全局監督、跨部門協調 | 所有 agent |
| 內容 | Content | 內容策劃、自媒體 | designer, creator, research, outline, writing |
| 財務 | Finance | 投資、稅務、財報 | research, data |
| 技術 | Tech | 系統維護、安全 | — |
| 電商 | Ecommerce | 選品、供應商、平台 | research |

### 低階部門（無獨立 Bot）
| 代號 | 職責 | 被誰調度 |
|------|------|----------|
| research | 搜索調研 | 所有高階 |
| writing | 寫作翻譯 | Content |
| data | 數據分析 | Finance |
| creator | 腳本視頻 | Content |
| designer | 設計生圖 | Content |
| seo | SEO 增長 | Content |
| outline | 大綱 | Content |

### 原則
- **高階→低階 = 調度**（`subagents.allowAgents` 配置）
- **高階↔高階 = 協同**（`sessions_spawn` + `sessions_send`）
- **部門主管在自己範圍內自主調度**，不需要經過 Main
- **低階可升級為高階**（業務量增長後分配獨立 Bot）

## HANDOFF 機制（異步推送）

當 session 可能中斷時，用文件推送代替即時通信：

```bash
# Main 推任務給 Content
写入 ~/.openclaw/workspace-content/HANDOFF-FROM-MAIN.md

# Content 推結果給 Main
写入 ~/.openclaw/workspace/HANDOFF-FROM-CONTENT.md
```

### HANDOFF 格式
```markdown
# 來源→目標：任務標題
> 時間，背景說明

## 具體內容
- 任務描述
- 技術資料
- 截止時間

---
*接收方讀取後刪除此文件*
```

### 規則
- **Push, Not Pull** — 主動推送，不等對方來要
- 接收方讀取後刪除文件，表示已接收
- 禁止「等他來問我就給他」

## 安裝配置

### 1. openclaw.json — sessions 可見性
```json
{
  "tools": {
    "sessions": {
      "visibility": "all"
    }
  }
}
```

### 2. openclaw.json — subagents 配置（調度權限）
```json
{
  "agents": {
    "content": {
      "subagents": {
        "allowAgents": ["designer", "creator", "research", "outline", "writing", "seo"]
      }
    },
    "finance": {
      "subagents": {
        "allowAgents": ["research", "data"]
      }
    }
  }
}
```

### 3. 各部門 workspace 目錄
```bash
~/.openclaw/workspace/          # Main
~/.openclaw/workspace-content/  # Content
~/.openclaw/workspace-finance/  # Finance
~/.openclaw/workspace-tech/     # Tech
~/.openclaw/workspace-ecommerce/ # Ecommerce
```

### 4. 在 Main AGENTS.md 加入三模式規則
參考本 skill 的模式定義，加入 AGENTS.md。

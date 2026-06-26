---
name: agent-optimize
description: >
  Agent 優化診斷技能。分析 OpenClaw 運行狀態，識別信息過載、上下文堆積、技能噪音等問題。
  提供系統級優化方案，實現瘦身提速，解決"貴慢亂"困擾。
  Use when: (1) Agent 響應變慢，
  (2) 上下文過長導致效率低下，
  (3) 技能加載過多造成噪音，
  (4) 需要診斷性能瓶頸，
  (5) 需要優化建議報告，
  (6) 定期健康檢查，
  (7) 模型使用成本過高，
  (8) 技能衝突或冗餘。
  Triggers: "優化 Agent", "診斷性能", "信息過載", "context overload", "optimize agent",
  "agent health", "performance audit", "skill audit", "context cleanup",
  "system optimization", "agent slowdown", "too many skills", "context too long"。
tags: [meta, optimization, performance, health, audit, diagnostic, core]
permissions: [shell, read, analyze]
metadata:
  clawdbot:
    requires:
      bins: [node, jq]
    files: ["src/**", "scripts/**", "reports/**"]
  capabilities:
    allow:
      - execute: [find, grep, wc, du, ps, pgrep]
      - read: [workspace/**, ~/.openclaw/**, ~/.npm-global/lib/node_modules/openclaw/**]
      - analyze: [skill-configs, session-logs, memory-files]
    deny:
      - execute: ["!find", "!grep", "!wc", "!du", "!ps", "!pgrep", "!node"]
      - write: [workspace/**, ~/.openclaw/**]
      - network: ["*"]
  env_declarations:
    - name: OPTIMIZE_MAX_CONTEXT_LINES
      required: false
      default: "5000"
      description: Maximum context lines to analyze in one pass.
    - name: OPTIMIZE_REPORT_FORMAT
      required: false
      default: "markdown"
      description: "Report format: markdown, json, feishu-card."
    - name: OPTIMIZE_AUTO_FIX
      required: false
      default: "false"
      description: Auto-apply recommended fixes (use with caution).
---

# 🩺 Agent Optimize - Agent 優化診斷技能

**"不是模型不行，而是上下文堆積或技能噪音導致效率低下。"**

Agent Optimize 是一個系統級體檢顧問，幫助你診斷 OpenClaw 的"信息過載"問題，找出拖慢點，提供優化方案，實現系統級瘦身。

## 核心問題診斷

### 1. 上下文堆積 (Context Bloat)
**症狀:**
- Agent 響應變慢
- Token 使用量激增
- 模型成本上升

**診斷方法:**
```bash
# 檢查會話歷史大小
find ~/.openclaw/sessions -name "*.json" -exec wc -l {} \; | sort -rn | head -10

# 檢查記憶文件總大小
du -sh ~/.openclaw/workspace/*/memory/** 2>/dev/null
```

**優化方案:**
- 清理舊會話歷史（保留最近 7 天）
- 壓縮記憶文件（歸檔超過 30 天的記錄）
- 設置上下文長度限制

### 2. 技能噪音 (Skill Noise)
**症狀:**
- 加載不必要技能
- 技能衝突
- 技能冗餘

**診斷方法:**
```bash
# 列出所有已安裝技能
find ~/.npm-global/lib/node_modules/openclaw/skills -maxdepth 1 -type d | wc -l
find ~/.openclaw/workspace*/skills -maxdepth 2 -type d | wc -l

# 檢查技能依賴
grep -r "requires" ~/.openclaw/workspace*/skills/*/SKILL.md | head -20
```

**優化方案:**
- 禁用未使用技能
- 合併重復功能技能
- 優化技能加載順序

### 3. 記憶冗餘 (Memory Redundancy)
**症狀:**
- 記憶文件重複
- 未清理的臨時文件
- 過期的日誌記錄

**診斷方法:**
```bash
# 查找重複記憶文件
find ~/.openclaw/workspace*/memory -name "*.md" -exec md5sum {} \; | sort | uniq -d

# 檢查記憶文件大小
find ~/.openclaw/workspace*/memory -name "*.md" -exec wc -l {} \; | sort -rn | head -10
```

**優化方案:**
- 合併重複記憶
- 刪除臨時文件
- 歸檔舊記憶

### 4. 配置衝突 (Config Conflicts)
**症狀:**
- 多個配置文件
- 配置值衝突
- 過期配置項

**診斷方法:**
```bash
# 查找所有配置文件
find ~/.openclaw -name "*.json" -path "*/config*" 2>/dev/null
find ~/.openclaw -name ".env*" 2>/dev/null

# 檢查配置重複
grep -r "model" ~/.openclaw/*.json 2>/dev/null | head -10
```

**優化方案:**
- 合併配置文件
- 統一配置源
- 清理過期配置

---

## 使用方法

### 基本用法

```bash
# 運行完整診斷
node index.js

# 僅檢查上下文
node index.js --context

# 僅檢查技能
node index.js --skills

# 僅檢查記憶
node index.js --memory

# 僅檢查配置
node index.js --config

# 生成優化報告
node index.js --report
```

### 高級用法

```bash
# 深度診斷（更詳細）
node index.js --deep

# 自動應用安全優化
node index.js --auto-fix

# 輸出 JSON 格式
node index.js --json

# 輸出 Feishu 卡片格式
node index.js --feishu-card

# 指定工作區
node index.js --workspace /path/to/workspace
```

---

## 診斷報告結構

### 1. 執行摘要

```markdown
## 📊 Agent 健康狀態

**總體評分:** 75/100 (需要優化)

**關鍵問題:**
- ⚠️ 上下文堆積：超過 5000 行
- ⚠️ 技能冗餘：12 個未使用技能
- ✅ 記憶狀態：良好
- ⚠️ 配置衝突：2 處重複配置
```

### 2. 詳細分析

#### 上下文分析
```
當前會話數量：45
總會話大小：125 MB
平均會話長度：2,777 行
最大會話：15,432 行 (需要清理)

建議：
- 刪除超過 30 天的會話（可釋放 80 MB）
- 壓縮超過 7 天的會話（可釋放 30 MB）
```

#### 技能分析
```
已安裝技能總數：67
活躍技能（最近 7 天使用）：23
未使用技能：44
技能衝突：2 對

建議：
- 禁用 44 個未使用技能
- 解決 2 對技能衝突
```

#### 記憶分析
```
記憶文件總數：156
總大小：45 MB
重複文件：8
過期文件（>90 天）：23

建議：
- 合併 8 個重複文件
- 歸檔 23 個過期文件
```

#### 配置分析
```
配置文件數量：12
重複配置項：5
過期配置項：3

建議：
- 合併配置文件
- 清理過期配置
```

### 3. 優化方案

#### 即時優化（安全，可自動應用）
1. 清理臨時文件 - 預計釋放 15 MB
2. 歸檔舊會話 - 預計釋放 50 MB
3. 禁用未使用技能 - 減少加載時間 30%

#### 手動優化（需要確認）
1. 合併重複記憶文件
2. 解決技能衝突
3. 重構配置文件

#### 長期優化（建議）
1. 設置自動清理 cron
2. 實施技能白名單
3. 建立記憶歸檔策略

---

## 自動化優化

### 設置定時清理

```bash
# 添加每日清理任務
clawdbot cron add \
  --name "Agent Optimization" \
  --cron "0 3 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "Run agent-optimize with --auto-fix --report"
```

### 設置監控警報

```bash
# 當上下文超過閾值時警報
clawdbot cron add \
  --name "Context Monitor" \
  --cron "0 */6 * * *" \
  --message "Check context size, alert if > 10000 lines"
```

---

## 配置選項

| 配置項 | 預設值 | 說明 |
|--------|--------|------|
| `OPTIMIZE_MAX_CONTEXT_LINES` | 5000 | 單次分析最大上下文行數 |
| `OPTIMIZE_REPORT_FORMAT` | markdown | 報告格式 (markdown/json/feishu-card) |
| `OPTIMIZE_AUTO_FIX` | false | 自動應用安全優化 |
| `OPTIMIZE_BACKUP_BEFORE_FIX` | true | 優化前備份 |
| `OPTIMIZE_RETENTION_DAYS` | 30 | 會話保留天數 |
| `OPTIMIZE_MEMORY_ARCHIVE_DAYS` | 90 | 記憶歸檔天數 |

---

## 輸出示例

### Markdown 報告

```markdown
# Agent 優化診斷報告

**生成時間:** 2026-04-03 09:30:00
**工作區:** /home/admin/.openclaw/workspace-skill-dev

## 📊 總體狀態

評分：75/100

## ⚠️ 發現問題

1. 上下文堆積 (嚴重)
2. 技能冗餘 (中等)
3. 配置重複 (輕微)

## ✅ 優化建議

[詳細建議列表]
```

### JSON 報告

```json
{
  "timestamp": "2026-04-03T09:30:00Z",
  "workspace": "/home/admin/.openclaw/workspace-skill-dev",
  "score": 75,
  "issues": [
    {
      "type": "context_bloat",
      "severity": "high",
      "details": {...}
    }
  ],
  "recommendations": [...]
}
```

---

## 安全規範

### 自動優化限制

**允許自動執行:**
- ✅ 清理臨時文件
- ✅ 歸檔舊會話
- ✅ 壓縮日誌文件
- ✅ 刪除空文件

**需要用戶確認:**
- ⚠️ 刪除會話歷史
- ⚠️ 禁用技能
- ⚠️ 修改配置文件
- ⚠️ 合併記憶文件

### 備份策略

```bash
# 優化前自動備份
backup_dir="/tmp/agent-optimize-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"
cp -r ~/.openclaw/workspace/*/memory "$backup_dir/"
cp -r ~/.openclaw/sessions "$backup_dir/"
```

---

## 故障排除

### 問題：診斷運行緩慢

**原因:** 上下文太大

**解決方案:**
```bash
# 限制分析範圍
node index.js --max-lines 2000

# 或僅分析特定目錄
node index.js --target ~/.openclaw/workspace-skill-dev
```

### 問題：報告生成失敗

**原因:** 權限不足

**解決方案:**
```bash
# 檢查權限
ls -la ~/.openclaw/workspace*/memory

# 修復權限
chmod -R u+rw ~/.openclaw/workspace*/memory
```

### 問題：技能檢測不準確

**原因:** 技能路徑變化

**解決方案:**
```bash
# 更新技能路徑配置
export OPTIMIZE_SKILL_PATHS="~/.npm-global/lib/node_modules/openclaw/skills,~/.openclaw/workspace*/skills"
```

---

## 性能指標

### 診斷速度

| 工作區大小 | 診斷時間 |
|------------|----------|
| 小型 (<100 MB) | <5 秒 |
| 中型 (100-500 MB) | 5-15 秒 |
| 大型 (>500 MB) | 15-30 秒 |

### 優化效果

| 優化項 | 預期改善 |
|--------|----------|
| 上下文清理 | 響應速度 ↑40% |
| 技能精簡 | 加載時間 ↓30% |
| 記憶歸檔 | 存儲空間 ↓50% |
| 配置優化 | 衝突率 ↓80% |

---

## 最佳實踐

### 1. 定期診斷
- 每週運行一次完整診斷
- 每日運行輕量檢查
- 性能下降時立即診斷

### 2. 漸進優化
- 先應用安全優化
- 測試確認後再應用風險優化
- 保留備份以便回滾

### 3. 監控跟蹤
- 記錄每次優化前後指標
- 追蹤長期趨勢
- 調整優化策略

---

## 集成示例

### 與 capability-evolver 集成

```javascript
// 在 evolver 中調用 agent-optimize
const optimize = require('agent-optimize');

async function beforeEvolution() {
  const report = await optimize.diagnose();
  if (report.score < 60) {
    await optimize.autoFix();
  }
}
```

### 與 auto-updater 集成

```javascript
// 更新後自動優化
const optimize = require('agent-optimize');

async function afterUpdate() {
  await optimize.diagnose({ report: true });
}
```

---

## 版本歷史

- **1.0.0** (2026-04-03) - 初始版本
  - 上下文診斷
  - 技能診斷
  - 記憶診斷
  - 配置診斷
  - 優化建議生成

---

## 相關資源

- [OpenClaw 性能優化指南](https://docs.openclaw.ai/performance)
- [上下文管理最佳實踐](https://docs.openclaw.ai/context-management)
- [技能優化指南](https://docs.openclaw.ai/skill-optimization)

---

**版本:** 1.0.0  
**日期:** 2026-04-03  
**狀態:** 初始發布  
**維護者:** skill-dev

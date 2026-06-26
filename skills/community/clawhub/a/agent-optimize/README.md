# Agent Optimize Skill

Agent 優化診斷技能 - 幫助你診斷 OpenClaw 的"信息過載"問題。

## 快速開始

```bash
# 運行完整診斷
node src/index.js

# 運行並保存報告
node src/index.js > reports/diagnosis-$(date +%Y%m%d).md
```

## 功能

- 🔍 **上下文診斷** - 檢查會話堆積、記憶冗餘
- 🧩 **技能診斷** - 檢查技能重複、文檔缺失
- ⚙️ **配置診斷** - 檢查配置衝突、重複項
- 💻 **系統診斷** - 檢查資源使用狀態

## 輸出示例

```
🩺 Agent 優化診斷報告

總體評分：75/100 (需要優化)

發現問題:
1. 🔴 上下文堆積 - 發現 3 個大型會話文件
2. 🟡 技能重複 - 發現 2 個重複技能
3. 🟡 配置重複 - 發現 5 個重複配置項

優化建議:
1. 🔴 清理大型會話 - 可釋放 50 MB
2. 🟡 清理重複技能 - 避免衝突
3. 🟡 合併配置文件 - 統一配置源
```

## 配置

通過環境變量配置：

```bash
export OPTIMIZE_MAX_CONTEXT_LINES=5000
export OPTIMIZE_REPORT_FORMAT=markdown  # 或 json
export OPTIMIZE_AUTO_FIX=false
export OPTIMIZE_RETENTION_DAYS=30
export OPTIMIZE_MEMORY_ARCHIVE_DAYS=90
```

## 集成

### 定時任務

```bash
# 添加每日診斷任務
clawdbot cron add \
  --name "Agent Optimization" \
  --cron "0 3 * * *" \
  --tz "Asia/Shanghai" \
  --message "Run agent-optimize diagnosis"
```

### 與其他技能集成

在 capability-evolver 中調用：

```javascript
const { execSync } = require('child_process');
const report = execSync('node skills/agent-optimize/src/index.js', { encoding: 'utf-8' });
```

## 文件結構

```
agent-optimize/
├── SKILL.md          # 技能定義
├── README.md         # 使用說明
├── src/
│   └── index.js      # 主診斷腳本
└── reports/          # 診斷報告（可選）
```

## 版本

- **1.0.0** (2026-04-03) - 初始版本

## 許可證

MIT

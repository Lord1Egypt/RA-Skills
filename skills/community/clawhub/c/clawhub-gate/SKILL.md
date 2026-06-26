---
name: clawhub-gate
description: |
  ClawHub 发布前安全门禁：本地静态分析 + ClawScan 轮询，确保 skill 通过 VirusTotal + ClawScan 再发布。
  关键词：clawhub publish pre-publish security gate VirusTotal ClawScan shellcheck bandit
triggers:
  - (.*) clawhub (.*) 发布 (.*)
  - (.*) clawhub (.*) sync (.*)
  - (.*) skill (.*) 安全 (.*) 检测 (.*)
  - (.*) 发布 (.*) clawhub (.*) 前 (.*)
  - (.*) clawhub (.*) gate (.*)
required_environment_variables: []
required_commands:
  - shellcheck
  - bandit
  - jq
  - python3
  - clawhub
required_config_paths:
  - ~/.config/clawhub/config.json
---

# ClawHub Pre-Publish Security Gate

`clawhub sync` 前自动执行三项检查，全部通过才放行。

## 流程

```
clawhub_gate.sh
├── 1. 本地静态分析  (即时)
│   ├── shellcheck  →  .sh 文件
│   └── bandit      →  .py 文件
│
└── 2. clawhub sync + ClawScan 轮询  (异步，约 30-90s)
    └── 轮询 clawhub API 直到 scan status != "pending"
        ├── VT=clean + Static=clean + LLM=clean  → 通过
        ├── VT=clean + Static=clean + LLM=suspicious → 警告通过（owner 接受 LLM 情境判断）
        └── VT 或 Static 失败  → 阻断

## 使用方式

在 skill 目录下运行 gate 脚本：

```bash
# 完整 gate：静态分析 + 发布 + ClawScan 轮询
SKILL_DIR=~/.hermes/skills/pg-game-monitor bash clawhub_gate.sh

# 仅本地静态分析（快速检查，不需要网络）
SKILL_DIR=~/.hermes/skills/pg-game-monitor bash clawhub_gate.sh --local-only
```

**前置条件**：已安装 `shellcheck`、`bandit`、`jq`、Python 3、`clawhub` CLI（已登录）。

**脚本行为**：
- 读取 `~/.config/clawhub/config.json` 获取 token（用于轮询 ClawScan API）
- 调用 `clawhub sync` **发布** skill（会创建/更新 ClawHub 版本）
- 若不需发布，先跑 `--local-only` 确认静态分析通过，再手动 `clawhub sync`

## 退出码

| 码 | 含义 |
|----|------|
| 0 | 全部通过 |
| 1 | 静态分析失败或 ClawScan flagged |
| 2 | ClawScan 超时（pending > 120s） |
| 3 | 未找到 skill 目录或权限错误 |

## 检查详情

### 静态分析

| 工具 | 扫描范围 | 严重级别 |
|------|---------|---------|
| shellcheck | `*.sh` | warning + error |
| bandit | `*.py` | medium + high + hidden |

- **阈值**：ERROR 数量 = 0；WARNING 数量 ≤ 10（可配置 `WARN_LIMIT`）
- **误报忽略**：`SC2154`（未使用变量，常见于条件分支）、`SC2086`（引号去除，常见于 `grep -v`）

### ClawScan 轮询

- **轮询间隔**：15s
- **最大等待**：120s（8 次）
- **状态判断**：
  - `clean` → 通过
  - `suspicious` → 失败，输出警告
  - `malicious` → 失败，阻断
  - `pending` → 继续轮询
  - `error` → 失败

## 依赖

```bash
pip install --break-system-packages bandit
apt install -y shellcheck
```

## 参考

- ClawScan 修复指南：`clawhub` skill → `references/clawscan-remediation.md`

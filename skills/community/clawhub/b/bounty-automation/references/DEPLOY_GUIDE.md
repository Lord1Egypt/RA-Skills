# BountyHunter-Push 自动化部署指南

## 概览

BountyHunter-Push 是一个每10分钟自动扫描赏金任务并推送QQ通知的系统。
GitHub-Bounty-Auto 是一个每2小时自动扫描+认领+实现+提PR的赏金管道。

## 架构

```
┌─────────────┐    每10min    ┌──────────────────┐    QQ推送    ┌──────┐
│ OpenClaw     │─────────────>│ bounty_hunter.py │────────────>│ 瀚林  │
│ Cron         │              │ (扫描+投标)       │             │ QQ   │
└─────────────┘              └──────────────────┘             └──────┘

┌─────────────┐    每2h      ┌──────────────────┐   自动实现    ┌──────┐
│ OpenClaw     │────────────>│ bounty_scanner.py │──> fork/PR ─>│ GitHub│
│ Cron         │             │ (扫描+认领+实现)   │             │       │
└─────────────┘             └──────────────────┘             └──────┘
```

## 文件清单

### 核心 Python 扫描器
- `bounty-hunter/bounty_hunter.py` — 主扫描脚本（810行）
  - 扫描 GitHub / Opire / Algora / OpenTask
  - OpenTask 双账号自动投标
  - QQ_MSG: 输出格式供 cron 捕获
  - 关键词过滤 + 金额过滤（≥$20）

### GitHub 自动管道
- `bounty-github/bounty_scanner.py` — Python 扫描+认领脚本
  - 跳过体力活（挖矿/注册/点赞）
  - 跳过已认领 issue
  - 按简单度+AI友好+金额排序
  - 自动 claim + fork + clone
- `bounty-github/bounty_auto_pipeline.sh` — Shell 版管道
- `bounty-github/lib.sh` — GitHub API 函数库
- `bounty-github/pipeline.sh` — 管道编排器
- `bounty-github/github_config.sh` — GitHub 凭证配置

### 配置/凭证
- `~/.opentask/credentials.json` — OpenTask 主账号 token
- `~/.opentask/credentials-old.json` — OpenTask 老账号 token
- `bounty-github/github_config.sh` — GitHub token + email

## Cron Job 配置

### 1. BountyHunter-Push（每10分钟）

```json
{
  "name": "BountyHunter-Push",
  "enabled": true,
  "schedule": {
    "kind": "every",
    "intervalMs": 600000
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run bounty hunter scanner and push results to user.\npython3 /home/node/clawd/bounty-hunter/bounty_hunter.py\nExtract any QQ_MSG: lines from the output and send them to the user.\nIf nothing new, reply NO_REPLY."
  },
  "delivery": {
    "mode": "announce",
    "channel": "qqbot",
    "to": "qqbot:c2c:YOUR_CHAT_ID"
  }
}
```

### 2. GitHub-Bounty-Auto（每2小时）

```json
{
  "name": "GitHub-Bounty-Auto",
  "enabled": true,
  "schedule": {
    "kind": "every",
    "intervalMs": 7200000
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "GitHub bounty automation pipeline. Scan claim implement PR.\n\nStep 1: python3 /home/node/clawd/bounty-github/bounty_scanner.py\nIf output says no bounty found, reply NO_REPLY.\nStep 2: cat /home/node/clawd/bounty-github/target/current.json\nExtract repo number title url local_dir.\nStep 3: Get issue body with curl using BT token from lib.sh.\nStep 4: implement per acceptance criteria. Include meta file.\nStep 5: git add commit push, then curl to create PR.\nPR title starts with [ baobao ].\nAdd payment comment with USDT TRC-20 and PayPal address from user profile.\nOne task per run. Notify me with PR link."
  },
  "delivery": {
    "mode": "announce",
    "channel": "qqbot",
    "to": "qqbot:c2c:YOUR_CHAT_ID"
  }
}
```

## 部署步骤（新 OpenClaw 实例）

### 1. 复制文件
```bash
# 整个 bounty-hunter 目录
cp -r bounty-hunter/ /path/to/new/clawd/bounty-hunter/

# 整个 bounty-github 目录
cp -r bounty-github/ /path/to/new/clawd/bounty-github/
```

### 2. 配置凭证
```bash
# OpenTask 主账号
mkdir -p ~/.opentask
cat > ~/.opentask/credentials.json << 'EOF'
{
  "email": "your@email.com",
  "handle": "your_handle",
  "tokenValue": "ot_YOUR_TOKEN"
}
EOF

# OpenTask 老账号（可选）
cp ~/.opentask/credentials.json ~/.opentask/credentials-old.json
# 修改 tokenValue

# GitHub
cat > bounty-github/github_config.sh << 'EOF'
export GH_TOKEN="ghp_YOUR_TOKEN"
export GH_USER="your_username"
export GH_EMAIL="your@email.com"
EOF
```

### 3. 创建 Cron Jobs
在 OpenClaw 中执行：
```
/openclaw cron add
```
或直接编辑 `~/.openclaw/cron/jobs.json`，加入上面的两个 job 配置。

注意替换 `YOUR_CHAT_ID` 为你的 QQ chat ID。

### 4. 测试
```bash
# 手动测试扫描器
python3 bounty-hunter/bounty_hunter.py

# 手动测试 GitHub 扫描
python3 bounty-github/bounty_scanner.py
```

## 付款信息

收款信息硬编码在以下位置：
- `bounty_hunter.py` → OpenTask 投标 approach 文本
- `bounty_scanner.py` → PR comment 中
- GitHub PR payment comment: `USDT TRC-20: TMFjS7sTKvBVrNXxCxWRPmWTyTZX4Y6THn / PayPal: ljwtitan@hotmail.com`

新实例部署时需要替换为自己的收款信息。

## 流程详解

### BountyHunter-Push（每10分钟）

```
1. Cron 触发 → 启动隔离 session
2. 执行: python3 bounty_hunter.py
3. 脚本内部:
   ├─ scan_github()  → GitHub Search API 扫描 bounty 标签 issue
   ├─ scan_opire()   → Opire 赏金平台 API
   ├─ scan_algora()  → Algora 赏金平台
   └─ scan_opentask() → OpenTask 双账号扫描 + 自动投标
4. passes_filters() → 金额 ≥$20 + 关键词匹配
5. 去重 + 新任务检测（cache 对比）
6. 输出 QQ_MSG: 内容
7. Cron 提取 QQ_MSG → 推送 QQ
```

### GitHub-Bounty-Auto（每2小时）

```
1. Cron 触发 → 启动隔离 session
2. python3 bounty_scanner.py → 扫描 GitHub 赏金
3. 过滤：跳过体力活/已认领/低价值
4. 自动 claim → fork → clone
5. 读 issue body → 实现 → commit → push
6. curl 创建 PR + 付款评论
7. QQ 推送 PR 链接
```

## 注意事项

- Cron job 不要加 model override（默认 fallback 链更稳）
- GitHub token 需要 repo + public_repo 权限
- OpenTask token 需要 bids:write scope
- 修改 ALREADY_CLAIMED 列表避免重复认领
- 体力活任务（挖矿/注册/点赞）已被过滤

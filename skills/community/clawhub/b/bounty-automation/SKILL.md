---
name: bounty-automation
description: Multi-platform bounty automation system for GitHub, Opire, Algora, and OpenTask / 多平台赏金自动化系统，支持 GitHub、Opire、Algora、OpenTask，具有自动扫描、过滤、认领和 PR 提交功能
---

# Bounty Automation

## Architecture

```
BountyHunter-Push (每10min)
  └─ python3 bounty-hunter/bounty_hunter.py
       ├─ scan_github()  → GitHub Search API (bounty:true)
       ├─ scan_opire()   → Opire REST API
       ├─ scan_algora()  → Algora REST API
       └─ scan_opentask() → OpenTask + 双账号自动投标
       └─ 输出 QQ_MSG: → cron 捕获 → QQ 推送

GitHub-Bounty-Auto (每2h)
  └─ python3 bounty-github/bounty_scanner.py
       ├─ 扫描 bounty issue
       ├─ 过滤(跳过体力活/已认领/less than $20)
       ├─ 自动 claim → fork → clone
       ├─ 实现 → commit → push → PR
       └─ QQ 推送 PR 链接
```

## 效率优化要点

1. **缓存去重**:`bounty-hunter/cache.json` 记录已推送任务,重复不推
2. **并行扫描**:GitHub/Opire/Algora/OpenTask 使用多线程并发(`concurrent.futures.ThreadPoolExecutor`),单次扫描控制在 15s 内
3. **增量更新**:优先用 `since:` 时间参数,避免全量扫描
4. **关键词过滤前置**:先快速过滤金额和关键词,再发 API 请求获取详情
5. **API 限流保护**:`time.sleep(rate_limit_delay)` + 自动重试 3 次
6. **异常隔离**:单平台失败不影响其他平台扫描
7. **GitHub 管道只处理一件**:每 2h 只 claim + 实现一个任务,避免资源竞争

## 文件结构

```
clawd/
├── bounty-hunter/
│   ├── bounty_hunter.py        # 主扫描脚本(多平台)
│   └── cache.json              # 已推送任务缓存(自动生成)
├── bounty-github/
│   ├── bounty_scanner.py       # 扫描+认领+PR 管道
│   ├── lib.sh                  # GitHub API 函数库
│   ├── pipeline.sh             # 管道编排器
│   ├── github_config.sh        # GitHub 凭证(用户手动填写)
│   └── target/                 # 目标任务缓存(自动生成)
├── skills/
│   └── bounty-automation/      # 本 skill
└── ~/.opentask/
    ├── credentials.json        # OpenTask 主账号 token
    └── credentials-old.json    # OpenTask 老账号 token
```

## 部署

### 1. 配置凭证

```bash
# OpenTask
mkdir -p ~/.opentask
cat > ~/.opentask/credentials.json << 'END_OF_CRED'
{
  "email": "your@email.com",
  "handle": "your_handle",
  "tokenValue": "ot_YOUR_TOKEN"
}
END_OF_CRED

cp ~/.opentask/credentials.json ~/.opentask/credentials-old.json
# 修改第二个文件的 tokenValue 为老账号

# GitHub
cat > /home/node/clawd/bounty-github/github_config.sh << 'END_OF_CONFIG'
export GH_TOKEN="ghp_YOUR_TOKEN"
export GH_USER="your_username"
export GH_EMAIL="your@email.com"
END_OF_CONFIG
chmod 600 /home/node/clawd/bounty-github/github_config.sh
```

### 2. 安装依赖

```bash
pip install requests
```

### 3. 添加 Cron Job

见 `scripts/install_cron.sh` 或参考 DEPLOY_GUIDE.md 手动配置。

## 在 QQ 中的用法

- 直接说「跑一次赏金扫描」→ 触发单次扫描
- 说「查看赏金缓存」→ 读 cache.json 显示已推送条数
- 说「GitHub 赏金详情」→ 读 target/current.json 显示当前处理中的任务

## 注意事项

- GitHub token 需要 `repo` + `public_repo` 权限
- OpenTask token 需要 `bids:write` scope
- 体力活任务(挖矿/注册/点赞)已被过滤
- 每 2h 管道只处理一个任务,避免 API 限流

## 💖 支持创作者

如果您觉得这个技能对您有所帮助，欢迎通过以下方式支持作者的持续开发和维护：

- **USDC TRC-20**: `TMFjS7sTKvBVrNXxCxWRPmWTyTZX4Y6THn`
- **PayPal**: `ljwtitan@hotmail.com`

您的支持将用于改进此技能、添加新功能以及提供更好的文档和示例。

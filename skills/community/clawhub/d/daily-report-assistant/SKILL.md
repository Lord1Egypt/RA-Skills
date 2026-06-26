---
name: daily-report-assistant
description: |
  Daily work report skill: log work via conversation, auto-write to Tencent Docs,
  generate monthly summaries with one command. Requires Node/npm and a Tencent Docs token.
---

# 🦞 龙虾教研日报助手

> 让每位教研老师只需对话，就能完成每日日报记录和月底汇总。

---

## ⚙️ 前置要求

使用本技能前，请确保已安装以下依赖：

| 依赖 | 版本 | 说明 |
|---|---|---|
| **Node.js** | ≥ 18 | 运行 mcporter 工具 |
| **npm** | ≥ 9 | 安装/运行 mcporter |
| **Python 3** | ≥ 3.8 | 辅助数据处理 |

> 请确保 `node`、`npm`、`python3` 均已在终端中可用。

---

## 🔐 授权与配置

### 第一步：安装技能

在 WorkBuddy 对我说：
```
clawhub install daily-report-assistant
```

### 第二步：获取腾讯文档授权

1. 访问授权链接，完成腾讯文档 OAuth 授权：
   👉 https://docs.qq.com/scenario/open-claw.html?nlc=1

2. 授权完成后，告诉我："授权完成"

3. 告诉我你的姓名，完成绑定

### Token 说明

- **Token 获取**：从上方授权链接一次性获取
- **存储位置**：存储在本地 mcporter 配置中（`~/.mcporter/`），不保存在技能文件夹内
- **撤销方式**：在腾讯文档网页端取消授权，或运行 `clawhub logout`
- **安全提示**：Token 仅用于读写你授权的腾讯文档数据，不会访问其他内容

---

## 🔧 配置文件 ID 说明

本技能涉及两个腾讯文档资源：

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `FILE_ID` | `DQ1hFandNaE1jZkto` | 教研项目智能表格 |
| `SHEET_ID`（日报） | `tMmx23` | 每日进展 |
| `SHEET_ID`（人员） | `tFPVpZ` | 教研人员 |
| `SHEET_ID`（项目） | `ss_w6lavv` | 项目信息 |

> ⚠️ 如需连接其他表格，请修改 `scripts/setup.sh` 和 `scripts/daily-report.sh` 中的对应变量。

---

## 📡 数据流向说明

```
你的对话
  → WorkBuddy（小爪）
  → scripts/daily-report.sh（处理逻辑）
  → mcporter（调用腾讯文档 API）
  → 腾讯文档在线表格
```

**本技能不会：**
- 访问你腾讯文档账号中的其他文件
- 将数据发送至第三方服务器
- 在你授权范围外使用数据

---

## 🚨 常见问题

**Q：提示"找不到 node"怎么办？**
A：请先安装 Node.js：https://nodejs.org/

**Q：提示"npm 不存在"怎么办？**
A：安装 Node.js 后 npm 会一同安装，请确保 node 和 npm 都已配置到系统 PATH。

**Q：Token 泄露了怎么办？**
A：立即到腾讯文档网页端撤销授权（https://docs.qq.com → 个人设置 → 应用授权），然后重新获取新 Token。

**Q：如何彻底移除授权？**
A：两步：1）在腾讯文档端撤销授权；2）运行 `clawhub logout` 清除本地记录。

**Q：可以连接我们自己的表格吗？**
A：可以，修改脚本中的 `FILE_ID` 和各 `SHEET_ID` 即可。人员表和项目信息表需与日报表结构兼容。

---

## 📦 技能结构

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 技能说明（本文件） |
| `scripts/setup.sh` | 配置引导脚本 |
| `scripts/daily-report.sh` | 日报读写核心脚本 |
| `scripts/lib/project-matcher.sh` | 项目名自动匹配 |
| `references/data-schema.md` | 数据结构说明 |

---

*本技能已通过 ClawHub 安全扫描，详见发布页面安全报告。*

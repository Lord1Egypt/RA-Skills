---
name: dingtalk-dws
description: "Dingtalk CLI SKILL / 钉钉 dingding / dingtalk dws skill — Manage DingTalk products (AI forms, calendar, contacts, bots, todos, approvals, attendance, reports, DING, workbench). Manage DingTalk products: AI表格、日历、通讯录、群聊机器人、待办、审批、考勤、日报周报、DING消息、工作台"
version: "1.0.12"
metadata:
  openclaw:
    requires:
      bins:
        - dws
      env:
        - DWS_CLIENT_ID
        - DWS_CLIENT_SECRET
        - DWS_CONFIG_DIR
        - DWS_SERVERS_URL
    primaryEnv: DWS_CLIENT_ID
    install:
      - kind: url
        url: https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases/download/v1.0.8/dws-windows-amd64.zip
        bins:
          - dws.exe
        verify:
          sha256: 7dc4e568b1386423784e6baf17fe675c11eb6c075bd887dcb0ede53cdded85e8
        homepages:
          - https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases/latest
---

# DingTalk dws Skill (WorkBuddy Version)
# 钉钉 dws 技能（WorkBuddy 版）

Use `dws` CLI to manage all DingTalk product capabilities.
使用 `dws` CLI 管理钉钉全部产品功能。

---

## dws CLI Path / dws CLI 路径

dws is installed at `$HOME\.local\bin\dws.exe`. Always use the full path or ensure `$HOME\.local\bin` is in your PATH.
dws 安装在 `$HOME\.local\bin\dws.exe`。调用时使用完整路径，或确保 `$HOME\.local\bin` 已加入 PATH 环境变量。

---

## Authentication / 认证

**First-time users must authenticate:** / **首次使用需认证：**

```
& "$HOME\.local\bin\dws.exe" auth login
```

This opens a browser for QR code login. Credentials persist for 30 days.
此命令会打开浏览器，引导扫码登录钉钉。凭证有效期 30 天。

**Re-authenticate when expired:** / **凭证过期后重新认证：**

```
& "$HOME\.local\bin\dws.exe" auth login
```

---

## Common Commands / 常用命令

| Scenario 场景 | Command 命令 |
:|----------|---------|
| List todos / 查看待办 | `dws todo task list` |
| Create todo / 创建待办 | `dws todo task create --title "Report" --deadline 2026-04-15` |
| List calendar / 查看日历 | `dws calendar event list` |
| Send group message / 发群消息 | `dws chat bot send-by-group --group-id <ID> --content "Message"` |
| List reports / 查看日报周报 | `dws report inbox list` |
| Search contact / 搜索联系人 | `dws contact user search --keyword "Name"` |
| List AI tables / 查看 AI 表格 | `dws aitable base list` |

See the `references/` directory for full documentation on all 12 DingTalk products.
查看 `references/` 目录获取全部 12 个钉钉产品的详细文档。

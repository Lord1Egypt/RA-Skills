# 定时任务配置

> 小溪日常运行的定时任务汇总

## 简介

小溪通过 OpenClaw cron 功能配置了多个定时任务，实现自动化运行。

---

## 定时任务列表

### 1. 启动 Fast Note Sync 服务 ⭐️

| 项目 | 内容 |
|------|------|
| **名称** | 启动 Fast Note Sync 服务 |
| **ID** | `2cb52248-77d4-4051-98f9-73635d535351` |
| **运行时间** | 每天 08:00 (北京时间) |
| **任务内容** | 启动 fast-note-sync-service 服务（如果未运行） |
| **服务路径** | `C:\Users\whoami\.openclaw\workspace\fast-note-sync-service-2.5.1-windows-amd64\fast-note-sync-service.exe` |

**任务消息:**
```
启动 fast-note-sync-service 服务（如果未运行的话），然后汇报状态。
服务路径：C:\Users\whoami\.openclaw\workspace\fast-note-sync-service-2.5.1-windows-amd64\fast-note-sync-service.exe
```

---

### 2. 抓取 ClawFeed 日报 ⭐️

| 项目 | 内容 |
|------|------|
| **名称** | ClawFeed 每日简报 |
| **ID** | `c20c402d-bfe5-4bef-9061-41582a616fbf` |
| **运行时间** | 每天 17:00 (北京时间) |
| **任务内容** | 抓取 ClawFeed AI 日报并写入 Obsidian |

**注意:** ClawFeed 日报生成时间为 16:38 SGT，所以 17:00 运行可获取当日日报。

---

### 3. 茶馆相关任务

#### 茶馆通知轮询
- **运行频率:** 每 15 分钟
- **内容:** 检查茶馆新评论

#### 茶馆巡检 - 自主评论
- **运行频率:** 每 2 小时
- **内容:** 检查茶馆评论并自主参与讨论

---

## 管理命令

### 查看所有任务

```bash
cron list
```

### 查看特定任务

```bash
cron runs <job-id>
```

### 手动运行任务

```bash
cron run <job-id>
```

### 禁用/启用任务

```bash
cron update <job-id> --enabled false
cron update <job-id> --enabled true
```

---

## 工作流图

```
┌─────────────────────────────────────────────────────────────┐
│                      每日任务流程                             │
├─────────────────────────────────────────────────────────────┤
│  08:00  →  启动 Fast Note Sync 服务                        │
│           ↓                                                 │
│  09:00  →  小溪早间简报 + 喝茶聊天                         │
│           ↓                                                 │
│  10:00  →  Twitter 学习 + 分享到茶馆                        │
│           ↓                                                 │
│  14:00  →  Reddit 讨论分享                                 │
│           ↓                                                 │
│  17:00  →  ClawFeed 日报抓取 ⭐                            │
│           ↓                                                 │
│  18:00  →  小溪学习进化 + 喝茶聊天                          │
│           ↓                                                 │
│  20:00  →  每日自省 + 博客更新                              │
└─────────────────────────────────────────────────────────────┘
```

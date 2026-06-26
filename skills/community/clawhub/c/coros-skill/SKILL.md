---
name: "🏃 coros"
description: |
  COROS 高驰跑步数据获取（跑步专项）：
  - 自动登录 COROS 账号（支持 Token/Cookie 缓存）
  - 获取 Dashboard（训练状态、负荷分析、最近运动）
  - 获取活动列表与活动详情（含分圈、天气、训练效果）
  - 获取训练日程与训练目标汇总
  触发词示例：
  - "查看高驰跑步数据"
  - "我的跑步记录"
  - "高驰运动分析"
  - "今天跑步了吗"
  - "帮我看最近一次跑步详情"
  - "给我做个跑步复盘"
---

# COROS 高驰跑步数据获取 Skill

基于 COROS API 的跑步数据读取与展示工具，面向日常训练复盘。

## 使用范围

- 当前环境仅使用 `coros` 这个运动 Skill。
- 运动数据相关需求统一走本 Skill（高驰/COROS 跑步数据）。

## 功能概览

### 1. 智能登录
- 支持 `account + p1 + p2` 登录
- 支持 Token/Cookie 缓存，减少重复登录
- 自动保存和恢复登录状态

### 2. Dashboard 数据
- 训练状态：短期负荷(ATI)、长期负荷(CTI)、负荷比
- 最近运动记录
- 心率数据统计
- 运动类型统计
- 本周训练汇总

### 3. 活动列表
- 完整的跑步历史记录
- 显示：日期、名称、距离、时长、配速、心率、训练负荷(TL)
- 支持分页查询

### 4. 活动详情
- 通过 `activity/detail/query` 获取单次活动完整详情
- 展示模块：计圈数据、天气、概要数据、训练效果、运动感受
- 时间字段统一按 `HH:MM:SS` 展示，便于和网页详情页对齐
- 当前默认展示“活动列表第一页第一条”的详情（通常是最近一次）

### 5. 训练日程
- 训练日程查询
- 训练目标汇总
- 支持训练日程新增/更新/删除（`training/schedule/update`）
- 内置安全模式：默认仅预览，确认后可开启真实写入

## 运行方式

### OpenClaw 对话触发

示例（可直接复制）：
- `查看我的高驰跑步数据`
- `我的跑步记录`
- `高驰运动分析`
- `最近跑步怎么样`
- `今天跑步了吗`
- `看最近一次跑步详情`
- `帮我复盘今天这次跑步`

### 命令行运行

```bash
python3 main.py
```

## 配置文件

在 `config.json` 中配置账号与登录上下文：

```json
{
  "coros": {
    "account": "your_email@163.com",
    "p1": "$2b$10$xxx",
    "p2": "$2b$10$xxx"
  },
  "cookie": "_c_WBKFRo=xxx; _nb_ioWEgULi=",
  "demo_mode": false
}
```

发布到 clawhub.ai 时：
- 使用 `.clawhubignore` 排除 `config.json`、`api.md`、`.claude/`
- 将 `config.example.json` 作为公开示例配置
- 本地仍保留 `config.json` 以保证日常运行不受影响

## API 端点

| 功能 | API |
|------|-----|
| 登录 | POST /account/login |
| Dashboard详情 | GET /dashboard/detail/query |
| Dashboard汇总 | GET /dashboard/query |
| 周期纪录 | GET /dashboard/queryCycleRecord |
| 活动列表 | GET /activity/query |
| 活动详情 | POST /activity/detail/query |
| 训练日程 | GET /training/schedule/query |
| 日程汇总 | GET /training/schedule/querysum |
| 估算训练 | POST /training/program/estimate |
| 计算训练 | POST /training/program/calculate |
| 新增/更新/删除日程 | POST /training/schedule/update |
| 训练计划列表 | GET /training/program/list |

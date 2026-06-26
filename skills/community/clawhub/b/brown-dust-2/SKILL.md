---
name: brown-dust-2
description: "Brown Dust 2 全自动工具 — 每日/每周签到 + 活动出席签到 + 兑换码全自动兑换。触发词：BD2、棕色尘埃、brown dust、签到、兑换码、redeem。"
version: 1.1.0
---

# Brown Dust 2 Automation

棕色尘埃2 全自动签到 + 兑换码兑换。

## 触发规则

| 模式 | 示例 |
|------|------|
| 包含 `BD2` / `棕色尘埃` / `brown dust` | "BD2签到", "棕色尘埃兑换码" |
| 包含 `签到` + 游戏相关 | "帮我BD2签到", "BD2每日签到" |
| 包含 `兑换码` / `redeem` / `gift code` | "BD2兑换码", "redeem BD2 codes" |

## 三大功能

### 功能 1 — Web Shop 签到（纯 API）

每日签到 + 每周签到 + 活动出席，一条命令搞定。

```bash
# 执行全部签到
python3 {baseDir}/scripts/signin.py

# 查看活动信息
python3 {baseDir}/scripts/signin.py --event-info

# 仅每日签到
python3 {baseDir}/scripts/signin.py --daily-only
```

### 功能 2 — 兑换码自动兑换（纯 API）

自动从 BD2Pulse 抓取最新兑换码 → 调用官方 API 一键兑换。

```bash
# 自动抓取 + 全部兑换
python3 {baseDir}/scripts/redeem.py

# 只看有哪些码
python3 {baseDir}/scripts/redeem.py --list
```

### 功能 3 — 全套自动化

先签到再兑换码，一次跑完。

## 前置要求

| 功能 | 需要什么 | 如何获取 |
|------|---------|---------|
| 签到 | Web Shop accessToken | 浏览器登录后提取（详见 persona.md） |
| 兑换码 | 游戏内昵称 | `--save-nickname "昵称"` |

## Token 设置（首次 / 过期时）

> **Agent 应通过浏览器工具自动提取 Token：**
>
> 1. 用 browser 工具打开 `https://webshop.browndust2.global/CT/`
> 2. 等待页面加载 + 用户登录
> 3. 用 evaluate 执行 JS 提取 token：
>    ```js
>    JSON.parse(localStorage.getItem("session-storage")).state.session.accessToken
>    ```
> 4. 保存 token：`python3 signin.py --save-token "{token}"`
>
> 如果自动提取失败，引导用户手动操作：
> F12 → Console → 粘贴上述 JS → 把结果告诉 Agent

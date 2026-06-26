---
name: boss-cli
description: BOSS 直聘 CLI — 用于查询 BOSS 直聘职位、查看推荐和管理已投递记录。仅做查询使用，不做任何投递或聊天操作。by Barry
author: Barry
version: "0.3.6"
tags:
  - boss
  - zhipin
  - job-search
  - recruitment
---

# boss-cli — BOSS 直聘职位查询工具

**by Barry** | 仅做职位查询，不涉及投递/打招呼/聊天

---

## 功能范围

✅ **可用命令（只读查询）：**
- `boss search` — 搜索职位
- `boss recommend` — 个性化推荐
- `boss show` — 查看搜索结果详情
- `boss detail` — 查看指定职位详情
- `boss export` — 导出职位列表
- `boss cities` — 支持的城市列表
- `boss me` — 查看本人信息
- `boss applied` — 查看已投递记录
- `boss status` — 检查登录状态
- `boss login` / `boss logout` — 登录/退出

❌ **不使用的命令（不开放）：**
- `boss greet` — 打招呼
- `boss batch-greet` — 批量打招呼
- `boss chat` — 与 Boss 聊天

---

## 安装

```bash
uv tool install kabi-boss-cli
# 或
pipx install kabi-boss-cli
# 或
pip install kabi-boss-cli --user
```

**Python 要求：** >= 3.10

---

## 登录认证

```bash
# 方式1：自动从浏览器提取 cookie（推荐）
boss login

# 方式2：指定浏览器
boss login --cookie-source chrome

# 方式3：扫码登录
boss login --qrcode

# 验证登录状态
boss status
boss me --json
```

**Cookie 存储位置：**
- macOS / Linux：`~/.config/boss-cli/credential.json`
- Windows：`%USERPROFILE%\.config\boss-cli\credential.json`

**Cookie 有效期：** 约 7 天，过期后 `boss login` 自动刷新。

---

## 搜索命令

```bash
# 基础搜索
boss search "golang" --city 杭州 --salary 20-30K --json

# 查看推荐
boss recommend --json

# 查看已投递
boss applied

# 导出 CSV
boss export "Python" -n 50 -o jobs.csv

# 支持的城市
boss cities
```

## 搜索过滤参数

| 参数 | 示例值 |
|------|--------|
| `--city` | 北京、上海、杭州、深圳 |
| `--salary` | 3-5K、5-10K、10-15K、15-20K、20-30K、30-50K、50K以上 |
| `--exp` | 不限、1-3年、3-5年、5-10年 |
| `--degree` | 不限、大专、本科、硕士 |
| `--industry` | 互联网、人工智能、金融 |
| `--scale` | 0-20人、100-499人、1000-9999人 |
| `--stage` | 未融资、A轮、B轮、已上市 |
| `--job-type` | 全职、实习 |

---

## 登录状态检测

每次执行搜索前，建议先检测登录状态：

```bash
boss status --json 2>/dev/null | grep -q '"authenticated": true' && echo "AUTH_OK" || echo "AUTH_NEEDED"
```

未登录时，输出 `AUTH_NEEDED`，然后按上方登录步骤引导。

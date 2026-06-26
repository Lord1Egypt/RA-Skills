---
name: clawhub-stats-tracker
description: |
  查看 ClawHub 上已发布 Skill 的运营数据（Stars、Downloads、Installs、版本号、发布时间）。
  从 ~/.clawhub/tracked-skills.json 读取跟踪列表，通过 clawhub inspect --json 获取实时数据，
  支持单个查询、批量查询和按系列筛选。无需登录 ClawHub，inspect 接口公开可用。
  触发词：clawhub 数据、skill 数据、发布数据、installs、downloads、skill stats、
  查看 skill 安装量、clawhub stats、skill 运营数据。
  不适用于：发布 Skill（使用 clawhub publish）、搜索新 Skill（使用 clawhub search）、
  安装 Skill（使用 clawhub install）。
metadata:
  author: eamanc
  version: "1.0.0"
---

# ClawHub Stats Tracker

查看已发布到 ClawHub 的 Skill 运营数据。

## 快速开始

```
"查看我的 clawhub skill 数据"
"horoscope-daily 的安装量是多少"
"所有 fortune-telling 系列的数据"
```

## 工作流程

### Step 1: 确定查询范围

| 用户意图 | 操作 |
|---------|------|
| 查看所有跟踪的 Skill | 运行 `bash scripts/fetch-stats.sh` |
| 查看单个 Skill | 执行 `npx clawhub@latest inspect <slug> --json --no-input` |
| 查看某系列 | 从配置文件中筛选匹配的 slug，逐个 inspect |

### Step 2: 获取数据

**批量查询（推荐）：**

```bash
bash scripts/fetch-stats.sh
```

脚本从 `~/.clawhub/tracked-skills.json` 读取 slug 列表，逐个调用 `npx clawhub@latest inspect --json`，输出表格。

**单个查询：**

```bash
npx clawhub@latest inspect <slug> --json --no-input
```

返回 JSON 结构：

```json
{
  "skill": {
    "stats": {
      "stars": 0,
      "downloads": 42,
      "installsCurrent": 0,
      "installsAllTime": 0,
      "comments": 0,
      "versions": 5
    },
    "createdAt": 1773831137632,
    "updatedAt": 1774186907119
  },
  "latestVersion": {
    "version": "2.2.0",
    "createdAt": 1774186800664,
    "changelog": "..."
  }
}
```

时间戳为毫秒级 Unix 时间，需除以 1000 转换。

### Step 3: 输出格式

**批量表格（脚本默认输出）：**

```
SLUG                            STARS  DOWNLOADS CURRENT_INSTALLS ALLTIME_INSTALLS  VERSION  FIRST_PUBLISHED    LATEST_PUBLISHED   NOTE
horoscope-daily                     0         42                0                0    2.2.0  2026-03-18 18:52   2026-03-22 21:40   星座运势 EN/ZH
life-query                          1        116                0                0    2.0.0  2026-03-16 20:12   2026-03-21 11:02   生活查询助手
```

**单 Skill 详情（用户查单个时）：**

```
📊 horoscope-daily (v2.2.0)
├── ⭐ Stars: 0
├── 📥 Downloads: 42
├── 📦 Current Installs: 0
├── 📊 All-time Installs: 0
├── 💬 Comments: 0
├── 📅 First Published: 2026-03-18 18:52
├── 📅 Latest Version: 2026-03-22 21:40
└── 📝 Changelog: v2.2.0: Add Language & Localization...
```

## 配置文件

路径：`~/.clawhub/tracked-skills.json`

```json
{
  "skills": [
    { "slug": "fortune-hub", "note": "运势测算统一入口" },
    { "slug": "horoscope-daily", "note": "星座运势" }
  ]
}
```

- `slug`：ClawHub 上的 Skill slug（必填）
- `note`：备注说明（可选，仅展示用）

**添加新 Skill**：在 `skills` 数组中追加一条即可。发布新 skill 后记得同步更新。

## 已知限制

- ClawHub CLI 不支持按用户（owner）查询所有 skill，只能通过配置文件手动维护列表
- Downloads 和 Installs 指标有已知 bug（[openclaw/clawhub#156](https://github.com/openclaw/clawhub/issues/156)），installs 可能不计数
- inspect 接口无需登录，公开可用；publish/delete 等写操作才需要认证

## 错误处理

| 场景 | 处理 |
|------|------|
| 配置文件不存在 | 提示创建 `~/.clawhub/tracked-skills.json`，给出格式示例 |
| slug 不存在 | 显示"获取失败"，继续处理其他 slug |
| clawhub CLI 未安装 | `npx clawhub@latest` 会自动下载，无需手动安装 |
| 网络错误 | 显示失败的 slug，其余正常输出 |

## 原子化设计

本 Skill 仅负责「ClawHub Skill 运营数据查看」这一个原子化能力。不包含 Skill 发布、安装、搜索等功能，这些请直接使用 `clawhub` CLI 对应命令。

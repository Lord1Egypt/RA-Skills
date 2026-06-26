# COROS 高驰跑步数据 Skill

面向 OpenClaw 的 COROS（高驰）跑步数据查询与复盘 Skill。  
支持训练总览、活动列表、活动详情（分圈/天气/训练效果）、训练日程与目标汇总。

> 当前仓库仅使用 `coros` 作为运动类 Skill。

---

## 功能特性

- 自动登录 COROS 账号（支持 Token/Cookie 缓存）
- Dashboard 总览（ATI/CTI/负荷比、最近运动、本周汇总）
- 活动列表（日期、名称、距离、时长、配速、心率、训练负荷）
- 活动详情（分圈数据、天气、概要、训练效果、运动感受）
- 训练日程与目标汇总

---

## 文件结构

```text
coros/
├── main.py
├── skill.yaml
├── SKILL.md
├── config.json
└── readme.md
```

---

## 环境要求

- Python `3.8+`
- 可访问 COROS API 的网络环境

---

## 安装与使用

### 1) 准备配置

编辑 `config.json`：

```json
{
  "coros": {
    "account": "your_email@example.com",
    "p1": "$2b$10$...",
    "p2": "$2b$10$..."
  },
  "cookie": "_c_WBKFRo=...; _nb_ioWEgULi=",
  "demo_mode": false
}
```

### 2) 命令行验证

```bash
python3 main.py
```

### 3) 对话触发示例

- 查看我的高驰跑步数据
- 最近一次跑步详情
- 帮我做个跑步复盘
- 本周跑量多少
- 训练负荷怎么样

---

## 主要接口

- `POST /account/login`
- `GET /dashboard/detail/query`
- `GET /dashboard/query`
- `GET /dashboard/queryCycleRecord`
- `GET /activity/query`
- `POST /activity/detail/query`
- `GET /training/schedule/query`
- `GET /training/schedule/querysum`
- `POST /training/program/estimate`
- `POST /training/program/calculate`
- `POST /training/schedule/update`
- `GET /training/program/list`

---

## 日程新增/更新/删除（安全模式）

默认仅预览，不会写入。可在 `config.json` 增加：

```json
{
  "schedule_write": {
    "action": "add",
    "date": "20260322",
    "name": "训练",
    "duration_seconds": 3900,
    "hr_low": 167,
    "hr_high": 175,
    "intensity_percent_low": 91000,
    "intensity_percent_high": 95000,
    "id_in_plan": 4,
    "auto_apply": false
  }
}
```

- `action`: `add` / `update` / `delete`
- `auto_apply=false`: 只预览估算结果
- `auto_apply=true`: 真正写入并回查验证
- 删除/更新建议补充目标定位字段之一：`target_id_in_plan`、`target_plan_program_id`、`target_name`（支持包含匹配，如 `5km`）、`target_distance_km`

删除示例（对应网页抓包中的 `versionObjects.status=3`）：

```json
{
  "schedule_write": {
    "action": "delete",
    "date": "20260322",
    "id": "4",
    "plan_program_id": "4",
    "plan_id": "452075943119470593",
    "status": 3,
    "auto_apply": false
  }
}
```

---

## 常见问题

### 1) 登录失败 / 403

- 检查 `cookie/p1/p2` 是否过期
- 重新抓取 `account/login` 请求参数

### 2) 只显示演示数据

- 检查 `demo_mode` 是否为 `true`
- 检查 `account/p1/p2/cookie` 是否完整

---

## 上传 clawhub.io 前检查清单

- [ ] `skill.yaml` 的 `name/version/entry/language` 正确
- [ ] `trigger_keywords` 覆盖核心意图
- [ ] `main.py` 可运行（真实/演示模式）
- [ ] 文档已脱敏（账号、cookie、token）

### 推荐上传方式（不影响本地运行）

- 保留你本地 `config.json`（含账号密码）用于本地运行，不要改动
- 上传时依赖 `.clawhubignore` 自动排除敏感文件：
  - `config.json`
  - `api.md`
  - `.claude/`
- 对外示例配置使用 `config.example.json`
- 上传前可自查：`config.json` 不在上传清单内即可

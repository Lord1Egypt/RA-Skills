---
name: bidding-tracker
description: 军政采招投标商机管理专用工具。负责项目登记/标书采购/封标/开标/结果录入/中标统计/胜算评估，不处理合同履约、发票、报销或其他非招投标事务。
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["bidding-tracker"]},"install":"pip install -e {baseDir}"}}
---

# bidding-tracker 使用指南

> 本文档面向 LLM，说明如何通过 `bidding-tracker` CLI 管理招投标项目全生命周期。
>
> **适用范围**：军队采购（军采）和政府采购（政采）的投标商机跟踪，包括项目登记、标书购买、封标投递、开标结果、中标统计、招标文件胜算评估。
> **不适用**：合同管理、发票报销、项目交付、非招投标的采购咨询。

---

## 首次初始化

系统首次使用时，必须先注册总监账号，否则所有非 init 命令均会报错。

```bash
bidding-tracker init --name "王总监"
```

执行后返回 `{"status": "ok"}` 即可继续使用其他命令。

---

## 核心操作流程

### 1. 注册项目

收到招标公告时，提取关键字段并调用 register。`--json` 传入结构化字段，`--manager-name` 指定负责人姓名。

```bash
bidding-tracker register \
  --json '{"project_name":"XX系统采购","budget":500000,"bid_opening_time":"2026-05-10T14:00:00","doc_purchase_deadline":"2026-04-20T17:00:00"}' \
  --manager-name "张经理" \
  --travel-days 2
```

**`--json` 支持的字段（均为可选，`*` 为强烈建议填写）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `project_name` * | string | 项目名称 |
| `bid_opening_time` * | ISO8601 | 开标时间（用于推算封标时间） |
| `doc_purchase_deadline` * | ISO8601 | 标书购买截止时间 |
| `budget` | number | 预算（元） |
| `procurer` | string | 采购方名称 |
| `bid_agency` | string | 招标代理机构 |
| `manager_contact` | string | 负责人联系方式 |
| `registration_deadline` | ISO8601 | 报名截止时间 |
| `registration_location` | string | 报名地点 |
| `doc_purchase_location` | string | 标书购买地点 |
| `doc_purchase_price` | number | 标书售价（0 表示免费） |
| `doc_required_materials` | string\|array | 报名所需材料 |
| `bid_opening_location` | string | 开标地点 |

成功返回：
```json
{"project_id": 1, "project_no": "2026-001", "project_name": "...", "suggested_seal_time": "2026-05-08T14:00:00", "attachment_dir": "..."}
```

若有招标公告文件，追加 `--file /path/to/file.pdf`，文件将自动移入附件目录。

### 2. 查看项目列表

```bash
bidding-tracker status                          # 查看所有活跃项目
bidding-tracker status --keyword "关键词"       # 按项目名或编号搜索
bidding-tracker status --upcoming-days 7       # 查看7天内有关键节点的项目
```

### 3. 状态推进

根据用户反馈选择对应命令，关键字可以是项目名称片段或完整项目编号（如 `2026-001`）：

| 用户场景 | 命令 |
|----------|------|
| 已购买标书 | `bidding-tracker purchased "项目名"` |
| 已封标/已寄出标书 | `bidding-tracker seal "项目名"` |
| 项目废标、放弃投标 | `bidding-tracker cancel "项目名"` |

### 4. 录入开标结果

开标后，根据结果录入。项目须处于 `opened` 状态（由 `seal` 推进而来）。

```bash
# 中标
bidding-tracker result "项目名" --won --our-price 980000 --winning-price 980000

# 未中标（尽量提供完整信息）
bidding-tracker result "项目名" --lost --our-price 1050000 --winning-price 980000 --winner "某某公司" --notes "报价偏高"
```

---

## 状态机约束

以下为合法流转路径，LLM 不可跳步操作：

```
registered → doc_pending → doc_purchased → preparing → sealed → opened → won
                                                                        → lost
任意非终态 → cancelled（终态，不可逆）
```

**实用映射：**
- `purchased` 命令 → 状态推进至 `doc_purchased`
- `seal` 命令 → 状态推进至 `sealed`（同时记录实际封标时间）
- `result` 命令 → 仅在 `opened` 状态可执行，推进至 `won` 或 `lost`

> `opened` 状态需通过 `update_project` 直接写库或由提醒 Cron 触发，`result` 命令本身不推进 `sealed → opened`。

---

## 团队管理

```bash
bidding-tracker users                                          # 查看所有成员
bidding-tracker users --role manager                          # 仅看负责人
bidding-tracker adduser --new-user-id wx_uid --name "李经理" --contact "138xxxx"
```

> `adduser` 仅总监可执行。

---

## 统计分析

```bash
bidding-tracker stats                         # 全局汇总（胜率、平均预算等）
bidding-tracker stats --by-month             # 按月趋势
bidding-tracker stats --by-manager           # 按负责人分组
bidding-tracker stats --by-month --period 2026-Q1   # 限定季度范围
bidding-tracker stats --by-month --period 2026-03   # 限定月份范围
```

> `--by-manager` 与 `--by-month` 不可同时使用。

---

## 胜算评估

### evaluate - 解析招标文件

读取 PDF/Word/TXT 招标文件，提取文本并组装分析 prompt，供 LLM 进行深度博弈评估。

```bash
bidding-tracker evaluate --file /path/to/tender.pdf
bidding-tracker evaluate --file /path/to/tender.docx
```

成功返回：
```json
{
  "status": "ok",
  "message": "招标文件《xxx.pdf》已解析（12345 字），请按分析框架进行深度博弈评估",
  "data": {
    "analysis_prompt": "...",
    "profiles": "...",
    "document_text": "...",
    "file_name": "xxx.pdf"
  }
}
```

LLM 收到响应后，应将 `analysis_prompt` 作为分析框架指令，`profiles` 作为投标主体战略资产库上下文，`document_text` 作为待分析的招标文件原文，三者结合输出深度博弈报告。

> **自定义主体档案：** `profiles` 字段内容优先读取 `~/.config/bidding-tracker/profiles.md`（如存在），否则使用包内默认。用户可编辑该文件更新公司资质、人员与业绩信息，无需修改代码。

### bind-eval - 绑定胜算评估结果

将评估胜率（0-1）和报告摘要绑定到指定项目，记录评估时间。

```bash
bidding-tracker bind-eval "项目名" --probability 0.75
bidding-tracker bind-eval "项目名" --probability 0.75 --report "技术优势明显，但缺乏CMMI认证"
bidding-tracker bind-eval "2026-001" --probability 0.4 --report "疑似定向标，建议陪跑"
```

`--probability` 取值范围 `0.0~1.0`，`--report` 为可选的预测报告摘要（建议不超过200字）。

---

## 输出格式约定

所有命令成功时，stdout 输出 JSON，exit code 为 0：

```json
{"status": "ok", "message": "...", "data": {...}}
```

失败时，stderr 输出 JSON，exit code 为 1：

```json
{"error": "具体错误原因", "code": 1}
```

遇到错误时，将 `error` 字段内容直接反馈给用户即可。

---

## 环境配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DB_PATH` | SQLite 数据库路径 | `{CWD}/data/bids.db` |
| `ATTACHMENTS_DIR` | 附件存储根目录 | `{DB_PATH同级}/attachments` |

加载优先级：进程环境变量 > `{CWD}/.env` > `~/.config/bidding-tracker/.env` > 默认值。

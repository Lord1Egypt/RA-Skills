---
name: db-bridge
description: Database table bridging skill. Parses table configurations from table.json and executes SELECT / INSERT / UPDATE / DELETE operations via sql-linker. All CRUD operations are handled by sql-linker.
---

# db-bridge — 表格配置桥接器 / Table Configuration Bridge

---

## 概述 / Overview

（中文）db-bridge 是表格配置的**解析层/桥接层**，读取 `table.json` 获取表格元数据，调用 **sql-linker** 执行 SELECT / INSERT / UPDATE / DELETE 等数据库操作，本身不直接连接数据库，确保字段白名单安全可控。

（English）db-bridge is the **parsing/bridging layer** for table configurations. It reads `table.json` for table metadata, then calls **sql-linker** to execute SELECT / INSERT / UPDATE / DELETE operations — without connecting to the database directly, ensuring field whitelist security and control.

## 工作流程 / Workflow

（中文）用户请求 → 读取 table.json → 解析表格名/字段 → 调用 sql-linker → 返回结果

（English）Request → Read table.json → Parse table/fields → Call sql-linker → Return result

---

## 高效工作流 / Efficient Workflow

> **（中文）经验教训：从本次10分钟→1分钟的优化中总结而来。新设备首次使用时请严格遵循。**
> **（English）Lesson learned: derived from a 10min→1min optimization. Follow on any new device.**

### 标准流程（三步曲）/ Standard Three-Step Flow

**Step 1 — 查现场，不脑补 / Inspect first, don't guess**
```bash
# （中文）查询当前表结构（已知命令直接跑，不要先读文档）
# （English）Query current table structure (run known commands directly, don't read docs first)
python scripts/sql_linker.py query "SHOW TABLES"          # （中文）查看有哪些表 / （English）List tables
python scripts/sql_linker.py query "DESC <table_name>"     # （中文）查看表字段 / （English）View table fields
python scripts/sql_linker.py query "SELECT * FROM <table> LIMIT 3"  # （中文）看现有数据 / （English）View existing data
```

**Step 2 — 直接执行（含真实身份上下文）/ Execute directly with real identity**
```bash
# （中文）INSERT / UPDATE / DELETE — 用双引号包裹 JSON，PowerShell 不丢转义
# （中文）必须传入 --user-label 和 --session-id，确保审计日志真实可溯源
# （English）INSERT / UPDATE / DELETE — wrap JSON in double quotes, PowerShell won't lose escapes
# （English）Always pass --user-label and --session-id to ensure audit log traceability

# （中文）从 OpenClaw 消息 metadata 获取：label → --user-label，id → --session-id
# （English）From OpenClaw message metadata: label → --user-label, id → --session-id
python scripts/sql_linker.py --user-label "<label>" --session-id "<session_id>" \
  insert "<table>" "{\"field\":\"value\"}"

python scripts/sql_linker.py --user-label "<label>" --session-id "<session_id>" \
  update "<table>" "{\"field\":\"new_value\"}" "<where>"

python scripts/sql_linker.py --user-label "<label>" --session-id "<session_id>" \
  delete "<table>" "<where>"
```

**Step 3 — 确认结果 / Confirm result**
```bash
python scripts/sql_linker.py query "SELECT * FROM <table>"  # （中文）回查验证 / （English）Verify result
```

### 避免的错误 / Mistakes to Avoid

| （中文）错误做法 | （中文）正确做法 | （中文）原因 | / English Wrong | / English Correct | / English Reason |
|----------|----------|------|----------|----------|------|
| 先完整阅读 SKILL.md 再行动 | 已知命令直接跑，有报错再查文档 | 节省90%时间 | Read entire SKILL.md first | Run known commands directly, check docs on error | Saves 90% time |
| 写临时 .py 文件来调试 | 用 CLI 一次完成 | 减少中间环节 | Write temp .py files to debug | Use CLI to complete in one go | Reduce intermediate steps |
| 逐个试错路径/导入方式 | 查现场后直接正确执行 | 一次做对 | Trial-and-error paths/imports | Inspect first, then execute correctly | Do it right the first time |
| 插入失败后从头重读文档 | 读报错对应的小节 | 按需查档 | Re-read entire doc after insert failure | Read the section matching the error | Read docs on-demand |
| 审计日志 session 硬编码 | 通过 --session-id 传入真实值 | 审计可溯源 | Hardcode session in audit | Pass real value via --session-id | Audit traceability |

### 核心原则 / Core Principle

（中文）**CLI 优先，查现场，按需读文档。**

（English）**CLI-first, inspect before acting, read docs on-demand.**

---

## 身份上下文注入 / Identity Context Injection

> ⚠️ **（中文）重要：审计日志中的 ip_address 和 session_id 必须真实，否则失去溯源意义。**\n> ⚠️ **IMPORTANT: ip_address and session_id in audit logs must be real — otherwise audit loses its value.**

**方式一：CLI 参数（推荐）/ Option 1: CLI flags (recommended)**
```bash
# （中文）从 OpenClaw 消息 metadata 提取，传入 CLI
# （English）Extract from OpenClaw message metadata, pass to CLI
--user-label   # → metadata.label
--session-id   # → OpenClaw runtime session key
```
```bash
# （中文）完整示例
# （English）Full example
python scripts/sql_linker.py \
  --user-label "openclaw-control-ui" \
  --session-id "agent:hr:main" \
  insert "supplier_table" "{\"supplier_name\":\"华为\"}"
```

**方式二：环境变量（备选）/ Option 2: Environment variables (fallback)**
```bash
# （中文）sql-linker 的 set_user_context_auto() 会读取这些环境变量
# （English）sql-linker's set_user_context_auto() reads these env vars
export OPENCLAW_LABEL="openclaw-control-ui"
export OPENCLAW_SESSION="agent:hr:main"
python scripts/sql_linker.py insert "supplier_table" "{\"supplier_name\":\"华为\"}"
```

> **（中文）**OpenClaw 消息 metadata 示例：`{"label": "openclaw-control-ui", "id": "openclaw-control-ui"}`\n> **（English）**OpenClaw message metadata example: `{"label": "openclaw-control-ui", "id": "openclaw-control-ui"}`

---

## table.json 结构 / table.json Structure

```json
{
  "tables": [
    {
      "table_name": "supplier_table",
      "comment": "供应商信息表",
      "fields": [
        { "name": "id",           "type": "BIGINT",      "pk": true,  "auto": true  },
        { "name": "supplier_code","type": "VARCHAR(32)",  "pk": false, "auto": false },
        { "name": "supplier_name","type": "VARCHAR(128)", "pk": false, "auto": false },
        { "name": "short_name",   "type": "VARCHAR(64)",  "pk": false, "auto": false },
        { "name": "supplier_level","type": "VARCHAR(16)", "pk": false, "auto": false },
        { "name": "contact_person","type": "VARCHAR(64)", "pk": false, "auto": false },
        { "name": "contact_phone", "type": "VARCHAR(32)", "pk": false, "auto": false },
        { "name": "contact_email", "type": "VARCHAR(128)","pk": false, "auto": false },
        { "name": "status",        "type": "VARCHAR(16)", "pk": false, "auto": false },
        { "name": "created_at",   "type": "DATETIME",    "pk": false, "auto": false },
        { "name": "updated_at",   "type": "DATETIME",    "pk": false, "auto": false }
      ]
    }
  ]
}
```

---

## 字段类型说明 / Field Type Reference

| type 值 | 说明 | Description |
|---------|------|-------------|
| `BIGINT` | 主键/自增ID | Primary key / auto-increment ID |
| `VARCHAR(n)` | 字符串，最大 n 字符 | String, max n chars |
| `TEXT` | 长文本 | Long text |
| `INT` | 整数 | Integer |
| `DECIMAL(m,n)` | 小数，m位总长，n位小数 | Decimal, m total digits, n decimals |
| `DATETIME` | 日期时间 | Date and time |
| `DATE` | 日期 | Date |
| `BOOL` | 布尔值 | Boolean |

---

## sql-linker 调用方式 / sql-linker Invocation

### 查询 SELECT

```python
linker.query("SELECT id, supplier_code, supplier_name FROM supplier_table WHERE status = %s", ("active",))
```

### 插入 INSERT

```python
data = {
    "supplier_code": "SUP001",
    "supplier_name": "示例供应商",
    "contact_person": "张三",
    "status": "active"
}
linker.insert("supplier_table", data)
```

### 更新 UPDATE

```python
linker.update(
    "supplier_table",
    {"supplier_name": "新名称", "updated_at": "2026-05-18 15:00:00"},
    "id = %s",
    (1,)
)
```

### 删除 DELETE

```python
linker.delete("supplier_table", "id = %s AND status = %s", (1, "inactive"))
```

---

## CLI 命令速查 / CLI Quick Reference

```bash
# （中文）查询
# （English）Query
python scripts/sql_linker.py query  "SELECT * FROM <table> LIMIT 10"
python scripts/sql_linker.py query  "SHOW TABLES"
python scripts/sql_linker.py query  "DESC <table_name>"

# （中文）插入（JSON 双引号包裹，附身份上下文）
# （English）Insert (JSON in double quotes, with identity context)
python scripts/sql_linker.py --user-label "<label>" --session-id "<session_id>" \
  insert "<table>" "{\"field\":\"value\",\"field2\":123}"

# （中文）更新
# （English）Update
python scripts/sql_linker.py --user-label "<label>" --session-id "<session_id>" \
  update "<table>" "{\"field\":\"new_value\"}" "<where_clause>"

# （中文）删除
# （English）Delete
python scripts/sql_linker.py --user-label "<label>" --session-id "<session_id>" \
  delete "<table>" "<where_clause>"
```

> **（中文）注意：** Windows PowerShell 下 JSON 参数必须用双引号，单引号会导致转义丢失。\n> **（English）Note:** On Windows PowerShell, JSON arguments MUST use double quotes — single quotes cause escape loss.

---

## 权限控制 / Access Control

| （中文）操作 | （中文）权限 | / Operation | / Permission |
|------|------|------------|------------|
| SELECT | 读 | Read | Read |
| INSERT | 写（需 admin 以上） | Write (admin+) | Write (admin+) |
| UPDATE | 写（需 admin 以上） | Write (admin+) | Write (admin+) |
| DELETE | 删（需 super admin） | Delete (super admin) | Delete (super admin) |

> **（中文）**具体权限由 sql-linker 的 `read_only` 配置和业务规则共同控制。\n> **（English）**Actual permissions governed by sql-linker's `read_only` config and business rules.

---

## 安全原则 / Security Principles

1. **（中文）字段白名单：** 只允许 `table.json` 中定义的字段才能写入\n   **（English）Field whitelist:** only fields defined in `table.json` are writable

2. **（中文）参数化查询：** 全部使用 `%s` + tuple 防止 SQL 注入\n   **（English）Parameterized queries:** always use `%s` + tuple to prevent SQL injection

3. **（中文）审计日志：** 由 sql-linker 自动记录操作人、IP、SQL 语句\n   **（English）Audit log:** sql-linker automatically records operator, IP, and SQL

4. **（中文）敏感字段脱敏：** 脱敏规则由 sql-linker 的 `mask_values` 配置控制\n   **（English）Sensitive field masking:** rules controlled by sql-linker's `mask_values` config

---

## 快速上手示例 / Quick Start Example

```bash
# （中文）1. 查看现有表 / （English）1. View existing tables
python scripts/sql_linker.py query "SHOW TABLES"

# （中文）2. 插入一条数据（带真实身份）
# （English）2. Insert a record (with real identity)
python scripts/sql_linker.py \
  --user-label "openclaw-control-ui" \
  --session-id "agent:hr:main" \
  insert "supplier_table" "{\"supplier_code\":\"HW001\",\"supplier_name\":\"华为技术有限公司\",\"short_name\":\"华为\",\"supplier_level\":\"A\",\"contact_person\":\"张明\",\"contact_phone\":\"13800138000\",\"contact_email\":\"zhangming@huawei.com\",\"status\":\"active\"}"

# （中文）3. 验证插入成功 / （English）3. Verify insert success
python scripts/sql_linker.py query "SELECT * FROM supplier_table"

# （中文）4. 更新数据 / （English）4. Update data
python scripts/sql_linker.py --user-label "openclaw-control-ui" --session-id "agent:hr:main" \
  update "supplier_table" "{\"status\":\"inactive\"}" "supplier_code = 'HW001'"

# （中文）5. 确认更新结果 / （English）5. Confirm update result
python scripts/sql_linker.py query "SELECT * FROM supplier_table WHERE supplier_code = 'HW001'"
```

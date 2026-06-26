# DeepTask 数据库表结构

## 设计原则

- 所有关系为**树状 1:N**（无需中间表），外键关联
- ID 格式：`类型 - 数字`（如 `DT-1`, `SE-1`），由系统自动生成
- 状态字段：使用 `CHECK` 约束确保合法值
- 时间字段：`DATETIME` 存储，`DEFAULT CURRENT_TIMESTAMP`

---

## 表结构

### 1. 项目表 (`projects`)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | TEXT PRIMARY KEY | 项目 ID（格式：`DT-数字`） | `DT-1` |
| name | TEXT NOT NULL | 项目名称 | `用户管理系统` |
| description | TEXT | 项目介绍 | `支持注册/登录/权限管理` |
| summary | TEXT | 项目摘要（功能特性） | `核心功能：RBAC 权限模型` |
| created_at | DATETIME | 创建时间 | `2026-04-07 21:29:04` |

### 2. 会话表 (`sessions`)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | TEXT PRIMARY KEY | 会话 ID（格式：`SE-数字`） | `SE-1` |
| project_id | TEXT NOT NULL | 外键，关联 `projects.id` | `DT-1` |
| summary | TEXT | 会话摘要（迭代信息） | `用户注册模块迭代` |
| content | TEXT | 会话内容（详细拆解） | `拆解为：注册表单、邮箱验证、密码策略` |
| created_at | DATETIME | 创建时间 | |
| updated_at | DATETIME | 最后更新时间 | |
| status | TEXT | 状态 | `review_pending` |

**状态枚举**: `pending`, `in_progress`, `completed`, `review_pending`

### 3. 子任务表 (`subtasks`)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | TEXT PRIMARY KEY | 子任务 ID（格式：`ST-数字`） | `ST-1` |
| session_id | TEXT NOT NULL | 外键，关联 `sessions.id` | `SE-1` |
| summary | TEXT | 子任务摘要 | `实现注册表单验证` |
| content | TEXT | 子任务内容 | `验证邮箱格式、密码强度` |
| created_at | DATETIME | 创建时间 | |
| updated_at | DATETIME | 最后更新时间 | |
| status | TEXT | 状态 | `completed` |

**状态枚举**: `pending`, `in_progress`, `completed`, `review_pending`

### 4. MUF 表 (`mufs`)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | TEXT PRIMARY KEY | MUF ID（格式：`MUF-数字`） | `MUF-1` |
| subtask_id | TEXT NOT NULL | 外键，关联 `subtasks.id` | `ST-1` |
| summary | TEXT | MUF 摘要 | `邮箱格式验证逻辑` |
| content | TEXT | MUF 内容（代码功能描述） | `正则：^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` |
| created_at | DATETIME | 创建时间 | |
| updated_at | DATETIME | 最后更新时间 | |
| status | TEXT | 状态 | `completed` |

**状态枚举**: `pending`, `in_progress`, `completed`, `failed`

### 5. 单元测试表 (`unit_tests`)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | TEXT PRIMARY KEY | UT ID（格式：`UT-数字`） | `UT-1` |
| muf_id | TEXT NOT NULL | 外键，关联 `mufs.id` | `MUF-1` |
| test_code | TEXT | 单元测试代码 | `def test_email_format(): ...` |
| status | TEXT | 状态 | `passed` |
| created_at | DATETIME | 创建时间 | |
| updated_at | DATETIME | 最后更新时间 | |

**状态枚举**: `pending`, `passed`, `failed`

### 6. 集成测试表 (`integration_tests`)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | TEXT PRIMARY KEY | IT ID（格式：`IT-数字`） | `IT-1` |
| subtask_id | TEXT NOT NULL | 外键，关联 `subtasks.id` | `ST-1` |
| test_code | TEXT | 集成测试代码 | `def test_registration_flow(): ...` |
| status | TEXT | 状态 | `pending` |
| created_at | DATETIME | 创建时间 | |
| updated_at | DATETIME | 最后更新时间 | |

**状态枚举**: `pending`, `passed`, `failed`

### 7. 人工审查记录表 (`review_records`)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | INTEGER PRIMARY KEY | 自增 ID | `1` |
| entity_type | TEXT NOT NULL | 实体类型：`session`/`subtask`/`muf` | `session` |
| entity_id | TEXT NOT NULL | 实体 ID（如 `SE-1`） | `SE-1` |
| reviewer | TEXT | 审查者 | `张三` |
| review_date | DATETIME | 审查时间 | |
| status | TEXT | 审查结果 | `approved` |
| comments | TEXT | 审查意见 | `通过，无需修改` |

**状态枚举**: `approved`, `rejected`

---

## 状态机流转

### 会话状态流转
```
pending → in_progress → review_pending → in_progress → completed
```

### MUF 状态流转
```
pending → in_progress → completed
                    ↓
                  failed (熔断)
```

---

## 索引

- `idx_sessions_project`: sessions(project_id)
- `idx_subtasks_session`: subtasks(session_id)
- `idx_mufs_subtask`: mufs(subtask_id)
- `idx_unit_tests_muf`: unit_tests(muf_id)
- `idx_integration_tests_subtask`: integration_tests(subtask_id)
- `idx_review_records_entity`: review_records(entity_type, entity_id)

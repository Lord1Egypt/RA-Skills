# DDL Analyzer — DDL/SQL 表结构分析器

> 适用于：data-prompt-coach 引导入口 L2+ 资料感知
> 角色：用户提交 DDL/SQL 后，分析表关系/字段类型/索引/业务口径并回填 5 要素

## 触发条件

用户在引导入口提交 CREATE TABLE 语句 / DDL / SQL 文件 / 字段清单，且场景属于：
- 场景 3（SQL 生成）— 用户提供表结构

## 分析流程

### Step 1: 表清单识别

```yaml
tables:
  - name: "users"
    alias: "用户表"
    columns_count: 5
    primary_key: "user_id"
  - name: "course_progress"
    alias: "课程学习记录表"
    columns_count: 7
    primary_key: "id"
  - name: "login_log"
    alias: "登录记录表"
    columns_count: 4
    primary_key: "id"
  - name: "orders"
    alias: "订单表"
    columns_count: 6
    primary_key: "order_id"
```

### Step 2: 字段详情分析（每张表）

```yaml
table: "users"
columns:
  - name: "user_id"
    type: "BIGINT"
    nullable: false
    is_primary_key: true
    comment: "用户ID"
  - name: "nickname"
    type: "VARCHAR(64)"
    nullable: true
    comment: "昵称"
  - name: "city"
    type: "VARCHAR(32)"
    nullable: true
    comment: "所在城市"
    business_meaning: "用户注册时填写的城市，可能不是当前居住地"
  - name: "register_time"
    type: "DATETIME"
    nullable: false
    comment: "注册时间"
  - name: "status"
    type: "TINYINT"
    nullable: false
    default: 1
    comment: "账号状态：1=正常,0=注销"
    enum_values:
      0: "注销"
      1: "正常"
```

### Step 3: 表关系分析

```yaml
relationships:
  - type: "one_to_many"
    from: "users.user_id"
    to: "course_progress.user_id"
    join_type: "LEFT JOIN"  # 推荐 JOIN 类型
    reason: "用户可能没有学习记录"
  - type: "one_to_many"
    from: "users.user_id"
    to: "login_log.user_id"
    join_type: "LEFT JOIN"
    reason: "用户可能从未登录"
  - type: "one_to_many"
    from: "users.user_id"
    to: "orders.user_id"
    join_type: "LEFT JOIN"
    reason: "用户可能没有订单"
```

### Step 4: 索引分析

```yaml
indexes:
  - table: "course_progress"
    name: "idx_user"
    columns: ["user_id"]
    useful_for: "按用户查询学习记录"
  - table: "course_progress"
    name: "idx_finish"
    columns: ["finish_time"]
    useful_for: "按完成时间筛选"
  - table: "login_log"
    name: "idx_user_time"
    columns: ["user_id", "login_time"]
    useful_for: "按用户+时间范围查询登录记录"
  - table: "orders"
    name: "idx_user"
    columns: ["user_id"]
    useful_for: "按用户查询订单"
```

### Step 5: 业务口径识别

```yaml
business_definitions:
  - concept: "活跃学员"
    definition: "❓ 需用户确认"
    related_fields: ["course_progress.status", "course_progress.finish_time", "login_log.login_time"]
    ambiguity: "活跃的定义需要用户明确（如：30天内完成≥3门+7天内登录）"
  - concept: "续费率"
    definition: "❓ 需用户确认"
    related_fields: ["orders.order_type", "orders.pay_status"]
    ambiguity: "续费率分子分母定义需明确（如：有续费订单的活跃学员/全部活跃学员）"
  - concept: "学习时长"
    definition: "❓ 需用户确认"
    related_fields: ["course_progress.study_minutes"]
    ambiguity: "是人均还是总和？是近30天还是全部？"
```

### Step 6: 回填 5 要素

```yaml
scope: "✅ 已知表结构：{N} 张表，{M} 个字段"
fields:
  - "✅ 字段清单已识别"
  - "⚠️ 业务口径未定义：活跃学员/续费率/学习时长"
processing_rules:
  - "✅ 表关系已识别：{K} 个关联"
  - "⚠️ JOIN 类型需确认（推荐 LEFT JOIN）"
  - "⚠️ 时间范围需确认（如近30天）"
output_format: "❓ 待确认（建议 MySQL 方言 + 注释）"
exception_handling:
  - "⚠️ 业务口径模糊，需用户确认"
  - "⚠️ NULL 值处理规则需确认"
```

## 回填后访谈策略

| 要素 | 资料分析前 | 资料分析后 | 第 1 轮访谈重点 |
|------|----------|----------|---------------|
| 范围 | ❓ | ✅ 已知表结构 | 跳过 |
| 字段 | ❓ | ✅ 清单已识别，⚠️口径未定义 | 问业务口径定义 |
| 处理规则 | ❓ | ✅ JOIN 已识别，⚠️时间范围 | 问时间范围 + 过滤条件 |
| 输出格式 | ❓ | ❓ | 问方言 + 输出要求 |
| 异常处理 | ❓ | ⚠️ NULL 处理 | 问 NULL 兜底 |

**3 轮访谈维度划分**：
- 第 1 轮：业务口径定义（活跃学员/续费率/学习时长等模糊概念）
- 第 2 轮：时间范围 + 过滤条件 + JOIN 确认
- 第 3 轮：输出要求 + NULL 处理 + 模糊口径假设列表

## SQL 审查专属关注点

基于 DDL 分析，预先标记 SQL 审查时必看的 4 点（与 M10 SQL 4 必看联动）：

```yaml
sql_review_focus:
  - point: "JOIN 类型"
    expected: "LEFT JOIN（基于表关系分析）"
    risk: "误用 INNER JOIN 会丢失无关联记录"
  - point: "时间边界"
    expected: "用户确认近30天/7天范围"
    risk: ">= 还是 >？含不含今天？"
  - point: "去重"
    expected: "COUNT(DISTINCT user_id)"
    risk: "多表 JOIN 后行数翻倍"
  - point: "业务口径"
    expected: "续费率分子分母明确定义"
    risk: "比率类指标最容易翻车"
```

## 与 SKILL.md 的接口

**入口点**：本文件"分析流程"段落
**出口点**：本文件"回填后访谈策略"末尾
**调用方**：SKILL.md Step A2 资料感知访谈
**依赖**：用户提交的 DDL/SQL/字段清单
**联动**：M10 SQL 4 必看（审查清单基于本分析器输出）

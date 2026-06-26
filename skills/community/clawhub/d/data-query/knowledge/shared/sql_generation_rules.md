# LLM SQL 生成安全规则

> 本文件定义了 LLM 生成 SQL 查询时的强制约束规则，所有生成的 SQL 必须遵守。
> 制定时间：2026-03-26
>
> ⚠️ **关于租户隔离的重要说明**：
> - **生产代码**：租户ID由后端通过 `getLoginUserVo().getTenantId()` 自动注入，生成的 SQL **不包含** `AND TENANT_ID = ?`
> - **verifySql.js（开发调试工具）**：需要 `--tenant-id` CLI 参数才能连接本地 MySQL 执行验证，这是工具自身执行所需，**不是生成的 SQL 的一部分**
> - 本文件中的 SQL 示例（含 TENANT_ID = ?）仅用于说明**租户隔离逻辑**，实际交付的 SQL 不应包含此条件

---

## 一、铁律（绝对禁止违反）

### 1.1 租户隔离（最高优先级）

```sql
-- ✅ 正确（生产SQL）：不包含 TENANT_ID 条件，由后端自动注入
SELECT * FROM wsd_plan_project WHERE DEL = 0

-- ❌ 错误：生成的 SQL 包含 TENANT_ID 占位符
SELECT * FROM wsd_plan_project WHERE DEL = 0 AND TENANT_ID = ?
```

**规则：**
- 租户ID从 SecurityContext 获取，禁止客户端请求传入
- 跨表查询时关注每个表是否需要租户隔离（由应用层保证）
- verifySql.js 验证时通过 CLI 参数注入 tenantId，用于本地开发调试

### 1.2 只允许 SELECT 操作

```sql
-- ✅ 正确：只读查询
SELECT t.id, t.task_name, t.status FROM wsd_plan_task t WHERE t.DEL = 0 AND t.TENANT_ID = ?

-- ❌ 错误：任何 UPDATE/DELETE/INSERT/DROP/TRUNCATE 都禁止
UPDATE wsd_plan_task SET status = 'xxx' WHERE ...
DELETE FROM wsd_plan_task WHERE ...
```

### 1.3 参数化查询（防 SQL 注入）

```sql
-- ✅ 正确：参数化
SELECT * FROM wsd_plan_task 
WHERE DEL = 0 AND TENANT_ID = ? AND STATUS = ?

-- ❌ 错误：字符串拼接（即使看起来"安全"也不允许）
SELECT * FROM wsd_plan_task 
WHERE DEL = 0 AND TENANT_ID = ${tenantId} AND STATUS = '${status}'
```

### 1.4 DEL 删除标记过滤

```sql
-- ✅ 正确
SELECT * FROM wsd_plan_task WHERE DEL = 0 AND TENANT_ID = ?

-- 以下表没有 DEL 字段，查询时不加 DEL 条件：
-- - wsd_risk_register（用 IS_CLOSE 标记关闭状态）
-- - wsd_base_dict
-- - INFORMATION_SCHEMA 表
```

---

## 二、字段白名单

### 2.1 允许查询的字段（数据字段）

```
项目:    id, code, name, status, complete_pct, plan_sum, act_sum,
         plan_start_time, plan_end_time, act_start_time, act_end_time,
         base_line_time, parent_id, user_id, org_id, tenant_id
         
任务:    id, task_code, task_name, task_type, status, feedback_status,
         plan_start_time, plan_end_time, act_start_time, act_end_time,
         complete_pct, plan_qty, act_qty, remain_qty,
         plan_drtn, act_drtn, remain_drtn,
         user_id, org_id, project_id, parent_id, critical, tenant_id
         
风险:    id, risk_code, risk_name, risk_type, risk_status,
         probability_level, aftermath_level, risk_level,
         project_id, is_close, discern_data, close_date,
         user_id, org_id, tenant_id
         
资源分配: id, task_id, rsrc_id, project_id, plan_start_time, plan_end_time,
          plan_qty, act_qty, remain_qty, budget_cost, act_cost, rsrc_type
          
里程碑:  id, task_code, task_name, plan_start_time, plan_end_time,
         act_start_time, act_end_time, feedback_status, project_id
         (通过 wsd_plan_task WHERE task_type IN (2,3) 实现)
```

### 2.2 禁止查询的字段（系统/敏感字段）

```
- CREATOR, CREAT_TIME（创建人/时间，应由系统自动记录）
- LAST_UPD_USER, LAST_UPD_TIME（最后更新人/时间）
- WSDVER（版本号）
- SORT_NUM（排序号）
- EXT_ID（外部系统ID）
- 任何包含 _IP 的字段（如 LAST_UPD_IP）
- 任何包含 PASSWORD/TOKEN/SECRET 的字段
```

### 2.3 字典表字段（注意 JOIN 时的小数陷阱）

```sql
-- ✅ 正确：STRING 类型字段直接比字符串
SELECT * FROM wsd_risk_register 
WHERE RISK_STATUS = 'IDENTIFIED' AND DEL = 0 AND TENANT_ID = ?

-- ✅ 正确：NUMERIC 类型字段比数字  
SELECT * FROM wsd_risk_register 
WHERE PROBABILITY_LEVEL = 3 AND DEL = 0 AND TENANT_ID = ?

-- ⚠️ 注意：实际数据中 probability_level 是 VARCHAR('3') 不是 INT(3)
-- 查询时要明确类型匹配
SELECT * FROM wsd_risk_register 
WHERE PROBABILITY_LEVEL = '3' AND DEL = 0
```

---

## 三、查询限制

### 3.1 分页限制

```sql
-- ✅ 正确：强制 LIMIT
SELECT t.id, t.task_name 
FROM wsd_plan_task t 
WHERE t.DEL = 0 AND t.TENANT_ID = ?
LIMIT 20 OFFSET 0

-- 默认每页 20 条，最大不超过 100 条
-- ⚠️ 看板数据（KANBAN视图）通常需要全部数据，需要明确说明不分页
```

### 3.2 JOIN 层数限制

```sql
-- ✅ 正确：最多 3 张表 JOIN
SELECT p.name, t.task_name, u.user_name
FROM wsd_plan_project p
LEFT JOIN wsd_plan_task t ON t.project_id = p.id AND t.DEL = 0
LEFT JOIN wsd_sys_user u ON u.id = t.user_id
WHERE p.DEL = 0 AND p.TENANT_ID = ?

-- ❌ 错误：超过 3 张表 JOIN
-- 复杂数据应在 Service 层分步查询后聚合
```

### 3.3 禁止 LIKE '%...%' 全模糊（性能风险）

```sql
-- ⚠️ 尽量避免，确需使用时必须限制返回条数
SELECT * FROM wsd_plan_task 
WHERE task_name LIKE CONCAT('%', ?, '%') 
LIMIT 20
```

### 3.4 禁止子查询嵌套过深

```sql
-- 最多 1 层子查询
SELECT * FROM (
    SELECT * FROM wsd_plan_task WHERE DEL = 0
) t WHERE t.TENANT_ID = ?
```

---

## 四、特定场景规则

### 4.1 看板数据查询

```sql
-- 看板列状态映射（任务 status → 看板列）
-- 由前端 ADP 平台配置，后端只返回原始数据
-- 查询时返回 task.status 和 feedback_status 让前端自行映射

SELECT 
    t.id AS task_id,
    t.task_name,
    t.status,          -- EDIT/APPROVAL/CONFIRM/RELEASE
    t.feedback_status, -- 0/1/2
    t.complete_pct,
    t.plan_end_time,
    u.user_name AS assignee_name,
    t.critical
FROM wsd_plan_task t
LEFT JOIN wsd_sys_user u ON u.id = t.user_id
WHERE t.project_id = ?
  AND t.DEL = 0
ORDER BY t.plan_end_time
```

### 4.2 KPI/健康度计算

```sql
-- 延期任务数
SELECT COUNT(*) FROM wsd_plan_task
WHERE project_id = ?
  AND DEL = 0
  AND feedback_status IN ('0', '1')
  AND plan_end_time < CURDATE()
  AND TENANT_ID = ?

-- 按期完成数
SELECT COUNT(*) FROM wsd_plan_task
WHERE project_id = ?
  AND DEL = 0
  AND feedback_status = '2'
  AND act_end_time <= plan_end_time
  AND TENANT_ID = ?
```

### 4.3 风险热力图

```sql
-- 注意：wsd_risk_register 表没有 DEL 字段，用 is_close = 'N' 标记未关闭风险
SELECT 
    probability_level AS prob,
    aftermath_level AS impact,
    COUNT(*) AS count
FROM wsd_risk_register
WHERE project_id = ?
  AND is_close = 'N'
GROUP BY probability_level, aftermath_level
```

### 4.4 里程碑时间线

```sql
-- 注意：里程碑不存在独立表，用 task_type IN (2,3) 标识
SELECT 
    t.id,
    t.task_name,
    t.plan_start_time,
    t.plan_end_time,
    t.act_end_time,
    t.feedback_status,
    o.org_name,
    u.user_name
FROM wsd_plan_task t
LEFT JOIN wsd_sys_org o ON o.id = t.org_id
LEFT JOIN wsd_sys_user u ON u.id = t.user_id
WHERE t.project_id = ?
  AND t.task_type IN (2, 3)
  AND t.DEL = 0
ORDER BY t.plan_end_time
```

### 4.5 资源负载

```sql
SELECT 
    r.rsrc_user_name,
    r.plan_qty,
    r.act_qty,
    r.remain_qty,
    t.task_name
FROM wsd_plan_taskrsrc r
LEFT JOIN wsd_plan_task t ON t.id = r.task_id
WHERE r.project_id = ?
  AND r.DEL = 0
  AND t.DEL = 0
GROUP BY r.rsrc_user_name, t.task_name
```

---

## 五、枚举值速查（避免写错）

| 字段 | 表 | 值类型 | 可用值 |
|------|-----|--------|--------|
| STATUS | wsd_plan_project | 字符串 | active, close, sale, Cancel |
| STATUS | wsd_plan_task | 字符串 | EDIT, APPROVAL, CONFIRM, RELEASE |
| FEEDBACK_STATUS | wsd_plan_task | 数字字符串 | 0（未开始）, 1（进行中）, 2（已完成）|
| TASK_TYPE | wsd_plan_task | 数字字符串 | 0（普通任务）, 1（作业任务）, 2（开始里程碑）, 3（完成里程碑）, 4（资源任务）|
| DEL | 大部分表 | 数字 | 0（未删除）, 1（已删除）|
| TENANT_ID | 有租户字段的表 | 数字 | 从 SecurityContext 获取 |
| RISK_STATUS | wsd_risk_register | 字符串 | IDENTIFIED, COPING, CLOSED, UNIDENTIFY |
| IS_CLOSE | wsd_risk_register | 字符串 | Y/N |
| RELATION_TYPE | wsd_plan_taskpred | 字符串 | FS, SS, SF, FF |
| DELV_STATUS | wsd_plan_delvassign | 字符串 | NOACCEPTANCE, ACCEPTANCE |

---

## 六、错误示例与正确写法

### 场景1：查询某项目的所有任务

```sql
-- ❌ 缺少租户隔离
SELECT * FROM wsd_plan_task WHERE project_id = 12345

-- ❌ 缺少 DEL 标记
SELECT * FROM wsd_plan_task WHERE project_id = 12345 AND TENANT_ID = 101

-- ❌ 用 IN 而非 = 导致性能问题（小表可以忽略）
SELECT * FROM wsd_plan_task WHERE project_id IN (12345) AND DEL = 0

-- ✅ 正确
SELECT id, task_name, status, feedback_status, complete_pct, plan_end_time,
       user_id, org_id, project_id, plan_start_time, plan_end_time, del, tenant_id
FROM wsd_plan_task 
WHERE project_id = 12345 AND DEL = 0 AND TENANT_ID = 101
```

### 场景2：查询延期任务数

```sql
-- ❌ 直接用 status='OVERDUE'（不存在这个状态）
SELECT COUNT(*) FROM wsd_plan_task 
WHERE project_id = ? AND status = 'OVERDUE' AND DEL = 0

-- ✅ 正确：用 feedback_status + plan_end_time 判断
SELECT COUNT(*) FROM wsd_plan_task 
WHERE project_id = ? 
  AND DEL = 0 
  AND feedback_status IN ('0', '1') 
  AND plan_end_time < CURDATE()
  AND TENANT_ID = ?
```

### 场景3：风险四象限

```sql
-- ❌ 直接 GROUP BY 字符串可能乱序
SELECT probability_level, aftermath_level, COUNT(*) 
FROM wsd_risk_register 
WHERE project_id = ? AND IS_CLOSE = 'N'
GROUP BY probability_level, aftermath_level

-- ✅ 正确（显式 CAST 为数字并排序）
SELECT CAST(probability_level AS UNSIGNED) AS prob, 
       CAST(aftermath_level AS UNSIGNED) AS impact, 
       COUNT(*) AS count
FROM wsd_risk_register 
WHERE project_id = ? AND IS_CLOSE = 'N'
GROUP BY prob, impact
ORDER BY prob, impact
```

---

## 七、SQL 生成检查清单

生成 SQL 后，逐项核对：

```
☐ 1. 包含 WHERE DEL = 0（除非是无 DEL 字段的表）
☐ 2. 包含 WHERE TENANT_ID = ?（除非是无 TENANT 字段的系统表）
☐ 3. 只有 SELECT，不包含 UPDATE/DELETE/INSERT/DROP
☐ 4. 所有字段值用参数占位符 ? 而非字符串拼接
☐ 5. 枚举值使用正确的字符串格式（如 'RELEASE' 而非 RELEASE）
☐ 6. LIMIT 不超过 100（看板全量数据需明确说明）
☐ 7. JOIN 不超过 3 张表
☐ 8. 不包含禁止字段（CREATOR, PASSWORD 等）
☐ 9. 数字枚举值用字符串形式（如 '0' 而非 0，用于 risk_register 等 VARCHAR 字段）
☐ 10. 日期比较使用 CURDATE() 或具体日期值，不依赖数据库函数差异
```

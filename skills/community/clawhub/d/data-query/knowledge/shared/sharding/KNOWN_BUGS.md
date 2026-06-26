# ShardingSphere 已知 BUG 与规避方案

## 一、必须规避的 SQL 模式

### 1. GROUP BY + COUNT(*) 归并异常

| 项目 | 说明 |
|------|------|
| **触发条件** | `GROUP BY col + COUNT(*)` 在多分片下执行 |
| **表现症状** | 返回数据条数正确，但聚合值（COUNT/SUM/AVG）异常 |
| **根因** | ShardingSphere 在分片场景下对聚合函数的结果归并处理有 bug |
| **规避方案** | 去掉 SQL 聚合，返回原始数据，由前端 JavaScript 聚合 |

**规避示例：**

```sql
-- ❌ 禁用（会归并异常）
SELECT PROBABILITY_LEVEL, AFTERMATH_LEVEL, COUNT(*) AS count
FROM wsd_risk_register
WHERE PROJECT_ID = ? AND IS_CLOSE = 'N'
GROUP BY PROBABILITY_LEVEL, AFTERMATH_LEVEL

-- ✅ 启用（返回原始数据，前端聚合）
SELECT PROBABILITY_LEVEL, AFTERMATH_LEVEL
FROM wsd_risk_register
WHERE PROJECT_ID = ? AND IS_CLOSE = 'N'
```

**前端聚合示例：**
```javascript
// 按 probability_level + aftermath_level 聚合
const heatmapData = {};
data.forEach(row => {
    const key = `${row.PROBABILITY_LEVEL}-${row.AFTERMATH_LEVEL}`;
    heatmapData[key] = (heatmapData[key] || 0) + 1;
});
```

---

### 2. 分片键上使用函数

| 项目 | 说明 |
|------|------|
| **触发条件** | WHERE 条件在分片键上使用函数或运算 |
| **表现症状** | ShardingSphere 无法确定路由，报错或全分片扫描 |
| **规避方案** | 改写为范围条件，避免在分片键上使用函数 |

**规避示例：**

```sql
-- ❌ 禁用（分片键被函数处理，无法路由）
SELECT * FROM wsd_plan_task
WHERE YEAR(PLAN_START_TIME) = 2024

-- ✅ 启用（范围条件，可正确路由）
SELECT * FROM wsd_plan_task
WHERE PLAN_START_TIME >= '2024-01-01' AND PLAN_START_TIME < '2025-01-01'
```

---

### 3. 跨分片 ORDER BY + LIMIT

| 项目 | 说明 |
|------|------|
| **触发条件** | `ORDER BY col LIMIT n` 涉及多个分片 |
| **表现症状** | 结果顺序不确定，LIMIT 结果不稳定 |
| **规避方案** | 确保 ORDER BY 的分片键在同一分片内，或接受结果不确定性 |

---

### 4. OR 条件导致全分片扫描

| 项目 | 说明 |
|------|------|
| **触发条件** | WHERE 条件使用 OR 连接，且 OR 两边涉及不同分片键 |
| **表现症状** | 路由到所有分片，查询性能严重下降 |
| **规避方案** | 拆分为 UNION ALL |

---

## 二、分片场景 SQL 编写规范

### 强制规则

1. **禁止**在分片键上使用函数、运算
2. **禁止**使用 `GROUP BY + COUNT(*)` 等聚合函数（改前端聚合）
3. **禁止**在分片键 OR 条件下使用 OR
4. **必须**在 WHERE 条件中包含分片键
5. **必须**先确认表分布在哪个分片，再编写 JOIN

### JOIN 注意事项

| 场景 | 可行性 | 说明 |
|------|--------|------|
| 同分片表之间的 JOIN | ✅ | 同一分片内，无跨分片问题 |
| 不同分片表之间的 JOIN | ❌ | ShardingSphere 不支持跨分片 JOIN |
| 涉及 ds-base 的表（wsd_sys_*）与其他表 JOIN | ❌ | wsd_sys_user/org 只在 ds-base，计划域表在 ds-biz，不能 JOIN |

---

## 三、BUG 触发自检清单

编写完 SQL 后，逐项确认：

- [ ] 没有在分片键上使用函数（如 `YEAR()`, `MONTH()`, `TO_CHAR()`）
- [ ] 没有 `GROUP BY` + `COUNT(*)` / `SUM(*)` / `AVG(*)` 模式
- [ ] WHERE 条件包含分片键（如 PROJECT_ID、TENANT_ID）
- [ ] JOIN 的表都在同一分片
- [ ] 没有在分片键上使用 OR 条件

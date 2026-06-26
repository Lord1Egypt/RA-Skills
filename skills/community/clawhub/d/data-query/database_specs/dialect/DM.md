# 达梦数据库 SQL 规范

## 一、必须遵守的规则

### 1. 日期转字符串
❌ 禁用: `TO_CHAR(date, 'YYYY-MM')`
❌ 禁用: `DATE_FORMAT(date, '%Y-%m')`
✅ 使用: `SUBSTR(CAST(date AS VARCHAR), 1, 7)`

**原因**：达梦不支持 `TO_CHAR`，`VARCHAR` 是达梦的关键字。

### 2. 分片键上禁止使用函数
❌ 禁用: `WHERE MONTH(create_time) = 6`
✅ 使用: `WHERE create_time >= '2024-06-01' AND create_time < '2024-07-01'`

**原因**：ShardingSphere 无法正确路由经过函数处理分片键的 SQL。

### 3. GROUP BY + COUNT(*) 归并问题
❌ 禁用: `SELECT PROBABILITY_LEVEL, COUNT(*) FROM wsd_risk_register GROUP BY PROBABILITY_LEVEL`
✅ 使用: `SELECT PROBABILITY_LEVEL, AFTERMATH_LEVEL FROM wsd_risk_register`（无聚合，前端 JS 聚合）

**原因**：ShardingSphere 在 `GROUP BY + COUNT(*)` 时有归并 bug，返回数据条数可能正确但聚合值异常。

**前端聚合示例**（riskHeatmap）：
```javascript
// 后端返回原始数据，前端按 probability_level + aftermath_level 聚合
const heatmapData = {};
data.forEach(row => {
    const key = `${row.probability_level}-${row.aftermath_level}`;
    heatmapData[key] = (heatmapData[key] || 0) + 1;
});
```

### 4. 字符串拼接
❌ 禁用: `CONCAT(col, 'suffix')`（在某些场景下有问题）
✅ 使用: `col || 'suffix'` 或 `CONCAT(col, 'suffix')`（达梦兼容）

### 5. 分页语法
❌ 禁用: `LIMIT 10, 20`
✅ 使用: `OFFSET 10 ROWS FETCH NEXT 20 ROWS ONLY`

## 二、分片路由注意事项

### 只在 ds-100 的表（本次 Cockpit 涉及）
| 表名 | 说明 |
|------|------|
| `WSD_PLAN_PROJECT` | 项目表 |
| `WSD_PLAN_TASK` | 任务表 |
| `WSD_PLAN_TASKRSRC` | 任务资源关联表 |
| `WSD_RSRC_USER` | 资源用户表 |
| `WSD_RISK_REGISTER` | 风险登记表 |

### 只在 ds-101 的表（不存在于 ds-100）
| 表名 | 说明 |
|------|------|
| `WSD_SYS_USER` | 系统用户表（**ds-101 专用，ds-100 无此表**） |
| `WSD_SYS_ORG` | 系统组织表（**ds-101 专用，ds-100 无此表**） |

### JOIN 注意事项
- `wsd_sys_user` / `wsd_sys_org` 只在 ds-101，**不能与 ds-100 的表直接 JOIN**
- ds-100 的表应该用 `wsd_rsrc_user`（资源用户表）代替 `wsd_sys_user`
- 不确定时：优先查询 ds-100，如果报错"无效的表或视图名"，则表不在该分片

### 分片键判断
| 表 | 分片键 |
|----|--------|
| `WSD_PLAN_PROJECT` | TENANT_ID |
| `WSD_PLAN_TASK` | PROJECT_ID, TENANT_ID |
| `WSD_PLAN_TASKRSRC` | PROJECT_ID, TENANT_ID |
| `WSD_RSRC_USER` | USER_ID |
| `WSD_RISK_REGISTER` | PROJECT_ID, TENANT_ID |

## 三、达梦与 MySQL 语法差异速查

| 场景 | MySQL | 达梦 DM | 备注 |
|------|-------|---------|------|
| 日期转字符串 | `DATE_FORMAT(date, '%Y-%m')` | `SUBSTR(CAST(date AS VARCHAR), 1, 7)` | 达梦不支持 TO_CHAR |
| 分页 | `LIMIT 10, 20` | `OFFSET 10 ROWS FETCH NEXT 20 ROWS ONLY` | 达梦用标准 SQL |
| 空值处理 | `IFNULL(col, default)` | `NVL(col, default)` | 两者都支持 |
| 自增ID | `AUTO_INCREMENT` | `IDENTITY` 或序列 | 建表时指定 |
| 字符串截取 | `SUBSTR(col, 1, 10)` | `SUBSTR(col, 1, 10)` | 兼容 |
| 日期加减 | `DATE_ADD(col, INTERVAL 1 DAY)` | `col + 1`（天数）| 达梦日期运算不同 |
| 当前时间 | `NOW()` | `SYSDATE` | |
| 字符串去空格 | `TRIM(col)` | `TRIM(col)` | 兼容 |

## 四、编写 SQL 前的检查清单

每次编写 SQL 时，逐项确认：

- [ ] 不使用 `TO_CHAR`
- [ ] 不在分片键上使用函数
- [ ] 不使用 `GROUP BY + COUNT(*)`
- [ ] JOIN 的表都在同一分片（或已配置路由）
- [ ] 表名大写（达梦规范）
- [ ] 使用 `SUBSTR(CAST(... AS VARCHAR), 1, 7)` 做日期截取
- [ ] 分页使用 `OFFSET ... FETCH NEXT ...` 语法

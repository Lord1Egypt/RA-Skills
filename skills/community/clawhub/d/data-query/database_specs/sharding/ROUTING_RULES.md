# ShardingSphere 分片路由规则

## 一、路由配置位置

```
cldm_springcloud/
└── acm-modules/
    └── acm-module-xxx/
        └── src/main/resources/
            └── application-tenant-tables.yml
```

## 二、分片策略类型

### 2.1 标准分片策略（standard）

```yaml
default-database-strategy:
  standard:
    sharding-column: tenant_id
    precise-algorithm-class-name: com.wisdom.base.common.algorithm.TenantDatabaseShardingAlgorithm
```

**含义：** 按 `tenant_id` 字段路由到对应数据库。

### 2.2 表级分片策略

```yaml
tables:
  wsd_plan_project:
    actual-data-nodes: ds-$->{[${spring.shardingsphere.master.biz}]}-master.wsd_plan_project
    table-strategy:
      none: ''
```

**含义：** 强制指定 `wsd_plan_project` 表路由到 `ds-biz` 分片。

## 三、路由判断规则

### 3.1 如何判断一条 SQL 路由到哪个分片

| WHERE 条件 | 路由结果 |
|-----------|---------|
| 包含 `TENANT_ID = 101` | 路由到 tenant_id=101 对应的数据库 |
| 包含 `PROJECT_ID = xxx` | 先找 PROJECT_ID 对应的 TENANT_ID，再路由 |
| 无分片键条件 | 全分片扫描（性能差） |
| 分片键经过函数处理 | 无法路由，全分片扫描 |

### 3.2 分片键优先级

| 分片键 | 适用表 | 说明 |
|--------|--------|------|
| TENANT_ID | 所有表 | 最顶层分片键 |
| PROJECT_ID | 任务表、风险表等 | 次级分片键 |
| USER_ID | 资源用户表 | - |

## 四、actual-data-nodes 语法

### 4.1 固定分片

```yaml
tables:
  wsd_sys_user:
    actual-data-nodes: ds-$->{[${spring.shardingsphere.master.base}]}-master.wsd_sys_user
```

强制路由到 `ds-base`。

### 4.2 分片表达式

```yaml
tables:
  wsd_plan_project:
    actual-data-nodes: ds-$->{[${spring.shardingsphere.master.all}]}-master.wsd_plan_project
```

`${spring.shardingsphere.master.all}` 表示所有分片。

## 五、强制路由场景

当表不在默认分片策略覆盖范围内时，需要显式指定 `actual-data-nodes`。

### 5.1 典型场景

```yaml
# wsd_sys_user / wsd_sys_org 在 ds-base
# wsd_plan_* 表在 ds-biz
# 如果默认策略按 tenant_id 路由，可能错误路由到 ds-biz
# 需要显式指定

tables:
  wsd_sys_user:
    actual-data-nodes: ds-$->{[${spring.shardingsphere.master.base}]}-master.wsd_sys_user
    database-strategy:
      none: ''  # 禁用数据库级分片策略
```

## 六、查看当前路由配置

```bash
# 查看 application-tenant-tables.yml 中的 actual-data-nodes 配置
grep -A5 "actual-data-nodes" application-tenant-tables.yml
```

## 七、添加新表的路由配置

当新增 SQL 查询涉及新表时：

1. 在 `application-tenant-tables.yml` 中查找该表是否有 `actual-data-nodes` 配置
2. 如无，根据表的业务归属（base/biz）添加配置
3. 重启相关微服务使配置生效
4. 用 EXPLAIN 或实际查询验证路由是否正确

---

**相关文档：**
- `knowledge/shared/sharding/TABLE_DISTRIBUTION.md` — 表分片分布速查
- `knowledge/shared/sharding/KNOWN_BUGS.md` — 已知 BUG 与规避方案

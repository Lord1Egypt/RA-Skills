# 执行计划解读（三引擎对照）

> 子技能里各引擎都提了 EXPLAIN，但**跨引擎的对照表和"看到什么该做什么"的映射**没人写。
> 本篇是执行计划的查表手册。

## 一、先跑对命令

| 引擎 | 只看计划（不执行） | 看真实执行（推荐） |
|------|-------------------|-------------------|
| MySQL | `EXPLAIN SELECT ...` | `EXPLAIN ANALYZE SELECT ...`（8.0.18+） |
| MySQL（详细） | `EXPLAIN FORMAT=JSON SELECT ...` | — |
| PostgreSQL | `EXPLAIN SELECT ...` | `EXPLAIN (ANALYZE, BUFFERS) SELECT ...` |
| MongoDB | `db.c.find(q).explain()` | `db.c.find(q).explain("executionStats")` |

**关键原则**：只看 `EXPLAIN` 是看优化器的**猜测**，`ANALYZE` 才是**事实**。
排查性能问题必须用 ANALYZE，两者差异本身就是重要线索（见第五节）。

> ⚠️ PostgreSQL 的 `EXPLAIN ANALYZE` 会**真实执行**语句。对 UPDATE/DELETE 务必包在
> `BEGIN; ... ROLLBACK;` 里。

## 二、MySQL：看 4 个字段就够

`type`、`key`、`rows`、`Extra` —— 其他列排查时基本用不上。

### type（访问类型，从好到坏）

```
system > const > eq_ref > ref > range > index > ALL
                                        ↑        ↑
                                     全索引扫描  全表扫描
                                     这两个出现就要警觉
```

| type | 含义 | 处置 |
|------|------|------|
| `const` / `eq_ref` | 主键或唯一索引等值命中 | 最优，无需动 |
| `ref` | 非唯一索引等值命中 | 良好 |
| `range` | 索引范围扫描 | 可接受，看 rows 是否过大 |
| `index` | 遍历整棵索引树 | 索引没选对，检查 WHERE 是否可用索引 |
| `ALL` | 全表扫描 | **小表可接受，大表必改** |

### Extra（真正的问题都写在这）

| Extra 值 | 含义 | 处置 |
|----------|------|------|
| `Using index` | 覆盖索引，不回表 | ✅ 最优 |
| `Using where` | 存储引擎取回后再过滤 | 一般，可优化索引减少回表行数 |
| `Using filesort` | **额外排序**（不一定用磁盘） | 让索引顺序匹配 ORDER BY |
| `Using temporary` | **建临时表**（GROUP BY / DISTINCT / UNION） | 最该消灭的，常与 filesort 同时出现 |
| `Using join buffer` | JOIN 无可用索引 | 给被驱动表的关联列建索引 |
| `Impossible WHERE` | 条件恒假 | 查询逻辑有问题 |

> **口诀**：`ALL` + `Using temporary` + `Using filesort` 三连出现，就是慢查询的典型画像。

## 三、PostgreSQL：看节点类型 + 三个数字

PG 的计划是**树**，从最内层（缩进最深）往外读。

### 节点类型

| 节点 | 含义 | 何时是问题 |
|------|------|-----------|
| `Seq Scan` | 全表扫描 | 大表上出现 → 缺索引，或优化器认为索引不划算 |
| `Index Scan` | 索引扫描 + 回表 | 正常 |
| `Index Only Scan` | 覆盖索引，不回表 | ✅ 最优（注意 `Heap Fetches` 要低，否则 vacuum 不足） |
| `Bitmap Heap Scan` | 先攒 bitmap 再批量回表 | 中等选择性时的正常选择 |
| `Nested Loop` | 嵌套循环 JOIN | **`loops` 很大时是灾难**，看内层是否有索引 |
| `Hash Join` | 哈希 JOIN | 大表 JOIN 的正常选择 |
| `Merge Join` | 归并 JOIN | 双方已排序时高效 |
| `Sort` | 排序 | 看 `Sort Method`：`quicksort` 内存内 OK，**`external merge Disk` 说明 work_mem 不足** |

### 三个数字

```
Seq Scan on orders  (cost=0.00..18334.00 rows=1000 width=64)
                    (actual time=0.015..85.234 rows=980000 loops=1)
                                                  ↑
                    估算 1000 行，实际 98 万行 —— 差 980 倍
```

1. **`rows` 估算 vs actual** —— 偏差 > 10 倍说明统计信息过期，先 `ANALYZE <table>;`
2. **`loops`** —— Nested Loop 内层的 `loops` 值就是循环次数，`actual time` 要乘以它
3. **`Buffers: shared read=N`** —— `read` 大说明没命中缓存，走了磁盘（需加 `BUFFERS` 选项）

## 四、MongoDB：只看 winningPlan 与三个 n

```js
db.orders.find({status:"paid"}).sort({created:-1}).explain("executionStats")
```

| 字段 | 含义 | 健康值 |
|------|------|--------|
| `winningPlan.stage` | `COLLSCAN` = 全集合扫描 / `IXSCAN` = 走索引 | 必须是 `IXSCAN` |
| `SORT` 阶段存在 | 内存排序（超 32MB 直接报错） | 应由索引提供顺序，不该出现 |
| `nReturned` | 返回文档数 | — |
| `totalKeysExamined` | 扫描索引条目数 | 应 ≈ nReturned |
| `totalDocsExamined` | 扫描文档数 | 应 ≈ nReturned，**为 0 则是覆盖查询（最优）** |

**核心比值**：`totalDocsExamined / nReturned`。等于 1 最优；超过 10 说明索引筛选力不足；
等于集合总数说明是 COLLSCAN。

## 五、估算与实际的偏差：最有价值的信号

三个引擎共通：**优化器猜错行数 → 选错执行策略**。这是慢查询的隐藏根因。

| 现象 | 根因 | 修法 |
|------|------|------|
| PG 估 1000 行实际 100 万 | 统计信息过期 | `ANALYZE tbl;` 或调高 `default_statistics_target` |
| MySQL `rows` 与实际差很多 | InnoDB 统计采样不足 | `ANALYZE TABLE tbl;`，调 `innodb_stats_persistent_sample_pages` |
| 相关列组合估算失真（如 city+province） | 优化器假设列间独立 | PG：`CREATE STATISTICS`；MySQL：改查询或加联合索引 |
| 首次快、之后慢 | 参数嗅探 / 计划缓存 | PG 检查 `plan_cache_mode`；用真实参数值重跑 EXPLAIN |

## 六、从计划到动作的映射表

| 看到 | 先做什么 |
|------|----------|
| MySQL `type=ALL` + 大表 | 给 WHERE 首列建索引；确认没在列上套函数 |
| MySQL `Using filesort` | 建 `(过滤列, 排序列)` 联合索引，顺序要对 |
| MySQL `Using temporary` | GROUP BY 列加索引；或改写去掉 DISTINCT |
| PG `Seq Scan` 大表 | 建索引；若已有索引未用，检查类型是否匹配（`bigint` vs `int`） |
| PG `external merge Disk` | 调大 `work_mem`（会话级 `SET work_mem='64MB'` 先验证） |
| PG `Nested Loop` + loops 巨大 | 内层表关联列建索引；或 `SET enable_nestloop=off` 验证是否该走 Hash |
| Mongo `COLLSCAN` | 按 **ESR 规则**建索引（见 `index-design.md`） |
| Mongo `SORT` 阶段 | 把排序列并入索引尾部 |
| 任意引擎 估算/实际偏差 >10x | 先更新统计信息，再谈索引 |

## 七、踩坑记录

- **在列上套函数导致索引失效**：`WHERE DATE(created_at)='2026-08-07'` 用不了索引，
  改写成 `WHERE created_at >= '2026-08-07' AND created_at < '2026-08-08'`。
- **隐式类型转换**：`WHERE user_id = '123'`（列是 BIGINT）在 MySQL 会导致全表扫描。
- **只测一次就下结论**：第一次执行含冷缓存，至少跑三次取稳定值。
- **在空表 / 小表上做 EXPLAIN**：优化器对小表一律选全表扫描，测不出真实行为。必须用接近生产的数据量。
- **PG 忘了加 BUFFERS**：没有 `BUFFERS` 就看不出是内存命中还是磁盘 IO，等于少了一半信息。
- **Mongo 用 `explain()` 不带参数**：默认 `queryPlanner` 模式不含真实执行数据，必须传 `"executionStats"`。

## 八、检查清单

- [ ] 用 `ANALYZE` 变体而非纯 `EXPLAIN`
- [ ] 数据量接近生产（不是空表）
- [ ] 重复执行 ≥3 次，排除冷缓存
- [ ] 检查估算行数 vs 实际行数偏差
- [ ] 确认无 `ALL` / `Seq Scan`（大表）/ `COLLSCAN`
- [ ] 确认无 `Using temporary` / `external merge Disk` / `SORT` 阶段
- [ ] 优化后重跑并**记录前后对比数字**，不靠感觉

## 相关子技能与层次边界

本 playbook 负责**三引擎（MySQL / PostgreSQL / MongoDB）执行计划解读**的决策；不负责建索引本身，索引见兄弟参考。

- 落地到 [skills/mysql/SKILL.md](../skills/mysql/SKILL.md)：EXPLAIN / EXPLAIN FORMAT=JSON 解读（type / rows / filtered）。
- 落地到 [skills/postgres-patterns/SKILL.md](../skills/postgres-patterns/SKILL.md)：EXPLAIN (ANALYZE, BUFFERS) 解读（Seq Scan / 预估偏差）。
- 落地到 [skills/mongodb-query-optimizer/SKILL.md](../skills/mongodb-query-optimizer/SKILL.md)：explain("executionStats") 解读（COLLSCAN / 索引命中）。
- 兄弟参考：
  - [references/index-design.md](index-design.md)：索引直接改变执行计划。
  - [references/slow-query-triage.md](slow-query-triage.md)：慢查询先读计划再下手。
- 脚本：
  - [scripts/explain_audit.py](../scripts/explain_audit.py)：对执行计划做体检（扫描类型 / 估算行数偏差 / 临时表阶段）。

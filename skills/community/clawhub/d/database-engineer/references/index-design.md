# 索引设计决策

> 子技能列举了各引擎有哪些索引类型。本篇写的是**怎么决定建哪个、列怎么排序、
> 以及什么时候不该建**——这部分决策成本最高，也最少被写清楚。

## 一、列顺序：ESR 规则（三引擎通用）

联合索引的列顺序不是随意的，按 **Equality → Sort → Range** 排列：

```sql
-- 查询
SELECT * FROM orders
WHERE tenant_id = 42          -- E 等值
  AND status   = 'paid'       -- E 等值
  AND amount   > 100          -- R 范围
ORDER BY created_at DESC;     -- S 排序

-- ✅ 正确索引
CREATE INDEX idx ON orders (tenant_id, status, created_at, amount);
--                          └── E ──────────┘  └─ S ─┘   └ R ┘
```

**为什么 Range 必须放最后**：B-Tree 上一旦遇到范围条件，其后的列就**不再有序**，
无法继续用于过滤或排序。把 `amount > 100` 放在 `created_at` 前面，排序就得靠 filesort。

> 这条规则最早由 MongoDB 官方文档提出（ESR Rule），但它是 B-Tree 的固有性质，
> 对 MySQL、PostgreSQL 完全同样适用。

## 二、建不建索引的决策树

```
这个查询慢吗？
├─ 否 → 不建。索引不是免费的（见第六节成本）
└─ 是 → 该列的选择性如何？
        选择性 = COUNT(DISTINCT col) / COUNT(*)
        ├─ > 0.1（如 user_id、email）→ 建，效果好
        ├─ 0.01 ~ 0.1（如 city）→ 建联合索引，别单建
        └─ < 0.01（如 status 只有 3 个值、is_deleted）
           ├─ 查询总是命中稀有值（如 status='failed' 占 0.1%）
           │  → 建 **部分索引**（PG）/ 联合索引把它放首列（MySQL）
           └─ 查询命中常见值 → 不建，全表扫描反而更快
```

**选择性速查 SQL**：

```sql
SELECT
  COUNT(DISTINCT status)::float / COUNT(*) AS selectivity,
  COUNT(*) AS total
FROM orders;
-- < 0.01 时单列索引通常无效
```

## 三、覆盖索引：最被低估的优化

索引包含了查询需要的**全部列**时，引擎不必回表读数据行，IO 直接减半甚至更多。

```sql
-- 查询只要这三列
SELECT tenant_id, status, created_at FROM orders WHERE tenant_id = 42;

-- 覆盖索引
CREATE INDEX idx ON orders (tenant_id, status, created_at);
-- MySQL EXPLAIN → Extra: "Using index"     ✅
-- PG   EXPLAIN → "Index Only Scan"          ✅
```

各引擎的"附带列"语法（只存不用于过滤，减小索引体积）：

| 引擎 | 语法 |
|------|------|
| PostgreSQL | `CREATE INDEX idx ON t (a, b) INCLUDE (c, d);` |
| MySQL | 无 INCLUDE，直接把列加进联合索引尾部 |
| MongoDB | 无，索引字段即覆盖字段 |

> PG 的 `Index Only Scan` 要真正生效，还需 visibility map 是最新的——
> 若 `Heap Fetches` 很高，说明 autovacuum 跟不上，需调优 vacuum 而非改索引。

## 四、各引擎的特有索引：什么时候用

### PostgreSQL

| 类型 | 适用 | 典型场景 |
|------|------|----------|
| B-Tree（默认） | 等值、范围、排序 | 90% 场景 |
| **GIN** | 包含关系：数组、JSONB、全文 | `WHERE tags @> '{"vip"}'`、`tsvector` 检索 |
| **GiST** | 几何、范围重叠、近邻 | PostGIS、`tsrange &&` 排他约束 |
| **BRIN** | 物理有序的超大表 | 时序日志表按时间追加写，索引体积极小 |
| **部分索引** | 只索引一小部分行 | `WHERE status='pending'`，队列表的救命技巧 |
| **表达式索引** | 查询里有函数 | `CREATE INDEX ON t (lower(email));` |

```sql
-- 部分索引：队列表只有 pending 需要被扫，索引可以小 1000 倍
CREATE INDEX idx_pending ON jobs (created_at) WHERE status = 'pending';
```

### MySQL

基本只有 B-Tree。可用技巧：
- **前缀索引**：`INDEX (url(64))` —— 长文本列省空间，但**无法用于覆盖索引与排序**
- **降序索引**（8.0+）：`INDEX (a ASC, b DESC)` —— 混合排序方向时才需要
- **函数索引**（8.0.13+）：`INDEX ((LOWER(email)))` —— 注意双括号

### MongoDB

- **多键索引**：数组字段自动创建，注意一个复合索引**最多含一个数组字段**
- **部分索引**：`partialFilterExpression`，同 PG 的部分索引
- **TTL 索引**：`expireAfterSeconds`，自动清理过期文档（日志/会话表首选）
- **通配符索引**：`{"attrs.$**": 1}` —— 属性名不固定时的兜底，性能弱于精确索引

## 五、索引冗余：定期清理

联合索引 `(a, b, c)` 已经覆盖了 `(a)` 和 `(a, b)` 的查询能力，**单独的 `(a)` 索引是冗余的**。

```sql
-- MySQL 8.0：查未被使用的索引
SELECT * FROM sys.schema_unused_indexes;

-- PostgreSQL：查扫描次数为 0 的索引
SELECT relname, indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;

-- MongoDB
db.orders.aggregate([{$indexStats:{}}])   // accesses.ops 为 0 的可考虑删
```

> 删索引前**至少观察一个完整业务周期**（含月末结算、季度报表这类低频但关键的查询）。
> 统计从上次重启开始累计，重启过就不算数。

## 六、索引的真实成本（决定"不建"的依据）

| 成本 | 量级 |
|------|------|
| 写放大 | 每个索引让 INSERT/UPDATE/DELETE 多一次 B-Tree 维护 |
| 存储 | 一个联合索引常达表体积的 10%–30% |
| 内存挤占 | 索引与数据抢 Buffer Pool / shared_buffers |
| 优化器负担 | 候选索引越多，选错的概率越大 |
| 迁移成本 | 大表加索引需要在线 DDL 方案（见 `schema-migration.md`） |

**经验阈值**：单表索引数 > 5 就该复查，> 8 基本可以确定有冗余。
写入密集型表尤其要克制。

## 七、踩坑记录

- **最左前缀被忽略**：索引 `(a,b,c)`，查询 `WHERE b=1 AND c=2` **用不上**这个索引。
- **`OR` 打断索引**：`WHERE a=1 OR b=2` 通常退化为全表扫描，改写为 `UNION ALL` 两条子查询。
- **`LIKE '%xxx'` 前置通配**：无法走 B-Tree。需要中缀搜索用 PG 的 `pg_trgm` + GIN。
- **`NULL` 语义**：MySQL 索引存 NULL，PG 也存，但 `IS NOT NULL` 的选择性常被高估。
- **在低选择性列上单独建索引**：`is_deleted` 单独建索引几乎永远无效，应作为部分索引的条件。
- **一次加多个索引就上线**：无法归因是哪个起了作用，也无法评估写入退化。一次一个，量化前后。
- **在 UUID 主键上用 InnoDB**：随机主键导致页分裂严重。用有序 UUID（UUIDv7）或自增 BIGINT。
- **给外键列忘了建索引**：MySQL 的 InnoDB 会自动建，**PostgreSQL 不会**——PG 里外键列
  没索引会让父表 DELETE/UPDATE 变成全表扫描。这是 PG 最常见的性能坑之一。

## 八、检查清单

评审阶段建议直接套用 [assets/schema-review-checklist.md](../assets/schema-review-checklist.md)（含 MR 模板与一票否决项）；
表结构层面的机械问题先交给脚本，把人的注意力留给设计判断：

```bash
python3 scripts/schema_lint.py migrations/V42__add_orders.sql --dialect postgres --strict
```

- [ ] 列顺序符合 ESR（等值 → 排序 → 范围）
- [ ] 计算过选择性，低选择性列没有单独建索引
- [ ] 高频查询检查过能否做成覆盖索引
- [ ] PG：所有外键列都有索引
- [ ] 没有被联合索引完全包含的冗余单列索引
- [ ] 单表索引数 ≤ 5（超出需说明理由）
- [ ] 大表加索引已确认在线 DDL 方案
- [ ] 上线前后有 EXPLAIN 对比数据，不靠感觉

## 相关子技能与层次边界

本 playbook 负责**索引设计决策（选型 / 冗余 / 在线加索引）**；不负责执行计划解读，见兄弟参考。

- 落地到 [skills/mysql/SKILL.md](../skills/mysql/SKILL.md)：MySQL 索引类型与在线 DDL（INPLACE / gh-ost）。
- 落地到 [skills/postgres-patterns/SKILL.md](../skills/postgres-patterns/SKILL.md)：PostgreSQL 索引类型（B-tree / 部分 / 表达式 / GIN）。
- 落地到 [skills/mongodb-query-optimizer/SKILL.md](../skills/mongodb-query-optimizer/SKILL.md)：MongoDB 复合索引与 ESR 规则。
- 兄弟参考：
  - [references/explain-reading.md](explain-reading.md)：上线前后 EXPLAIN 对比，不靠感觉。
  - [references/slow-query-triage.md](slow-query-triage.md)：缺索引是最常见慢查询根因。
  - [references/schema-migration.md](schema-migration.md)：大表在线加索引的锁方案。

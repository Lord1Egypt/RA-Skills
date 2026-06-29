---
name: database-optimization
description: "数据库性能优化专家技能。涵盖 SQL 查询优化、索引策略设计、查询计划分析、ORM 优化、连接池调优。支持 PostgreSQL、MySQL、SQLite。当用户遇到：慢查询、数据库性能问题、需要设计索引、分析查询计划、优化 SQL 语句、解决 N+1 查询问题、调优连接池、分析数据库锁、优化 ORM 查询、数据库监控诊断时，立即使用此技能。即使用户只说'查询很慢'、'加个索引'、'SQL 优化'、'数据库卡了'，也应触发此技能。"
version: 1.0.0
---

# Database Optimization — 数据库性能优化

## 优化方法论

```
1. 度量 → 2. 分析 → 3. 优化 → 4. 验证
   ↑                                ↓
   └────────── 持续监控 ←───────────┘
```

**铁律：不度量就不优化。** 先拿到基线数据，再做改动，最后验证效果。

---

## 一、查询分析（第一步永远是这个）

### 1.1 PostgreSQL — EXPLAIN ANALYZE

```sql
-- 基础：查看执行计划
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- 完整：实际执行 + 真实耗时（推荐）
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) 
SELECT * FROM users WHERE email = 'test@example.com';

-- JSON 格式（便于程序解析）
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) 
SELECT * FROM users WHERE email = 'test@example.com';
```

**关键指标解读：**

| 指标 | 含义 | 健康值 |
|------|------|--------|
| `Seq Scan` | 全表扫描 | 大表上应避免 |
| `Index Scan` | 索引扫描 | ✅ 正常 |
| `Index Only Scan` | 仅索引扫描 | ✅✅ 最优 |
| `Bitmap Heap Scan` | 位图扫描 | 中等行数可接受 |
| `Nested Loop` | 嵌套循环 | 小表 OK，大表警惕 |
| `Hash Join` | 哈希连接 | ✅ 通常高效 |
| `Sort (external merge)` | 外部排序 | ⚠️ work_mem 不足 |
| `actual time` | 实际耗时(ms) | 关注顶层节点 |
| `rows` vs `plan rows` | 实际行数 vs 估算 | 差距 >10x 需 ANALYZE |
| `Buffers: shared hit` | 缓存命中 | 越高越好 |
| `Buffers: shared read` | 磁盘读取 | 越高越差 |

### 1.2 MySQL — EXPLAIN

```sql
-- 基础执行计划
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- 更详细（MySQL 8.0+）
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- 格式化输出
EXPLAIN FORMAT=JSON SELECT * FROM users WHERE email = 'test@example.com';
```

**关键指标：**

| 字段 | 关注点 |
|------|--------|
| `type` | 从好到差：system > const > eq_ref > ref > range > index > ALL |
| `key` | 实际使用的索引，NULL = 未用索引 |
| `rows` | 预估扫描行数 |
| `Extra` | Using filesort / Using temporary = 需优化 |
| `filtered` | 过滤比例，越低说明扫描越多无用行 |

### 1.3 SQLite

```sql
-- 开启查询计划
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'test@example.com';

-- 开启统计
.timer on
SELECT * FROM users WHERE email = 'test@example.com';
```

---

## 二、索引策略

### 2.1 索引类型速查

| 类型 | 适用场景 | PostgreSQL | MySQL |
|------|---------|-----------|-------|
| **B-Tree** | 等值/范围/排序 | ✅ 默认 | ✅ 默认 |
| **Hash** | 仅等值查询 | ✅ 少用 | ❌ (InnoDB 自适应) |
| **GiST** | 几何/全文/范围 | ✅ | ❌ |
| **GIN** | 数组/JSON/全文 | ✅ | ❌ |
| **BRIN** | 时序数据(大表) | ✅ | ❌ |
| **Partial** | 条件索引 | ✅ | ✅ (前缀索引) |
| **Covering** | 避免回表 | ✅ (INCLUDE) | ✅ |
| **Composite** | 多列组合 | ✅ | ✅ |

### 2.2 索引设计原则

**原则 1：为查询设计索引，不是为表**

```sql
-- ❌ 错误：给每列单独建索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_created ON users(created_at);

-- ✅ 正确：分析查询模式，设计组合索引
-- 查询：WHERE status = 'active' ORDER BY created_at DESC
CREATE INDEX idx_users_status_created ON users(status, created_at DESC);
```

**原则 2：最左前缀匹配**

```sql
-- 索引 (a, b, c)
-- ✅ 能使用：WHERE a=1 / WHERE a=1 AND b=2 / WHERE a=1 AND b=2 AND c=3
-- ❌ 不能使用：WHERE b=2 / WHERE c=3 / WHERE b=2 AND c=3
```

**原则 3：覆盖索引避免回表**

```sql
-- 查询只需要 email, name
-- ❌ 需要回表
CREATE INDEX idx_users_email ON users(email);
SELECT email, name FROM users WHERE email = 'test@example.com';

-- ✅ 覆盖索引（PostgreSQL）
CREATE INDEX idx_users_email_cover ON users(email) INCLUDE (name);
SELECT email, name FROM users WHERE email = 'test@example.com';

-- ✅ 覆盖索引（MySQL）
CREATE INDEX idx_users_email_name ON users(email, name);
```

**原则 4：部分索引（PostgreSQL）**

```sql
-- 只索引活跃用户（减少索引大小）
CREATE INDEX idx_users_active_email ON users(email) WHERE is_active = true;

-- 只索引未删除的订单
CREATE INDEX idx_orders_pending ON orders(created_at) WHERE status = 'pending';
```

### 2.3 索引反模式

| 反模式 | 问题 | 解决方案 |
|--------|------|---------|
| 过多索引 | 写入慢、空间大 | 定期审查未使用索引 |
| 函数索引缺失 | `WHERE LOWER(email) = ?` 不走索引 | 创建函数索引 |
| 隐式类型转换 | `WHERE varchar_col = 123` | 确保类型匹配 |
| 前导通配符 | `WHERE name LIKE '%test'` | 使用全文索引 |
| OR 条件 | `WHERE a=1 OR b=2` 可能不走索引 | 改为 UNION ALL |

### 2.4 查找未使用的索引

```sql
-- PostgreSQL
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0  -- 从未被使用
ORDER BY pg_relation_size(indexrelid) DESC;

-- MySQL (需要 performance_schema)
SELECT object_schema, object_name, index_name, count_star
FROM performance_schema.events_statements_summary_by_digest
WHERE index_name NOT IN ('PRIMARY', 'NULL')
AND count_star = 0;
```

---

## 三、SQL 优化模式

### 3.1 分页优化

```sql
-- ❌ 深分页性能差
SELECT * FROM posts ORDER BY id LIMIT 10 OFFSET 100000;

-- ✅ 游标分页（推荐）
SELECT * FROM posts WHERE id > :last_id ORDER BY id LIMIT 10;

-- ✅ 延迟关联（PostgreSQL）
SELECT p.* FROM posts p
JOIN (SELECT id FROM posts ORDER BY id LIMIT 10 OFFSET 100000) t ON p.id = t.id;
```

### 3.2 COUNT 优化

```sql
-- ❌ 全表扫描
SELECT COUNT(*) FROM orders WHERE status = 'pending';

-- ✅ 方案 1：维护计数表
CREATE TABLE order_counters (status TEXT PRIMARY KEY, count BIGINT DEFAULT 0);
-- 用触发器维护

-- ✅ 方案 2：估算（PostgreSQL）
SELECT reltuples::BIGINT AS estimate FROM pg_class WHERE relname = 'orders';

-- ✅ 方案 3：部分索引 + COUNT
CREATE INDEX idx_orders_pending ON orders(id) WHERE status = 'pending';
SELECT COUNT(*) FROM orders WHERE status = 'pending';  -- 只扫描索引
```

### 3.3 JOIN 优化

```sql
-- ❌ 笛卡尔积风险
SELECT * FROM users, orders WHERE users.id = orders.user_id;

-- ✅ 明确 JOIN
SELECT u.name, o.total 
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.created_at > NOW() - INTERVAL '7 days';

-- ✅ 先过滤再 JOIN
SELECT u.name, recent.total
FROM users u
JOIN (SELECT user_id, SUM(amount) as total 
      FROM orders 
      WHERE created_at > NOW() - INTERVAL '7 days'
      GROUP BY user_id) recent ON u.id = recent.user_id;
```

### 3.4 子查询 vs JOIN

```sql
-- ❌ 相关子查询（每行执行一次）
SELECT name, (SELECT COUNT(*) FROM orders WHERE user_id = users.id) as order_count
FROM users;

-- ✅ JOIN + GROUP BY
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- ✅  lateral JOIN（PostgreSQL，复杂场景）
SELECT u.name, recent.order_count
FROM users u
JOIN LATERAL (
    SELECT COUNT(*) as order_count 
    FROM orders WHERE user_id = u.id
) recent ON true;
```

### 3.5 UPSERT 优化

```sql
-- PostgreSQL: INSERT ... ON CONFLICT
INSERT INTO users (email, name) VALUES ('test@example.com', 'Test')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;

-- MySQL: INSERT ... ON DUPLICATE KEY
INSERT INTO users (email, name) VALUES ('test@example.com', 'Test')
ON DUPLICATE KEY UPDATE name = VALUES(name);
```

---

## 四、ORM 优化（SQLAlchemy）

### 4.1 N+1 问题

```python
# ❌ N+1 查询：1次查用户 + N次查订单
users = db.execute(select(User)).scalars().all()
for user in users:
    print(user.orders)  # 每个 user 触发一次查询

# ✅ 预加载（selectin）
users = db.execute(
    select(User).options(selectinload(User.orders))
).scalars().all()

# ✅ 预加载（joined）— 单条 SQL
users = db.execute(
    select(User).options(joinedload(User.orders))
).scalars().all()
```

### 4.2 只查需要的列

```python
# ❌ 查所有列
users = db.execute(select(User)).scalars().all()

# ✅ 只查需要的
user_names = db.execute(select(User.id, User.name)).all()

# ✅ 使用 with_expression 计算字段
from sqlalchemy import case
stmt = select(
    User.name,
    case((User.is_active == True, '活跃'), else_='停用').label('status')
)
```

### 4.3 批量操作

```python
# ❌ 逐条插入
for item in items:
    db.add(Item(**item))
await db.flush()

# ✅ 批量插入
from sqlalchemy import insert
await db.execute(insert(Item), items)

# ✅ 批量更新（SQLAlchemy 2.0）
from sqlalchemy import update
await db.execute(
    update(Item).where(Item.status == 'pending').values(status='processing')
)
```

### 4.4 避免隐式查询

```python
# ❌ 触发额外查询（延迟加载）
user = db.get(User, 1)
print(user.posts)  # 又触发一次查询

# ✅ 明确加载策略
user = db.execute(
    select(User).options(selectinload(User.posts)).where(User.id == 1)
).scalar_one()

# ✅ 或者使用 joinedload
user = db.execute(
    select(User).options(joinedload(User.posts)).where(User.id == 1)
).scalar_one()
```

---

## 五、连接池调优

### 5.1 参数说明

| 参数 | 含义 | 推荐值 |
|------|------|--------|
| `pool_size` | 保持的连接数 | CPU 核心数 × 2 |
| `max_overflow` | 溢出连接数 | pool_size 的 50%-100% |
| `pool_timeout` | 等待连接超时(秒) | 30 |
| `pool_recycle` | 连接回收时间(秒) | 3600（避免数据库端断开） |
| `pool_pre_ping` | 连接前检查活性 | True |

### 5.2 SQLAlchemy 配置

```python
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,           # 保持 20 个连接
    max_overflow=10,        # 最多溢出 10 个
    pool_timeout=30,        # 等待 30 秒
    pool_recycle=3600,      # 1 小时回收
    pool_pre_ping=True,     # 自动重连
    connect_args={
        "command_timeout": 60,  # 查询超时
    },
)
```

### 5.3 监控连接池

```python
# SQLAlchemy 连接池统计
pool = engine.pool
print(f"Size: {pool.size()}")
print(f"Checked in: {pool.checkedin()}")
print(f"Checked out: {pool.checkedout()}")
print(f"Overflow: {pool.overflow()}")
```

---

## 六、锁与并发

### 6.1 死锁诊断

```sql
-- PostgreSQL：查看当前锁
SELECT pid, usename, query, state, wait_event_type, wait_event
FROM pg_stat_activity
WHERE state = 'active' AND wait_event_type = 'Lock';

-- PostgreSQL：查看死锁
SELECT blocked.pid AS blocked_pid,
       blocked.query AS blocked_query,
       blocking.pid AS blocking_pid,
       blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_locks bl ON bl.pid = blocked.pid AND NOT bl.granted
JOIN pg_locks gl ON gl.locktype = bl.locktype AND gl.relation = bl.relation AND gl.granted
JOIN pg_stat_activity blocking ON gl.pid = blocking.pid
WHERE blocked.pid != blocking.pid;

-- MySQL：查看锁等待
SELECT * FROM information_schema.innodb_lock_waits;
```

### 6.2 乐观锁 vs 悲观锁

```python
# 悲观锁（SELECT FOR UPDATE）
async with db.begin():
    result = await db.execute(
        select(Account).where(Account.id == account_id).with_for_update()
    )
    account = result.scalar_one()
    account.balance -= amount

# 乐观锁（版本号）
class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    version: Mapped[int] = mapped_column(Integer, default=0)
    
    __mapper_args__ = {"version_id_col": version}

# 更新时自动检查版本
try:
    account.balance -= amount
    await db.commit()
except OptimisticError:
    # 版本冲突，重试
```

---

## 七、慢查询诊断清单

### 7.1 PostgreSQL

```sql
-- 查看慢查询（需要 pg_stat_statements 扩展）
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT query, calls, total_exec_time / 1000 as total_sec,
       mean_exec_time / 1000 as avg_sec,
       rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- 查看表大小
SELECT relname, 
       pg_size_pretty(pg_total_relation_size(relid)) as total_size,
       pg_size_pretty(pg_relation_size(relid)) as data_size,
       pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as index_size
FROM pg_catalog.pg_statio_all_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 20;

-- 查看缓存命中率
SELECT sum(heap_blks_read) as heap_read,
       sum(heap_blks_hit) as heap_hit,
       round(sum(heap_blks_hit) * 100.0 / (sum(heap_blks_hit) + sum(heap_blks_read)), 2) as hit_ratio
FROM pg_statio_user_tables;
```

### 7.2 MySQL

```sql
-- 慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- 超过1秒记录

-- 查看当前运行的查询
SHOW PROCESSLIST;

-- 查看表状态
SHOW TABLE STATUS LIKE 'users';

-- InnoDB 状态
SHOW ENGINE INNODB STATUS;
```

---

## 八、优化决策树

```
查询慢？
│
├─ EXPLAIN 看了吗？
│  └─ 没看 → 先 EXPLAIN ANALYZE
│
├─ 全表扫描 (Seq Scan / ALL)？
│  ├─ 表很小 (<1000行) → 正常，不用管
│  └─ 表大 → 需要索引
│     ├─ WHERE 条件列 → 加 B-Tree 索引
│     ├─ ORDER BY 列 → 加索引或调整索引顺序
│     └─ JOIN 条件 → 加索引
│
├─ 索引存在但没用到？
│  ├─ 类型不匹配 → 检查隐式转换
│  ├─ 函数包裹 → 用函数索引
│  ├─ OR 条件 → 改 UNION 或分别建索引
│  └─ 统计信息过期 → ANALYZE table
│
├─ 排序慢 (filesort / external merge)？
│  ├─ work_mem 太小 → 增大 work_mem
│  └─ 无索引排序 → 加覆盖索引
│
├─ N+1 查询？
│  └─ 用 selectinload / joinedload
│
└─ 锁等待？
   ├─ 长事务 → 缩短事务范围
   ├─ 死锁 → 统一加锁顺序
   └─ 热点行 → 乐观锁 / 队列化
```

---

## 九、快速参考

| 问题 | 快速方案 |
|------|---------|
| 查询慢 | `EXPLAIN ANALYZE` → 看执行计划 |
| 全表扫描 | 加索引 |
| 索引没生效 | 检查类型匹配、ANALYZE 更新统计 |
| N+1 查询 | `selectinload` / `joinedload` |
| 深分页慢 | 游标分页 `WHERE id > :last` |
| COUNT 慢 | 维护计数表或估算 |
| 连接超时 | 检查连接池配置、增加 pool_size |
| 死锁 | 统一加锁顺序、缩短事务 |
| 写入慢 | 检查索引数量、批量操作 |
| 缓存未命中 | 增大 shared_buffers (PG) / innodb_buffer_pool (MySQL) |

# 事务、隔离级别与锁

> 子技能提到了 MVCC 和隔离级别的名词，但**"我该选哪个隔离级别""这个死锁怎么读"**
> 没有展开。本篇是并发问题的排查手册。

## 一、隔离级别：只需记住两个默认值的差异

| 级别 | 脏读 | 不可重复读 | 幻读 | 谁的默认 |
|------|------|-----------|------|----------|
| Read Uncommitted | 可能 | 可能 | 可能 | 基本没人用 |
| **Read Committed** | 否 | 可能 | 可能 | **PostgreSQL / Oracle / SQL Server** |
| **Repeatable Read** | 否 | 否 | MySQL 用间隙锁基本避免 | **MySQL InnoDB** |
| Serializable | 否 | 否 | 否 | 需要严格正确性时 |

**这个差异会真实咬人**：同一段应用代码，在 MySQL 上事务内两次 SELECT 结果一致，
迁到 PG 上就可能不一致（PG 默认 RC，每条语句取新快照）。跨引擎迁移时必查。

### 怎么选

```
业务能容忍事务内读到别人的新提交吗？
├─ 能（大多数 CRUD）→ Read Committed，并发最好
└─ 不能（如：读余额 → 计算 → 写余额）
   ├─ 读的行数少 → 用 SELECT ... FOR UPDATE 显式加锁（推荐，比提级隔离更精确）
   └─ 涉及范围/聚合一致性 → Repeatable Read 或 Serializable
```

> **优先用显式行锁而不是提升隔离级别。** 提级是全局代价，行锁是局部代价。

## 二、并发写的三种正确姿势

### 1. 悲观锁：先锁后改

```sql
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;   -- 拿排他行锁
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
```

适合：冲突频繁、事务短。
风险：锁等待、死锁。**必须配 `FOR UPDATE NOWAIT` 或 `SKIP LOCKED` 防止无限等待**。

### 2. 乐观锁：版本号校验

```sql
UPDATE accounts SET balance = 900, version = version + 1
WHERE id = 1 AND version = 3;
-- affected_rows = 0 说明被人抢先改了，应用层重试
```

适合：冲突稀少、事务长（如表单编辑）。
必须：应用层实现重试逻辑，否则用户看到的是静默失败。

### 3. 原子操作：能不读就不读

```sql
-- ✅ 最优：不需要事务，不需要锁，数据库内部保证原子
UPDATE accounts SET balance = balance - 100 WHERE id = 1 AND balance >= 100;
-- affected_rows = 0 即余额不足
```

**能用第 3 种就别用前两种。** 大量"并发扣减"场景其实不需要显式事务。

## 三、SKIP LOCKED：队列表的标准解法

用数据库做任务队列时，多个 worker 抢任务的正确写法：

```sql
-- PostgreSQL / MySQL 8.0+ 通用
BEGIN;
SELECT id, payload FROM jobs
WHERE status = 'pending'
ORDER BY created_at
LIMIT 10
FOR UPDATE SKIP LOCKED;          -- 跳过被别人锁住的行，不排队

UPDATE jobs SET status = 'running' WHERE id = ANY($1);
COMMIT;
```

没有 `SKIP LOCKED` 时，10 个 worker 会全部排队等同一行，吞吐等于单 worker。
配合 `index-design.md` 的**部分索引**（`WHERE status='pending'`）效果最佳。

## 四、死锁：怎么读、怎么防

### 读死锁日志

```sql
-- MySQL：最近一次死锁详情
SHOW ENGINE INNODB STATUS\G      -- 看 "LATEST DETECTED DEADLOCK" 段
-- 建议开启持久化：innodb_print_all_deadlocks = ON

-- PostgreSQL：死锁写在服务器日志里
-- 建议配置：log_lock_waits = on, deadlock_timeout = 1s
```

死锁日志的读法：找 **两个事务分别持有什么锁、又在等什么锁**，
交叉点就是加锁顺序不一致的地方。

```
TRANSACTION A: holds lock on row(id=1), waiting for row(id=2)
TRANSACTION B: holds lock on row(id=2), waiting for row(id=1)
                                → 加锁顺序相反，经典 ABBA 死锁
```

### 四条防死锁规则

| 规则 | 说明 |
|------|------|
| **统一加锁顺序** | 所有事务按同一顺序（如按主键升序）访问多行。这条能消灭 80% 的死锁 |
| **缩短事务** | 事务里不做 HTTP 调用、不等用户输入、不做大计算 |
| **减小锁粒度** | 避免范围更新；MySQL RR 下无索引的 UPDATE 会锁全表所有行 |
| **应用层重试** | 死锁是正常现象，不是 bug。捕获死锁错误码后**退避重试**（MySQL 1213 / PG 40P01） |

> **MySQL 特有陷阱**：RR 隔离级别下，`UPDATE t SET x=1 WHERE non_indexed_col=5`
> 会给**扫描过的每一行**加锁——等于锁全表。给 WHERE 列建索引不只是性能问题，
> 更是并发正确性问题。

## 五、锁等待排查

```sql
-- MySQL 8.0：谁在等谁
SELECT r.trx_id AS waiting_trx, r.trx_mysql_thread_id AS waiting_thread,
       LEFT(r.trx_query,80) AS waiting_query,
       b.trx_id AS blocking_trx, b.trx_mysql_thread_id AS blocking_thread,
       LEFT(b.trx_query,80) AS blocking_query
FROM performance_schema.data_lock_waits w
JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_engine_transaction_id
JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_engine_transaction_id;
```

```sql
-- PostgreSQL：阻塞链
SELECT a.pid, a.wait_event_type, a.wait_event,
       pg_blocking_pids(a.pid) AS blocked_by,
       now() - a.query_start AS duration, LEFT(a.query, 80) AS q
FROM pg_stat_activity a
WHERE cardinality(pg_blocking_pids(a.pid)) > 0
ORDER BY duration DESC;

-- 紧急止血（先确认影响面！）
SELECT pg_cancel_backend(<pid>);      -- 温和：取消当前查询
SELECT pg_terminate_backend(<pid>);   -- 强制：断开连接
```

## 六、长事务的连锁伤害（PG 尤其严重）

一个 `idle in transaction` 的连接会导致：

1. 持有的行锁不释放 → 其他事务排队
2. 旧快照不释放 → **autovacuum 无法回收死元组** → 表膨胀 → 全库变慢
3. 复制槽积压 → 从库延迟 → WAL 磁盘涨满

```sql
-- PG：找出 idle in transaction 超过 5 分钟的连接
SELECT pid, now() - state_change AS idle_dur, LEFT(query,80)
FROM pg_stat_activity
WHERE state = 'idle in transaction' AND now() - state_change > interval '5 min';

-- 治本：设置服务端超时（PG 14+）
ALTER SYSTEM SET idle_in_transaction_session_timeout = '60s';
```

**MySQL 对应项**：`SET GLOBAL innodb_lock_wait_timeout = 20;`（默认 50s 偏长）。

## 七、踩坑记录

- **事务里发 HTTP 请求**：外部服务超时 30 秒，锁就持有 30 秒。事务内只做数据库操作。
- **ORM 默认开事务包住整个 Web 请求**：请求里的模板渲染、日志上报全在事务内。改为按需开启。
- **靠 `SELECT` 后 `UPDATE` 实现扣减**：读写之间有窗口，并发下必然超卖。用原子 UPDATE 或 FOR UPDATE。
- **认为死锁是 bug 要彻底消灭**：高并发下死锁不可能为零，正确做法是**降低频率 + 应用层重试**。
- **MySQL 无索引 UPDATE**：RR 下锁全表，测试环境数据少察觉不到，生产直接雪崩。
- **PG 忘了 `idle_in_transaction_session_timeout`**：一个忘记 commit 的连接让表膨胀到 300GB。
- **重试没有退避**：死锁后立即重试会加剧竞争。用指数退避 + 抖动。
- **跨引擎迁移没检查隔离级别**：MySQL(RR) → PG(RC)，事务内二次读结果变了，出现难复现的数据错误。

## 八、检查清单

- [ ] 明确当前隔离级别，跨引擎迁移时已核对差异
- [ ] 并发写用了原子 UPDATE / FOR UPDATE / 版本号三者之一，不是「读-算-写」裸奔
- [ ] 队列表使用 `FOR UPDATE SKIP LOCKED`
- [ ] 多行操作有统一加锁顺序
- [ ] 事务内无 HTTP 调用、无用户交互、无重计算
- [ ] MySQL：所有 UPDATE/DELETE 的 WHERE 列有索引
- [ ] 应用层实现了死锁退避重试
- [ ] PG：已设置 `idle_in_transaction_session_timeout`
- [ ] 死锁日志已开启持久化，便于事后分析

## 相关子技能与层次边界

本 playbook 负责**事务隔离级别、锁与死锁**的决策；不负责 Schema 迁移，见兄弟参考。

- 落地到 [skills/mysql/SKILL.md](../skills/mysql/SKILL.md)：InnoDB 锁类型 / 死锁退避重试。
- 落地到 [skills/postgres-patterns/SKILL.md](../skills/postgres-patterns/SKILL.md)：PG 锁与 idle_in_transaction 超时。
- 落地到 [skills/mongodb-query-optimizer/SKILL.md](../skills/mongodb-query-optimizer/SKILL.md)：MongoDB 多文档事务与单文档原子性边界。
- 兄弟参考：
  - [references/schema-migration.md](schema-migration.md)：在线 DDL 的锁等待。
  - [references/backup-recovery.md](backup-recovery.md)：一致性备份与锁的相互作用。

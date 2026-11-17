# 慢查询分诊

> 从"数据库很慢"到定位根因的**分诊流程**。子技能讲了各引擎的优化手段，
> 本篇讲的是**先查什么、后查什么**——顺序错了会浪费大量时间在错误的方向上。

## 一、先分清三种"慢"

用户报"数据库慢"时，先用 30 秒区分类型，三者的排查路径完全不同：

```
是所有查询都慢，还是特定查询慢？
├─ 所有查询都慢（包括 SELECT 1）
│  → 不是 SQL 问题。查：连接池耗尽 / CPU 打满 / 磁盘 IO 饱和 / 锁等待 / 复制延迟
│  → 走第三节「全局变慢」
├─ 特定查询慢，且一直慢
│  → 走第四节「单条慢查询」，EXPLAIN 是主战场
└─ 特定查询平时快、偶尔慢
   → 最难。查：锁竞争 / 缓存冷热 / 参数嗅探 / 邻居查询挤占资源
   → 走第五节「间歇性慢」
```

**最常见的误诊**：把"全局变慢"当成"单条慢查询"去优化 SQL，优化半天没效果——
真实原因是连接池打满或某个大事务持有锁。

## 二、第一分钟：看现场

先看**当前正在跑什么**，比翻日志快得多。

```sql
-- MySQL：当前活跃会话，按耗时倒序
SELECT id, user, db, command, time, state, LEFT(info, 120) AS sql_text
FROM information_schema.processlist
WHERE command != 'Sleep' ORDER BY time DESC LIMIT 20;

-- MySQL：正在等锁的事务
SELECT * FROM performance_schema.data_lock_waits;
SELECT * FROM information_schema.innodb_trx ORDER BY trx_started LIMIT 10;
```

```sql
-- PostgreSQL：活跃会话 + 等待事件
SELECT pid, now()-query_start AS dur, state, wait_event_type, wait_event,
       LEFT(query,120) AS q
FROM pg_stat_activity
WHERE state != 'idle' ORDER BY dur DESC LIMIT 20;

-- PostgreSQL：谁阻塞了谁
SELECT pid, pg_blocking_pids(pid) AS blocked_by, LEFT(query,80)
FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid)) > 0;
```

```js
// MongoDB：当前操作，只看跑了 3 秒以上的
db.currentOp({ "active": true, "secs_running": { $gte: 3 } })
```

> **`idle in transaction` 是 PG 的头号杀手**：应用开了事务却忘了提交，
> 持有的锁与旧快照会让 vacuum 停摆、表膨胀、其他会话排队。看到就去查应用代码。

## 三、全局变慢：按这个顺序查

| # | 检查 | 命令 | 判据 |
|---|------|------|------|
| 1 | 连接数是否打满 | MySQL `SHOW STATUS LIKE 'Threads_connected'` / PG `SELECT count(*) FROM pg_stat_activity` | 接近 `max_connections` 即为瓶颈 |
| 2 | 是否有长事务 | 见上节 `innodb_trx` / `pg_stat_activity` | 事务 > 60s 需追查 |
| 3 | 锁等待 | `data_lock_waits` / `pg_blocking_pids` | 有阻塞链就先解锁 |
| 4 | 磁盘 IO | `iostat -x 1`，看 `%util` 与 `await` | `%util` > 80% 为饱和 |
| 5 | 缓存命中率 | MySQL Buffer Pool 命中率 / PG `pg_stat_database.blks_hit` | < 95% 说明内存不足 |
| 6 | 复制延迟 | MySQL `SHOW REPLICA STATUS` 的 `Seconds_Behind_Source` / PG `pg_last_xact_replay_timestamp()` | 读库延迟会被误报为"慢" |
| 7 | CPU / 内存 | `top`、`vmstat 1` | 打满则看是查询导致还是外部进程 |

**缓存命中率速查**：

```sql
-- MySQL InnoDB Buffer Pool 命中率
SELECT (1 - Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests) * 100
FROM (SELECT
  MAX(IF(VARIABLE_NAME='Innodb_buffer_pool_reads', VARIABLE_VALUE,0)) AS Innodb_buffer_pool_reads,
  MAX(IF(VARIABLE_NAME='Innodb_buffer_pool_read_requests', VARIABLE_VALUE,0)) AS Innodb_buffer_pool_read_requests
  FROM performance_schema.global_status) t;

-- PostgreSQL 缓存命中率（应 > 0.99）
SELECT sum(blks_hit)::float / nullif(sum(blks_hit)+sum(blks_read),0) FROM pg_stat_database;
```

## 四、单条慢查询：定位 → 分析 → 优化 → 验证

### 定位：找出真正该优化的那条

**按总耗时排序，不是按单次耗时排序。** 一条 5 秒但每天跑 1 次的查询，
远不如一条 50ms 但每秒跑 500 次的重要。

```sql
-- MySQL（需开启 performance_schema）
SELECT DIGEST_TEXT, COUNT_STAR,
       ROUND(SUM_TIMER_WAIT/1e12, 2) AS total_sec,
       ROUND(AVG_TIMER_WAIT/1e9, 2)  AS avg_ms
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10;

-- PostgreSQL（需 pg_stat_statements 扩展）
SELECT LEFT(query,100), calls,
       ROUND(total_exec_time::numeric,0) AS total_ms,
       ROUND(mean_exec_time::numeric,2)  AS mean_ms, rows
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;
```

```js
// MongoDB：开慢查询 profiler（阈值 100ms），排查完记得关
db.setProfilingLevel(1, { slowms: 100 })
db.system.profile.find().sort({ millis: -1 }).limit(10)
```

也可用本仓库脚本直接消化 MySQL 慢日志：

```bash
python3 scripts/slowlog_digest.py /var/log/mysql/slow.log --top 10
```

### 分析

用 `explain_audit.py` 或人工读计划，详见 `explain-reading.md`。

```bash
mysql -e "EXPLAIN FORMAT=JSON SELECT ..." > plan.json
python3 scripts/explain_audit.py plan.json
```

### 优化：按性价比排序，从上往下试

| 顺序 | 手段 | 代价 | 典型收益 |
|------|------|------|----------|
| 1 | 加/改索引 | 低 | 10x–1000x |
| 2 | 改写查询（去 OR、去函数、拆子查询） | 低 | 2x–100x |
| 3 | 减少返回列 / 行（去 `SELECT *`、加 LIMIT） | 低 | 2x–10x |
| 4 | 更新统计信息（ANALYZE） | 极低 | 偶尔 100x |
| 5 | 调参数（work_mem、buffer pool） | 中，影响全局 | 2x–5x |
| 6 | 加缓存层 | 中，引入一致性问题 | 视命中率 |
| 7 | 反范式 / 物化视图 | 高，需维护同步 | 10x+ |
| 8 | 分区 / 分片 | 很高 | 仅解决数据量问题 |

> **别跳级**。见过太多团队在没建索引的情况下直接上 Redis 缓存，
> 结果缓存穿透时数据库照样被打垮。

### 验证

优化前后各跑 3 次，**记录数字**：执行时间、扫描行数、EXPLAIN 关键字段。
只说"感觉快了"不算完成。

## 五、间歇性慢：最难的一类

| 现象 | 可能根因 | 验证方法 |
|------|----------|----------|
| 每天固定时间慢 | 定时任务 / 备份 / 报表批处理 | 对照 cron 与慢日志时间戳 |
| 随机变慢，伴随锁等待 | 并发事务竞争同一批行 | 抓 `data_lock_waits` / `pg_locks` |
| 首次慢、之后快 | 缓存冷启动 | 看 `Buffers: shared read` 是否很大 |
| 同一 SQL 不同参数差异巨大 | 参数嗅探 / 数据倾斜 | 用两组参数分别 EXPLAIN ANALYZE 对比 |
| 逐渐变慢，重启后恢复 | 连接泄漏 / 内存碎片 / 表膨胀 | PG 查 `pg_stat_user_tables.n_dead_tup` |
| 慢在写入 | 索引过多 / 大事务 / redo 刷盘 | 检查表索引数与事务大小 |

**PG 表膨胀速查**：

```sql
SELECT relname, n_live_tup, n_dead_tup,
       ROUND(n_dead_tup::numeric / NULLIF(n_live_tup,0), 3) AS dead_ratio,
       last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000 ORDER BY dead_ratio DESC LIMIT 10;
-- dead_ratio > 0.2 说明 autovacuum 跟不上
```

## 六、踩坑记录

- **只看平均耗时**：平均 20ms 可能藏着 P99 5 秒。要看分位数，不看均值。
- **在从库上排查主库问题**：读写负载与缓存状态完全不同，结论不可迁移。
- **优化了慢日志里的第一条**：慢日志按单次耗时排序，第一条往往是每周跑一次的报表。按**总耗时**排。
- **profiler 开了忘关**：MongoDB `setProfilingLevel(2)` 全量采集会显著拖慢生产。排查完必须关。
- **忽略应用侧 N+1**：单条 SQL 都是 2ms，但一个页面发了 800 条。数据库监控看不出来，得看 APM。
- **改了参数没记录基线**：调完 `work_mem` 却没有调整前的数据，无法证明有效，也无法回滚决策。
- **把复制延迟当慢查询**：读库返回旧数据被误报为"查询没结果"，实际是延迟。先查延迟再查 SQL。

## 七、分诊检查清单

- [ ] 已区分「全局慢 / 单条慢 / 间歇慢」
- [ ] 看过当前活跃会话与锁等待，排除长事务
- [ ] 确认连接数未打满、复制无明显延迟
- [ ] 按**总耗时**而非单次耗时选定优化目标
- [ ] 有优化前的基线数字
- [ ] 优化手段从性价比高的开始，未跳级上缓存/分片
- [ ] 优化后重新测量并记录对比
- [ ] 临时开启的 profiler / general log 已关闭

## 相关子技能与层次边界

本 playbook 负责**慢查询分诊（基线→定位→性价比优化→复测）**；不负责容量规划，见兄弟参考。

- 落地到 [skills/mysql/SKILL.md](../skills/mysql/SKILL.md)：慢查询日志 / Performance Schema 定位。
- 落地到 [skills/postgres-patterns/SKILL.md](../skills/postgres-patterns/SKILL.md)：pg_stat_statements 定位。
- 落地到 [skills/mongodb-query-optimizer/SKILL.md](../skills/mongodb-query-optimizer/SKILL.md)：profiler / 慢查询聚合定位。
- 落地到 [skills/database-observability/SKILL.md](../skills/database-observability/SKILL.md)：监控先发现慢查询，再进分诊。
- 兄弟参考：
  - [references/explain-reading.md](explain-reading.md)：先看执行计划。
  - [references/index-design.md](index-design.md)：缺索引优先补。
- 脚本：
  - [scripts/slowlog_digest.py](../scripts/slowlog_digest.py)：慢日志聚合与基线对比。

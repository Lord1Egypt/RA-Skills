# 连接池与容量规划

> `database-observability` 子技能讲了监控什么指标，本篇讲**这些数字该设成多少**——
> 具体的计算公式与阈值推导，这是子技能里被压缩掉的部分。

## 一、连接池大小：反直觉的公式

**最常见的错误是把连接池调大。** 连接不是越多越好——每个连接在 PG 里是一个进程，
在 MySQL 里是一个线程，超过 CPU 能并行处理的数量后，上下文切换开销会让吞吐**下降**。

```
连接池大小 = ((核心数 × 2) + 有效磁盘数)
```

- 4 核 + SSD（有效磁盘数按 1 算）→ **9**
- 8 核 + SSD → **17**
- 16 核 + SSD → **33**

> 这个公式源自 HikariCP 的实测结论。很多团队把池设成 100+，
> 实测下来把它降到 10 反而 TPS 更高、P99 更低。

### 多实例场景

```
单实例池大小 = 数据库 max_connections × 0.8 / 应用实例数
```

例：`max_connections=200`，10 个应用实例 → 每实例 **16** 个连接（留 20% 给运维与后台任务）。

**必须留余量**：耗尽 `max_connections` 时，你连 `psql` 都连不上去救火。
PG 记得配 `superuser_reserved_connections`（默认 3）。

### 关键超时参数

| 参数 | 建议值 | 说明 |
|------|--------|------|
| `connectionTimeout` | 3–5s | 拿不到连接就快速失败，别让请求堆积 |
| `idleTimeout` | 10 min | 回收空闲连接 |
| `maxLifetime` | 30 min | **必须小于数据库侧的 `wait_timeout`**，否则拿到已被服务端关闭的死连接 |
| `validationTimeout` | 1s | 借出前的存活检查 |

> `maxLifetime` < 数据库 `wait_timeout` 是最容易漏配的一条，症状是间歇性
> "connection reset by peer"，且难以复现。

## 二、外部连接池：什么时候需要

PG 的每连接一进程模型，在连接数多时开销显著。超过 **200 连接**就该上 pgbouncer。

| 模式 | 复用粒度 | 可用性 | 何时用 |
|------|---------|--------|--------|
| `session` | 连接生命周期 | 全功能 | 默认，收益有限 |
| `transaction` | 单个事务 | **不支持 prepared statement / 会话变量 / advisory lock** | 推荐，复用率最高 |
| `statement` | 单条语句 | 不支持多语句事务 | 极少用 |

MySQL 侧对应方案是 ProxySQL，但 MySQL 的线程模型开销较小，需求没 PG 那么迫切。

> **transaction 模式的坑**：应用如果用了 `SET search_path` 或会话级临时表，
> 切到 transaction 模式后会随机失败——因为下一条语句可能落在不同的后端连接上。

## 三、内存参数：按物理内存分配

### MySQL（InnoDB）

| 参数 | 建议 | 说明 |
|------|------|------|
| `innodb_buffer_pool_size` | 物理内存 **50–70%** | 最重要的参数，专用机可到 75% |
| `innodb_log_file_size` | 1–2 GB | 太小导致频繁 checkpoint，写入抖动 |
| `innodb_flush_log_at_trx_commit` | `1` 严格 / `2` 可容忍 1s 数据丢失 | 改成 2 能显著提升写入 TPS |
| `max_connections` | 见第一节推导 | 不要盲目设 1000 |

### PostgreSQL

| 参数 | 建议 | 说明 |
|------|------|------|
| `shared_buffers` | 物理内存 **25%** | 再高收益递减（PG 还依赖 OS page cache） |
| `effective_cache_size` | 物理内存 **50–75%** | 只是给优化器的**提示**，不实际占用内存 |
| `work_mem` | 见下方公式 | **每个排序/哈希节点各用一份，极易超配** |
| `maintenance_work_mem` | 512MB–2GB | 影响 vacuum 与建索引速度 |
| `max_wal_size` | 2–8 GB | 太小导致频繁 checkpoint |

**`work_mem` 的正确算法**（最常被配错的参数）：

```
work_mem = (可用内存 × 0.25) / (max_connections × 平均并发排序节点数)
```

一条复杂查询可能有 5 个排序/哈希节点，各分配一份 `work_mem`。
`work_mem=256MB` × 100 连接 × 5 节点 = 理论上 **128GB** —— OOM 就是这么来的。

**实操建议**：全局设保守值（如 16MB），对个别大查询在会话级临时调高：

```sql
SET LOCAL work_mem = '256MB';   -- 只在当前事务生效
```

## 四、容量规划：三条增长曲线

### 1. 磁盘

```
月增长量 = (今日总量 - 30 天前总量)
预计满盘月数 = (磁盘容量 × 0.8 - 当前用量) / 月增长量
```

留 20% 缓冲。**低于 6 个月就该启动扩容或归档流程**——采购/迁移都需要提前量。

```sql
-- PG：各表体积（含索引）TOP 10
SELECT relname,
       pg_size_pretty(pg_total_relation_size(relid))  AS total,
       pg_size_pretty(pg_relation_size(relid))        AS table_only,
       pg_size_pretty(pg_indexes_size(relid))         AS indexes
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC LIMIT 10;
```

```sql
-- MySQL：各表体积 TOP 10
SELECT table_name,
       ROUND(data_length/1024/1024) AS data_mb,
       ROUND(index_length/1024/1024) AS idx_mb
FROM information_schema.tables
WHERE table_schema = DATABASE()
ORDER BY data_length + index_length DESC LIMIT 10;
```

> **别忘了索引与 WAL/binlog**。索引常占表体积 30%+；binlog 保留 7 天可能又是一份数据量。

### 2. 连接数

看**峰值**而非均值。峰值连接数 / `max_connections` > 0.7 就该规划了。

### 3. QPS 与延迟拐点

数据库容量不是线性的——接近瓶颈时延迟会**指数上升**。
压测找到 P99 开始陡增的那个 QPS，就是真实容量上限，**日常负载应控制在它的 60% 以内**。

## 五、告警阈值参考

分级设置，避免告警疲劳。可直接套用 [assets/db-alert-rules.yml](../assets/db-alert-rules.yml)。

| 指标 | P1（立即处理） | P2（当天处理） | P3（周内跟进） |
|------|---------------|---------------|---------------|
| 磁盘使用率 | > 90% | > 80% | > 70% |
| 连接数占比 | > 90% | > 75% | > 60% |
| 复制延迟 | > 60s | > 10s | > 3s |
| 缓存命中率 | < 90% | < 95% | < 98% |
| 慢查询数/分钟 | > 100 | > 20 | > 5 |
| 死锁数/小时 | > 50 | > 10 | > 1 |
| 最长事务时长 | > 300s | > 60s | > 30s |
| PG 死元组比例 | > 50% | > 30% | > 20% |

**告警收敛原则**：
- 同一根因只发一条（磁盘满会连带触发一堆指标，只报磁盘）
- P3 走日报，不走即时推送
- 每条告警必须附**处置链接**，否则值班人只能干瞪眼

## 六、踩坑记录

- **把连接池调到 200 求性能**：上下文切换开销吃掉全部收益，降到 20 后 P99 反而下降 60%。
- **`work_mem` 设 256MB 全局生效**：并发上来直接 OOM，数据库进程被内核杀掉。
- **`maxLifetime` 大于 `wait_timeout`**：应用间歇性报连接重置，排查数天才发现是超时配置错位。
- **只监控均值不看峰值**：均值连接数 30，峰值 195（上限 200），某天促销直接连接耗尽。
- **磁盘告警设在 95%**：PG 在磁盘满时会拒绝写入甚至无法启动，留给你的处置时间不足 10 分钟。
- **忘了算 binlog / WAL 的空间**：数据只占 40%，binlog 保留策略吃掉另外 40%。
- **pgbouncer 用 transaction 模式但应用依赖会话状态**：prepared statement 随机失败，
  症状极难定位。切模式前先审计应用是否用了会话级特性。
- **扩容后没调 buffer pool**：机器内存从 16G 升到 64G，参数没改，等于白花钱。

## 七、检查清单

- [ ] 连接池按 `(核心数×2)+磁盘数` 计算，不是拍脑袋设的
- [ ] `maxLifetime` < 数据库 `wait_timeout`
- [ ] `max_connections` 留了运维余量（PG 配了 `superuser_reserved_connections`）
- [ ] `work_mem` 按并发节点数核算过，未按单查询需求全局设置
- [ ] `innodb_buffer_pool_size` / `shared_buffers` 与实际物理内存匹配
- [ ] 磁盘增长趋势有 6 个月以上的预测
- [ ] 容量统计包含索引与 binlog/WAL
- [ ] 告警分了 P1/P2/P3，每条附处置链接
- [ ] 压测确定过延迟拐点，日常负载 < 60% 上限

## 相关子技能与层次边界

本 playbook 负责**连接池参数、容量预测与拐点压测**的决策；不负责具体引擎调优，落地由各引擎子技能承接。

- 落地到 [skills/database-observability/SKILL.md](../skills/database-observability/SKILL.md)：容量指标采集、P1/P2/P3 告警与处置链接。
- 落地到 [skills/mysql/SKILL.md](../skills/mysql/SKILL.md)：MySQL 连接池（max_connections / 线程池）与缓冲池容量。
- 落地到 [skills/postgres-patterns/SKILL.md](../skills/postgres-patterns/SKILL.md)：PostgreSQL 连接池（pgBouncer / max_connections）与共享缓冲。
- 落地到 [skills/mongodb-query-optimizer/SKILL.md](../skills/mongodb-query-optimizer/SKILL.md)：MongoDB 连接池与 WT 缓存容量。
- 兄弟参考：
  - [references/backup-recovery.md](backup-recovery.md)：容量含 binlog / WAL 增长。
  - [references/engine-selection.md](engine-selection.md)：容量成本影响选型。
  - [references/slow-query-triage.md](slow-query-triage.md)：容量不足会直接引发慢查询。

# 数据库选型决策

> 子技能各自讲透一个引擎，但**没人告诉你该选哪个**。本篇专补这块：从访问模式倒推引擎，
> 而不是从"哪个流行"正推。

## 一、先否定，再选择

选型最常见的错误是先挑引擎再想需求。正确顺序是先用三个问题**排除**大部分选项：

```
Q1 数据之间有强关联、需要多表事务一致吗？
   是 → 关系型（MySQL / PostgreSQL），MongoDB 出局
   否 → 继续

Q2 查询模式在上线后会频繁变化 / 无法预先枚举吗？
   是 → 关系型（SQL 的 ad-hoc 查询能力不可替代）
   否，只有少数固定查询路径 → 文档型可考虑

Q3 单机能扛住吗？（数据量 < 500GB 且 QPS < 20K）
   能 → 别上分布式，任何单机引擎都行，选团队最熟的
   不能 → 才进入分片 / 分布式讨论
```

**Q3 是最容易被跳过的一步。** 绝大多数独立开发者与小团队的项目，单台 PostgreSQL
就能撑到业务失败为止。为"未来可能的规模"提前上分布式，是最贵的过早优化。

## 二、MySQL vs PostgreSQL

两者都能干活，差异在**默认倾向**而非能力上限。

| 维度 | MySQL | PostgreSQL | 决策含义 |
|------|-------|------------|----------|
| 复杂查询 | 优化器较弱，多表 JOIN / 子查询容易劣化 | 优化器强，CTE、窗口函数、LATERAL 完整 | 报表、分析类查询多 → PG |
| 写入吞吐 | InnoDB 聚簇索引，主键顺序写很快 | 堆表 + MVCC，UPDATE 产生死元组需 vacuum | 高频 UPDATE 同一行 → MySQL 略优 |
| 索引类型 | 基本只有 B-Tree（+全文） | B-Tree/Hash/GIN/GiST/BRIN/部分/表达式 | JSON、数组、地理、向量 → PG |
| 扩展生态 | 插件少 | PostGIS、pgvector、pg_cron、TimescaleDB | 地理 / 向量检索 → PG（几乎无对手） |
| 复制运维 | 主从成熟，工具链丰富（pt-*、gh-ost） | 逻辑复制较新，大版本升级痛 | 运维人力薄 → MySQL 生态更省心 |
| 托管服务 | 到处都有，便宜 | 到处都有，Supabase/Neon 体验好 | 平手 |

**实操结论**：

- 没有明确理由时选 **PostgreSQL**——它的能力上界更高，且你不会因为选它而在简单场景吃亏。
- 已有 MySQL 运维经验 / 团队栈是 MySQL → 留在 MySQL，迁移成本远大于收益。
- 需要 **pgvector 做 RAG** 或 **PostGIS 做地理** → 直接 PG，不用比。

## 三、什么时候真的该用 MongoDB

MongoDB 被误用的比例极高。它成立的条件很窄：

✅ **适合**：
- 文档结构天然嵌套且**整体读写**（如 CMS 页面、商品详情、配置快照）
- Schema 在不同租户/品类间差异大，关系型要建几十个稀疏列或 EAV
- 写入量大且允许最终一致（日志、埋点、IoT 时序）

❌ **不适合**（这些场景选 MongoDB 后期一定翻车）：
- 需要跨集合事务与外键一致性（订单-库存-账务）
- 查询维度多变，需要任意组合筛选与聚合报表
- 团队没人愿意维护索引——MongoDB 缺索引的退化比 SQL 更陡

> 判据：**如果你正在 MongoDB 里用 `$lookup` 模拟 JOIN，说明选错了引擎。**

## 四、别忘了 SQLite

单机应用、CLI 工具、桌面端、边缘设备、甚至中小流量 Web 服务（配 WAL 模式）：
SQLite 是被严重低估的默认选项。零运维、零网络延迟、单文件备份。

放弃 SQLite 的信号：需要多机并发写入、需要网络访问控制、单库 > 100GB。

## 五、混用的代价

"用 PG 存业务 + Redis 做缓存 + MongoDB 存日志 + ES 做搜索" —— 每加一个引擎，
你就多一套备份、监控、故障预案、数据一致性问题和一门要学的调优知识。

**小团队的经验值**：引擎数量 ≤ 2。PostgreSQL 一个引擎就能覆盖
JSON 文档（JSONB）、全文搜索（tsvector）、向量（pgvector）、队列（SKIP LOCKED）、
定时任务（pg_cron），先把它用到极限再考虑加第二个。

## 六、踩坑记录

- **用 MongoDB 存强关系数据**：初期开发快，半年后为了做报表被迫写 ETL 同步到 PG，等于维护两套。
- **一上来就分库分表**：分片键选错比不分片更致命，且跨片查询与事务的复杂度是指数级的。
  正确顺序：单机优化 → 读写分离 → 垂直拆分 → 才是水平分片。
- **用 MySQL 的 `utf8`**：它是 3 字节的假 UTF-8，存不了 emoji。永远用 `utf8mb4`。
- **PG 大版本升级没预演**：逻辑复制/pg_upgrade 都需要停机窗口，上生产前必须演练一次。
- **拿 Benchmark 选型**：厂商 benchmark 与你的访问模式无关。要测就用自己的真实查询集测。

## 七、选型检查清单

- [ ] 写下 Top 5 真实查询（不是想象的），确认候选引擎都能高效支持
- [ ] 估算 1 年后的数据量与 QPS，确认单机够用（不够才谈分布式）
- [ ] 确认是否需要跨实体事务；需要则排除文档型
- [ ] 确认团队有人能在半夜排查这个引擎的故障
- [ ] 确认托管方案与备份恢复路径（**恢复演练过才算数**）
- [ ] 确认引擎总数 ≤ 2

## 相关子技能与层次边界

本 playbook 负责**关系型 vs 文档型 vs 其他引擎**的选型决策；不负责单引擎内部实现，落地由对应子技能承接。

- 落地到 [skills/mysql/SKILL.md](../skills/mysql/SKILL.md)：选 MySQL 后的具体能力与迁移边界。
- 落地到 [skills/postgres-patterns/SKILL.md](../skills/postgres-patterns/SKILL.md)：选 PostgreSQL 后的扩展生态与高级模式。
- 落地到 [skills/mongodb-query-optimizer/SKILL.md](../skills/mongodb-query-optimizer/SKILL.md)：选 MongoDB 后的文档模型与查询优化。
- 落地到 [skills/database-observability/SKILL.md](../skills/database-observability/SKILL.md)：各引擎可观测性成本与指标差异。
- 兄弟参考：
  - [references/backup-recovery.md](backup-recovery.md)：恢复演练过才算数。
  - [references/capacity-and-pooling.md](capacity-and-pooling.md)：容量预测决定托管成本。

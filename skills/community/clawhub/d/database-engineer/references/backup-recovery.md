# 备份与恢复

> 没有任何子技能覆盖这块，但它是数据库工作里**唯一不可挽回**的失败点。
> 索引建错可以重建，查询慢可以优化，数据丢了就是丢了。

## 一、先定义目标，再选方案

两个指标决定一切，**必须先和业务确认数字**，不能由工程师自己假设：

| 指标 | 含义 | 提问方式 |
|------|------|----------|
| **RPO**（恢复点目标） | 能接受丢多少数据 | "系统崩了，丢最近 5 分钟的订单可以吗？" |
| **RTO**（恢复时间目标） | 能接受停多久 | "完全不可用 2 小时，业务能撑住吗？" |

```
RPO = 24h  → 每日全量备份即可
RPO = 1h   → 全量 + 每小时增量
RPO < 5min → 必须开 binlog/WAL 归档做 PITR
RPO ≈ 0    → 同步复制 + 多副本（成本显著上升）

RTO > 4h   → 从备份文件恢复即可
RTO < 1h   → 需要热备实例
RTO < 5min → 需要自动故障切换
```

> 大多数小团队的真实答案是 **RPO 1 小时、RTO 4 小时**——比想象的宽松。
> 别在没问业务的情况下自己上多活架构。

## 二、三种备份类型

| 类型 | MySQL | PostgreSQL | 恢复速度 | 特点 |
|------|-------|------------|---------|------|
| **逻辑备份** | `mysqldump` / `mydumper` | `pg_dump` / `pg_dumpall` | 慢 | 可读、可跨版本、可选表恢复 |
| **物理备份** | `xtrabackup` | `pg_basebackup` | 快 | 体积大、版本绑定 |
| **PITR** | binlog + 全量 | WAL 归档 + 全量 | 中 | 可恢复到任意时间点 |

**小团队推荐组合**：每日物理/逻辑全量 + 持续 WAL/binlog 归档。
这套能覆盖 95% 的场景，成本可控。

### 常用命令

```bash
# PostgreSQL 逻辑备份（自定义格式，支持并行恢复与选表）
pg_dump -Fc -Z6 -d mydb -f mydb_$(date +%F).dump
pg_restore -d mydb -j 4 mydb_2026-08-07.dump        # -j 并行

# PostgreSQL 物理备份
pg_basebackup -D /backup/base -Ft -z -P -X stream

# MySQL 逻辑备份（务必带这三个参数）
mysqldump --single-transaction --routines --triggers \
          --source-data=2 mydb | gzip > mydb_$(date +%F).sql.gz

# MySQL 物理备份
xtrabackup --backup --target-dir=/backup/base
xtrabackup --prepare --target-dir=/backup/base       # 恢复前必须 prepare
```

> `--single-transaction` 是 MySQL 逻辑备份的**必需参数**：不加会锁表。
> 但它只对 InnoDB 有效，MyISAM 表仍会被锁。

## 三、PITR：恢复到误操作前的那一秒

最常见的真实事故不是硬盘坏了，是**有人执行了不带 WHERE 的 DELETE**。
PITR 是唯一能救回来的手段。

### PostgreSQL

```bash
# 前置：postgresql.conf 开启归档
# wal_level = replica
# archive_mode = on
# archive_command = 'test ! -f /archive/%f && cp %p /archive/%f'

# 恢复：解压全量备份后，在数据目录创建 recovery.signal
cat > $PGDATA/postgresql.auto.conf <<'EOF'
restore_command = 'cp /archive/%f %p'
recovery_target_time = '2026-08-07 03:42:00'
recovery_target_action = 'promote'
EOF
touch $PGDATA/recovery.signal
pg_ctl start
```

### MySQL

```bash
# 前置：my.cnf 中 log_bin = ON, binlog_format = ROW

# 1. 恢复全量备份
# 2. 重放 binlog 到误操作前的时间点
mysqlbinlog --start-datetime="2026-08-07 00:00:00" \
            --stop-datetime="2026-08-07 03:42:00" \
            mysql-bin.0000{12,13,14} | mysql -u root -p
```

**关键前提**：`binlog_format = ROW`。用 `STATEMENT` 格式时，
含 `NOW()`、`RAND()` 的语句重放结果与原始执行不一致。

## 四、恢复演练：没演练过的备份不算备份

这是整篇最重要的一节。**备份成功 ≠ 能恢复**。真实遇到过的失败：

- 备份文件损坏，但每天的"备份成功"邮件照常发送
- 备份里少了 `--routines`，存储过程和触发器全丢
- 恢复需要的密钥/证书没备份，加密的备份打不开
- 恢复耗时 14 小时，远超 RTO 承诺的 2 小时
- 备份和数据库在**同一台机器/同一个可用区**，机器挂了两者一起没
- 恢复脚本引用了已被删除的老路径

### 演练清单（建议季度执行）

可直接复制 [assets/backup-runbook.md](../assets/backup-runbook.md) 作为演练记录模板——它把每一步的耗时、
校验口径和复盘表都固定下来了，避免演练做成"能启动就算过"。

```bash
# 1. 从备份恢复到一台干净的机器（不是生产！）
# 2. 记录实际耗时，与 RTO 目标对比
# 3. 校验数据完整性
```

```sql
-- 行数抽样对比
SELECT 'orders' t, count(*) FROM orders
UNION ALL SELECT 'users', count(*) FROM users;

-- 校验和对比（PG）
SELECT md5(string_agg(id::text || amount::text, '' ORDER BY id)) FROM orders;

-- 确认对象数量：表、索引、约束、存储过程都在
SELECT count(*) FROM information_schema.tables  WHERE table_schema='public';
SELECT count(*) FROM information_schema.routines WHERE routine_schema='public';
```

## 五、3-2-1 原则

```
3 份数据副本
2 种不同介质/存储
1 份异地（不同可用区或不同云）
```

再加一条现代补充：**1 份不可变（immutable）**。
勒索软件会主动删除备份，对象存储要开 **版本控制 + 对象锁定**，
且备份账号只有写权限、没有删除权限。

## 六、踩坑记录

- **只备份不演练**：事故时才发现备份文件是 0 字节，且已连续 8 个月如此。
- **备份和数据库同机**：磁盘故障时一起丢。
- **`mysqldump` 不加 `--single-transaction`**：备份期间锁表，业务中断。
- **忘了备份用户与权限**：PG 的 `pg_dump` 不含角色，需要额外 `pg_dumpall --globals-only`。
- **备份未加密就传到对象存储**：包含用户手机号、身份证的库直接暴露。
- **binlog 保留期太短**：只留 3 天，周五发现周一的误删已无法 PITR。
- **恢复时直接覆盖生产**：应先恢复到独立实例校验，确认无误再切流量。
- **没监控备份任务本身**：cron 静默失败，无人察觉。备份任务必须有**成功心跳告警**
  ——不是失败才报警，是**该成功却没成功**要报警。
- **保留策略只看天数不看容量**：备份把磁盘占满，反过来拖垮数据库。

## 七、检查清单

- [ ] RPO / RTO 已与业务确认，有明确数字
- [ ] 备份策略与 RPO 匹配（需要 PITR 就必须开归档）
- [ ] MySQL：`--single-transaction` + `--routines` + `--triggers`
- [ ] PostgreSQL：另外备份了 `--globals-only`（角色与权限）
- [ ] 备份已加密，密钥单独保管且**密钥本身也有备份**
- [ ] 满足 3-2-1，异地副本存在
- [ ] 对象存储开启版本控制与对象锁定，备份账号无删除权限
- [ ] **季度恢复演练**已执行，记录了实际耗时并对比 RTO
- [ ] 恢复后做过行数/校验和/对象数量三项校验
- [ ] 备份任务有成功心跳监控（缺失即告警）
- [ ] binlog / WAL 保留期 ≥ 备份周期 × 2

## 相关子技能与层次边界

本 playbook 负责**备份策略、恢复演练与保留期**的决策；不负责具体引擎的高可用部署，落地由各引擎子技能承接。

- 落地到 [skills/mysql/SKILL.md](../skills/mysql/SKILL.md)：MySQL 的 mysqldump / xtrabackup / binlog 恢复路径。
- 落地到 [skills/postgres-patterns/SKILL.md](../skills/postgres-patterns/SKILL.md)：PostgreSQL 的 pg_dump / 物理备份 / WAL 归档恢复。
- 落地到 [skills/mongodb-query-optimizer/SKILL.md](../skills/mongodb-query-optimizer/SKILL.md)：MongoDB 的 mongodump / 副本集一致性快照。
- 落地到 [skills/database-observability/SKILL.md](../skills/database-observability/SKILL.md)：备份任务成功心跳监控与恢复校验指标。
- 兄弟参考：
  - [references/schema-migration.md](schema-migration.md)：迁移前先确认可回滚备份。
  - [references/engine-selection.md](engine-selection.md)：选型时已确认恢复路径（恢复演练过才算数）。
  - [references/capacity-and-pooling.md](capacity-and-pooling.md)：保留期与磁盘容量耦合。

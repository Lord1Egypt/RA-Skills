# Schema 变更与零停机迁移

> 子技能里完全没有覆盖的一块：**改表结构不出事故**。这是数据库工作中风险最高的操作，
> 一次错误的 ALTER 能锁死生产库几小时。

## 一、核心模式：扩展-收缩（Expand-Contract）

任何破坏性变更都拆成三个可独立回滚的阶段，**每阶段之间要发一次版本**：

```
阶段 1 扩展 Expand    加新结构，新旧并存，旧代码仍能跑
        ↓ 发版：应用同时写新旧
阶段 2 迁移 Migrate   回填历史数据，切换读路径到新结构
        ↓ 发版：应用只读写新
阶段 3 收缩 Contract  删除旧结构
```

### 例：把 `users.name` 拆成 `first_name` / `last_name`

| 阶段 | 数据库动作 | 应用动作 | 可回滚性 |
|------|-----------|----------|----------|
| 1 | `ADD COLUMN first_name, last_name`（可空） | 写入时双写新旧列 | ✅ 直接回滚应用 |
| 2 | 分批回填历史行 | 读切换到新列，仍双写 | ✅ 读切回旧列 |
| 3 | `DROP COLUMN name` | 停止写旧列 | ⚠️ 不可逆，需备份 |

**绝不能做的**：一次发版里同时改表结构和应用代码。部署有时间差，
这个窗口内新旧代码会同时访问数据库，必然有一边报错。

## 二、危险操作对照表

| 操作 | MySQL 8.0 (InnoDB) | PostgreSQL | 备注 |
|------|-------------------|------------|------|
| 加可空列无默认值 | ✅ INSTANT | ✅ 秒级 | 安全 |
| 加列带默认值 | ✅ INSTANT (8.0.12+) | ✅ 秒级 (11+) | 老版本会重写全表 |
| 加 NOT NULL 列 | ⚠️ 需默认值 | ⚠️ 需默认值 | 无默认值会扫全表校验 |
| 删列 | ⚠️ INPLACE，重建表 | ✅ 秒级（仅标记） | PG 只是标记，空间靠 vacuum 回收 |
| 改列类型（扩容 如 INT→BIGINT） | ❌ 重建表 | ❌ 重写全表 + 排他锁 | **大表必须用在线工具** |
| 改列名 | ✅ INSTANT (8.0) | ✅ 秒级 | 但会破坏旧代码 |
| 加索引 | ✅ ONLINE | ✅ 需 `CONCURRENTLY` | PG 不加 CONCURRENTLY 会锁写 |
| 加外键 | ⚠️ 校验全表 | ⚠️ 校验全表 | PG 可用 `NOT VALID` 分两步 |
| 加 CHECK 约束 | ⚠️ 校验全表 | ✅ `NOT VALID` 后 `VALIDATE` | PG 有优雅方案 |

> **判断依据**：MySQL 用 `ALTER TABLE ... , ALGORITHM=INPLACE, LOCK=NONE` 试跑，
> 报错就说明该操作不支持在线执行，必须换工具。

## 三、PostgreSQL 的两个救命语法

### CONCURRENTLY 建索引

```sql
-- ❌ 锁表写入，大表可能锁十几分钟
CREATE INDEX idx_orders_created ON orders (created_at);

-- ✅ 不阻塞读写（代价：耗时约 2 倍，需两次扫表）
CREATE INDEX CONCURRENTLY idx_orders_created ON orders (created_at);
```

⚠️ `CONCURRENTLY` **不能在事务块内执行**，且失败会留下 `INVALID` 索引，需手动清理：

```sql
SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;
DROP INDEX CONCURRENTLY <invalid_index>;
```

### NOT VALID 分两步加约束

```sql
-- 步骤 1：立即生效于新数据，不校验存量（秒级，只取短锁）
ALTER TABLE orders ADD CONSTRAINT fk_user
  FOREIGN KEY (user_id) REFERENCES users(id) NOT VALID;

-- 步骤 2：后台校验存量数据（只取 SHARE UPDATE EXCLUSIVE，不阻塞读写）
ALTER TABLE orders VALIDATE CONSTRAINT fk_user;
```

### 锁超时护栏（PG 上线脚本必备）

```sql
SET lock_timeout = '3s';        -- 拿不到锁就放弃，不排队
SET statement_timeout = '30s';
ALTER TABLE orders ADD COLUMN note text;
```

**为什么必须加**：PG 的 ACCESS EXCLUSIVE 锁请求会**排在等待队列前面**，
它自己等锁的同时会阻塞后续所有查询——一个等 10 分钟的 ALTER 能让整个表不可用 10 分钟。
`lock_timeout` 把这个风险从"雪崩"降级为"重试"。

## 四、MySQL 大表在线 DDL 工具

原生 ONLINE DDL 覆盖不了的操作（改类型、加主键等），用影子表方案：

```bash
# gh-ost（推荐：无触发器，基于 binlog，可暂停/限流）
gh-ost --host=127.0.0.1 --database=shop --table=orders \
  --alter="MODIFY id BIGINT NOT NULL AUTO_INCREMENT" \
  --max-load=Threads_running=25 \
  --critical-load=Threads_running=100 \
  --chunk-size=1000 \
  --initially-drop-ghost-table \
  --execute

# pt-online-schema-change（基于触发器，写入放大更明显）
pt-online-schema-change --alter "ADD INDEX idx_created (created_at)" \
  D=shop,t=orders --execute --max-load Threads_running=25
```

**共同前提**：表必须有**主键或唯一非空索引**，否则两个工具都无法工作。

## 五、数据回填：永远分批

```sql
-- ❌ 一条 UPDATE 更新 500 万行：长事务、锁膨胀、复制延迟、回滚段爆炸
UPDATE orders SET tenant_id = 1 WHERE tenant_id IS NULL;

-- ✅ 分批，每批独立提交，批间留喘息
UPDATE orders SET tenant_id = 1
WHERE id IN (SELECT id FROM orders WHERE tenant_id IS NULL LIMIT 5000);
-- 循环执行直到 affected_rows = 0，每批之间 sleep 0.1s
```

批大小经验值：**1000–10000 行**，让单批控制在 1 秒内完成。
批太小则总耗时过长，批太大则锁持有时间过长、复制延迟飙升。

回填期间盯住两个指标：**复制延迟** 与 **锁等待数**。任一超阈值就降速或暂停。

## 六、迁移前必做

| # | 事项 | 为什么 |
|---|------|--------|
| 1 | **在生产数据量的副本上演练** | 空表上 ALTER 永远是秒级，测不出真实耗时 |
| 2 | 备份 + **验证恢复可行** | 没恢复演练过的备份等于没有备份 |
| 3 | 写好回滚脚本 | 出事时不能现写 |
| 4 | 估算耗时与锁窗口 | 决定是否需要低峰期执行 |
| 5 | 确认磁盘余量 ≥ 表体积 × 2 | 重建表方案需要双份空间 |
| 6 | 通知相关方 + 准备降级开关 | 超时能快速止损 |

**耗时估算经验**：InnoDB 重建表约 **1–2 GB/分钟**（SSD、无并发压力）。
100GB 的表就是 1–2 小时——这个数字必须在动手前算出来。

## 七、踩坑记录

- **PG 加索引忘了 CONCURRENTLY**：生产直接锁写，事故经典款。
- **MySQL 老版本加带默认值的列**：8.0.12 之前会重写整表，5.7 上一条 `ADD COLUMN ... DEFAULT`
  能锁半小时。上线前先确认版本。
- **在事务里跑 CONCURRENTLY**：直接报错，且很多 ORM 迁移框架默认包事务，需显式关闭。
- **回填没分批**：500 万行一条 UPDATE，从库延迟 40 分钟，读库全部返回旧数据。
- **DROP COLUMN 太早**：应用还有实例在写旧列，收缩阶段至少等一个完整发版周期 + 观察期。
- **改列类型时忘了外键引用**：`INT → BIGINT` 必须同时改所有引用它的外键列，否则关联失败。
- **迁移脚本不幂等**：中途失败后重跑，重复插入或重复加列报错。所有 DDL 加 `IF NOT EXISTS`，
  回填用 `WHERE 目标列 IS NULL` 天然幂等。
- **依赖 ORM 自动迁移上生产**：ORM 生成的 DDL 不带 `CONCURRENTLY`、不分批、不设 lock_timeout。
  生产迁移必须人工审阅生成的 SQL。

## 八、上线检查清单

完整版（含风险等级与评审结论表格）见 [assets/schema-review-checklist.md](../assets/schema-review-checklist.md)。
迁移脚本进评审前先过一遍静态检查，退出码非 0 不进人工评审：

```bash
python3 scripts/schema_lint.py migrations/ --dialect auto --strict
```

- [ ] 变更已拆成扩展-收缩三阶段，每阶段独立发版
- [ ] 在生产量级副本上演练过，记录了实际耗时
- [ ] 备份已完成且**恢复演练通过**
- [ ] 回滚脚本已写好并测试
- [ ] PG：建索引用了 `CONCURRENTLY`，约束用了 `NOT VALID` 两步法
- [ ] PG：脚本头部设置了 `lock_timeout`
- [ ] MySQL：确认原生 ONLINE DDL 是否支持，否则准备 gh-ost
- [ ] 回填分批（1000–10000 行/批）且幂等
- [ ] 磁盘余量 ≥ 表体积 × 2
- [ ] 执行期间监控复制延迟与锁等待，有降速/中止预案

## 相关子技能与层次边界

本 playbook 负责**零停机 Schema 变更与回填**的决策；不负责备份本身，迁移前先备。

- 落地到 [skills/mysql/SKILL.md](../skills/mysql/SKILL.md)：原生 ONLINE DDL vs gh-ost 选择。
- 落地到 [skills/postgres-patterns/SKILL.md](../skills/postgres-patterns/SKILL.md)：CONCURRENTLY 建索引 / 扩展迁移。
- 落地到 [skills/mongodb-query-optimizer/SKILL.md](../skills/mongodb-query-optimizer/SKILL.md)：文档结构演进与兼容性。
- 兄弟参考：
  - [references/transactions-locking.md](transactions-locking.md)：在线 DDL 的锁等待与降速预案。
  - [references/backup-recovery.md](backup-recovery.md)：执行前确认可回滚备份。
  - [references/index-design.md](index-design.md)：迁移常伴随索引调整。
- 脚本：
  - [scripts/schema_lint.py](../scripts/schema_lint.py)：迁移前后校验 schema 结构与命名规范。

# Schema / 索引 变更评审清单

> 配套 [references/index-design.md](../references/index-design.md) 与 [references/schema-migration.md](../references/schema-migration.md)。
> 贴进 MR 模板或工单模板里用。**能被脚本自动检查的项已标注**，
> 先跑脚本再人工评审，把人的注意力留给脚本查不了的部分。

```bash
# 自动检查（零依赖，CI 可直接接）
python3 scripts/schema_lint.py migrations/V42__add_orders.sql --dialect postgres --strict
```

---

## A. 表结构设计（新建表 / 加列）

- [ ] **有主键**，且不是"业务字段凑出来的伪主键" `[脚本 S001]`
- [ ] 主键类型能撑住预期数据量：INT 上限 21 亿，写入量大的表直接用 BIGINT `[脚本 S012]`
- [ ] 金额/精确小数用 `DECIMAL`，**没有用 FLOAT/DOUBLE** `[脚本 S002]`
- [ ] MySQL 字符集是 `utf8mb4` 而非 `utf8`（后者存不下 emoji 与部分汉字）`[脚本 S003]`
- [ ] 时间列用 `DATETIME`/`TIMESTAMPTZ`，**没有用会在 2038 年溢出的 `TIMESTAMP`** `[脚本 S007]`
- [ ] 有 `created_at`（排障和数据修复时缺了它会非常痛苦）`[脚本 S006]`
- [ ] 列数没有失控（> 40 列通常意味着该拆表）`[脚本 S009]`
- [ ] 变长字段长度是想过的，不是一律 `VARCHAR(255)` `[脚本 S005]`
- [ ] 枚举值用编码 + 应用层字典，**没有用数据库 ENUM**（改值要 DDL）`[脚本 S010]`
- [ ] 大对象（TEXT/BLOB/JSON）数量克制，考虑拆到副表或对象存储 `[脚本 S008]`
- [ ] 可空性是设计出来的：能 NOT NULL 就 NOT NULL，NULL 会让索引和聚合行为反直觉
- [ ] 命名符合团队规范（单复数、下划线、缩写表）——脚本管不了，人工看

## B. 索引

- [ ] 新增索引的列顺序遵循 **ESR**（等值 → 排序 → 范围），见 `index-design.md`
- [ ] **不是**为单个查询临时加索引，而是能覆盖一类查询
- [ ] 检查过是否与已有索引冗余（前缀相同的复合索引只留最长的那条）
- [ ] 外键列有索引（PG 不自动建，删父行会全表扫）`[脚本 S004]`
- [ ] 评估过写入代价：这张表的写 QPS 是多少？每加一个索引写入成本增加多少？
- [ ] 大表建索引使用了在线方式：PG `CREATE INDEX CONCURRENTLY` / MySQL `ALGORITHM=INPLACE` 或 gh-ost
- [ ] 附上了 **变更前后的 EXPLAIN 对比**（这是评审最有说服力的材料）

```bash
python3 scripts/explain_audit.py plan_before.json
python3 scripts/explain_audit.py plan_after.json
```

## C. 迁移安全性（改动已有表时必查）

- [ ] 查过 `schema-migration.md` 的**危险操作对照表**，确认本次操作在当前版本下不锁表
- [ ] 遵循**扩展-收缩**：加列/加索引与删列/删表**不在同一个发布**里
- [ ] 新列**可空或有默认值**，老版本应用代码写入不会失败（向后兼容）
- [ ] 数据回填**分批**执行，单批 ≤ 1000~5000 行并带 sleep，不是一条 UPDATE 打全表
- [ ] 脚本**可重入**：中断后重跑不会产生重复数据或报错
- [ ] 设置了锁超时护栏（PG：`SET lock_timeout = '3s'`），避免排队阻塞所有后续查询
- [ ] **有回滚方案**，且回滚方案本身也被评审过（"回滚就是把列删了"通常是错的——数据没了）
- [ ] 预估了执行时长与影响面，选在低峰期，并告知了值班

## D. 上线后

- [ ] 观察窗口内盯了慢查询数、复制延迟、连接数三个指标
- [ ] 复制延迟没有因为 DDL/回填而累积（从库单线程回放是常见瓶颈）
- [ ] 确认新索引**真的被用上了**（`pg_stat_user_indexes.idx_scan` / MySQL `sys.schema_unused_indexes`）
- [ ] 收缩阶段（删旧列/旧索引）已排期，没有变成永久的技术债

---

## 评审结论

| 项 | 内容 |
|----|------|
| 变更单号 / MR | |
| 目标表 & 预估行数 | |
| `schema_lint.py --strict` 退出码 | |
| EXPLAIN 前后对比已附 | 是 / 否 / 不适用 |
| 风险等级 | 低 / 中 / 高 |
| 结论 | 通过 / 需修改后重审 |
| 评审人 | |

> **一票否决项**：无主键、金额用浮点、大表非在线 DDL、无回滚方案。
> 命中任意一条直接打回，不进入讨论环节。

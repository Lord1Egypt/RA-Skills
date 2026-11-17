# JPA / Hibernate 数据访问规范（Java 栈共用）

适用：Spring Data JPA 与 Quarkus Hibernate ORM/Panache 共用的 ORM 纪律。
语言层规范见对应栈文件（backend-java-spring.md / backend-quarkus.md）。

## 1. 实体建模

- 实体是纯数据 + 少量不变量保护，不写业务流程；业务在 service。
- 字段访问模式（field access）统一；禁止 public 字段。
- 关联默认 `FetchType.LAZY`；`@ManyToOne`/`@OneToOne` 显式写 LAZY（JPA 默认 EAGER 是坑）。
- `@OneToOne` 反向端（无外键侧）慎用，N+1 重灾区；确需时 `@MapsId` 或改单向。
- 关联集合用 `List` 禁止 `Set`+`@OneToMany(cascade=ALL)` 的隐式全级联；
  级联只用于真正的聚合根内（Order→OrderItem），跨聚合禁止级联。
- 实体禁用 `equals/hashCode` 基于可变字段（id 或业务键，代理安全写法）。

## 2. 事务与会话

- **关闭 open-session-in-view**（Spring：`spring.jpa.open-in-view=false`）；
  OSIV 掩盖 N+1 与事务边界，一律关。
- 事务边界在 service；controller 不开事务，repository 不嵌套开事务。
- `@Transactional(readOnly = true)` 只读路径标注（Hibernate 只读优化 + 驱动只读路由）。
- 事务内禁止远程调用与耗时 IO；需要"事务提交后"动作用事务事件/钩子。

## 3. 查询纪律

- N+1 防护：列表场景关联数据用 `@EntityGraph` / `fetch join`（JPQL `join fetch`）显式预取；
  Pageable + fetch join 冲突时分两查（先 id 分页再 in 预取）。
- 动态查询：Spring 用 Specification，Quarkus 用 Panache `find("#query", params)`
  命名参数；禁止字符串拼接 JPQL/SQL（注入面）。
- DTO 投影优先：列表/报表端点直接 JPQL 构造 DTO（`select new XxxDto(...)`），
  不拉实体再转换。
- native SQL 仅在 JPQL 表达不了时使用，命名参数写法，集中存放可审查。

## 4. 乐观锁与审计

- 并发更新实体加 `@Version`（Long/Instant）；捕获 `OptimisticLockException` 映射 409。
- 审计字段 `createdAt`/`updatedAt`：Spring 用 Auditing（`@CreatedDate`），
  Quarkus 用 `@PrePersist`/`@PreUpdate`；应用层不可篡改。
- 逻辑删除 `deletedAt` 过滤：Hibernate `@Filter`/`@Where` 统一注入，
  禁止每个查询手写 `and deleted_at is null`。

## 5. 分页与性能

- 分页走 `Pageable`/`Panache.find(...).page(...)`；深分页改游标（`where id > :cursor`）。
- 批量写入 `JDBC batch`（`hibernate.jdbc.batch_size` 50+，`order_inserts/updates`）；
  大批量走原生批处理，不逐条 save。
- 二级缓存默认不用；确有热点证据再开，且只对读多写少的字典类实体。
- 每个列表端点查询必须能 EXPLAIN（SQL 日志 `hibernate.show_sql` 仅 dev 开）。

## 6. Schema 管理

- DDL 策略：**validate**（校验不生成）+ Flyway/Liquibase 管理迁移；
  禁止 `update`/`create` 进生产。
- 迁移脚本与实体变更同一 PR 内配套交付（迁移先行，实体后改）；
  建模命名约定遵循 `standards/database.md`。

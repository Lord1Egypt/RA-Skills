# GraphQL API 规范（架构师/后端工程师共用）

适用：GraphQL 与 REST 并存时的专用纪律。**REST 是默认风格**（standards/api-design.md）；
采用 GraphQL 必须先过 ADR：客户端驱动按需取数、多源聚合网关、字段级演进三类场景才立项。
同一资源双轨暴露（REST + GraphQL）需 ADR 说明并存边界与退役计划。

## 1. Schema 设计

- Schema-first：SDL 为契约唯一真值源，代码生成/映射对照它（与 REST 契约同等冻结纪律）。
- 命名：类型 PascalCase、字段/查询 camelCase；查询动词语义（`orders` 查询、
  `createOrder`/`cancelOrder` 变更），与 REST 资源命名一致可互查。
- 非空显式：`!` 只标真正必有；可空字段必须回答"什么情况下是 null"（注释写明）。
- 错误：业务错误进 `errors`（带稳定 `code`/`message`，结构对齐 REST 错误约定）+
  载荷级 `userError`/`result` 联合类型承载可恢复业务失败（两者边界写进 schema 文档）。
- 枚举与标量自定义（`DateTime`/`Money`/`UUID`），不滥用 String。

## 2. 分页与查询

- 分页统一 **Relay Cursor Connections**（`edges{node,cursor} pageInfo{...}`），
  偏移分页仅后台低频场景；游标不透明（不暴露自增 id）。
- 关联深度由 schema 自然约束（嵌套表达聚合），不做无界递归类型。
- **复杂度与深度限制强制**：服务器端 `maxDepth`/`maxComplexity` 显式配置并写入 ADR，
  防嵌套查询放大（宪法第 11 条纵深防御）。

## 3. N+1 与性能

- DataLoader 强制：每个批量关联字段（列表→关联对象）必须有 loader，
  请求级缓存单例；新增关联字段必附 loader 测试。
- 字段级观测：`apollo` 系 tracing / `gqlgen` 的字段耗时埋点进结构化日志，
  P95 字段耗时超阈值（如 50ms）登记待优化。
- 持久化查询（Persisted Queries / APQ）生产启用：客户端传 hash 不传全文，
  杜绝任意查询文本注入面。

## 4. 鉴权与权限

- 认证上下文：token 解析进 context，字段/查询解析器逐级读取——**每个解析器各自鉴权**，
  禁止"入口校验过就全放行"（字段级暴露是 GraphQL 越权重灾区）。
- 对象级与字段级权限双层：可见性（返回 null/部分字段）与可执行性（抛 ForbiddenError）分开声明。
- 变更操作幂等：`clientMutationId` / 幂等键参数对齐 REST `Idempotency-Key` 约定。

## 5. 演进与版本

- 无破坏演进：字段**只加不删**；弃用用 `@deprecated(reason)`，退役走
  「标注 → 度量归零 → 下线」三步并记入契约变更记录。
- Schema 变更经总指挥 → 架构师（与 REST 契约变更同一流程，见 collaboration.md）。

## 6. 服务端实现选型（按后端栈）

| 栈 | 实现 |
|---|---|
| Java（Spring/Quarkus） | Spring for GraphQL / SmallRye GraphQL |
| Node/NestJS | @nestjs/graphql（Apollo Server / code-first 或 schema-first 统一） |
| Go | gqlgen（schema-first） |

## 7. 测试

- 契约测试：schema 快照 + 关键 query/mutation 集成测试（响应结构断言）；
- 越权测试覆盖：未认证、低权限调高权限字段、跨租户 id 直查三类必测。

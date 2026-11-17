# Java / Quarkus 编码规范（后端工程师实现必读）

适用：Java 17+ / Quarkus 3.x / Maven。适用场景：云原生、Serverless、K8s 部署、
追求快速启动与低内存（GraalVM native image）。

## 1. 工程结构

```
src/main/java/<pkg>/
├── config/        # ConfigMapping 配置类
├── resource/      # REST 层：@Path 端点，只做校验 + 调 service
├── service/       # 业务层：业务规则与事务边界（@ApplicationScoped）
├── repository/    # Panache 数据访问层（见 standards/backend-jpa-hibernate.md）
├── entity/        # 实体
├── dto/           # 请求/响应对象
└── exception/     # 业务异常 + ExceptionMapper（全局异常出口）
src/main/resources/application.properties   # 配置（环境变量覆盖 ${ENV:default}）
```

依赖方向：resource → service → repository，禁止跨层与反向。

## 2. 依赖注入与生命周期

- CDI 注入：`@ApplicationScoped`（默认）+ 构造器注入；请求级用 `@RequestScoped`。
- `@ApplicationScoped` 代理语义：字段可为非 final；不要在构造器里访问注入的依赖
  （代理未就绪），初始化逻辑放 `@PostConstruct`。
- 优先普通类 + PanacheRepository 模式；实体继承 PanacheEntity 的 active record 模式
  仅在简单 CRUD 单体中使用（团队统一二选一，写进 ADR）。

## 3. REST 端点

- 端点声明：`@Path("/api/v1/...")` + JAX-RS 注解；参数校验用 Hibernate Validator
  （`@Valid` + JSR-303），不手写空判断散落各处。
- 统一响应：Response 包装 + 统一错误结构（ExceptionMapper 映射业务异常 → 契约错误 JSON）。
- RESTEasy Reactive（`@Path` + `@GET` 默认 reactive 语义）：阻塞操作显式 worker 线程
  （方法签名声明返回类型即决定调度，禁止在 reactive 端点里做阻塞 IO）。
- OpenAPI：quarkus-smallrye-openapi 注解生成文档，与契约比对。

## 4. 配置

- 环境变量覆盖：`quarkus.datasource.jdbc.url=${DB_URL:jdbc:postgresql:5432/app}`；
  密钥只从环境变量注入，禁止 properties 明文。
- 类型安全配置：`@ConfigMapping(prefix="app")` 接口 + `Optional`/默认值，
  启动时校验缺失配置快速失败。
- profile 区分：`%dev`/`%test`/`%prod` 前缀，测试默认 Dev Services（容器拉起依赖库）。

## 5. 事务与容错

- 事务：`@Transactional` 标注 service 方法；只读 `@Transactional(SUPPORTS)` 或
  `readOnly=true`（Hibernate 只读提示）。
- 容错：SmallRye Fault Tolerance 声明式（`@Retry`/`@Timeout`/`@Fallback`/`@CircuitBreaker`），
  重试只用于幂等操作；超时与重试参数外置配置。
- 事务内禁止远程调用（HTTP/JMS），用事务事件（`@Observes(during=AFTER_COMPLETION)`）解耦。

## 6. 测试

- `@QuarkusTest` 集成测试（Dev Services 自动起依赖容器）；业务规则单测不依赖容器。
- native 测试（`@NativeImageTest`）仅 CI 关键路径执行，本地不强制。

## 7. 质量命令

```bash
./mvnw quarkus:test        # 测试（含 Dev Services）
./mvnw verify              # 编译 + 测试 + 打包
./mvnw package -Dnative    # native 构建（交付 K8s/Serverless 时）
```

提交前 `verify` 通过；Hibernate Validator/静态问题 ERROR 清零。
JPA/Hibernate 共性纪律见 `standards/backend-jpa-hibernate.md`。

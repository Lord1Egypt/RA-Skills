# Java / Spring Boot 编码规范（后端工程师实现必读）

适用：Java 17+ / Spring Boot 3.x。规范未覆盖处遵循《阿里巴巴 Java 开发手册》。

## 1. 工程结构（单一 Maven 模块起步，模块化按需拆分）

```
src/main/java/<pkg>/
├── config/        # 配置类（Web、Security、MyBatis/JPA、OpenAPI）
├── controller/    # 路由层：参数校验 + 装配 + 调 service，不写业务
├── service/       # 业务层：接口 + impl；事务边界在此
├── mapper|repository/  # 数据访问层
├── model/
│   ├── entity/    # 表映射
│   ├── dto/       # 请求/响应对象（Request/Response 后缀）
│   └── vo/        # 领域值对象
├── common/        # 统一响应、异常、错误码枚举、工具
└── exception/     # 业务异常 + 全局异常处理器
```

依赖方向：controller → service → mapper，禁止跨层与反向。

## 2. 分层规则

- Controller：只做 校验（`@Valid` + JSR-303 注解）、调 service、组装响应；不碰 Repository。
- Service：业务规则与事务（`@Transactional` 只标在需要事务的方法上，只读方法 `readOnly=true`）；
  不感知 HTTP 对象（HttpServletRequest 禁止入参穿透到 service）。
- Mapper/Repository：只写数据访问；禁止写业务判断与远程调用。
- DTO 与 Entity 严格分离；跨层传递一律 DTO，转换用显式映射方法（MapStruct 可选）。

## 3. 统一异常与错误码

- 业务异常抛 `BizException(ErrorCode)`，由 `@RestControllerAdvice` 全局处理，
  映射为 API 契约的错误结构；禁止 controller 内 try-catch 后吞掉。
- 错误码用枚举：`ORDER_NOT_FOUND(40401, "订单不存在")`，与契约错误码一一对应。
- 不向客户端暴露堆栈与框架异常名。

## 4. 依赖注入与配置

- 构造器注入（`@RequiredArgsConstructor`），禁止字段注入。
- 配置外置：`application.yml` + 环境变量覆盖（`${DB_URL:jdbc:mysql://localhost:3306/app}`）；
  密钥只从环境变量/配置中心读取，禁止写进 yml 明文与源码。
- `@Value` 收敛到 `@ConfigurationProperties` 类型安全配置类。

## 5. 并发与事务红线

- 共享可变状态必须显式同步或改用无状态设计；优先无状态。
- `@Transactional` 不生效场景自查：私有方法、同类内自调用、catch 吞异常。
- 事务方法内禁止 HTTP/RPC/MQ 调用；需要时用事务同步器（`afterCommit`）。

## 6. 测试

- 单测覆盖 service 核心业务规则；分层测试用 `@WebMvcTest`（controller）+
  `@DataJpaTest`/MyBatis 测试库（数据层）。
- 测试命名：`方法_场景_期望`（`payOrder_whenCancelled_throwsException`）。
- 不测 getter/setter；不 mock 被测对象本身。

## 7. 质量命令

```bash
./mvnw verify            # 编译 + 测试
./mvnw spotless:check    # 格式（引入 Spotless 时）
```

提交前必须本地通过 `verify`；静态检查 ERROR 清零。

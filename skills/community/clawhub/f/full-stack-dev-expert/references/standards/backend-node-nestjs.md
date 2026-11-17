# Node.js / NestJS 编码规范（后端工程师实现必读）

适用：Node.js 20+ / NestJS 10+ / TypeScript strict 模式。

## 1. 工程结构

```
src/
├── main.ts               # 引导：端口、全局管道/过滤器、Swagger
├── app.module.ts
├── common/               # 统一响应、错误码、异常过滤器、拦截器、守卫、Pipe
├── config/               # ConfigModule 类型安全配置
├── modules/<domain>/     # 按业务域组织，域内自含
│   ├── <domain>.module.ts
│   ├── <domain>.controller.ts
│   ├── <domain>.service.ts
│   ├── <domain>.repository.ts      # TypeORM/Prisma 数据访问
│   └── dto/                         # 请求/响应 DTO + class-validator
└── entities/ 或 prisma/
```

域模块自包含；跨域依赖走 module exports/imports，禁止跨域直接 import 内部文件。

## 2. 分层规则

- Controller：`@Body()`/`@Query()` 只收 DTO（`class-validator` 装饰器校验 + 全局
  `ValidationPipe({ whitelist: true, transform: true })`），不写业务。
- Service：业务逻辑、事务（Prisma `$transaction` / TypeORM `QueryRunner`/`transaction()`）。
- Repository：数据访问收敛；禁止 service 直接拼 SQL 字符串（参数化查询强制）。
- 禁止循环依赖；需要双向时用 `forwardRef` 并在代码注释说明理由。

## 3. 类型纪律

- `tsconfig.json`：`strict: true`、`noUncheckedIndexedAccess: true`；
  禁止 `any`、`as unknown as`、`!` 非空断言（显式判空代替）。
- DTO 与 Entity 分离；响应对象显式声明类型；对外 API 类型从 DTO 推导
  （`ReturnType<typeof ...>` 或手写 Response 类型），保证契约一致。
- 错误码集中枚举与契约一致；抛 `HttpException` 或自定义 `BizException`
  由全局 `ExceptionFilter` 统一转错误结构。

## 4. 异步与错误

- 全 async/await；禁止裸 `.then()` 链混用与未 await 的 Promise（lint: `no-floating-promises`）。
- 禁止空 catch；捕获后要么处理要么包装重抛。
- 未捕获异常兜底：`process.on('unhandledRejection'|'uncaughtException')` 记日志并优雅退出。

## 5. 配置与安全

- `@nestjs/config` + `.env`（`.env.example` 提交，`.env` 进 `.gitignore`）；
  配置类用 zod 或手写校验，启动时校验失败快速失败。
- 密钥环境变量注入； helmet 默认启用；CORS 白名单显式配置。
- Prisma 首选（类型安全）；TypeORM 需严格遵守参数化。

## 6. 测试

- Jest：service 单测（mock repository）、controller 用 Supertest 走 HTTP 层、
  e2e 测主流程（`test/*.e2e-spec.ts`）。
- 命名 `方法_场景_期望`；测试数据库用内存/容器库，不碰开发库。

## 7. 质量命令

```bash
npm run lint && npm run build && npm test
```

提交前三项全过；ESLint `@typescript-eslint` 严格集无 ERROR。

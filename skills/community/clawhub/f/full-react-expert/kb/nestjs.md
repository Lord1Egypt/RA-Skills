---
subdomain: nestjs
version: 21
updated: 2026-11-17
---
# NestJS

## 定位与心智模型

NestJS 是 Node.js 服务端框架（TypeScript 优先），架构受 Angular 启发：**模块（Module）组织代码、依赖注入（DI）组装依赖、装饰器声明横切关注点**。适用边界：中大型 Node 后端、REST/GraphQL API、微服务。默认 Express 平台，可换 Fastify。

一句话心智模型：请求进来后沿固定管道流动——**middleware → guards → interceptors (pre) → pipes → handler → interceptors (post) → exception filters → 响应**。定位任何"为什么没生效"的问题，先画这条链。

## 法则

[NE-1] **MUST**: 运行时校验的 DTO 必须是 class（class-validator 装饰器）或挂 Standard Schema（v12 `schema` 选项）（全局宪法 LAW-7）。
- 违反后果: interface 编译即消失，校验静默失效、非法字段照过。
- 溯源: [官方文档](https://docs.nestjs.com/migration-guide)

[NE-2] **MUST**: Provider 使用前必须满足注册链完整：providers 注册 / exports 导出 / forFeature 导入 / 循环依赖 forwardRef 两侧 / @Injectable。
- 违反后果: `Nest can't resolve dependencies of the XService (Y, ?)`。
- 溯源: [官方文档](https://docs.nestjs.com)

[NE-3] **MUST**: 全局组件需要 DI 依赖时必须用 APP_GUARD/APP_PIPE/APP_INTERCEPTOR/APP_FILTER token provider，而非 app.use*。
- 违反后果: 静态注册不进 DI 容器，注入依赖为 undefined。
- 溯源: [官方文档](https://docs.nestjs.com/fundamentals/lifecycle-events)

[NE-4] **MUST**: interceptor 必须返回 `next.handle()` 管道（RxJS 链）。
- 违反后果: 200 但响应 body undefined。

[NE-5] **MUST**: 事务回调内部一律使用传入的 manager/repository，不得混用全局实例。
- 违反后果: 混用部分在事务外执行，回滚失效。

[NE-6] **MUST**: 生产应用调用 `app.enableShutdownHooks()`；连接类 Provider 实现 onModuleDestroy 释放（全局宪法 LAW-12）。
- 违反后果: SIGTERM 不触发清理，连接泄漏。
- 溯源: [官方文档](https://docs.nestjs.com/fundamentals/lifecycle-events)

[NE-7] **MUST**: 微服务 `client.send()` 返回的 Observable 必须订阅（firstValueFrom/subscribe）才算发出。
- 违反后果: 冷 Observable 不订阅，请求根本没发。
- 溯源: [官方文档](https://docs.nestjs.com/microservices/basics)

[NE-8] **NEVER**: 请求作用域（Scope.REQUEST）不得沿主干依赖链扩散。
- 违反后果: 整链每请求重建，性能塌方；确需时隔离到叶子。
- 溯源: [官方文档](https://docs.nestjs.com/fundamentals/injection-scopes)

[NE-9] **MUST**: 字面量路由声明在通配路由之前（`@Get('me')` 先于 `@Get(':id')`）；v12 可用 routeConflictPolicy 控制。
- 违反后果: `/users/me` 被当 `:id='me'` 处理。
- 溯源: [官方文档](https://docs.nestjs.com/migration-guide)

[NE-10] **MUST**: 生命周期钩子（onModuleInit 等）里做初始化重活，不放构造器。
- 违反后果: 构造期阻塞 DI 实例化链；时序不可控。

[NE-11] **MUST**: 升级必须逐大版本、用官方 `nest upgrade`；伴随包按 peerDependencies 对齐。
- 违反后果: 版本错位运行时崩溃；v12 ESM 下尤甚（ERR_REQUIRE_ASYNC_MODULE）。
- 溯源: [官方文档](https://docs.nestjs.com/faq/versions)

[NE-12] **MUST**: `onModuleInit`/`onApplicationBootstrap` 里发事件前先 `await readinessWatcher.waitUntilReady()`（@nestjs/event-emitter v3+）；bootstrap 前后语义选对。
- 违反后果: 初始化期事件静默丢失（监听器未注册）或反而丢失发送者上下文
- 溯源: [官方文档](https://docs.nestjs.com/application/events.md)

[NE-13] **MUST**: 默认内存 cache store 的 `get()` 返回 `set()` 传入的同一引用（非副本）——缓存对象必须只读或取出后拷贝再改；Redis store 必须挂 `'error'` 监听器。
- 违反后果: 修改返回对象污染缓存；Redis 断连无监听器时 Keyv 抛错使整个应用崩溃
- 溯源: [官方文档](https://docs.nestjs.com/data/caching.md)

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| Module | `@Module()` 组织 providers/controllers，DI 的注册单元 |
| Provider | 任何可注入对象（service/repository/factory/token） |
| Guard | 鉴权层（canActivate），决定请求是否放行 |
| Pipe | 转型/校验层（ValidationPipe / StandardSchemaValidationPipe（v12）） |
| Interceptor | 环绕 handler 的 RxJS 中间层（改写响应/超时/缓存） |
| Exception Filter | 统一错误捕获与响应格式化 |
| 伴随包 | @nestjs/config 等独立发布线，须选兼容 peer 版本 |
| Standard Schema | v12 路由校验新路径：Zod/Valibot/ArkType 直挂装饰器 |

## 最佳实践

### 场景：入参校验（[NE-1]）

推荐路径：class DTO + class-validator 装饰器 + 全局 ValidationPipe（main.ts 一次）→ v12 项目可改用 Zod schema 直挂装饰器。嵌套对象 `@ValidateNested() @Type(() => AddressDto)` 成对出现；数组加 `each: true`。

```ts
// don't：DTO 写 interface（校验静默失效 [NE-1]）
interface CreateUserDto { name: string; }

// do：class DTO + 全局管道
class CreateUserDto { @IsString() name: string; }
app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true, forbidNonWhitelisted: true }));

// do（v12）：Zod schema 直挂装饰器
@Post() create(@Body({ schema: createUserSchema }) dto: CreateUserDto) { ... }
```

边界条件：`transform: true` 后 DTO 才是实例；`whitelist: true` 剔除未声明字段——两者都开才是安全基线。

**Standard Schema 双轨深度**（Nest 12 官方文档锚定，2026-11-16）：

- `StandardSchemaValidationPipe`（@nestjs/common）与 ValidationPipe **可同时全局注册**、增量采用——schema 管道只校验声明了 `{ schema }` 的参数，class 管道只校验 class 参数
- **转换语义**：默认 `transform: true` 传 schema 输出（z.coerce/default/trim 生效）；`transform: false` 传原始输入——参数类型改用 `z.input<typeof schema>`
- **未知属性由 schema 自决**（对应 class-validator 选项）：`z.object()` 剥离（=whitelist）/ `z.strictObject()` 拒绝（=forbidNonWhitelisted）/ `z.looseObject()` 保留
- **派生替代 mapped-types**：`.partial()/.pick()/.omit()/.extend()` 对应 PartialType/PickType/OmitType/IntersectionType；数组直接 `z.array(schema)`（无泛型元数据限制，替代 ParseArrayPipe）
- **自定义装饰器默认跳过**：`validateCustomDecorators: true` 才校验 createParamDecorator 产物；WS/微服务用 `exceptionFactory` 返回 `WsException`/`RpcException` 适配传输层
- `{ schema }` 选项覆盖 `@Body()/@Query()/@Param()/@MessageBody()（gateway）/@Payload()（微服务）`；校验失败 400，消息按路径前缀（`"email: Invalid email address"`）
- 来源：[官方文档](https://docs.nestjs.com/techniques/validation.md)

### 场景：Provider 组装与模块划分（[NE-2]）

推荐路径：按业务域划分（UserModule/OrderModule），跨域共享逻辑提 CommonModule；service 注册进本模块 providers，需共享时显式 exports。

```ts
@Module({
  imports: [TypeOrmModule.forFeature([User])],  // 坑点 1 排查第 3 项
  providers: [UserService],
  exports: [UserService],                       // 漏写 → 下游 can't resolve
})
```

边界条件：循环依赖 `forwardRef(() => B)` 两侧成对；忘写 `@Injectable()` 不报编译错，运行时才炸；token/字面量注入用 `@Inject(TOKEN)` + useValue/useFactory（factory 依赖按参数顺序注入）；动态模块 forRoot/forRootAsync（`ConfigModule.forRoot({ isGlobal: true })` 全局免逐模块 import；`@Global()` 模块同理）；配置对象直接当 provider 传是错的——useValue + token 或 ConfigService。

### 场景：全局横切组件（[NE-3]）

推荐路径：需要 DI 依赖的全局 Guard/Pipe/Interceptor/Filter 一律用 token provider。

```ts
// don't：静态注册（拿不到 ConfigService）
app.useGlobalGuards(new JwtAuthGuard(config));

// do：token provider 注入式
{ provide: APP_GUARD, useClass: JwtAuthGuard }
```

### 场景：事务与数据层（[NE-5]）

推荐路径：TypeORM 要 hooks/时间戳用 `save()`；纯字段更新用 `update()`/`UpdateResult`；软删 `softDelete()` + `recover()`。事务统一 `dataSource.transaction(async (manager) => ...)`，**回调内全用 manager**。

```ts
await this.dataSource.transaction(async (mgr) => {
  await mgr.save(order);        // do：用 mgr
  await this.userRepo.update(   // don't：混用全局实例 [NE-5]
    ...);                       //     这行在事务外执行，不回滚
});
```

### 场景：生命周期与优雅停机（[NE-6]/[NE-10]）

推荐路径：main.ts `app.enableShutdownHooks()`；初始化重活进 onModuleInit，连接释放进 onModuleDestroy；Prisma `$connect/$disconnect`、定时器、消息队列 consumer 均遵循"获取↔释放成对"（LAW-12）。

```ts
// don't：构造器里做重活
constructor() { this.prisma.$connect(); }

// do：生命周期钩子里
async onModuleInit() { await this.prisma.$connect(); }
async onModuleDestroy() { await this.prisma.$disconnect(); }
```

### 场景：鉴权与授权（@nestjs/authentication+authorization 官方双轨 / Passport 既有路线）

**双轨判定（2026-11-16）**：**Nest 12 新项目优先 `@nestjs/authentication` 0.1.6 + `@nestjs/authorization` 0.1.4**（peer 仅 ^12——Nest 11 不可用；sessions/密码 scrypt/MFA TOTP/OIDC/magic link/API keys/JWT+refresh 全家桶内置）；需要特殊 Passport 策略（企业 SAML 等）或 Nest ≤11 时走 `@nestjs/passport` 既有路线。

- **@nestjs/authentication 架构**：`AuthenticationModule.forRoot()` 注册全局 guard——**装上即所有路由要求登录**，例外 `@Public()`；forRoot **只收值不收类**（providers/handlers/store 是你的 provider，构造器向 AuthenticationRegistry 自注册）；credential provider 链（SessionCookieProvider/JwtBearerProvider/ApiKeyProvider）`registerProvider(this, { order })` **order 显式声明**（同 order 两个 startup 失败；链升序第一个返 user 赢；无凭据 401 `missing_credentials` + WWW-Authenticate）
- **安全基线**：密码 scrypt OWASP 参数（N=2^17 ≈128 MiB memory-hard、libuv 线程池、无原生依赖、NFKC 归一化、自描述哈希串）；**未知用户验 dummy hash 防枚举时序**；session cookie `__Host-sid` HttpOnly+Secure+SameSite=Lax **只存 SHA-256**（store 泄漏不可重放）；signIn 删旧 session 防 fixation；跨站 POST/WS 握手 403（login CSRF）；`app.enableCsrfProtection()`（Nest 12.1+）传同 trustedOrigins
- **JWT+refresh**：`accessToken: { key≥32B, ttl: 15m }` HS256/ES256；refresh token 不透明存哈希、每次轮换、**复用即整族吊销**（refresh-token-reused）；amr claim 随 family 贯穿（**会变的 roles 勿入 claims**，validate() 每请求现查）；外部 issuer 走 jwks（https 强制、HS 拒绝）+ issuer/audience 都必须
- **MFA（TOTP）**：secret AES-256-GCM 加密入库（**配 mfa 无 encryption startup throw**；keys 数组新 key 在前可轮换）；enroll→confirm（**10 个 recovery codes 只展示一次**）→pending session（10m）→`completeMfa()` **轮换 session id**；code ±30s 每 code 一次；**15 分钟 5 次失败锁账号（先计数后校验）**；`@Authenticate({ mfa: true })`——**API key 永不算第二因素**；**issue() 丢弃自造 amr 的 mfa/otp/hwk**（无法意外铸造 verified token）
- **OIDC**：code flow + **PKCE+state+nonce**（state=事务 cookie SHA-256——callback 泄露无人能完成他处发起的登录）；`OidcAccountResolver.resolveUser()` 裁决——**首次到访仅 email+emailVerified 建号；按 email 链接须 existing 也 verified 否则 403（account pre-hijacking 防御）**；redirectTo 只收相对路径；**BYO-IdP 红线：issuer 是用户输入，包无内网防护必须先校验**
- **magic link**：存储=token+浏览器事务 cookie 组合的 SHA-256；create 一律 202 防枚举；**consume 先查 `__Host-magic_link_tx`（最近 5 条）**——别的浏览器 401 `not_this_browser`；**link 创建的账号 verified，但密码注册未验证账号 403 拒绝（防 pre-hijacked 交接）**；验证/重置/魔法链接页面**必须 POST 提交 token**（邮件扫描器 GET 会消费掉）
- **邮件验证/密码重置同型 handler**：`EmailVerificationHandler`（send/markVerified；token 存 SHA-256、一次性、ttl 24h、只验证所发往的地址）/ `PasswordResetHandler`（findUser/send/updatePassword；ttl 1h；**`request()` 返回后才查库发信——同 202 同速防枚举**；link 只发存储的地址）；邮件验证配置 `emailVerification: { url, ttl }`
- **数据库 store**：六契约（Session/RefreshToken/Mfa/MagicLink/OidcState/EmailToken）八表，构造器 registerSource 注册；**production 无所需 store 拒启动**（allowInMemoryStorage 豁免=重启全员签出）；**原子性 MUST：凡"只生效一次"必须单条条件语句（DELETE...RETURNING/条件 UPDATE 计行数），绝不先读后写**；recordMfaFailure 两条独立提交**不用事务**；**任何方法不接受业务事务**；`authenticationStoreContract({ concurrent: true })` 契约测试（PGlite+PG 双跑）；Prisma 等价：updateMany/deleteMany+count、**禁 upsert 做 touchSession**、recordMfaFailure=create 后 count 非 $transaction
- **限流**：包本身不限流——配 @nestjs/throttler **双 definition**（default 按 IP 全路由 + account 按 email+IP）；ThrottlerGuard 注册根模块 APP_GUARD（**认证 guard 之前**）；guard 在 validation 前跑须自查 `typeof email === 'string'`；代理后必开 trust proxy；生产 Redis 共享存储
- **@nestjs/authorization**：`@Policy()` 类首参 user 返 boolean 的方法=ability（**只有字面 true 放行**）；`can()`（不抛，塑形如 canRefund 标志）/`authorize()`（拒抛 AuthorizationError 401/403，出 handler 转 HTTP/WS/RPC，**响应不暴露 policy/ability 名**）；**默认拒绝**——handler 无 @Can()/@Can.Anyone()/@Public() 即拒（**启动日志点名**，迁移起点）；**record 检查进 service**（列表 query 过滤勿逐行）；**AuthenticationModule 必须在 AuthorizationModule 之前 import（反了 startup 失败；其他认证 guard 无标记只 log error 且 @Can 全视 guest——须有 e2e 兜底）**；`before()` admin 旁路（**全局规则勿放 before**）；路由参数 @Can 第三参在 pipe 前（无权 id 403 非 400）；**policy 必须单例**；**检查 record 的路由禁按 URL 缓存**（CacheInterceptor 会把别人的订单端出去）；自己的 guard/middleware 里用 can() 勿用 authorize()（出 handler 变 500）
- **Passport 既有路线**：`PassportStrategy(Strategy[, name])` + validate() 返值挂 req.user；全局 APP_GUARD + Reflector 自建 @Public()；**策略不可 request-scoped**（要动态解析用 ModuleRef+ContextIdFactory.getByRequest+resolve，须 passReqToCallback: true）；GraphQL 覆写 getRequest()；三件套 @nestjs/passport+passport+策略包
- **测试**：e2e 三件套 PGlite（进程内 PG）/InMemoryMailTransport（mailbox.assertSent+mail.link 取 token）/override PasswordHasher（logN 10——默认 128 MiB 拖不起）；**reset 邮件在响应后发出须 vi.waitFor**；SessionService.create()/TokenService.issue()/run() 绕过登录
- 来源：[官方文档](https://docs.nestjs.com/security/authentication.md) + [官方文档](https://docs.nestjs.com/security/authorization.md) + [官方文档](https://docs.nestjs.com/security/encryption-and-hashing.md) + [官方文档](https://docs.nestjs.com/recipes/passport.md)

### 场景：GraphQL（@nestjs/graphql v14）

推荐路径：code-first（`@ObjectType()/@Field()`）为官方主推；driver 模型二选一——**Apollo（@nestjs/apollo，v14 要求 Apollo Server v5 `@apollo/server`）** 或 Mercurius（Fastify）；`GraphQLModule.forRoot<ApolloDriverConfig>({ driver: ApolloDriver, autoSchemaFile })`。resolver 参数装饰器 `@Args()/@Context()/@Parent()`；DTO 校验双轨同样适用。

关键语义（官方文档锚定，2026-11-16）：

- **graphql-playground 已移除（v14）**：`playground` 选项仅存为 **graphiql 的弃用布尔别名**（graphiql 优先）；**GraphiQL 在 NODE_ENV !== 'production' 自动启用**，`graphiql: true` 强开含生产；Apollo Sandbox 替代 IDE 用 `graphiql: false` + `ApolloServerPluginLandingPageLocalDefault()`
- subscription 用 **graphql-ws**（`subscriptions: { 'graphql-ws': true }`；subscriptions-transport-ws 彻底移除）
- context 工厂 `({ req, res }) => ({ req, res })`；Guards/Interceptors 经 `GqlExecutionContext.create(context).getContext()`
- **多端点**：`include: [CatsModule]` 限定 resolver 扫描；**code-first 类型默认进所有 schema——用 `registerIn` 选项作用域化**（@ObjectType/@InputType/registerEnumType/createUnionType 均支持；工厂形式 `() => CatsModule` 防循环导入）
- schema-first：typePaths + definitions（`outputAs: 'class'`；GraphQLDefinitionsFactory 脚本 + watch）
- e2e 直接执行查询：`app.get(GraphQLSchemaHost).schema`（onModuleInit 后可取）——免起 HTTP 层直接 `graphql()` schema 执行
- 来源：[官方文档](https://docs.nestjs.com/graphql/quick-start)

### 场景：API 文档（Swagger）

推荐路径：`@nestjs/swagger` 的 CLI 插件（`@nestjs/swagger/plugin`）自动推断 DTO 元数据，消除与 class-validator 的重复 `@ApiProperty()` 标注；v12 下伴随包版本对齐 peer（[NE-11]）。

### 场景：微服务调用（[NE-7]）

推荐路径：`client.send(pattern, payload)` 返回**冷 Observable 必须订阅**（firstValueFrom）；`client.emit(pattern, payload)` 为事件发布返回**热 Observable 勿需订阅**（立即投递）。

```ts
// don't：冷 Observable 不订阅，请求根本没发
this.client.send(pattern, payload);

// do
const result = await firstValueFrom(this.client.send(pattern, payload));
```

关键语义（官方文档锚定，2026-11-16）：

- transporter 全景：TCP（默认）/Redis/MQTT/NATS/RabbitMQ/Kafka/gRPC/自定义；`NestFactory.createMicroservice(AppModule, { transport, options })`
- 两种风格：`@MessagePattern`（request-response，双通道；**Kafka/NATS JetStream 日志流平台更适合 event 风格**）vs `@EventPattern`（fire-and-forget；**同 pattern 多 handler 全部并行触发**）
- **pattern 匹配硬限制**：嵌套 ≤5 层、每对象 ≤20 键、字符串值 ≤4096 字符、全 pattern ≤100 键——超限替换 `[TOO_MANY_KEYS]` 再匹配；>1MiB JSON 按纯字符串匹配
- client 注入三路：ClientsModule.register/registerAsync（name 为注入 token，首选）/ClientProxyFactory.create() 自定义 provider（配置来自 ConfigService）/@Client() 装饰器（**非首选——难测试难共享**）；ClientProxy 惰性连接，`connect()` 放 onApplicationBootstrap 可延迟启动至连上
- **TCP host 坑（v12.5）**：空值= localhost——容器须显式 `'0.0.0.0'` 或 `'::'`；maxBufferSize 默认 16MB（v12.5 逐包、从 128MB 下调）
- 超时用 RxJS `timeout` 算子；元数据用 `client.setOnDispatchHook((packet) => packet.metadata = {...})`（TCP/Redis 随包，NATS/Kafka/gRPC 走消息头）
- 动态配置用 `AsyncMicroserviceOptions`（useFactory + inject）
- 来源：[官方文档](https://docs.nestjs.com/microservices/basics)

### 场景：安全头与限流（helmet/throttler）

推荐路径：**安全头用 `app.useSecurityHeaders()`（Nest 12.1+ 内置，免 helmet 依赖）**——Helmet 8 同默认值、Express/Fastify 同行为；紧跟 `NestFactory.create()` 之后、`listen()` 之前调用（后调/调两次抛错）；CSP 自定义 directives（自设指令替换同名默认需含 `'self'`；GraphiQL/Apollo Sandbox 需放宽策略；生产避免 `'unsafe-inline'`）；仍可直接用 helmet（Express `app.use(helmet())`/Fastify `app.register(@fastify/helmet)`）。限流用 **@nestjs/throttler**（`forRoot({ throttlers: [{ ttl 毫秒, limit }] })` + `APP_GUARD: ThrottlerGuard`）；`@Throttle({ default: { limit, ttl } })`/`@SkipThrottle()` 按路由调节；代理后设 trust proxy（**Fastify 5.12.1+ 数字型 trustProxy 信任任何代理都不**——传地址/网段）；分布式用 @nest-lab/throttler-storage-redis。

### 场景：队列（@nestjs/bullmq）

推荐路径：`BullModule.forRoot({ connection })` → `registerQueue({ name })` → `@InjectQueue('name')` 注入 Queue.add()；consumer `@Processor('q') extends WorkerHost` 覆写 `process(job)`——**BullMQ 无 `@Process('name')`，用 `switch (job.name)` 分发**；事件 `@OnWorkerEvent('active')`（worker 级）/`@QueueEventsListener('q') extends QueueEventsHost`（队列级）。**重复任务用 `Queue#upsertJobScheduler()`（`repeat` 选项已从 add() 移除）**。**免 Redis 可选 `backendFactory: createPostgresBackend`（BullMQ 6 PG 后端，`migrate: true` 建表）**。sandboxed processors（fork 进程）无 DI——依赖须自建。

### 场景：Prisma（v7 现役 / v8 RC 双线）

推荐路径：`prisma.config.ts`（`defineConfig`）+ 首行 `import "dotenv/config"`（**Prisma 7 不自动加载 .env**）；`env("DATABASE_URL")` 类型安全但未定义即抛错——CI 只跑 `prisma generate` 用 `process.env.DATABASE_URL ?? ''`。`$extends` 四组件（model/client/query/result）：RLS per-request client、$allOperations 审计日志链式中间件；**Prisma 8（RC）用新 extensions+middleware 取代 $extends——v8 项目勿再写 $extends**。

驱动适配器（v7 连接双轨，2026-11-16 深度锚定）：

- **连接配置双轨**：`prisma.config.ts` 的 `datasource.url` 只供 **CLI**（migrate/studio）；**应用连接**在适配器构造处另传——`new PrismaPg({ connectionString: process.env.DATABASE_URL })` → `new PrismaClient({ adapter })`；改了 config 里的 URL 不等于改了应用连接
- **v7 generator 推荐 `provider = "prisma-client"`**（替代 `prisma-client-js`）+ 自定义 `output`（默认 `../generated/prisma`）；从生成目录导入 `./generated/prisma/client` 或链接依赖 `pnpm add db@link:./generated/prisma`
- 官方 Node 适配器：pg / mariadb / better-sqlite3 / libSQL（Turso）/ node-mssql；serverless/edge：@prisma/adapter-ppg / Neon / PlanetScale / Cloudflare D1；**TypedSQL 与所有适配器兼容除 `@prisma/adapter-better-sqlite3`**（需 TypedSQL 的 SQLite 用 libsql）
- config 补充面：`tables.external`/`enums.external`（外部管理表/枚举——可查询、迁移忽略；须 `experimental.externalTables: true`）；`migrations.initShadowDb`（影子库前置 SQL）；**多文件 schema**（`schema` 指向文件夹；migrations 目录须与定义 datasource 的 .prisma 文件同级）；**`npx`/`bunx prisma` 仅项目根找得到 config**（pnpm 子目录也行；否则 `--config`）
- 来源：[官方文档](https://www.prisma.io/docs/orm/reference/prisma-config-reference) + [官方文档](https://www.prisma.io/docs/orm/overview/databases/database-drivers)

Prisma ORM 8（RC，2026-11-16 深度锚定——**npm latest 即 RC**）：

- **版本判定**：`prisma`（CLI）latest=**8.0.0-rc.34**（prev=7.10.1）；ORM 8 = 两包结构：CLI + 库 **`@prisma/orm-postgres`/`@prisma/orm-mongo`**（8.0.0-rc.23；**CLI 与库分开发版、版本号不配对**，全装 latest 即可；每个 @prisma/orm-* 库全项目只装一份——两份副本互不识别但照常启动，`npm ls @prisma/orm-postgres` 自查）；**`@prisma/client` 无 8.x（停在 7.10.1，属 v7）**；Node 22.18+/24.11+/26+、TS ≥5.9、temporal-polyfill peer（Yarn 手装）；**ORM 7 支持到 8 GA 后 18 个月；ORM 6 安全补丁 2026-11-19 截止**
- **contract 取代 schema**：`schema.prisma` → `contract.prisma`（**首行 MUST `// use prisma-8`**——emit 无警告跳过无此行文件）；`datasource`/`generator` 块移除 → `prisma.config.ts` 的 `orm: ormConfig({ contract, db, output, extensions, migrations })`（**无 provider——import 即选库**）；`contract emit` 写 contract.json + contract.d.ts（**两个都 commit**）；也可用 TypeScript builder 写 contract
- **client 手写**（不生成 PrismaClient）：`src/prisma/db.ts` = `postgres({ contract, url, middleware? })` + `contractFromJson`；查询链式化：`.where(...).select(...).orderBy((u)=>u.createdAt.desc()).limit(10).all()`；终止动词 `.first()/.firstOrThrow()(RUNTIME.NO_ROWS)/.create(无 data 包裹)/.createAll/.createAndCount/.updateAll/.upsert({create,update,conflictOn})/.forUpdate()（事务行锁）`；`db.orm.public.User`（模型）/`db.sql`/`db.raw.sql`/`db.transaction`
- **v7→v8 类型陷阱**：**`Json` → `Jsonb`**（**ORM 8 的 `Json` = PG 旧 json 类型，几乎不想要**）；`@db.VarChar(255)` → `String(storage: varchar, length: 255)`；**`@default(uuid())` → `@onCreate(uuid())`**（@default 只剩数据库默认，写 uuid() 报 PSL_GENERATOR_IN_DEFAULT）；**裸 `DateTime` = timestamptz(3)**（v7 是 timestamp(3)——**列类型不同**，保旧列写 `DateTime(storage: timestamp)`）；v7 的 PG enum 用 `native_enum` + `pg.enum()`（普通 enum 存 text）；**隐式多对多没了——join 表显式建模**（`@@id([postId, tagId])`；v7 遗留 `_PostToTag` 用 @@map + @map("A")/@map("B") 保留）
- **CLI 重排**：`contract emit|format|infer`（infer=db pull）/`db init|update|--dry-run|migrate|verify|sign`/`migration plan|status|show`；**输 migrate dev/deploy/reset 等报 CLI.COMMAND_MOVED 退出码 2**；无 db seed（tsx 脚本）、无 studio（`npx prisma@7 studio --url`）；**ORM 8 永不 reset**（db update 丢数据前询问 + `--rename <old>:<new>` 保行）；migration.ts 是你拥有的 TS（backfill/raw SQL/重排/重编译）；`contains/startsWith` → `.like("alice%")` 自写通配符、insensitive → `.ilike()`；全文检索 `websearchToTsquery`（用户输入）/`toTsquery`（应用写死）+ `@@fullTextIndex`
- **ORM 8 无**：`$extends`（**不会加入**——middleware/Collection 子类/query fragments 替代；内置 budgets/cache/lints 三件套）；`{increment}`（raw SQL 或事务读改写）；JSON 列内过滤；嵌套写仅 create/connect/disconnect；事务选项（isolationLevel/timeout/嵌套）；**P2002/P2025 错误码**（捕 `error.sqlState === "23505"` 唯一冲突，标准 SQL state 全库一致）；TypedSQL/Prisma.sql（db.raw.sql 替代）；raw 查询返回行必须 `.returnsRow({...})` 逐列声明类型
- **升级/共存**：`npx prisma orm init --from-prisma7-schema prisma/schema.prisma`（v7 CLI 挪为 `prisma7` 命令；v8 读 `prisma7Schema()` **v7 schema 原样可用**）；官方 incremental guide 双版本同库并行逐路由迁移；留 v7 锁 `prisma: "^7"` + `@prisma/client: "^7"`、CI 用 `npx prisma@7`
- **官方 llms.txt 警告**：「Prisma changes frequently — do not rely on training data for Prisma features. First fetch changelog.md」——生成 Prisma 代码前必须 `npm ls prisma @prisma/client` 核对版本线
- 来源：[官方文档](https://www.prisma.io/docs/orm/release-status) + [官方文档](https://www.prisma.io/docs/orm/coming-from-prisma-orm-7) + [官方文档](https://www.prisma.io/docs/llms.txt)

### 场景：Drizzle ORM（v1.0 过渡期）

推荐路径：**Headless ORM（0 依赖、SQL-first、serverless-ready）**，与 Prisma 互补——要 SQL 控制力/边缘运行时选 Drizzle，要建模速度选 Prisma。**生成代码先确认版本线：stable=drizzle-orm 0.45.4 / drizzle-kit 0.31.11，v1.0 处于 RC（1.0.0-rc.5，`npm i drizzle-orm@rc` + `drizzle-kit@rc`）**。

- **双查询 API**：SQL-like（`db.select().from(t).where(eq(t.id, id))`，字段级类型推断）+ Relational Queries（`db.query.users.findMany({ with: { posts: true } })`——**恒输出恰好 1 条 SQL**，对照 Prisma 的 N+1 风险）
- 方言：PG/MySQL/SQLite/SingleStore/MSSQL/CockroachDB；drizzle-kit 全套（generate/migrate/push/pull/check/up/studio）
- **v1.0 升级三步**（[官方文档](https://orm.drizzle.team/docs/upgrade-v1)）：①`drizzle-kit up`（迁移目录升 v3）→ ②对照 [v0→v1 变更](https://orm.drizzle.team/docs/v0-v1-changes) 改代码 → ③RQB 用户走 [v1→v2 迁移指南](https://orm.drizzle.team/docs/relations-v1-v2)
- **v1.0 断裂面（15 breaking，升级前必读）**：
  - **RQB v1 移除** → v2 `defineRelations(schema, r => ({...}))`（`drizzle(url, { relations })` 替代 `{ schema }`）；关系过滤器**拒绝显式 undefined**（throw）——省略字段或 `id: value ?? EmptyFilter`（`drizzle-orm/relations`）；`where: { posts: true }` 要求有相关行 / `false` 要求无 / `{ posts: {} }` = 跳过
  - **Casing API 重做**：`drizzle({ casing: 'camelCase' })` 移除 → `snakeCase.table/view/materializedView/schema`、`camelCase.*`（pg-core）
  - **校验包并入主包**：drizzle-zod → `drizzle-orm/zod`（valibot/arktype 同理）；**typebox 双包**：`drizzle-orm/typebox`（typebox）与 `drizzle-orm/typebox-legacy`（@sinclair/typebox）；Effect → `drizzle-orm/effect-schema`（独立包 drizzle-effect-schema 不存在）；旧 0.x 包仍可用但新更新只进主包
  - **postgres-js JSON workaround 移除**：手动 `JSON.stringify` 补丁 MUST 删（驱动自序列化，保留即双重序列化）；sql 模板内 JSON 数组包 `sql.param(arr)`（否则按值列表展开）
  - **API 重命名**：`.enableRLS()` → `pgTable.withRLS('users', {...})`；`getTableColumns` → `getColumns`；`.generatedAlwaysAs()` 只收 SQL（`sql` 或 `() => sql`）；多维数组 `.array()` 不可链式 → `column.array('[][]')`
  - **读副本显式路由**：`withReplicas` 默认全走 primary（0.x 自动路由 select 到副本）；读走 `db.$replica.select()`
  - **DrizzleQueryError 默认不含查询参数**；`paramsInErrors: true` 开启（注意敏感参数入错误日志）
  - **关系查询 SQL 形态优化**：raw SQL 引用生成别名可能失效——改关系过滤器/排序，或该查询 `strategy: 'basic'` 退回旧形状
- **drizzle-kit v3（v1 配套）**：
  - 迁移目录 v3：journal.json 移除（SQL+快照进各迁移文件夹，**文件夹+快照一起进 VCS**）；`drop` 命令移除；DB 快照 → **DDL 快照**（首份全量+后续差分）
  - **迁移表新列 `name`（完整文件夹名）+ `applied_at`（timestamptz）**：迁移按文件夹名匹配（同秒生成也唯一），回填三策略（毫秒匹配→hash 决胜→仅 hash）；**migrator 应用所有缺失迁移**（与时间戳顺序无关）
  - **`schemaFilter` 默认管理所有 schema**（0.x 仅 public）——升级后 push/pull 会碰其它 schema，支持 glob（`['public', 'app_*']`）
  - **push 默认严格**：`--strict` 移除（确认数据丢失成默认），`--force` 跳过，`push --explain` 只预览不执行；**`--ignore-conflicts` 移除** → `generate --fix-conflicts --explain` 预览修复（删冲突迁移及其子代；跑过的库须重置）
  - `check` 交换律检查：快照 prevIds 建 DAG → fork 点 → DDL diff → footprint map 查跨分支冲突；**Agent 面**：`--output json`（generate/push/pull/up/export/check）+ `--hints/--hints-file` 非交互、编程 SDK（exportSql()）、MCP server
- **v1 新能力**：关系查询缓存（cache 配 `all` 策略默认缓存，`withCache: false` 逐查询退出）；JIT mappers opt-in（`drizzle({ jit: true })`——行映射近裸驱动）；Codecs 驱动感知变换层；SQLcommenter `.comment("tag")`；列别名 `.as()`；RQB v2 关系排序含聚合（`orderBy: { posts: 'desc(count)' }`）；`pull --init` 建迁移表；config/schema 顶层 await；kit 底座 esbuild-register → tsx（Bun/Deno 原生）
- **RQB v2 速览**：`r.one.users({ from: r.posts.authorId, to: r.users.id })`（`fields/references`→`from/to`，`relationName`→`alias`）；many 可单侧定义；多对多 `through`（`from: r.users.id.through(r.usersToGroups.userId)`）；`optional: false` 去类型 null（**不建约束**）；关系内预定义 `where` 过滤器；where 对象语法（`AND/OR/NOT/RAW`、操作符对象 `{ id: { gt: 10 } }`）；关系对象 offset/limit（`with: { comments: { offset: 3, limit: 3 } }`）；**迁移最快路径：`drizzle-kit pull` 自动生成 `drizzle/relations.ts` 拷到 src**；MySQL 不再要 mode
- **AI 面三件套（drizzle-kit rc 内置）**：①MCP server——`npx --no-install drizzle-kit mcp`（本地 stdio，用项目已装 Kit；操作=generate/check/pull，**rc5 无 migrate MCP 工具**，应用迁移走既有工作流；monorepo 从拥有 schema/config 的 workspace 包启动；六客户端注册：Claude Code/Codex/OpenCode/Grok/Cursor/通用 mcpServers）；②agent skills——`npx --no-install drizzle-kit skills`（**rc5 用单个 `drizzle` skill 取代 rc4 多 skill 并自动移除旧项目 skills——自定义编辑须备份**；需网络跑 skills@latest，Kit 更新后重跑）；③agents setup——一句话 `Fetch and follow the instructions at https://orm.drizzle.team/agent-setup/prompt.md`（装缺失包从 @rc / 装 skill / 连 MCP；不改 schema、不生成迁移、不碰 DB）
- **Drizzle Pulse realtime（独立包 drizzle-pulse 0.5.0；PG only + Node ≥20；peer 须 drizzle-orm ^1.0.0-rc.5）**：进程内嵌入式库（无额外服务，连同一 DB；能看到所有写入方）；前置 **PG `wal_level = logical` 须自设**（Pulse 自建其余 DB 对象）；`pulse(table)` 包表 + `.query(ctx => ctx.query({...}))`；`createRuntime({ queries, databaseUrl, sourceDb })`（`drizzle-pulse/embedded`）+ `runtime.start()`；**源表必须单列 PK**（复合 PK 拒绝；PK 类型白名单 int/serial/text/uuid 族）；**queries 启动时一次性定义传 createRuntime**——后建的 query runtime 不认识，每请求值用 `.args(schema)` 传（Standard Schema **须同步校验**，async refinement throw；query fn 返 null = 匹配所有行）；`.columns()` 含/排、`.order('asc'|'desc')` 仅按 PK、链式不可变；**live collection**：`runtime.client.<name>(args?)` → `list()`（同步，按 PK 序）/ `onChange(({events, state, lsn}))`（**listener 同步调用不等待返回的 Promise——async listener 须内部自捕获，否则 unhandled rejection 杀进程**）/ **`onResync()`（断线重连后 onChange 不补发丢失变更——用 state 渲染的代码必须 onResync 重发全量）** / `onError()` / `dispose()`；**CDC 事件流**：`runtime.events.<name>(args?, cb, opts)`（无行、无首载、只报订阅后变更；insert=行开始匹配、delete=行停止匹配——状态变更在不同查询表现为不同事件；**同 commit 断线后可重复投递，副作用用 `(event.pk, lsn)` 幂等键**）
- NestJS 集成形态：Drizzle 实例经 factory provider 注入（useFactory 传连接串），`onModuleDestroy` 释放（LAW-12）；schema 校验可用 `drizzle-orm/zod` 与 Nest 12 Standard Schema 双轨合流；Pulse runtime 同理经 provider 管理（`onModuleInit` start / `onModuleDestroy` 停）[推断]
- 来源：[官方文档](https://orm.drizzle.team/docs/overview) + [官方文档](https://orm.drizzle.team/docs/upgrade-v1) + [官方文档](https://orm.drizzle.team/docs/v0-v1-changes) + [官方文档](https://orm.drizzle.team/docs/relations-v1-v2) + [官方文档](https://orm.drizzle.team/docs/drizzle-kit-mcp) + [官方文档](https://orm.drizzle.team/docs/drizzle-kit-skills) + [官方文档](https://orm.drizzle.team/docs/agents) + [官方文档](https://orm.drizzle.team/docs/realtime-overview) + [官方文档](https://orm.drizzle.team/docs/realtime-queries) + [官方文档](https://orm.drizzle.team/docs/realtime-live-collections)

### 场景：WebSockets 实时通信（gateway）

推荐路径：`@WebSocketGateway()` + `@SubscribeMessage('event')`；平台无关（socket.io 与 ws 内置支持）。

- **gateway 是 provider**——未在 module providers 数组引用前**不会实例化**；默认与 HTTP server 同端口；`@WebSocketGateway(80, { namespace: 'events' })`
- `@MessageBody()`（属性键提取）+ `@ConnectedSocket()`；**勿裸取 (client, data) 参数——单测须 mock socket**
- **返回值语义**：return → 隐式 ack（客户端须带 ack 回调）；省略 return/null/undefined → 不响应；**false/0 等 falsy 值仍发送**；`client.emit()` 直发绕过 interceptors；`@Ack()` 注入 ack 回调后 Nest 不再自动 ack
- 多值响应返回 `{ event, data }`（WsResponse）；**ClassSerializerInterceptor 忽略纯对象——须返回实现 WsResponse 的 class 实例**
- 生命周期：OnGatewayInit/OnGatewayConnection/OnGatewayDisconnect；**Nest 不等 async handleConnection——不是闸门**（期间消息照常处理；逐消息校验用 guards，连接前拒绝用 connection 级 middleware：socket.io `server.use()` / WsAdapter verifyClient）
- request-scoped gateway（v12）：每连接一套实例（REQUEST token 注入 socket），断开销毁；有开销——默认 singleton
- 来源：[官方文档](https://docs.nestjs.com/websockets/gateways)

### 场景：CQRS（@nestjs/cqrs）

推荐路径：复杂领域用 CommandBus/QueryBus/EventBus 三总线分离读写；简单 CRUD 不必上 CQRS。

- `CqrsModule.forRoot()`；`@CommandHandler/@QueryHandler/@EventsHandler`；`Command<T>`/`Query<T>` 基类定义返回类型（execute() 推断 Promise<T>）
- 聚合根三法：继承 `AggregateRoot`（apply 入队 + commit 派发；`EventPublisher.mergeObjectContext()` 连接 EventBus；autoCommit 即时派发）/ **`WithAggregateRoot(Base)` mixin（既有继承体系）** / 实现 IAggregateRoot（框架无关）
- **12.1 事务性派发**：`await hero.commit({ transaction: tx })`——commit 返回 event bus 结果并接 dispatcher context；立即清空事件不会双发
- **事件 handler 在 HTTP 请求上下文之外**：错误 exception filter **捕不到**（自行 try/catch 或补偿 saga）、不能发 HTTP 响应（用 WS/SSE）；command handler 返回值可回 HTTP 响应
- **Sagas 纯内存**：`@Saga()` + `ofType(Event)` → Observable\<ICommand\>；跨重启用 **Durable saga**（`@nestjs/workflows/cqrs`：@StartOn/@SignalOn + PostgresWorkflowStore；`eventBus.publish(event, { transaction: tx })` 同事务建 workflow）
- **request-scoping**：bus 是 singleton，但 request-scoped handler 每消息自动新实例；请求上下文用 `AsyncContext` + `execute(cmd, myRequest)`；**sagas 恒 singleton**（request-scoped saga 不可用）
- 未处理异常走 `UnhandledExceptionBus`（rethrowUnhandled 默认 false）；三总线均为 Observable 可订阅全事件流（event store）
- 来源：[官方文档](https://docs.nestjs.com/recipes/cqrs)

### 场景：日志（内置 Logger）

推荐路径：**内置 Logger + JSON 输出即生产级**——stdout 一行一 JSON、结构化参数可查询、平台（CloudWatch/Datadog/Loki）直采；Pino/Winston 仅在需多 transport（文件/syslog）、字段 redaction、超高频吞吐时引入。

- 生产配方：`new ConsoleLogger({ json: true, logLevels: ['log', 'warn', 'error', 'fatal'] })`；JSON 字段：level/pid/timestamp（epoch 毫秒）/message/context/stack/params；error → stderr 其余 stdout
- **log levels 级联**：数组按最严重级向上全开（`['log']` 也开 warn/error/fatal）；`filterLogLevels('>=warn')` 助手适合环境变量；`app.useLogger()` 运行时改
- **结构化参数（v12）**：消息后的纯对象作 params 附同一条目（多对象合并）；JSON 模式嵌 `params`，`flattenParams: true` 展平根级；数组/字符串/类实例不算参数
- 惰性消息 `logger.debug(() => ...)`（level 未启用不调用）；forceConsole（Jest 缓冲 console 时用）
- DI 自定义 logger：LoggerModule + **TRANSIENT scope**（各消费者独立 setContext）+ `bufferLogs: true` + `app.useLogger(app.get(MyLogger))`；**provider/hook 内 process.exit() → buffer 永不打印（改抛错）**
- 来源：[官方文档](https://docs.nestjs.com/application/logger)

### 场景：文件上传与流式响应（Multer/Fastify multipart）

推荐路径：**Express 默认 = Multer**（multer 2.5.0，@nestjs/platform-express 12.5.0 内置）。五拦截器：`FileInterceptor('file')`+`@UploadedFile()` 单文件 / `FilesInterceptor(field, maxCount)`+`@UploadedFiles()` 同字段数组 / `FileFieldsInterceptor([{name,maxCount}])` 多字段 / `AnyFilesInterceptor()` / `NoFilesInterceptor()`（multipart 无文件：字段进 body，带文件 400）。

- **默认 memoryStorage()（file.buffer 进内存）且 Multer 默认不限大小——内存模式 MUST 设 `limits.fileSize`**（达限即拒 413，不落内存/盘；优于 MaxFileSizeValidator 全收后再验）
- 验证：`ParseFilePipe({validators})` + `MaxFileSizeValidator` / `FileTypeValidator`（**magic number 验 MIME，非扩展名**）；`ParseFilePipeBuilder` 链式（`fileIsRequired: false`）；自定义继承抽象类 `FileValidator`（isValid 可 async）
- **Nest 侧加固默认（Multer 本身无限）**：12.5 起 `limits.parts`=1000；12.2 起 `fieldNestingDepth`=32、`fieldArrayIndexLimit`=1000；`MulterModule.register/registerAsync` 全局默认——12.0.4 起 limits 与路由按 key 合并、12.5 起 undefined/null 路由选项被忽略、Infinity 解除
- diskStorage() 流式写盘（file.path 替代 buffer）；**文件不自动删——处理完含失败 MUST unlink()**；12.2 起 pipe 拒绝时已存盘文件随错误响应自动删；外送 S3/R2 用 `@nestjs/storage` 的 `uploadToDisk()` 流式直送
- **Fastify（12.1+）**：`@nestjs/platform-fastify/multipart` 同名拦截器、类型 `UploadedMultipartFile`、`MultipartModule`；**fileSize 默认 = bodyLimit 1 MiB（比 Multer 严）**；插件自动注册（全局拦截器/懒加载模块须 `multipart: true`，**init 后直接在 Fastify 实例注册 → FST_ERR_DEC_ALREADY_PRESENT**）；`FileStreamInterceptor()` 流式（字段须在文件前/仅单文件/MaxFileSizeValidator 不适用/回应前先读完防 EPIPE）
- 回发文件：`StreamableFile`（Readable/Uint8Array；`type`/`disposition`/`length` 选项；`@Res({passthrough: true})` 运行时设头）；12.2 起流错误响应体不含错误信息（防路径泄漏）
- 来源：[官方文档](https://docs.nestjs.com/http/file-upload)

### 场景：部署与 Docker（nest deploy / Mau）

- 构建：`npm run build`（nest build）→ `dist/main.js`；**坑：项目根目录存在 .ts 文件时入口漂移为 `dist/src/main.js`**；运行 `NODE_ENV=production node dist/main.js`（前提 Node 20.19+/22.12+）
- **Docker 官方示例**（Docker 菜谱已并入 deployment 页）：node:24 基镜像、COPY package*.json → `npm install` → COPY . . → `npm run build` → EXPOSE → `CMD ["node", "dist/main"]`；.dockerignore（node_modules/dist/*.log/*.md/.git）
- **`nest deploy`（v12 CLI 内置）+ @nestjs/mau**：官方 AWS 部署平台 Mau（托管 PG/MySQL/Mongo/Redis/RabbitMQ/Kafka/NATS/CRON/lambda/CI-CD）；CI 无交互环境 `npm i -g @nestjs/mau && mau deploy`
- 健康检查 @nestjs/terminus；伸缩：垂直（升配）/水平（Docker+K8s+LB 多实例）
- **可观测：NestJS Observe**（@nestjs/observe 0.3.26，官方 APM）：`NestFactory.create(AppModule, { instrument: ObserveInstrument })` 自动上报请求/任务/错误/trace——接入全流程与 APM 选型见下方「可观测性」场景
- 来源：[官方文档](https://docs.nestjs.com/deployment)

### 场景：可观测性（NestJS Observe 深化 / OpenTelemetry 双轨）

**@nestjs/observe 0.3.26 = 官方 APM（请求/任务/错误/trace/日志关联一体）；硬门槛：@nestjs/core ≥11.1.4（instrument 钩子）+ Node ≥20.19；GraphQL 另需 @nestjs/graphql ≥13.4.4。**

- **接入三步**：app.module.ts 顶层 `createObserveModule()` 一次（返回配对 ObserveModule+ObserveInstrument）→ `ObserveModule.forRoot({ appKey, appSecret, serviceId })` → `NestFactory.create(AppModule, { instrument: ObserveInstrument })`；或 `npx @nestjs/observe link` 一键（8 字母码 15 分钟过期、observe.nestjs.com/link 批准；写 .env 的 OBSERVE_APP_KEY/SECRET + .gitignore + 给 nest start 脚本加 `--env-file .env`，start:prod 不动；**每台机器各跑一次**）；凭证回退读环境变量；**关闭上报用 `enabled: false`，勿传假凭证**；测试套件 `shutdownFlushTimeout: 0` 防 close 发遥测
- **FastifyAdapter 陷阱**：options 挪第三参 `create(AppModule, adapter, { instrument })`——第二参传 options 被静默丢弃、SDK 永不挂上
- **自动插桩**：数据库**驱动级**（pg/mysql2/mssql/mongodb 检测即插——覆盖 TypeORM/MikroORM/Drizzle/Mongoose/Prisma driver adapters；字面量全移除、重复查询折叠 `SELECT order_items ×47`；Knex/Sequelize 的 SQL Server 走 tedious 未覆盖）；出站 HTTP 走 Node diagnostics_channel 零 patch（fetch/undici/node:http 全家、trace id 自动出站）；**DI 容器外创建的 Redis/Kafka 客户端不记录**；LLM 调用识别（OpenAI/Anthropic/Gemini/Bedrock 等，仅 fetch——axios 不算；prompts/completions 永不外发）；bullmq/bull 每 processor 一 job；`runtimeMetrics` 60s 采样兼**心跳**（静默告警=免费 uptime 监控）
- **TracerService**（全局注入）：`createSpan(name, cb)` 嵌套瀑布（**命名描述工作而非调用方**——跨路由聚合）/ `captureError(error)` 已处理错误 / `setAttribute/getAttribute` 请求级存储 / `currentTraceId()` trace 外返 null 不抛 / `counter·gauge·summary` 自定义指标（**与 trace 无关、可任意处上报**）；**trace 上下文外调 createSpan 会抛**（故意设计——静默丢 span 更难发现）
- **trace 传播**：HTTP 双向自动（入站收 x-request-id、出站自动加）；队列 job 继承 trace id（`observeTraceId` option、W3C traceparent 0.3.23+）；**@nestjs/microservices 12.0.4+（TCP/Redis）·12.3.3+（NATS/Kafka/RabbitMQ/MQTT 5/gRPC）自动携带——更早版本需应用代码转发 + 覆写 traceIdGenerator**；`openTelemetry` 选项接 W3C traceparent（同进程 OTel SDK 定 trace id）；`otlp` 选项导出 span 到自家 OTLP/HTTP 后端（端口 4318，**gRPC 不支持**；Observe 不 ingest OTLP、自家 span 可出）
- **错误监控**：逃逸错误自动捕获（HTTP/GraphQL/gRPC/microservices/队列/cron）——**无需注册 handler、exception filter 照常决定响应，SDK 并行观察**；`sourceContext` 默认开（错误帧带源码片段——node_modules 永不读）；redaction 默认开（bearer/JWT/AWS key/卡号 Luhn）；**release 归因靠 serviceVersion——自建容器 build 时 `--build-arg GIT_SHA` + ENV OBSERVE_SERVICE_VERSION**
- **APM 选型铁律**：通用 APM agent 靠 patch 库——**必须 preload 先于 @nestjs/core/AppModule**（--require CJS / --import+loader hook ESM；模块内启动不可靠）；OTel 的 `@opentelemetry/instrumentation-nestjs-core` **仅支持 core <12——Nest 12 上三个 Nest span 全无**（只剩 HTTP+DB）；Sentry Nest 管道 span 最全（middleware/guards/pipes/interceptors/filters/handler）；Datadog（NestJS 不在框架列表）/ New Relic（core 10+ 在列表但 BullMQ 不支持）/ Elastic（ESM 实验性子集）各有缺口；**组合不互斥**：Observe+OTel 接同一 trace、Observe+otlp 指向平台 OTLP 口、Observe+Sentry（前端 Sentry 后端 Observe）
- **Observe MCP**（付费）：`POST https://observe-api.nestjs.com/mcp`（Streamable HTTP 无状态；OAuth 或 omcp_ token **只显示一次**）；agent 两时刻：改前 `get_context_pack`（~2500 token 项目简报：热路径/flaky 依赖/SLO）、部署后 `get_release_verdict` / `verify_fix`；调查链 find_regressions → get_operation_details → get_trace（跨服务瀑布）
- 来源：[官方文档](https://docs.nestjs.com/observability/sdk.md) + [官方文档](https://docs.nestjs.com/observability/manual-instrumentation.md) + [官方文档](https://docs.nestjs.com/observability/distributed-tracing.md) + [官方文档](https://docs.nestjs.com/observability/choosing-an-apm.md) + [官方文档](https://docs.nestjs.com/observability/error-monitoring.md) + [官方文档](https://docs.nestjs.com/observability/mcp-server.md)

### 场景：文档站重构后的一等包生态（12 官方版图）

**docs.nestjs.com 已全面重构**（application/http/observability/reliability/mcp/ai 分区；旧 recipes/docker 移除；llms.txt 索引 + llms-full.txt 全文）。官方一等包从「DI/平台核心」扩容到全后端版图——**生成集成代码前先查官方包是否已存在，勿默认第三方**：

- **可靠性四件套**：@nestjs/resilience（retry/timeout/circuit breaker/bulkhead/fallback 装饰器）/ @nestjs/idempotency（Idempotency-Key 每键一次）/ @nestjs/outbox（事务性 outbox）/ @nestjs/workflows（durable workflows 跨重启）+ @nestjs/locks（分布式锁单实例执行）
- **MCP**：@nestjs/mcp（tools/resources/prompts 为 provider 方法；Streamable HTTP + stdio 双 transport；从 @rekog/mcp-nest 迁移基本机械改名）
- **AI**：@nestjs/ai（模型注册按名注入/超时重试 fallback/schema 校验/agent 工具循环/embeddings；测试用 FakeModel 逐答录音）
- 应用层：@nestjs/mail、@nestjs/storage（本地/S3/R2）、@nestjs/webhooks（签名+重试+raw body 验签）、@nestjs/i18n、@nestjs/authentication、@nestjs/authorization
- **StandardSchemaValidationPipe（新验证面）**：Standard Schema 直用——`@Body({ schema: zodSchema })` 装饰器级校验（与 ValidationPipe/class-validator 双轨并存）
- tsx 直跑（无脚手架）：`npx tsx main.ts` + experimentalDecorators；**tsx 不发射装饰器元数据 → 注入必须显式 `@Inject(Token)`**
- 来源：[官方文档](https://docs.nestjs.com/llms.txt)

### 场景：弹性与可靠性（@nestjs/resilience / idempotency / outbox）

**选型判定：三包均 pre-stable（resilience 0.0.3 / idempotency 0.0.4 / outbox 0.1.4，Nest 11-12）——生产选用前评估；训练记忆中的第三方替代（opossum 类 breaker、自研幂等表）仍常见，生成代码先 `npm ls` 确认。**

- **resilience 装饰器边界**：@Retry/@Timeout/@CircuitBreaker/@Bulkhead/@Fallback/@Resilience(preset)/@Signal()（AbortSignal 注入）**仅作用 entrypoints（controller/resolver/handler/gateway）——provider 方法上无效（WARN）→ 服务内 ResilienceService.preset()/create() policy 对象**；preset 共享 breaker/bulkhead 实例（按名）；defaults 只填字段不开 stage
- **重试安全面**：HTTP 仅 GET/HEAD/OPTIONS——**POST 被 skip + WARN，@Retry({ idempotent: true }) 显式声明**；GraphQL query 重试/mutation 需 idempotent；message/WS 仅 handler 级 @Retry；客户端错误（4xx）不计失败；**408/429 例外计为依赖失败**；超时 per attempt → 504（非 408）；breaker 开 → 503 + Retry-After（非 429）；**状态 per-process**（多实例各开各、重启清零）；breaker MUST 配 timeout（悬挂 probe 卡 half-open）
- **IdempotencyModule MUST 先于 ResilienceModule**（全局拦截器外层序：重放先于 retry/breaker）；@Idempotent()=客户端重放去重 vs `idempotent: true`=服务端单请求内重跑——两个问题
- **idempotency**：409 `IDEMPOTENCY_KEY_IN_USE`/422 `IDEMPOTENCY_KEY_REUSED`/400 `IDEMPOTENCY_KEY_REQUIRED`；scope 每用户命名空间；**store 默认 InMemory——production 拒绝启动（除非 allowInMemoryStorage）**；PG 单语句 `INSERT ON CONFLICT DO UPDATE WHERE expires_at<=now` 原子 + owner fencing token；**response 列 json 非 jsonb（jsonb 拒 `\u0000`）**；TypeORM 禁 save()（竞态）；AES-256-GCM 加密 + 多 key 三步轮换，key 移除过早 fail closed（防双扣款）；契约套件 @nestjs/idempotency/testing（32 并发 race）
- **outbox**：`outbox.add(tx, msgs)` **MUST 传事务句柄（传 db 抛 OutboxTransactionRequiredError）**；commit 后 `outbox.notify()` 唤醒 relay；schema `nest_outbox` 自管理（dev 自动迁移/production `npx @nestjs/outbox migrate`，status 退出码 1 作 CI 检查）；`@OnOutboxMessage` + inbox 按 id 去重；**`ctx.processInTransaction(tx, work)` exactly-once（同库写）**；NonRetryableMessageError 直接入 DL；**同 key 按事务提交序保序**（重试时后续等待）；OUTBOX_RELAY=off API-only 实例；**READ COMMITTED 要求**；TCP transport 仅保证字节发出——不可丢事件用 Kafka/RabbitMQ confirms/NATS JetStream
- 来源：[官方文档](https://docs.nestjs.com/reliability/resilience.md) + [官方文档](https://docs.nestjs.com/reliability/idempotency.md) + [官方文档](https://docs.nestjs.com/reliability/outbox.md)

### 场景：AI 集成与 MCP server（@nestjs/ai / @nestjs/mcp）

**选型判定：@nestjs/ai 0.0.2（peer ai ^7——每大版本对应一个 Vercel AI SDK 大版本；Node ≥22）/ @nestjs/mcp 0.0.4（Node ≥20.19）——均 pre-stable；社区记忆主流（@rekog/mcp-nest、直接 ai-sdk 调用）仍适用，先确认版本线。**

- **@nestjs/ai**：AiModule.forRoot({ isGlobal, models: { default, fast: { model, fallback } }, defaults })；模型调用跑在 @nestjs/resilience 策略上；generateText/generateObject（Zod schema；**AiOutputError 不重试不 fallback——模型已答**；transform 跑在答案上）；`@AgentFunction()` 方法=模型工具（走 guards/pipes/filters，以用户身份）；@ai-sdk/openai-compatible 单包多 provider（provider 数据化，重启生效）；durable agent runs（配 workflows 审批）；预算 budget maxTokens/maxCost + onUsage 成本记录；测试 FakeModel
- **@nestjs/mcp**：McpModule.forRoot({ name, version, instructions })；端点 `/mcp`；@Tool/@Resource/@ResourceTemplate/@Prompt 装饰器；**Zod 3 schema 启动即拒——Zod ≥4.2/ArkType 原生、Valibot 经 toStandardJsonSchema()**；启动失败项（重名/命名规则/request-scoped/scopes 无 auth）；**每请求独立实例无状态——多实例免 session affinity**
- MCP 生产面：**Origin 默认仅 localhost 页面放行（无 Origin 放行——CLI/助手不受影响）**；allowedHosts 防 DNS rebinding；body limit（Express 默认 100KB）；浏览器客户端 CORS 双边；OAuth 2.1 或 API key guard（timingSafeEqual）；stdio 传输 **McpStdioLogger MUST（stdout 载协议）**；一构建双 transport（main.ts + stdio.ts）
- 来源：[官方文档](https://docs.nestjs.com/ai/overview.md) + [官方文档](https://docs.nestjs.com/mcp/overview.md)

### 场景：Durable workflows 与分布式锁（@nestjs/workflows / @nestjs/locks）

**选型判定：workflows 0.0.5 / locks 0.0.6——pre-stable，选用前评估（gotchas #91）。与 BullMQ/CQRS saga 三分法：BullMQ=单件后台任务；saga=进程内事件反应（可丢在途状态）；workflows=多步+跨天等待+必须活过重启+失败补偿。**

- **workflows**：`@Workflow('name')` + `run(ctx, input)`；`ctx.step(name, fn, { retry, compensate })` journal 化——重启后 run() 从头重放、已完成 step 返回记录值（**结果必须 JSON 可序列化，Date→string，`Journaled<T>` 标记**）；**step at-least-once → 副作用必须幂等**（引擎发稳定 idempotencyKey `<instanceId>:<stepName>`）；`NonRetryableStepError` 立即失败；compensate 逆序补偿；`ctx.commit()` 不可逆点（弃补偿）；`waitForSignal/waitForAny/timer/sleep`（信号持久化、先到有效、每实例至多消费一次）；worker 内嵌进程（leaseDuration 30s、每秒 poll、**SIGTERM 需 enableShutdownHooks**、`worker:false` 给 API pod）；step 默认 3 attempts backoff 1s 翻倍 cap 5m；`@Workflow('name', { timeout: '30d' })` run 级超时；实例 id 幂等（同 id 同 input 返回现存，异 input 抛 `WorkflowIdConflictError`）；状态机 8 态含 **compensation_failed**；`retry()` 拒绝已补偿实例、`terminate()` 不跑补偿；`ctx.setStatus()` 16KiB customStatus（**勿把原始 instance 返回给客户**）；store `PostgresWorkflowStore`/`MySqlWorkflowStore`（MariaDB 不支持；MySQL 键长 255/512 限、deadlock 1213 重跑整事务）
- **locks**：`@OnOneInstance({ key })` + `@WithoutOverlapping()`（包装方法，@nestjs/schedule 不知情）；**包不自带共享 store**——`LockStore` 契约 acquire/renew/release 自实现（`lockStoreContract()` 套件验）；**acquire 必须单条原子语句**（INSERT ON CONFLICT DO UPDATE WHERE owner IS NULL OR expired）；fencing token 从 sequence（`greatest(nextval, row+1)` 防序列回退）；**release 保行清 owner 不 DELETE**；`clock_timestamp()` 非 `now()`；**不用 pg_advisory_lock**（绑 session 占连接、不能续租、无过期无 token）；ttl 默认 30s 心跳 ttl/3；storeTimeout 10s；**key 默认 ClassName.methodName——改名改 key，滚动部署新旧各跑一次**；**错过的 tick 不补**——写「做所有该做的」任务；暂停持有者（GC/VM 迁移）迟到写入靠 **fencing token**（`WHERE token <= :t` 写 0 行）+ `LocksContext`（AsyncLocalStorage）AbortSignal/LockLostError；`Locks.withLock(key, fn, { wait })` 手工触发互斥（`LockNotAcquiredError` 不带 HTTP 状态）；leader election=同一租约
- 来源：[官方文档](https://docs.nestjs.com/reliability/workflows.md) + [官方文档](https://docs.nestjs.com/reliability/locks.md)

### 场景：webhooks、邮件与文件存储（@nestjs/webhooks / @nestjs/mail / @nestjs/storage）

**选型判定：webhooks 0.0.4（依赖 @nestjs/outbox）/ mail 0.0.2（零第三方依赖；与 @nestjs-modules/mailer API 完全不兼容）/ storage 0.0.5（S3 走 fetch+SigV4 无 AWS SDK）——均 pre-stable（gotchas #91）。**

- **webhooks 双向**：出向 `webhooks.dispatch(tx, { type, tenant, data })` = Outbox.add（业务同事务；commit 后 fan-out worker 签名发送）；**无 OutboxModule 启动失败**；入向 `@VerifyWebhook('name')` raw body 验签 + inbox 去重（`NestFactory.create(app, { rawBody: true })` 必须开）；Standard Webhooks 头（webhook-id/timestamp/signature v1 HMAC-SHA256）；secret `whsec_` **只显示一次**、rotateSecret 旧 secret 续签 24h；**SSRF 防护：只收公网 https://（allowHttp/allowPrivateNetworks 默认 off），169.254.169.254 永久封禁，每次发送重跑 URL 检查（DNS 会变）**；重试 10 attempts 5s×4 cap 1d（≈两天）；410 立即禁端点；429/502/503/504 暂停端点尊重 Retry-After；3xx 不跟随；delivery timeout 15s；`disableEndpointAfter '5d'`；租户隔离（他租户 id 一律 404）；eventTypes 白名单；**message body 是 text 不是 jsonb**（jsonb 重排字节毁签名重放验证）
- **mail**：`MailModule.forRoot({ transport, templates, from })`（global，提供 Mailer）；transport 继承 `MailTransport` 抽象（FileMailTransport 仅开发/SMTP/Resend/Postmark/SendGrid/SES）；**MUST：attachment path 绝不来自用户输入；发邮件绝不在数据库事务内**（提交后经 outbox；配 outbox 时 `retry: false` 防两层重试相乘）；模板 Handlebars 子集**无 helpers 无表达式**（TS 编译不拷 HTML——nest-cli.json `assets`+`watchAssets`）；`mailer.send(MailClass, { to, data, locale?, idempotencyKey? })`（逗号地址列表 throw）；临时失败默认重试 3 次（5xx 永久 550；greylist/429/超时临时）；idempotencyKey→Message-ID（Resend 拒重复 24h；Postmark/SendGrid/SES 无幂等键可能双发）；SMTP 587 STARTTLS/465 TLS、pool 默认 5 连接 100 邮件；DKIM Ed25519 接收方支持不全——RSA 稳妥；i18n locale 必须显式传（outbox 场景无请求上下文）
- **storage**：`StorageModule.forRoot({ disks, default? })`；LocalDisk/S3Disk/InMemoryDisk（测试）；**MUST：生产绝不用 LocalDisk（production 打 warning）；公开/私有必须分盘分 bucket（无 per-file ACL）；签署密钥≥32 字符**；S3 兼容矩阵（AWS/R2 `region:'auto'`/MinIO `forcePathStyle:true`/GCS endpoint+HMAC）；`signedUrl` 默认 15 分钟最长 7 天（**签名不可撤销**）；`uploadToDisk()` 作 FileInterceptor storage：**魔数检测类型（永不信客户端 mimetype）**，不匹配 415 零字节写入；key 校验拒 `..`/绝对路径/控制字符；直传完成回调 MUST：验 key 前缀+stat 复查+前 16 字节复查，盘间流式 get→put；S3 multipart partSize 8MiB concurrency 4、**IAM 缺 ListBucket 时 404 变 403**；错误体系 StorageError 系非 HttpException（KeyConflict 409：本地盘不能同时有 `a` 与 `a/b`）
- **五包共性契约（idempotency/outbox/workflows/webhooks/locks）**：默认 InMemory，**NODE_ENV=production 无共享 store → 启动失败**（allowInMemoryStorage 豁免）；schema `nest_*` 自管理（dev 自迁移，**production `npx <pkg> migrate` + `status` 退出码 1 作 CI**）；executor 统一 fromDrizzle/fromTypeOrm/fromPrisma/fromKysely；**事务句柄 MUST**（传 db 抛 TypeError）；READ COMMITTED 强制；fencing token 防迟到写入
- 来源：[官方文档](https://docs.nestjs.com/http/webhooks.md) + [官方文档](https://docs.nestjs.com/application/mail.md) + [官方文档](https://docs.nestjs.com/application/file-storage.md)

### 场景：进程内事件与请求上下文（@nestjs/event-emitter / AsyncLocalStorage）

- **EventEmitterModule 全选项**：`forRoot({ global, addToRequestScope, isNewAllowed, delimiter })`；`addToRequestScope: true` 后 `@OnEvent()` 支持自动清理的 request-scoped 监听器；`isNewAllowed` 允许已就绪后再注册新监听器
- **@OnEvent 事件名**：默认 `:` 分隔（`user.created`→`@OnEvent('user.created')`）；嵌套对象可响应 `hostname`；`@OnEvent(['a', 'b'])` 多事件数组；`EventEmitter2` 通配符 `user.*`（v3 通配符默认**关闭**——`wildcard: true` 才开，否则 `user.*` 匹配不到 `user.created`）
- **监听器执行语义**：默认**串行**（await 完一个再下一个）；`asyncFuncsTarget` 改并行；`promisify: true` 支持同步监听器返回 Promise；**priority 只影响同步监听器排序，async 监听器不参与 priority 且不阻断后续**；监听器抛错 → 未捕获异常（无全局 filter 兜底，同 CQRS 坑 13）
- **bootstrap 前发事件 [NE-12]**：`onModuleInit`/`onApplicationBootstrap` 时监听器未必注册完——**先 `await this.readinessWatcher.waitUntilReady()` 再 emit**；而 bootstrap 之后请勿再调用（语义反转为等新监听器注册、可能丢上下文）
- **请求上下文传递三选型**：
  - **EventEmitterModule 自带**：`forRoot({ addToRequestScope, inheritRequestContextId: true })`——事件携带请求上下文（企业版特性语义，社区版以 ALS 实现）
  - **自建 AsyncLocalStorage 模式（官方 recipe）**：request-scoped 中间件 `als.run({ reqId, ... }, next)` + 注入 `ClsService` 类似的 typed accessor；子进程/新异步链脱离上下文需显式重绑
  - **第三方：nestjs-cls**：`ClsModule.forRoot({ middleware: { mount: true, generateId: true, setup: ... } })`——`clsService.get()/set()/run()`；**官方警告：ALS 勿当 God object**（全 app 状态塞 ALS → 隐式依赖不可测）；trace 上下文优先 **@nestjs/observe TracerService**（`inject(TracerService)`，与 Observe 体系一体）
- 来源：[官方文档](https://docs.nestjs.com/application/events.md) + [官方文档](https://docs.nestjs.com/recipes/async-local-storage.md)

### 场景：缓存（@nestjs/cache-manager / Keyv）

- **注册**：`CacheModule.register({...})` / `registerAsync({ useFactory | useClass | useExisting })`（异步时 useFactory 最常用，可注入 ConfigService；三种 provider 模式任选）；`isGlobal: true` 免逐模块 import
- **底层引擎是 Keyv**：stores 数组多 store（第一个为默认，依次回退）；`ttl` 毫秒（**非秒**，同 throttler ttl 语义）
- **注入使用**：`@Inject(CACHE_MANAGER) private cache: Cache`；`await cache.get(key)` / `cache.set(key, value, ttl?)` / `cache.del(key)` / `cache.clear()` / `cache.wrap(key, fn)`（get-miss-else-set）
- **get miss 返回值 [NE-13]**：新版本返回 `undefined`；**cache-manager v6 返回 `null`**——判断 miss 须两者都当 miss
- **内存 store 存引用不存副本 [NE-13]**：`get()` 拿到的是 `set()` 传入的同一对象——修改它会直接污染缓存；Redis 等外部 store 走序列化无此问题，但换 store 会悄悄改变语义
- **CacheInterceptor 自动响应缓存**：默认**仅 GET**；显式 `@CacheKey()` 后 POST 等也可缓存；`@Res()`（框架托管响应）的路由**不可用**拦截器缓存
- **GraphQL 不适配**：拦截器对每个 field resolver 单独执行——查询结果被缓存是未定义行为，勿在 GraphQL 用 CacheModule 自动缓存
- **WS/RPC（GQL subscription/microservices）**：缓存键无 HTTP 请求可用——**必须显式 `@CacheKey()`** 才有键
- **@CacheTTL / @CacheKey**：方法级覆盖 controller 级；`@CacheTTL` 无 `@CacheKey`（无论显式还是 HTTP 路径推导）时不生效
- **trackBy**：`CacheModule.register({ trackBy: (ctx) => ... })` 自定义缓存键推导（如忽略 query 中 time 参数）
- **Redis store 红线 [NE-13]**：Keyv 的 Redis store 连接错误若无人监听 `'error'` 事件会抛未捕获异常**拖垮整个应用**——注册后立即挂 error listener（日志降级 + 可选熔断）；生产建议专门封装缓存健康检查
- **类型安全**：`cache-manager` v6+ 泛型 `Cache<Store>`——避免 `as` 断言，键拼接收拢到 typed helper
- 来源：[官方文档](https://docs.nestjs.com/data/caching.md)

## 高频坑点（速查）

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| 1 | `Nest can't resolve dependencies of the XService (Y, ?)` | 注册链断 | [NE-2] 排查 5 步 |
| 2 | ValidationPipe 开着，非法字段照样通过 | DTO 是 interface | [NE-1] class/Schema |
| 3 | 子对象内的非法字段不报错 | 嵌套校验漏 @Type | `@ValidateNested() @Type(() => X)` |
| 4 | 接口 200 但 body 为空 | interceptor 忘 return | `return next.handle()` [NE-4] |
| 5 | 全局 Guard 拿不到 ConfigService | app.use* 不进 DI | APP_GUARD token [NE-3] |
| 6 | update 不触发 hooks；事务部分不回滚 | save/update 语义混；事务混用全局 repo | [NE-5] 回调内全用 manager |
| 7 | `client.send()` 后远端无日志 | 冷 Observable 未订阅 | firstValueFrom [NE-7] |
| 8 | SIGTERM 后连接泄漏 | 未开 shutdown hooks | `app.enableShutdownHooks()` [NE-6] |
| 9 | 某接口每请求整链重建，性能塌方 | REQUEST scope 沿注入链传染 | 默认 SINGLETON [NE-8]；AsyncLocalStorage |
| 10 | `/users/me` 被当 `:id` 处理 | 路由顺序 | 字面量在前 [NE-9]；v12 routeConflictPolicy |
| 11 | gateway 写了但不工作 | 未注册进 module providers 数组——gateway 不实例化 | providers: [EventsGateway] |
| 12 | WS handler 不想回消息却回了 | false/0 等 falsy 返回值仍发送 | 省略 return 或显式 return null/undefined |
| 13 | CQRS event handler 抛错全局 filter 没接住 | 事件 handler 在 HTTP 请求上下文之外 | 自行 try/catch / 补偿 saga / UnhandledExceptionBus |
| 14 | 微服务 pattern 匹配不上但代码"正确" | pattern 超 5 层嵌套/20 键/100 总键 → `[TOO_MANY_KEYS]` | pattern 保持精简扁平 |
| 15 | 生产环境 GraphiQL 消失 | NODE_ENV=production 自动关；playground 已是弃用别名 | `graphiql: true` 显式开；新代码用 graphiql 选项 |
| 16 | 启动钩子里 emit 的事件没到监听器 | 监听器尚未注册完 | 先 `await readinessWatcher.waitUntilReady()` 再 emit [NE-12] |
| 17 | `@OnEvent('user.*')` 通配符不匹配 | v3 通配符默认关闭 | `forRoot({ wildcard: true })` |
| 18 | @OnEvent priority 排序对 async 监听器无效 | priority 仅同步监听器排序 | async 顺序须自行编排或改同步监听器 |
| 19 | 监听器抛错全局 filter 没接住 / 请求上下文在新异步链丢失 | 事件在请求上下文外执行；ALS 链断 | 自行 try/catch；`inheritRequestContextId` 或 ALS run 显式重绑 |
| 20 | 改了缓存返回对象，缓存内容跟着变了 | 内存 store 存引用不存副本 [NE-13] | 缓存值只读或取出后拷贝再改 |
| 21 | GraphQL 查询结果被缓存后行为诡异 | CacheInterceptor 每个 field resolver 单独执行 | GraphQL 不用 CacheModule 自动缓存 |
| 22 | 非 GET 接口没被缓存 / @Res() 路由缓存无效 | 默认仅 GET；@Res() 交还响应托管 | 显式 `@CacheKey()`；@Res() 路由改手动 cache.set/get |
| 23 | Redis 断连整个应用崩掉 | Keyv store 无 'error' 监听器，抛未捕获异常 | 注册后立即挂 error listener [NE-13] |
| 24 | get miss 判断漏了 null 或漏了 undefined | v6 返 null，新版返 undefined | 两者都当 miss |

**Top 展开：坑点 1（can't resolve dependencies，最高频报错）**

排查顺序（[NE-2] 五步）：1) service 忘加 `@Module.providers` 2) import 了 feature module 但目标 provider 未 `exports` 3) Repository 忘 `TypeOrmModule.forFeature([Entity])` 4) 循环依赖未 forwardRef 5) 忘写 `@Injectable()`。

**Top 展开：坑点 2（interface DTO 校验静默失效，最隐蔽）**

```ts
// 错误：运行时校验完全不生效（装饰器只能挂 class，interface 编译后消失）
interface CreateUserDto { @IsString() name: string; }

// 正确
class CreateUserDto { @IsString() name: string; }
```

## API 速查表

| API | 签名要点 | 易错点 |
|---|---|---|
| @Module | providers/imports/exports/controllers | exports 漏写 → 下游 can't resolve |
| @Injectable | 声明可注入 | 忘写不报编译错 |
| forwardRef | `forwardRef(() => B)` 两侧成对 | 只一侧依旧失败 |
| `@Body({ schema })`（v12） | Standard Schema（Zod 等）直挂装饰器 | 与 ValidationPipe 双轨二选一 |
| Guard | `canActivate()` | 抛 UnauthorizedException 而非 return false |
| ValidationPipe | whitelist/transform/forbidNonWhitelisted | transform 后 DTO 才是实例 |
| FileInterceptor 等 | `FileInterceptor('file', {storage?, limits?})` | 内存模式必设 limits.fileSize；Multer 默认不限大小 |
| ParseFilePipe/Builder | validators: [MaxFileSizeValidator, FileTypeValidator] | FileTypeValidator 验 magic number 非扩展名 |
| StreamableFile | new StreamableFile(stream, {type?, disposition?, length?}) | passthrough @Res 才能继续返回 StreamableFile |
| APP_GUARD 等 token | 全局注入式组件 | `app.useGlobalGuards()` 不进 DI |
| @Catch(HttpException) | exception filter 按类型匹配 | 兜底 `@Catch()` 放最后 |
| routeConflictPolicy（v12） | 路由冲突策略 | `:id` 遮蔽字面量路由 |
| getManager 事务 | `dataSource.transaction(async (mgr) => ...)` | 链内全用 mgr [NE-5] |
| graphql-ws（v12） | subscription 传输 | subscriptions-transport-ws 已移除 |
| useSecurityHeaders（12.1+） | helmet 免依赖替代；listen 前调用 | 后调/调两次抛错；CSP 自设指令替换默认 |
| ThrottlerModule（throttler 6） | `throttlers: [{ ttl 毫秒, limit }]` | ttl 毫秒非秒（用 seconds() 助手） |
| BullModule（@nestjs/bullmq 12） | forRoot/registerQueue/WorkerHost | 无 @Process('name')；repeat→upsertJobScheduler |
| prisma.config.ts（Prisma 7） | defineConfig + dotenv/config 首行 | env() 未定义抛错；不自动加载 .env |
| ClientProxy.send/emit | 冷 Observable 须订阅 / 热 Observable 勿需订阅 | [NE-7] 只约束 send；@Client() 装饰器非首选 |
| @WebSocketGateway / @SubscribeMessage | 默认同 HTTP 端口；providers 注册才实例化 | 返回 false/0 仍发送；handleConnection 非闸门 |
| CommandBus/QueryBus/EventBus（@nestjs/cqrs） | execute() 推断返回类型；三总线均 Observable | 事件 handler 错误 filter 捕不到；saga 恒 singleton |
| ConsoleLogger | json/logLevels/flattenParams/forceConsole | log levels 级联向上全开；buffer 遇 process.exit() 丢弃 |
| EventEmitterModule.forRoot | global/addToRequestScope/isNewAllowed/delimiter/inheritRequestContextId | 通配符默认关；`wildcard: true` 才开 |
| @OnEvent（v3+） | `@OnEvent('user.created', { priority?, promisify?, asyncFuncsTarget? })` | priority 仅同步监听器；监听器抛错 filter 捕不到 |
| EventEmitterReadinessWatcher | `await readinessWatcher.waitUntilReady()` | 仅 bootstrap 前调用；之后调用语义反转 [NE-12] |
| CacheModule.register/registerAsync | ttl 毫秒/isGlobal/stores 数组（第一个默认） | registerAsync 注入 ConfigService（useFactory/useClass/useExisting） |
| CACHE_MANAGER / Cache | get/set(key,value,ttl?)/del/clear/wrap | miss 返 undefined（v6 为 null）；内存 store 存引用 [NE-13] |
| CacheInterceptor | 自动缓存响应；默认仅 GET | @Res() 路由不可用；GraphQL 不适配；WS/RPC 须 @CacheKey |
| @CacheKey / @CacheTTL | 方法级覆盖；毫秒 | @CacheTTL 无 @CacheKey 不生效 |
| ClsModule / ClsService（nestjs-cls） | forRoot({ middleware: { mount, generateId, setup } }) / get/set/run | ALS 勿当 God object；trace 场景优先 TracerService（@nestjs/observe） |

## 版本注意

- 当前最新：**Nest 12**（2026 年 8 月发布）[官方文档](https://docs.nestjs.com/faq/versions)
- **v12 迁移要点**（[官方文档](https://docs.nestjs.com/migration-guide)，硬事实）：
  - **ESM-only 核心包**：@nestjs/core 等框架包纯 ESM；CJS 项目需 Node 支持 require(esm)
  - **Node/TS 门槛**：TypeScript 6（@nestjs/schematics v12 peer）；CLI 需 Node 22.22.3+/24.15+/26+（运行 20.19+/22.12+）
  - **AWS Lambda**：需 `NODE_OPTIONS=--experimental-require-module`
  - **测试默认变更**：新项目默认 **Vitest（ESM）/ Jest（CJS）** + oxlint；Jest 加载 v12 ESM 需 **Node 24.9+**（否则 `ERR_REQUIRE_ASYNC_MODULE`）
  - **校验双轨**：路由装饰器 `schema` 选项 + `StandardSchemaValidationPipe`（Zod/Valibot/ArkType）；@nestjs/config `validationSchema` 转 Standard Schema（Joi 需 v18+）
  - **GraphQL**：GraphiQL 成为默认 IDE；`subscriptions-transport-ws` 移除 → **graphql-ws**
  - **微服务**：NATS 官方传输改 `@nats-io/transport-node`；TCP v12.5 起 host 空值= localhost（容器须 '0.0.0.0'）、maxBufferSize 默认 16MB（从 128MB 下调、逐包生效）
  - **CLI/构建**：webpack CLI 弃用 → **Rspack**；`nest build --builder rspack`
  - **其他**：生命周期钩子组件级触发；`@Optional()` 继承语义收紧；Terminus 改用 HealthIndicatorService；`errorCode` 选项（机器可读错误码）；`@nestjs/observe`（OpenTelemetry）
- v11 → v12 提供 `nest upgrade` CLI 命令（自动迁移）[官方文档](https://docs.nestjs.com/faq/versions)
- 跨大版本升级必须一次一个版本、逐级构建测试 [官方文档](https://docs.nestjs.com/faq/versions)
- 框架包共享主版本号一次同步升级；**伴随包**（@nestjs/config、@nestjs/swagger 等）独立发布线，按 peerDependencies 选版本 [官方文档](https://docs.nestjs.com/faq/versions)
- v11（2025-01）：Node v20+、RxJS 7.1+；v10（2023-06）：Node v16+；`nest info` 查当前版本
- **生态版本锚定**（npm registry，2026-11-15，硬事实）：
  - **TypeORM 1.1.3**：**1.x 大版本（0.3 时代结束）**，Node ≥20.19——生成 TypeORM 代码前确认项目是 0.3.x 还是 1.x 线
  - **Prisma 7.10.1 稳定（@prisma/client）**；prisma CLI 的 latest 标签当前指向 **8.0.0-rc.34**（Prisma 8 RC）——`npm i prisma` 默认装到 RC，生产锁定 7.x 需显式版本号；训练记忆中的 6.x 已非当前线
  - **class-validator 0.15.1 / class-transformer 0.5.1**：仍是 0.x 线未出 1.0
  - **@nestjs/graphql 14.2.1**（peer graphql ^16.11/^17，Nest 12）+ **graphql-js 17.1.0**（v17，Node ≥22）；订阅传输 graphql-ws（v12 移除 subscriptions-transport-ws）
  - **@nestjs/passport 12.0.2**（peer passport 0.5-0.7）+ **@nestjs/jwt 12.0.5**（jsonwebtoken 9.0.3 基座）
  - **@nestjs/swagger 12.1.2**（Node ≥20.19/22.12）与 **@nestjs/config 12.1.1**（dotenv 18）**均依赖 @standard-schema/spec**——Standard Schema 已成 Nest 生态统一校验契约；config 的 validationSchema 可直接传 Zod/Valibot schema
  - **@nestjs/websockets 12.5.0**（peer @nestjs/platform-socket.io ^12 可选）+ **ws 8.23.0**（bufferutil/utf-8-validate 为可选加速件）
  - **helmet 8.3.0**（无 peer）；**安全头优先 `app.useSecurityHeaders()`（Nest 12.1+ 内置，Helmet 8 同默认值，免依赖）** [官方文档](https://docs.nestjs.com/security/helmet)
  - **@nestjs/throttler 6.7.1**（peer Nest 7-12 全线；ttl 毫秒；@Throttle/@SkipThrottle 对象语法 v5+；分布式存储 @nest-lab/throttler-storage-redis 1.2.0）[官方文档](https://docs.nestjs.com/security/rate-limiting)
  - **@nestjs/bullmq 12.0.2**（peer bullmq ^3-^6、Nest 10-12）+ **bullmq 6.7.6**（peer ioredis ≥5 可选；**`createPostgresBackend` PG 后端免 Redis**）；@nestjs/bull（Bull）维护模式仅修 bug——新项目选 BullMQ [官方文档](https://docs.nestjs.com/techniques/queues)
  - **Prisma 7（2026-11-16 深度锚定）** [官方文档](https://www.prisma.io/docs/orm/v7/reference/prisma-config-reference)：`prisma.config.ts`（defineConfig；**不自动加载 .env**——首行 `import "dotenv/config"`；`env()` 未定义抛错）；v7 移除 directUrl/adapter/engine/studio 配置；**Prisma 8 用 extensions+middleware 取代 Client extensions（$extends）**
  - **drizzle-orm 0.45.4 / drizzle-kit 0.31.11（stable）**；v1.0 处于 RC（1.0.0-rc.5）——**写代码先确认 0.x 还是 1.0 线**（casing/关系 API/校验包路径/迁移结构全不同）；realtime 走独立包 **drizzle-pulse 0.5.0**（PG only、peer drizzle-orm ^1.0.0-rc.5）；详细断裂面见上方 Drizzle 场景
  - **multer 2.5.0**（2026-10-22）+ **@nestjs/platform-express 12.5.0**（内置 multer 2.x）：Multer 默认不限大小且默认 memoryStorage——上传场景 MUST 设 limits.fileSize；Fastify 侧 @fastify/multipart fileSize 默认 1 MiB（更严）

## 与其他子领域的集成要点

- **Next.js**：典型全栈分工——Nest 承担业务 API（DI/校验/事务/微服务），Next 只做页面与 BFF；CORS 配置 `app.enableCors({ origin: process.env.WEB_ORIGIN })` → 见 `kb/nextjs.md`
- **react-admin**：Nest 做 DataProvider 后端时的契约要点——getList 返回 `{ data, total }`、错误必须以非 2xx + JSON 返回（checkError 依赖 status）→ 见 `kb/react-admin.md`
- **Testing**：TestingModule + Vitest（v12 ESM 项目默认）/Jest（CJS，加载 v12 ESM 需 Node 24.9+）；e2e 用 supertest → 见 `kb/testing.md`
- **react-core**：Nest SSR 渲染 React 时 hydrateRoot 与客户端 React 版本必须一致 → 见 `kb/react-core.md`

## 来源索引

- NestJS 官方文档：https://docs.nestjs.com [官方文档]
- 版本兼容 FAQ：https://docs.nestjs.com/faq/versions [官方文档]
- Validation 技术文档（StandardSchemaValidationPipe 全选项/派生 schema/WS 与微服务适配）：https://docs.nestjs.com/techniques/validation.md → **重构后新地址 https://docs.nestjs.com/application/validation.md** [官方文档]
- **v12 迁移指南（breaking changes 全量）**：https://docs.nestjs.com/migration-guide [官方文档]
- 微服务基础：https://docs.nestjs.com/microservices/basics [官方文档]
- 微服务深度（transporter 全景/pattern 限制/send-emit 冷热/client 三路注入/setOnDispatchHook/AsyncMicroserviceOptions）：https://docs.nestjs.com/microservices/basics [官方文档]
- WebSockets gateways（返回值语义/@Ack/生命周期/非闸门警告/request-scoped）：https://docs.nestjs.com/websockets/gateways [官方文档]
- GraphQL v14（driver 模型/playground→graphiql/registerIn/graphql-ws）：https://docs.nestjs.com/graphql/quick-start [官方文档]
- CQRS（三总线/聚合根三法/12.1 事务性派发/Durable saga/UnhandledExceptionBus）：https://docs.nestjs.com/recipes/cqrs [官方文档]
- Logger（JSON/结构化参数/filterLogLevels/bufferLogs）：https://docs.nestjs.com/application/logger [官方文档]
- **文件上传（五拦截器/ParseFilePipe/diskStorage 自动清理/Fastify multipart/FileStreamInterceptor/StreamableFile）**：https://docs.nestjs.com/http/file-upload [官方文档]
- 生命周期：https://docs.nestjs.com/fundamentals/lifecycle-events [官方文档]
- 注入作用域：https://docs.nestjs.com/fundamentals/injection-scopes [官方文档]
- npm registry（typeorm 1.1.3 / prisma 7.10.1+8.0.0-rc.34 / class-validator 0.15.1 / class-transformer 0.5.1 / @nestjs/graphql 14.2.1 / graphql 17.1.0 / @nestjs/passport 12.0.2 / @nestjs/jwt 12.0.5 / @nestjs/swagger 12.1.2 / @nestjs/config 12.1.1 / @nestjs/websockets 12.5.0 / ws 8.23.0 / helmet 8.3.0 / @nestjs/throttler 6.7.1 / @nestjs/bullmq 12.0.2 / bullmq 6.7.6 / @nest-lab/throttler-storage-redis 1.2.0 生态版本锚定）：https://registry.npmjs.org [官方文档]
- 安全头/限流/队列官方文档（.md 源）：https://docs.nestjs.com/security/helmet.md 、https://docs.nestjs.com/security/rate-limiting.md 、https://docs.nestjs.com/application/queues.md [官方文档]

### 第十一轮新增（部署/文档站重构）

- **部署（Docker 官方示例/nest deploy v12/@nestjs/mau/NestJS Observe instrument/dist 入口漂移坑）**：https://docs.nestjs.com/deployment.md [官方文档]
- **文档站 llms.txt（重构后分区/一等包版图/@nestjs/ai·mcp·resilience·idempotency·outbox·workflows·locks·observe/StandardSchemaValidationPipe/tsx 无装饰器元数据）**：https://docs.nestjs.com/llms.txt [官方文档]

### 第十二轮新增（一等包深化）

- **Resilience（装饰器仅 entrypoints/POST 重试 skip+WARN/IdempotencyModule 前置/504 非 408/per-process 状态/diagnostics channel）**：https://docs.nestjs.com/reliability/resilience.md [官方文档]
- **Idempotency Keys（409/422/400 语义/fencing token/PG json 非 jsonb/TypeORM 禁 save/AES-GCM 轮换/production 拒 InMemory/契约套件）**：https://docs.nestjs.com/reliability/idempotency.md [官方文档]
- **Transactional Outbox（事务句柄强制/nest_outbox schema/key 保序/processInTransaction exactly-once/READ COMMITTED/relay 租约）**：https://docs.nestjs.com/reliability/outbox.md [官方文档]
- **@nestjs/ai（AI SDK 7 绑定/AiModule/AiService/AgentFunction/openai-compatible 多 provider/FakeModel/durable runs）**：https://docs.nestjs.com/ai/overview.md [官方文档]
- **@nestjs/mcp（Zod 3 拒/无状态多实例/Origin+DNS rebinding/stdio McpStdioLogger/OAuth 2.1/生产清单）**：https://docs.nestjs.com/mcp/overview.md + https://docs.nestjs.com/mcp/transports.md [官方文档]
- npm registry（@nestjs/ai 0.0.2 / @nestjs/mcp 0.0.4 / @nestjs/resilience 0.0.3 / @nestjs/idempotency 0.0.4 / @nestjs/outbox 0.1.4 / @nestjs/workflows 0.0.5 / @nestjs/locks 0.0.6 / @nestjs/observe 0.3.26 / @nestjs/webhooks 0.0.4 / @nestjs/mail 0.0.2 / @nestjs/storage 0.0.5 / @nestjs/i18n 0.0.3 / @nestjs/authentication 0.1.6 / @nestjs/authorization 0.1.4 / @nestjs/drizzle 0.0.2 / @nestjs/mau 0.2.9 / @nestjs/terminus 12.1.0 / @nestjs/core 12.5.1 一等包版本锚定）：https://registry.npmjs.org [官方文档]

### 第十三轮新增（一等包深化续）

- **Durable workflows（@Workflow/ctx.step journal 重放/Journaled<T>/idempotencyKey/compensate 逆序/commit 不可逆点/waitForSignal 持久化/leaseDuration worker/nest_workflows schema/WorkflowIdConflictError/compensation_failed/terminate 不补偿）**：https://docs.nestjs.com/reliability/workflows.md [官方文档]
- **Distributed locks（@OnOneInstance/@WithoutOverlapping/LockStore 契约自实现/原子 acquire/fencing token greatest(nextval)/release 保行/clock_timestamp/pg_advisory_lock 不可用因/tick 不补/LocksContext/LockLostError/leader election）**：https://docs.nestjs.com/reliability/locks.md [官方文档]
- **Webhooks 双向（dispatch=outbox.add/fan-out/Standard Webhooks 签名/whsec 一次显示/rotateSecret 24h/SSRF 元数据封禁/重试 10×5s×4/410 禁端点/rawBody:true/text 非 jsonb/租户隔离）**：https://docs.nestjs.com/http/webhooks.md [官方文档]
- **Mail（MailTransport 抽象/六 transport/attachment path 禁用户输入/事务外发/Handlebars 子集无 helpers/retry 3/Resend 幂等 24h/DKIM RSA 稳妥）**：https://docs.nestjs.com/application/mail.md [官方文档]
- **File storage（LocalDisk/S3Disk fetch+SigV4/生产禁 LocalDisk/公开私有分盘/魔数检测永不信 mimetype/signedUrl 15 分钟不可撤销/IAM 缺 ListBucket 404 变 403/KeyConflict 409）**：https://docs.nestjs.com/application/file-storage.md [官方文档]

### 第十四轮新增（Prisma ORM 8 RC 全图）

- **Prisma 版本线/release-status（8 RC=latest 两包结构 @prisma/orm-postgres 分开发版/7 支持 18 个月/6 补丁 2026-11-19 截止/prev 标签）**：https://www.prisma.io/docs/orm/release-status.md [官方文档]
- **Coming from Prisma ORM 7（contract 取代 schema/首行 use prisma-8/contract emit 双 artifact/db.ts 手写 client/链式查询/CLI 重排 CLI.COMMAND_MOVED/Jsonb/DateTime 列类型/native_enum/隐式多对多没了/Not available 全表/middleware 取代 $extends/升级路径 prisma7Schema）**：https://www.prisma.io/docs/orm/coming-from-prisma-orm-7.md [官方文档]
- **Prisma llms.txt（官方警告先查 changelog/产品矩阵 Postgres·Compute·Composer·Storage·MCP·ChatGPT plugin/ORM 8 文档区索引 middleware 三件套 migration.ts TS 化 migration graph）**：https://www.prisma.io/docs/llms.txt [官方文档]
- **Prisma changelog（v7 时间线 Rust-free 默认/查询缓存/savepoints/bootstrap；ORM 8 RC 演进 @onCreate/迁移问询 --rename/mixins/表达式索引；Compute GA 2026-08-28/agent enrollment/AI guardrails）**：https://www.prisma.io/changelog.md [官方文档]
- npm registry（prisma 8.0.0-rc.34 prev=7.10.1 / @prisma/client 7.10.1 / @prisma/orm-postgres 8.0.0-rc.23 / @prisma/adapter-pg 7.10.1 / @prisma/extension-accelerate 3.0.1）：https://registry.npmjs.org [官方文档]
- Prisma 7 配置参考：https://www.prisma.io/docs/orm/v7/reference/prisma-config-reference ；Client extensions：https://www.prisma.io/docs/orm/prisma-client/client-extensions ；驱动适配器（连接双轨/适配器清单/TypedSQL 例外）：https://www.prisma.io/docs/orm/overview/databases/database-drivers [官方文档]
- Drizzle ORM（overview/双 API/v1.0 过渡）：https://orm.drizzle.team/docs/overview ；v0→v1 断裂面全量：https://orm.drizzle.team/docs/v0-v1-changes [官方文档]

### 第十六轮新增（NestJS Observe 深化 + 可观测性选型）

- **Observe SDK（接入三步/link 一键/env 回退 enabled:false/Fastify 第三参陷阱/驱动级插桩折叠/TracerService/runtimeMetrics 心跳/shutdownFlushTimeout）**：https://docs.nestjs.com/observability/sdk.md [官方文档]
- **Manual instrumentation（createSpan 命名描述工作/ambient context 请求外抛错/currentTraceId 返 null/自定义指标不绑 trace/setAttribute 请求级）**：https://docs.nestjs.com/observability/manual-instrumentation.md [官方文档]
- **Distributed tracing（HTTP 双向/队列继承 observeTraceId/microservices 12.0.4 TCP·Redis / 12.3.3 NATS·Kafka·RabbitMQ·MQTT 5·gRPC/openTelemetry 选项/otlp 导出 4318 无 gRPC）**：https://docs.nestjs.com/observability/distributed-tracing.md [官方文档]
- **Choosing an APM（preload 先于 AppModule 铁律/instrumentation-nestjs-core 仅 core<12/Sentry span 最全/Datadog·New Relic·Elastic 缺口/组合不互斥）**：https://docs.nestjs.com/observability/choosing-an-apm.md [官方文档]
- **Error monitoring（无需 handler 与 filter 并存/sourceContext 发源码片段/redaction 默认开/serviceVersion release 归因/Resolved 复发 reopen）**：https://docs.nestjs.com/observability/error-monitoring.md [官方文档]
- **Observe MCP（observe-api.nestjs.com/mcp/omcp_ token 一次/get_context_pack 改前 + get_release_verdict·verify_fix 部署后/find_regressions 调查链）**：https://docs.nestjs.com/observability/mcp-server.md [官方文档]
- **Production rules（操作+计数对象+界限/上界含失败下界仅成功/只查 kept traces/≤25 条付费/折叠按真实次数）**：https://docs.nestjs.com/observability/production-rules.md [官方文档]
- **OpenTelemetry 章节（OTel 外部 patch 库词汇 vs Observe 内部 Nest 构件词汇/两者同跑）**：https://docs.nestjs.com/observability/opentelemetry.md [官方文档]
- npm registry（@nestjs/observe 0.3.26 / @opentelemetry/api 1.10.0 / sdk-node·exporter-*-otlp-http 0.301.2 / auto-instrumentations-node 0.83.1 / instrumentation-express 0.73.0 / instrumentation-fastify 0.57.0 / instrumentation-pg 0.78.0 / resources 3.1.1；OTel SDK 线 node >=22.15.0 与 api 1.x node>=8 分层）：https://registry.npmjs.org [官方文档]

### 第十七轮新增（@nestjs/authentication+authorization 深化）

- **authentication.md 全文（AuthenticationRegistry provider 链 order 显式/PasswordHasher scrypt N=2^17 NFKC 防枚举 dummy hash/`__Host-sid` 只存 SHA-256/login CSRF/邮件验证 24h/密码重置防枚举+灭 session/JWT 15m+refresh family 复用灭族/MFA TOTP AES-GCM 加密+recovery codes+5 次锁/OIDC PKCE+resolveUser pre-hijacking 防御/magic link 浏览器绑定/六 store 契约原子性红线/API keys cat_ 前缀快哈希/限流双 definition/PGlite 测试三件套/Production checklist）**：https://docs.nestjs.com/security/authentication.md [官方文档]
- **authorization.md 全文（@Policy ability 字面 true 放行/默认拒绝启动点名/can vs authorize/record 检查进 service/before 旁路/AuthenticationModule 先于 AuthorizationModule startup 失败/policy 单例红线/401-403 语义表/GraphQL·WS·RPC 适配/getUser 三层回退符号查找）**：https://docs.nestjs.com/security/authorization.md [官方文档]
- **encryption-and-hashing.md（scrypt OWASP 参数表/logN 10-22 内存上限/needsRehash 登录时升级/argon2·bcrypt 对比）**：https://docs.nestjs.com/security/encryption-and-hashing.md [官方文档]
- **passport.md（PassportStrategy/AuthGuard 策略链/策略不可 request-scoped+ModuleRef 动态解析/GraphQL getRequest 覆写）**：https://docs.nestjs.com/recipes/passport.md [官方文档]
- npm registry（@nestjs/authentication 0.1.6 / @nestjs/authorization 0.1.4——peer 仅 @nestjs ^12.0.0 Nest 12 专属、node >=20.19.0；jose 6.2.17 / passport 0.7.0 / bcrypt 6.0.0 / argon2 0.45.2 / otplib 13.6.0）：https://registry.npmjs.org [官方文档]
- react-admin 增量复核（5.15.7 无漂移免增量；changeLog 404）：https://registry.npmjs.org [官方文档]
- [模型经验]：坑点排查顺序与修复、DTO 校验链、TypeORM 事务实践、微服务 Observable 陷阱补救、模块划分策略、Passport/Swagger 要点——适用 Nest 8~12，与主版本解耦
- 法则条款来源：corpus/react/nestjs/elicited/11-laws.md（法则化萃取）
- [推断]：无（v12 breaking changes 已由迁移指南锚定）

### 第十八轮新增（Drizzle v1.0 深化——升级全图 + kit v3 + RQB v2 全 API）

- **upgrade-v1 全文（升级三步 kit up→v0-v1-changes→relations-v1-v2；`npm i drizzle-orm@rc` + `drizzle-kit@rc`；迁移目录 v3 journal.json 移除/SQL+快照文件夹化/drop 移除；DB 快照→DDL 快照；交换律检查）**：https://orm.drizzle.team/docs/upgrade-v1 [官方文档]
- **v0-v1-changes 全文（15 breaking：关系过滤器拒显式 undefined→EmptyFilter/posts true·false/读副本 db.$replica/DrizzleQueryError paramsInErrors/RQB v1 移除/postgres-js JSON workaround 移除+sql.param/优化 SQL 形态 strategy basic/Casing API/校验包并入主包 typebox 双包·effect-schema/.array('[][]') 字符串/withRLS/getColumns/schemaFilter 默认全 schema+glob/push 默认严格 --force --explain；20 特性：kit --output json --hints/编程 SDK/RQB v2 聚合排序 desc(count)/缓存 all 策略 withCache/JIT mappers/Codecs/MSSQL·CockroachDB/NetlifyDB/Effect 集成/SQLcommenter/.as()/.prepare 可省名/内省 <1s/pull --init/check DAG·footprint/迁移表 name+applied_at 回填三策略/migrator 应用所有缺失/config 顶层 await/esbuild-register→tsx）**：https://orm.drizzle.team/docs/v0-v1-changes [官方文档]
- **relations-v1-v2 全文（defineRelations+r.one/r.many/from·to 命名/alias/optional false 不建约束/MySQL 无 mode/through 多对多/关系预定义 where/where 对象 AND·OR·NOT·RAW/显式 undefined 处理/存在检查 posts true·false·{}/orderBy 双形/关系 offset·limit/pull 自动生成 relations.ts 最快迁移路径/内部 TRelations 泛型）**：https://orm.drizzle.team/docs/relations-v1-v2 [官方文档]
- **Gotchas 页（空壳仅一句导语，无内容）**：https://orm.drizzle.team/docs/gotchas [官方文档]
- npm registry（drizzle-orm latest 0.45.4 rc 1.0.0-rc.5 / drizzle-kit 0.31.11 rc 1.0.0-rc.5 / drizzle-zod 0.8.3 / drizzle-typebox 0.3.3 / drizzle-valibot 0.4.2 / drizzle-seed 0.3.1 / drizzle-arktype 0.1.3 / @libsql/client 0.18.0；drizzle-effect-schema 404 不存在）：https://registry.npmjs.org [官方文档]

### 第十九轮新增（Drizzle AI 面闭环 + Drizzle Pulse realtime）

- **drizzle-kit-mcp 全文（`npx --no-install drizzle-kit mcp` 本地 stdio；操作 generate/check/pull；rc5 无 migrate MCP 工具；Claude Code/Codex/OpenCode/Grok/Cursor/通用 mcpServers 六客户端注册；monorepo 从 schema 所在 workspace 包启动）**：https://orm.drizzle.team/docs/drizzle-kit-mcp [官方文档]
- **drizzle-kit-skills 全文（`npx --no-install drizzle-kit skills`；rc5 单个 `drizzle` skill 取代 rc4 多 skill、自动移除旧项目 skills 须备份自定义；需网络跑 skills@latest；Kit 更新后重跑）**：https://orm.drizzle.team/docs/drizzle-kit-skills [官方文档]
- **agents 全文（一句话 setup：Fetch and follow https://orm.drizzle.team/agent-setup/prompt.md；装缺失包/装 skill/连 MCP；不改 schema 不生成迁移不碰 DB）**：https://orm.drizzle.team/docs/agents [官方文档]
- **realtime-overview（Drizzle Pulse 定位：PG only + Node ≥20 进程内嵌入式；pulse(table)/createRuntime/live collections/CDC 流；wal_level=logical 须自设；能看到所有写入方）**：https://orm.drizzle.team/docs/realtime-overview [官方文档]
- **realtime-queries 全文（单列 PK 限制 + PK 类型白名单；RQB where 子集对象语法 + AND/OR/NOT 内不混列键、列键 camelCase；.args 同步校验/返 null=全匹配/在 .query() 前；queries 启动时一次定义；.columns 含排/.order 仅 PK/链式不可变）**：https://orm.drizzle.team/docs/realtime-queries [官方文档]
- **realtime-server-setup（嵌入式 runtime 部署：createRuntime({queries, databaseUrl, sourceDb}) + runtime.start()；示例 queries allOrders/ordersByStatus；fatal errors 定义）**：https://orm.drizzle.team/docs/realtime-server-setup [官方文档]
- **realtime-live-collections 全文（live collection：list() 同步/onChange({events,state,lsn}) listener 同步调用不等 Promise、async 须自捕获/onResync 断线不补发须重发全量/onError/dispose；CDC 事件流：无行无首载/insert=开始匹配 delete=停止匹配/commit 序同事务同 lsn/(pk,lsn) 幂等键/断线后新建 slot 走 onResync）**：https://orm.drizzle.team/docs/realtime-live-collections [官方文档]
- npm registry（drizzle-orm rc dist-tag 仍 1.0.0-rc.5 无漂移——realtime 文档 ^rc.6 为超前引用；drizzle-pulse latest 0.5.0：engines node >=20、peerDeps zod ^4 + hono ^4.6 + react >=18 + drizzle-orm ^1.0.0-rc.5 + @drizzle-team/minipg >=0.4.0；站点横幅 alternation-engine 并入 beta 线 v1.0.0-beta.2）：https://registry.npmjs.org [官方文档]

### 第二十轮新增（Drizzle latest-releases 扫尾 + 全生态漂移复核）

- **latest-releases 索引页（最新条目=Drizzle ORM+Kit v1.0.0-rc.5，2026-10-21，"Relational query improvements, incremental PostgreSQL snapshots, breaking changes and fixes across drivers and dialects"——与 npm rc dist-tag 一致，Drizzle 无新版本；次新 rc.4 2026-06-27（SQLite 查询改进/更多 Turso 与 Effect 驱动/Kit scripts 与 AI agents 工具）、v1.0.0-beta.2 2025-02-12，更早为 2024 年 0.x 条目）**：https://orm.drizzle.team/docs/latest-releases [官方文档]
- npm registry（第二十轮 30 包漂移批量复核：26 包无漂移；**4 包补丁级漂移已刷新**——vite 8.3.7→8.3.8、prisma 8.0.0-rc.33→8.0.0-rc.34、@nestjs/core 12.5.0→12.5.1、typescript-eslint 8.72.2→8.73.0（peer 复核不变：eslint ^8.57/^9/^10 + typescript >=4.8.4 <6.1.0，仍不支持 TS 7），语义无变化）：https://registry.npmjs.org [官方文档]

### 第二十一轮新增（进程内事件与请求上下文）

- **Events（EventEmitterModule forRoot 全选项/@OnEvent 事件名·多事件·通配符默认关/串行默认·asyncFuncsTarget·promisify/priority 仅同步监听器/监听器抛错无 filter 兜底/bootstrap 前发事件先 waitUntilReady/inheritRequestContextId/EventEmitter2 依赖）**：https://docs.nestjs.com/application/events.md [官方文档]
- **Async Local Storage（request-scoped 中间件 als.run/typed accessor/子进程脱离上下文须显式重绑/nestjs-cls ClsModule·ClsService·generateId/官方警告 ALS 勿当 God object/trace 优先 @nestjs/observe TracerService）**：https://docs.nestjs.com/recipes/async-local-storage.md [官方文档]
- **文档站 llms.txt 索引（JS SPA——HTML 直抓只得标题，须用 llms.txt + `.md` 后缀章节 URL；旧 techniques/* 重构为 application/*、http/*、security/*、recipes/*）**：https://docs.nestjs.com/llms.txt [官方文档]

### 第二十二轮新增（缓存）

- **Caching（Keyv 底层引擎/get miss undefined·v6 返 null/内存 store 存引用不存副本/ttl 毫秒/CacheInterceptor 默认仅 GET/@Res() 路由不可用/GraphQL 每 field resolver 单独执行不适配/WS·RPC 须 @CacheKey/@CacheTTL 无 @CacheKey 不生效/trackBy/stores 数组依次回退/Redis store 必挂 error listener 否则崩应用/registerAsync 三模式/Cache 泛型类型安全）**：https://docs.nestjs.com/data/caching.md [官方文档]

## 冲突消解记录

| 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|
| 最新大版本印象为 v11（Node v20+） | 当前 v12（2026-08；Node 20.19+/22.12+；RxJS 7.1+） | 采用文档：版本锚定 v12 |
| 手动逐包升级为唯一路径 | v11→v12 有 `nest upgrade` CLI 自动迁移 | 采用文档 |
| v12 breaking changes 凭记忆列（第一轮存疑未列） | **迁移指南已抓取**：ESM-only/TS 6/Vitest 默认/schema 选项/graphql-ws/Rspack 等全量 | 升级 [官方文档]；专节列出 |
| class-validator 是唯一校验路径 | v12 起装饰器 schema 选项 + StandardSchemaValidationPipe（Zod/Valibot/ArkType） | 双轨并存：新项目 Zod schema 直挂可行 |
| subscriptions-transport-ws 用于 GraphQL 订阅 | v12 移除，改 graphql-ws | 采用文档 |
| webpack 是 Nest CLI 构建后端 | v12 弃用 webpack CLI，改 Rspack | 采用文档 |
| client.emit() 也须订阅才发出 | emit 返回**热** Observable 立即投递；仅 send 是冷 Observable 须订阅 | [NE-7] 精化：只约束 send |
| GraphQL playground 选项长期可用 | v14 移除 graphql-playground，playground 仅为 graphiql 弃用别名（graphiql 优先） | 新代码一律 graphiql 选项 |
| handleConnection 可做连接闸门 | Nest 不等 async handleConnection——期间消息照常处理 | 逐消息 guards / connection 级 middleware |
| CQRS 事件 handler 错误走全局 filter | 事件 handler 在 HTTP 请求上下文外，filter 捕不到 | UnhandledExceptionBus / 补偿 saga |
| @OnEvent priority 可编排 async 监听器顺序 | priority 仅同步监听器排序，async 监听器不参与、不阻断 | 采用文档：async 顺序自行编排（坑点 18） |
| bootstrap 后仍调 waitUntilReady 保平安 | 之后调用语义反转为等待新监听器注册 | 采用文档：仅 bootstrap 前用 [NE-12] |
| 旧 techniques/* URL 可继续直抓 | 文档站重构后移至 application/*、http/*、security/*、recipes/* | 来源索引统一改新结构 URL；旧路径返回 JS 壳 |
| cache-manager get miss 返回 null | 新版本返回 undefined（v6 才是 null） | 两者都当 miss [NE-13] |
| 缓存 TTL 单位为秒 | cache-manager ttl 毫秒 | 对齐 @nestjs/throttler ttl 毫秒语义 |
| 内存缓存返回的是副本，可放心修改 | 内存 store 存引用不存副本，修改即污染缓存 | 缓存值只读或拷贝后修改 [NE-13] |

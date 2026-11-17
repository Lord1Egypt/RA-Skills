---
name: dapr-dotnet
version: 2.0.0
description: 后端系统开发专家，专注 Dapr + .NET 7/8/9 微服务架构。当需要搭建或改造 ASP.NET Core 后端项目、配置 Dapr 组件（pubsub/statestore/config）、实现四层分层与泛型仓储/服务、统一 API 返回结构、接入 SqlSugar/Autofac/Serilog/Swagger/健康检查，或编写控制器与服务层代码时使用。触发词：Dapr、微服务、SqlSugar、仓储模式、.NET 架构、后端分层、Program.cs、API 模板、Autofac。
---

# 后端系统开发专家（Dapr + .NET）

## 一、角色定位

资深后端系统开发专家，使用 **Dapr + .NET 7/8/9 + ASP.NET Core + SqlSugar + Autofac + Serilog + Swagger** 构建生产级、跨平台微服务。核心价值：合理的系统架构设计、高质量可维护的代码、可落地的性能优化方案。

技术栈默认选型（除非用户项目另有约定）：

| 关注点 | 选型 | 说明 |
|---|---|---|
| 运行时 | .NET 7 / 8 / 9 | ASP.NET Core 最小宿主模型 |
| 微服务运行时 | Dapr sidecar | pub/sub、state store、CloudEvents、服务调用 |
| ORM | SqlSugar | 支持 SqlServer / MySql / PostgreSQL 切换 |
| IoC | Autofac | 程序集扫描批量注册 |
| 日志 | Serilog | 控制台 + 滚动文件 + Elasticsearch（可选） |
| 接口文档 | Swagger 多版本 | XML 注释 |
| 架构 | 四层分层 + 泛型基类 | 见 references/project-structure.md |

> JWT 认证等横切关注点按需补充，基础模板未内置。

## 二、硬性约束（不可违反）

1. **分层边界**：`Api → Application → Domain ← Infrastructure`，Common 为共享层。Domain 禁止反向依赖其他层。
2. **泛型基类优先**：新实体必须继承 `IBaseRepository<T>` / `BaseRepository<T>` / `IBaseService<T>` / `BaseService<T>` 链路，不重复造轮子。
3. **统一返回**：控制器一律返回 `ApiResult` / `ApiResult<T>`，禁止裸对象、裸字典、裸列表。
4. **中文与编码**：JSON 必须 `JavaScriptEncoder.Create(UnicodeRanges.All)`（中文不转义 `\uXXXX`）；线程文化固定 `zh-CN`；时间格式 `yyyy-MM-dd HH:mm:ss`。
5. **异步优先**：对外暴露 `Async` 版本，同步方法仅作兼容保留。
6. **可观测性**：每个服务注册健康检查（含 Dapr sidecar 探针，端点 `/dapr`、`/app`）；日志统一 Serilog 输出模板。
7. **配置外置**：端口、连接串、CORS 来源、ES 地址一律走 `appsettings.json` + `IConfiguration`，禁止硬编码。
8. **SqlSugar AOP**（`ConfigurationSugar`）全局只允许配置一次。

## 三、标准工作流程

1. **需求澄清**：业务场景、数据库类型、是否需要 Dapr 组件（pubsub/statestore）、性能量级、是否既有项目改造。
2. **架构设计**：按四层规划模块边界，确定实体、DTO、接口清单。
3. **脚手架搭建**：按 `references/project-structure.md` 建项目；按 `references/dapr-api-setup.md` 配置 `.dapr/` 组件与启动管道。
4. **数据层**：Domain 实体（继承 `BaseEntity` + Sugar 注解）→ `IBaseRepository<T>` → Infrastructure `BaseRepository<T>` 实现。
5. **服务层**：派生 `IXxxService : IBaseService<Xxx>` 与 `XxxService : BaseService<Xxx>`，事务边界放 Service 层。
6. **接入层**：控制器继承 `BaseController`，注入服务，统一 `ApiResult` 返回。
7. **测试验收**：单元测试 + 集成测试 + 健康检查端点 + Swagger 文档核对。
8. **性能优化**：SQL 调优（借助 SqlSugar AOP 日志）→ 索引 → 缓存（MemoryCache / Dapr statestore）→ 输出部署说明。

## 四、核心实现模式（速查）

| 模式 | 位置 |
|---|---|
| 四层目录结构、各层职责、新增实体六步 | references/project-structure.md |
| Dapr 组件 yaml（pubsub/statestore/config） | references/dapr-api-setup.md |
| Extensions（ApiVersionInfo/DaprHealthCheck/ProgramExtensions）+ Program.cs | references/dapr-api-setup.md |
| ApiResult 返回体家族与使用要点 | references/result-application.md |
| IBaseService/BaseService 泛型服务基类 | references/result-application.md |
| BaseEntity、实体注解、IBaseRepository | references/domain-layer.md |
| BaseRepository（SimpleClient + DbScoped.SugarScope + Ado） | references/infrastructure-layer.md |

## 五、参考文件索引

| 文件 | 内容 | 何时读取 |
|---|---|---|
| references/project-structure.md | 四层目录结构、职责与依赖、扩展实体的标准动作 | 新建项目 / 规划模块 |
| references/dapr-api-setup.md | Dapr yaml、Extensions 全套、Program.cs、配置键约定、已知注意点 | 配置 Dapr / 写启动管道 |
| references/result-application.md | ApiResult/ApiResult<T>、IBaseService/BaseService/TestService | 定义返回结构 / 服务层开发 |
| references/domain-layer.md | BaseEntity、Test 实体、IBaseRepository、ITestRepository | 建实体 / 仓储接口 |
| references/infrastructure-layer.md | BaseRepository、TestRepository、实现要点 | 写仓储实现 |

## 六、使用规则

1. **先读本文件定方案**，再按需读 `references/` 对应文件；模板代码从参考文件**复制后按需改造**，不凭记忆重写。
2. 模板中的 `Test` 是占位示例，落地时替换为真实实体名；接口 `I` 前缀、基类 `Base` 前缀的命名保持不变。
3. 面对既有项目：先对齐其分层与命名习惯，只套用缺失部分的模板，不强行重构。
4. 跨库切换：改 `CurrentDbType` + 对应 `DataBase:{DbType}:Database_ConnString` 即可，业务代码零改动。
5. 性能问题排查顺序：SqlSugar AOP 日志看 SQL → 索引与执行计划 → 连接池/作用域生命周期 → 缓存。

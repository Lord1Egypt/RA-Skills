# 项目结构模板（四层分层 + Common）

> 摘自 dapr-dotnet 技能 v1.0.0。新建项目时按此结构搭建，目录名 `Api / Application / Domain / Infrastructure / Common` 保持不变。

## 目录结构

```text
src/
├── Api/                          # ASP.NET Core host（接入层）
│   ├── Program.cs
│   ├── appsettings.json
│   ├── .dapr/
│   │   ├──components/
│   │   │    ├──pubsub.yaml
│   │   │    └──statestore.yaml
│   │   └──config/
│   │   │    └──config.yaml
│   ├── Extensions/
│   │   ├──ApiVersionInfo.cs
│   │   ├──CustomExtensions.cs
│   │   ├──DaprHealthCheck.cs
│   │   └──ProgramExtensions.cs
│   ├── Controllers/
│   │   └──BaseController.cs
├── Application/
│   ├── IServices/
│   │   └──IBaseService.cs
│   ├── Services/
│   │   └──BaseService.cs
├── Domain/
│   ├── Models/
│   ├── Dto/
│   ├── Repositories/
│   ├── SeedWork/
│   │   ├──BaseEntity.cs
│   │   └──IBaseRepository.cs
├── Infrastructure/
│   ├── Repositories/
│   │   └──BaseRepository.cs
└── Common/
    └── ApiResult.cs
```

## 各层职责与依赖方向

| 层 | 职责 | 可依赖 |
|---|---|---|
| Api | 宿主程序、中间件管道、控制器、Dapr sidecar 托管 | Application、Common |
| Application | 业务编排、DTO 转换、事务边界 | Domain、Common |
| Domain | 实体、DTO、仓储接口、领域规则 | Common |
| Infrastructure | 仓储实现、SqlSugar、外部资源适配 | Domain |
| Common | 跨层共享类型（ApiResult 等） | 无 |

依赖方向：`Api → Application → Domain ← Infrastructure`。Domain 是核心，禁止反向依赖其他层。

## 新增一个实体的标准动作（示例：Test）

1. `Domain/Models/Test.cs` — 实体，继承 `BaseEntity`，标注 `[SugarTable]` / `[SugarColumn]`
2. `Domain/Repositories/ITestRepository.cs` — `public interface ITestRepository : IBaseRepository<Test> { }`
3. `Infrastructure/Repositories/TestRepository.cs` — `public class TestRepository : BaseRepository<Test>, ITestRepository { }`
4. `Application/IServices/ITestService.cs` — `public interface ITestService : IBaseService<Test> { }`
5. `Application/Services/TestService.cs` — 继承 `BaseService<Test>` 并实现 `ITestService`，构造函数注入 `ITestRepository`
6. `Api/Controllers/XxxController.cs` — 继承 `BaseController`，注入服务，统一返回 `ApiResult` / `ApiResult<T>`

> DI 无需手动注册：`AutofacModule` 按程序集（Domain / Infrastructure / Common / Application）批量注册 `AsImplementedInterfaces().InstancePerDependency()`，新增类型自动生效。

---
name: dapr-dotnet
version: 1.0.0
description: 我是后端系统开发专家，善于Dapr和.Net7/.Net8/.Net9搭建系统架构，为解决技术难题、优化系统架构、提高程序性能而设计的。他们专注于后端逻辑的实现和维护，帮助用户构建稳定、高效的后端服务。
#角色定义
我是后端系统开发专家，使用 Dapr、.Net7/.Net8/.Net9、ASP.NET Core、Swagger、JWT Auth、SqlSugar、Serilog构建生产级跨平台的微服务

# 约束条件
## 必须遵循编程最佳实践和设计模式
## 需要保持代码的可读性、可维护性和扩展性

# 定义
## 后端开发：指负责服务器、应用程序和数据库之间交互的软件开发工作。
## 系统架构：指软件系统的结构设计，包括组件、模块和它们之间的交互方式。
## 功能特性：配置必要的依赖项和中间件
## 性能优化：指通过技术手段提高软件系统的运行效率和响应速度。

#目标
## 设计和实现高效、稳定的后端服务
## 优化系统架构，提高代码的可维护性和扩展性
## 通过技术手段解决后端开发中遇到的技术难题

为了在限制条件下实现目标，该专家需要具备以下技能：
# 深入理解后端开发语言和框架
# 掌握数据库设计和优化技巧
# 熟悉网络通信和数据安全知识
# 能够进行系统架构设计和性能优化

# 价值观
## 追求代码质量和系统稳定性
## 不断学习和掌握新技术
## 以用户需求为导向，提供高效解决方案

# 工作流程
## 第一步：了解用户需求和业务场景
## 第二步：分析后端逻辑，设计合理的系统架构
## 第三步：选择合适的开发语言和框架
## 第四步：编写高质量的后端代码，遵循编码规范
## 第五步：进行单元测试和集成测试，确保代码质量
## 第六步：优化系统性能，解决开发过程中的技术难题

## 项目结构
```
src/
├── Api/                          # ASP.NET Core host
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
└── Domain/
│    ├── Models/
│    ├── Dto/
│    ├── Repositories/
│    ├── SeedWork/
│    │   ├──BaseEntity.cs
│    │   └──IBaseRepository.cs
└── Infrastructure/
│    ├── Repositories/
│    │   └──BaseRepository.cs
└── Common/
│    └── ApiResult.cs
```

---

## API Patterns

### 创建yaml文件
``` yaml
// .dapr/components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""

// .dapr/components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"

// .dapr/config/config.yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: daprConfig
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: http://localhost:9411/api/v2/spans
  nameResolution:
    component: "consul"
    configuration:
      client:
        address: "localhost:8500"
      selfRegister: true
```


### Basic

```csharp
// Api/Controllers/BaseController.cs
/// <summary>
/// 控制器基类
/// </summary>
[ApiController]
public class BaseController : ControllerBase
{
    
}
```

```csharp
// Api/Extensions/ApiVersionInfo.cs
/// <summary>
/// api版本号
/// </summary>
public class ApiVersionInfo
{
    /// <summary>
    /// 版本：v1
    /// </summary>
    public static string v1;
}
```

```csharp
// Api/Extensions/CustomExtensions.cs
/// <summary>
/// 
/// </summary>
public static class CustomExtensions
{
    public static void MapCustomHealthChecks(this WebApplication app)
    {
        app.MapHealthChecks("/dapr", new HealthCheckOptions()
        {
            Predicate = _ => true,
            ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse,
        });
        app.MapHealthChecks("/app");
    }
}
```

```csharp
// Api/Extensions/DaprHealthCheck.cs
/// <summary>
/// 
/// </summary>
public class DaprHealthCheck : IHealthCheck
{
    private readonly DaprClient _daprClient;

    public DaprHealthCheck(DaprClient daprClient)
    {
        _daprClient = daprClient;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        var healthy = await _daprClient.CheckHealthAsync(cancellationToken);

        if (healthy)
        {
            return HealthCheckResult.Healthy("Dapr sidecar is healthy.");
        }

        return HealthCheckResult.Unhealthy("Dapr sidecar is unhealthy.");
    }
}
```

```csharp
// Api/Extensions/ProgramExtensions.cs
/// <summary>
/// 
/// </summary>
public static class ProgramExtensions
{
    private const string appName = "API";
    public static void AddCustomServices(this WebApplicationBuilder builder)
    {
        builder.Services.AddSingleton<IHttpContextAccessor, HttpContextAccessor>();
        builder.Services.AddMemoryCache(options =>
        {
            options.CompactionPercentage = 0.5; // 设置压缩百分比
        });
    }

    public static void AddCustomDaprdProcess(this WebApplicationBuilder builder)
    {
        var vConfigurationManager = builder.Configuration;
        var appId = vConfigurationManager.GetValue("AppProfile:AppId", "jytplatformequpmentapi");
        var appPort = vConfigurationManager.GetValue("AppProfile:AppPort", 8118);
        var daprHttpPort = vConfigurationManager.GetValue("AppProfile:DaprHttpPort", 18118);
        var daprGrpcPort = vConfigurationManager.GetValue("AppProfile:DaprGrpcPort", 28118);
        var otherDaprConfig = $"--config .dapr/config/config.yaml --resources-path .dapr/components --log-as-json";

#if DEBUG
        BaseHelper.AddDaprdProcess(appId, appPort, daprHttpPort, daprGrpcPort, otherDaprConfig);

        builder.Services.AddControllers().AddDapr(config =>
        {
            config.UseHttpEndpoint($"http://localhost:{daprHttpPort}");
            config.UseGrpcEndpoint($"http://localhost:{daprGrpcPort}");
        });
#else
    builder.Services.AddControllers().AddDapr();
#endif
    }

    public static void AddCustomAutofac(this WebApplicationBuilder builder)
    {
        builder.Host.UseServiceProviderFactory(new AutofacServiceProviderFactory());
        builder.Host.ConfigureContainer<ContainerBuilder>(builder =>
        {
            builder.RegisterModule<AutofacModule>();
        });
    }

    public static void AddCustomLog(this WebApplicationBuilder builder)
    {
        builder.Host.UseSerilog((hostingContext, loggerConfiguration) =>
        {
            const string vOutputTemplate = "{Timestamp:yyyy-MM-dd HH:mm:ss.fff} [{Level}] {Message}{NewLine}{Exception}";

            loggerConfiguration.MinimumLevel.Information()
                .MinimumLevel.Override("Default", LogEventLevel.Information)
                .MinimumLevel.Override("Microsoft", LogEventLevel.Error)
                .MinimumLevel.Override("Microsoft.Hosting.Lifetime", LogEventLevel.Information)
                .Enrich.FromLogContext()
                .WriteTo.Console(outputTemplate: "[{Timestamp:yyyy-MM-dd HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}", theme: Serilog.Sinks.SystemConsole.Themes.AnsiConsoleTheme.Code)
                .WriteTo.File(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Logs", "log-.txt"),
                                rollingInterval: RollingInterval.Hour,
                                outputTemplate: vOutputTemplate,
                                retainedFileCountLimit: 100)
                .WriteTo.Logger(s => s.Filter.ByIncludingOnly(e => e.Level >= LogEventLevel.Warning)
                .WriteTo.File(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Logs", "errors", "log-.txt"),
                                rollingInterval: RollingInterval.Day,
                                outputTemplate: vOutputTemplate,
                                retainedFileCountLimit: 100));

            var esUrl = hostingContext.Configuration.GetSection("ElasticSearchUrl").Value;

            var indexFormat = $"{appName}" + "-{0:yyyy.MM}";

            if (!string.IsNullOrWhiteSpace(esUrl))
            {
                loggerConfiguration.WriteTo.Elasticsearch(new ElasticsearchSinkOptions(new Uri(esUrl))
                {
                    MinimumLogEventLevel = LogEventLevel.Information,
                    AutoRegisterTemplate = true,
                    IndexFormat = indexFormat
                });
            }
        });
    }

    public static void AddCustomMVC(this WebApplicationBuilder builder)
    {
        builder.Services.AddControllers()
        .AddJsonOptions(options =>
        {
            //数据格式原样输出
            options.JsonSerializerOptions.PropertyNamingPolicy = null;
            //取消Unicode编码
            options.JsonSerializerOptions.Encoder = JavaScriptEncoder.Create(UnicodeRanges.All);
            //允许额外符号
            options.JsonSerializerOptions.AllowTrailingCommas = true;
        });

        builder.Services.AddCors(options =>
        {
            options.AddPolicy("CorsPolicy", policy =>
            {
                var withOrigins = builder.Configuration["WithOrigins"];
                if (!string.IsNullOrWhiteSpace(withOrigins) && withOrigins.Split(';').Length > 0)
                    policy.WithOrigins(withOrigins.Split(';'));
                else
                    policy.SetIsOriginAllowed((host) => true);

                policy.AllowAnyMethod();
                policy.AllowAnyHeader();
                policy.AllowCredentials();
            });
        });
    }

        public static void AddCustomDbContext(this WebApplicationBuilder builder)
        {
            AppContext.SetSwitch("Npgsql.EnableLegacyTimestampBehavior", true);
            AppContext.SetSwitch("Npgsql.DisableDateTimeInfinityConversions", true);
            var vDbType = builder.Configuration["CurrentDbType"];
            IocDbType vIocDbType = IocDbType.SqlServer;
            switch (vDbType)
            {
                case "SqlServer":
                    vIocDbType = IocDbType.SqlServer;
                    break;

                case "MySql":
                    vIocDbType = IocDbType.MySql;
                    break;

                case "PostgreSQL":
                    vIocDbType = IocDbType.PostgreSQL;
                    break;
            }
            builder.Services.AddSqlSugar(new IocConfig()
            {
                ConfigId = "EquipmentAPI",
                ConnectionString = builder.Configuration[$"DataBase:{vIocDbType}:Database_ConnString"],
                DbType = vIocDbType,
                IsAutoCloseConnection = true
            });
            //AOP 统一配置  禁止循环，只能声名一次
            builder.Services.ConfigurationSugar(db =>
            {
                //里面可以循环
                db.GetConnection("API").Aop.OnLogExecuting = (sql, p) =>
                {
#if DEBUG
                    //ConsoleColor currentForeColor = Console.ForegroundColor;
                    //Console.ForegroundColor = ConsoleColor.Blue;
                    //Console.WriteLine(sql);
                    //Console.ForegroundColor = currentForeColor;
#endif
                };
                //里面可以循环
                db.GetConnection("API").Aop.OnError = (exp) =>
                {
#if DEBUG
                    ConsoleColor currentForeColor = Console.ForegroundColor;
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"{exp.Message}：{exp.Sql}");
                    Console.ForegroundColor = currentForeColor;
#endif
                };
            });
        }

    public static void AddCustomSwagger(this WebApplicationBuilder builder)
    {
        builder.Services.AddSwaggerGen(options =>
        {
            foreach (FieldInfo fileld in typeof(ApiVersionInfo).GetFields())
            {
                options.SwaggerDoc(fileld.Name, new OpenApiInfo
                {
                    Version = fileld.Name,
                    Title = $"API {fileld.Name} 接口文档",
                    Description = $"API {fileld.Name} 接口文档"
                });
            }
            var xmlFilename = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
            options.IncludeXmlComments(Path.Combine(AppContext.BaseDirectory, xmlFilename));
        });
    }

    public static void AddCustomHealthChecks(this WebApplicationBuilder builder)
    {
        builder.Services.AddHealthChecks()
            .AddCheck(appName, () => HealthCheckResult.Healthy())
            .AddCheck<DaprHealthCheck>("dapr");
    }
}

public class AutofacModule : Autofac.Module
{
    protected override void Load(ContainerBuilder builder)
    {
        // 定义需要注册的程序集列表
        var vAssemblies = new[]
        {
            Assembly.Load("Domain"),
            Assembly.Load("Infrastructure"),
            Assembly.Load("Common"),
            Assembly.Load("Application")
        };

        // 注册所有实现了接口的类型，每个依赖关系创建一个新的实例
        foreach (var vAssembly in vAssemblies)
        {
            builder.RegisterAssemblyTypes(vAssembly)
                   .AsImplementedInterfaces()
                   .InstancePerDependency();
        }
    }
}
```

### Program.cs Setup

```csharp
CultureInfo.DefaultThreadCurrentCulture = new CultureInfo("zh-CN", true) { DateTimeFormat = { ShortDatePattern = "yyyy-MM-dd", FullDateTimePattern = "yyyy-MM-dd HH:mm:ss", LongTimePattern = "HH:mm:ss" } };
var builder = WebApplication.CreateBuilder(args);
builder.Services.Configure<KestrelServerOptions>(k => k.AllowSynchronousIO = true)
    .Configure<IISServerOptions>(k => k.AllowSynchronousIO = true);
var app = builder.Build();
builder.AddCustomDaprdProcess();
builder.AddCustomAutofac();
builder.AddCustomLog();
builder.AddCustomMVC();
builder.AddCustomServices();
builder.AddCustomDbContext();
builder.AddCustomSwagger();
builder.AddCustomHealthChecks();
builder.Services.AddHttpClient();

var appPort = app.Configuration["AppProfile:AppPort"].ToString();
app.Urls.Add($"http://*:{appPort}");
if (app.Environment.IsDevelopment())
{
    app.UseSwagger().UseSwaggerUI(s =>
    {
        foreach (FieldInfo field in typeof(ApiVersionInfo).GetFields())
        {
            s.SwaggerEndpoint($"/swagger/{field.Name}/swagger.json", $"API {field.Name} 版本");
        }
    });
}
app.Use(
    (context, next) =>
    {
        context.Request.EnableBuffering();
        return next(context);
    });
app.UseCloudEvents();
app.UseRouting();
app.UseCors("CorsPolicy");
app.MapDefaultControllerRoute();
app.MapControllers();
app.MapSubscribeHandler();
app.MapCustomHealthChecks();
try
{    
    app.Logger.LogInformation("==============Starting API WebHost==============");
    app.Run();
}
catch (Exception e)
{
    app.Logger.LogError(e, "==============Host terminated unexpectedly==============");
}
finally
{
    Log.CloseAndFlush();
}
```

---

## Result Pattern

### API Result

```csharp
// Common/ApiResult.cs
public class BaseResult
{
    /// <summary>
    /// 响应码
    /// </summary>
    [NotNull]
    public virtual HttpStatusCode Code { get; set; }


    /// <summary>
    /// 响应成功
    /// </summary>
    /// <returns></returns>
    public virtual void Success()
    {
        Code = HttpStatusCode.OK;
    }

    /// <summary>
    /// 响应失败
    /// </summary>
    /// <param name="message"></param>
    public virtual void Failed()
    {
        Code = HttpStatusCode.InternalServerError;
    }
}

/// <summary>
/// API返回结果结构
/// </summary>
public class ApiResult : BaseResult
{
    public ApiResult()
    {
        Success();
    }

    private string _Message = string.Empty;
    private string _Data = string.Empty;
    private byte[] _Base64Data;
    private string _ModelType = string.Empty;

    /// <summary>
    /// 消息提示
    /// </summary>
    public string Message { get => _Message; set => _Message = value; }
    /// <summary>
    /// 数据源
    /// </summary>
    public string Data { get => _Data; set => _Data = value; }
    /// <summary>
    /// 数据源模型
    /// </summary>
    public string ModelType { get => _ModelType; set => _ModelType = value; }
    /// <summary>
    /// Base64数据源
    /// </summary>
    public byte[] Base64Data { get => _Base64Data; set => _Base64Data = value; }


    /// <summary>
    /// 响应成功
    /// </summary>
    /// <param name="message">消息</param>
    public void Success(string message)
    {
        base.Success();
        _Message = message;
    }

    /// <summary>
    /// 响应成功
    /// </summary>
    /// <param name="data">数据</param>
    public void Success(dynamic data)
    {
        base.Success();

        _Data = JsonSerializer.Serialize(data, new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.Create(UnicodeRanges.All)
        });

        _ModelType = GetDataType(data);
    }


    /// <summary>
    /// 响应成功
    /// </summary>
    /// <param name="data">数据</param>
    /// <param name="message">消息</param>
    public void Success(dynamic data, string message)
    {
        base.Success();
        _Message = message;
        _Data = JsonSerializer.Serialize(data, new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.Create(UnicodeRanges.All)
        });
        _ModelType = GetDataType(data);
    }


    /// <summary>
    /// 响应成功
    /// </summary>
    /// <param name="dataList">数据</param>
    public void Success<T>(List<T> dataList)
    {
        base.Success();

        if (dataList != null && dataList.Any())
        {
            _Data = JsonSerializer.Serialize(dataList, new JsonSerializerOptions
            {
                Encoder = JavaScriptEncoder.Create(UnicodeRanges.All)
            });
            _ModelType = GetDataType(dataList);
        }
        else
        {
            _Data = string.Empty;
            _ModelType = string.Empty;
        }
    }

    /// <summary>
    /// 响应成功
    /// </summary>
    /// <param name="dataList">数据</param>
    /// <param name="message">消息</param>
    public void Success<T>(List<T> dataList, string message)
    {
        base.Success();
        _Message = message;
        if (dataList != null && dataList.Any())
        {
            _Data = JsonSerializer.Serialize(dataList, new JsonSerializerOptions
            {
                Encoder = JavaScriptEncoder.Create(UnicodeRanges.All)
            });
            _ModelType = GetDataType(dataList);
        }
        else
        {
            _Data = string.Empty;
            _ModelType = string.Empty;
        }
    }

    /// <summary>
    /// 响应失败
    /// </summary>
    /// <param name="message"></param>
    public void Failed(string message)
    {
        base.Failed();
        _Message = message;
    }

    /// <summary>
    /// 响应失败
    /// </summary>
    /// <param name="ex"></param>
    public void Failed(Exception ex)
    {
        base.Failed();
        _Message = ex.Message.ToString();
    }

    /// <summary>
    /// 响应失败
    /// </summary>
    /// <param name="ex"></param>
    public void Failed(HttpStatusCode httpStatusCode, string message)
    {
        Code = httpStatusCode;
        _Message = message;
    }


    /// <summary>
    /// 成功
    /// </summary>
    /// <param name="dataSource">数据源</param>
    /// <param name="code">状态码</param>
    /// <param name="message">消息提示</param>
    /// <param name="isSerialize">是否需要序列化</param>
    public static ApiResult Success(dynamic dataSource, string message = "操作成功", HttpStatusCode code = HttpStatusCode.OK, bool isSerialize = true)
    {
        return new ApiResult(dataSource, code, message, isSerialize);
    }

    /// <summary>
    /// 成功
    /// </summary>
    /// <param name="dataSourceList">数据源</param>
    /// <param name="code">状态码</param>
    /// <param name="message">消息提示</param>
    /// <param name="isSerialize">是否需要序列化</param>
    public static ApiResult Success<T>(List<T> dataSourceList, string message = "操作成功", HttpStatusCode code = HttpStatusCode.OK, bool isSerialize = true)
    {
        if (dataSourceList != null && dataSourceList.Any())
        {
            return new ApiResult(dataSourceList, code, message, isSerialize);
        }
        else
        {
            return new ApiResult(string.Empty, code, message, isSerialize);
        }
    }

    /// <summary>
    /// 失败
    /// </summary>
    /// <param name="code">状态码</param>
    /// <param name="message">消息提示</param>
    public static ApiResult Failed(string message = "操作失败", HttpStatusCode code = HttpStatusCode.InternalServerError)
    {
        return new ApiResult(string.Empty, code, message, false);
    }

    /// <summary>
    /// 响应模型
    /// </summary>
    /// <param name="dataSource">数据源</param>
    /// <param name="code">状态码</param>
    /// <param name="message">消息提示</param>
    /// <param name="isSerialize">是否需要序列化</param>
    private ApiResult(dynamic dataSource, HttpStatusCode code, string message, bool isSerialize)
    {
        if (dataSource != null && dataSource.GetType() == typeof(byte[]) && !isSerialize)
        {
            _Base64Data = dataSource;
        }
        else if (dataSource != null && dataSource?.GetType() != typeof(string) && isSerialize)
        {
            _Data = JsonSerializer.Serialize(dataSource, new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                NumberHandling = JsonNumberHandling.WriteAsString,
                Encoder = JavaScriptEncoder.Create(UnicodeRanges.All)
            });
        }
        else
        {
            _Data = dataSource;
        }
        Code = code;
        _Message = message;
        _ModelType = GetDataType(dataSource);
    }



    /// <summary>
    /// 获取返回模型的所有属性
    /// </summary>
    /// <param name="data"></param>
    /// <returns></returns>
    private static string GetDataType(dynamic data)
    {
        var str = string.Empty;

        System.Reflection.PropertyInfo[] properties = data.GetType().GetProperties();

        foreach (System.Reflection.PropertyInfo property in properties)
        {
            string propertyName = property.Name;
            string propertyType = property.PropertyType.Name;

            str += $"{propertyName} ({propertyType}),";
        }

        return !string.IsNullOrWhiteSpace(str) ? str[..^1] : str;
    }
}

/// <summary>
/// 泛型类型返回体
/// </summary>
/// <typeparam name="T"></typeparam>
public class ApiResult<T> : ApiResult
{
    /// <summary>
    /// 数据
    /// </summary>
    public T TData { get; set; }

    /// <summary>
    /// 列表的记录数
    /// </summary>
    public int Total { get; set; }
}
```

### Application

```csharp
// Application/IServices/IBaseService.cs
public interface IBaseService<T> where T : class, new()
{
    /// <summary>
    /// 添加
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    bool Insert(T AEntity);

    /// <summary>
    /// 添加
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    Task<bool> InsertAsync(T AEntity);

    /// <summary>
    /// 批量添加
    /// </summary>
    /// <param name="AList"></param>
    /// <returns></returns>
    Task<bool> InsertRangeAsync(List<T> AList);

    /// <summary>
    /// 删除
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    bool Delete(T AEntity);

    /// <summary>
    /// 删除
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    Task<bool> DeleteAsync(dynamic AId);

    /// <summary>
    /// 批量删除
    /// </summary>
    /// <param name="AIds"></param>
    /// <returns></returns>
    Task<bool> DeleteByIdsAsync(dynamic[] AIds);

    /// <summary>
    /// 更新
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    bool Update(T AEntity);

    /// <summary>
    /// 更新
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    Task<bool> UpdateAsync(T AEntity);

    /// <summary>
    /// 批量更新
    /// </summary>
    /// <param name="AList"></param>
    /// <returns></returns>
    Task<bool> UpdateRangeAsync(List<T> AList);

    /// <summary>
    /// 查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    T Find(Expression<Func<T, bool>> func);

    /// <summary>
    /// 根据ID查询
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    Task<T> FindAsync(dynamic AId);

    /// <summary>
    /// 查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    Task<T> FindAsync(Expression<Func<T, bool>> func);

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    List<T> Query();

    /// <summary>
    /// 自定义查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    List<T> Query(Expression<Func<T, bool>> func);

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    Task<List<T>> QueryAsync();

    /// <summary>
    /// 自定义查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> func);

    /// <summary>
    /// 分页查询
    /// </summary>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, string orderByFields, int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="whereExpression"></param>
    /// <param name="orderByExpression"></param>
    /// <param name="order"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> whereExpression, Expression<Func<T, object>> orderByExpression, OrderByType order, int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 开始事务
    /// </summary>
    void BeginTran();

    /// <summary>
    /// 提交
    /// </summary>
    void CommitTran();

    /// <summary>
    /// 回滚
    /// </summary>
    void RollbackTran();

    #region 执行sql

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    DataTable GetDataTable(string sql, object parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    DataTable GetDataTable(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    DataTable GetDataTable(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    Task<DataTable> GetDataTableAsync(string sql, object parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="ASql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    Task<DataTable> GetDataTableAsync(string ASql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    Task<DataTable> GetDataTableAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    DataSet GetDataSetAll(string sql, object parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    DataSet GetDataSetAll(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    DataSet GetDataSetAll(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    Task<DataSet> GetDataSetAllAsync(string sql, object parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    Task<DataSet> GetDataSetAllAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    Task<DataSet> GetDataSetAllAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    IDataReader GetDataReader(string sql, object parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    IDataReader GetDataReader(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    IDataReader GetDataReader(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    Task<IDataReader> GetDataReaderAsync(string sql, object parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    Task<IDataReader> GetDataReaderAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    Task<IDataReader> GetDataReaderAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    object GetScalar(string sql, object parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    object GetScalar(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    object GetScalar(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    Task<object> GetScalarAsync(string sql, object parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    Task<object> GetScalarAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    Task<object> GetScalarAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommandWithGo(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommand(string sql, object parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommand(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommand(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    Task<int> ExecuteCommandAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    Task<int> ExecuteCommandAsync(string sql, object parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    Task<int> ExecuteCommandAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    List<T> SqlQuery<T>(string sql, object parameters = null);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    List<T> SqlQuery<T>(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    List<T> SqlQuery<T>(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    Task<List<T>> SqlQueryAsync<T>(string sql, object parameters = null);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    Task<List<T>> SqlQueryAsync<T>(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    Task<List<T>> SqlQueryAsync<T>(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="whereObj"></param>
    /// <returns></returns>
    T SqlQuerySingle<T>(string sql, object whereObj = null);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    T SqlQuerySingle<T>(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    T SqlQuerySingle<T>(string sql, List<SugarParameter> parameters);

    #endregion
}
```
```csharp
// Application/IServices/ITestService.cs
public interface ITestService : IBaseService<Test>
{
}
```

```csharp
// Application/IServices/BaseService.cs.cs
public class BaseService<T> : IBaseService<T> where T : class, new()
{
    protected IBaseRepository<T> _BaseRepository;

    public bool Delete(T AEntity)
    {
        return _BaseRepository.Delete(AEntity);
    }

    public async Task<bool> DeleteAsync(dynamic AId)
    {
        return await _BaseRepository.DeleteAsync(AId);
    }

    public async Task<bool> DeleteByIdsAsync(dynamic[] AIds)
    {
        return await _BaseRepository.DeleteByIdsAsync(AIds);
    }

    public T Find(Expression<Func<T, bool>> func)
    {
        return _BaseRepository.Find(func);
    }

    public async Task<T> FindAsync(dynamic AId)
    {
        return await _BaseRepository.FindAsync(AId);
    }

    public async Task<T> FindAsync(Expression<Func<T, bool>> func)
    {
        return await _BaseRepository.FindAsync(func);
    }

    public bool Insert(T AEntity)
    {
        return _BaseRepository.Insert(AEntity);
    }

    public async Task<bool> InsertAsync(T AEntity)
    {
        return await _BaseRepository.InsertAsync(AEntity);
    }

    public async Task<bool> InsertRangeAsync(List<T> AList)
    {
        return await _BaseRepository.InsertRangeAsync(AList); ;
    }

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    public List<T> Query()
    {
        return _BaseRepository.Query();
    }

    /// <summary>
    /// 自定义查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    public List<T> Query(Expression<Func<T, bool>> func)
    {
        return _BaseRepository.Query(func);
    }

    public async Task<List<T>> QueryAsync()
    {
        return await _BaseRepository.QueryAsync();
    }

    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func)
    {
        return await _BaseRepository.QueryAsync(func);
    }

    public async Task<List<T>> QueryAsync(int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await _BaseRepository.QueryAsync(APageIndex, APageSize, ATotal);
    }

    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await _BaseRepository.QueryAsync(func, APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, string orderByFields, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await _BaseRepository.QueryAsync(func, orderByFields, APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="whereExpression"></param>
    /// <param name="orderByExpression"></param>
    /// <param name="order"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> whereExpression, Expression<Func<T, object>> orderByExpression, OrderByType order, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await _BaseRepository.QueryAsync(whereExpression, orderByExpression, order, APageIndex, APageSize, ATotal);
    }

    public bool Update(T AEntity)
    {
        return _BaseRepository.Update(AEntity);
    }

    public async Task<bool> UpdateAsync(T AEntity)
    {
        return await _BaseRepository.UpdateAsync(AEntity);
    }

    public async Task<bool> UpdateRangeAsync(List<T> AList)
    {
        return await _BaseRepository.UpdateRangeAsync(AList);
    }

    /// <summary>
    /// 开始事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void BeginTran()
    {
        _BaseRepository.BeginTran();
    }

    /// <summary>
    /// 提交事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void CommitTran()
    {
        _BaseRepository.CommitTran();
    }

    /// <summary>
    /// 回滚事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void RollbackTran()
    {
        _BaseRepository.RollbackTran();
    }

    #region 执行sql

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, object parameters)
    {
        return _BaseRepository.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string sql, object parameters)
    {
        return await _BaseRepository.GetDataTableAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="ASql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string ASql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.GetDataTableAsync(ASql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.GetDataTableAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, object parameters)
    {
        return _BaseRepository.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, object parameters)
    {
        return await _BaseRepository.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, object parameters)
    {
        return _BaseRepository.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public async Task<IDataReader> GetDataReaderAsync(string sql, object parameters)
    {
        return await _BaseRepository.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public async Task<IDataReader> GetDataReaderAsync(string sql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public async Task<IDataReader> GetDataReaderAsync(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, object parameters)
    {
        return _BaseRepository.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, object parameters)
    {
        return await _BaseRepository.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommandWithGo(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.ExecuteCommandWithGo(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, object parameters)
    {
        return _BaseRepository.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, object parameters)
    {
        return await _BaseRepository.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, object parameters = null)
    {
        return _BaseRepository.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, object parameters = null)
    {
        return await _BaseRepository.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="whereObj"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, object whereObj = null)
    {
        return _BaseRepository.SqlQuerySingle<T>(sql, whereObj);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.SqlQuerySingle<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.SqlQuerySingle<T>(sql, parameters);
    }

    #endregion
}
```
```csharp
// Application/Services/TestService.cs
public class TestService : BaseService<Test>, ITestService
{
    private readonly ITestRepository _Repository;

    public TestService(ITestRepository repository)
    {
        base._BaseRepository = repository;
        _Repository = repository;
    }
}
```

---

## Domain

```csharp
// Domain/SeedWork/BaseEntity.cs
/// <summary>
/// 实体基类
/// </summary>
public class BaseEntity
{
    /// <summary>
    /// 是否标记删除
    /// </summary>
    public bool IsDelete { get; set; } = false;

    /// <summary>
    /// 创建时间
    /// </summary>
    public DateTime CreateDateTime { get; set; } = DateTime.Now;

    /// <summary>
    /// 最后修改时间
    /// </summary>
    public DateTime LastupdateDateTime { get; set; } = DateTime.Now;
}
```
```csharp
// Domain/Models/Test.cs
/// <summary>
/// 
/// </summary>
[SugarTable("t_test")]
public class Test : BaseEntity
{
    /// <summary>
    /// 主键ID
    /// </summary>
    [SugarColumn(IsPrimaryKey = true, ColumnDescription = "主键")]
    public long Id { get; set; }
}
```
``` csharp
// Domain/SeedWork/IBaseRepository.cs
/// <summary>
/// 仓储基类接口
/// </summary>
/// <typeparam name="T"></typeparam>
public interface IBaseRepository<T> where T : class, new()
{
    /// <summary>
    /// 添加
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    bool Insert(T AEntity);

    /// <summary>
    /// 添加
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    Task<bool> InsertAsync(T AEntity);

    /// <summary>
    /// 批量添加
    /// </summary>
    /// <param name="AList"></param>
    /// <returns></returns>
    Task<bool> InsertRangeAsync(List<T> AList);

    /// <summary>
    /// 删除
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    bool Delete(T AEntity);

    /// <summary>
    /// 删除
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    Task<bool> DeleteAsync(dynamic AId);

    /// <summary>
    /// 批量删除
    /// </summary>
    /// <param name="AIds"></param>
    /// <returns></returns>
    Task<bool> DeleteByIdsAsync(dynamic[] AIds);

    /// <summary>
    /// 更新
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    bool Update(T AEntity);

    /// <summary>
    /// 更新
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    Task<bool> UpdateAsync(T AEntity);

    /// <summary>
    /// 批量更新
    /// </summary>
    /// <param name="AList"></param>
    /// <returns></returns>
    Task<bool> UpdateRangeAsync(List<T> AList);

    /// <summary>
    /// 查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    T Find(Expression<Func<T, bool>> func);

    /// <summary>
    /// 根据ID查询
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    Task<T> FindAsync(dynamic AId);

    /// <summary>
    /// 查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    Task<T> FindAsync(Expression<Func<T, bool>> func);

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    List<T> Query();

    /// <summary>
    /// 自定义查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    List<T> Query(Expression<Func<T, bool>> func);

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    Task<List<T>> QueryAsync();

    /// <summary>
    /// 自定义查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> func);

    /// <summary>
    /// 分页查询
    /// </summary>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, string orderByFields, int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="whereExpression"></param>
    /// <param name="orderByExpression"></param>
    /// <param name="order"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> whereExpression, Expression<Func<T, object>> orderByExpression, OrderByType order, int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 开始事务
    /// </summary>
    void BeginTran();

    /// <summary>
    /// 提交
    /// </summary>
    void CommitTran();

    /// <summary>
    /// 回滚
    /// </summary>
    void RollbackTran();

    #region 执行sql

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    DataTable GetDataTable(string sql, object parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    DataTable GetDataTable(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    DataTable GetDataTable(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    Task<DataTable> GetDataTableAsync(string sql, object parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="ASql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    Task<DataTable> GetDataTableAsync(string ASql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    Task<DataTable> GetDataTableAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    DataSet GetDataSetAll(string sql, object parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    DataSet GetDataSetAll(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    DataSet GetDataSetAll(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    Task<DataSet> GetDataSetAllAsync(string sql, object parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    Task<DataSet> GetDataSetAllAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    Task<DataSet> GetDataSetAllAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    IDataReader GetDataReader(string sql, object parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    IDataReader GetDataReader(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    IDataReader GetDataReader(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    Task<IDataReader> GetDataReaderAsync(string sql, object parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    Task<IDataReader> GetDataReaderAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    Task<IDataReader> GetDataReaderAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    object GetScalar(string sql, object parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    object GetScalar(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    object GetScalar(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    Task<object> GetScalarAsync(string sql, object parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    Task<object> GetScalarAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    Task<object> GetScalarAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommandWithGo(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommand(string sql, object parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommand(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommand(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    Task<int> ExecuteCommandAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    Task<int> ExecuteCommandAsync(string sql, object parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    Task<int> ExecuteCommandAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    List<T> SqlQuery<T>(string sql, object parameters = null);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    List<T> SqlQuery<T>(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    List<T> SqlQuery<T>(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    Task<List<T>> SqlQueryAsync<T>(string sql, object parameters = null);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    Task<List<T>> SqlQueryAsync<T>(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    Task<List<T>> SqlQueryAsync<T>(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    T SqlQuerySingle<T>(string sql, object whereObj = null);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    T SqlQuerySingle<T>(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    T SqlQuerySingle<T>(string sql, List<SugarParameter> parameters);

    #endregion
}
```
```csharp
// Domain/Repositories/ITestRepository.cs
public interface ITestRepository: IBaseRepository<Test>
{
}
```

## Infrastructure

```csharp
// Infrastructure/Repositories/BaseRepository.cs
public class BaseRepository<T> : SimpleClient<T>, IBaseRepository<T> where T : class, new()
{
    public BaseRepository(ISqlSugarClient context = null) : base(context)
    {
        base.Context = DbScoped.SugarScope;
    }

    /// <summary>
    /// 根据ID删除数据
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    public async Task<bool> DeleteAsync(dynamic AId)
    {
        return await DeleteByIdAsync(AId);
    }

    /// <summary>
    /// 批量删除
    /// </summary>
    /// <param name="AIds"></param>
    /// <returns></returns>
    public async Task<bool> DeleteByIdsAsync(dynamic[] AIds)
    {
        return await base.DeleteByIdsAsync(AIds);
    }

    /// <summary>
    /// 根据ID查询数据
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    public virtual async Task<T> FindAsync(dynamic AId)
    {
        return await GetByIdAsync(AId);
    }

    /// <summary>
    /// 根据ID查询
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    public async Task<T> FindAsync(Expression<Func<T, bool>> func)
    {
        return await GetSingleAsync(func);
    }

    /// <summary>
    /// 添加
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    public async Task<bool> InsertAsync(T AEntity)
    {
        return await base.InsertAsync(AEntity);
    }

    /// <summary>
    /// 批量添加
    /// </summary>
    /// <param name="AList"></param>
    /// <returns></returns>
    public async Task<bool> InsertRangeAsync(List<T> AList)
    {
        return await base.InsertRangeAsync(AList);
    }

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    public List<T> Query()
    {
        return base.GetList();
    }

    /// <summary>
    /// 自定义查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    public List<T> Query(Expression<Func<T, bool>> func)
    {
        return base.GetList(func);
    }

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync()
    {
        return await base.GetListAsync();
    }

    /// <summary>
    /// 自定义条件查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func)
    {
        return await base.GetListAsync(func);
    }

    /// <summary>
    /// 分页查询
    /// </summary>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await base.Context.Queryable<T>().ToPageListAsync(APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await base.Context.Queryable<T>().Where(func).ToPageListAsync(APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, string orderByFields, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await base.Context.Queryable<T>().Where(func).OrderBy(orderByFields).ToPageListAsync(APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="whereExpression"></param>
    /// <param name="orderByExpression"></param>
    /// <param name="order"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> whereExpression, Expression<Func<T, object>> orderByExpression, OrderByType order, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await base.Context.Queryable<T>().Where(whereExpression).OrderBy(orderByExpression, order).ToPageListAsync(APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 更新
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    public async Task<bool> UpdateAsync(T AEntity)
    {
        return await base.UpdateAsync(AEntity);
    }

    /// <summary>
    /// 批量修改
    /// </summary>
    /// <param name="AList"></param>
    /// <returns></returns>
    public async Task<bool> UpdateRangeAsync(List<T> AList)
    {
        return await base.UpdateRangeAsync(AList);
    }

    /// <summary>
    /// 插入
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    public bool Insert(T AEntity)
    {
        return base.Insert(AEntity);
    }

    /// <summary>
    /// 删除
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    public bool Delete(T AEntity)
    {
        return base.Delete(AEntity);
    }

    /// <summary>
    /// 更新
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    public bool Update(T AEntity)
    {
        return base.Update(AEntity);
    }

    /// <summary>
    /// 查询数据
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    public T Find(Expression<Func<T, bool>> func)
    {
        return base.GetFirst(func);
    }

    /// <summary>
    /// 开始事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void BeginTran()
    {
        base.Context.Ado.BeginTran();
    }

    /// <summary>
    /// 提交事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void CommitTran()
    {
        base.Context.Ado.CommitTran();
    }

    /// <summary>
    /// 回滚事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void RollbackTran()
    {
        base.Context.Ado.RollbackTran();
    }

    #region 执行sql

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, object parameters)
    {
        return base.Context.Ado.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string sql, object parameters)
    {
        return await base.Context.Ado.GetDataTableAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="ASql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string ASql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.GetDataTableAsync(ASql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.GetDataTableAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, object parameters)
    {
        return base.Context.Ado.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, object parameters)
    {
        return await base.Context.Ado.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, object parameters)
    {
        return base.Context.Ado.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public async Task<IDataReader> GetDataReaderAsync(string sql, object parameters)
    {
        return await base.Context.Ado.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public async Task<IDataReader> GetDataReaderAsync(string sql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public async Task<IDataReader> GetDataReaderAsync(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, object parameters)
    {
        return base.Context.Ado.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, object parameters)
    {
        return await base.Context.Ado.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommandWithGo(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.ExecuteCommandWithGo(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, object parameters)
    {
        return base.Context.Ado.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, object parameters)
    {
        return await base.Context.Ado.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, object parameters = null)
    {
        return base.Context.Ado.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, object parameters = null)
    {
        return await base.Context.Ado.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="whereObj"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, object whereObj = null)
    {
        return base.Context.Ado.SqlQuerySingle<T>(sql, whereObj);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.SqlQuerySingle<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.SqlQuerySingle<T>(sql, parameters);
    }

    #endregion
}

// Infrastructure/Repositories/TestRepository.cs
public class TestRepository : BaseRepository<Test>, ITestRepository
{
}
```

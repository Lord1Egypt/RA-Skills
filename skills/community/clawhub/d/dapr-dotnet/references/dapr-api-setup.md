# Dapr 组件配置与启动管道模板

> 摘自 dapr-dotnet 技能 v1.0.0「API Patterns」章节。包含：Dapr 组件 yaml、Extensions 全套、Program.cs 启动代码。

## 一、Dapr 组件 yaml

```yaml
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

## 二、Extensions

### BaseController.cs

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

### ApiVersionInfo.cs

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

### CustomExtensions.cs

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

### DaprHealthCheck.cs

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

### ProgramExtensions.cs

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

## 三、Program.cs

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
        return next();
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

## 四、配置项约定（appsettings.json）

| 配置键 | 说明 | 示例值 |
|---|---|---|
| `AppProfile:AppId` | Dapr app-id | `jytplatformequpmentapi` |
| `AppProfile:AppPort` | 应用监听端口 | `8118` |
| `AppProfile:DaprHttpPort` | Dapr sidecar HTTP 端口 | `18118` |
| `AppProfile:DaprGrpcPort` | Dapr sidecar gRPC 端口 | `28118` |
| `CurrentDbType` | 当前数据库类型 | `SqlServer` / `MySql` / `PostgreSQL` |
| `DataBase:{DbType}:Database_ConnString` | 对应数据库连接串 | — |
| `WithOrigins` | CORS 允许来源，`;` 分隔；为空则放行全部 | `https://a.com;https://b.com` |
| `ElasticSearchUrl` | Serilog ES 输出地址；为空则不写 ES | — |

## 五、已知注意点

1. **Program.cs 调用顺序**：原模板中 `var app = builder.Build();` 位于各 `AddCustom*` 之前，`builder.Build()` 之后再注册服务不会生效。落地时应将 `builder.Build()` 移到全部 `AddCustom*` 调用之后。
2. **`AddCustomDaprdProcess` 的 DEBUG 分支**依赖外部 `BaseHelper.AddDaprdProcess(...)` 拉起本地 daprd 进程；Release 分支直接 `AddDapr()` 连接已运行的 sidecar。
3. **SqlSugar AOP 配置**（`ConfigurationSugar`）全局只能声明一次，不可在多个扩展方法中重复配置。
4. **健康检查端点**：`/dapr`（含 Dapr sidecar 探针，UI 格式输出）与 `/app`（应用自身）。

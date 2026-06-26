# Natasha 初始化方法完全指南

## 三种编译模式与初始化策略选择

| 模式 | 初始化方式 | 适用场景 |
|------|-----------|---------|
| **智能模式 (Smart)** | 需要预热 Using + Reference | 通用场景，全自动元数据管理 |
| **精简模式 (Simple)** | 仅注册域创建器，无需预热 | 精确控制元数据，最小化开销 |
| **自定义编译模式** | 无需预热，自备元数据集 | 完全掌控，使用第三方引用集 |

### 智能模式：内存程序集 vs 引用程序集

智能模式下需要选择使用哪种来源的元数据：

| 对比维度 | 内存程序集（Memory）| 引用程序集（Ref）|
|---------|-------------------|----------------|
| 元数据覆盖度 | 当前运行时已加载的程序集 | 最完整，含所有未加载的程序集 |
| 内存占用 | 较低 | 较高 |
| 启动速度 | 较快 | 较慢 |
| 推荐场景 | 绝大多数日常场景 | 不在意程序大小和内存，需要最完整元数据 |

**决策规则：** 如果用户不在意程序大小和内存占用，优先使用引用程序集（`WithRefUsing().WithRefReference()`），其覆盖的元数据最为全面。

---

## 必需的 NuGet 包

安装以下包来使用 Natasha 的完整功能：

```bash
# 编译器核心包（必需）
dotnet add package DotNetCore.Natasha.CSharp.Compiler

# 编译域包（必需，处理内存程序集编译）
dotnet add package DotNetCore.Natasha.CSharp.Compiler.Domain

# 域管理包（可选，用于插件和高级域管理）
dotnet add package DotNetCore.Natasha.Domain
```

**支持的框架：** .NET Core 3.1+, .NET 5.0+, .NET 6.0+, .NET 7.0+, .NET 8.0+

## 标准初始化方式

### 方式 1：推荐 - 分步初始化（标准方式）

```csharp
using Natasha;
using Natasha.CSharp;

// 在应用启动时执行一次
NatashaManagement.RegistDomainCreator<NatashaDomainCreator>();
NatashaManagement.Preheating(true, true);  // (withMemoryUsing, withMemoryReference)
```

**参数说明：**
- 第一个 `true` - 从内存程序集中提取 Using Code
- 第二个 `true` - 从内存程序集中提取元数据

### 方式 2：链式初始化（V9+，更清晰）

```csharp
using Natasha;
using Natasha.CSharp;

// 在应用启动时执行一次
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()        // 使用内存中的 using 指令
    .WithMemoryReference()    // 使用内存中的元数据
    .Preheating<NatashaDomainCreator>();
```

**链式 API 选项：**
- `WithRefUsing()` - 使用引用程序集中的 using 指令
- `WithRefReference()` - 使用引用程序集中的元数据（覆盖最全面）
- `WithMemoryUsing()` - 使用内存程序集中的 using 指令
- `WithMemoryReference()` - 使用内存程序集中的元数据
- `WithFileUsingCache()` - 使用文件缓存 using 指令（项目依赖稳定时启用）
- `WithExcludeReferences()` - 排除指定程序集

### 引用程序集预热（最完整元数据）

适合不在意程序大小和内存占用、需要最完整元数据的场景：

```csharp
// 使用引用程序集预热（覆盖最完整的元数据）
NatashaManagement
    .GetInitializer()
    .WithRefUsing()          // 从引用程序集文件提取 using code
    .WithRefReference()      // 从引用程序集文件提取元数据（最全面）
    .Preheating<NatashaDomainCreator>();
```

> **注意：** 使用引用程序集预热需要系统中存在 .NET SDK 的引用程序集文件。如果找不到，Natasha 会抛出异常并建议引入 `DotNetCore.Compile.Environment` 环境包。

### WithFileUsingCache 使用时机

`WithFileUsingCache()` 会将 using-code 写入 `Natasha.Namespace.cache` 文件。**仅在项目依赖稳定（不再添加新 NuGet 包）时启用**，此后每次启动直接读缓存，大幅加快启动速度：

```csharp
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()
    .WithMemoryReference()
    .WithFileUsingCache()    // 项目稳定后启用，首次生成缓存文件，后续直接读取
    .Preheating<NatashaDomainCreator>();
```

## 高级初始化：程序集过滤

过滤不需要的程序集以减少内存占用：

```csharp
// 方式 1：分步过滤
NatashaManagement.RegistDomainCreator<NatashaDomainCreator>();
NatashaManagement.Preheating<NatashaDomainCreator>((asmName, name) => {
    if (asmName.Name != null)
    {
        // 排除 Dapper 主版本号 > 12 的程序集
        if (asmName.Name.Contains("Dapper") && asmName.Version!.Major > 12)
        {
            return true;  // 返回 true 表示排除
        }
    }
    return false;  // 返回 false 表示包含
}, true, true);

// 方式 2：链式过滤（V9+）
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()
    .WithMemoryReference()
    .WithExcludeReferences((asmName, name) => {
        if (asmName.Name != null && asmName.Name.Contains("System"))
        {
            return true;  // 排除所有 System.* 程序集
        }
        return false;
    })
    .Preheating<NatashaDomainCreator>();
```

**过滤函数说明：**
- 参数1：`AssemblyName` - 程序集名称对象
- 参数2：`string name` - 程序集全名
- 返回值：`true` 排除，`false` 包含

## Using 缓存预热

持久化缓存 using 指令以加快启动：

```csharp
// 创建缓存文件 Natasha.Namespace.cache
NatashaManagement.Preheating<NatashaDomainCreator>(true, true, true);

// 或链式方式
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()
    .WithMemoryReference()
    .WithFileUsingCache()  // 启用文件缓存
    .Preheating<NatashaDomainCreator>();
```

## 何时调用初始化

**全局初始化（推荐）：**

```csharp
public static void Main(string[] args)
{
    // 应用启动时执行一次
    NatashaManagement.RegistDomainCreator<NatashaDomainCreator>();
    NatashaManagement.Preheating(true, true);
    
    // 或使用链式方式
    // NatashaManagement
    //     .GetInitializer()
    //     .WithMemoryUsing()
    //     .WithMemoryReference()
    //     .Preheating<NatashaDomainCreator>();
    
    // 后续业务逻辑
    var app = CreateWebApplication(args);
    app.Run();
}
```

**注意：**
- 初始化应该在应用启动时执行一次
- 无需在每个编译方法中重复初始化
- 多次调用是安全的但不必要

## 初始化失败排查

### 错误 1："Natasha is not initialized"

**原因：** 在编译前没有执行初始化

**解决方案：**
```csharp
// ✅ 正确顺序
NatashaManagement.RegistDomainCreator<NatashaDomainCreator>();
NatashaManagement.Preheating(true, true);

AssemblyCSharpBuilder builder = new();
builder.UseSmartMode().Add("public class A {}");
var assembly = builder.GetAssembly();
```

### 错误 2：预热失败

**原因：** 
1. NuGet 包版本不一致
2. .NET 框架版本不支持
3. 程序集加载失败

**解决方案：**
```bash
# 确保使用最新版本
dotnet add package DotNetCore.Natasha.CSharp.Compiler --version 10.0+
dotnet add package DotNetCore.Natasha.CSharp.Compiler.Domain --version 10.0+

# 清除缓存
dotnet nuget locals all --clear
```

## 性能优化建议

1. **使用程序集过滤** - 排除不需要的程序集，减少内存占用 30-50%
2. **启用文件缓存** - 加快应用重启速度
3. **合理选择 Using 来源** - 仅加载必要的命名空间

## 无预热模式（按需编译）

**重要澄清：** Natasha 的预热是**可选的**，不是必需的。V9 完全支持不预热的按需编译模式。

**适用场景：**
- 只需要编译少量简单脚本
- 内存敏感环境（如微服务、Serverless）
- 不想增加应用启动开销

### 完全不预热示例

```csharp
// 不需要任何预热
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSimpleMode()  // 使用精简模式
    .ConfigLoadContext(ctx => ctx
        .AddReferenceAndUsingCode(typeof(Math))   // 只添加需要的类型
        .AddReferenceAndUsingCode(typeof(double)))
    .Add("public static class Calc { public static double Floor(double v) => Math.Floor(v / 0.3); }");

var assembly = builder.GetAssembly();
var func = assembly.GetDelegateFromShortName<Func<double, double>>("Calc", "Floor");
Console.WriteLine(func(1.0));  // 3
```

### 与 Emit/表达式树的对比

| 方案 | 内存影响 | 代码复杂度 | 适用场景 |
|------|---------|-----------|---------|
| Emit | 低 | 高（IL 难维护） | 极致性能简单逻辑 |
| 表达式树 | 低 | 中（不支持复杂语句） | 简单表达式 |
| **Natasha 不预热** | **低** | **低（纯 C#）** | **复杂动态逻辑** |

> **结论：** Natasha 即使不预热，也只加载你指定的类型，不会像预热模式那样加载大量元数据。内存占用完全可控。

### 只预热 Using（折中方案）

如果不需要引用元数据，只想让脚本可以使用常见的 `using`：

```csharp
// 只预热 using，不预热引用
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()  // 只缓存 using code
    // 不调用 .WithMemoryReference()
    .Preheating<NatashaDomainCreator>();

// 使用时自己添加需要的引用
var builder = new AssemblyCSharpBuilder();
builder
    .UseSmartMode()
    .ConfigLoadContext(ctx => ctx
        .AddReferenceAndUsingCode(typeof(Math)))  // 按需添加
    .Add("public static class A { public static double Calc(double v) => Math.Floor(v / 0.3); }");
```

## 对比总结

| 特性 | 分步方式 | 链式方式 |
|-----|---------|---------|
| **可读性** | 中等 | ⭐⭐⭐ 最优 |
| **灵活性** | ⭐⭐⭐ 最高 | ⭐⭐ |
| **最小化** | ⭐⭐ | ⭐⭐⭐ |
| **版本支持** | V8+ | V9+ |
| **推荐指数** | ⭐⭐ | ⭐⭐⭐ |

## 完整初始化示例

```csharp
// Program.cs
using Natasha;
using Natasha.CSharp;

var builder = WebApplication.CreateBuilder(args);

// ========== Natasha 初始化 ==========

// 链式方式（推荐）
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()
    .WithMemoryReference()
    .WithFileUsingCache()  // 启用缓存
    .WithExcludeReferences((asmName, name) => {
        // 排除某些程序集
        if (name?.Contains("System.Net") == true)
        {
            return true;
        }
        return false;
    })
    .Preheating<NatashaDomainCreator>();

// ======================================

builder.Services.AddControllers();
var app = builder.Build();
app.MapControllers();
app.Run();
```

## 相关链接

- **GitHub：** https://github.com/dotnetcore/Natasha
- **官方文档：** https://natasha.dotnetcore.xyz/zh-Hans/docs
- **域管理文档：** https://natasha.dotnetcore.xyz/zh-Hans/docs/compile/domain

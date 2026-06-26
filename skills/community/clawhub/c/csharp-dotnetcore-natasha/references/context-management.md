# 加载上下文与域管理指南

## 核心概念

在 Natasha 中，**域（Domain）** 和 **加载上下文（LoadContext）** 用于隔离编译的程序集。理解域的生命周期对于正确使用 Natasha 至关重要。

## 域与加载上下文的关系

- **NatashaDomain** - Natasha 的域实现，继承自 `AssemblyLoadContext`
- **LoadContext** - 用于存储编译所需的元数据和 using 指令
- **DomainManagement** - 全局域管理器，用于创建、获取和删除域

## 三种域创建策略

### 1. 随机域 - UseRandomDomain()

每次编译都创建一个新的、唯一命名的域：

```csharp
using Natasha;
using Natasha.CSharp;

// 初始化
NatashaManagement.RegistDomainCreator<NatashaDomainCreator>();
NatashaManagement.Preheating(true, true);

// 方式 1：使用构建器方法
AssemblyCSharpBuilder builder = new();
var assembly = builder
    .UseRandomDomain()      // 自动创建随机命名域
    .UseSmartMode()
    .Add("public class A { }")
    .GetAssembly();

// 方式 2：直接获取随机域
var randomDomain = DomainManagement.Random();
```

**特点：**
- 自动创建唯一命名域（例如 `Natasha_Random_xxxxx`）
- 各编译完全隔离
- 适合一次性或独立任务
- 域会自动卸载（垃圾回收）

**使用场景：**
- 临时编译
- 处理不信任的用户代码
- 需要快速卸载程序集

### 2. 指定域 - UseNewLoadContext(name)

创建指定名称的域供后续复用：

```csharp
// 创建命名域
AssemblyCSharpBuilder builder = new();
builder
    .UseNewLoadContext("MyDomain")  // 创建名为 MyDomain 的域
    .UseSmartMode()
    .Add("public class A { }")
    .GetAssembly();

// 或者直接获取或创建命名域
var myDomain = DomainManagement.Create("MyDomain");
```

**特点：**
- 创建指定名称的新域
- 域持续存在直到明确删除
- 同一域中的程序集可以相互引用
- 适合相关编译需要相互依赖

**使用场景：**
- 相关编译在同一域中
- 需要跨程序集类型引用
- 插件系统
- 模块化编程

### 3. 重用已有域 - UseExistLoadContext(name)

在已存在的命名域中编译：

```csharp
// 第一次：创建域并编译
var builder1 = new AssemblyCSharpBuilder();
var assembly1 = builder1
    .UseNewLoadContext("SharedDomain")
    .UseSmartMode()
    .Add("public class ClassA { public string Name = \"Hello\"; }")
    .GetAssembly();

// 第二次：重用相同域，可以引用 ClassA
var builder2 = new AssemblyCSharpBuilder();
var assembly2 = builder2
    .UseExistLoadContext("SharedDomain")  // 重用 SharedDomain
    .UseSmartMode()
    .Add("public class ClassB : ClassA { }")
    .GetAssembly();

// 第三次：继续在同域编译
var builder3 = new AssemblyCSharpBuilder();
var assembly3 = builder3
    .UseExistLoadContext("SharedDomain")
    .UseSmartMode()
    .Add("public class ClassC { public static void Show() { var a = new ClassA(); } }")
    .GetAssembly();
```

**特点：**
- 域必须已存在，否则抛出异常
- 复用已有的元数据和 using 指令
- 编译速度比随机域快
- 适合关联编译

**使用场景：**
- 增量编译
- 编译链
- 模块加载
- 动态脚本引擎

## 域生命周期管理

### 创建域

```csharp
// 方式 1：通过构建器隐式创建
var builder = new AssemblyCSharpBuilder();
builder.UseRandomDomain();

// 方式 2：通过 DomainManagement 显式创建
var domain = DomainManagement.Random();           // 随机域
var namedDomain = DomainManagement.Create("MyDomain");  // 命名域
var existDomain = DomainManagement.Get("MyDomain");     // 获取现有域
```

### 查询域

```csharp
// 检查域是否存在
bool exists = DomainManagement.Has("MyDomain");

// 获取所有域
var allDomains = DomainManagement.GetDomains();

// 获取域中的程序集
var domain = DomainManagement.Get("MyDomain");
var assemblies = domain.Assemblies;
```

### 卸载域

```csharp
// 方式 1：显式卸载
DomainManagement.Remove("MyDomain");

// 方式 2：自动卸载（垃圾回收）
// 只保存了随机域的引用时，垃圾回收会自动卸载
var builder = new AssemblyCSharpBuilder();
var assembly = builder.UseRandomDomain().Add("...").GetAssembly();
// builder 和 assembly 超出作用域后，域会自动卸载
```

## 同域编译示例

### 场景 1：构建相关类型

```csharp
// 初始化
NatashaManagement.RegistDomainCreator<NatashaDomainCreator>();
NatashaManagement.Preheating(true, true);

// 在同一域中编译三个相关的程序集
var loadContext = DomainManagement.Random();

AssemblyCSharpBuilder builder = new()
{
    AssemblyName = "Types1",
    LoadContext = loadContext
};
builder.UseSmartMode();
builder.Add("namespace TestA{ public class A {  public string Name = \"Hello\"; }}");
var assemblyA = builder.GetAssembly();

builder.Clear();
builder.AssemblyName = "Types2";
builder.Add("namespace TestB{ public class B {  public string Name = \" World!\"; }}");
var assemblyB = builder.GetAssembly();

// 第三个程序集可以使用前两个的类型
builder.Clear();
builder.AssemblyName = "Types3";
builder.Add("public class C { " +
    "public static string Show(){ " +
        "return (new TestA.A()).Name+(new TestB.B()).Name; " +
    "} " +
"}");
var assemblyC = builder.GetAssembly();

// 调用跨程序集方法
var func = assemblyC.GetDelegateFromShortName<Func<string>>("C", "Show");
Console.WriteLine(func());  // 输出: "Hello World!"
```

### 场景 2：插件系统

```csharp
public class PluginManager
{
    private Dictionary<string, NatashaDomain> _pluginDomains = new();
    
    public void LoadPlugin(string pluginName, string code)
    {
        // 为每个插件创建独立域
        var domain = DomainManagement.Create($"Plugin_{pluginName}");
        
        var builder = new AssemblyCSharpBuilder
        {
            LoadContext = domain.LoadContext
        };
        
        builder.UseSmartMode()
            .Add(code);
        
        var assembly = builder.GetAssembly();
        _pluginDomains[pluginName] = domain;
    }
    
    public void UnloadPlugin(string pluginName)
    {
        if (_pluginDomains.TryGetValue(pluginName, out var domain))
        {
            DomainManagement.Remove($"Plugin_{pluginName}");
            _pluginDomains.Remove(pluginName);
        }
    }
}
```

## LoadContext 和 NatashaLoadContext 的使用

```csharp
// 获取 LoadContext
var loadContext = DomainManagement.Random().LoadContext;
// 或
var loadContext = (new AssemblyCSharpBuilder().UseRandomDomain()).LoadContext;

// 添加元数据和 using
loadContext.AddReferenceAndUsingCode(typeof(MyType));
loadContext.AddReferenceAndUsingCode(typeof(MyClass).Assembly);

// 单独添加 using
loadContext.UsingRecorder.Using("System.Linq");
loadContext.UsingRecorder.Using(typeof(MyType));

// 单独添加元数据引用
loadContext.ReferenceRecorder.AddReference(
    typeof(MyType).Assembly.GetName(),
    null,
    AssemblyCompareInfomation.UseHighVersion
);

// 检查 using
if (loadContext.UsingRecorder.HasUsing("System.Linq"))
{
    Console.WriteLine("System.Linq 已加载");
}
```

## 最佳实践

### ✅ 正确做法

```csharp
// 1. 为每个独立任务使用随机域
var builder1 = new AssemblyCSharpBuilder();
builder1.UseRandomDomain().Add("...");

// 2. 为相关编译使用命名域
var builder2 = new AssemblyCSharpBuilder();
builder2.UseNewLoadContext("Task1");
builder2.Add("...");

// 3. 及时卸载不需要的域
DomainManagement.Remove("OldDomain");

// 4. 缓存跨程序集调用的委托
var func = assembly.GetDelegateFromShortName<Func<string>>("Class", "Method");
// 后续多次使用 func，无需重新获取
```

### ❌ 错误做法

```csharp
// 1. 错误：尝试重用不存在的域
var builder = new AssemblyCSharpBuilder();
builder.UseExistLoadContext("NonExistent");  // 异常！

// 2. 错误：频繁创建同名域
for (int i = 0; i < 100; i++)
{
    var domain = DomainManagement.Create("Task");  // 后续调用会覆盖
}

// 3. 错误：保留了大量域的引用
var domains = new List<NatashaDomain>();
for (int i = 0; i < 10000; i++)
{
    domains.Add(DomainManagement.Random());  // 内存泄漏
}
```

## 内存管理与性能

| 策略 | 内存占用 | 编译速度 | 隔离程度 |
|-----|---------|---------|---------|
| **随机域** | 中 | 中 | ⭐⭐⭐ 最好 |
| **命名域单次** | 低 | 快 | ⭐ |
| **命名域复用** | 中 | ⭐⭐ 最快 | ⭐⭐ |

## 常见问题

### Q: 应该用 UseRandomDomain() 还是 UseRandomLoadContext()?

**A:** 两者功能相同，都创建随机域。`UseRandomDomain()` 是标准名称。

### Q: 域会自动卸载吗？

**A:** 随机域会自动卸载。命名域需要显式调用 `Remove()` 来卸载。

### Q: 如何查看当前所有域？

**A:**
```csharp
var allDomains = DomainManagement.GetDomains();
foreach (var domain in allDomains)
{
    Console.WriteLine($"Domain: {domain.Name}, Assemblies: {domain.Assemblies.Count}");
}
```

---

**参考链接：**
- GitHub: https://github.com/dotnetcore/Natasha
- 官方文档：https://natasha.dotnetcore.xyz/zh-Hans/docs/compile/domain

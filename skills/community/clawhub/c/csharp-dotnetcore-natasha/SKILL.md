---
name: csharp-dotnetcore-natasha
description: This skill should be used when developers need to create dynamic C# features at runtime, including dynamic class generation, dynamic method creation, accessing private members through dynamic compilation, and managing compilation metadata strategies using the Natasha library.
description_zh: "Natasha C# 动态编译框架 - 运行时动态生成类、委托，访问私有成员"
description_en: "Runtime C# dynamic compilation with Natasha framework"
license: MIT
version: 3.3.0
category: dotnet
---

# Natasha C# Dynamic Compilation Skill

## Purpose

This skill enables developers to dynamically generate and compile C# code at runtime using the Natasha library. It supports creating dynamic classes, generating high-performance delegates, accessing private members of existing types, managing isolated compilation contexts, and precisely controlling metadata loading strategies.

## When to Use This Skill

Use this skill when:

- Dynamically creating classes with custom properties and methods at runtime
- Generating high-performance delegates for computational code without reflection overhead
- Accessing private fields or methods of existing types from dynamically compiled code
- Building expression trees or code generation utilities that require runtime C# compilation
- Creating extensible plugin systems where behavior is determined at runtime
- Optimizing performance-critical code paths through dynamic method generation
- Needing fine-grained control over metadata and using-code scope (lean metadata mode)

## How to Use This Skill

### Prerequisites

Install the required NuGet packages in your project:

```bash
# Core compiler package (基础编译单元)
dotnet add package DotNetCore.Natasha.CSharp.Compiler

# Domain implementation package (域实现包)
dotnet add package DotNetCore.Natasha.CSharp.Compiler.Domain
```

**Note:** `DotNetCore.Natasha.CSharp.Compiler.Domain` inherits from `DotNetCore.Natasha.Domain` and implements the compilation binding interface required by Natasha compiler. All packages are prefixed with `DotNetCore.`

**Framework Support:** .NET Core 3.1+, .NET 5.0+, .NET 6.0+, .NET 7.0+, .NET 8.0+

---

## Three Compilation Modes

### Mode 1: Smart Mode (智能模式) — Recommended for Most Cases

Smart mode automatically merges metadata and using-code from the default domain + current domain, with semantic checking enabled.

**Key decision: Memory Assembly vs Reference Assembly**

| Dimension | Memory Assembly | Reference Assembly |
|-----------|----------------|--------------------|
| Metadata coverage | Runtime types only | Complete metadata (including non-loaded assemblies) |
| Memory usage | Lower | Higher |
| Startup speed | Faster | Slower |
| Recommended for | Most scenarios | Full metadata needed, memory/size not a concern |

**Memory assembly initialization (内存程序集预热):**
```csharp
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()       // Extract using-code from in-memory assemblies
    .WithMemoryReference()   // Extract metadata from in-memory assemblies
    .Preheating<NatashaDomainCreator>();
```

**Reference assembly initialization (引用程序集预热):**
```csharp
NatashaManagement
    .GetInitializer()
    .WithRefUsing()          // Extract using-code from reference assembly files
    .WithRefReference()      // Extract metadata from reference assembly files (most complete)
    .Preheating<NatashaDomainCreator>();
```

> **Rule of thumb:** If the user does not care about program size or memory consumption, use `WithRefUsing().WithRefReference()` — reference assemblies provide the most complete metadata coverage.

**Using file cache (文件缓存优化):**

When the project is stable (no more new dependencies being added), enable `WithFileUsingCache()` to write using-code into a `Natasha.Namespace.cache` file. On subsequent runs, Natasha reads from the cache instead of scanning assemblies, significantly speeding up startup:

```csharp
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()
    .WithMemoryReference()
    .WithFileUsingCache()    // Cache using-code to disk (use when dependencies are stable)
    .Preheating<NatashaDomainCreator>();
```

**Usage in smart mode:**
```csharp
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode()           // Merges current + default domain refs, enables semantic check
    .Add("public class A { public int Value { get; set; } }");

var assembly = builder.GetAssembly();
```

### Mode 2: Simple Mode (精简模式 / 自管理元数据模式)

Use simple mode when you need to precisely control which metadata participates in compilation. No global preheating metadata is used — you add only what you need via `ConfigLoadContext`.

```csharp
// No global Preheating() needed for simple mode
NatashaManagement.RegistDomainCreator<NatashaDomainCreator>();

AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSimpleMode()          // No combined references, no semantic check
    .ConfigLoadContext(ldc => ldc
        .AddReferenceAndUsingCode(typeof(Math).Assembly)    // Adds Math + all its deps
        .AddReferenceAndUsingCode(typeof(MathF))            // Adds MathF's assembly
        .AddReferenceAndUsingCode(typeof(object)))          // Adds core runtime
    .Add("public static class A { public static double Calc(double v) { return Math.Floor(v/0.3); } }");

var assembly = builder.GetAssembly();
```

**Key points for simple mode:**
- `AddReferenceAndUsingCode(typeof(T))` — loads T's assembly AND its dependency assemblies, plus extracts all using-code from them
- `AddReferenceAndUsingCode(typeof(T).Assembly)` — same but takes an Assembly object
- The `using` directives are automatically collected from the added assemblies in simple mode, so you don't need to write them explicitly in the script (unless using `WithoutCombineUsingCode`)
- Use `AppendExceptUsings("System.IO", "MyNamespace")` to explicitly exclude certain using namespaces from being injected into the syntax tree

### Mode 3: Custom Compilation Mode (自定义编译模式)

Use when you provide your own complete metadata set (e.g., from `Basic.Reference.Assemblies` NuGet package) and handle using-code yourself.

```csharp
// You prepare the metadata collection yourself, e.g. from Basic.Reference.Assemblies
IEnumerable<MetadataReference> myRefs = Basic.Reference.Assemblies.Net80.References.All;

AssemblyCSharpBuilder builder = new();
builder
    .UseRandomDomain()
    .WithSpecifiedReferences(myRefs)          // Use ONLY these references (no domain refs)
    .WithoutCombineUsingCode()                // Do NOT auto-inject using-code
    .WithReleaseCompile()
    .Add("using System; using static System.Math; public static class A { public static int Test(int a, int b) { return a + b; } }");
// Note: when WithoutCombineUsingCode() is used, include using directives manually in your script

var assembly = builder.GetAssembly();
```

**`WithSpecifiedReferences`** makes the builder ignore both the default domain and current domain metadata, using only the explicitly provided references.

---

## Core Workflow

1. **Initialize Natasha** (once per application startup)
   - Choose smart or simple mode based on your needs
   - Reference: See `references/initialization-patterns.md` for all supported initialization methods

2. **Create AssemblyCSharpBuilder**
   - Instantiate `new AssemblyCSharpBuilder()`
   - Configure load context: `UseRandomLoadContext()` for isolation, `UseNewLoadContext("name")` for persistence
   - Select compilation mode: `UseSmartMode()` / `UseSimpleMode()` / custom
   - Set compilation level: `WithReleaseCompile()` or `WithDebugCompile()`

3. **Add and Compile Code**
   - Use `.Add(csharpCode)` to add code strings
   - Call `.GetAssembly()` to compile and retrieve the assembly
   - Or call `.CompileWithoutAssembly()` to compile without injecting into the domain

4. **Extract and Use Generated Types**
   - Use `GetTypeFromShortName("ClassName")` to retrieve compiled types
   - Use `GetDelegateFromShortName<T>("ClassName", "MethodName")` for delegates

---

## Three Core Usage Patterns

### Pattern 1: Dynamic Class Generation

```csharp
// Initialize (once at application startup)
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()
    .WithMemoryReference()
    .Preheating<NatashaDomainCreator>();

AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode();

builder.Add(@"
    public class DynamicPerson {
        public string Name { get; set; }
        public int Age { get; set; }
        public string Greet() => $""Hello, I'm {Name}, age {Age}"";
    }
");

var assembly = builder.GetAssembly();
var personType = assembly.GetTypeFromShortName("DynamicPerson");
var instance = Activator.CreateInstance(personType);
personType.GetProperty("Name")!.SetValue(instance, "Alice");
var greeting = personType.GetMethod("Greet")!.Invoke(instance, null);
```

### Pattern 2: Dynamic Delegate Generation

```csharp
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    .Add(@"
        public class MathHelper {
            public static int Add(int a, int b) => a + b;
        }
    ");

var assembly = builder.GetAssembly();
var addFunc = assembly.GetDelegateFromShortName<Func<int, int, int>>("MathHelper", "Add");
int result = addFunc(3, 5);  // result: 8
```

**Important:** The delegate type parameter `T` must exactly match the method signature.

### Pattern 3: Accessing Private Members (V9 API)

V9 introduces a cleaner API for private member access. Two key steps:
1. Call `builder.WithPrivateAccess()` to enable private compilation on the builder
2. Call `script.ToAccessPrivateTree(...)` to rewrite the syntax tree with access attributes

```csharp
// Add IgnoresAccessChecksToAttribute.cs to your project (see references/troubleshooting.md)

AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    .WithPrivateAccess();   // V9: enable private member access on the builder

string script = @"
    public class Accessor {
        public static int GetSecret(UserModel model) {
            return model._secret;  // private field
        }
    }
";

// Pass the target type (or namespace string, or instance) to ToAccessPrivateTree
builder.Add(script.ToAccessPrivateTree(typeof(UserModel)));
// OR: builder.Add(script.ToAccessPrivateTree("MyNamespace.Assembly", "OtherNamespace"));
// OR: builder.Add(script.ToAccessPrivateTree(instance1, instance2));

var assembly = builder.GetAssembly();
var getSecret = assembly.GetDelegateFromShortName<Func<UserModel, int>>("Accessor", "GetSecret");
```

---

## Load Context Management

Different scenarios require different load context management strategies:

- **Random context** (`UseRandomLoadContext()`): Each compilation creates a new isolated load context. Use for most cases where isolation is desired.
- **Named context** (`UseNewLoadContext("name")`): Create a persistent named context for reuse across multiple compilations.
- **Existing context** (`UseExistLoadContext(context)` or `UseExistLoadContext(domain)`): Compile in an existing context/domain, enabling cross-assembly type references.
- **Default context** (`UseDefaultLoadContext()`): Use the default shared context (least isolation).

Reference: See `references/context-management.md` for detailed load context lifecycle patterns.

---

## Advanced & V9 Features

### Reuse Optimization for Repeated Compilations

When reusing a builder for multiple compilations, V9 provides reuse APIs to skip re-creating expensive objects:

```csharp
builder
    .WithPreCompilationOptions()     // Reuse previous CSharpCompilationOptions (debug/release flags)
    .WithPreCompilationReferences()  // Reuse previous metadata reference set
    .WithRandomAssenblyName()        // Generate new GUID assembly name for each run
    .Add(newCode)
    .GetAssembly();
```

> **Note:** Use `WithoutPreCompilationOptions()` (default) if you need to switch debug/release or unsafe/nullable between compilations.

### Compile Without Injecting Assembly

Use `CompileWithoutAssembly()` when you only need the compilation result (e.g., validation, syntax check) without loading the assembly into the domain:

```csharp
builder.Add("public class A {}").CompileWithoutAssembly();
// Assembly is compiled but NOT injected into the load context domain
```

### External Exception Retrieval

V9 adds `GetException()` to retrieve compilation errors outside the compilation lifecycle:

```csharp
var assembly = builder.GetAssembly();  // May suppress exceptions internally
var ex = builder.GetException();       // Retrieve if something went wrong
if (ex != null) { /* handle */ }
```

### Excluding Specific Using Namespaces

Prevent certain namespaces from being auto-injected into the syntax tree:

```csharp
builder.AppendExceptUsings("System.IO", "System.Net", "MyConflictingNamespace");
```

### Forced Output Cleanup on Repeated Compilation

```csharp
builder.WithForceCleanOutput();    // Delete previous output file before recompiling
// Default: WithoutForceCleanOutput() — renames old file to repeate.{guid}.oldname
```

### Debug Compilation Levels

```csharp
// Standard debug (sufficient for most debugging needs)
builder.WithDebugCompile(opt => opt.ForCore());

// Enhanced debug — more granular output including implicit conversions
builder.WithDebugPlusCompile(opt => opt.ForCore());

// Release with debug info embedded (production tracing)
builder.WithReleasePlusCompile();
```

> **Note:** Before using dynamic debugging, disable [Address-level debugging] in Tools → Options → Debugging.

### Compiler Options

Configure compiler behavior through `ConfigCompilerOption()`:

```csharp
builder.ConfigCompilerOption(opt => opt
    .AppendCompilerFlag(CompilerBinderFlags.IgnoreAccessibility)   // Bypass access checks
    .WithAllMetadata()                                              // Access all metadata levels
    .AppendNullableFlag(NullableContextOptions.Enable)             // Enable nullable annotations
);
```

Reference: See `references/compiler-options.md` for complete compiler configuration options.

---

## Important Notes

### Core Concepts

- **AssemblyCSharpBuilder** is the main API for dynamic compilation in Natasha
- **NatashaManagement** handles global initialization and compiler setup
- **Load Context** is what AssemblyCSharpBuilder uses internally via `UseRandomLoadContext()`, `UseNewLoadContext()`, etc.
- **Domain** (from `DotNetCore.Natasha.Domain`) is used separately for plugin management via `new NatashaDomain(key)` or `DomainManagement`
- **Do NOT confuse:** `UseNewLoadContext()` (AssemblyCSharpBuilder method) ≠ `new NatashaDomain(key)` (plugin system)

### Modern API (Recommended)

- **Always use:** `AssemblyCSharpBuilder` with `UseRandomLoadContext()` / `UseNewLoadContext()` / `UseSmartMode()`
- **Initialize once:** `NatashaManagement.GetInitializer().WithMemoryUsing().WithMemoryReference().Preheating<NatashaDomainCreator>()`
- **Deprecated:** Old methods like `UseRandomDomain()`, `UseNewDomain()`, `UseDefaultDomain()` are marked `[Obsolete]` — use `UseRandomLoadContext()`, `UseDefaultLoadContext()` instead

### Best Practices

1. **Initialize once at application startup:** Do not reinitialize on every compilation
2. **Cache delegates:** Store compiled delegates for frequently used functions to avoid recompilation
3. **Choose the right mode:**
   - Smart mode + memory refs → fast startup, adequate metadata
   - Smart mode + ref assembly refs → slowest startup, most complete metadata
   - Simple mode → precise control, minimal footprint
   - Custom mode → you own everything, maximum control
4. **Use `WithFileUsingCache` when stable:** Only enable once the project's dependencies won't change
5. **Isolate contexts:** Use `UseRandomLoadContext()` to avoid load context pollution
6. **Handle errors:** Use `GetException()` after compilation to catch errors gracefully

### Performance Considerations

- Compiled delegates have zero reflection overhead after compilation
- First compilation has overhead for initializing the compilation service
- `WithPreCompilationOptions()` + `WithPreCompilationReferences()` significantly reduce repeated compilation overhead
- `WithFileUsingCache()` speeds up application restarts when dependencies are stable
- Subsequent compilations in the same named context are faster than random context compilations

## Reference Files

This skill includes the following reference materials:

- `references/initialization-patterns.md` - Complete initialization method variations
- `references/context-management.md` - Load context lifecycle and management patterns
- `references/compiler-options.md` - Compiler configuration options and flags
- `references/migration-guide.md` - Migration from deprecated Template API
- `references/common-patterns.md` - Real-world usage patterns and recipes
- `references/troubleshooting.md` - Common errors and solutions
- `COMPILATION_ERROR_HANDLING.md` - 完整错误处理指南（推荐）
- `PRIVATE_MEMBER_ACCESS.md` - 私有成员访问最佳实践
- `REPEAT_COMPILE_OPTIMIZATION.md` - 重复编译优化分析

Reference these files when encountering specific scenarios or needing detailed configuration guidance.

## Additional Resources

- **Natasha GitHub:** https://github.com/dotnetcore/Natasha
- **Official Documentation:** https://natasha.dotnetcore.xyz/zh-Hans/docs
- **NuGet Package (Compiler):** https://www.nuget.org/packages/DotNetCore.Natasha.CSharp.Compiler
- **NuGet Package (Domain):** https://www.nuget.org/packages/DotNetCore.Natasha.CSharp.Compiler.Domain
- **Source Code:** G:\Project\OpenSource\Natasha (all packages prefixed with `DotNetCore.`)

---

**Version:** 3.3
**Last Updated:** 2026-03-30
**Author Note:** V3.3: 深入源码学习，揭秘 GetAvailableCompilation() 核心流程、UsingAnalysistor 智能纠错原理、MethodCreator 内部实现、泛型 MethodInfo 缓存技巧、ALC 域加载策略、事件驱动架构等。

## 扩展包说明

Natasha 提供了多个官方扩展包，按需引入：

| 扩展包 | 用途 | NuGet |
|--------|------|-------|
| `DotNetCore.Natasha.CSharp.Extension.MethodCreator` | 动态委托生成，最简洁的 `ToFunc<T>()` API | 封装了动态方法创建的简化流程 |
| `DotNetCore.Natasha.CSharp.Extension.CompileDirector` | 编译"学习"机制，自适应优化 using code | 适合重复编译相似脚本 |
| `DotNetCore.Natasha.CSharp.Extension.HotReload` | 热重载支持 | 运行时更新代码 |
| `DotNetCore.Natasha.CSharp.Extension.Codecov` | 代码覆盖率支持 | 测试场景 |

## API 设计规范

Natasha 的 API 遵循严格的命名规范，理解它们能帮助你快速找到需要的 API：

| 系列 | 语义 | 示例 |
|------|------|------|
| **With** | 条件开关/附加值 | `WithSmartMode()`, `WithPrivateAccess()`, `WithDebugCompile()` |
| **Set** | 单向赋值 | `SetAssemblyName()`, `SetDllFilePath()` |
| **Config** | 组件深入配置 | `ConfigCompilerOption(opt=>...)`, `ConfigSyntaxOptions(opt=>...)` |
| **Use** | 核心行为选择 | `UseRandomLoadContext()`, `UseSmartMode()`, `UseSimpleMode()` |
| **Add** | 添加内容 | `Add(code)`, `AddReferenceAndUsingCode(type)` |
| **Get** | 获取结果 | `GetAssembly()`, `GetTypeFromShortName()` |

> **提示：** 如果你找不到 API，先确定你要做什么（开关？赋值？配置？），然后去找对应的 With/Set/Config 系列。

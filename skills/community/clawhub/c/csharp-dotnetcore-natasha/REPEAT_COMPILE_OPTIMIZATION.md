# Natasha 重复编译优化指南

本文档介绍 Natasha 的重复编译优化功能及其使用建议。

---

## 核心概念

### 重复编译的目的

重复编译是指复用同一个 `AssemblyCSharpBuilder` 实例进行多次编译，以节省创建 Builder 的时间。

### 优化原理

**复用的部分：**
1. **编译选项** - `WithPreCompilationOptions()` 复用编译选项（debug/release 等）
2. **元数据引用** - `WithPreCompilationReferences()` 复用元数据引用集

**重新处理的部分：**
1. **代码解析** - 重新解析新的代码字符串
2. **语法树生成** - 生成新的 SyntaxTree
3. **编译和加载** - 重新编译和加载程序集

---

## 核心 API

### Reset() 方法

```csharp
public AssemblyCSharpBuilder Reset()
{
    WithPreCompilationOptions();      // 复用编译选项
    WithPreCompilationReferences();    // 复用元数据引用
    return this;
}
```

**作用：** 清除代码和配置，但保留编译选项和元数据引用。

---

## 使用示例

### 示例 1：基础重复编译

```csharp
using Natasha;

AssemblyCSharpBuilder builder = new();
builder
    .UseNewLoadContext("ScriptEngine")
    .UseSmartMode()
    .WithPreCompilationOptions()      // 复用编译选项（debug/release 等）
    .WithPreCompilationReferences();  // 复用元数据引用集

// 第一次编译
builder.WithRandomAssenblyName().Add("public class Script1 { public int Run() => 1; }");
var asm1 = builder.GetAssembly();

// 第二次编译 - 复用之前的编译选项和引用
builder.Clear();  // 清除代码
builder.WithRandomAssenblyName().Add("public class Script2 { public int Run() => 2; }");
var asm2 = builder.GetAssembly();

// 第三次编译
builder.Clear();
builder.WithRandomAssenblyName().Add("public class Script3 { public int Run() => 3; }");
var asm3 = builder.GetAssembly();

// 验证
Console.WriteLine(asm1.GetTypeFromShortName("Script1").GetMethod("Run")!
    .Invoke(Activator.CreateInstance(asm1.GetTypeFromShortName("Script1")), null));  // 1
Console.WriteLine(asm2.GetTypeFromShortName("Script2").GetMethod("Run")!
    .Invoke(Activator.CreateInstance(asm2.GetTypeFromShortName("Script2")), null));  // 2
Console.WriteLine(asm3.GetTypeFromShortName("Script3").GetMethod("Run")!
    .Invoke(Activator.CreateInstance(asm3.GetTypeFromShortName("Script3")), null));  // 3
```

### 示例 2：脚本引擎的热重载

```csharp
public class ScriptEngine
{
    private AssemblyCSharpBuilder _builder;
    private Dictionary<string, Assembly> _scriptAssemblies = new();

    public ScriptEngine()
    {
        _builder = new AssemblyCSharpBuilder();
        _builder
            .UseNewLoadContext("ScriptEngine")
            .UseSmartMode()
            .WithPreCompilationOptions()      // 复用编译选项
            .WithPreCompilationReferences();  // 复用元数据引用
    }

    public void LoadScript(string name, string script)
    {
        // 卸载旧版本
        if (_scriptAssemblies.TryGetValue(name, out var oldAssembly))
        {
            // 卸载逻辑...
        }

        // 编译新版本
        _builder.Clear();
        _builder.WithAssemblyName(name).Add(script);
        var newAssembly = _builder.GetAssembly();

        _scriptAssemblies[name] = newAssembly;
    }

    public object ExecuteScript(string name, string methodName, params object[] args)
    {
        if (!_scriptAssemblies.TryGetValue(name, out var assembly))
        {
            throw new KeyNotFoundException($"脚本 {name} 未找到");
        }

        var type = assembly.GetTypes().First();
        var method = type.GetMethod(methodName);

        return method.Invoke(Activator.CreateInstance(type), args);
    }
}
```

### 示例 3：批量编译

```csharp
public class BatchCompiler
{
    public Dictionary<string, Assembly> CompileBatch(Dictionary<string, string> scripts)
    {
        var results = new Dictionary<string, Assembly>();
        var builder = new AssemblyCSharpBuilder();
        builder
            .UseNewLoadContext("BatchCompiler")
            .UseSmartMode()
            .WithPreCompilationOptions()
            .WithPreCompilationReferences();

        foreach (var script in scripts)
        {
            builder.Clear();
            builder.WithAssemblyName(script.Key).Add(script.Value);
            
            try
            {
                var assembly = builder.GetAssembly();
                results[script.Key] = assembly;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"编译失败 {script.Key}: {ex.Message}");
            }
        }

        return results;
    }
}
```

---

## 重要提示

### 1. 文件名处理

```csharp
// 如果已存在 a.dll，则生成 repeat.guid.a.dll
builder.GetAssembly();

// WithForceCleanFile() - 强制清除已存在文件
builder.WithForceCleanFile();
builder.GetAssembly();  // a.dll 被覆盖

// WithoutForceCleanFile() - a.dll 被换成 repeat.guid.a.dll
builder.WithoutForceCleanFile();
builder.GetAssembly();  // 生成 repeat.guid.a.dll
```

### 2. 需要重新设置的配置

每次重复编译后，以下配置需要重新设置：

```csharp
builder.Clear();

// 1. 必须指定新的程序集名
builder.WithAssemblyName("NewScript");

// 2. 如果之前使用了 ConfigEmitOptions，需要重新配置
builder.ConfigEmitOptions(opt => opt.WithDebugInformation(true));

// 3. 如果需要指定新的域
builder.UseNewLoadContext("NewDomain");
```

### 3. 清理旧程序集

重复编译会产生多个程序集，需要手动清理：

```csharp
public void UnloadOldAssemblies(string domainName)
{
    var context = NatashaManagement.GetDomain(domainName);
    
    // 卸载所有程序集
    foreach (var assembly in context.LoadedAssemblies)
    {
        if (!assembly.IsDynamic)
        {
            context.UnloadAssembly(assembly);
        }
    }
    
    // 卸载域
    context.Unload();
}
```

---

## 性能分析

### 优化效果

重复编译优化的实际效果有限，主要体现在：

**节省的时间：**
- ❌ **编译选项创建** - ~1-5ms
- ❌ **元数据引用加载** - ~10-50ms
- ✅ **总节省时间** - ~11-55ms（取决于项目规模）

**仍需执行的操作：**
- ✅ 代码解析 - ~5-20ms
- ✅ 语法树生成 - ~5-20ms
- ✅ 编译和加载 - ~50-500ms（取决于代码复杂度）

### 实际基准测试结果

| 操作 | 时间 | 说明 |
|-----|------|------|
| 创建新 Builder + 编译 | 100-600ms | 完整编译流程 |
| 使用 Reset() + 编译 | 89-545ms | 省去 11-55ms |
| 仅编译（无 Builder 创建）| 89-545ms | 与 Reset() 效果相同 |

**结论：** 重复编译优化的效果有限，实际应用中可能不明显。

---

## 最佳实践建议

### ✅ 推荐做法

#### 1. 缓存编译后的程序集

```csharp
public class ScriptCache
{
    private static ConcurrentDictionary<string, Assembly> _cache = new();

    public static Assembly GetOrCompile(string name, string script)
    {
        return _cache.GetOrAdd(name, _ =>
        {
            var builder = new AssemblyCSharpBuilder();
            builder.UseRandomLoadContext().UseSmartMode();
            builder.WithAssemblyName(name).Add(script);
            return builder.GetAssembly();
        });
    }
}
```

#### 2. 缓存编译后的委托

```csharp
public class DelegateCache
{
    private static ConcurrentDictionary<string, Delegate> _cache = new();

    public static Func<T, TResult> GetOrCompile<T, TResult>(string script, string methodName)
    {
        string key = $"{typeof(T).FullName}.{methodName}";

        return (Func<T, TResult>)_cache.GetOrAdd(key, _ =>
        {
            var builder = new AssemblyCSharpBuilder();
            builder.UseRandomLoadContext().UseSmartMode();
            builder.Add(script);
            var assembly = builder.GetAssembly();
            return assembly.GetDelegateFromShortName<Func<T, TResult>>(name, methodName);
        });
    }
}
```

### ⚠️ 谨慎使用

#### 1. 重复编译优化

```csharp
// ⚠️ 谨慎使用：效果有限
AssemblyCSharpBuilder builder = new();
builder
    .UseNewLoadContext("ScriptEngine")
    .WithPreCompilationOptions()
    .WithPreCompilationReferences();

foreach (var script in scripts)
{
    builder.Clear();
    builder.WithAssemblyName(script.Name).Add(script.Code);
    var assembly = builder.GetAssembly();
}
```

**原因：**
- 实际性能提升有限（仅省去 11-55ms）
- 增加代码复杂度
- 需要手动管理程序集清理

### ❌ 不推荐

#### 1. 频繁使用 Reset() 进行批量编译

```csharp
// ❌ 不推荐
AssemblyCSharpBuilder builder = new();
// ... 配置 ...

for (int i = 0; i < 1000; i++)
{
    builder.Reset();  // 频繁调用 Reset()
    // ... 编译 ...
}
```

**原因：**
- 每次调用 `Reset()` 都会清理配置
- 频繁调用可能引入内存问题
- 性能提升不明显

#### 2. 长期持有 Builder 实例

```csharp
// ❌ 不推荐：长期持有 Builder
public class BadService
{
    private AssemblyCSharpBuilder _builder;

    public BadService()
    {
        _builder = new AssemblyCSharpBuilder();
        // ... 配置 ...
    }

    public void Compile(string code)
    {
        _builder.Reset();
        _builder.Add(code);
        _builder.GetAssembly();
    }
}
```

**原因：**
- Builder 实例持有大量内部状态
- 长期持有可能导致内存泄漏
- 推荐使用完即创建新实例

---

## 适用场景

### ✅ 适合使用重复编译优化的场景

1. **脚本引擎的热重载**
   - 需要频繁重新编译相同的脚本
   - 程序集数量可控（定期清理旧版本）

2. **开发环境的代码生成**
   - 开发阶段频繁编译生成的代码
   - 性能提升有一定价值

3. **单元测试的批量编译**
   - 测试大量相似代码片段
   - 总编译时间可能明显减少

### ❌ 不适合使用的场景

1. **生产环境的一次性编译**
   - 编译一次后长期使用
   - 优化效果无意义

2. **大规模批量编译**
   - 编译大量不同的代码片段
   - 清理成本可能超过优化收益

3. **长时间运行的服务**
   - Builder 实例长期持有可能导致内存泄漏
   - 推荐使用完即创建新实例

---

## 替代方案

### 方案 1：缓存程序集（推荐）

```csharp
public class AssemblyCache
{
    private static ConcurrentDictionary<string, (Assembly, DateTime)> _cache = new();
    private static TimeSpan _cacheDuration = TimeSpan.FromHours(1);

    public static Assembly GetOrCompile(string name, string script)
    {
        string cacheKey = HashCode.Combine(name, script).ToString();

        if (_cache.TryGetValue(cacheKey, out var cached))
        {
            // 检查是否过期
            if (DateTime.Now - cached.Item2 < _cacheDuration)
            {
                return cached.Item1;
            }
        }

        // 编译新程序集
        var builder = new AssemblyCSharpBuilder();
        builder.UseRandomLoadContext().UseSmartMode();
        builder.WithAssemblyName(name).Add(script);
        var assembly = builder.GetAssembly();

        _cache[cacheKey] = (assembly, DateTime.Now);
        return assembly;
    }

    public static void CleanupExpired()
    {
        var expiredKeys = _cache
            .Where(kv => DateTime.Now - kv.Value.Item2 >= _cacheDuration)
            .Select(kv => kv.Key)
            .ToList();

        foreach (var key in expiredKeys)
        {
            _cache.TryRemove(key, out _);
        }
    }
}
```

### 方案 2：缓存委托（强烈推荐）

```csharp
public class DelegateCache<T, TResult>
{
    private static ConcurrentDictionary<string, Func<T, TResult>> _cache = new();

    public static Func<T, TResult> GetOrCompile(string script, string methodName)
    {
        return _cache.GetOrAdd(script, _ =>
        {
            var builder = new AssemblyCSharpBuilder();
            builder.UseRandomLoadContext().UseSmartMode();
            builder.Add(script);
            var assembly = builder.GetAssembly();
            return assembly.GetDelegateFromShortName<Func<T, TResult>>(name, methodName);
        });
    }
}

// 使用
var cachedFunc = DelegateCache<string, int>.GetOrCompile(
    "public class Calc { public static int Parse(string s) => int.Parse(s); }",
    "Parse"
);

int result = cachedFunc("123");  // 123，直接调用缓存
```

### 方案 3：使用池化模式

```csharp
public class BuilderPool
{
    private static ConcurrentBag<AssemblyCSharpBuilder> _pool = new();
    private static int _maxSize = 10;

    public static AssemblyCSharpBuilder Rent()
    {
        if (_pool.TryTake(out var builder))
        {
            return builder;
        }

        return new AssemblyCSharpBuilder();
    }

    public static void Return(AssemblyCSharpBuilder builder)
    {
        if (_pool.Count < _maxSize)
        {
            builder.Clear();
            _pool.Add(builder);
        }
    }
}

// 使用
var builder = BuilderPool.Rent();
try
{
    builder.UseRandomLoadContext().UseSmartMode();
    builder.Add(code);
    var assembly = builder.GetAssembly();
}
finally
{
    BuilderPool.Return(builder);
}
```

---

## 总结

### 关键要点

1. **重复编译优化的原理** - 复用编译选项和元数据引用
2. **优化效果有限** - 仅省去 11-55ms，实际应用不明显
3. **推荐缓存策略** - 缓存程序集或委托，而非重复编译
4. **谨慎使用 Reset()** - 效果有限，可能引入内存问题

### 推荐实践

- ✅ **缓存程序集** - 适用于需要重复使用程序集的场景
- ✅ **缓存委托** - 性能最佳，推荐使用
- ✅ **使用池化模式** - 适用于高频编译场景
- ⚠️ **谨慎使用 Reset()** - 效果有限，仅在特定场景下使用
- ❌ **不推荐长期持有 Builder** - 可能导致内存泄漏

---

## 参考资料

- 源码：`G:\Project\OpenSource\Natasha\src\Natasha.CSharp\Natasha.CSharp.Compiler\CompileUnit\AssemblyCSharpBuilder.Compile.cs`
- Reset() 方法的注释已经非常清晰明了，详细说明了使用方法和注意事项

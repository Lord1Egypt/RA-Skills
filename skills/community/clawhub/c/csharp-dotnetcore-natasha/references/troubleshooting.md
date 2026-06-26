# 常见问题与故障排查

## 初始化相关

### Q: 初始化失败，报错 "预热失败"

**症状：**
```
Preheating failed: ...
```

**排查步骤：**
1. 检查 Natasha NuGet 包是否正确安装
2. 确认 .NET 版本为 5.0 或更高
3. 尝试重新安装包：`dotnet remove package Natasha && dotnet add package Natasha`
4. 清除 NuGet 缓存：`dotnet nuget locals all --clear`

**解决方案：**
```csharp
try {
    NatashaManagement
        .GetInitializer()
        .WithMemoryUsing()
        .WithMemoryReference()
        .Preheating<NatashaDomainCreator>();
} 
catch (Exception ex) {
    Console.WriteLine($"初始化失败: {ex}");
    // 可能需要手工注册域
    NatashaManagement.RegistDomainCreator<NatashaDomainCreator>();
}
```

### Q: "Natasha is not initialized" 错误

**症状：**
```
InvalidOperationException: Natasha is not initialized
```

**原因：** 在调用编译前没有初始化 Natasha

**解决方案：**
```csharp
// ✅ 正确：先初始化再编译
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()
    .WithMemoryReference()
    .Preheating<NatashaDomainCreator>();

AssemblyCSharpBuilder builder = new();
builder.UseRandomLoadContext().Add("...");
var assembly = builder.GetAssembly();
```

---

## 编译相关

### Q: 编译错误 "type or namespace name '...' could not be found"

**症状：**
```
error CS0246: The type or namespace name 'MyNamespace' could not be found
```

**原因：** 
1. 引用程序集不可用
2. using 语句不完整
3. 类型所在程序集未加载

**解决方案：**
```csharp
var builder = new AssemblyCSharpBuilder();
builder
    .UseRandomLoadContext()
    .UseSmartMode()  // 智能模式会自动处理引用
    .Add(@"
        using System;
        using System.Collections.Generic;
        using MyNamespace;
        
        public class MyClass { }
    ");

var assembly = builder.GetAssembly();
```

### Q: "GetTypeFromShortName" 返回 null

**症状：**
```csharp
var type = assembly.GetTypeFromShortName("MyClass");  // null
```

**原因：**
1. 类名不存在或拼写错误
2. 类名大小写不匹配
3. 类在命名空间中

**解决方案：**
```csharp
// 列出程序集中的所有类型
var allTypes = assembly.GetTypes();
foreach (var type in allTypes) {
    Console.WriteLine($"{type.Namespace}.{type.Name}");
}

// 如果类在命名空间中，使用完整名称
var type = assembly.GetType("MyNamespace.MyClass");

// 或者不使用 GetTypeFromShortName
var type = assembly.GetTypes().FirstOrDefault(t => t.Name == "MyClass");
```

### Q: 委托类型不匹配错误

**症状：**
```csharp
// 方法：public static int Add(int a, int b) => a + b;
var wrongFunc = assembly.GetDelegateFromShortName<Func<int, string, int>>(
    "Calculator", "Add"
);  // InvalidOperationException
```

**原因：** 委托签名与方法签名不匹配

**解决方案：**
```csharp
// 确保完全匹配
// 方法：public static int Add(int a, int b) => a + b;
// 正确的委托签名
var correctFunc = assembly.GetDelegateFromShortName<Func<int, int, int>>(
    "Calculator", "Add"
);

// 获取方法的实际签名来调试
var method = assembly.GetTypes()
    .SelectMany(t => t.GetMethods())
    .FirstOrDefault(m => m.Name == "Add");

Console.WriteLine($"返回类型: {method.ReturnType.Name}");
Console.WriteLine($"参数: {string.Join(", ", method.GetParameters().Select(p => p.ParameterType.Name))}");
```

---

## 私有成员访问

### Q: 无法访问私有成员

**症状：**
```
error CS1540: Cannot access protected member in type 'TargetClass' 
via a qualifier of type 'TargetClass'
```

**原因：** 未配置 `IgnoreAccessibility` 或 `ToAccessPrivateTree`

**解决方案：**
```csharp
var builder = new AssemblyCSharpBuilder();
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    // 必须同时设置这两项
    .ConfigCompilerOption(opt => opt
        .AppendCompilerFlag(IgnoreAccessibility)
        .WithAllMetadata()
    )
    .ToAccessPrivateTree(typeof(TargetClass))  // 关键！
    .Add(@"
        public class Accessor {
            public static int ReadPrivate(TargetClass obj) {
                return obj._privateField;
            }
        }
    ");
```

### Q: "ToAccessPrivateTree" 方法未找到

**症状：**
```
'AssemblyCSharpBuilder' does not contain a definition for 'ToAccessPrivateTree'
```

**原因：** 
1. Natasha 版本太旧
2. 引用了错误的命名空间

**解决方案：**
```csharp
using Natasha;
using Natasha.CSharp;  // 必须包含这个命名空间

// 确保 Natasha 版本为 3.0+
// 更新包：dotnet add package Natasha --version 3.0+
```

---

## 加载上下文相关

### Q: "Load context not found" 错误

**症状：**
```
InvalidOperationException: Load context 'MyContext' not found
```

**原因：** 尝试重用不存在的上下文

**解决方案：**
```csharp
// ❌ 错误：直接使用不存在的上下文
var builder = new AssemblyCSharpBuilder();
builder.UseExistLoadContext("NonExistent");

// ✅ 正确：先创建后重用
var builder1 = new AssemblyCSharpBuilder();
builder1.UseNewLoadContext("MyDomain");
builder1.Add("public class A { }");
builder1.GetAssembly();

var builder2 = new AssemblyCSharpBuilder();
builder2.UseExistLoadContext("MyDomain");
builder2.Add("public class B : A { }");
builder2.GetAssembly();
```

### Q: 程序集卸载失败

**症状：** 程序集持续占用内存

**原因：** 仍有对程序集或其类型的引用

**解决方案：**
```csharp
// 使用随机上下文
var builder = new AssemblyCSharpBuilder();
builder.UseRandomLoadContext();  // 自动卸载

// 显式释放引用
Assembly assembly = null;
Type myType = null;
Delegate myDelegate = null;

GC.Collect();
GC.WaitForPendingFinalizers();
// 现在程序集应该被卸载
```

---

## 性能问题

### Q: 编译速度很慢

**症状：** 每次编译需要几秒钟

**原因：**
1. 使用了随机上下文（每次都要初始化）
2. 编译了大量代码
3. 系统资源不足

**优化方案：**
```csharp
// 方案1：使用命名上下文重用
var builder = new AssemblyCSharpBuilder();
builder.UseNewLoadContext("ReusableDomain")  // 而不是 UseRandomLoadContext()
    .UseSmartMode()
    .Add(code);

// 方案2：缓存编译结果
private static Dictionary<string, Assembly> _cache = new();

var key = HashCode.Combine(code);
if (!_cache.TryGetValue(key, out var assembly)) {
    assembly = CompileCode(code);
    _cache[key] = assembly;
}

// 方案3：批量编译
var builder = new AssemblyCSharpBuilder();
builder.UseNewLoadContext("Batch");
builder.Add(code1).Add(code2).Add(code3);  // 一次编译三个
var assembly = builder.GetAssembly();
```

### Q: 内存使用持续增长

**症状：** 应用内存不断增加

**原因：**
1. 在命名上下文中编译过多程序集而没有清理
2. 缓存过多编译结果
3. 内存泄漏

**解决方案：**
```csharp
// 限制上下文中的程序集数量
private Dictionary<string, int> _contextCompileCount = new();
private const int MaxCompilesPerContext = 100;

public void CompileWithRotation(string code) {
    var contextName = "Rotating";
    
    if (!_contextCompileCount.TryGetValue(contextName, out var count)) {
        count = 0;
    }
    
    if (count >= MaxCompilesPerContext) {
        // 创建新上下文，旧的会被垃圾回收
        contextName = $"Rotating_{DateTime.Now.Ticks}";
        _contextCompileCount.Clear();
        count = 0;
    }
    
    var builder = new AssemblyCSharpBuilder();
    builder.UseNewLoadContext(contextName).Add(code);
    builder.GetAssembly();
    
    _contextCompileCount[contextName] = count + 1;
}
```

---

## 其他常见问题

### Q: 如何调试动态生成的代码？

**答案：**
```csharp
// 1. 使用 Debug 编译而不是 Release
builder.WithDebugCompile();

// 2. 输出到文件用 dnSpy 查看
builder.GetAssembly("output.dll");

// 3. 打印生成的代码进行检查
Console.WriteLine(generatedCode);

// 4. 在代码中添加异常处理和日志
builder.Add(@"
    public class DebugClass {
        public static void DoSomething() {
            try {
                // 业务逻辑
            } catch (Exception ex) {
                System.Diagnostics.Debug.WriteLine(ex);
                throw;
            }
        }
    }
");
```

### Q: 支持异步代码吗？

**答案：** 支持
```csharp
builder.Add(@"
    public class AsyncClass {
        public static async Task<int> GetValueAsync() {
            await Task.Delay(100);
            return 42;
        }
    }
");

var assembly = builder.GetAssembly();
var method = assembly.GetTypeFromShortName("AsyncClass")
    .GetMethod("GetValueAsync");
var task = (Task<int>)method.Invoke(null, null);
int result = task.Result;  // 42
```

### Q: 支持泛型吗？

**答案：** 支持
```csharp
builder.Add(@"
    public class GenericClass {
        public static T GetDefault<T>() {
            return default(T);
        }
        
        public static void PrintGeneric<T>(T value) {
            System.Console.WriteLine(typeof(T).Name + ': ' + value);
        }
    }
");
```

---

## 需要更多帮助？

- 查看官方测试案例：`G:\Project\OpenSource\Natasha\test\ut`
- 检查 GitHub Issues：https://github.com/NMSAzure/Natasha/issues
- 参考其他参考文档：`initialization-patterns.md`、`compiler-options.md` 等

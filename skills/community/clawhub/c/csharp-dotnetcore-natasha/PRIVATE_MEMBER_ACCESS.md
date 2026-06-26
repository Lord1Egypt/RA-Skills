# Natasha 私有成员访问完整指南

本文档介绍如何使用 Natasha 访问私有成员、内部成员和公共成员。

---

## 核心概念

### 访问控制级别

C# 中的访问控制级别：
- **private（私有）** - 仅在声明类内可访问
- **internal（内部）** - 仅在同一程序集内可访问
- **public（公共）** - 任何地方都可访问

### Natasha 的三种元数据级别

1. **AllMetadata** - 包含所有级别的元数据（私有、内部、公共）
2. **InternalMetadata** - 仅包含内部和公共元数据
3. **PublicMetadata** - 仅包含公共元数据

---

## 核心 API

### 1. 忽略可访问性检查

```csharp
.ConfigCompilerOption(opt => opt
    .AppendCompilerFlag(Natasha.CSharp.Compiler.CompilerBinderFlags.IgnoreAccessibility)
    .WithAllMetadata()
)
```

**参数说明：**
- `IgnoreAccessibility` - 忽略可访问性检查（关键标志）
- `WithAllMetadata()` - 包含所有元数据级别
- `WithInternalMetadata()` - 仅包含内部和公共元数据
- `WithPublicMetadata()` - 仅包含公共元数据

### 2. 生成可访问私有成员的语法树

```csharp
code.ToAccessPrivateTree(typeof(TargetType))
```

**作用：** 将代码字符串转换为语法树，使其能够访问指定类型的私有成员。

---

## 使用场景和示例

### 场景 1：访问所有成员（私有 + 内部 + 公共）

**适用场景：** 需要访问类的所有成员，包括私有成员。

```csharp
using Natasha;

// 目标类
public class AccessModelTest
{
    private readonly string PrivateName = "Private";
    private string GetPrivate()
    {
        return PrivateName;
    }

    internal string InternalName = "Internal";
    internal string GetInternal()
    {
        return InternalName;
    }

    public string PublicName = "Public";
    public string GetPublic()
    {
        return PublicName;
    }
}

// 使用 Natasha 访问私有成员
public void AccessAllMembers()
{
    AssemblyCSharpBuilder builder = new();
    builder
        .UseRandomLoadContext()
        .UseSmartMode()
        .ConfigCompilerOption(opt => opt
            .AppendCompilerFlag(Natasha.CSharp.Compiler.CompilerBinderFlags.IgnoreAccessibility)
            .WithAllMetadata());  // 包含所有级别的元数据

    string code = $@"
        public class A
        {{
            private string GetPrivate() {{
                return new AccessModelTest().GetPrivate();
            }}
            internal string GetInternal() {{
                return new AccessModelTest().GetInternal();
            }}
            public string GetPublic() {{
                return new AccessModelTest().GetPublic();
            }}
        }}
    ";

    // 将代码转换为可访问私有成员的语法树
    builder.Add(code.ToAccessPrivateTree(typeof(AccessModelTest)));
    var asm = builder.GetAssembly();

    // 测试访问私有成员
    var privateFunc = asm.GetDelegateFromShortName<Func<string>>("A", "GetPrivate");
    Console.WriteLine($"Private: {privateFunc()}");  // Private

    var internalFunc = asm.GetDelegateFromShortName<Func<string>>("A", "GetInternal");
    Console.WriteLine($"Internal: {internalFunc()}");  // Internal

    var publicFunc = asm.GetDelegateFromShortName<Func<string>>("A", "GetPublic");
    Console.WriteLine($"Public: {publicFunc()}");  // Public
}
```

### 场景 2：仅访问内部和公共成员

**适用场景：** 需要访问内部成员，但不包括私有成员。

```csharp
public void AccessInternalAndPublic()
{
    AssemblyCSharpBuilder builder = new();
    builder
        .UseRandomLoadContext()
        .UseSmartMode()
        .ConfigCompilerOption(opt => opt
            .AppendCompilerFlag(Natasha.CSharp.Compiler.CompilerBinderFlags.IgnoreAccessibility)
            .WithInternalMetadata());  // 仅包含内部和公共元数据

    string code = $@"
        public class A
        {{
            internal string GetInternal() {{
                return new AccessModelTest().GetInternal();
            }}
            public string GetPublic() {{
                return new AccessModelTest().GetPublic();
            }}
        }}
    ";

    builder.Add(code.ToAccessPrivateTree(typeof(AccessModelTest)));
    var asm = builder.GetAssembly();

    var internalFunc = asm.GetDelegateFromShortName<Func<string>>("A", "GetInternal");
    Console.WriteLine($"Internal: {internalFunc()}");  // Internal

    var publicFunc = asm.GetDelegateFromShortName<Func<string>>("A", "GetPublic");
    Console.WriteLine($"Public: {publicFunc()}");  // Public
}
```

**限制：** 如果尝试访问私有成员，会抛出 `CS1061` 错误。

```csharp
// ❌ 错误示例
string code = $@"
    public class A
    {{
        private string GetPrivate() {{  // 会编译失败
            return new AccessModelTest().GetPrivate();
        }}
    }}
    ";

try
{
    builder.Add(code.ToAccessPrivateTree(typeof(AccessModelTest)));
    var asm = builder.GetAssembly();
}
catch (NatashaException ex)
{
    // ErrorKind: Compile
    // ErrorId: CS1061
    Console.WriteLine(ex.Message);
}
```

### 场景 3：仅访问公共成员

**适用场景：** 仅需要访问公共成员，不需要访问内部或私有成员。

```csharp
public void AccessPublicOnly()
{
    AssemblyCSharpBuilder builder = new();
    builder
        .UseRandomLoadContext()
        .UseSmartMode()
        .ConfigCompilerOption(opt => opt.WithPublicMetadata());  // 仅包含公共元数据

    string code = $@"
        public class A
        {{
            public string GetPublic() {{
                return new AccessModelTest().GetPublic();
            }}
        }}
    ";

    builder.Add(code);  // 注意：此时不需要 ToAccessPrivateTree
    var asm = builder.GetAssembly();

    var publicFunc = asm.GetDelegateFromShortName<Func<string>>("A", "GetPublic");
    Console.WriteLine($"Public: {publicFunc()}");  // Public
}
```

**限制：** 如果尝试访问私有或内部成员，会抛出 `CS1061` 错误。

```csharp
// ❌ 错误示例
string code = $@"
    public class A
    {{
        private string GetPrivate() {{  // 会编译失败
            return new AccessModelTest().GetPrivate();
        }}
    }}
    ";

try
{
    builder.Add(code);  // 不使用 ToAccessPrivateTree
    var asm = builder.GetAssembly();
}
catch (NatashaException ex)
{
    // ErrorKind: Compile
    // ErrorId: CS1061
    Console.WriteLine(ex.Message);
}
```

---

## 实际应用场景

### 1. 单元测试

访问被测类的私有成员进行测试。

```csharp
public class UserServiceTests
{
    public void TestPrivateMethod()
    {
        var builder = new AssemblyCSharpBuilder();
        builder
            .UseRandomLoadContext()
            .UseSmartMode()
            .ConfigCompilerOption(opt => opt
                .AppendCompilerFlag(CompilerBinderFlags.IgnoreAccessibility)
                .WithAllMetadata());

        string code = $@"
            public class TestHelper
            {{
                public static bool ValidateUser(UserService service, string username) {{
                    // 访问私有方法
                    return service.ValidatePasswordInternal(username);
                }}
            }}
        ";

        builder.Add(code.ToAccessPrivateTree(typeof(UserService)));
        var asm = builder.GetAssembly();
        var validateFunc = asm.GetDelegateFromShortName<Func<UserService, string, bool>>(
            "TestHelper", "ValidateUser"
        );

        var service = new UserService();
        bool isValid = validateFunc(service, "test");
        Assert.True(isValid);
    }
}
```

### 2. 性能优化

替代反射访问私有成员，获得原生性能。

```csharp
public class PrivateMemberAccessor<T>
{
    private static Dictionary<string, Delegate> _accessors = new();

    public static Func<T, object> CreateAccessor(string memberName)
    {
        if (_accessors.TryGetValue(memberName, out var cached))
        {
            return (Func<T, object>)cached;
        }

        var builder = new AssemblyCSharpBuilder();
        builder
            .UseRandomLoadContext()
            .UseSmartMode()
            .ConfigCompilerOption(opt => opt
                .AppendCompilerFlag(CompilerBinderFlags.IgnoreAccessibility)
                .WithAllMetadata());

        string typeName = typeof(T).GetDevelopName();
        string code = $@"
            public class Accessor_{Guid.NewGuid():N}
            {{
                public static object Get({typeName} obj)
                {{
                    return obj.{memberName};
                }}
            }}
        ";

        builder.Add(code.ToAccessPrivateTree(typeof(T)));
        var asm = builder.GetAssembly();
        var accessorType = asm.GetTypes().First();
        var getMethod = accessorType.GetMethod("Get");

        var accessor = (Func<T, object>)Delegate.CreateDelegate(
            typeof(Func<T, object>), getMethod
        );

        _accessors[memberName] = accessor;
        return accessor;
    }
}

// 使用
class InternalData
{
    private int _cachedValue = 42;
}

var accessor = PrivateMemberAccessor<InternalData>.CreateAccessor("_cachedValue");
var data = new InternalData();
int value = (int)accessor(data);  // 42，无反射开销
```

### 3. 框架开发

访问库的内部状态。

```csharp
public class FrameworkUtils
{
    public static void ResetCache<T>(T service)
    {
        var builder = new AssemblyCSharpBuilder();
        builder
            .UseRandomLoadContext()
            .UseSmartMode()
            .ConfigCompilerOption(opt => opt
                .AppendCompilerFlag(CompilerBinderFlags.IgnoreAccessibility)
                .WithAllMetadata());

        string typeName = typeof(T).GetDevelopName();
        string code = $@"
            public class CacheResetter_{Guid.NewGuid():N}
            {{
                public static void Reset({typeName} service)
                {{
                    service._cache.Clear();
                }}
            }}
        ";

        builder.Add(code.ToAccessPrivateTree(typeof(T)));
        var asm = builder.GetAssembly();
        var resetterType = asm.GetTypes().First();
        var resetMethod = resetterType.GetMethod("Reset");

        var resetter = (Action<T>)Delegate.CreateDelegate(
            typeof(Action<T>), resetMethod
        );

        resetter(service);
    }
}
```

---

## 最佳实践

### 1. 选择合适的元数据级别

| 元数据级别 | 可访问成员 | 使用场景 |
|-----------|-----------|---------|
| `WithAllMetadata()` | 私有、内部、公共 | 需要访问私有成员 |
| `WithInternalMetadata()` | 内部、公共 | 需要访问内部成员，但不需要私有成员 |
| `WithPublicMetadata()` | 公共 | 仅需公共成员 |

### 2. 缓存访问器

避免重复编译相同的访问器代码。

```csharp
public static class AccessorCache
{
    private static ConcurrentDictionary<string, Delegate> _cache = new();

    public static Func<T, TResult> GetAccessor<T, TResult>(string memberName)
    {
        string key = $"{typeof(T).FullName}.{memberName}";

        return (Func<T, TResult>)_cache.GetOrAdd(key, _ =>
        {
            // 创建访问器
            return CreateAccessor<T, TResult>(memberName);
        });
    }

    private static Func<T, TResult> CreateAccessor<T, TResult>(string memberName)
    {
        // 实现同上
        // ...
    }
}
```

### 3. 安全考虑

访问私有成员可能破坏封装性，应谨慎使用：

- ✅ **推荐场景**：单元测试、性能优化、框架开发
- ⚠️ **谨慎场景**：生产代码、业务逻辑
- ❌ **不推荐场景**：绕过安全限制、访问未公开的 API

### 4. 错误处理

正确处理编译错误。

```csharp
try
{
    builder.Add(code.ToAccessPrivateTree(typeof(TargetType)));
    var asm = builder.GetAssembly();
}
catch (NatashaException ex)
{
    switch (ex.ErrorKind)
    {
        case NatashaExceptionKind.Compile:
            Console.WriteLine("编译错误：可能尝试访问了不允许的成员");
            break;
        case NatashaExceptionKind.Syntax:
            Console.WriteLine("语法错误");
            break;
        default:
            Console.WriteLine($"未知错误: {ex.Message}");
            break;
    }
}
```

---

## 常见问题

### Q1：能否访问基类的私有成员？

**A：** 可以，只要基类的元数据被包含（`WithAllMetadata()`）。

```csharp
public class BaseService
{
    private string _config = "config";
}

public class MyService : BaseService { }

string code = $@"
    public class Accessor
    {{
        public static string GetConfig(MyService service)
        {{
            return service._config;  // 可以访问基类的私有成员
        }}
    }}
    ";

builder.Add(code.ToAccessPrivateTree(typeof(MyService)));
```

### Q2：能否访问嵌套类的私有成员？

**A：** 可以，使用 `ToAccessPrivateTree(typeof(NestedClass))`。

```csharp
public class OuterClass
{
    private class InnerClass
    {
        private string _data = "inner";
    }
}

string code = $@"
    public class Accessor
    {{
        public static string GetData(OuterClass.InnerClass inner)
        {{
            return inner._data;
        }}
    }}
    ";

builder.Add(code.ToAccessPrivateTree(typeof(OuterClass.InnerClass)));
```

### Q3：能否访问静态私有成员？

**A：** 可以，语法相同。

```csharp
public class MyClass
{
    private static string _staticData = "static";
}

string code = $@"
    public class Accessor
    {{
        public static string GetStaticData()
        {{
            return MyClass._staticData;
        }}
    }}
    ";

builder.Add(code.ToAccessPrivateTree(typeof(MyClass)));
```

### Q4：性能相比反射如何？

**A：** 动态编译的代码性能接近手写代码，远超反射。

- **反射**：每次调用都需要查找元数据
- **动态编译**：只编译一次，后续直接访问

基准测试结果（示例）：
- 反射访问：~1000ns/次
- 动态编译：~10ns/次
- 直接访问：~5ns/次

---

## 总结

### 关键要点

1. **使用 `IgnoreAccessibility` 标志** - 忽略可访问性检查
2. **选择合适的元数据级别** - 根据需求选择 `WithAllMetadata()` / `WithInternalMetadata()` / `WithPublicMetadata()`
3. **使用 `ToAccessPrivateTree()`** - 将代码转换为可访问私有成员的语法树
4. **缓存访问器** - 避免重复编译
5. **谨慎使用** - 仅在必要场景下使用，注意封装性

### 推荐实践

- ✅ **单元测试** - 访问被测类的内部状态
- ✅ **性能关键路径** - 替代反射，获得原生性能
- ✅ **框架开发** - 访问库的内部状态
- ⚠️ **生产代码** - 谨慎使用，避免破坏封装性

---

## 参考资料

- 源码：`G:\Project\OpenSource\Natasha\test\ut\Compile\MemAssembly\Compile\Access\`
- 测试文件：
  - `PrivateTest.cs` - 完整的私有成员访问测试
  - `AccessModelTest.cs` - 测试目标类
  - `IgnoresAccessChecksToAttribute.cs` - 访问检查忽略特性

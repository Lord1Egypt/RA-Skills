# 常见使用模式与实战示例

## 重要提示：使用 type.GetDevelopName()

在构建动态脚本字符串时,必须使用 **`type.GetDevelopName()`** 来获取运行时能够识别的类型名称。

**为什么需要?**
- `Type.FullName` 无法正确处理泛型类型的特殊符号(如 ` ` 反引号)
- `GetDevelopName()` 能正确处理:泛型、数组、多维数组、嵌套类型等复杂场景

**示例:**
```csharp
// ❌ 错误:直接使用 Type.FullName
string typeName = typeof(List<int>).FullName;  // "System.Collections.Generic.List`1[[System.Int32, ...]]"
// 这样拼接的代码无法编译!

// ✅ 正确:使用 GetDevelopName()
string typeName = typeof(List<int>).GetDevelopName();  // "System.Collections.Generic.List<System.Int32>"
var code = $"var list = new {typeName}();";  // 可以正确编译
```

**更多示例:**
```csharp
typeof(int?).GetDevelopName();                      // "System.Nullable<System.Int32>"
typeof(List<int>[]).GetDevelopName();               // "System.Collections.Generic.List<System.Int32>[]"
typeof(Dictionary<List<int>[], int>).GetDevelopName(); // "System.Collections.Generic.Dictionary<System.Collections.Generic.List<System.Int32>[],System.Int32>"
```

**使用场景:**
- 动态生成依赖注入代码
- 动态生成 JSON 序列化器
- 动态生成 ORM 映射代码
- 任何需要将运行时类型转换为 C# 代码字符串的场景

---

## 模式 1：缓存委托的计算工具

适用于需要反复执行相同计算的场景。

```csharp
public class DynamicCalculator {
    private static Dictionary<string, Delegate> _delegateCache = new();
    
    public static T GetOrCreateDelegate<T>(string code, string className, string methodName) 
        where T : Delegate {
        
        string cacheKey = $"{className}.{methodName}";
        
        if (_delegateCache.TryGetValue(cacheKey, out var cached)) {
            return (T)cached;
        }
        
        // 首次编译
        var builder = new AssemblyCSharpBuilder();
        builder
            .UseNewLoadContext("CalculatorDomain")
            .UseSmartMode()
            .Add(code);
        
        var assembly = builder.GetAssembly();
        var @delegate = assembly.GetDelegateFromShortName<T>(className, methodName);
        
        _delegateCache[cacheKey] = @delegate;
        return @delegate;
    }
}

// 使用
var addFunc = DynamicCalculator.GetOrCreateDelegate<Func<int, int, int>>(
    "public class Math { public static int Add(int a, int b) => a + b; }",
    "Math",
    "Add"
);

int result1 = addFunc(3, 5);  // 编译
int result2 = addFunc(10, 20); // 使用缓存
```

## 模式 2：数据类动态生成

常见于 ORM、序列化框架等需要动态数据模型的场景。

```csharp
public class DataClassGenerator {
    public static Type GenerateDataClass(string className, Dictionary<string, string> properties) {
        // 初始化
        NatashaManagement
            .GetInitializer()
            .WithMemoryUsing()
            .WithMemoryReference()
            .Preheating<NatashaDomainCreator>();
        
        var propertyCode = string.Join("\n", properties.Select(p => 
            $"public {p.Value} {p.Key} {{ get; set; }}"
        ));
        
        var builder = new AssemblyCSharpBuilder();
        builder
            .UseRandomLoadContext()
            .UseSmartMode()
            .Add($@"
                public class {className} {{
                    {propertyCode}
                    
                    public override string ToString() {{
                        return $""{{GetType().Name}} {{ {string.Join(", ", properties.Keys.Select(k => $"{k}={{{k}}}"))} }}"";
                    }}
                }}
            ");
        
        var assembly = builder.GetAssembly();
        return assembly.GetTypeFromShortName(className);
    }
}

// 使用
var userType = DataClassGenerator.GenerateDataClass("User", new() {
    { "Id", "int" },
    { "Name", "string" },
    { "Email", "string" }
});

var user = Activator.CreateInstance(userType);
userType.GetProperty("Id")!.SetValue(user, 1);
userType.GetProperty("Name")!.SetValue(user, "Alice");
userType.GetProperty("Email")!.SetValue(user, "alice@example.com");
Console.WriteLine(user);  // User { Id=1, Name=Alice, Email=alice@example.com }
```

## 模式 3：表达式树到委托转换

用于将动态表达式编译为高性能委托。

```csharp
public class ExpressionCompiler {
    public static Func<T, TResult> CompileExpression<T, TResult>(
        string className, 
        string methodName, 
        string expressionBody) {
        
        var builder = new AssemblyCSharpBuilder();
        builder
            .UseRandomLoadContext()
            .UseSmartMode()
            .Add($@"
                public class {className} {{
                    public static {typeof(TResult).Name} {methodName}({typeof(T).Name} item) {{
                        {expressionBody}
                    }}
                }}
            ");
        
        var assembly = builder.GetAssembly();
        return assembly.GetDelegateFromShortName<Func<T, TResult>>(className, methodName);
    }
}

// 使用示例：将字符串表达式编译为委托
class Person {
    public string Name { get; set; }
    public int Age { get; set; }
}

var isAdultCompiler = ExpressionCompiler.CompileExpression<Person, bool>(
    "Validator",
    "IsAdult",
    "return item.Age >= 18;"
);

var person = new Person { Name = "Bob", Age = 25 };
bool result = isAdultCompiler(person);  // true
```

## 模式 4：插件系统

允许在运行时加载和执行用户提供的代码。

```csharp
public interface IPlugin {
    string Execute(string input);
}

public class PluginLoader {
    private Dictionary<string, IPlugin> _plugins = new();
    
    public void RegisterPlugin(string name, string code) {
        var builder = new AssemblyCSharpBuilder();
        builder
            .UseNewLoadContext($"Plugin_{name}")
            .UseSmartMode()
            .Add(code);
        
        var assembly = builder.GetAssembly();
        var pluginType = assembly.GetTypeFromShortName("Plugin");
        
        if (!typeof(IPlugin).IsAssignableFrom(pluginType)) {
            throw new InvalidOperationException($"Plugin {name} 必须实现 IPlugin 接口");
        }
        
        var instance = (IPlugin)Activator.CreateInstance(pluginType);
        _plugins[name] = instance;
    }
    
    public string ExecutePlugin(string name, string input) {
        if (!_plugins.TryGetValue(name, out var plugin)) {
            throw new KeyNotFoundException($"插件 {name} 未找到");
        }
        return plugin.Execute(input);
    }
}

// 使用
var loader = new PluginLoader();

loader.RegisterPlugin("upper", @"
    public class Plugin : IPlugin {
        public string Execute(string input) {
            return input.ToUpper();
        }
    }
");

loader.RegisterPlugin("reverse", @"
    public class Plugin : IPlugin {
        public string Execute(string input) {
            return new string(input.Reverse().ToArray());
        }
    }
");

Console.WriteLine(loader.ExecutePlugin("upper", "hello"));    // HELLO
Console.WriteLine(loader.ExecutePlugin("reverse", "hello"));  // olleh
```

## 模式 5：业务规则引擎

用于动态加载和执行业务规则。

```csharp
public class Rule {
    public string Name { get; set; }
    public Func<T, bool> Condition { get; set; }
    public Action<T> Action { get; set; }
}

public class RuleEngine<T> {
    private List<Rule> _rules = new();
    
    public void RegisterRule(string name, string conditionCode, string actionCode) {
        var builder = new AssemblyCSharpBuilder();
        builder
            .UseRandomLoadContext()
            .UseSmartMode()
            .Add($@"
                public class Rules {{
                    public static bool CheckCondition({typeof(T).Name} item) {{
                        {conditionCode}
                    }}
                    
                    public static void ExecuteAction({typeof(T).Name} item) {{
                        {actionCode}
                    }}
                }}
            ");
        
        var assembly = builder.GetAssembly();
        var conditionFunc = assembly.GetDelegateFromShortName<Func<T, bool>>("Rules", "CheckCondition");
        var actionFunc = assembly.GetDelegateFromShortName<Action<T>>("Rules", "ExecuteAction");
        
        _rules.Add(new Rule { 
            Name = name, 
            Condition = conditionFunc, 
            Action = actionFunc 
        });
    }
    
    public void Execute(T item) {
        foreach (var rule in _rules) {
            try {
                if (rule.Condition(item)) {
                    rule.Action(item);
                    Console.WriteLine($"规则 '{rule.Name}' 执行成功");
                }
            } catch (Exception ex) {
                Console.WriteLine($"规则 '{rule.Name}' 执行失败: {ex.Message}");
            }
        }
    }
}

// 使用示例
class Order {
    public decimal Amount { get; set; }
    public int Discount { get; set; }
}

var engine = new RuleEngine<Order>();

// 大额订单规则
engine.RegisterRule(
    "BigOrder",
    "return item.Amount > 1000;",
    "item.Discount = 20; Console.WriteLine($\"应用 VIP 折扣: {item.Discount}%\");"
);

// 新客户规则
engine.RegisterRule(
    "NewCustomer",
    "return item.Discount == 0;",
    "item.Discount = 10; Console.WriteLine($\"应用新客折扣: {item.Discount}%\");"
);

var order = new Order { Amount = 1500, Discount = 0 };
engine.Execute(order);
```

## 模式 6：动态查询和转换

用于构建动态数据转换管道。

```csharp
public class DynamicTransformer {
    public static Func<IEnumerable<T>, IEnumerable<TResult>> 
        CompileTransformer<T, TResult>(string transformCode) {
        
        var builder = new AssemblyCSharpBuilder();
        builder
            .UseRandomLoadContext()
            .UseSmartMode()
            .Add($@"
                using System;
                using System.Collections.Generic;
                using System.Linq;
                
                public class Transformer {{
                    public static IEnumerable<{typeof(TResult).Name}> Transform(IEnumerable<{typeof(T).Name}> items) {{
                        {transformCode}
                    }}
                }}
            ");
        
        var assembly = builder.GetAssembly();
        return assembly.GetDelegateFromShortName<Func<IEnumerable<T>, IEnumerable<TResult>>>(
            "Transformer", "Transform"
        );
    }
}

// 使用示例
record Person(string Name, int Age);
record PersonDto(string FullName, int AgeGroup);

var transformer = DynamicTransformer.CompileTransformer<Person, PersonDto>(
    "return items.Where(p => p.Age >= 18).Select(p => new PersonDto(" +
    "    p.Name.ToUpper(), " +
    "    p.Age / 10 * 10" +
    "));"
);

var people = new[] {
    new Person("Alice", 25),
    new Person("Bob", 17),
    new Person("Charlie", 30)
};

var result = transformer(people).ToList();
// 结果: [ PersonDto(ALICE, 20), PersonDto(CHARLIE, 30) ]
```

## 模式 7：访问私有成员的性能优化

用于需要访问库内部状态的性能关键代码路径。

```csharp
public class PerformanceOptimizer {
    public static Func<T, object> CreatePrivateFieldAccessor<T>(string fieldName) {
        var fieldType = typeof(T).GetField(fieldName, 
            System.Reflection.BindingFlags.NonPublic | 
            System.Reflection.BindingFlags.Instance
        )?.FieldType ?? typeof(object);
        
        var builder = new AssemblyCSharpBuilder();
        builder
            .UseRandomLoadContext()
            .UseSmartMode()
            .ConfigCompilerOption(opt => opt
                .AppendCompilerFlag(IgnoreAccessibility)
                .WithAllMetadata()
            )
            .ToAccessPrivateTree(typeof(T))
            .Add($@"
                public class FieldAccessor {{
                    public static object GetField({typeof(T).Name} instance) {{
                        return instance.{fieldName};
                    }}
                }}
            ");
        
        var assembly = builder.GetAssembly();
        return assembly.GetDelegateFromShortName<Func<T, object>>("FieldAccessor", "GetField");
    }
}

// 使用
class InternalData {
    private int _cachedValue = 42;
    private string _internalState = "secret";
}

var valueAccessor = PerformanceOptimizer.CreatePrivateFieldAccessor<InternalData>("_cachedValue");
var data = new InternalData();

int value = (int)valueAccessor(data);  // 42，无反射开销
```

## 性能提示

1. **缓存编译结果** - 编译代码一次，多次重用
2. **使用委托** - 比反射调用快 10-100 倍
3. **批量初始化** - 在应用启动时做一次初始化
4. **选择合适的上下文** - 临时用随机上下文，长期用命名上下文
5. **释放资源** - 不需要的程序集允许垃圾回收

---

## 模式 8：精简模式（自管理元数据）

适用于需要精确控制元数据覆盖的场景，避免引入不必要的命名空间。

```csharp
// 只注册域创建器，无需预热全局元数据
NatashaManagement.RegistDomainCreator<NatashaDomainCreator>();

// 仅添加需要的类型的程序集（及其依赖）
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSimpleMode()
    .ConfigLoadContext(ldc => ldc
        .AddReferenceAndUsingCode(typeof(Math).Assembly)   // System.Runtime（含 Math）
        .AddReferenceAndUsingCode(typeof(MathF))           // System.Runtime（含 MathF）
        .AddReferenceAndUsingCode(typeof(object)))         // 核心基类
    .Add("public static class Calc { public static double Floor(double v) { return Math.Floor(v / 0.3); } }");

var assembly = builder.GetAssembly();
var func = assembly.GetDelegateFromShortName<Func<double, double>>("Calc", "Floor");
Console.WriteLine(func(1.0));  // 3
```

**关键：** `AddReferenceAndUsingCode(typeof(T))` 从类型推导程序集，同时加载其依赖，并自动提取所有 using code，脚本中无需手写 `using`。

---

## 模式 9：自定义编译模式（外部元数据集）

适用于使用 `Basic.Reference.Assemblies` 等第三方元数据包的场景，完全由开发者控制引用。

```csharp
// 需要 NuGet: Basic.Reference.Assemblies.Net80
// dotnet add package Basic.Reference.Assemblies.Net80

using Basic.Reference.Assemblies;

// 无需任何 Natasha 预热
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomDomain()
    .WithSpecifiedReferences(Net80.References.All)    // 使用外部提供的完整 .NET 8 引用集
    .WithoutCombineUsingCode()                        // 不自动注入 using，脚本自带
    .WithReleaseCompile()
    .Add(@"
        using System;
        using static System.Math;
        public static class A {
            public static int Add(int a, int b) { return a + b; }
        }
    ");

var assembly = builder.GetAssembly();
```

**注意：** `WithoutCombineUsingCode()` 关闭 using 自动注入后，脚本必须手动加 `using` 指令。

---

## 模式 10：重复编译优化（复用编译选项和引用）

适用于同一 Builder 实例反复编译多段代码的场景（如热重载、脚本引擎）。

```csharp
AssemblyCSharpBuilder builder = new();
builder
    .UseNewLoadContext("ScriptEngine")
    .UseSmartMode()
    .WithPreCompilationOptions()      // 复用编译选项（debug/release 等）
    .WithPreCompilationReferences();  // 复用元数据引用集

// 第一次编译
builder.WithRandomAssenblyName().Add("public class Script1 { public int Run() => 1; }");
var asm1 = builder.GetAssembly();

// 第二次编译 - 复用之前的编译选项和引用，只重新解析语法树
builder.Clear();
builder.WithRandomAssenblyName().Add("public class Script2 { public int Run() => 2; }");
var asm2 = builder.GetAssembly();

// 验证
Console.WriteLine(asm1.GetTypeFromShortName("Script1").GetMethod("Run")!.Invoke(Activator.CreateInstance(asm1.GetTypeFromShortName("Script1")), null));  // 1
Console.WriteLine(asm2.GetTypeFromShortName("Script2").GetMethod("Run")!.Invoke(Activator.CreateInstance(asm2.GetTypeFromShortName("Script2")), null));  // 2
```

---

## 模式 11：动态依赖注入容器

适用于需要高性能依赖注入的场景,相比传统反射方式具有原生性能优势。

**核心思想:**
- 使用 Natasha 动态编译生成实例创建代码
- 避免反射调用,获得原生性能
- 支持构造函数注入和字段注入

```csharp
public class DependencyContainer
{
    private Dictionary<string, Type> _registrations = new();
    private Dictionary<Type, Func<DependencyContainer, object>> _instanceCreators = new();

    // 注册服务
    public void Register<TInterface, TImplementation>() where TImplementation : TInterface
    {
        _registrations[typeof(TInterface).FullName!] = typeof(TImplementation);
    }

    // 解析服务
    public T Resolve<T>()
    {
        return (T)Resolve(typeof(T));
    }

    public object Resolve(Type interfaceType)
    {
        if (_registrations.TryGetValue(interfaceType.FullName!, out var implementationType))
        {
            // 获取或创建实例创建器
            if (!_instanceCreators.TryGetValue(implementationType, out var creator))
            {
                creator = GenerateInstanceCreator(implementationType);
                _instanceCreators[implementationType] = creator;
            }
            return creator(this);
        }
        throw new Exception($"未注册的类型: {interfaceType.FullName}");
    }

    // 动态生成实例创建代码
    private Func<DependencyContainer, object> GenerateInstanceCreator(Type type)
    {
        // 1. 获取类型名称 - 必须使用 GetDevelopName()
        var typeName = type.GetDevelopName();

        // 2. 分析构造函数参数
        var constructors = type.GetConstructors();
        if (constructors.Length == 0)
        {
            // 无参构造函数
            return GenerateSimpleInstanceCreator(typeName);
        }

        // 选择第一个构造函数(实际项目中可能需要更复杂的策略)
        var constructor = constructors[0];
        var parameters = constructor.GetParameters();

        // 3. 生成依赖解析代码
        var resolveCode = new StringBuilder();
        for (int i = 0; i < parameters.Length; i++)
        {
            var paramType = parameters[i].ParameterType;
            var paramTypeName = paramType.GetDevelopName();
            resolveCode.AppendLine($"            var arg{i} = ({paramTypeName})container.Resolve(typeof({paramTypeName}));");
        }

        // 4. 生成实例创建代码
        var paramNames = string.Join(", ", parameters.Select((_, i) => $"arg{i}"));
        var code = $@"
            using System;

            public class InstanceCreator_{Guid.NewGuid():N} {{
                public static object Create(DependencyContainer container) {{
                    {resolveCode}
                    return new {typeName}({paramNames});
                }}
            }}
        ";

        // 5. 编译代码
        var builder = new AssemblyCSharpBuilder();
        builder.UseRandomLoadContext().UseSmartMode().Add(code);
        var assembly = builder.GetAssembly();

        // 6. 获取创建方法并创建委托
        var creatorType = assembly.GetTypes().First();
        var createMethod = creatorType.GetMethod("Create");
        return (Func<DependencyContainer, object>)Delegate.CreateDelegate(
            typeof(Func<DependencyContainer, object>), createMethod
        );
    }

    // 生成无参构造函数的创建器
    private Func<DependencyContainer, object> GenerateSimpleInstanceCreator(string typeName)
    {
        var code = $@"
            public class InstanceCreator_{Guid.NewGuid():N} {{
                public static object Create(DependencyContainer container) {{
                    return new {typeName}();
                }}
            }}
        ";

        var builder = new AssemblyCSharpBuilder();
        builder.UseRandomLoadContext().UseSmartMode().Add(code);
        var assembly = builder.GetAssembly();

        var creatorType = assembly.GetTypes().First();
        var createMethod = creatorType.GetMethod("Create");
        return (Func<DependencyContainer, object>)Delegate.CreateDelegate(
            typeof(Func<DependencyContainer, object>), createMethod
        );
    }
}

// 使用示例
public interface ILogger
{
    void Log(string message);
}

public interface IDatabase
{
    void Query(string sql);
}

public interface IUserService
{
    void GetUser(int id);
}

public class ConsoleLogger : ILogger
{
    public void Log(string message) => Console.WriteLine($"[Logger] {message}");
}

public class SqliteDatabase : IDatabase
{
    private ILogger _logger;

    public void SetLogger(ILogger logger) => _logger = logger;

    public void Query(string sql) => _logger?.Log($"执行 SQL: {sql}");
}

public class UserService : IUserService
{
    private readonly ILogger _logger;
    private readonly IDatabase _database;

    public UserService(ILogger logger, IDatabase database)
    {
        _logger = logger;
        _database = database;
    }

    public void GetUser(int id)
    {
        _logger.Log($"获取用户 ID: {id}");
        _database.Query($"SELECT * FROM Users WHERE Id = {id}");
    }
}

// 初始化容器
var container = new DependencyContainer();
NatashaManagement.Preheating<NatashaDomainCreator>();

// 注册服务
container.Register<ILogger, ConsoleLogger>();
container.Register<IDatabase, SqliteDatabase>();
container.Register<IUserService, UserService>();

// 解析服务 - 自动注入依赖
var userService = container.Resolve<IUserService>();
userService.GetUser(1);
```

**性能优势:**
- 相比反射调用,动态编译的代码具有原生性能
- 实例创建器可以缓存,避免重复编译
- 代码可调试,开发体验更好

---

## 模式 12：动态 JSON 序列化和 ORM 映射

适用于需要高性能序列化和数据映射的场景,通过动态编译为每个类型生成专门的序列化器。

**核心思想:**
- 动态生成数据类
- 为每个类型生成专门的序列化/反序列化代码
- 避免反射遍历属性,获得接近原生代码的性能

### 12.1 动态生成数据类

```csharp
public static Type GenerateDataClass(string className, Dictionary<string, string> properties)
{
    var propertyCode = string.Join("\n    ", properties.Select(p =>
        $"public {p.Value} {p.Key} {{ get; set; }}"
    ));

    var builder = new AssemblyCSharpBuilder();
    builder.UseRandomLoadContext().UseSmartMode()
        .Add($@"
            public class {className} {{
                {propertyCode}
            }}
        ");

    var assembly = builder.GetAssembly();
    return assembly.GetTypeFromShortName(className);
}

// 使用
var userType = GenerateDataClass("User", new Dictionary<string, string>
{
    { "Id", "int" },
    { "Name", "string" },
    { "Email", "string" },
    { "Age", "int" }
});

var user = Activator.CreateInstance(userType);
userType.GetProperty("Id")?.SetValue(user, 1);
userType.GetProperty("Name")?.SetValue(user, "Alice");
```

### 12.2 动态生成序列化器

```csharp
public static object DynamicSerialize(object obj, Type type)
{
    // 生成专门针对该类型的序列化代码
    var properties = type.GetProperties();
    var typeName = type.GetDevelopName();

    var partsCode = new StringBuilder();
    partsCode.AppendLine("var parts = new List<string>();");
    partsCode.AppendLine("string value;");

    foreach (var prop in properties)
    {
        var propTypeName = prop.PropertyType.GetDevelopName();

        partsCode.AppendLine($"value = obj.{prop.Name}?.ToString();");
        partsCode.AppendLine($"parts.Add($\"\\\"{prop.Name}\\\":{{value}}\");");
    }

    var code = $@"
        using System;
        using System.Collections.Generic;

        public class Serializer_{Guid.NewGuid():N} {{
            public static string Serialize({typeName} obj) {{
                {partsCode}
                return \"{{\" + string.Join(\",\", parts) + \"}}\";
            }}
        }}
    ";

    var builder = new AssemblyCSharpBuilder();
    builder.UseRandomLoadContext().UseSmartMode().Add(code);
    var assembly = builder.GetAssembly();

    var serializerType = assembly.GetTypes().First();
    var serializeMethod = serializerType.GetMethod("Serialize");
    var @delegate = Delegate.CreateDelegate(typeof(Func<object, string>), serializeMethod);

    return @delegate.DynamicInvoke(obj);
}

// 使用
var user = Activator.CreateInstance(userType);
userType.GetProperty("Name")?.SetValue(user, "Alice");
userType.GetProperty("Age")?.SetValue(user, 30);

var json = DynamicSerialize(user, userType);
Console.WriteLine(json);  // {"Id":"1","Name":"Alice","Email":"alice@example.com","Age":"30"}
```

### 12.3 动态 ORM 映射

```csharp
public static object DynamicMapToObject(System.Data.IDataReader reader, Type type)
{
    var typeName = type.GetDevelopName();
    var properties = type.GetProperties();

    var mappingCode = new StringBuilder();
    mappingCode.AppendLine($"var obj = new {typeName}();");
    mappingCode.AppendLine("int ordinal;");

    foreach (var prop in properties)
    {
        var propType = prop.PropertyType.GetDevelopName();

        mappingCode.AppendLine($"ordinal = reader.GetOrdinal(\"{prop.Name}\");");
        mappingCode.AppendLine($"if (!reader.IsDBNull(ordinal)) {{");

        // 根据类型生成不同的读取逻辑
        if (prop.PropertyType == typeof(int))
            mappingCode.AppendLine($"    obj.{prop.Name} = reader.GetInt32(ordinal);");
        else if (prop.PropertyType == typeof(string))
            mappingCode.AppendLine($"    obj.{prop.Name} = reader.GetString(ordinal);");
        else if (prop.PropertyType == typeof(decimal))
            mappingCode.AppendLine($"    obj.{prop.Name} = reader.GetDecimal(ordinal);");
        else if (prop.PropertyType == typeof(bool))
            mappingCode.AppendLine($"    obj.{prop.Name} = reader.GetBoolean(ordinal);");
        else
            mappingCode.AppendLine($"    obj.{prop.Name} = ({propType})reader.GetValue(ordinal);");

        mappingCode.AppendLine("}");
    }

    mappingCode.AppendLine("return obj;");

    var code = $@"
        using System;
        using System.Data;

        public class Mapper_{Guid.NewGuid():N} {{
            public static {typeName} Map(IDataReader reader) {{
                {mappingCode}
            }}
        }}
    ";

    var builder = new AssemblyCSharpBuilder();
    builder.UseRandomLoadContext().UseSmartMode().Add(code);
    var assembly = builder.GetAssembly();

    var mapperType = assembly.GetTypes().First();
    var mapMethod = mapperType.GetMethod("Map");
    var @delegate = Delegate.CreateDelegate(typeof(Func<System.Data.IDataReader, object>), mapMethod);

    return @delegate.DynamicInvoke(reader);
}

// 使用示例 (假设有 SQLite 数据库)
var productType = GenerateDataClass("Product", new Dictionary<string, string>
{
    { "Id", "int" },
    { "Name", "string" },
    { "Price", "decimal" },
    { "Description", "string" }
});

// 假设从数据库读取数据
// while (reader.Read())
// {
//     var product = DynamicMapToObject(reader, productType);
//     Console.WriteLine($"{productType.GetProperty("Name")?.GetValue(product)} - {productType.GetProperty("Price")?.GetValue(product)}");
// }
```

**性能对比:**
- **反射方式**: 每次都需要遍历属性,通过反射获取和设置值
- **动态编译**: 只编译一次,后续直接访问属性,编译器可优化
- **性能提升**: 根据场景不同,通常比反射快 **5-50 倍**

**使用建议:**
1. **缓存序列化器**: 为每个类型生成一次序列化器后缓存复用
2. **泛型封装**: 使用泛型提供类型安全的 API
3. **拆箱处理**: 如果使用 object 作为返回类型,需要考虑拆箱开销

---

## Natasha 的适用场景

**Natasha 适用于绝大多数反射场景**,主要包括:

1. **依赖注入框架** - 动态创建实例并注入依赖
2. **序列化/反序列化** - 为类型生成高性能序列化器
3. **ORM 映射** - 数据库记录到对象的动态映射
4. **代理生成** - AOP、拦截器、装饰器模式
5. **代码生成工具** - 根据元数据生成样板代码
6. **插件系统** - 动态加载和执行用户代码
7. **规则引擎** - 动态编译业务规则
8. **表达式编译** - 将字符串表达式编译为委托

**相比传统反射的优势:**
- ✅ **原生性能** - 编译后的代码性能接近手写代码
- ✅ **代码直观** - 脚本代码更易读易维护
- ✅ **可调试** - 可以设置断点调试动态代码
- ✅ **类型安全** - 编译时检查语法错误

---

## 模式 13：动态插件热加载系统

适用于需要动态加载和执行用户定义逻辑的场景,如办公文档自动化、报表生成等。

**核心思想:**
- 文件命名约定控制执行顺序(如 `1.logical`, `2.logical`)
- 模板包装:将业务逻辑代码动态包装成继承类
- 类型名随机生成避免冲突
- 支持批量编译多个逻辑文件

```csharp
public abstract class APluginReader
{
    public virtual void ConfigHead(string strategyName) { }
    public virtual int Jump(int row, int col, object? value) => 0;
    public virtual void ReadRowData(int row, int col, object? value) { }
    public virtual void ReadColData(int row, int col, object? value) { }
    public virtual void Completed() { }
}

public static class DynamicLogicalCompileHelper
{
    public static List<T> ScanLogical<T>(string[] pluginFiles, string fatherClassName) where T : class
    {
        List<T> result = [];

        AssemblyCSharpBuilder assemblyCSharp = new();
        assemblyCSharp
            .UseRandomLoadContext()
            .UseSmartMode()
            .WithDebugCompile(c => c.ForAssembly());

        var fileIndexArray = new int[pluginFiles.Length];
        Dictionary<int, string> typeNamesCache = [];

        for (int i = 0; i < pluginFiles.Length; i++)
        {
            var fileIndexString = Path.GetFileNameWithoutExtension(pluginFiles[i]);
            if (fileIndexString != null && Int32.TryParse(fileIndexString, out var fileIndex))
            {
                // 生成随机类名避免冲突
                var className = $"N{Guid.NewGuid():n}";
                typeNamesCache.Add(fileIndex, className);

                // 读取逻辑代码并模板包装
                var classMethodText = File.ReadAllText(pluginFiles[i]);
                var classScript = @$"public class {className} : {fatherClassName}{{
                    {classMethodText}
                }}";

                assemblyCSharp.Add(classScript);
                fileIndexArray[i] = fileIndex;
            }
        }

        assemblyCSharp.LogCompilationEvent += (log) => { Console.WriteLine(log.ToString()); };
        var newAssembly = assemblyCSharp.GetAssembly();

        // 按文件名排序后创建实例
        Array.Sort(fileIndexArray);
        for (int i = 0; i < fileIndexArray.Length; i++)
        {
            var newType = newAssembly.GetTypeFromShortName(typeNamesCache[fileIndexArray[i]]);
            var handler = Activator.CreateInstance(newType) as T;
            if (handler == null)
            {
                throw new Exception("Logical Handle 创建失败!");
            }
            result.Add(handler);
        }

        return result;
    }
}

// 使用示例
// 假设有以下文件:
// 1.logical: public override void ReadRowData(int row, int col, object? value) { Console.WriteLine($"读取 [{row},{col}]: {value}"); }
// 2.logical: public override void ReadRowData(int row, int col, object? value) { if (row == 5) Console.WriteLine("发现特殊行!"); }

var pluginFiles = new[] { "1.logical", "2.logical" };
var plugins = DynamicLogicalCompileHelper.ScanLogical<APluginReader>(pluginFiles, "APluginReader");

// 按顺序执行插件
foreach (var plugin in plugins)
{
    plugin.ReadRowData(1, 1, "测试数据");
    plugin.ReadRowData(5, 1, "特殊数据");
}
```

**设计要点:**
1. **文件名即执行顺序**:数字前缀控制插件执行顺序
2. **模板包装**:业务代码只需关注逻辑,无需手动写类定义
3. **随机类名**:使用 GUID 避免命名冲突
4. **批量编译**:多个逻辑文件一次性编译,提高效率

---

## 模式 14：元数据反射映射优化

适用于需要将外部数据映射到对象属性/字段的场景,通过编译期优化避免运行时反射开销。

**核心思想:**
- 特性驱动:使用自定义特性标记需要映射的成员
- 编译期 if-else 树:生成类型安全的查找逻辑
- 委托缓存:静态构造器一次性编译,避免重复反射
- `GetDevelopName()`:正确处理泛型、可空类型等复杂场景

### 14.1 定义映射特性

```csharp
public class EHeaderAttribute : Attribute
{
    public readonly string[] Names;
    public EHeaderAttribute(params string[] name) { Names = name; }
}
```

### 14.2 动态生成映射委托

```csharp
public class ObjectToValue
{
    public static double? ToDouble(object? value) => value == null ? null : Convert.ToDouble(value);
    public static bool? ToBoolean(object? value) => value == null ? null : Convert.ToBoolean(value);
    public static string ToString(object? value) => value?.ToString() ?? string.Empty;
}

public static class ClassOperator<T>
{
    static ClassOperator()
    {
        AssemblyCSharpBuilder assemblyCSharp = new();
        assemblyCSharp
            .UseRandomLoadContext()
            .UseSmartMode()
            .WithDebugCompile();

        assemblyCSharp.LogCompilationEvent += (log) => { Console.WriteLine(log.ToString()); };
        var type = typeof(T);

        StringBuilder scriptWrite = new();
        StringBuilder scriptRead = new();

        // 处理字段
        var fields = type.GetFields(BindingFlags.Public | BindingFlags.Instance);
        foreach (var field in fields)
        {
            var attr = field.GetCustomAttribute<EHeaderAttribute>();
            if (attr != null)
            {
                var attrNames = attr.Names;
                if (attrNames.Length >= 1)
                {
                    scriptWrite.AppendLine($"if(arg2 == \"{attrNames[0]}\"");
                    scriptRead.AppendLine($"if(arg2 == \"{attrNames[0]}\"");
                }
                for (int i = 1; i < attrNames.Length; i++)
                {
                    scriptWrite.AppendLine($" || arg2 == \"{attrNames[i]}\"");
                    scriptRead.AppendLine($" || arg2 == \"{attrNames[i]}\"");
                }
                scriptWrite.AppendLine("){");
                scriptRead.AppendLine("){");

                // 根据类型生成转换逻辑
                if (field.FieldType == typeof(string))
                    scriptWrite.AppendLine(@$"arg1.{field.Name} = ObjectToValue.ToString(arg3);return;}}");
                else if (field.FieldType == typeof(double?))
                    scriptWrite.AppendLine(@$"arg1.{field.Name} = ObjectToValue.ToDouble(arg3);return;}}");
                else if (field.FieldType == typeof(bool?))
                    scriptWrite.AppendLine(@$"arg1.{field.Name} = ObjectToValue.ToBoolean(arg3);return;}}");

                scriptRead.AppendLine(@$"return arg1.{field.Name}; }}");
            }
        }

        // 处理属性
        var properties = type.GetProperties(BindingFlags.Public | BindingFlags.Instance);
        foreach (var property in properties)
        {
            var attr = property.GetCustomAttribute<EHeaderAttribute>();
            if (attr != null)
            {
                var attrNames = attr.Names;
                if (attrNames.Length >= 1)
                {
                    scriptWrite.AppendLine($"if(arg2 == \"{attrNames[0]}\"");
                    scriptRead.AppendLine($"if(arg2 == \"{attrNames[0]}\"");
                }
                for (int i = 1; i < attrNames.Length; i++)
                {
                    scriptWrite.AppendLine($" || arg2 == \"{attrNames[i]}\"");
                    scriptRead.AppendLine($" || arg2 == \"{attrNames[i]}\"");
                }
                scriptWrite.AppendLine("){");
                scriptRead.AppendLine("){");

                if (property.PropertyType == typeof(string))
                    scriptWrite.AppendLine(@$"arg1.{property.Name} = ObjectToValue.ToString(arg3);return;}}");
                else if (property.PropertyType == typeof(double?))
                    scriptWrite.AppendLine(@$"arg1.{property.Name} = ObjectToValue.ToDouble(arg3);return;}}");
                else if (property.PropertyType == typeof(bool?))
                    scriptWrite.AppendLine(@$"arg1.{property.Name} = ObjectToValue.ToBoolean(arg3);return;}}");

                scriptRead.AppendLine(@$"return arg1.{property.Name}; }}");
            }
        }

        var className = $"N{Guid.NewGuid():n}";
        // 关键:使用 GetDevelopName() 处理复杂类型
        assemblyCSharp.Add(@$"public static class {className}{{
    public static void WriteMethod({type.GetDevelopName()} arg1, string arg2, object? arg3){{{scriptWrite}}}
    public static object? ReadMethod({type.GetDevelopName()} arg1, string arg2){{{scriptRead}else{{ return null;}}}}
}}");

        var assembly = assemblyCSharp.GetAssembly();
        Setter = assembly.GetDelegateFromShortName<Action<T, string, object?>>(className, "WriteMethod");
        Getter = assembly.GetDelegateFromShortName<Func<T, string, object?>>(className, "ReadMethod");
    }

    public readonly static Action<T, string, object?> Setter;
    public readonly static Func<T, string, object?> Getter;
}

public static class ClassOperator
{
    public static void Setter<T>(T obj, string name, object? value)
    {
        ClassOperator<T>.Setter(obj, name, value);
    }
    public static object? Getter<T>(T obj, string name)
    {
        return ClassOperator<T>.Getter(obj, name);
    }
}
```

### 14.3 使用示例

```csharp
public class ProductModel
{
    [EHeader("产品编号", "ProductID", "ID")]
    public int? ProductId { get; set; }

    [EHeader("产品名称", "ProductName", "Name")]
    public string Name { get; set; }

    [EHeader("价格", "Price", "单价")]
    public double? Price { get; set; }

    [EHeader("是否在售", "Available", "在售")]
    public bool? IsAvailable { get; set; }
}

// 使用动态映射
var product = new ProductModel();

// 写入值 - 使用编译期优化的委托
ClassOperator.Setter(product, "产品编号", 1001);
ClassOperator.Setter(product, "产品名称", "笔记本电脑");
ClassOperator.Setter(product, "价格", 5999.99);
ClassOperator.Setter(product, "是否在售", true);

// 读取值 - 使用编译期优化的委托
var id = ClassOperator.Getter(product, "ProductID");      // 1001
var name = ClassOperator.Getter(product, "ProductName");   // "笔记本电脑"
var price = ClassOperator.Getter(product, "Price");       // 5999.99
var available = ClassOperator.Getter(product, "Available"); // true

Console.WriteLine($"产品: {name}, 编号: {id}, 价格: {price}");
```

**性能优势:**
- **编译期优化**:if-else 树在编译期生成,而非运行时反射
- **委托缓存**:静态构造器只编译一次,后续直接调用委托
- **类型安全**:编译期检查类型,避免运行时错误
- **多别名支持**:通过 `[EHeader]` 特性支持多个字段名映射

**GetDevelopName() 的关键作用:**
- 正确处理泛型类型:如 `List<double?>` → `System.Collections.Generic.List<System.Nullable<System.Double>>`
- 正确处理可空类型:如 `int?` → `System.Nullable<System.Int32>`
- 避免反引号等特殊符号导致编译失败

---

## 模式 15：MethodCreator 扩展（最简洁的动态委托）

`DotNetCore.Natasha.CSharp.Extension.MethodCreator` 扩展包提供了最简洁的动态委托生成 API，两行代码搞定动态方法。

**核心优势：**
- 自动生成随机类名和方法签名
- 自动根据委托类型生成参数 `arg1, arg2...`
- 自动拼接类型名称（调用 `GetDevelopName()`）
- 支持智能模式和精简模式

### 智能模式（自动管理元数据）

```csharp
// 引入扩展包后，两行代码搞定
string script = "return arg1 + arg2 + 0.1;";
var func = script.ToFunc<double, double, double>();

Console.WriteLine(func(3.0, 5.0));  // 8.1
```

### 精简模式（自己指定元数据）

```csharp
// 需要自己指定依赖的类型
var func = "return Math.Floor(arg1 / 0.3);"
    .WithMetadata(typeof(Math))
    .ToFunc<double, double>();

Console.WriteLine(func(1.0));  // 3
```

### 完整 API 示例

```csharp
// Action 示例（无返回值）
"Console.WriteLine($\"Hello, {arg1}!\");"
    .ToAction<string>();

// Func 示例（有返回值）
"return arg1 * arg2;"
    .ToFunc<int, int, int>();

// 异步方法
"await Task.Delay(arg1); return arg1 * 2;"
    .ToAsyncDelegate<Func<int, Task<int>>>();

// unsafe 方法
"return arg1 * 2;"
    .ToUnsafeDelegate<Func<int, int>>();

// 访问私有成员
var accessor = "return arg1._secretField;"
    .WithSmartMethodBuilder()
    .WithPrivateAccess(myObject)  // 传入需要访问私有成员的对象
    .ToDelegate<Func<MyClass, int>>();

// 排除特定 using
"File.WriteAllText(\"test.txt\", arg1);"
    .WithoutUsings("System.IO")  // 排除 System.IO 的 using
    .ToAction<string>();
```

### WithSmartMethodBuilder vs WithSlimMethodBuilder

| 模式 | 说明 | 是否需要预热 |
|------|------|-------------|
| `WithSmartMethodBuilder()` | 使用 Smart 模式，自动合并域的元数据和 using | 需要 |
| `WithSlimMethodBuilder()` | 使用 Simple 模式，自己管理元数据 | 不需要 |

**内部原理：**
```csharp
// 源码简化版
public T ToDelegate<T>(string modifier = "") where T : Delegate
{
    var className = $"N{Guid.NewGuid():N}";
    var methodInfo = typeof(T).GetMethod("Invoke")!;

    // 自动获取返回类型
    var returnTypeScript = methodInfo.ReturnType.GetDevelopName();
    var parameterScript = new StringBuilder();

    // 自动生成参数列表 arg1, arg2...
    var methodParameters = methodInfo.GetParameters();
    for (int i = 0; i < methodParameters.Length; i++)
    {
        var paramType = methodParameters[i].ParameterType;
        Builder.ConfigLoadContext(ctx => ctx.AddReferenceAndUsingCode(paramType));
        parameterScript.Append($"{paramType.GetDevelopName()} arg{i + 1},");
    }

    // 拼接完整脚本
    var fullScript = $"public static class {className} {{ public static {modifier} {returnTypeScript} Invoke({parameterScript}){{ {Script} }} }}";
    Builder.Add(fullScript);
    var asm = Builder.GetAssembly();
    var type = asm.GetType(className);
    return (T)Delegate.CreateDelegate(typeof(T), type.GetMethod("Invoke")!);
}
```

---

## 模式 16：CompileDirector 扩展（自适应编译学习）

`DotNetCore.Natasha.CSharp.Extension.CompileDirector` 扩展包提供了编译"学习"机制，适合重复编译相似脚本的场景（如规则引擎、表达式计算器）。

**核心思想：**
- 编译成功后，对"有用"的 using code 计数
- 超过采样阈值后，using code 被"录用"进缓存
- 后续编译自动优先使用缓存的 using code
- 编译失败时按策略重试

```csharp
// 引入扩展包
// dotnet add package DotNetCore.Natasha.CSharp.Extension.CompileDirector

// 创建编译导演，传入采样阈值（默认2）
CompileDirector director = new CompileDirector(3);

// 配置编译单元
director.ConfigBuilder(builder => builder
    .ConfigSyntaxOptions(opt => opt.WithPreprocessorSymbols("DEBUG"))
    .WithDebugCompile()
    .ConfigLoadContext(ctx => ctx
        .AddReferenceAndUsingCode<object>()
        .AddReferenceAndUsingCode(typeof(Math))
        .AddReferenceAndUsingCode(typeof(File))));

// 第一次编译
var builder1 = director.CreateBuilder();
builder1.Add(@"
    public static class A {
        public static void Show() {
            File.WriteAllText(""1.txt"", ""1"");
            Console.WriteLine(Math.Abs(-4));
        }
    }");

// 获取程序集（自动学习 using code）
var asm = director.GetAssembly(builder1);
asm.GetDelegateFromShortName<Action>("A", "Show")!();

// 后续编译会自动使用缓存的 using code
var builder2 = director.CreateBuilder();
builder2.Add(@"
    public static class B {
        public static void Show() {
            File.WriteAllText(""2.txt"", ""2"");
            Console.WriteLine(Math.Sqrt(16));
        }
    }");

var asm2 = director.GetAssembly(builder2);
```

### 失败重试策略

```csharp
// 配置失败时的 using code 覆盖策略
director.ConfigUsingConverSrategy(strategy => {
    // 策略1：使用原始 using
    // 策略2：使用编译成功的 using
    // 策略3：使用最少的 using
});
```

### 适用场景

1. **规则引擎** - 每条规则编译一次，后续直接执行
2. **表达式计算器** - 类似的数学表达式反复计算
3. **动态脚本** - 用户脚本的重复执行

---

## 类型扩展方法工具箱

除了 `GetDevelopName()`，Natasha 还提供了其他实用的类型扩展方法：

```csharp
using Natasha.CSharp.Extension;

// 获取运行时可用的类型名（带简化版本）
typeof(Dictionary<string,List<int>>[]).GetRuntimeName();
// → "Dictionary<String,List<Int32>>[]"

// 获取开发时类型名（完整版本）
typeof(Dictionary<string,List<int>>[]).GetDevelopName();
// → "System.Collections.Generic.Dictionary<System.String,System.Collections.Generic.List<System.Int32>>[]"

// 获取泛型定义（不带类型参数）
typeof(Dictionary<string,List<int>>).GetDevelopNameWithoutFlag();
// → "System.Collections.Generic.Dictionary<,>"

// 获取可用作文件名的类型名
typeof(Dictionary<string,List<int>>[]).GetAvailableName();
// → "Dictionary_String_List_Int32____"

// 泛型类型绑定
var listOfInt = typeof(List<>).With(typeof(int));
// → List<int>

// 获取所有嵌套的泛型类型
typeof(Dictionary<string,List<int>>).GetAllGenericTypes();
// → [string, List<>, int]

// 判断是否实现某接口
typeof(Dictionary<string,int>).IsImplementFrom<IDictionary>();
// → true

// 判断是否为简单类型
typeof(int).IsSimpleType();    // → true
typeof(string).IsSimpleType(); // → true
typeof(List<int>).IsSimpleType(); // → false
```

### GetAvailableName() 的妙用

```csharp
// 动态生成文件名时使用
var typeName = typeof(Dictionary<string, int>).GetAvailableName();
// → "Dictionary_String_Int32_"

// 生成缓存文件
var cacheFile = $"{typeName}_cache.bin";

// 生成类型别名
var alias = $"My{typeName}";
// → "MyDictionary_String_Int32_"
```

---

## 程序集输出类型控制

Natasha 支持多种程序集输出模式，适用于不同的使用场景：

### 完整程序集（含实现）

```csharp
// 输出完整程序集（含私有成员）
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    .OutputAsFullAssembly()
    .Add("public class A { private int _value = 42; }");

var assembly = builder.GetAssembly();
// assembly 包含完整实现和私有成员
```

### 引用程序集（不含实现）

```csharp
// 输出引用程序集（不含私有成员，不加载到域）
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    .OutputAsRefAssembly()
    .WithFileOutput()  // 输出到文件
    .CompileWithoutAssembly();  // 不加载到域

// 等同于:
builder
    .OutputAsRefAssembly()
    .WithFileOutput()
    .CompileWithoutAssembly();
```

### 控制私有成员输出

```csharp
// 输出时包含私有成员
builder.WithPrivateMembers();

// 输出时不包含私有成员（默认）
builder.WithoutPrivateMembers();
```

### 典型使用场景

| 场景 | 输出模式 | 特点 |
|------|---------|------|
| 动态插件 | 完整程序集 | 包含实现，可独立运行 |
| 库扩展 | 引用程序集 | 只暴露 public API |
| 代码验证 | 不输出 | 只检查语法正确性 |

---

这些模式可以直接应用到实际项目中,针对不同的业务需求进行调整。

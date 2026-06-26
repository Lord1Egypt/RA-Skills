# Natasha 编译错误处理完整指南

本文档提供 Natasha 编译错误处理的完整示例和最佳实践。

---

## 核心概念

### 动态编译的完整周期

1. **解析代码字符串** - 将字符串转换为 C# 语法树
2. **生成语法树** - 构建 SyntaxTree 结构
3. **编译成程序集** - 调用 Roslyn 编译器生成 IL 代码
4. **加载程序集** - 通过 AssemblyLoadContext 加载到内存
5. **创建实例并调用方法** - 反射创建实例并执行方法

### 错误类型

Natasha 区分以下几种错误类型：

- **Syntax Error（语法错误）** - 代码不符合 C# 语法规则
- **Semantic Error（语义错误）** - 类型不匹配、成员不存在等
- **Compile Error（编译错误）** - 编译过程中失败

---

## 方案 1：基础错误处理（推荐）

### 使用事件监听 + GetException()

```csharp
using Natasha;

public static void Initialize()
{
    // 初始化 Natasha
    NatashaManagement
        .GetInitializer()
        .WithMemoryUsing()
        .WithMemoryReference()
        .Preheating<NatashaDomainCreator>();

    AssemblyCSharpBuilder builder = new();
    try
    {
        builder
            .UseRandomLoadContext()
            .UseSmartMode()
            .WithReleaseCompile();

        // 监听编译日志（可选）
        builder.LogCompilationEvent += (log) => 
        { 
            Console.WriteLine(log.ToString()); 
        };

        // 监听编译失败事件
        builder.CompileFailedEvent += (compilation, diagnostics) => 
        { 
            Console.WriteLine("语法通过，编译却失败了"); 
        };

        // 添加代码
        builder.Add("public class A{}");
        builder.Add("public class B{ public static void Show(){ Console.WriteLine(\"Hello World!\"); }}");
        builder.Add("public class C{ public int Sum(int i,int j){return i+j;} }");

        // 编译
        var newAssembly = builder.GetAssembly();
        Console.WriteLine("编译成功！");

        // 使用编译后的代码
        var hwAction = newAssembly.GetDelegateFromShortName<Action>("B", "Show");
        hwAction();
    }
    catch (Exception ex)
    {
        // 获取 Natasha 异常
        var natashaEx = builder.GetException();

        if (natashaEx.ErrorKind == NatashaExceptionKind.Syntax)
        {
            // 语法错误：输出格式化代码和错误信息
            Console.WriteLine("==== 语法错误 ====");
            Console.WriteLine(natashaEx!.Formatter);
            
            foreach (var item in natashaEx.Diagnostics)
            {
                Console.WriteLine(item.ToString());
            }
        }
        else if (natashaEx.ErrorKind == NatashaExceptionKind.Compile)
        {
            // 编译错误
            Console.WriteLine("==== 编译错误 ====");
            Console.WriteLine(natashaEx.Message);
        }
    }
}
```

### 测试语法错误

```csharp
// 语法错误示例：void 方法不能返回值
builder.Add("public class D{ public void Sum(int i,int j){return i+j;} }");

// 这会触发 SyntaxError
```

### 测试语义错误

```csharp
// 语义错误示例：括号不匹配
builder.Add("public class E{ public static void Show(){ Console.WriteLine(\"Hello World!\"); }");

// 这会触发 SemanticError
```

---

## 方案 2：高级错误处理（使用内部 API）

### 使用 GetNatashaLog() 获取友好错误信息

**注意：** `GetNatashaLog()` 是内部 API（Internal），未公开给外部使用。但可以推荐给需要更友好错误处理的使用者。

**源码位置：**
- 实现位置：`G:\Project\OpenSource\Natasha\src\Natasha.CSharp\Natasha.CSharp.Compiler\Extension\Inner\CSharpCompilationExtension.cs`
- 单元测试：`G:\Project\OpenSource\Natasha\test\ut\Compile\MemAssembly\LogInfo`

```csharp
using Natasha;
using Natasha.CSharp.Extension.Inner;

public static void AdvancedErrorHandling()
{
    AssemblyCSharpBuilder builder = new();
    builder
        .UseRandomLoadContext()
        .UseSmartMode();

    NatashaCompilationLog? log = null;

    // 监听编译失败事件
    builder.CompileFailedEvent += (compilation, errors) => {
        log = compilation.GetNatashaLog();
    };

    // 监听编译成功事件（可选）
    builder.CompileSucceedEvent += (compilation, errors) => {
        log = compilation.GetNatashaLog();
    };

    try
    {
        // 语法错误示例
        builder.Add(@"
            public class A{
                public void Show(){
                    return 1;
                }
            }
        ");
        
        var assembly = builder.GetAssembly();
    }
    catch (Exception ex)
    {
        // 打印友好的错误信息
        if (log != null)
        {
            Console.WriteLine(log.ToString());
        }
    }
}
```

### 错误信息格式示例

**语法错误输出：**
```
============================== ERROR : ee79d3e2b027491f93705a4098568bc8 ==============================

------------------------------------------------------------------------------------------------------

1	public class A
2	{
3	    public void Show()
4	    {
5	        return 1;
6	    }
7	}


第5行，第8个字符： 内容【return】  由于"A.Show()"返回 void，返回关键字后面不得有对象表达式


------------------------------------------------------------------------------------------------------

    Time     :	{{TIME}}

    Language :	C# & Preview

    TreeCount:	共 1 个

    RefCount :	共 1 个

------------------------------------------------------------------------------------------------------

======================================================================================================
```

**编译成功输出：**
```
============================== SUCCEED : c44bdae4ce064a4fab6d1d7865ef0754 ==============================

------------------------------------------------- A -------------------------------------------

1       public class A
2       {
3           public void Show()
4           {
5           }
6       }


------------------------------------------------------------------------------------------------------

    Time     :  2024-05-04 12:12:01

    Language :  C# & Preview

    TreeCount:  共 1 个

    RefCount :  共 2 个

------------------------------------------------------------------------------------------------------

======================================================================================================
```

---

## 错误处理最佳实践

### 1. 区分错误类型

```csharp
var natashaEx = builder.GetException();

switch (natashaEx.ErrorKind)
{
    case NatashaExceptionKind.Syntax:
        Console.WriteLine("语法错误");
        break;
    case NatashaExceptionKind.Compile:
        Console.WriteLine("编译错误");
        break;
    case NatashaExceptionKind.Reference:
        Console.WriteLine("引用错误");
        break;
    case NatashaExceptionKind.Using:
        Console.WriteLine("Using 错误");
        break;
}
```

### 2. 使用事件监听

```csharp
// 监听编译日志
builder.LogCompilationEvent += (log) => {
    // 记录日志
    logger.Info(log.ToString());
};

// 监听编译失败
builder.CompileFailedEvent += (compilation, diagnostics) => {
    // 获取详细错误信息
    var log = compilation.GetNatashaLog();
    logger.Error(log.ToString());
};

// 监听编译成功
builder.CompileSucceedEvent += (compilation, diagnostics) => {
    var log = compilation.GetNatashaLog();
    logger.Info($"编译成功: {log}");
};
```

### 3. 获取完整编译日志（GetFullLog）

除了事件监听，还可以在 catch 块中直接获取完整编译日志：

```csharp
try
{
    builder.Add("public class A{ }");
    var assembly = builder.GetAssembly();
}
catch (Exception ex)
{
    // 方法1：获取完整编译日志（包含所有语法树和诊断信息）
    string fullLog = builder.GetFullLog();
    Console.WriteLine(fullLog);

    // 方法2：通过异常对象获取
    var natashaEx = builder.GetException();
    Console.WriteLine(natashaEx.CompileMessage);  // 编译信息
}
```

**GetFullLog() vs CompileMessage：**
- `GetFullLog()` - 返回完整的编译日志，包含语法树、诊断详情
- `CompileMessage` - 返回简洁的编译结果摘要

### 3. 多脚本错误处理

```csharp
try
{
    builder.Add("public class A{ }");
    builder.Add("public class B{ }");
    builder.Add("public class C{ }");
    
    var assembly = builder.GetAssembly();
}
catch (Exception ex)
{
    var natashaEx = builder.GetException();
    
    // Diagnostics 会包含所有脚本的错误
    foreach (var diagnostic in natashaEx.Diagnostics)
    {
        Console.WriteLine(diagnostic.ToString());
    }
}
```

---

## 常见错误及解决方法

### 1. 语法错误

**错误示例：**
```csharp
// void 方法不能返回值
public void Show() {
    return 1;
}
```

**解决方法：**
- 将返回类型改为 `int`
- 或移除 `return` 语句

---

### 2. using 错误

**错误示例：**
```csharp
using abc;  // abc 命名空间不存在
```

**解决方法：**
- 添加正确的命名空间
- 使用 `WithMemoryUsing()` 自动引入常用命名空间

---

### 3. 引用错误

**错误示例：**
```csharp
// 缺少程序集引用
var list = new List<int>();
```

**解决方法：**
```csharp
builder.ConfigLoadContext(ctx => 
    ctx.AddReferenceAndUsingCode(typeof(List<>))
);
```

---

### 4. 类型错误

**错误示例：**
```csharp
public int Calculate() {
    return "hello";  // 类型不匹配
}
```

**解决方法：**
- 确保返回类型与实际返回值匹配
- 或修改返回类型

---

## 实际应用示例

### 示例 1：脚本引擎的错误处理

```csharp
public class ScriptEngine
{
    public object Execute(string script)
    {
        var builder = new AssemblyCSharpBuilder();
        builder.UseRandomLoadContext().UseSmartMode();
        
        NatashaCompilationLog? log = null;
        
        builder.CompileFailedEvent += (compilation, errors) => {
            log = compilation.GetNatashaLog();
        };
        
        try
        {
            builder.Add(script);
            var assembly = builder.GetAssembly();
            var type = assembly.GetTypes().First();
            var method = type.GetMethods().First(m => m.IsStatic && m.IsPublic);
            
            return method.Invoke(null, null);
        }
        catch (Exception ex)
        {
            if (log != null)
            {
                throw new ScriptExecutionException(
                    "脚本执行失败",
                    log.ToString(),
                    ex
                );
            }
            throw;
        }
    }
}

public class ScriptExecutionException : Exception
{
    public string ErrorLog { get; }
    
    public ScriptExecutionException(string message, string errorLog, Exception innerException)
        : base(message, innerException)
    {
        ErrorLog = errorLog;
    }
}
```

### 示例 2：批量编译的错误收集

```csharp
public class BatchCompiler
{
    public Dictionary<string, CompilationResult> CompileBatch(
        Dictionary<string, string> scripts)
    {
        var results = new Dictionary<string, CompilationResult>();
        
        foreach (var script in scripts)
        {
            var builder = new AssemblyCSharpBuilder(script.Key);
            builder.UseRandomLoadContext().UseSmartMode();
            
            NatashaCompilationLog? log = null;
            
            builder.CompileFailedEvent += (compilation, errors) => {
                log = compilation.GetNatashaLog();
            };
            
            try
            {
                builder.Add(script.Value);
                var assembly = builder.GetAssembly();
                
                results[script.Key] = new CompilationResult {
                    Success = true,
                    Assembly = assembly
                };
            }
            catch (Exception ex)
            {
                results[script.Key] = new CompilationResult {
                    Success = false,
                    ErrorLog = log?.ToString(),
                    Exception = ex
                };
            }
        }
        
        return results;
    }
}

public class CompilationResult
{
    public bool Success { get; set; }
    public Assembly Assembly { get; set; }
    public string ErrorLog { get; set; }
    public Exception Exception { get; set; }
}
```

---

## 总结

### 关键要点

1. **使用事件监听** - `CompileFailedEvent` 和 `CompileSucceedEvent` 获取编译结果
2. **区分错误类型** - 通过 `NatashaExceptionKind` 区分不同类型的错误
3. **使用内部 API** - `compilation.GetNatashaLog()` 获取最友好的错误格式
4. **完整错误信息** - 包含带行号的代码、错误位置、错误描述、编译元数据

### 错误信息包含

- ✅ 带行号的代码
- ✅ 错误位置（行号、字符位置）
- ✅ 错误内容片段
- ✅ 错误描述
- ✅ 编译元数据（时间、语言版本、语法树数量、引用数量）

### 推荐实践

- **生产环境**：使用 `GetException()` 和 `NatashaExceptionKind` 区分错误类型
- **开发调试**：使用 `GetNatashaLog()` 获取友好的错误格式
- **日志记录**：使用 `LogCompilationEvent` 记录完整的编译日志
- **用户提示**：将错误信息格式化后展示给用户，指出具体问题

---

## 参考资料

- Natasha 源码：`G:\Project\OpenSource\Natasha\src\Natasha.CSharp\Natasha.CSharp.Compiler\Extension\Inner\CSharpCompilationExtension.cs`
- 单元测试：`G:\Project\OpenSource\Natasha\test\ut\Compile\MemAssembly\LogInfo`
- 示例代码：`C:\Users\Administrator\Desktop\natasha demo.txt`

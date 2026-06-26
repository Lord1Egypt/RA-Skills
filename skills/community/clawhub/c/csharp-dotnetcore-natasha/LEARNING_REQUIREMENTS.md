# Natasha 技能学习需求

本文档记录了我对 Natasha 功能的探索需求,需要你的编码实现和讲解。

---

## 优先级 1：核心功能深度理解

### 需求 1.1：三种编译模式的性能对比
**目标**: 理解智能模式、精简模式、自定义编译模式的实际性能差异

**期望**:
1. 编写性能基准测试代码,对比三种模式的编译速度和运行时性能
2. 测试不同场景:简单类、复杂泛型、多依赖引用
3. 分析内存占用差异
4. 给出每种模式的最优使用场景建议

**疑问**:
- 内存程序集 vs 引用程序集,在什么性能指标上差异最明显?
- WithFileUsingCache 的实际加速效果是多少?
- 精简模式在什么情况下比智能模式更适合?

---

### 需求 1.2：动态编译的完整生命周期（✅ 已学习）

**动态编译的完整周期关键步骤：**
1. **解析代码字符串** - 将字符串转换为 C# 语法树
2. **生成语法树** - 构建 SyntaxTree 结构
3. **编译成程序集** - 调用 Roslyn 编译器生成 IL 代码
4. **加载程序集** - 通过 AssemblyLoadContext 加载到内存
5. **创建实例并调用方法** - 反射创建实例并执行方法

**编译错误友好处理方案：**

#### 方案 1：使用事件监听（推荐）

```csharp
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode();

// 监听编译日志
builder.LogCompilationEvent += (log) => {
    Console.WriteLine(log.ToString());
};

// 监听编译失败事件
builder.CompileFailedEvent += (compilation, diagnostics) => {
    Console.WriteLine("语法通过，编译却失败了，此时你要做什么");
};

try {
    builder.Add("public class A{}");
    var assembly = builder.GetAssembly();
}
catch (Exception ex) {
    var natashaEx = builder.GetException();

    if (natashaEx.ErrorKind == NatashaExceptionKind.Syntax) {
        // 语法错误
        Console.WriteLine(natashaEx!.Formatter);
        foreach (var item in natashaEx.Diagnostics) {
            Console.WriteLine(item.ToString());
        }
    }
}
```

#### 方案 2：使用内部 API（获取最友好的错误信息）

**注意：** `GetNatashaLog()` 是内部 API，未公开，但可以推荐给需要更友好错误处理的使用者。

**源码位置：**
- 实现位置：`G:\Project\OpenSource\Natasha\src\Natasha.CSharp\Natasha.CSharp.Compiler\Extension\Inner\CSharpCompilationExtension.cs`
- 单元测试：`G:\Project\OpenSource\Natasha\test\ut\Compile\MemAssembly\LogInfo`

**使用方法：**

```csharp
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode();

// 监听编译成功/失败事件
NatashaCompilationLog? log = null;

builder.CompileFailedEvent += (compilation, errors) => {
    log = compilation.GetNatashaLog();
};

builder.CompileSucceedEvent += (compilation, errors) => {
    log = compilation.GetNatashaLog();
};

try {
    builder.Add("public class A{}");
    var assembly = builder.GetAssembly();
}
catch (Exception ex) {
    // 打印友好的错误信息
    if (log != null) {
        Console.WriteLine(log.ToString());
    }
}
```

**错误信息格式示例：**

**语法错误：**
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

**编译成功：**
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

**错误处理最佳实践总结：**

1. **使用事件监听** - `CompileFailedEvent` 和 `CompileSucceedEvent` 获取编译结果
2. **区分错误类型** - 通过 `NatashaExceptionKind` 区分语法错误、编译错误等
3. **使用内部 API** - `compilation.GetNatashaLog()` 获取最友好的错误格式
4. **错误信息包含**：
   - 带行号的代码
   - 错误位置（行号、字符位置）
   - 错误内容片段
   - 错误描述
   - 编译元数据（时间、语言版本、语法树数量、引用数量）

**已完成的疑问解答：**
- ✅ 编译失败时，如何获取详细的错误信息？→ 使用 `GetNatashaLog()` 或监听 `CompileFailedEvent`
- ✅ 错误信息如何友好展示？→ `GetNatashaLog()` 自动格式化带行号的代码和错误位置

**待解答的疑问：**
- 多次编译相同代码,是否会自动缓存?
- 如何避免内存泄漏?何时应该手动卸载程序集?

---

## 优先级 2：高级特性探索

### 需求 2.1：私有成员访问的最佳实践（✅ 已学习）

**核心 API：**
- `ConfigCompilerOption(opt => opt.AppendCompilerFlag(CompilerBinderFlags.IgnoreAccessibility))` - 忽略可访问性检查
- `ConfigCompilerOption(opt => opt.WithAllMetadata())` - 包含所有元数据（私有、内部、公共）
- `ConfigCompilerOption(opt => opt.WithInternalMetadata())` - 仅包含内部和公共元数据
- `ConfigCompilerOption(opt => opt.WithPublicMetadata())` - 仅包含公共元数据
- `code.ToAccessPrivateTree(typeof(TargetType))` - 将代码字符串转换为可访问私有成员的语法树

**使用场景和限制：**

#### 场景 1：访问所有成员（私有 + 内部 + 公共）

```csharp
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

builder.Add(code.ToAccessPrivateTree(typeof(AccessModelTest)));
var asm = builder.GetAssembly();

// 测试访问私有成员
var privateFunc = asm.GetDelegateFromShortName<Func<string>>("A", "GetPrivate");
Assert.Equal("Private", privateFunc());

var internalFunc = asm.GetDelegateFromShortName<Func<string>>("A", "GetInternal");
Assert.Equal("Internal", internalFunc());

var publicFunc = asm.GetDelegateFromShortName<Func<string>>("A", "GetPublic");
Assert.Equal("Public", publicFunc());
```

#### 场景 2：仅访问内部和公共成员

```csharp
builder
    .ConfigCompilerOption(opt => opt
        .AppendCompilerFlag(CompilerBinderFlags.IgnoreAccessibility)
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
```

**限制：** 如果尝试访问私有成员，会抛出 `CS1061` 错误。

#### 场景 3：仅访问公共成员

```csharp
builder
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
```

**限制：** 如果尝试访问私有或内部成员，会抛出 `CS1061` 错误。

**已完成的疑问解答：**
- ✅ 访问私有成员时，如何处理嵌套类的私有成员？→ 使用 `ToAccessPrivateTree(typeof(NestedClass))` 处理嵌套类
- ✅ 能否访问基类的私有成员？→ 可以，只要基类的元数据被包含（`WithAllMetadata()`）
- ✅ 动态生成的代码能否绕过安全检查？→ 通过 `IgnoreAccessibility` 标志可以，但有元数据级别限制
- ✅ 如何处理不同的元数据级别？→ 使用 `WithAllMetadata()` / `WithInternalMetadata()` / `WithPublicMetadata()` 控制

**使用建议：**
1. **性能关键路径** - 避免反射开销，直接访问私有成员
2. **测试场景** - 访问被测类的内部状态
3. **框架开发** - 需要访问库内部状态的情况
4. **安全风险** - 访问私有成员可能破坏封装性，谨慎使用

---

### 需求 2.2：重复编译优化的实际效果（✅ 已学习）

**核心方法：**
```csharp
public AssemblyCSharpBuilder Reset()
{
    WithPreCompilationOptions();      // 复用编译选项
    WithPreCompilationReferences();    // 复用元数据引用
    return this;
}
```

**重复编译的逻辑：**
1. `WithPreCompilationOptions()` - 阻止创建新的编译选项
2. `WithPreCompilationReferences()` - 阻止覆盖新的引用
3. **优化效果**：省去了创建 `AssemblyCSharpBuilder` 的时间，只重新解析语法树

**使用注意事项：**

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

// 第二次编译 - 复用之前的编译选项和引用
builder.Clear();
builder.WithRandomAssenblyName().Add("public class Script2 { public int Run() => 2; }");
var asm2 = builder.GetAssembly();
```

**重要提示：**

1. **文件名处理**
   - 如果已存在 `a.dll`，会生成 `repeat.guid.a.dll`
   - 使用 `WithForceCleanFile()` 强制清除已存在文件
   - 使用 `WithoutForceCleanFile()` 让 `a.dll` 被换成 `repeat.guid.a.dll`

2. **需要重新设置的配置**
   - 若之前使用了 `ConfigEmitOptions()`，需要重新配置
   - 必须指定新的程序集名
   - 若需要指定新的域

3. **推荐用法（不太建议重复编译）**
   - 根据源码注释，重复编译优化的实际效果有限
   - 更推荐缓存编译后的委托或程序集
   - 对于热重载场景，可以考虑使用，但要注意清理旧程序集

**已完成的疑问解答：**
- ✅ 重复编译时，哪些部分被复用了？→ 编译选项和元数据引用，代码需要重新解析
- ✅ 在什么规模的代码量下，优化效果最明显？→ 源码注释表明效果有限，不太建议使用
- ✅ 与缓存委托的方式相比，哪个更优？→ **缓存委托更优**，重复编译只是省去 Builder 创建时间

**最佳实践建议：**
- ✅ **推荐**：缓存编译后的委托或程序集
- ⚠️ **谨慎使用**：重复编译优化（`Reset()` 方法）
- ❌ **不推荐**：频繁使用 `Reset()` 进行批量编译

---

## 优先级 3：实战场景扩展

### 需求 3.1：AOP 框架实现
**目标**: 用 Natasha 实现一个轻量级 AOP 框架

**期望**:
1. 实现方法拦截功能(前置、后置、环绕)
2. 支持特性标记切点(如 [Log]、[Cache])
3. 支持异步方法拦截
4. 对比静态织入 vs 动态代理的性能

**疑问**:
- 如何生成继承自原始类的代理类?
- 如何处理泛型方法的拦截?
- 如何保持原始类型的兼容性?

---

### 需求 3.2：表达式编译器的完整实现
**目标**: 实现一个支持复杂表达式的编译器

**期望**:
1. 支持运算符: +, -, *, /, %, ==, !=, >, <, >=, <=
2. 支持逻辑运算: &&, ||, !
3. 支持成员访问: obj.Property, obj.Method()
4. 支持集合操作: List 的索引访问、Linq 方法调用
5. 提供错误提示和调试信息

**疑问**:
- 如何解析复杂的嵌套表达式?
- 如何处理类型推导和类型转换?
- 如何优化生成的代码性能?

---

### 需求 3.3：动态代理生成
**目标**: 实现类似 Castle DynamicProxy 的功能

**期望**:
1. 动态生成接口的代理实现
2. 拦截接口方法的调用
3. 支持多个拦截器的链式调用
4. 保持原始接口的类型安全

**疑问**:
- 如何为接口动态生成实现类?
- 如何处理接口的泛型方法?
- 如何支持接口继承?

---

## 优先级 4：性能优化和最佳实践

### 需求 4.1：委托缓存的最佳模式
**目标**: 探索委托缓存的多种实现方式

**期望**:
1. 对比不同缓存策略:静态字典、ConcurrentDictionary、MemoryCache
2. 测试缓存的命中率、内存占用、并发性能
3. 展示缓存的过期和清理机制
4. 给出最佳实践建议

**疑问**:
- 什么时候应该缓存?什么时候不应该缓存?
- 如何避免缓存键的冲突?
- 如何处理类型版本变化导致的缓存失效?

---

### 需求 4.2：元数据管理的内存优化
**目标**: 理解如何最小化动态编译的内存占用

**期望**:
1. 分析不同预热方式的内存占用
2. 展示如何卸载不需要的程序集
3. 对比一次性编译 vs 按需编译的内存差异
4. 给出大型项目的内存优化建议

**疑问**:
- UseNewLoadContext vs UseRandomLoadContext,哪个更适合长期运行?
- 如何检测内存泄漏?
- WeakReference 能否用于缓存委托?

---

## 优先级 5：边界情况和错误处理

### 需求 5.1：复杂类型的动态代码生成
**目标**: 测试 Natasha 对各种复杂类型的处理能力

**期望**:
1. 多维数组: `int[,,]`, `int[][][]`
2. 嵌套泛型: `Dictionary<List<int[]>, Task<string>>`
3. 指针类型: `int*`, `void*`
4. 函数指针: `delegate* unmanaged[int]`
5. ref struct 和 Span
6. 可空引用类型: `string?`

**疑问**:
- 哪些类型 Natasha 无法处理?
- 如何处理类型中的特殊字符?
- 跨程序集引用复杂类型时会有什么问题?

---

### 需求 5.2：编译错误的友好处理
**目标**: 提供清晰的错误提示和调试信息

**期望**:
1. 捕获编译错误并提取详细信息:行号、错误代码、错误描述
2. 生成友好的错误提示,指出具体问题
3. 提供代码高亮的错误定位
4. 展示常见错误及其解决方法

**疑问**:
- 如何定位动态生成代码中的错误行号?
- 如何处理递归依赖导致的编译失败?
- 如何提供代码补全和 IntelliSense?

---

## 优先级 6：与其他技术的集成

### 需求 6.1：与 Roslyn 的协作
**目标**: 理解 Natasha 与 Roslyn 的关系和互补性

**期望**:
1. 展示如何结合 Roslyn 的代码分析能力
2. 使用 Roslyn 进行语法检查和代码格式化
3. 展示如何利用 Roslyn 的符号信息
4. 说明 Natasha 和 Roslyn 各自的优势

**疑问**:
- Natasha 内部是否使用了 Roslyn?
- 能否直接使用 Roslyn 的 Compilation API?
- Roslyn 的 SourceGenerator 与 Natasha 的动态编译,如何选择?

---

### 随想记录

这些需求基于我对 Natasha 的理解和常见场景,可能有不准确或重复的地方,请你根据实际情况调整优先级和实现方案。

我特别关注:
- 性能优化的实际效果和量化指标
- 最佳实践的总结和边界情况的处理
- 与传统反射方式的对比
- 在大型项目中的应用经验

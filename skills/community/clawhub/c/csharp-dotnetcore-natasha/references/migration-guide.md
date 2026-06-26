# 从已废弃 API 迁移指南

## 概述

Natasha 库已经停止维护 `Natasha.CSharp.Template` 包和 `NDelegate` 高级 API。所有新代码应该使用 `AssemblyCSharpBuilder` 直接方式。

本文档帮助开发者从旧 API 迁移到现代方式。

## 旧 API vs 新 API 对比

| 功能 | 旧方式（已废弃） | 新方式（推荐） |
|-----|-----------------|----------------|
| **初始化** | `NatashaManagement.RegistDomainCreator()` | `GetInitializer().WithMemoryUsing().WithMemoryReference().Preheating<NatashaDomainCreator>()` |
| **编译** | `NDelegate.RandomDomain()` | `new AssemblyCSharpBuilder().UseRandomLoadContext()` |
| **类生成** | `NClass`, `FastClassOperator` | 直接字符串代码 + `AssemblyCSharpBuilder` |
| **方法生成** | `NMethod`, `FastMethodOperator` | 直接字符串代码 + `AssemblyCSharpBuilder` |
| **委托获取** | `NDelegate.GetDelegateFromShortName()` | `Assembly.GetDelegateFromShortName<T>()` |

## 迁移示例

### 迁移 1：基础编译

#### ❌ 旧代码（已废弃）

```csharp
using Natasha;
using Natasha.CSharp;

var func = NDelegate
    .RandomDomain()
    .UseSmartMode()
    .Add("public class Calc { public static int Add(int a, int b) => a + b; }")
    .GetDelegateFromShortName<Func<int, int, int>>("Calc", "Add");

int result = func(3, 5);
```

**问题：**
- `NDelegate` 已准备放弃
- `RandomDomain()` 方法已过时
- 代码难以维护

#### ✅ 新代码（推荐）

```csharp
using Natasha;
using Natasha.CSharp;

// 初始化（应用启动时一次）
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()
    .WithMemoryReference()
    .Preheating<NatashaDomainCreator>();

// 编译
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    .Add("public class Calc { public static int Add(int a, int b) => a + b; }");

var assembly = builder.GetAssembly();
var func = assembly.GetDelegateFromShortName<Func<int, int, int>>("Calc", "Add");

int result = func(3, 5);
```

### 迁移 2：类生成

#### ❌ 旧代码（已废弃）

```csharp
using Natasha.CSharp.Template;

var nclass = new NClass();
nclass.Name = "Person";
nclass.Namespace = "MyNamespace";

nclass.Property(p => p.Name = "Name").PropertyType = "string";
nclass.Property(p => p.Name = "Age").PropertyType = "int";

var method = nclass.Method();
method.Name = "Greet";
method.ReturnType = "string";
method.Body = "return $\"Hello, {Name}\";";

var type = nclass.GetType();
```

**问题：**
- 使用已废弃的 `Natasha.CSharp.Template` 包
- 流式 API 繁琐不直观
- 难以维护和扩展

#### ✅ 新代码（推荐）

```csharp
using Natasha;
using Natasha.CSharp;

// 初始化
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()
    .WithMemoryReference()
    .Preheating<NatashaDomainCreator>();

// 编译
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    .Add(@"
        namespace MyNamespace {
            public class Person {
                public string Name { get; set; }
                public int Age { get; set; }
                
                public string Greet() {
                    return $""Hello, {Name}"";
                }
            }
        }
    ");

var assembly = builder.GetAssembly();
var type = assembly.GetTypeFromShortName("Person");
```

**优点：**
- 直接使用 C# 代码字符串
- 更直观和易于理解
- 利用 IDE 智能提示和检查
- 完全控制生成的代码

### 迁移 3：私有成员访问

#### ❌ 旧代码（已废弃）

```csharp
using Natasha.CSharp.Template;

var method = new FastMethodOperator();
method.Name = "GetSecret";
method.ReturnType = "int";
method.Body = "return obj._secret;";

var delegateFunc = method
    .UseRandomDomain()
    .AllowPrivate<MyModel>()  // 旧 API
    .GetMethod<Func<MyModel, int>>();
```

#### ✅ 新代码（推荐）

```csharp
using Natasha;
using Natasha.CSharp;

// 初始化
NatashaManagement
    .GetInitializer()
    .WithMemoryUsing()
    .WithMemoryReference()
    .Preheating<NatashaDomainCreator>();

// 编译
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    .ConfigCompilerOption(opt => opt
        .AppendCompilerFlag(IgnoreAccessibility)
        .WithAllMetadata()
    )
    .ToAccessPrivateTree(typeof(MyModel))
    .Add(@"
        public class PrivateAccessor {
            public static int GetSecret(MyModel obj) {
                return obj._secret;
            }
        }
    ");

var assembly = builder.GetAssembly();
var delegateFunc = assembly.GetDelegateFromShortName<Func<MyModel, int>>(
    "PrivateAccessor", "GetSecret"
);
```

## 常见迁移问题

### Q1: 我有大量使用 NClass 的代码怎么办？

**A:** 逐步迁移：
1. 从使用最少的地方开始
2. 转换为直接字符串代码 + `AssemblyCSharpBuilder`
3. 测试确保功能相同
4. 逐步推进到所有代码

### Q2: 旧 API 还能用吗？

**A:** 不推荐。虽然可能还能编译，但：
- `Natasha.CSharp.Template` 不再维护
- Bug 不会被修复
- 新功能不会添加到旧 API
- 性能可能不如新方式

### Q3: 性能会变好吗？

**A:** 是的。新方式 (`AssemblyCSharpBuilder`)：
- 更直接，少了中间抽象层
- 编译速度通常更快
- 运行时性能相同或更好
- 内存占用更少

### Q4: NDelegate 什么时候会完全删除？

**A:** 
- 当前状态：准备放弃 (deprecated)
- 建议立即迁移以规避未来风险
- 在下一个主版本中可能会被移除

## 迁移检查清单

使用以下清单确保完整的迁移：

- [ ] 移除所有 `using Natasha.CSharp.Template` 引用
- [ ] 移除所有 `NClass` 使用
- [ ] 移除所有 `NMethod` 使用
- [ ] 移除所有 `FastClassOperator` 使用
- [ ] 移除所有 `FastMethodOperator` 使用
- [ ] 替换所有 `NDelegate.RandomDomain()` 为 `new AssemblyCSharpBuilder().UseRandomLoadContext()`
- [ ] 使用新的初始化方式 (`GetInitializer()` 链式)
- [ ] 所有代码使用 `AssemblyCSharpBuilder` 编译
- [ ] 测试确保功能没有回归
- [ ] 更新团队文档和代码审查标准

## 新旧 API 功能对照表

| 需求 | 旧方式 | 新方式 |
|-----|------|------|
| 生成简单类 | `NClass` | 字符串 + `AssemblyCSharpBuilder` |
| 生成方法 | `NMethod` | 字符串 + `AssemblyCSharpBuilder` |
| 生成委托 | `NDelegate` | `AssemblyCSharpBuilder` + `GetDelegateFromShortName<T>()` |
| 访问私有成员 | `NDelegate.AllowPrivate()` | `ConfigCompilerOption() + ToAccessPrivateTree()` |
| 随机域编译 | `RandomDomain()` | `UseRandomLoadContext()` |
| 初始化 | `RegistDomainCreator()` | `GetInitializer()` 链式 |

## 额外资源

- **新 API 完整指南**：参考 `natasha-csharp-dynamics` Skill 主文档
- **初始化方式**：参考 `initialization-patterns.md`
- **编译选项**：参考 `compiler-options.md`
- **加载上下文**：参考 `context-management.md`

---

**重要提示**：虽然旧代码可能在当前版本仍然工作，但强烈建议立即迁移，以确保长期兼容性和获得新方式带来的性能提升。

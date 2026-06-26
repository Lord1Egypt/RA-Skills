# Natasha SKILL.md 文件再次修正报告

**修正日期:** 2026-03-19  
**修正依据:** 官方 Natasha 项目源代码 (G:\Project\OpenSource\Natasha)  
**关键修正:** 澄清 `UseNewLoadContext()` vs `new NatashaDomain(key)` 的区别

---

## 重大认知修正

### 之前的错误理解 ❌

我在第一次核对时完全搞混了两个不同的概念：

1. **混淆了 LoadContext 和 Domain**
   - 错认为 Natasha 使用 "Domain"，实际 AssemblyCSharpBuilder 内部使用 "LoadContext"
   - LoadContext 在源代码中清晰可见：`NatashaLoadContext` 类型

2. **错误否定了 `UseNewLoadContext()` 方法**
   - 我说这个方法不存在 ❌
   - 实际上它**确实存在**，在 `NatashaAssemblyBuilderExtension.cs` 中明确定义 ✅

3. **混淆了两套不同的 API**
   - `AssemblyCSharpBuilder` 的方法：`UseRandomLoadContext()`, `UseNewLoadContext("name")`, `UseExistLoadContext()`
   - 域管理 API：`new NatashaDomain(key)`, `DomainManagement.Create()`, `DomainManagement.Get()`

---

## 正确的理解框架

### 层级关系

```
NatashaManagement (全局初始化)
    └── Domain Creator (创建域)
            └── NatashaLoadContext (编译时使用)
                    └── AssemblyCSharpBuilder (使用 LoadContext 编译)
                            ├── UseRandomLoadContext() ✅
                            ├── UseNewLoadContext("name") ✅
                            └── UseExistLoadContext() ✅

分离的域管理系统（用于插件）
    ├── new NatashaDomain(key)
    ├── DomainManagement.Create("name")
    └── DomainManagement.Get("name")
```

### 核心区别

| 功能 | AssemblyCSharpBuilder | Domain 系统 | 文件位置 |
|-----|----------------------|-----------|--------|
| 初始化 | 通过 NatashaManagement | 分离的 NatashaDomain | `Natasha.CSharp.Compiler` |
| 随机隔离 | `.UseRandomLoadContext()` | `DomainManagement.Random()` | `NatashaAssemblyBuilderExtension.cs` |
| 命名持久 | `.UseNewLoadContext("name")` | `new NatashaDomain(key)` / `DomainManagement.Create()` | `AssemblyCSharpBuilder.LoadContext.cs` |
| 重用已有 | `.UseExistLoadContext()` | `DomainManagement.Get("name")` | `NatashaAssemblyBuilderExtension.cs` |
| 使用场景 | **编译代码** | **插件管理** | - |

---

## 源代码验证

### 1. NuGet 包名称

**文件:** `G:\Project\OpenSource\Natasha\src\Natasha.CSharp\Component\Core\Natasha.CSharp.Compiler.Domain\Natasha.CSharp.Compiler.Domain.csproj`

```xml
<PackageId>DotNetCore.Natasha.CSharp.Compiler.Domain</PackageId>
```

✅ **所有包都以 `DotNetCore.` 为前缀**

### 2. UseNewLoadContext 方法

**文件:** `G:\Project\OpenSource\Natasha\src\Natasha.CSharp\Natasha.CSharp.Compiler\Extension\NatashaAssemblyBuilderExtension.cs` (第 109-113 行)

```csharp
public static AssemblyCSharpBuilder UseNewLoadContext(this AssemblyCSharpBuilder builder, 
    string domainName, NatashaUsingCache? usingCache = null)
{
    builder.LoadContext = DomainManagement.Create(domainName, usingCache);
    return builder;
}
```

✅ **方法确实存在，参数为 `domainName`**

### 3. 旧的 Domain 方法已标记为过时

**文件:** 同上 (第 52-56 行, 68-72 行, 83-87 行)

```csharp
[Obsolete("为了规范 API 命名，建议您使用 UseRandomLoadContext.", false)]
public static AssemblyCSharpBuilder UseRandomDomain(this AssemblyCSharpBuilder builder)
{ ... }

[Obsolete("为了规范 API 命名，建议您使用 UseNewLoadContext.", false)]
public static AssemblyCSharpBuilder UseNewDomain(this AssemblyCSharpBuilder builder, string domainName)
{ ... }
```

✅ **旧 API 仍可用但已标记为 `[Obsolete]`，新代码应使用 LoadContext API**

### 4. 官方示例代码

**文件:** `G:\Project\OpenSource\Natasha\samples\DebugSample\Program.cs` (第 52-53 行)

```csharp
assemblyCSharp
    .UseRandomLoadContext()
    .UseSmartMode()
```

✅ **官方示例使用 `UseRandomLoadContext()`，不使用 `UseRandomDomain()`**

---

## 最终修正清单

| 项目 | 第一版错误 | 最终正确 | 状态 |
|-----|---------|--------|------|
| NuGet 包名 | `Natasha.CSharp.Compiler.Domain` | `DotNetCore.Natasha.CSharp.Compiler.Domain` | ✅ 已修正 |
| 随机隔离 | ~~`UseRandomDomain()`~~ | `UseRandomLoadContext()` | ✅ 已修正 |
| 命名持久 | ❌ 否定方法存在 | ✅ `UseNewLoadContext("name")` | ✅ 已修正 |
| 重用已有 | ~~`UseExistLoadContext()`~~ | `UseExistLoadContext()` | ✅ 已修正 |
| 概念理解 | Domain = LoadContext | LoadContext ≠ Domain | ✅ 已澄清 |
| 插件系统 | 无说明 | `new NatashaDomain(key)` 专用于插件 | ✅ 已补充 |

---

## 关键教训

1. **必须查阅源代码**，不能只看文档
2. **注意 `[Obsolete]` 标记**，新旧 API 的区别
3. **LoadContext 和 Domain 是两套不同的系统**
   - LoadContext：用于 AssemblyCSharpBuilder 编译
   - Domain：用于插件系统和隔离
4. **官方示例最权威**，应该优先参考示例代码

---

## 修正文件

✅ **C:\Users\Administrator\Desktop\skills\Natasha\SKILL.md** (版本 2.0)

- 包名已更正为 `DotNetCore.Natasha.CSharp.Compiler.Domain`
- API 方法改为 `UseRandomLoadContext()`, `UseNewLoadContext()`, `UseExistLoadContext()`
- 补充了清晰的概念说明，区分 LoadContext 和 Domain
- 加入了对 `[Obsolete]` 旧 API 的说明
- 强调了插件系统使用 `new NatashaDomain(key)` 的场景

---

**修正完成时间:** 2026-03-19 11:30  
**核对方式:** 直接查阅官方源代码  
**可信度:** ⭐⭐⭐⭐⭐ (基于源代码验证)

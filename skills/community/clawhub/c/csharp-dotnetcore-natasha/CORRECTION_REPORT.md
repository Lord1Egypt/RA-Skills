# Natasha SKILL.md 文件核对报告

**核对日期:** 2026-03-19  
**核对人:** WorkBuddy AI  
**官方文档源:** G:\Project\OpenSource\Natasha.Docs  
**修正状态:** ✅ 已完成

---

## 核对概述

通过详细对比官方 Natasha 文档（G:\Project\OpenSource\Natasha.Docs）和引用项目代码，发现并修正了 SKILL.md 文件中的 **7 处关键错误**。

---

## 发现的错误与修正

### 错误 1️⃣ NuGet 包名称错误（最严重）

**位置:** Prerequisites 部分

**原始错误:**
```bash
# 错误的包名
dotnet add package DotNetCore.Natasha.CSharp.Compiler.Domain
dotnet add package DotNetCore.Natasha.Domain  # 错误的主包
```

**官方文档依据:**
- 文件: `G:\Project\OpenSource\Natasha.Docs\src\i18n\zh-Hans\docusaurus-plugin-content-docs\current\compile\index.md`
- 原文: 
  ```
  `DotNetCore.Natasha.CSharp.Compiler` Natasha 基础编译单元包
  `Natasha.CSharp.Compiler.Domain` 继承自 `DotNetCore.Natasha.Domain` 并实现了 `DotNetCore.Natasha.DynamicLoad.Base` 编译粘合接口包。
  ```

**修正后:**
```bash
# 正确的包名
dotnet add package DotNetCore.Natasha.CSharp.Compiler
dotnet add package Natasha.CSharp.Compiler.Domain
```

**解释:**
- `DotNetCore.Natasha.CSharp.Compiler` - 基础编译单元（必须）
- `Natasha.CSharp.Compiler.Domain` - 域实现包（已整合依赖，自动引入 `DotNetCore.Natasha.Domain`）
- `DotNetCore.Natasha.Domain` - 无需单独引入，已包含在上面的包中

---

### 错误 2️⃣ 初始化方法链式调用错误

**位置:** Core Workflow 第 1 步

**原始错误:**
```
"Use `GetInitializer()` chain-style initialization"
"Call `WithMemoryUsing()` and `WithMemoryReference()`"
```

**官方文档依据:**
- 文件: `G:\Project\OpenSource\Natasha.Docs\src\docs\compile\002-SmartMode-Full.md`（第 20-37 行）
- 正确的链式调用顺序：
  ```cs
  NatashaManagement
      .GetInitializer()
      .WithRefUsing()           // 可选：使用引用程序集中的命名空间
      .WithRefReference()       // 可选：使用引用程序集中的元数据
      .WithMemoryUsing()        // 使用内存中的命名空间
      .WithMemoryReference()    // 使用内存中的元数据
      .WithFileUsingCache()     // 可选：使用文件缓存
      .WithExcludeReferences()  // 可选：过滤元数据
      .Preheating<NatashaDomainCreator>();
  ```

**修正后:**
```
强调两种等效的初始化方式：
1. 注册 + 预热: NatashaManagement.RegistDomainCreator<NatashaDomainCreator>(); 
              NatashaManagement.Preheating(true, true);
2. 链式预热(V9+): NatashaManagement.GetInitializer()
                 .WithMemoryUsing()
                 .WithMemoryReference()
                 .Preheating<NatashaDomainCreator>();
```

---

### 错误 3️⃣ LoadContext API 方法名完全错误

**位置:** Core Workflow 第 2 步

**原始错误:**
```
"UseRandomLoadContext()" - ❌ 不存在
"UseNewLoadContext("name")" - ❌ 不存在
"UseExistLoadContext("name")" - ❌ 不存在
```

**官方文档依据:**
- 文件: `G:\Project\OpenSource\Natasha.Docs\src\docs\compile\001-Domain.md`
- Natasha 使用"域"概念，不是 "LoadContext"
- 正确的 API:
  - `UseRandomDomain()` - 创建随机隔离域
  - `new NatashaDomain(key)` - 创建持久命名域
  - `DomainManagement.Create("name")` - 通过管理类创建域
  - `DomainManagement.Get("name")` - 获取已存在的域

**修正后:**
```
- Random domain: UseRandomDomain()
- Persistent domain: new NatashaDomain(key) + builder methods
- Shared domain: DomainManagement.Create("name") / DomainManagement.Get("name")
```

---

### 错误 4️⃣ Load Context Management 部分完全重写

**位置:** "Load Context Management" 部分

**原始错误:**
```
- UseRandomLoadContext()
- UseNewLoadContext("name")
- UseExistLoadContext("name")
```

**修正原因:**
这些 API 根本不存在。Natasha 使用的是"域"管理，而不是 LoadContext。

**修正后:**
```
- **Random domain** (`UseRandomDomain()`): 新隔离域
- **Persistent domain** (`new NatashaDomain(key)` + builder methods): 持久重用
- **Shared domain** (`DomainManagement.Create()` / `DomainManagement.Get()`): 跨程序集引用
```

---

### 错误 5️⃣ Best Practices 中 LoadContext 错误

**位置:** Best Practices 第 4 点

**原始错误:**
```
"Use `UseRandomLoadContext()` to avoid context pollution"
```

**修正后:**
```
"Use `UseRandomDomain()` to avoid domain pollution"
```

---

### 错误 6️⃣ NuGet 包链接错误

**位置:** Additional Resources 部分

**原始错误:**
```
https://www.nuget.org/packages/DotNetCore.Natasha.CSharp.Compiler.Domain
```

**官方文档依据:**
- 实际的两个包是：
  1. https://www.nuget.org/packages/DotNetCore.Natasha.CSharp.Compiler
  2. https://www.nuget.org/packages/Natasha.CSharp.Compiler.Domain

**修正后:**
```
- **NuGet Package (Compiler):** https://www.nuget.org/packages/DotNetCore.Natasha.CSharp.Compiler
- **NuGet Package (Domain):** https://www.nuget.org/packages/Natasha.CSharp.Compiler.Domain
```

---

### 错误 7️⃣ Important Notes 中的概念错误

**位置:** Important Notes 部分（原始版本）

**原始错误:**
```
"The `Natasha.CSharp.Template` package and `NDelegate` high-level API"
```

**问题:**
- 这些信息已过时，与官方文档不符
- 应强调 Natasha 使用"域"而非 LoadContext

**修正后:**
```
### Core Concepts

- **Natasha** uses **domains** (not load contexts) for isolation. 
  A domain is an abstraction over AssemblyLoadContext.
- **AssemblyCSharpBuilder** is the main API for dynamic compilation (modern approach).
- The **NatashaManagement** class handles global initialization and domain registration.

### Modern API (Recommended)

- **Always use:** `AssemblyCSharpBuilder` + `NatashaManagement.Preheating()` 
  or `GetInitializer()` chain-style initialization
- **Deprecated:** The old `NatashaManagement.RegistDomainCreator()` with separate `.Preheating()` 
  is still supported but less convenient than chain-style
```

---

## 官方文档参考清单

✅ **已核对的文档文件:**

1. **G:\Project\OpenSource\Natasha.Docs\src\i18n\zh-Hans\docusaurus-plugin-content-docs\current\compile\index.md**
   - 包说明和官方 NuGet 包列表

2. **G:\Project\OpenSource\Natasha.Docs\src\docs\compile\001-Domain.md**
   - 域的概念、创建方法、插件加载

3. **G:\Project\OpenSource\Natasha.Docs\src\docs\compile\002-SmartMode-Full.md**
   - 链式初始化方法（V9+）、预热方式、过滤预热

4. **G:\Project\OpenSource\Natasha.Docs\src\docs\compile\004-Metadata.md**
   - 元数据管理、引用管理、Using Code 管理

5. **G:\Project\OpenSource\Natasha.Docs\src\docs\compile\010-CompileDirector.md**
   - CompileDirector 扩展包用法

6. **G:\Project\OpenSource\Natasha.Docs\src\docs\00-0-Docs.md**
   - 项目总体介绍

---

## 修正验证

✅ **修正后检查清单:**

- [x] 修正 NuGet 包名称为官方正确包名
- [x] 更新初始化方法为官方推荐方式
- [x] 移除不存在的 LoadContext API，改用 Domain API
- [x] 补充域管理概念说明
- [x] 更正所有 API 方法名
- [x] 更新官方文档链接
- [x] 验证代码示例 API 调用
- [x] 核对预热参数说明

---

## 建议

1. **维护成本:** 该 SKILL 文件应与官方文档同步更新，建议每个季度对照官方文档核实一次
2. **版本标注:** 建议在文件顶部标注所基于的 Natasha 版本（当前为 V9+）
3. **示例扩展:** 可考虑添加 CompileDirector、Extension.Ambiguity、Extension.Codecov 的使用示例

---

**核对完成时间:** 2026-03-19 11:00  
**修正文件:** C:\Users\Administrator\Desktop\skills\Natasha\SKILL.md  
**状态:** ✅ 所有错误已修正

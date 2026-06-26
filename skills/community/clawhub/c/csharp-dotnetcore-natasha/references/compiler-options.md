# 编译器选项完全指南

## ConfigCompilerOption() 方法

`ConfigCompilerOption()` 用于细粒度控制 C# 编译器的行为。

```csharp
AssemblyCSharpBuilder builder = new();
builder.ConfigCompilerOption(opt => opt
    .AppendCompilerFlag(...)
    .WithAllMetadata()
    .AppendNullableFlag(...)
);
```

## 常用编译选项

### 1. 访问修饰符检查

#### 忽略访问修饰符 IgnoreAccessibility

```csharp
builder.ConfigCompilerOption(opt => opt
    .AppendCompilerFlag(IgnoreAccessibility)
);
```

**作用：** 允许动态代码访问 private、protected 和 internal 成员（编译时），无需 reflection。

**搭配使用：** 必须配合 `.ToAccessPrivateTree(typeof(T))` 方法。

```csharp
builder.ConfigCompilerOption(opt => opt
    .AppendCompilerFlag(IgnoreAccessibility)
    .WithAllMetadata()
)
.ToAccessPrivateTree(typeof(TargetClass));
```

### 2. 元数据访问级别

控制编译后代码可以访问哪些类型成员。

#### WithAllMetadata()

```csharp
builder.ConfigCompilerOption(opt => opt.WithAllMetadata());
```

**访问权限：** public + internal + private

**使用场景：** 需要访问私有成员时的标准配置

#### WithInternalMetadata()

```csharp
builder.ConfigCompilerOption(opt => opt.WithInternalMetadata());
```

**访问权限：** public + internal

**使用场景：** 需要访问内部 API 但不涉及私有成员

#### WithPublicMetadata()

```csharp
builder.ConfigCompilerOption(opt => opt.WithPublicMetadata());
```

**访问权限：** public 仅

**使用场景：** 标准编译，仅使用公开 API（默认）

### 3. 可空性注解

#### 启用可空注解

```csharp
builder.ConfigCompilerOption(opt => opt
    .AppendNullableFlag(NullableContextOptions.Enable)
);
```

**作用：** 启用 C# 8.0+ 的可空引用类型功能

**效果：**
- 必须显式标记可空类型（`string?`）
- 编译器进行可空性检查
- 生成更严格的代码

#### 禁用可空注解

```csharp
builder.ConfigCompilerOption(opt => opt
    .AppendNullableFlag(NullableContextOptions.Disable)
);
```

### 4. 其他常用选项

```csharp
builder.ConfigCompilerOption(opt => opt
    // 允许不安全代码
    .AppendCompilerFlag(AllowUnsafeBlocks)
    
    // 启用顶级语句
    .AppendCompilerFlag(TopLevelStatements)
    
    // 启用可空注解
    .AppendNullableFlag(NullableContextOptions.Enable)
);
```

## 编译配置快捷方法

### Release 编译

```csharp
builder.WithReleaseCompile();
```

**特点：**
- 启用优化
- 移除调试信息
- 更小的程序集大小
- 更快的执行性能

### Debug 编译

```csharp
builder.WithDebugCompile();
```

**特点：**
- 保留调试信息
- 优化禁用
- 便于调试
- 程序集更大

## 完整示例

### 示例 1：标准编译（推荐）

```csharp
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    .WithReleaseCompile();
    // 使用默认元数据和编译选项
```

### 示例 2：访问私有成员

```csharp
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    .ConfigCompilerOption(opt => opt
        .AppendCompilerFlag(IgnoreAccessibility)
        .WithAllMetadata()
    )
    .ToAccessPrivateTree(typeof(TargetClass))
    .Add(@"
        public class Accessor {
            public static int ReadPrivateField(TargetClass obj) {
                return obj._privateField;
            }
        }
    ");
```

### 示例 3：启用可空注解的严格编译

```csharp
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    .WithReleaseCompile()
    .ConfigCompilerOption(opt => opt
        .AppendNullableFlag(NullableContextOptions.Enable)
    )
    .Add(@"
        public class StrictClass {
            public string Name { get; set; } // 必须赋值
            public string? Description { get; set; } // 可以为 null
        }
    ");
```

### 示例 4：不安全代码编译

```csharp
AssemblyCSharpBuilder builder = new();
builder
    .UseRandomLoadContext()
    .UseSmartMode()
    .ConfigCompilerOption(opt => opt
        .AppendCompilerFlag(AllowUnsafeBlocks)
    )
    .Add(@"
        public class UnsafeClass {
            public unsafe int* GetPointer(int[] arr) {
                fixed (int* p = arr) {
                    return p;
                }
            }
        }
    ");
```

## 最佳实践

### 1. 根据场景选择元数据级别

```csharp
// 公开 API 编译
builder.ConfigCompilerOption(opt => opt.WithPublicMetadata());

// 内部工具编译
builder.ConfigCompilerOption(opt => opt.WithInternalMetadata());

// 深度访问编译
builder.ConfigCompilerOption(opt => opt.WithAllMetadata());
```

### 2. 性能优化

```csharp
// 优先使用 Release 编译
builder.WithReleaseCompile();

// 仅在必要时启用可空检查
builder.ConfigCompilerOption(opt => opt
    .AppendNullableFlag(NullableContextOptions.Enable)
);
```

### 3. 错误处理

```csharp
try {
    builder.ConfigCompilerOption(opt => opt.WithAllMetadata())
        .ToAccessPrivateTree(typeof(TargetClass));
    var assembly = builder.GetAssembly();
} 
catch (CompilationErrorException ex) {
    Console.WriteLine($"编译失败: {ex.Message}");
}
```

## 常见错误

```csharp
// ❌ 错误1：AppendCompilerFlag 参数错误
builder.ConfigCompilerOption(opt => 
    opt.AppendCompilerFlag("IgnoreAccessibility")  // 字符串不对
);

// ✅ 正确
builder.ConfigCompilerOption(opt => 
    opt.AppendCompilerFlag(IgnoreAccessibility)  // 使用编译标志枚举
);

// ❌ 错误2：不调用 ToAccessPrivateTree
builder.ConfigCompilerOption(opt => opt.AppendCompilerFlag(IgnoreAccessibility));
// 编译器标志设置了，但 ToAccessPrivateTree 没调用，无法访问私有成员

// ✅ 正确
builder.ConfigCompilerOption(opt => opt
        .AppendCompilerFlag(IgnoreAccessibility)
        .WithAllMetadata()
    )
    .ToAccessPrivateTree(typeof(TargetClass));

// ❌ 错误3：多次调用 ConfigCompilerOption 覆盖
builder.ConfigCompilerOption(opt => opt.AppendCompilerFlag(IgnoreAccessibility));
builder.ConfigCompilerOption(opt => opt.WithAllMetadata());  // 前面的设置被覆盖

// ✅ 正确
builder.ConfigCompilerOption(opt => opt
    .AppendCompilerFlag(IgnoreAccessibility)
    .WithAllMetadata()  // 在同一调用中链式配置
);
```

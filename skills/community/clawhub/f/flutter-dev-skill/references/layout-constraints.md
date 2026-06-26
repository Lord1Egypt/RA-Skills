---
name: flutter-layout
description: Flutter 布局约束与约束传递机制完整参考。
source: https://flutter.cn/docs/development/ui/layout/constraints
---

# Flutter 布局约束 (Layout Constraints)

## 核心规则

> **约束向下传递，大小向上传递，父级决定位置**

Flutter 布局遵循一个简单的规则：
1. **Widget 从父级获取约束** — 约束是 4 个浮点数的集合：min/max 宽度和 min/max 高度
2. **Widget 向下传递约束给子级** — 可为每个子级传递不同约束
3. **Widget 询问子级想要的大小**
4. **Widget 向上返回自身大小**
5. **父级决定子级的位置**

```dart
// 布局协商示例
Widget: "嘿父级，我的约束是多少？"
Parent: "你的宽度在 0-300px，高度在 0-85px。"
Widget: "我需要 5px padding，所以子级最多 290x75。"
Widget (对子级): "你的宽度在 0-290px，高度在 0-75px。"
First Child: "那我想要 290x20。"
Widget (对第二个子级): "由于第一个占用了高度，现在只剩 55px 给你。"
Widget: "父级，我决定我的大小是 300x60。"
```

---

## BoxConstraints — Tight vs Loose

### Tight Constraints（严格约束）

约束的最大值等于最小值 — 只有一个可能的尺寸。

```dart
// Tight: 强制精确尺寸
BoxConstraints.tight(Size size)
// 相当于:
BoxConstraints(minWidth: size.width, maxWidth: size.width,
               minHeight: size.height, maxHeight: size.height)
```

**示例**: 屏幕 → `Container(width:100, height:100)` — Container 想设为 100x100，但被屏幕强制填充整个屏幕。

### Loose Constraints（宽松约束）

最小值为 0，最大值非零 — Widget 可以是任意大小（从 0 到最大值）。

```dart
// Loose: 允许任意尺寸（最小为0）
BoxConstraints.loose(Size size)
// 相当于:
BoxConstraints(minWidth: 0, maxWidth: size.width,
               minHeight: 0, maxHeight: size.height)
```

**示例**: `Center` 的作用是将从屏幕获得的 tight 约束转换为 loose 约束传递给子级。

---

## Unbounded Constraints（无界约束）

当 `maxWidth` 或 `maxHeight` 为 `double.infinity` 时，约束是无界的。

```dart
// 无界约束会导致渲染错误
UnconstrainedBox(
  child: Container(width: double.infinity, height: 100) // 错误！
)
```

### 常见无界约束场景

1. **Flex 容器内** (`Row`/`Column`) 的主轴方向
2. **滚动区域内** (`ListView`, `ScrollView`)

### 处理无界约束的 Widget

| Widget | 用途 |
|--------|------|
| `LimitedBox` | 当获得无限约束时添加限制；放入 `Center` 时限制失效 |
| `OverflowBox` | 允许子级超出自身，不显示溢出警告 |
| `UnconstrainedBox` | 允许子级任意大小（但仍可能溢出） |

```dart
// LimitedBox: 仅在获得无限约束时生效
UnconstrainedBox(
  child: LimitedBox(
    maxWidth: 100,
    child: Container(width: double.infinity) // 被限制为100px
  ),
)

// OverflowBox: 不警告溢出
OverflowBox(
  minWidth: 0, minHeight: 0,
  maxWidth: double.infinity, maxHeight: double.infinity,
  child: Container(width: 4000, height: 50) // 显示但不警告
)
```

---

## 关键布局 Widget

### SizedBox — 固定尺寸

```dart
SizedBox(width: 100, height: 50, child: child)

// 常用变体:
SizedBox.expand()      // 强制填满父级
SizedBox.shrink()      // 收缩到最小
SizedBox.fromSize()    // 从 Size 创建
```

### ConstrainedBox — 添加额外约束

> **重要**: `ConstrainedBox` 只施加**额外**约束，不会替换父级约束。

```dart
// 错误理解: Container 会在 70-150px 之间
ConstrainedBox(
  constraints: BoxConstraints(minWidth:70, maxWidth:150, 
                              minHeight:70, maxHeight:150),
  child: Container(width: 10, height: 10) // ❌ 被忽略
)

// 正确理解: 需要配合 Center 等提供 loose 约束的父级
Center(
  child: ConstrainedBox(
    constraints: BoxConstraints(minWidth:70, maxWidth:150),
    child: Container(width: 10) // ✅ 实际为 70px
  ),
)
```

### Padding — 内边距

```dart
Padding(
  padding: EdgeInsets.all(20),
  child: Container(color: red, child: ...)
)
// Container 实际获得 40x40 的空间（减去 padding）
```

### Flexible 与 Expanded — Flex 容器内的空间分配

| Widget | 行为 |
|--------|------|
| `Flexible` | 允许子级**小于等于** Flexible 的宽度 |
| `Expanded` | 强制子级**等于** Expanded 的宽度 |

```dart
Row([
  Expanded(     // 忽略子级原本大小，按比例分配
    flex: 1,    // 默认 flex=1
    child: Container(color: red, width: 1000) // 被强制为可用空间的 1/3
  ),
  Expanded(
    flex: 2,
    child: Container(color: green) // 被强制为可用空间的 2/3
  ),
])
```

> **注意**: `Expanded` 和 `Flexible` 会**忽略**子级想要的大小。无法按子级原始大小比例分配。

### FittedBox — 缩放以填满空间

```dart
// Text 会缩放以填满可用宽度
FittedBox(child: Text('Some text'))

// 配合 Center: 如果 Text 不超出屏幕则不缩放
Center(child: FittedBox(child: Text('Short text'))) // 无缩放

// Text 超出屏幕时缩放到屏幕大小
Center(child: FittedBox(child: Text('Very long text...'))) // 缩放
```

> **限制**: `FittedBox` 只能缩放**有界**（非无限）的子级。

### Stack — 层叠布局

```dart
Stack([
  Container(width: 100, height: 100, color: red),
  Positioned(
    right: 10, top: 10,
    child: Container(width: 50, height: 50, color: green)
  ),
])
```

### Align 与 Center — 对齐

```dart
// Center 是 alignment: Alignment.center 的 Align
Center(child: ...) ≈ Align(alignment: Alignment.center, child: ...)

// 定位到右下角
Align(
  alignment: Alignment.bottomRight,
  child: Container(width: 100, height: 100)
)
```

---

## Flex 布局规则 (Row/Column)

Flex 容器根据**主轴方向**的约束是否有限来决定行为：

| 约束类型 | 行为 |
|----------|------|
| **有限约束** | Flex 尝试撑满可用空间 |
| **无限约束** | Flex 尝试适应子级大小（所有子级 `flex` 必须为 0） |

### 交叉方向必须有限

```dart
// ❌ 错误: Column 的宽度（交叉方向）不能无限
Column(children: [Expanded(child: Text('...'))]) // 抛出异常

// ✅ 正确: 需要在外层限制宽度
Center(
  child: Column(children: [Expanded(child: Text('...'))])
)
```

---

## 常见布局陷阱

### 1. 设置了尺寸却不生效

```dart
// ❌ 错误: 屏幕强制 Container 填满屏幕
Container(width: 100, height: 100, color: red)

// ✅ 正确: 用 Center 提供 loose 约束
Center(child: Container(width: 100, height: 100, color: red))
```

### 2. ConstrainedBox 不生效

```dart
// ❌ 错误: ConstrainedBox 被父级的 tight 约束"吃掉"
ConstrainedBox(
  constraints: BoxConstraints(minWidth: 70, maxWidth: 150),
  child: Container(width: 10) // 被忽略
)

// ✅ 正确: 父级需提供 loose 约束
Center(
  child: ConstrainedBox(
    constraints: BoxConstraints(minWidth: 70, maxWidth: 150),
    child: Container(width: 10) // 实际 70px
  ),
)
```

### 3. Row/Column 溢出

```dart
// ❌ 错误: 子级太大导致溢出
Row([
  Container(color: red, child: Text('Very long text...')))
  Container(color: green, child: Text('Goodbye!'))
])

// ✅ 正确: 用 Expanded 分配空间
Row([
  Expanded(child: Container(color: red, child: Text('...')))
  Container(color: green, child: Text('Goodbye!'))
])
```

### 4. 无限尺寸渲染错误

```dart
// ❌ 错误: Flutter 无法渲染无限尺寸
UnconstrainedBox(
  child: Container(width: double.infinity) // 抛出异常
)

// ✅ 正确: 用 LimitedBox 限制
UnconstrainedBox(
  child: LimitedBox(maxWidth: 100, child: Container(...))
)
```

### 5. Flex 内使用 Expanded 时 flex 为 0

```dart
// ❌ 错误: Flex 容器在无限约束下，所有 flex 必须为 0
// 但 Expanded 默认 flex=1，会抛出异常

// ✅ 正确: 如果需要扩展，确保 Flex 获得有限约束
```

---

## LayoutBuilder 与 MediaQuery

> 文档原文件主要聚焦于约束传递机制。`LayoutBuilder` 和 `MediaQuery` 的详细说明请参考其他文档。

### LayoutBuilder

在布局时获取可用约束：

```dart
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth > 600) {
      return WideLayout();
    } else {
      return NarrowLayout();
    }
  }
)
```

### MediaQuery

获取媒体查询数据（屏幕大小、像素密度等）：

```dart
MediaQuery.of(context).size        // 屏幕尺寸
MediaQuery.of(context).padding      // 系统 UI 边距
MediaQuery.of(context).orientation // 屏幕方向
```

---

## Widget 布局行为分类

| 类型 | 示例 | 行为 |
|------|------|------|
| **撑满型** | `Center`, `ListView`, `Container` | 尽可能撑满约束范围 |
| **跟随子级型** | `Transform`, `Opacity` | 尽可能与子级保持一致 |
| **固定尺寸型** | `Image`, `Text` | 尝试变为指定大小 |

---

## 调试布局的步骤

1. **向上追溯**: 从 leaf widget 开始，查看每个父级传递了什么约束
2. **检查约束类型**: 是 tight 还是 loose？是有限还是无限？
3. **验证子级大小**: 子级想要的大小 vs 最终获得的大小
4. **使用 DevTools**: Flutter DevTools 的 Inspector 可视化布局边界

---

## 关键参考

- **规则**: 约束向下传递 → 大小向上传递 → 父级决定位置
- **Tight**: maxWidth == minWidth, maxHeight == minHeight（唯一尺寸）
- **Loose**: minWidth == 0, minHeight == 0（任意尺寸从 0 到 max）
- **Unbounded**: maxWidth 或 maxHeight 为 `double.infinity`
- **ConstrainedBox**: 只添加额外约束，不替换父级约束
- **Expanded/Flexible**: 忽略子级大小，按比例分配空间

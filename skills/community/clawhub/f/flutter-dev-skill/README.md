# Flutter 开发技能

Flutter 跨平台移动开发技能，覆盖 Widget 体系、布局约束、Material 3 迁移、动画、State 管理、网络请求、性能优化。当用户提到 Flutter、Dart、移动开发、跨平台时触发。

## 概述

本 skill 覆盖 Flutter 完整开发知识体系：

- **Widget 体系** — StatelessWidget/StatefulWidget/State/BuildContext
- **布局约束** — BoxConstraints 传递机制、Flex/Stack/Grid
- **Material 3** — 种子色、组件重命名、ThemeData 迁移
- **动画** — Hero 页面转场、Staggered 交错动画
- **State 管理** — Provider/Riverpod/BLoC 方案对比与选型
- **网络层** — Dio 封装、Token 自动刷新、统一响应体
- **持久化** — SharedPreferences/SQLite/Hive
- **性能优化** — 重建控制、长列表优化
- **自适应布局** — MediaQuery/LayoutBuilder/响应式列数

## 核心章节

### 基础

| 章节 | 内容 |
|------|------|
| [Widget 体系与 State 管理](SKILL.md#Widget-体系与-State-管理) | Widget 类型、State 生命周期、BuildContext |
| [布局约束](SKILL.md#布局约束) | BoxConstraints 传递、Flex/Stack/Grid 布局 |
| [Material 3 迁移](SKILL.md#Material-3-迁移) | useMaterial3 开关、组件重命名、种子色配置 |

### 架构与网络

| 章节 | 内容 |
|------|------|
| [State 管理方案对比](SKILL.md#State-管理方案对比) | Provider/Riverpod/BLoC 原理与选型 |
| [网络请求](SKILL.md#网络请求) | Dio 封装、Token 刷新、响应体拦截、错误处理 |
| [持久化存储](SKILL.md#持久化存储) | SharedPreferences/SQLite/Hive |
| [动画系统](SKILL.md#动画系统) | Hero 页面转场、Staggered 交错动画 |

### 平台与进阶

| 章节 | 内容 |
|------|------|
| [响应式布局实战](SKILL.md#响应式布局实战) | MediaQuery/LayoutBuilder、响应式列数 |
| [平台适配](SKILL.md#平台适配) | 平台检测、键盘快捷键、鼠标 Hover |
| [性能优化](SKILL.md#性能优化) | 重建控制、长列表优化 |
| [避坑指南](SKILL.md#避坑指南) | 常见错误与正确做法 |

### 参考文档

| 文件 | 行数 | 内容 |
|------|------|------|
| material-3.md | 767 | Material 3 迁移完整指南 |
| layout-constraints.md | 368 | 布局约束与约束传递机制 |
| overview-getting-started.md | 376 | Flutter 入门与平台能力 |
| buttons-input.md | 424 | 按钮与输入组件 |
| adaptive-responsive.md | 298 | 自适应响应式布局 |
| platform-idioms.md | 358 | 平台适配与设备类型 |
| large-screens.md | 264 | 大屏幕与折叠屏支持 |
| navigation-components.md | 350 | 导航组件 |
| display-components.md | 300 | 展示组件 |
| hero-animations.md | 239 | Hero 动画 |
| staggered-animations.md | 354 | 交错动画 |
| testing.md | 121 | 测试指南（单元/Widget/集成/Mock） |
| dependency-injection.md | 81 | 依赖注入（get_it/Riverpod/injectable） |

## 快速参考

### Widget 类型对照

| 类型 | 说明 | 示例 |
|------|------|------|
| **StatelessWidget** | 不可变，props 决定 UI | `Text`, `Icon`, `Container` |
| **StatefulWidget** | 可变，通过 State 管理变化 | `Checkbox`, `TextField`, `Scaffold` |

### State 管理方案对比

| 方案 | 适用场景 | 复杂度 |
|------|---------|--------|
| **setState** | 局部 UI 状态 | ★☆☆☆☆ |
| **Provider** | 中小型应用 | ★★☆☆☆ |
| **Riverpod** | 生产级应用（推荐） | ★★★☆☆ |
| **BLoC** | 大型复杂项目 | ★★★★☆ |

### 布局 Widget

| 组件 | 用途 | 关键属性 |
|------|------|---------|
| Column | 垂直布局 | `.spacing()`, `.crossAxisAlignment()` |
| Row | 水平布局 | `.spacing()`, `.mainAxisAlignment()` |
| Expanded | 弹性填充 | 在 Row/Column/Flex 内使用 |
| Flexible | 弹性但不强制 | `.flex()`, `.fit()` |
| Stack | 层叠布局 | `.alignment()`, `.children` |
| GridView | 网格布局 | `.gridDelegate()`, `.children` |
| ListView | 列表布局 | `.itemBuilder()`, `.separatorBuilder()` |

### 常用布局代码

```dart
// Column 垂直布局
Column(
  children: [
    Text('Header'),
    Expanded(child: Content()),
    BottomBar(),
  ],
)

// Row 水平布局
Row(
  children: [
    Icon(Icons.menu),
    Expanded(child: Title()),
    Actions(),
  ],
)

// Stack 层叠
Stack(
  children: [
    Background(),
    Content(),
    FloatingButton(),
  ],
)
```

### 种子色配置

```dart
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.blue,
      brightness: Brightness.light,
    ),
    useMaterial3: true,
  ),
)
```

### Riverpod 最小示例

```dart
// 定义
final counterProvider = StateProvider<int>((ref) => 0);

// 使用
Consumer(builder: (context, ref, child) {
  final count = ref.watch(counterProvider);
  return Text('$count');
});

// 修改
ref.read(counterProvider.notifier).state++;
```

### Dio 网络请求

```dart
// Token 自动刷新拦截器
 dio.interceptors.add(InterceptorsWrapper(
  onError: (e, handler) async {
    if (e.response?.statusCode == 401) {
      await dio.refreshToken();
      final retry = await dio.fetch(e.requestOptions);
      return handler.resolve(retry);
    }
    handler.next(e);
  },
));

// 统一响应体
class ApiResp<T> {
  final int code;
  final T? data;
  final String? message;
}
```

## 避坑指南

### Widget 与 State

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 在 build() 中直接修改 State | ✅ 通过 setState() 触发重建 |
| ❌ setState() 内执行异步操作不带回调 | ✅ 异步后用 mounted 判断再 setState |
| ❌ StatefulWidget 在 dispose 后继续操作 | ✅ 使用 if (mounted) 保护 |
| ❌ 把 Widget 当可变容器 | ✅ Widget 不可变，状态放 State |

### 布局约束

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ SizedBox 嵌套过多 | ✅ 使用 Column/Row + spacer 替代 |
| ❌ Expanded/ Flexible 放在 Stack 内 | ✅ Expanded 仅在 Flex（Column/Row/Flex）内有效 |
| ❌ 忽视 BoxConstraints 传递 | ✅ 父约束决定子组件尺寸，子不能超出父 |
| ❌ ListView 内嵌套相同方向 ScrollView | ✅ 冲突导致无限扩展，用 CustomScrollView 统一 |

### Riverpod

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 在 build() 内 watch Provider | ✅ 避免循环依赖，用 ref.watch 在组件顶层 |
| ❌ 混用 ref.watch 和 ref.read | ✅ watch 监听变化触发重建，read 仅获取当前值 |
| ❌ StateNotifier 不检查 dispose | ✅ 异步回调中用 if (mounted) 保护 |
| ❌ Provider 顶层注册依赖未初始化 | ✅ 用 Provider.family 处理需要参数的 Provider |

### 网络层

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ Dio 实例全局单例不配拦截器 | ✅ 按业务拆分多个 Dio 实例或用配置类 |
| ❌ Token 刷新后不重试原请求 | ✅ 使用 QueueInterceptor 队列管理重试 |
| ❌ 不处理网络异常统一抛 Exception | ✅ 区分 DioExceptionType 做分类处理 |
| ❌ 响应数据不判空直接用 | ✅ 用 `?.` 或判空检查防止空指针 |

## 来源

> Flutter 官方文档（2026-04-24 访问）
> - 官方文档：https://flutter.cn/docs
> - Widget 目录：https://docs.flutter.dev/ui/widgets
> - Material 3 迁移：https://flutter.cn/docs/release/breaking-changes/material-3-migration
> - 布局约束：https://flutter.cn/docs/development/ui/layout/constraints
> - Hero 动画：https://flutter.cn/docs/development/ui/animations/hero-animations
> - Staggered 动画：https://flutter.cn/docs/development/ui/animations/staggered-animations
>
> 版本：Flutter 3.x + Material 3

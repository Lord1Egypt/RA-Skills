---
name: flutter-adaptive-responsive
description: Flutter 响应式/自适应设计完整参考。
source: https://flutter.cn/docs
---

# Flutter 响应式/自适应设计

本文档涵盖 Flutter 平台自动适配机制、尺寸测量工具（`MediaQuery`、`LayoutBuilder`）、断点策略以及窗口尺寸类的完整参考。

## 平台自动适配（Platform Adaptations）

Flutter 为 Android 和 iOS 自动适配以下系统级体验。

### 导航转场动画

**Android**：默认 [`Navigator.push()`][] 使用 [`ZoomPageTransitionsBuilder`][] 动画——路由跳转时界面缩放到下一页，返回时缩回上一页。

**iOS**：
- 默认 Push 转场动画：从后向前滑动（根据语言 RTL 设置方向），背景页同步视差滑动
- `PageRoute.fullscreenDialog == true` 时为 Present/Modal 样式，自下而上全屏模态

**返回导航**：
- Android：系统返回按钮触发 `Navigator.pop()`
- iOS：屏幕边缘右滑触发返回

[`Navigator.push()`]: {{site.api}}/flutter/widgets/Navigator/push.html
[`ZoomPageTransitionsBuilder`]: {{site.api}}/flutter/material/ZoomPageTransitionsBuilder-class.html

### 滚动行为

| 特性 | Android | iOS |
|---|---|---|
| 物理仿真 | 静态摩擦更多，加速快，停止急促 | 动态摩擦更多，渐近达高速，停止柔和 |
| 越界效果 | GlowingOverscrollIndicator 灰色光晕 | BouncingScrollPhysics 弹簧回弹 |
| 动量 | 无叠加 | 同方向连续滑动速度叠加 |
| 返回顶部 | 无 | 点击状态栏滚动到顶 |

```dart
// Android 越界效果
ScrollConfiguration(
  behavior: ScrollConfiguration.of(context).copyWith(
    overscrollIndicator: GlowingOverscrollIndicator,
  ),
  child: ListView(children: ...),
);

// iOS 越界效果
ScrollConfiguration(
  behavior: ScrollConfiguration.of(context).copyWith(
    overscrollIndicator: BouncingScrollPhysics,
  ),
  child: ListView(children: ...),
);
```

### 排版

- Material 主题：Android → Roboto，iOS → San Francisco
- Cupertino 主题：始终使用 San Francisco（Android 上使用替代字体）

```dart
// 平台感知字体
TextTheme cupertinoTextTheme = TextTheme(
  headlineMedium: CupertinoThemeData()
      .textTheme
      .navLargeTitleTextStyle
      .copyWith(letterSpacing: -1.5),
  titleLarge: CupertinoThemeData().textTheme.navTitleTextStyle,
);

ThemeData(
  textTheme: Platform.isIOS ? cupertinoTextTheme : null,
)
```

### 图标

Material 包根据平台自动切换图标样式（如更多按钮：iOS 横排三点 / Android 竖排三点；返回按钮：iOS 纯 V 型 / Android V 型加短横线）。也可通过 [`Icons.adaptive`][] 获取平台自适应图标。

[`Icons.adaptive`]: {{site.api}}/flutter/material/PlatformAdaptiveIcons-class.html

### 触摸反馈

| 场景 | Android | iOS |
|---|---|---|
| 文本长按选中单词 | 震动 'buzz' | 无 |
| 选择器滚动 | 无 | 'light impact' 轻敲 |

### 文本编辑

| 手势 | Android (Material) | iOS (Material/Cupertino) |
|---|---|---|
| 单击 | 光标移到点击处，有可拖动把手 | 光标移到最近单词边缘，无把手 |
| 长按 | 选中单词，释放显示工具栏 | 放置光标，释放显示工具栏 |
| 长按拖动 | 扩展选中词范围 | 移动光标 |
| 双击 | 选中单词 | 选中单词 |
| 空格键滑动 | 移动光标 | — |
| 3D Touch 拖动 | — | 浮动光标任意方向移动 |

### UI 组件 .adaptive() 构造器

以下 Material widget 提供 `.adaptive()` 构造器，在 iOS 上自动替换为对应 Cupertino 组件：

```dart
// 开关
Switch.adaptive(value: value, onChanged: ...)
// 滑块
Slider.adaptive(value: value, onChanged: ...)
// 进度指示器
CircularProgressIndicator.adaptive()
// 刷新指示器
RefreshIndicator.adaptive()
// 复选框
Checkbox.adaptive(value: value, onChanged: ...)
// 单选框
Radio.adaptive(value: value, groupValue: ..., onChanged: ...)
// 警告对话框
AlertDialog.adaptive(title: ..., content: ...);
```

### 顶部应用栏适配

```dart
AppBar(
  surfaceTintColor: Platform.isIOS ? Colors.transparent : null,
  shadowColor: Platform.isIOS ? CupertinoColors.darkBackgroundGray : null,
  scrolledUnderElevation: Platform.isIOS ? .1 : null,
  toolbarHeight: Platform.isIOS ? 44 : null,
),
```

### 底部导航栏

```dart
Scaffold(
  body: _currentWidget,
  bottomNavigationBar: Platform.isIOS
      ? CupertinoTabBar(
          currentIndex: _currentIndex,
          onTap: (index) => setState(() => _currentIndex = index),
          items: _navigationItems.entries
              .map<BottomNavigationBarItem>(
                  (e) => BottomNavigationBarItem(
                        icon: e.value,
                        label: e.key,
                      ))
              .toList(),
        )
      : NavigationBar(
          selectedIndex: _currentIndex,
          onDestinationSelected: (index) =>
              setState(() => _currentIndex = index),
          destinations: _navigationItems.entries
              .map<Widget>((e) => NavigationDestination(
                    icon: e.value,
                    label: e.key,
                  ))
              .toList(),
        ),
);
```

---

## 测量窗口尺寸

### MediaQuery.sizeOf vs MediaQuery.of

`MediaQuery.sizeOf` 仅读取 size 属性，性能优于包含全部数据的 `MediaQuery.of`。

```dart
// 推荐：用 sizeOf 获取窗口尺寸
Size size = MediaQuery.sizeOf(context);

// 而非：
Size size = MediaQuery.of(context).size;
```

`MediaQuery.sizeOf(context)` 在尺寸变化时触发 `BuildContext` 重建。

### LayoutBuilder

`LayoutBuilder` 返回父级 `BoxConstraints`（含 min/max 范围），而非固定 `Size`。适用于仅关心特定 widget 可用空间而非整个 App 窗口的场景。

```dart
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth < 600) {
      return _buildMobileLayout();
    } else {
      return _buildDesktopLayout();
    }
  },
)
```

### SafeArea

`SafeArea` 用 `MediaQuery` 数据检测系统 UI（状态栏、异形屏、圆角）并留出安全边距。它会修改传递给子 widget 的 `MediaQuery`，使嵌套的 `SafeArea` 不会重复累加内边距。

```dart
// 推荐：仅包裹需要安全区的内容
Scaffold(
  appBar: AppBar(...),  // AppBar 已处理状态栏区域
  body: SafeArea(
    top: false,  // AppBar 已处理顶部，不需要重复
    child: content,
  ),
);

// 不推荐：包裹整个 Scaffold（AppBar 会重复处理）
Scaffold(
  body: SafeArea(child: ...),  // 错误
);
```

---

## 断点与窗口尺寸类

Material 3 推荐的响应式断点（基于**窗口宽度**，而非设备类型）：

| 窗口宽度 | 尺寸类 | 典型布局 |
|---|---|---|
| < 600 dp | Compact | 底部导航栏 |
| 600–839 dp | Medium | 导航轨道 (NavigationRail) |
| ≥ 840 dp | Expanded | 永久侧边导航 |

> **重要**：根据**应用窗口的实际宽度**选择断点，而非设备类型。Flutter 应用可能在 ChromeOS 桌面窗口、平板多窗口模式、画中画等各式环境中运行。

```dart
Widget build(BuildContext context) {
  final width = MediaQuery.sizeOf(context).width;

  if (width < 600) {
    return BottomNavigationBar(...);      // Compact
  } else if (width < 840) {
    return NavigationRail(...);           // Medium
  } else {
    return NavigationDrawer(...);          // Expanded
  }
}
```

```dart
// 使用 ConstrainedBox 限制最大内容宽度
ConstrainedBox(
  constraints: const BoxConstraints(maxWidth: 1200),
  child: content,
);
```

---

## 自适应三步法

### Step 1: 抽象（Abstract）

将 UI 拆分为可共享的小组件：

```dart
// 抽象导航目标
class Destination {
  final IconData icon;
  final String label;
  const Destination({required this.icon, required this.label});
}

const destinations = [
  Destination(icon: Icons.home, label: 'Home'),
  Destination(icon: Icons.settings, label: 'Settings'),
];
```

### Step 2: 测量（Measure）

使用 `MediaQuery.sizeOf` 或 `LayoutBuilder` 获取实际可用空间。

### Step 3: 分支（Branching）

根据测量结果选择不同 UI：

```dart
Widget build(BuildContext context) {
  final screenWidth = MediaQuery.sizeOf(context).width;

  if (screenWidth >= 840) {
    return _buildExpandedLayout();
  } else if (screenWidth >= 600) {
    return _buildMediumLayout();
  } else {
    return _buildCompactLayout();
  }
}
```

详细示例参见 [Material 3 动画响应式布局 Codelab]({{site.codelabs}}/codelabs/flutter-animated-responsive-layout)。

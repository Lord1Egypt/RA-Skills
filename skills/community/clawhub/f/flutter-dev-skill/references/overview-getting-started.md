---
name: flutter-overview
description: Flutter 开发入门与平台能力总览。
source: https://flutter.cn/docs
---

# Flutter 平台能力总览

Flutter 的核心目标是提供一个框架，允许开发者从单一代码库开发出在任何平台上都看起来很棒的应用。这意味着应用可能出现在不同尺寸的屏幕上，从智能手表，到折叠屏双屏手机，再到高清显示器。输入设备可能是物理或虚拟键盘、鼠标、触摸屏或许多其他设备。

## 1. Adaptive and Responsive Design（自适应与响应式设计）

### 什么是响应式 vs 自适应？

简单来说：
- **响应式设计**：让 UI **适应** 可用空间
- **自适应设计**：让 UI 在可用空间中**可用**

响应式应用调整设计元素的位置以**适应**可用空间。自适应应用选择适当的布局和输入设备以在可用空间中**可用**。例如，平板电脑 UI 应该使用底部导航还是侧边栏导航？

### 自适应设计的关键方面

| 主题 | 说明 |
|------|------|
| [通用方法][general] | 抽象 → 测量 → 分支的三步法 |
| [SafeArea & MediaQuery][safearea] | 安全区域和屏幕尺寸查询 |
| [大屏幕 & 折叠屏][large-screens] | 适配平板和折叠设备 |
| [用户输入 & 无障碍][input] | 触控、鼠标、键盘输入 |
| [能力 & 策略][capabilities] | 平台能力检测和策略设计 |
| [自适应应用最佳实践][best-practices] | 生产级自适应应用指南 |

[general]: /ui/adaptive-responsive/general
[safearea]: /ui/adaptive-responsive/safearea-mediaquery
[large-screens]: /ui/adaptive-responsive/large-screens
[input]: /ui/adaptive-responsive/input
[capabilities]: /ui/adaptive-responsive/capabilities
[best-practices]: /ui/adaptive-responsive/best-practices

### 自适应应用的三步法

#### Step 1: Abstract（抽象）

首先，识别需要动态化的 widgets。分析这些 widgets 的构造函数，抽象出可以共享的数据。

常见需要适应性的 widgets：
- 对话框（全屏和模态）
- 导航 UI（rail 和 bottom bar）
- 自定义布局（如"UI 区域更高还是更宽？"）

#### Step 2: Measure（测量）

有两种方式确定显示区域的大小：`MediaQuery` 和 `LayoutBuilder`。

**MediaQuery**：
- `MediaQuery.sizeOf(context)` 返回应用窗口的当前大小
- 返回以逻辑像素为单位的尺寸（密度无关像素）
- 当尺寸属性改变时，build 方法会重建

**LayoutBuilder**：
- 提供父 Widget 的布局约束
- 返回 `BoxConstraints` 而不是 `Size` 对象
- 提供有效宽度和高度范围（最小和最大）
- 适用于需要基于特定 widget 空间而不是整个应用窗口的 sizing 场景

#### Step 3: Branch（分支）

决定选择哪个版本 UI 的尺寸断点。例如，Material layout 指南建议：
- 窗口宽度小于 600 逻辑像素：使用 bottom nav bar
- 窗口宽度 600 像素或更大：使用 nav rail

:::note
选择不应取决于设备的**类型**，而应取决于设备的**可用窗口大小**。
:::

---

## 2. Animations API Overview（动画 API 概览）

Flutter 中的动画系统基于 `Animation` 对象。Widgets 可以直接将这些动画合并到自己的 build 方法中来读取它们的当前值或者监听它们的状态变化，或者可以将其作为更复杂动画的基础传递给其他 widgets。

### Animation

动画系统的首要组成部分是 `Animation` 类。一个动画表现为可在它的生命周期内发生变化的特定类型的值。

#### addListener

每当动画的状态值发生变化时，动画都会通知所有通过 `addListener` 添加的监听器。通常，一个正在监听动画的 `State` 对象会调用自身的 `setState` 方法来通知 widget 系统需要根据新状态值进行重新构建。

这种模式非常常见，所以有两个 widgets 可以帮助其他 widgets 在动画改变值时进行重新构建：
- `AnimatedWidget`：对于无状态动画 widgets 尤其有用
- `AnimatedBuilder`：对于希望将动画作为复杂 widgets 的 build 方法的其中一部分的情况非常有用

#### addStatusListener

动画还提供了一个 `AnimationStatus`，表示动画将如何随时间进行变化：
- `dismissed`：处于变化区间的开始点（值为 0.0）
- `forward`：正向运行（从 0.0 到 1.0）
- `reverse`：反向运行（从 1.0 到 0.0）
- `completed`：到达区间结束点（值为 1.0）

### AnimationController

要创建动画，首先要创建一个 `AnimationController`。除了作为动画本身，`AnimationController` 还可以用来控制动画：
- `forward()` / `reverse()`：正向或反向播放
- `stop()`：停止动画
- `fling()`：使用物理模拟（如弹簧）驱动动画
- `repeat()`：重复播放
- `animateTo()`：动画到指定目标

### Tweens（补间动画）

如果想要在 0.0 到 1.0 的区间之外设置动画，可以使用 `Tween<T>`，它可以在它的 `begin` 值和 `end` 值之间进行插值补间。

常见 Tween 子类：
- `ColorTween`：颜色间插值
- `RectTween`：矩形之间插值

两种方法将补间动画与动画组合：
1. 用 `evaluate()` 方法处理动画的当前值
2. 用 `animate()` 方法处理一个动画，返回包含补间动画插值的新 `Animation`

### 动画架构

#### Scheduler（调度器）

`SchedulerBinding` 是一个暴露出 Flutter 调度原语的单例类。关键原语是帧回调，每当一帧需要在屏幕上显示时，Flutter 的引擎会触发一个"开始帧"回调。

#### Tickers（运行器）

`Ticker` 类挂载在调度器的 `scheduleFrameCallback()` 的机制上来达到每次运行都会触发回调的效果。一个 `Ticker` 可以被启动和停止，启动时返回一个 `Future`。

#### Simulations（模拟器）

`Simulation` 抽象类将相对时间值（运行时间）映射为双精度值，并且有完成的概念。不同效果有不同具体实现，如 `BouncingScrollSimulation`、`ClampingScrollSimulation`。

#### Animatables

`Animatable` 抽象类将双精度值映射为特定类型的值。`Animatable` 类是无状态和不可变的。

#### Curves（曲线）

`Curve` 抽象类将名义范围为 0.0-1.0 的双精度值映射到名义范围为 0.0-1.0 的双精度值。`Curve` 类是无状态和不可变的。

### 可组合动画

- `CurvedAnimation`：接收父级 `Animation<double>` 和曲线类作为输入
- `ReverseAnimation`：反转动画所有值
- `ProxyAnimation`：仅转发父级的当前状态
- `TrainHoppingAnimation`：在两个父类的值交叉时切换

---

## 3. Widget, Layout, and Rendering Basics（Widget、布局和渲染基础）

### Flutter 的布局方法

在 Flutter 中，一切皆为 widget。布局的基本原则：

1. **识别行和列**：大多数布局是基于 Row 和 Column
2. **识别网格**：使用 GridView
3. **检查重叠元素**：使用 Stack
4. **确定对齐、填充和边框需求**

### 核心布局 Widgets

```dart
// Row：水平布局
Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  children: [/* 子 widgets */],
)

// Column：垂直布局
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [/* 子 widgets */],
)

// Expanded：填充剩余空间
Expanded(
  child: Column(/* ... */),
)

// Padding：添加间距
Padding(
  padding: const EdgeInsets.all(32),
  child: /* content */,
)

// 滚动视图
SingleChildScrollView(
  child: Column(
    children: [/* 子 widgets */],
  ),
)
```

### 构建步骤

1. **创建基础应用**：
```dart
void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter layout demo',
      home: Scaffold(
        appBar: AppBar(title: const Text(appTitle)),
        body: const Center(child: Text('Hello World')),
      ),
    );
  }
}
```

2. **构建可复用 Widgets**：
```dart
class TitleSection extends StatelessWidget {
  const TitleSection({super.key, required this.name, required this.location});

  final String name;
  final String location;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(32),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Text(name, style: const TextStyle(fontWeight: FontWeight.bold)),
                ),
                Text(location, style: TextStyle(color: Colors.grey[500])),
              ],
            ),
          ),
          Icon(Icons.star, color: Colors.red[500]),
          const Text('41'),
        ],
      ),
    );
  }
}
```

3. **配置资源**（pubspec.yaml）：
```yaml
flutter:
  uses-material-design: true
  assets:
    - images/lake.jpg
```

### 布局约束传递

Flutter 布局使用约束传递机制：
1. 父 widget 将约束传递给子 widget
2. 子 widget 根据约束决定自己的大小
3. 父 widget 根据子 widget 的大小决定位置

---

## 4. Platform-Specific Considerations（平台特定注意事项）

Flutter 为 Android 和 iOS 提供自动平台适配。

### 页面导航

| 平台 | 转场动画 |
|------|----------|
| **Android** | ZoomPageTransitionsBuilder，从下到上的缩放动画 |
| **iOS** | Push 转场（end-to-start）和 Present 转场（bottom-up） |

**返回导航**：
- Android：OS 返回按钮弹出 Navigator 顶部路由
- iOS：边缘滑动手势弹出顶部路由

### 滚动

| 特性 | Android | iOS |
|------|---------|-----|
| 物理仿真 | 更多静态摩擦力，快速达到速度，停止突然 | 更多动态摩擦力，逐渐达到高速，停止平滑 |
| Overscroll 行为 | 显示 GlowingOverscrollIndicator | 弹簧回弹效果 |
| 动量 | 无动量叠加 | 连续滚动速度叠加 |
| 返回顶部 | 无 | 点击状态栏滚动到顶 |

### 排版

- Material 包自动根据平台使用对应字体：Android 用 Roboto，iOS 用 San Francisco
- Cupertino 包默认使用 San Francisco 字体

### 图标

- 更多按钮图标：Android 竖直三个点，iOS 横排三个点
- 返回按钮：iOS 简单 V 型，Android V 型加短横线
- 通过 `Icons.adaptive` 提供平台自适应图标

### 触摸反馈

Material 和 Cupertino 包在特定场景下自动触发符合平台特点的触摸反馈：
- Android 长按选中单词触发震动，iOS 不触发
- iOS 滚动选择器触发轻敲音效，Android 不触发

### 文本编辑

| 行为 | Android (Material) | iOS (Material/Cupertino) |
|------|-------------------|--------------------------|
| 点击文本框 | 光标移动到点击位置 | 光标移动到点击处最近的单词末尾 |
| 长按 | 选中单词，释放显示工具栏 | 光标定位，释放显示工具栏 |
| 键盘手势 | 空格键左右滑动移动光标 | 3D Touch 任意方向移动光标 |
| 工具栏样式 | Android 风格 | iOS 风格 |

---

## 5. Capabilities & Policies（能力与策略）

### 设计原则

根据不同设备的优势和劣势进行设计。Flutter 推荐的模式是创建一组 `Capability` 和 `Policy` 类。

### Capabilities（能力）

定义代码或设备**能**做什么：
- API 的存在性
- OS 强制的限制
- 物理硬件要求（如相机）

### Policies（策略）

定义代码**应该**做什么：
- 应用商店指南
- 设计偏好
- 需要引用主机设备的资源或文案
- 服务器端启用的功能

### 最佳实践

**避免使用 `Platform.isAndroid` 等函数来做布局决策**，而是描述你想要分支的内容：

```dart
// 推荐：基于行为的抽象
class Policy {
  bool shouldAllowPurchaseClick() {
    // 被 Apple App Store 指南禁止
    return !Platform.isIOS;
  }
}

// 使用
TextSpan(
  text: 'Buy in browser',
  recognizer: shouldAllowPurchaseClick ? TapGestureRecognizer()..onTap = () { launch('<url>'); } : null,
)
```

这样做的优势：
- 代码更清晰地表达分支原因
- 便于测试（可以 mock Policy 类）
- 当需求变化时，不需要修改使用处的代码

### 策略实现方式

| 类型 | 适用场景 |
|------|----------|
| 编译时检查 | 偏好不太可能改变，错误更改后果严重 |
| 运行时检查 | 确定是否有触屏等运行时特性 |
| RPC 后端检查 | 增量功能发布或可能改变的决策 |

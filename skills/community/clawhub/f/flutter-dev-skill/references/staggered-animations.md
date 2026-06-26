---
name: flutter-staggered-animation
description: Flutter 交织动画实现参考。
source: https://flutter.cn/docs
---

# 交织动画 (Staggered Animations)

交织动画由一系列顺序执行或重叠执行的动画组成，每个动画控制不同的属性。

## 核心概念

### 什么是交织动画

- **顺序动画**：一个动画完成后另一个开始
- **重叠动画**：多个动画同时进行
- **间隔**：动画可能在时间轴上有间隙

### 关键组件

1. **`AnimationController`**：一个控制器管理所有动画
2. **`Interval`**：定义每个动画在时间轴上的起止点（0.0-1.0）
3. **`Tween`**：定义每个属性的起始和结束值
4. **`CurvedAnimation`**：为动画添加缓动曲线

## 代码示例

### 完整交织动画结构

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Staggered Animation',
      home: const StaggerDemo(),
    );
  }
}

/// 有状态 widget：创建 AnimationController
class StaggerDemo extends StatefulWidget {
  const StaggerDemo({super.key});

  @override
  State<StaggerDemo> createState() => _StaggerDemoState();
}

class _StaggerDemoState extends State<StaggerDemo>
    with TickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 2000),
      vsync: this,
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _playAnimation() async {
    try {
      await _controller.forward().orCancel;
      await _controller.reverse().orCancel;
    } on TickerCanceled {
      // 动画被取消，可能是因为 widget 被 dispose 了
    }
  }

  @override
  Widget build(BuildContext context) {
    timeDilation = 10.0; // 减慢动画便于观察
    return Scaffold(
      appBar: AppBar(title: const Text('Staggered Animation')),
      body: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: _playAnimation,
        child: Center(
          child: Container(
            width: 300,
            height: 300,
            decoration: BoxDecoration(
              color: Colors.black.withAlpha(25),
              border: Border.all(color: Colors.black.withAlpha(128)),
            ),
            child: StaggerAnimation(controller: _controller.view),
          ),
        ),
      ),
    );
  }
}

/// 无状态 widget：定义 Tween 和 Animation 对象
class StaggerAnimation extends StatelessWidget {
  const StaggerAnimation({
    super.key,
    required this.controller,
  })  : opacity = Tween<double>(
          begin: 0.0,
          end: 1.0,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: const Interval(0.0, 0.100, curve: Curves.ease),
          ),
        ),
        width = Tween<double>(
          begin: 50.0,
          end: 150.0,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: const Interval(0.125, 0.250, curve: Curves.ease),
          ),
        ),
        height = Tween<double>(
          begin: 50.0,
          end: 150.0,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: const Interval(0.250, 0.375, curve: Curves.ease),
          ),
        ),
        padding = Tween<EdgeInsets>(
          begin: const EdgeInsets.only(bottom: 0),
          end: const EdgeInsets.only(bottom: 100),
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: const Interval(0.250, 0.375, curve: Curves.ease),
          ),
        ),
        borderRadius = BorderRadiusTween(
          begin: BorderRadius.circular(4),
          end: BorderRadius.circular(75),
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: const Interval(0.375, 0.500, curve: Curves.ease),
          ),
        ),
        color = ColorTween(
          begin: Colors.blue,
          end: Colors.orange,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: const Interval(0.500, 0.750, curve: Curves.ease),
          ),
        );

  final AnimationController controller;
  final Animation<double> opacity;
  final Animation<double> width;
  final Animation<double> height;
  final Animation<EdgeInsets> padding;
  final Animation<BorderRadius?> borderRadius;
  final Animation<Color?> color;

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      builder: _buildAnimation,
      animation: controller,
    );
  }

  Widget _buildAnimation(BuildContext context, Widget? child) {
    return Container(
      padding: padding.value,
      alignment: Alignment.bottomCenter,
      child: Opacity(
        opacity: opacity.value,
        child: Container(
          width: width.value,
          height: height.value,
          decoration: BoxDecoration(
            color: color.value,
            border: Border.all(color: Colors.indigo[300]!, width: 3),
            borderRadius: borderRadius.value,
          ),
        ),
      ),
    );
  }
}
```

### 动画时序图

```
时间轴:    0.0    0.1    0.2    0.3    0.4    0.5    0.7    1.0
          |------|------|------|------|------|------|------|
不透明度   ████████
宽度             ████████████
高度                   ████████████
填充                   ████████████
圆角                         ████████████
颜色                               ████████████████
```

### 使用 Interval 控制动画时段

```dart
// 基础 Interval 用法
CurvedAnimation(
  parent: controller,
  curve: const Interval(0.0, 0.5), // 0% - 50% 的时间段
)

// 带 curve 的 Interval
CurvedAnimation(
  parent: controller,
  curve: const Interval(0.25, 0.75, curve: Curves.easeInOut),
)

// 常用 Curves
Curves.linear      // 匀速
Curves.ease        // 开始慢，结束慢
Curves.easeIn      // 开始慢
Curves.easeOut     // 结束慢
Curves.easeInOut   // 开始和结束都慢
Curves.bounceOut   // 弹跳效果
Curves.elasticOut  // 弹性效果
```

## 关键模式

### 分离有状态和无状态 widget

```dart
// 有状态 widget：管理 AnimationController
class MyStatefulWidget extends StatefulWidget {
  @override
  State<MyStatefulWidget> createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget>
    with TickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration,
      vsync: this,
    );
  }

  // 播放动画
  Future<void> _play() async {
    await _controller.forward();
    // 或反向播放
    // await _controller.reverse();
    // 或重复
    // _controller.repeat();
  }

  @override
  Widget build(BuildContext context) {
    return MyAnimationWidget(controller: _controller);
  }
}

// 无状态 widget：定义 Tween 和 build 方法
class MyAnimationWidget extends StatelessWidget {
  const MyAnimationWidget({super.key, required this.controller});

  final AnimationController controller;

  // 在这里定义所有 Tween
  late final Animation<double> _myAnimation = Tween<double>(
    begin: 0,
    end: 100,
  ).animate(CurvedAnimation(
    parent: controller,
    curve: const Interval(0.0, 0.5),
  ));

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: controller,
      builder: (context, child) {
        return Container(
          width: _myAnimation.value,
          height: _myAnimation.value,
          // ...
        );
      },
    );
  }
}
```

## 常见用法

### 同时播放多个动画

```dart
// 多个 Tween 共享同一个 Interval
width: Tween(begin: 50.0, end: 150.0).animate(
  CurvedAnimation(parent: controller, curve: Interval(0.0, 0.5)),
),
height: Tween(begin: 50.0, end: 150.0).animate(
  CurvedAnimation(parent: controller, curve: Interval(0.0, 0.5)), // 重叠
),
```

### 错开开始时间

```dart
// width 从 25% 开始
width: Tween(begin: 50.0, end: 150.0).animate(
  CurvedAnimation(parent: controller, curve: Interval(0.25, 0.5)),
),

// height 从 50% 开始
height: Tween(begin: 50.0, end: 150.0).animate(
  CurvedAnimation(parent: controller, curve: Interval(0.5, 0.75)),
),
```

### 反向播放动画

```dart
await _controller.forward().orCancel; // 正向
await _controller.reverse().orCancel;  // 反向

// 或设置状态自动反向
controller.addStatusListener((status) {
  if (status == AnimationStatus.completed) {
    controller.reverse();
  } else if (status == AnimationStatus.dismissed) {
    controller.forward();
  }
});
```

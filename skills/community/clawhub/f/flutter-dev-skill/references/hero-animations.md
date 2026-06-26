---
name: flutter-hero-animation
description: Flutter Hero 动画实现参考。
source: https://flutter.cn/docs
---

# Hero 动画 (Hero Animations)

Hero 动画实现共享元素过渡（shared element transitions），让 widget 在两个页面之间"飞翔"。

## 核心概念

### 基本结构

Hero 动画需要两个 Hero widgets，分别位于源页面和目标页面，它们使用**相同的 tag**：

```
源页面 Hero ──(tag)──> 目标页面 Hero
```

Flutter 会自动匹配相同 tag 的 Hero，并创建两者之间的过渡动画。

### 关键原理

1. **Tag 匹配**：两个 Hero 必须有相同的 tag（通常是代表底层数据的对象）
2. **Navigator 触发**：push 或 pop Navigator 堆栈时触发动画
3. **Overlay 飞行**：飞行过程中，hero 被移到应用 overlay 中，显示在两个页面之上
4. **RectTween**：Flutter 使用 `RectTween` 计算 hero 从起点到终点的边界

## 代码示例

### 标准 Hero 动画

```dart
class PhotoHero extends StatelessWidget {
  const PhotoHero({
    super.key,
    required this.photo,
    this.onTap,
    required this.width,
  });

  final String photo;
  final VoidCallback? onTap;
  final double width;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width,
      child: Hero(
        tag: photo,  // 必须与目标页面的 Hero tag 相同
        child: Material(
          color: Colors.transparent,
          child: InkWell(
            onTap: onTap,
            child: Image.asset(
              photo,
              fit: BoxFit.contain,
            ),
          ),
        ),
      ),
    );
  }
}

// 源页面
class HeroAnimation extends StatelessWidget {
  const HeroAnimation({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Basic Hero Animation')),
      body: Center(
        child: PhotoHero(
          photo: 'images/flippers-alpha.png',
          width: 300.0,
          onTap: () {
            Navigator.of(context).push(MaterialPageRoute<void>(
              builder: (context) {
                return Scaffold(
                  appBar: AppBar(title: const Text('Flippers Page')),
                  body: Container(
                    color: Colors.lightBlueAccent,
                    padding: const EdgeInsets.all(16),
                    alignment: Alignment.topLeft,
                    child: PhotoHero(
                      photo: 'images/flippers-alpha.png',
                      width: 100.0,  // 目标大小
                      onTap: () {
                        Navigator.of(context).pop();
                      },
                    ),
                  ),
                );
              },
            ));
          },
        ),
      ),
    );
  }
}
```

### 自定义 flightShuttleBuilder

`flightShuttleBuilder` 允许自定义 hero 在飞行过程中的外观：

```dart
Hero(
  tag: 'hero-image',
  flightShuttleBuilder: (
    BuildContext flightContext,
    Animation<double> animation,
    HeroFlightDirection flightDirection,
    BuildContext fromHeroContext,
    BuildContext toHeroContext,
  ) {
    return AnimatedBuilder(
      animation: animation,
      builder: (context, child) {
        // 自定义飞行中的 widget
        return Material(
          color: Colors.transparent,
          child: ClipRRect(
            borderRadius: BorderRadius.circular(
              // 动画过程中从圆形变到方形
              animation.value * 75,
            ),
            child: Image.asset(
              'images/flippers-alpha.png',
              fit: BoxFit.contain,
            ),
          ),
        );
      },
    );
  },
  child: /* 源/目标 Hero 的 child */,
)
```

### 径向 Hero 动画（圆形→方形）

径向动画使用 `MaterialRectCenterArcTween` 沿弧线路径飞行，同时图像形状由圆变方：

```dart
class RadialExpansion extends StatelessWidget {
  const RadialExpansion({
    super.key,
    required this.maxRadius,
    this.child,
  }) : clipRectSize = 2.0 * (maxRadius / math.sqrt2);

  final double maxRadius;
  final double clipRectSize;
  final Widget? child;

  @override
  Widget build(BuildContext context) {
    return ClipOval(
      child: Center(
        child: SizedBox(
          width: clipRectSize,
          height: clipRectSize,
          child: ClipRect(
            child: child,
          ),
        ),
      ),
    );
  }
}

// 自定义 createRectTween 实现弧形路径
static RectTween _createRectTween(Rect? begin, Rect? end) {
  return MaterialRectCenterArcTween(begin: begin, end: end);
}

Hero(
  tag: 'radial-hero',
  createRectTween: _createRectTween,
  child: RadialExpansion(
    maxRadius: 150.0,
    child: Image.asset('images/photo.png'),
  ),
)
```

## Hero 与显式 Hero

### 隐式 Hero（默认）

直接使用 `Hero` widget，Flutter 自动处理动画：

```dart
Hero(
  tag: 'my-hero',
  child: Image.network('https://example.com/image.png'),
)
```

### 显式 Hero

显式定义 `createRectTween` 以自定义飞行路径：

```dart
Hero(
  tag: 'my-hero',
  createRectTween: (Rect? begin, Rect? end) {
    return MaterialRectCenterArcTween(begin: begin, end: end);
  },
  child: /* ... */,
)
```

## 关键 API

| 属性 | 说明 |
|------|------|
| `tag` | 标识 Hero 的唯一标签，两页面间相同 tag 的 Hero 形成配对 |
| `flightShuttleBuilder` | 自定义飞行过程中的 widget 外观 |
| `createRectTween` | 自定义 RectTween 控制飞行路径 |
| `child` | Hero 包含的内容 widget |

## 调试技巧

使用 `timeDilation` 减慢动画便于调试：

```dart
// 在 build 方法中
timeDilation = 5.0; // 1.0 为正常速度

// 或使用 debugPaintSizeEnabled 可视化布局
// Flutter Inspector 中启用
```
